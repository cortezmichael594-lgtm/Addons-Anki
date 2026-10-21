"""Lectura de la actividad de estudio y calculo de las cifras del mapa.

Todo lo de aqui son lecturas: se cuentan repasos por dia y tarjetas por dia de
vencimiento, y nunca se escribe nada en la coleccion. Las consultas son de
agregacion (un unico group by por concepto), no una consulta por tarjeta, para
que una coleccion de cientos de miles de tarjetas siga dibujando el mapa en
una fraccion de segundo.

Se lee la base de datos directamente porque Anki no ofrece ninguna funcion
publica que devuelva la actividad por dia (y su servicio interno de
estadisticas no da las tarjetas distintas). Solo se hacen consultas de lectura.

Los criterios se han igualado a los de las estadisticas del propio Anki, para
que los numeros del mapa coincidan con los que la persona ve en la pantalla de
estadisticas:

  * Repasos por dia: se cuenta todo salvo los movimientos manuales de fecha
    (type 4) y las reprogramaciones (type 5), igual que el grafico Calendario.
  * Retencion: tasa de acierto de las tarjetas con intervalo de un dia o mas,
    excluyendo los repasos de mazo filtrado sin reprogramar, con el mismo
    criterio que la Retencion real de Anki. El periodo es la ventana del
    promedio elegida por la persona (decision del cliente, 2026-10-08).

El color puede medir tres cosas (MEASURES): repasos (cada respuesta cuenta
una), tarjetas distintas respondidas ese dia, o nuevas (tarjetas distintas que
se empezaron a estudiar ese dia). La medida en minutos se retiro el
2026-10-08 a peticion del cliente: hay dias con cientos de repasos guardados
sin tiempo y la cifra resultaba incoherente.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-27, restablecida 2026-10-08) — La comparativa semanal
#                        enfrentaba lo que va de semana con la semana natural
#                        anterior completa. El cliente la retiro el 2026-07-27
#                        y la pidio de nuevo el 2026-10-08.
# FIX-002 (2026-07-27) — La retencion mostraba 0% cuando no habia ningun
#                        repaso que pudiera contar.
# FIX-003 (2026-10-08) — Las tarjetas prestadas a un mazo filtrado faltaban en
#                        la prevision de su dia de vencimiento.
# FIX-004 (2026-10-08) — El historial de las tarjetas borradas contaba o no en
#                        el mapa general segun hubiera mazos excluidos.
# FIX-010 (2026-10-08) — El promedio diario mostraba 0 cuando la ventana no
#                        tenia ningun dia completo estudiado.
# FIX-011 (2026-10-13) — La medida «Nuevas» daba 0 en todo el historial
#                        anterior al planificador v3.
# FIX-012 (2026-10-13) — Con la hora de cambio de dia a las 12 o mas tarde,
#                        cada cuadrito llevaba la fecha del dia siguiente.
# FIX-013 (2026-10-13) — En la pantalla de un mazo grande, el calculo tardaba
#                        segundos y Anki se quedaba esperando.

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

from anki.collection import Collection
from anki.dbproxy import DBProxy, Row

from .decks import DeckScope

MAX_FUTURE_DAYS = 36500
# Con menos repasos medibles la retencion no dice nada fiable y se escribe N/A.
RETENTION_MIN_REVIEWS = 20
WEEK_DAYS = 7

MEASURES: tuple[str, ...] = ("reviews", "cards", "new")
# Ventanas del promedio (y de los dias estudiados y la retencion), en dias;
# 0 significa todo el historial.
# 7 y 90 se retiraron el 2026-10-13 al poner los botones rapidos junto al ano
# (peticion del cliente); quien los tuviera guardados pasa al valor por defecto.
WINDOWS: tuple[int, ...] = (30, 365, 0)

# Referencia minima de la escala de colores, en la unidad de cada medida: asi
# quien empieza no ve el mapa oscurisimo con muy poco esfuerzo.
SCALE_MINIMUM: dict[str, float] = {"reviews": 20.0, "cards": 20.0, "new": 10.0}

# Entradas del registro que no son un repaso de verdad: mover una fecha a mano
# (type 4) y reprogramar (type 5).
_NOT_A_REVIEW = "type not in (4, 5)"

# Primera respuesta de una tarjeta nueva. Con el planificador v3 Anki la guarda
# como aprendizaje (type 0) con intervalo anterior 0 (lastIvl = 0); los pasos
# siguientes llevan un intervalo anterior negativo (segundos). Tras «Olvidar»,
# la tarjeta vuelve a ser nueva y su siguiente respuesta es otra vez type 0
# con lastIvl 0, igual que la cuenta Anki en su limite diario de nuevas.
# Comprobado con una coleccion de prueba en Anki 26.09.3 (2026-10-08).
# --- FIX-011 (2026-10-13) --------------------------------------
# Sintoma: con la medida «Nuevas», todos los dias anteriores al planificador
#          v3 salian en gris y el promedio decia «N/A».
# Causa: los planificadores v1 y v2 guardaban la primera respuesta con
#        lastIvl negativo (el primer paso, en segundos), nunca 0.
# Regla: una respuesta de aprendizaje empieza una tarjeta nueva si lleva
#        lastIvl 0 o si es la primera respuesta que tuvo esa tarjeta, el
#        mismo criterio que la busqueda introduced: de Anki. La subconsulta
#        mira solo el registro, asi que las tarjetas borradas siguen contando
#        (Regla de FIX-004).
# ---------------------------------------------------------------
_STARTS_NEW_CARD = (
    "type = 0 and ease > 0 and (lastIvl = 0 or id = "
    "(select min(r2.id) from revlog r2 where r2.cid = revlog.cid and r2.ease > 0))"
)

# Tramo de cada consulta al registro, en dias. Anki atiende una consulta cada
# vez: partir la lectura en tramos de un ano deja huecos entre ellos para lo
# que Anki necesite hacer mientras tanto (por ejemplo, empezar a estudiar).
_CHUNK_DAYS = 365
_MAX_CHUNKS = 60

# Definicion literal de "repaso que cuenta para la retencion" en Anki, tal como
# la aplica su pantalla de estadisticas (fila Ultimo mes, columna Todas):
#
#   * ease > 0: se pulso un boton de respuesta. Deja fuera los movimientos de
#     fecha y los reinicios, que no son respuestas de la persona.
#   * no (type = 3 y factor = 0): deja fuera la practica en un mazo filtrado
#     con la reprogramacion desactivada, porque no afecta a la programacion.
#   * type = 1 o lastIvl >= 1 o lastIvl <= -86400: la tarjeta llevaba al menos
#     un dia de intervalo. lastIvl esta en dias cuando es positivo y en
#     segundos negados cuando es negativo, de ahi los dos limites; asi quedan
#     fuera los pasos de aprendizaje de minutos, que inflarian el porcentaje.
#
# Se acierta = se pulso cualquier boton que no sea "Otra vez" (ease > 1).
_RETENTION_REVIEW = (
    "ease > 0 and not (type = 3 and factor = 0)"
    " and (type = 1 or lastIvl <= -86400 or lastIvl >= 1)"
)


@dataclass(frozen=True)
class DayActivity:
    """Lo que se hizo un dia concreto."""

    reviews: int
    cards: int
    # Tarjetas distintas que se empezaron a estudiar ese dia (nuevas).
    new: int = 0


@dataclass(frozen=True)
class HeatmapData:
    # Clave: dias hacia atras desde hoy (0 = hoy). Solo dias con repasos.
    past: dict[int, DayActivity]
    # Clave: dias hacia delante (1 = manana). Tarjetas que vencen ese dia.
    future_counts: dict[int, int]
    today: date
    # Clave: dias hacia atras. Valor: (repasos medibles para la retencion,
    # de ellos acertados). Solo dias con algun repaso medible.
    retention_days: dict[int, tuple[int, int]] = field(default_factory=dict)
    # El mapa es el de un mazo que esta entre los excluidos.
    deck_excluded: bool = False
    # Tarjetas que aun vencen hoy en lo que cuenta el mapa (meta «Terminar lo
    # de hoy», 4.0.0); None si no se calculo.
    due_remaining: int | None = None
    # Retencion deseada de FSRS del mazo (0-1), solo en la pantalla de un mazo
    # con FSRS activado; None en los demas casos.
    fsrs_target: float | None = None


@dataclass(frozen=True)
class FullStats:
    # Promedio diario en la unidad de la medida; None si la ventana no tiene
    # ningun dia completo estudiado (no es lo mismo que cero, ver FIX-010).
    average: float | None
    studied_pct: int
    # None cuando no hay repasos suficientes para la retencion.
    # No es lo mismo que cero: cero significaria haber fallado todo.
    retention: int | None
    retention_reviews: int
    current_streak: int
    longest_streak: int
    # Dias desde el ultimo repaso; None si nunca se ha estudiado.
    last_session: int | None
    # Si hoy ya cuenta para la racha (version 3.6.0).
    today_done: bool = False
    # La racha mas larga sin contar la actual: sirve para saber si la actual
    # acaba de batir el record.
    previous_best: int = 0
    # Comodines guardados ahora mismo (4.0.0).
    freezes_left: int = 0
    # Dias perdonados (dias atras -> "freeze" o "pause"), para el mapa.
    forgiven: dict[int, str] = field(default_factory=dict)


@dataclass(frozen=True)
class StreakState:
    """Racha con comodines y pausa (4.0.0)."""

    current: int
    longest: int
    previous_best: int
    today_done: bool
    freezes_left: int
    forgiven: dict[int, str]


# Comodines: uno por cada 7 dias seguidos estudiados, dos guardados como
# maximo (informe de rediseno 4.0, apartado 7.2).
FREEZE_EVERY = 7
MAX_FREEZES = 2


def round_half_up(value: float) -> int:
    """Redondeo escolar (2,5 -> 3), no el bancario de round()."""
    magnitude = int(math.floor(abs(value) + 0.5))
    return magnitude if value >= 0 else -magnitude


def _id_list(deck_ids: tuple[int, ...]) -> str:
    if not deck_ids:
        # Lista vacia: ningun mazo coincide (mejor que un IN vacio, que no
        # todos los motores aceptan igual).
        return "(-1)"
    return "(" + ",".join(str(deck_id) for deck_id in deck_ids) + ")"


def cards_deck_filter(scope: DeckScope) -> str:
    """Condicion SQL sobre la tabla cards.

    Se mira tambien odid porque una tarjeta que esta ahora mismo dentro de un
    mazo filtrado conserva su mazo de origen ahi: sin esa comprobacion, el
    mapa de un mazo se vaciaria en cuanto se creara un mazo filtrado.
    """
    parts: list[str] = []
    if scope.include_ids is not None:
        ids = _id_list(scope.include_ids)
        parts.append(f" and (did in {ids} or odid in {ids})")
    if scope.exclude_ids:
        ids = _id_list(scope.exclude_ids)
        parts.append(f" and did not in {ids} and odid not in {ids}")
    return "".join(parts)


def revlog_deck_filter(scope: DeckScope) -> str:
    """La misma condicion, aplicada al registro de repasos por su tarjeta."""
    # --- FIX-004 (2026-10-08) --------------------------------------
    # Sintoma: el historial de las tarjetas borradas contaba en el mapa general
    #          mientras no hubiera mazos excluidos y desaparecia en cuanto se
    #          excluia cualquier mazo.
    # Causa: con exclusiones, el filtro exigia que la tarjeta siguiera
    #        existiendo ("cid in cards no excluidas"), y una tarjeta borrada ya
    #        no esta en cards.
    # Regla: las exclusiones quitan lo excluido ("cid not in cards excluidas"),
    #        nunca exigen que la tarjeta exista. Por decision del cliente
    #        (2026-10-08) las borradas cuentan siempre en el mapa general; en
    #        el de un mazo no pueden contar porque ya no tienen mazo.
    # ---------------------------------------------------------------
    # --- FIX-013 (2026-10-13) --------------------------------------
    # Sintoma: en la pantalla de un mazo con casi todas las tarjetas, el mapa
    #          tardaba segundos y, mientras, Anki no respondia al pulsar
    #          «Estudiar ahora».
    # Causa: con «cid in (...)» SQLite buscaba en el indice una vez por cada
    #        tarjeta del mazo, mucho mas lento que leer el registro de corrido.
    # Regla: la condicion de inclusion se escribe «+cid in (...)», para que el
    #        peor caso sea una lectura seguida, como el mapa general.
    # ---------------------------------------------------------------
    parts: list[str] = []
    if scope.include_ids is not None:
        ids = _id_list(scope.include_ids)
        parts.append(f" and +cid in (select id from cards where did in {ids} or odid in {ids})")
    if scope.exclude_ids:
        ids = _id_list(scope.exclude_ids)
        parts.append(f" and cid not in (select id from cards where did in {ids} or odid in {ids})")
    return "".join(parts)


def anki_today(cutoff_seconds: int, utc_offset: timedelta | None = None) -> date:
    """Dia de hoy segun el calendario de Anki.

    day_cutoff es el instante en que empieza el dia siguiente, a la hora de
    cambio de dia configurada y con el desfase horario de este momento. Se
    lee con ese mismo desfase y se resta un dia.
    """
    # --- FIX-012 (2026-10-13) --------------------------------------
    # Sintoma: con la hora de cambio de dia a las 12 o mas tarde, cada
    #          cuadrito llevaba la fecha del dia siguiente, el borde de hoy
    #          caia en manana y la cuenta atras de las fechas clave se quedaba
    #          corta en un dia.
    # Causa: se restaban doce horas al corte, y eso solo cae dentro del dia
    #        actual cuando la hora de cambio es anterior a mediodia.
    # Regla: el dia de Anki se calcula con aritmetica de calendario: fecha
    #        local del corte, con el desfase con que Anki lo calcula, menos un
    #        dia. Vale para las 24 horas de cambio y los cambios de horario.
    # ---------------------------------------------------------------
    if utc_offset is None:
        utc_offset = datetime.now().astimezone().utcoffset() or timedelta(0)
    cutoff = datetime.fromtimestamp(cutoff_seconds, timezone(utc_offset))
    return cutoff.date() - timedelta(days=1)


def _db(col: Collection) -> DBProxy:
    db = col.db
    if db is None:
        raise RuntimeError("La coleccion esta cerrada.")
    return db


def _rows_by_day(
    db: DBProxy, columns: str, condition: str, cutoff_seconds: int
) -> list[Row]:
    """Filas agrupadas por dia (dias hacia atras desde hoy), por tramos.

    Cada tramo abarca _CHUNK_DAYS dias completos del calendario de Anki, asi
    que un dia nunca queda repartido entre dos tramos y los recuentos de
    tarjetas distintas salen igual que con una sola consulta.
    """
    oldest = db.scalar("select min(id) from revlog")
    if oldest is None:
        return []
    rows: list[Row] = []
    high = cutoff_seconds
    chunks = 0
    while high * 1000 > int(oldest):
        chunks += 1
        # Un registro con fechas imposibles (siglos atras) no debe alargar el
        # bucle: pasado el limite, lo que quede se lee de una vez.
        low = high - _CHUNK_DAYS * 86400 if chunks < _MAX_CHUNKS else int(oldest) // 1000 - 1
        rows.extend(
            db.all(
                f"select (? - 1 - id / 1000) / 86400 as days_ago, {columns}"
                f" from revlog where {condition} and id >= ? and id < ?"
                " group by days_ago",
                cutoff_seconds,
                low * 1000,
                high * 1000,
            )
        )
        high = low
    return rows


def fetch_data(col: Collection, scope: DeckScope, measure: str = "reviews") -> HeatmapData:
    """Actividad por dia, vencimientos y repasos medibles para la retencion.

    Solo se cuentan las tarjetas distintas que pide la medida: es la parte
    mas costosa de la consulta y la medida por defecto (repasos) no la usa.
    """
    db = _db(col)
    cutoff_seconds = int(col.sched.day_cutoff)
    today = anki_today(cutoff_seconds)
    if scope.current_excluded:
        return HeatmapData(past={}, future_counts={}, today=today, deck_excluded=True)
    revlog_filter = revlog_deck_filter(scope)
    cards_filter = cards_deck_filter(scope)

    # Las nuevas se cuentan como tarjetas distintas, no como filas del registro.
    if measure == "cards":
        extra = "count(distinct cid)"
    elif measure == "new":
        extra = f"count(distinct case when {_STARTS_NEW_CARD} then cid end)"
    else:
        extra = "0"
    past: dict[int, DayActivity] = {}
    for row in _rows_by_day(
        db, f"count(*), {extra}", _NOT_A_REVIEW + revlog_filter, cutoff_seconds
    ):
        days_ago = int(row[0])
        if days_ago < 0:
            continue
        reviews, counted = int(row[1]), int(row[2])
        past[days_ago] = DayActivity(
            reviews=reviews,
            cards=counted if measure == "cards" else 0,
            new=counted if measure == "new" else 0,
        )

    # --- FIX-003 (2026-10-08) --------------------------------------
    # Sintoma: una tarjeta prestada a un mazo filtrado no contaba en el cuadrito
    #          gris de su dia de vencimiento, aunque Explorar si la encontraba.
    # Causa: dentro de un mazo filtrado Anki guarda en due una posicion de orden
    #        y deja la fecha real en odue; se leia siempre due.
    # Regla: para saber cuando vence una tarjeta se usa odue si esta en un mazo
    #        filtrado (odid distinto de 0) y due en caso contrario, igual que
    #        hace la busqueda prop:due de Anki.
    # ---------------------------------------------------------------
    today_index = int(col.sched.today)
    future_rows = db.all(
        "select (case when odid != 0 then odue else due end) - ? as days_ahead, count(*)"
        " from cards where queue in (2, 3)" + cards_filter + " group by days_ahead",
        today_index,
    )
    future_counts: dict[int, int] = {}
    for row in future_rows:
        # Solo desde manana: lo de hoy y lo atrasado no se dibuja en ningun
        # cuadrito (el de hoy muestra lo ya estudiado).
        days_ahead = int(row[0])
        if 1 <= days_ahead <= MAX_FUTURE_DAYS:
            future_counts[days_ahead] = future_counts.get(days_ahead, 0) + int(row[1])

    # Repasos medibles para la retencion, dia a dia: asi la ventana se elige
    # despues sin volver a consultar. El limite superior (final de hoy) deja
    # fuera las marcas de tiempo futuras (reloj desajustado o coleccion
    # importada).
    retention_rows = _rows_by_day(
        db,
        "count(*), coalesce(sum(ease > 1), 0)",
        _RETENTION_REVIEW + revlog_filter,
        cutoff_seconds,
    )
    retention_days: dict[int, tuple[int, int]] = {}
    for row in retention_rows:
        days_ago = int(row[0])
        if days_ago >= 0:
            retention_days[days_ago] = (int(row[1]), int(row[2]))

    return HeatmapData(
        past=past,
        future_counts=future_counts,
        today=today,
        retention_days=retention_days,
    )


def days_offset(col: Collection, day: date) -> int:
    """Distancia en dias entre un dia del mapa y hoy (positiva hacia el pasado)."""
    return (anki_today(int(col.sched.day_cutoff)) - day).days


# Medidas
# ---------------------------------------------------------------------------


def is_active(day: DayActivity, measure: str) -> bool:
    """Si el dia cuenta como estudiado en la medida elegida.

    Con «Nuevas», solo los dias en que se empezo alguna tarjeta nueva; con
    repasos y tarjetas, cualquier dia con repasos (peticion del cliente,
    2026-10-13: todas las cifras siguen la medida).
    """
    if measure == "new":
        return day.new > 0
    return day.reviews > 0


def active_days(data: "HeatmapData", measure: str) -> set[int]:
    return {days_ago for days_ago, day in data.past.items() if is_active(day, measure)}


def measure_value(day: DayActivity, measure: str) -> float:
    """Cantidad de un dia en la unidad de la medida."""
    if measure == "cards":
        return float(day.cards)
    if measure == "new":
        return float(day.new)
    return float(day.reviews)


def _window_end(days_ago: Iterable[int], window: int) -> int:
    """Ultimo dia (hacia atras) que abarca la ventana; 0 = todo el historial."""
    if window > 0:
        return window
    return max(days_ago, default=0)


def scale_reference(data: HeatmapData, measure: str) -> float:
    """Referencia de la escala de colores.

    Promedio de todo el historial en la medida elegida, contando solo los dias
    con estudio. No depende de la ventana del promedio, para que los colores
    de los meses pasados no cambien al cambiar esa opcion.
    """
    values = [measure_value(day, measure) for day in data.past.values() if is_active(day, measure)]
    average = sum(values) / len(values) if values else 0.0
    return max(SCALE_MINIMUM.get(measure, SCALE_MINIMUM["reviews"]), average)


def window_average(data: HeatmapData, measure: str, window: int) -> float | None:
    """Promedio diario de la ventana elegida.

    Solo dias completos: la ventana termina ayer, para que la cifra no baje
    cada manana antes de haber podido estudiar. Divide solo entre los dias con
    estudio.
    """
    last = _window_end(data.past, window)
    values = [
        measure_value(day, measure)
        for days_ago, day in data.past.items()
        if 1 <= days_ago <= last and is_active(day, measure)
    ]
    # --- FIX-010 (2026-10-08) --------------------------------------
    # Sintoma: con la ventana sin ningun dia completo estudiado (por ejemplo,
    #          si el unico dia estudiado es hoy), el promedio decia «0 repasos».
    # Causa: sin dias que promediar no se puede dividir, y se devolvia 0 en su
    #        lugar; pero un dia estudiado tiene al menos un repaso, asi que un
    #        promedio de dias estudiados nunca puede ser 0.
    # Regla: "no hay datos" y "cero" son cosas distintas (como en FIX-002): sin
    #        dias que promediar se devuelve None y la pantalla escribe "N/A".
    # ---------------------------------------------------------------
    return sum(values) / len(values) if values else None


def window_retention(data: HeatmapData, window: int) -> tuple[int, int]:
    """Repasos medibles y acertados dentro de la ventana elegida.

    Misma ventana que el promedio: dias completos que terminan ayer, asi la
    cifra no cambia a lo largo del dia (decision del cliente, 2026-10-08: la
    retencion sigue la ventana del promedio).
    """
    last = _window_end(data.retention_days, window)
    total = passed = 0
    for days_ago, (day_total, day_passed) in data.retention_days.items():
        if 1 <= days_ago <= last:
            total += day_total
            passed += day_passed
    return total, passed


def studied_fraction(data: HeatmapData, window: int, measure: str = "reviews") -> tuple[int, int]:
    """Dias estudiados y dias de la ventana (los de studied_pct, sin dividir)."""
    active = active_days(data, measure)
    if not active:
        return 0, 0
    start, end = _study_span(active, window)
    return sum(1 for days_ago in active if start <= days_ago <= end), end - start + 1


def _study_span(active: set[int], window: int) -> tuple[int, int]:
    """Primer y ultimo dia (contando hacia atras) de la ventana de estudio."""
    start = 0 if 0 in active else 1
    oldest = max(active)
    end = start + window - 1 if window > 0 else oldest
    return start, min(end, oldest)


def studied_pct(data: HeatmapData, window: int, measure: str = "reviews") -> int:
    """Porcentaje de dias con estudio dentro de la ventana.

    Si hoy ya hay repasos, la ventana son los N dias que terminan hoy; si no,
    los N que terminan ayer: hoy no cuenta como dia sin estudio antes de haber
    tenido ocasion de estudiar. La ventana nunca empieza antes del primer
    repaso, porque los dias anteriores a usar Anki no son dias sin estudio.
    """
    studied, span = studied_fraction(data, window, measure)
    return round_half_up(100 * studied / span) if span else 0


# FIX-001 restablecida: lee su nota antes de cambiar esta funcion.
def week_diff(data: HeatmapData, measure: str) -> tuple[float, bool]:
    """Diferencia entre los 7 ultimos dias completos y los 7 anteriores.

    Devuelve tambien si en los 7 dias anteriores se estudio: sin nada con lo
    que comparar, la cifra no significa nada y no se ensena. Con repasos y
    tarjetas es lo mismo que mirar la medida; con nuevas, una semana estudiada
    sin ninguna nueva si sirve para comparar («▲ 15 nuevas»).
    """
    # --- FIX-001 (2026-10-08) --------------------------------------
    # Sintoma: la comparativa salia muy negativa los lunes y subia a lo largo
    #          de la semana sin que cambiara el ritmo de estudio.
    # Causa: comparaba lo que iba de semana (de lunes a hoy) con la semana
    #        natural anterior completa: dos periodos de distinta longitud, uno
    #        de ellos a medias.
    # Regla: se comparan siempre dos periodos iguales y completos: los 7 dias
    #        que terminan ayer contra los 7 anteriores. Hoy no entra, asi que la
    #        cifra no cambia a lo largo del dia. Lo pidio el cliente el
    #        2026-10-08 y sustituye a la decision del 2026-07-27.
    # ---------------------------------------------------------------
    recent, previous, studied_before = week_totals(data, measure)
    return recent - previous, studied_before


def week_totals(data: HeatmapData, measure: str) -> tuple[float, float, bool]:
    """Lo hecho en los 7 ultimos dias completos y en los 7 anteriores.

    Mismos periodos que week_diff (Regla de FIX-001): terminan ayer. Devuelve
    tambien si en los 7 anteriores se estudio. La comparativa de la 3.6.0
    ensena el total junto a la diferencia, para que la cifra tenga su punto
    de referencia.
    """

    def total(first: int, last: int) -> float:
        return sum(
            measure_value(data.past[days_ago], measure)
            for days_ago in range(first, last + 1)
            if days_ago in data.past
        )

    studied_before = any(
        data.past[days_ago].reviews > 0
        for days_ago in range(WEEK_DAYS + 1, 2 * WEEK_DAYS + 1)
        if days_ago in data.past
    )
    return total(1, WEEK_DAYS), total(WEEK_DAYS + 1, 2 * WEEK_DAYS), studied_before


def streaks(studied_days_ago: set[int]) -> tuple[int, int]:
    current = 0
    # La racha actual no se rompe por no haber estudiado todavia hoy.
    cursor = 0 if 0 in studied_days_ago else 1
    while cursor in studied_days_ago:
        current += 1
        cursor += 1
    longest = 0
    run = 0
    previous: int | None = None
    for day in sorted(studied_days_ago):
        run = run + 1 if previous is not None and day == previous + 1 else 1
        longest = max(longest, run)
        previous = day
    return current, longest


def streak_state(
    studied_days_ago: set[int], use_freezes: bool, paused: frozenset[int] = frozenset()
) -> StreakState:
    """Racha dia a dia, del primer dia estudiado a hoy (4.0.0).

    * Un dia estudiado suma uno; cada 7 seguidos ganan un comodin (hasta 2).
    * Un dia sin estudiar dentro de una pausa ni suma ni rompe.
    * Un dia sin estudiar fuera de pausa gasta un comodin si hay (la racha
      ni suma ni se rompe); si no hay, la racha vuelve a cero.
    * Hoy sin estudiar todavia no rompe nada: queda pendiente.

    Sin comodines ni pausas da lo mismo que streaks().
    """
    if not studied_days_ago:
        return StreakState(0, 0, 0, False, 0, {})
    run = 0
    best_closed = 0
    freezes = 0
    forgiven: dict[int, str] = {}

    def add_day() -> None:
        nonlocal run, freezes
        run += 1
        if use_freezes and run % FREEZE_EVERY == 0 and freezes < MAX_FREEZES:
            freezes += 1

    for days_ago in range(max(studied_days_ago), 0, -1):
        if days_ago in studied_days_ago:
            add_day()
        elif run == 0:
            continue
        elif days_ago in paused:
            forgiven[days_ago] = "pause"
        elif use_freezes and freezes > 0:
            freezes -= 1
            forgiven[days_ago] = "freeze"
        else:
            best_closed = max(best_closed, run)
            run = 0
    today_done = 0 in studied_days_ago
    if today_done:
        add_day()
    return StreakState(run, max(best_closed, run), best_closed, today_done, freezes, forgiven)


def paused_days(pause: tuple[date, date] | None, today: date) -> frozenset[int]:
    """Dias de la pausa, contados hacia atras desde hoy (solo los pasados)."""
    if pause is None:
        return frozenset()
    start, end = pause
    return frozenset(
        (today - start).days - offset
        for offset in range((end - start).days + 1)
        if (today - start).days - offset > 0
    )


def surprise(data: HeatmapData, measure: str, stats: FullStats) -> tuple[str, int] | None:
    """Una sorpresa verdadera de hoy, como mucho una (4.0.0, informe ap. 8).

    Solo cuando ocurre y con datos reales, por este orden: nueva racha mas
    larga, mejor dia del ano, mes completo y una cifra redonda del ano
    (100, 500 y cada 1.000). Devuelve la clave y la cifra, o None.
    """
    today_day = data.past.get(0)
    if not stats.today_done or today_day is None:
        return None
    if stats.previous_best >= 1 and stats.current_streak == stats.previous_best + 1:
        return "record", 0
    today_value = measure_value(today_day, measure)
    year = data.today.year
    others = [
        measure_value(day, measure)
        for days_ago, day in data.past.items()
        if days_ago > 0 and (data.today - timedelta(days=days_ago)).year == year and is_active(day, measure)
    ]
    if len(others) >= WEEK_DAYS and today_value > max(others):
        return "best_day", 0
    month_days = range(data.today.day)
    if (data.today + timedelta(days=1)).month != data.today.month and all(
        d in data.past and is_active(data.past[d], measure) for d in month_days
    ):
        return "month", 0
    total = sum(others) + today_value
    before = total - today_value
    milestone = int(total // 1000) * 1000 if total >= 1000 else (500 if total >= 500 else 100)
    if before < milestone <= total:
        return "year_total", milestone
    return None


def previous_best(studied_days_ago: set[int], current: int) -> int:
    """La racha mas larga sin contar la actual (cero si no hay otra)."""
    start = 0 if 0 in studied_days_ago else 1
    current_run = set(range(start, start + current))
    _current, longest = streaks(studied_days_ago - current_run)
    return longest


def full_stats(
    data: HeatmapData,
    measure: str = "reviews",
    window: int = 30,
    use_freezes: bool = False,
    paused: frozenset[int] = frozenset(),
) -> FullStats:
    studied_days = active_days(data, measure)
    streak = streak_state(studied_days, use_freezes, paused)
    # --- FIX-002 (2026-07-27) --------------------------------------
    # Sintoma: la retencion aparecia como 0%, como si se hubiera fallado todo,
    #          en cuentas recien empezadas o que solo tienen tarjetas nuevas.
    # Causa: si ningun repaso cumple los requisitos de la retencion (hace falta
    #        que la tarjeta llevara al menos un dia de intervalo), el total es
    #        cero y la division se sustituia por un 0 sin mas.
    # Regla: "no hay datos" y "cero" son cosas distintas. Cuando no hay nada que
    #        medir se devuelve None y la pantalla escribe "N/A", que es lo mismo
    #        que hace Anki en su tabla de retencion.
    # ---------------------------------------------------------------
    # Desde 2026-10-08, "nada que medir" incluye tener menos de
    # RETENTION_MIN_REVIEWS repasos medibles: con tan pocos, el porcentaje
    # no es fiable. El periodo es la ventana del promedio.
    total_reviews, passed_reviews = window_retention(data, window)
    retention = (
        round_half_up(100 * passed_reviews / total_reviews)
        if total_reviews >= RETENTION_MIN_REVIEWS
        else None
    )
    return FullStats(
        average=window_average(data, measure, window),
        studied_pct=studied_pct(data, window, measure),
        retention=retention,
        retention_reviews=total_reviews,
        current_streak=streak.current,
        longest_streak=streak.longest,
        last_session=min(studied_days) if studied_days else None,
        today_done=streak.today_done,
        previous_best=streak.previous_best,
        freezes_left=streak.freezes_left,
        forgiven=streak.forgiven,
    )


def year_bounds(data: HeatmapData, extra_dates: tuple[date, ...] = ()) -> tuple[int, int]:
    min_year = (
        (data.today - timedelta(days=max(data.past))).year
        if data.past
        else data.today.year
    )
    max_year = (
        (data.today + timedelta(days=max(data.future_counts))).year
        if data.future_counts
        else data.today.year
    )
    for extra in extra_dates:
        min_year = min(min_year, extra.year)
        max_year = max(max_year, extra.year)
    return min(min_year, data.today.year), max(max_year, data.today.year)
