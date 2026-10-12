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

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta

from anki.collection import Collection
from anki.dbproxy import DBProxy

from .decks import DeckScope

MAX_FUTURE_DAYS = 36500
# Con menos repasos medibles la retencion no dice nada fiable y se escribe N/A.
RETENTION_MIN_REVIEWS = 20
WEEK_DAYS = 7

MEASURES: tuple[str, ...] = ("reviews", "cards", "new")
# Ventanas del promedio (y de los dias estudiados y la retencion), en dias;
# 0 significa todo el historial.
WINDOWS: tuple[int, ...] = (7, 30, 90, 365, 0)

# Referencia minima de la escala de colores, en la unidad de cada medida: asi
# quien empieza no ve el mapa oscurisimo con muy poco esfuerzo.
SCALE_MINIMUM: dict[str, float] = {"reviews": 20.0, "cards": 20.0, "new": 10.0}

# Entradas del registro que no son un repaso de verdad: mover una fecha a mano
# (type 4) y reprogramar (type 5).
_NOT_A_REVIEW = "type not in (4, 5)"

# Primera respuesta de una tarjeta nueva: Anki la guarda como aprendizaje
# (type 0) con intervalo anterior 0 (lastIvl = 0); los pasos siguientes llevan
# un intervalo anterior negativo (segundos). Tras «Olvidar», la tarjeta vuelve
# a ser nueva y su siguiente respuesta es otra vez type 0 con lastIvl 0, igual
# que la cuenta Anki en su limite diario de nuevas. Comprobado con una
# coleccion de prueba en Anki 26.09.3 (2026-10-08).
_STARTS_NEW_CARD = "type = 0 and lastIvl = 0 and ease > 0"

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
    parts: list[str] = []
    if scope.include_ids is not None:
        ids = _id_list(scope.include_ids)
        parts.append(f" and cid in (select id from cards where did in {ids} or odid in {ids})")
    if scope.exclude_ids:
        ids = _id_list(scope.exclude_ids)
        parts.append(f" and cid not in (select id from cards where did in {ids} or odid in {ids})")
    return "".join(parts)


def anki_today(cutoff_seconds: int) -> date:
    """Dia de hoy segun el calendario de Anki.

    day_cutoff es el instante en que empieza el dia siguiente (a la hora de
    reinicio configurada). Retroceder doce horas cae siempre dentro del dia
    actual, sea cual sea esa hora.
    """
    return date.fromtimestamp(cutoff_seconds - 43200)


def _db(col: Collection) -> DBProxy:
    db = col.db
    if db is None:
        raise RuntimeError("La coleccion esta cerrada.")
    return db


def fetch_data(col: Collection, scope: DeckScope) -> HeatmapData:
    db = _db(col)
    cutoff_seconds = int(col.sched.day_cutoff)
    today = anki_today(cutoff_seconds)
    revlog_filter = revlog_deck_filter(scope)
    cards_filter = cards_deck_filter(scope)

    # Una sola pasada por el registro da las tres medidas de cada dia. Las
    # nuevas se cuentan como tarjetas distintas, no como filas del registro.
    past_rows = db.all(
        "select (? - 1 - id / 1000) / 86400 as days_ago, count(*), count(distinct cid),"
        f" count(distinct case when {_STARTS_NEW_CARD} then cid end)"
        f" from revlog where {_NOT_A_REVIEW} and id < ?" + revlog_filter + " group by days_ago",
        cutoff_seconds,
        cutoff_seconds * 1000,
    )
    past: dict[int, DayActivity] = {}
    for row in past_rows:
        days_ago = int(row[0])
        if days_ago >= 0:
            past[days_ago] = DayActivity(
                reviews=int(row[1]), cards=int(row[2]), new=int(row[3])
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
    retention_rows = db.all(
        "select (? - 1 - id / 1000) / 86400 as days_ago, count(*), coalesce(sum(ease > 1), 0)"
        f" from revlog where {_RETENTION_REVIEW} and id < ?" + revlog_filter
        + " group by days_ago",
        cutoff_seconds,
        cutoff_seconds * 1000,
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
    values = [measure_value(day, measure) for day in data.past.values() if day.reviews > 0]
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
        if 1 <= days_ago <= last and day.reviews > 0
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


def studied_pct(data: HeatmapData, window: int) -> int:
    """Porcentaje de dias con estudio dentro de la ventana.

    Si hoy ya hay repasos, la ventana son los N dias que terminan hoy; si no,
    los N que terminan ayer: hoy no cuenta como dia sin estudio antes de haber
    tenido ocasion de estudiar. La ventana nunca empieza antes del primer
    repaso, porque los dias anteriores a usar Anki no son dias sin estudio.
    """
    active = {days_ago for days_ago, day in data.past.items() if day.reviews > 0}
    if not active:
        return 0
    start = 0 if 0 in active else 1
    oldest = max(active)
    end = start + window - 1 if window > 0 else oldest
    end = min(end, oldest)
    span = end - start + 1
    studied = sum(1 for days_ago in active if start <= days_ago <= end)
    return round_half_up(100 * studied / span)


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
    def total(first: int, last: int) -> float:
        return sum(
            measure_value(data.past[days_ago], measure)
            for days_ago in range(first, last + 1)
            if days_ago in data.past
        )

    recent = total(1, WEEK_DAYS)
    previous = total(WEEK_DAYS + 1, 2 * WEEK_DAYS)
    studied_before = any(
        data.past[days_ago].reviews > 0
        for days_ago in range(WEEK_DAYS + 1, 2 * WEEK_DAYS + 1)
        if days_ago in data.past
    )
    return recent - previous, studied_before


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


def full_stats(data: HeatmapData, measure: str = "reviews", window: int = 30) -> FullStats:
    studied_days = {days_ago for days_ago, day in data.past.items() if day.reviews > 0}
    current_streak, longest_streak = streaks(studied_days)
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
        studied_pct=studied_pct(data, window),
        retention=retention,
        retention_reviews=total_reviews,
        current_streak=current_streak,
        longest_streak=longest_streak,
        last_session=min(studied_days) if studied_days else None,
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
