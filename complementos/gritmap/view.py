"""Construccion del HTML del mapa y envio a la pagina de Anki.

El reparto de trabajo con la parte web es deliberado:

  * web/gritmap.css y web/gritmap.js se cargan una sola vez junto con la
    pagina, asi que no hay un instante en que el mapa se vea sin estilo.
  * La paleta de colores viaja en la cabecera de la pagina, porque es lo unico
    que depende de las opciones.
  * En cada dibujado solo se envia una llamada con los datos ya preparados.
    Antes se reenviaba en cada ocasion la hoja de estilos y todo el codigo de
    los detectores de eventos, que es lo que producia parpadeos.

Version 4.2.0 (correcciones del cliente del 2026-10-21): la tarjeta del mapa
(«Actividad») mide lo que piden sus cuadritos (tamano de celda y redondeo en
pixeles, como en las primeras versiones), centrada, y debajo van cinco
tarjetas pequenas (Hoy, Racha, Promedio diario, Retencion y Proxima fecha)
que suman el ancho del mapa.

Version 4.4.0 (peticion del cliente del 2026-10-21): de serie el mapa vuelve
a verse como en la 4.1.0, ajustado a todo el ancho de la tarjeta con las
esquinas apenas redondeadas. En la 4.5.0, un tamano fijo escala el dibujo
entero, con huecos y esquinas en proporcion.

Las cifras salen de aqui sin separadores de millares, envueltas en un
<span class="gritmap-n">, y los porcentajes en un <span class="gritmap-pct">:
el navegador los reescribe con el formato del idioma de Anki (Intl), que
conoce las costumbres de cada idioma. Los nombres de los meses y las fechas
de los globos tambien los pone el navegador.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-07-27) — La retencion mostraba 0% cuando no habia ningun
#                        repaso que pudiera contar.
# FIX-006 (2026-10-08) — El globo y el promedio decian "tarjetas" aunque
#                        contaban respuestas.
# FIX-008 (2026-10-08) — Lo que el mapa pone en la pagina de Anki usaba el
#                        prefijo "shm", que no es el nombre del paquete.
# FIX-010 (2026-10-08) — El promedio diario mostraba 0 cuando la ventana no
#                        tenia ningun dia completo estudiado.
# FIX-015 (2026-10-13) — El patron de archivos web dejaba que una tarjeta
#                        leyera archivos .css y .js de otros complementos.
# FIX-022 (2026-10-13) — En 13 idiomas, los dias, repasos, tarjetas y cuentas
#                        atras salian con la forma de plural equivocada.
# FIX-026 (2026-10-22) — La meta «Terminar lo de hoy», ya cumplida, volvia a
#                        «faltan 3» cuando vencian otra vez tarjetas en
#                        aprendizaje.
# FIX-031 (2026-10-27) — El ✓ de «✓ hoy» (Racha) no se veia igual que el de
#                        «✓ Meta cumplida» (Hoy).

from __future__ import annotations

import html
import json
import math
import re
from datetime import date, timedelta

from aqt import mw

from .config import FIT_WIDTH, Config, KeyDate
from .data import (
    DayActivity,
    FullStats,
    HeatmapData,
    full_stats,
    measure_value,
    paused_days,
    round_half_up,
    scale_reference,
    surprise,
    week_totals,
    year_bounds,
)
from .i18n import (
    PLURAL_CATEGORIES,
    anki_text,
    lang,
    locale_code,
    month_abbrev,
    plural_category,
    plural_form,
    plural_key,
    plural_text,
    t,
    unit_label,
)
from .palettes import due_thresholds, legend_thresholds, level_index, palette_css

# --- FIX-008 (2026-10-08) --------------------------------------
# Sintoma: los identificadores, clases, variables de color y ordenes del mapa
#          empezaban por "shm", un prefijo que podria usar otro complemento de
#          mapa de calor en la misma pagina.
# Causa: el prefijo venia de un nombre antiguo y no del nombre del paquete.
# Regla: todo lo que se inyecta en paginas de Anki (ids, clases, variables
#        CSS, atributos data-, ordenes pycmd) empieza por "gritmap".
# ---------------------------------------------------------------
MSG_PREFIX = "gritmap_"
ROOT_ID = "gritmap-root"
# Archivos de web/ que Anki sirve a la pagina (setWebExports, en controller).
# --- FIX-015 (2026-10-13) --------------------------------------
# Sintoma: con una ruta como web/..%2F..%2Fotro%2Fx.js, el JS de una tarjeta
#          podia leer archivos .css y .js de otros complementos.
# Causa: Anki compara el patron antes de resolver los «..», y «.*» los
#        aceptaba.
# Regla: el patron de setWebExports es cerrado: sin «/» ni «.» libres entre
#        la carpeta y la extension (APR-049).
# ---------------------------------------------------------------
WEB_PATTERN = r"web/[\w-]+\.(css|js)"

STYLE_ID = "gritmap-palette"

# Geometria del mapa, en unidades del dibujo, como en la 4.1.0: cuadrito de 14
# y hueco de 3. El dibujo se escala entero, asi que huecos y esquinas guardan
# siempre la proporcion (4.5.0, peticion del cliente): con «Ajustado al ancho»
# (el de serie) ocupa todo el ancho de la tarjeta, con 10 px por cuadrito como
# minimo (por debajo, se desplaza de lado); con un tamano, cada cuadrito mide
# esos pixeles.
_CELL = 14
_GAP = 3
_STEP = _CELL + _GAP
_FIT_MIN = 10
# La distancia al record solo se ensena si esta cerca (version 3.6.0): lejos,
# la cifra no anima y solo recuerda lo que falta.
_RECORD_GAP_MAX = 7
# ...y solo si el record significa algo: 7 dias o mas (4.7.0).
_RECORD_NEAR_MIN = 7
_TIP = '<div id="gritmap-tip" role="tooltip"></div>'


# Cifras y textos
# ---------------------------------------------------------------------------


def num_html(value: int) -> str:
    """Cifra que el navegador reescribe con el formato del idioma de Anki.

    La cifra sin separadores se queda como reserva por si el navegador no
    conociera el idioma. En espanol saldra 1.240 (con punto de millar).
    """
    number = int(value)
    return f'<span class="gritmap-n" data-n="{number}">{number}</span>'


def pct_html(value: int) -> str:
    """Porcentaje que el navegador escribe a la manera del idioma (85 %)."""
    number = int(value)
    return f'<span class="gritmap-pct" data-p="{number}">{number}%</span>'


def fill_html(key: str, **values: str) -> str:
    """Texto propio escapado, con los huecos rellenos de HTML ya preparado."""
    return _fill(t(key), values)


def fill_low(key: str, **values: str) -> str:
    """Como fill_html, pero empezando en minuscula (lt, 4.15.0)."""
    return _fill(lt(key), values)


def _fill(template: str, values: dict[str, str]) -> str:
    text = html.escape(template, quote=False)
    for name, value in values.items():
        text = text.replace("{" + name + "}", value)
    return text


# Textos que empiezan por un sustantivo en aleman, que alli se escribe
# siempre con mayuscula: lt no los toca (4.15.0).
_KEEP_CAPITAL: frozenset[tuple[str, str]] = frozenset({("de", "goal_done")})


def lt(key: str) -> str:
    """Texto propio en minuscula al empezar (4.15.0, peticion del cliente):
    las lineas grises de las tarjetas y el pie del mapa van siempre en
    minuscula, salvo donde la ortografia del idioma pide mayuscula (los
    sustantivos alemanes). Lo que escribe la persona (fechas clave, «Suelo
    estudiar») no pasa por aqui."""
    text = t(key)
    code = lang()
    if not text or (code, key) in _KEEP_CAPITAL:
        return text
    first = text[0]
    if code == "tr":
        # En turco, la I mayuscula sin punto es la ı minuscula.
        lowered = {"I": "ı", "İ": "i"}.get(first, first.lower())
    else:
        lowered = first.lower()
    return lowered + text[1:] if len(lowered) == 1 else text


# Separador «·» de las lineas grises (4.15.0, accesibilidad): se ve el punto
# medio y el lector de pantalla oye una pausa (coma) en lugar de «punto».
SEP = '<span aria-hidden="true"> · </span><span class="gritmap-sr">, </span>'


def unit_html(text: str) -> str:
    """Unidad de una cifra («repasos», «dias»): va mas pequena y en gris, para
    que destaque el numero."""
    return f'<span class="gritmap-unit">{html.escape(text)}</span>'


def unit_text(count: int, measure: str) -> str:
    """Unidad de la medida con la forma de plural que pide la cifra."""
    if measure == "new":
        return plural_text("unit_new", count)
    return unit_label(count, "card" if measure == "cards" else "review")


def count_html(count: int, measure: str) -> str:
    """Cantidad entera con su unidad: 85 repasos, 60 tarjetas, 8 nuevas."""
    return num_html(count) + " " + unit_html(unit_text(count, measure))


def countdown_html(days: int) -> str:
    """Cuenta atras de una fecha clave: nada si ya paso."""
    if days < 0:
        return ""
    if days == 0:
        return html.escape(t("kd_today"))
    return fill_html(plural_key("kd_left", days), count=num_html(days))


def _label(key: str) -> str:
    """Rotulo de una cifra sin los dos puntos finales («Retencion:»)."""
    return re.sub(r"[\s:：]+$", "", t(key))


def _days_html(count: int) -> str:
    return num_html(count) + " " + unit_html(unit_label(count, "day"))


def _not_available_html() -> str:
    """«N/A» con el texto del propio Anki, el mismo que usa la retencion."""
    return html.escape(anki_text("statistics_true_retention_not_applicable", "not_available"))


def _period_text(window: int) -> str:
    if window == 365:
        return html.escape(lt("period_year"))
    if window > 0:
        return fill_low("period_days", count=num_html(window))
    return html.escape(lt("period_all"))


# Iconos y botones
# ---------------------------------------------------------------------------


def _icon(kind: str) -> str:
    stroke = (
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round"'
        ' stroke-linejoin="round" fill="none"'
    )
    if kind == "left":
        body = f'<path d="M8.7 2.6 L4.6 7 L8.7 11.4" {stroke}/>'
    elif kind == "right":
        body = f'<path d="M5.3 2.6 L9.4 7 L5.3 11.4" {stroke}/>'
    elif kind == "chevron":
        body = f'<path d="M3 5.2 L7 9.2 L11 5.2" {stroke}/>'
    else:
        body = (
            f'<line x1="2.2" y1="3.8" x2="11.8" y2="3.8" {stroke}/>'
            f'<line x1="2.2" y1="7" x2="11.8" y2="7" {stroke}/>'
            f'<line x1="2.2" y1="10.2" x2="11.8" y2="10.2" {stroke}/>'
            '<circle cx="9.2" cy="3.8" r="1.7" fill="currentColor"/>'
            '<circle cx="4.8" cy="7" r="1.7" fill="currentColor"/>'
            '<circle cx="10" cy="10.2" r="1.7" fill="currentColor"/>'
        )
    return (
        '<svg width="12" height="12" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg"'
        f' aria-hidden="true" focusable="false">{body}</svg>'
    )


def _icon_button(cmd: str, label: str, icon_kind: str, disabled: bool = False, extra: str = "") -> str:
    """Boton con icono. Es un <button> real: se alcanza con el tabulador y un
    lector de pantalla lo anuncia."""
    safe_label = html.escape(label, quote=True)
    attrs = f' title="{safe_label}" aria-label="{safe_label}" data-gritmap-btn="{cmd}"{extra}'
    # Apagado con aria-disabled y no con disabled (4.7.0): un boton
    # desactivado del todo no recibe el raton y su nombre no saldria al pasar
    # por encima; el lector de pantalla lo anuncia como no disponible.
    attrs += ' aria-disabled="true"' if disabled else f' data-gritmap-cmd="{cmd}"'
    return f'<button type="button" class="gritmap-btn"{attrs}>{_icon(icon_kind)}</button>'


def _card(css: str, title: str, tools: str, body: str, subtitle: str = "", extra: str = "") -> str:
    """Tarjeta: titulo arriba a la izquierda, su control a la derecha, en la
    misma linea (Norman: el control junto a lo que controla)."""
    sub = f'<span class="gritmap-card-sub">{subtitle}</span>' if subtitle else ""
    if title:
        head = f'<div class="gritmap-card-head"><h3 class="gritmap-card-title">{html.escape(title)}{sub}</h3>'
    else:
        # Sin titulo (la tarjeta del mapa, 4.3.0): los botones, centrados.
        head = '<div class="gritmap-card-head gritmap-notitle">'
    return (
        f'<section class="gritmap-card {css}"{extra}>{head}'
        f'<div class="gritmap-card-tools">{tools}</div></div>'
        f'<div class="gritmap-card-body">{body}</div></section>'
    )


def _plain(html_text: str) -> str:
    """Texto de un trozo de HTML, sin etiquetas, para un title."""
    return html.unescape(re.sub(r"<[^>]+>", "", html_text))


def _mini(title: str, big: str, line: str, big_class: str = "") -> str:
    """Tarjeta pequena de la fila de resumen: titulo, dato grande y linea gris.

    La linea se ve siempre entera, en los renglones que necesite (4.15.0,
    accesibilidad: WCAG 1.4.10 y 1.4.12 piden que no se pierda texto, y sin
    globos lo cortado no se podia leer con el teclado ni en pantalla tactil).
    """
    cls = f"gritmap-big {big_class}".strip()
    return (
        '<section class="gritmap-card gritmap-mini">'
        f'<h3 class="gritmap-card-title">{html.escape(title)}</h3>'
        f'<div class="{cls}">{big}</div>'
        f'<div class="gritmap-line">{line or "&nbsp;"}</div></section>'
    )


def ring_svg(fraction: float, size: int) -> str:
    """Anillo de progreso: el nivel 4 del tema sobre el gris de pendientes
    (4.12.0). Solo se usa para «X de Y» (cada forma, un solo significado)."""
    stroke = 4 if size <= 32 else 6
    radius = (size - stroke) / 2
    length = 2 * math.pi * radius
    filled = max(0.0, min(1.0, fraction)) * length
    centre = size / 2
    return (
        f'<svg class="gritmap-ring" width="{size}" height="{size}" viewBox="0 0 {size} {size}"'
        ' aria-hidden="true" focusable="false">'
        f'<circle class="gritmap-ring-track" cx="{centre}" cy="{centre}" r="{radius:.2f}" stroke-width="{stroke}"/>'
        f'<circle class="gritmap-ring-fill" cx="{centre}" cy="{centre}" r="{radius:.2f}" stroke-width="{stroke}"'
        f' stroke-dasharray="{filled:.2f} {length:.2f}" transform="rotate(-90 {centre} {centre})"/>'
        "</svg>"
    )


# Fila de resumen
# ---------------------------------------------------------------------------


def _today_value(data: HeatmapData, measure: str) -> int:
    day = data.past.get(0)
    return int(measure_value(day, measure)) if day is not None else 0


def goal_progress(data: HeatmapData, cfg: Config) -> tuple[int, int] | None:
    """(hecho, meta) de hoy, o None si no hay meta que ensenar.

    Con «Un numero», en la unidad de la medida. Con «Terminar lo de hoy», en
    tarjetas: las respondidas hoy frente a esas mas las que aun vencen.
    """
    if cfg.goal_mode == "number":
        return _today_value(data, cfg.measure), cfg.goal
    if cfg.goal_mode == "due" and data.due_remaining is not None:
        done = _today_value(data, "cards")
        goal = done + data.due_remaining
        if goal == 0:
            # Hoy no vence nada ni se ha estudiado: una meta de 0 no es una
            # meta, y un ✓ sin estudiar seria falso (4.11.0). «Hoy» se ve
            # como sin meta.
            return None
        # --- FIX-026 (2026-10-22) ---------------------------------------
        # Sintoma: con «Terminar lo de hoy» ya cumplida, la tarjeta volvia a
        #          «faltan 3» al rato, sin haber hecho nada mal.
        # Causa: las tarjetas en aprendizaje vuelven a vencer horas despues,
        #        y la meta se recalculaba con ellas.
        # Regla: una meta cumplida queda cumplida el resto del dia; solo
        #        vuelve atras si se deshace la respuesta que la cumplio.
        # ----------------------------------------------------------------
        if data.due_reached is not None:
            goal = min(goal, data.due_reached)
        return done, goal
    return None


def goal_met(data: HeatmapData, cfg: Config) -> bool:
    progress = goal_progress(data, cfg)
    return progress is not None and progress[1] > 0 and progress[0] >= progress[1]


def _today_card(data: HeatmapData, cfg: Config, deck_only: bool, celebrate: bool) -> str:
    """¿He hecho lo de hoy? En un mazo no hay meta, que es de toda la coleccion:
    mezclarla confundiria que se mide (Norman, error de modo)."""
    done = _today_value(data, cfg.measure)
    # Sin meta, la linea dice lo hecho en los 7 ultimos dias completos, para
    # que la cifra de hoy tenga su referencia (sin enlaces: 4.2.0).
    recent, _previous, _studied = week_totals(data, cfg.measure)
    # Sin nada en esos 7 dias, ninguna linea: «0 tarjetas en 7 días» solo
    # repetiria el cero (4.15.0, informe del cliente).
    week = (
        fill_low("week_total", total=count_html(round_half_up(recent), cfg.measure))
        if round_half_up(recent) > 0
        else ""
    )
    if deck_only:
        return _mini(t("card_today_deck"), count_html(done, cfg.measure), week)
    progress = goal_progress(data, cfg) if cfg.show_streak else None
    if progress is None:
        return _mini(t("card_today"), count_html(done, cfg.measure), week)
    value, goal = progress
    big = ring_svg(value / goal if goal else 1.0, 32) + goal_of_html(value, goal)
    if value >= goal:
        # Al cumplirla, la primera vez que se dibuja: el ✓ aparece con un leve
        # aumento de 150 ms (animacion pedida por el cliente, dentro de la
        # guia: solo escala y transparencia; nada si se pide reducir).
        # «Al día» con «Terminar lo de hoy»: dice justo lo logrado (4.11.0).
        done_text = lt("goal_up_to_date" if cfg.goal_mode == "due" else "goal_done")
        # La cuenta de la semana sale desde el primer dia (4.11.2, peticion
        # del cliente), y el historial va en el globo de «✓ Meta cumplida».
        # Sin globo con el historial (4.14.0, peticion del cliente): sigue en
        # Opciones, donde se decide cambiar la meta.
        line = _check_html(done_text, celebrate)
        line += SEP + fill_low("goal_week", days=_days_html(goal_week_count(data)))
    else:
        left = goal - value
        unit = count_html(left, cfg.measure) if cfg.goal_mode == "number" else count_html(left, "cards")
        # «falta 1 tarjeta», «faltan 2 tarjetas»: la frase entera concuerda
        # con la cifra (4.14.0).
        line = fill_low(plural_key("goal_left", left), count=unit)
    return _mini(t("card_today"), big, line, "gritmap-big-ring")


def goal_of_html(done: int, goal: int) -> str:
    """«0 de 2» con la regla de las demas cifras (4.12.0): lo hecho, que es lo
    que cambia al estudiar, a 20 px; el resto («de 2»), pequeno y en gris como
    una unidad. Vale para cualquier orden de palabras del idioma."""
    template = html.escape(t("goal_of"), quote=False)
    before, _sep, after = template.partition("{done}")
    goal_text = num_html(goal)

    def unit(part: str) -> str:
        part = part.strip().replace("{goal}", goal_text)
        return f'<span class="gritmap-unit">{part}</span>' if part else ""

    return f'<span class="gritmap-big-text">{unit(before)}{num_html(done)}{unit(after)}</span>'


def _check_html(text: str, celebrate: bool = False, spoken: str = "") -> str:
    """«✓ texto» con el ✓ como pieza propia, igual en «Hoy» y en «Racha»
    (FIX-031). Si el texto traducido ya lleva el ✓ delante, se quita.

    Con spoken, el lector de pantalla oye ese texto en lugar de lo que se ve
    (4.15.0): «✓ hoy» sin el ✓ seria solo «hoy»; se oye «hoy hecho»."""
    label = text[1:].lstrip() if text.startswith("✓") else text
    check_class = "gritmap-check gritmap-celebrate" if celebrate else "gritmap-check"
    shown = f'<span class="{check_class}" aria-hidden="true">✓</span> ' + html.escape(label)
    if not spoken:
        return shown
    return f'<span aria-hidden="true">{shown}</span><span class="gritmap-sr">{html.escape(spoken)}</span>'



# Dias completos que mira el historial de la meta (4.11.0).
GOAL_HISTORY_DAYS = 14


def goal_record(
    data: HeatmapData, mode: str, pause: tuple[date, date] | None, today_met: bool = False
) -> tuple[int, int]:
    """(dias cumplidos, dias con datos) de esa meta en los ultimos 14 dias
    completos, sin los de pausa ni los dias sin datos (no son fallos). Con
    today_met, hoy cuenta tambien: solo si ya se cumplio, porque un dia a
    medias no es un fallo."""
    paused = paused_days(pause, data.today)
    marks = [True] if today_met else []
    for days_ago in range(1, GOAL_HISTORY_DAYS + 1):
        if days_ago in paused:
            continue
        mark = data.goal_days.get((data.today - timedelta(days=days_ago)).isoformat())
        if mark is not None and mark[0] == mode:
            marks.append(mark[1])
    return sum(marks), len(marks)


def goal_week_count(data: HeatmapData) -> int:
    """Dias con la meta cumplida de lunes a hoy, hoy incluido (4.11.0).

    Sin denominador: un dia sin datos (estudiado solo en el movil) no
    aparece como fallo. Se llama con la meta de hoy ya cumplida.
    """
    monday = data.today - timedelta(days=data.today.weekday())
    count = 1
    for key, (_mode, met) in data.goal_days.items():
        day = _iso_day(key)
        if met and day is not None and monday <= day < data.today:
            count += 1
    return count


def _iso_day(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _date_html(day: date) -> str:
    """Fecha corta («5 nov.»): la pone el navegador en el idioma activo; aqui
    queda una reserva."""
    return (
        f'<span class="gritmap-date" data-gritmap-date="{day.isoformat()}">'
        f"{day.day} {html.escape(month_abbrev(day.month))}</span>"
    )


def _pause_html(cfg: Config, today: date) -> str:
    """«en pausa hasta el 5 nov.» mientras dure una pausa (4.7.0)."""
    if cfg.pause is None or not cfg.pause[0] <= today <= cfg.pause[1]:
        return ""
    return fill_low("paused_until", date=_date_html(cfg.pause[1]))


def _streak_card(stats: FullStats, cfg: Config, today: date) -> str:
    """¿Llevo constancia? Informa sin presionar: nada de avisos de perdida.

    La linea gris va por orden de importancia («✓ hoy», la pausa, el record
    y los comodines).

    Con la racha a cero (4.15.0, informe del cliente): «0 días» y la linea de
    cualquier dia, «hoy pendiente · [su plan]», en lugar de «Última sesión:
    hace 4 días». Mira adelante, no cuenta la ausencia (el mapa ya ensena
    cuando estudio por ultima vez).
    """
    current = stats.current_streak
    pause = _pause_html(cfg, today)
    gap = stats.longest_streak - current
    # Vuelta tras romperla: un comienzo, no un fracaso (Hopkins, C1).
    big = html.escape(t("day_one")) if current == 1 and stats.previous_best >= 2 else _days_html(current)
    # --- FIX-031 (2026-10-27) ---------------------------------------
    # Sintoma: el ✓ de «✓ hoy» en «Racha» era gris y fino, y el de «✓ Meta
    #          cumplida» en «Hoy», del color del texto y en seminegrita.
    # Causa: el de la racha iba dentro del texto traducido y el de la meta,
    #        en su propia pieza con estilo.
    # Regla: todo ✓ de las tarjetas se dibuja con la misma pieza
    #        (_check_html), con el mismo aspecto.
    # ----------------------------------------------------------------
    if stats.today_done:
        parts = [_check_html(_lower_label(t("streak_today")), spoken=lt("today_done"))]
    else:
        parts = [html.escape(lt("today_pending"))]
    if not stats.today_done and cfg.study_plan:
        # Plan «Suelo estudiar…» (4.11.0): mientras hoy este pendiente, tal
        # como lo escribio (sin pasar a minuscula).
        parts[0] += SEP + html.escape(cfg.study_plan)
    if pause:
        parts.append(pause)
    # «Un año seguido» ya no va aqui, donde se cortaba el primero: es la
    # primera linea de sorpresa del mapa (4.8.0).
    # El record, delante de los comodines (4.14.0, peticion del cliente):
    # sale pocos dias y es lo que mas anima; los comodines estan siempre y,
    # si la linea no cabe, se pierden ellos primero. Sin globos: la regla de
    # los comodines esta en Opciones y el record se dice como distancia.
    if current > 0 and 0 < gap <= _RECORD_GAP_MAX and stats.longest_streak >= _RECORD_NEAR_MIN:
        parts.append(fill_low("record_near", days=_days_html(gap)))
    if cfg.freezes and stats.freezes_left > 0:
        count = num_html(stats.freezes_left)
        parts.append(fill_low(plural_key("freeze", stats.freezes_left), count=count))
    return _mini(t("card_streak"), big, SEP.join(parts))


def _lower_label(text: str) -> str:
    """«✓ Hoy» -> «✓ hoy»: minuscula tras el ✓ (4.15.0)."""
    if text.startswith("✓"):
        rest = text[1:].lstrip()
        return "✓ " + (rest[:1].lower() + rest[1:] if lang() != "de" else rest)
    return text


def _retention_card(stats: FullStats, window: int) -> str:
    """¿Estoy aprendiendo de verdad? La retencion mide aprendizaje, no uso."""
    # --- FIX-002 (2026-07-27) --------------------------------------
    # Sintoma: la retencion aparecia como 0%, como si se hubiera fallado todo,
    #          en cuentas recien empezadas o que solo tienen tarjetas nuevas.
    # Causa: no se distinguia "no hay repasos que contar" de "los fallaste
    #        todos"; ambos casos acababan escribiendo 0%.
    # Regla: cuando no hay dato que ensenar se escribe "N/A" en gris apagado,
    #        tomando el texto del propio Anki para que este en todos los
    #        idiomas. Un porcentaje solo se escribe si se ha calculado.
    #        (Desde la 4.15.0, a peticion del cliente, sin dato la tarjeta no
    #        se muestra: nunca se escribe un porcentaje que no se calculo.)
    # ---------------------------------------------------------------
    if stats.retention is None:
        # Sin 20 respuestas en el periodo, la tarjeta no se muestra (4.15.0,
        # informe del cliente), como «Próxima fecha» sin fechas: el primer
        # dia, o al volver tras mucho tiempo, no recibe un panel de ceros.
        return ""
    # Sin el objetivo de FSRS (4.14.0, peticion del cliente): ya esta en las
    # opciones del mazo de Anki.
    return _mini(_label("retention"), pct_html(stats.retention), _period_text(window))


def _average_card(stats: FullStats, measure: str, window: int) -> str:
    """Lo hecho por dia estudiado en el periodo de las cifras (4.1.0)."""
    big, reason = _average_html(stats.average, measure, window)
    if reason:
        # Sin dato, la tarjeta no se muestra (4.15.0, informe del cliente).
        return ""
    # Sin «por dia estudiado» (4.7.1, peticion del cliente): solo el periodo.
    return _mini(_label("daily_avg"), big, _period_text(window))


def _next_card(key_dates: tuple[KeyDate, ...], today: date) -> str:
    """¿Que tengo por delante? Sin enlaces (4.2.0, peticion del cliente):
    solo el nombre (4.3.0: sin la fecha al lado). Desde la 4.8.0 la tarjeta
    solo existe si hay alguna fecha de hoy en adelante (build_summary)."""
    day = min(kd.day for kd in key_dates if kd.day >= today)
    # Solo el nombre, sin el dia de la semana (4.7.1, peticion del cliente).
    names = " · ".join(html.escape(kd.label) for kd in key_dates if kd.day == day)
    return _mini(t("card_next"), countdown_html((day - today).days), names)


def build_summary(
    data: HeatmapData, cfg: Config, stats: FullStats, deck_only: bool, celebrate: bool = False
) -> str:
    """Las tarjetas de debajo del mapa, de una a cinco, del mismo ancho entre
    todas. Una tarjeta sin dato no se muestra (4.15.0): «Promedio diario» y
    «Retención» como ya hacia «Próxima fecha»."""
    cards = [_today_card(data, cfg, deck_only, celebrate)]
    if cfg.show_streak:
        cards.append(_streak_card(stats, cfg, data.today))
    cards.append(_average_card(stats, cfg.measure, cfg.avg_window))
    cards.append(_retention_card(stats, cfg.avg_window))
    # «Próxima fecha», solo si hay alguna de hoy en adelante (4.8.0): quien
    # no usa fechas clave no ve una tarjeta vacia para siempre.
    if any(kd.day >= data.today for kd in cfg.key_dates):
        cards.append(_next_card(cfg.key_dates, data.today))
    cards = [card for card in cards if card]
    return (
        f'<div class="gritmap-summary gritmap-n{len(cards)}"><div class="gritmap-cards">'
        + "".join(cards)
        + "</div></div>"
    )


# Tarjeta «Actividad»: el mapa
# ---------------------------------------------------------------------------


def _key_labels(key_dates: tuple[KeyDate, ...], today: date) -> dict[date, str]:
    """Cabecera del globo de cada fecha clave, ya en HTML.

    Nombres separados por " · " y, si la fecha no ha pasado, la cuenta atras
    entre parentesis: «Examen de Matematicas (faltan 23 dias)».
    """
    grouped: dict[date, list[str]] = {}
    for key_date in key_dates:
        grouped.setdefault(key_date.day, []).append(html.escape(key_date.label))
    labels: dict[date, str] = {}
    for day, names in grouped.items():
        head = " · ".join(names)
        countdown = countdown_html((day - today).days)
        labels[day] = f"{head} ({countdown})" if countdown else head
    return labels


def past_cell(
    day: DayActivity | None, measure: str, thresholds: list[float]
) -> tuple[int, int, str]:
    """Datos de un dia pasado (o de hoy) en la medida elegida.

    Devuelve el tono (0 = sin estudio, 1-4), la cifra del globo y la
    plantilla del globo.
    """
    if day is None or day.reviews == 0:
        return 0, 0, "none"
    if measure == "new":
        if day.new == 0:
            # Dia estudiado sin ninguna nueva: en gris, porque con esta medida
            # el mapa solo ensena los dias con nuevas (decision del cliente,
            # 2026-10-08). El globo dice «Ninguna nueva» y Explorar se abre igual.
            return 0, 0, "new_none"
        category = plural_category(lang(), day.new)
        return level_index(day.new, thresholds) + 1, day.new, f"new_{category}"
    value = day.cards if measure == "cards" else day.reviews
    return level_index(value, thresholds) + 1, value, "rev_" + plural_category(lang(), value)


def first_study_ago(data: HeatmapData) -> int:
    """Dias hacia atras del primer dia con repasos (0 si nunca se estudio:
    entonces todo lo anterior a hoy es «sin dato»)."""
    return max(data.past) if data.past else 0


def _future_template(count: int) -> str:
    if count == 0:
        return "fnone"
    return "due_" + plural_category(lang(), count)


def _fit(cfg: Config) -> bool:
    return cfg.cell_size == FIT_WIDTH


def _radius_units(cfg: Config) -> float:
    """Redondeo en unidades del dibujo: el elegido en pixeles, pasado a la
    escala del cuadrito de 14 (con «Ajustado al ancho», tal cual)."""
    if _fit(cfg):
        return float(cfg.border_radius)
    return round(cfg.border_radius * _CELL / cfg.cell_size, 2)


def _week_count(year: int) -> int:
    start = date(year, 1, 1)
    days = (date(year, 12, 31) - start).days + 1
    return (start.weekday() + days + 6) // 7


def _cell_position(day: date) -> tuple[int, int]:
    """Semana (columna) y dia de la semana (fila, lunes = 0) de un dia."""
    start = date(day.year, 1, 1)
    offset = start.weekday() + (day - start).days
    return offset // 7, offset % 7


def _build_cell(
    day: date,
    data: HeatmapData,
    cfg: Config,
    thresholds: tuple[list[float], list[float]],
    forgiven: dict[int, str],
    key_labels: dict[date, str],
    focusable: bool,
    first_ago: int = 0,
) -> str:
    week, row = _cell_position(day)
    cell = _CELL
    x, y = week * _STEP, row * _STEP
    days_ago = (data.today - day).days
    past_thresholds, future_thresholds = thresholds
    extra = ""
    # «Sin dato» (4.12.0, informe 4.11 aprobado por el cliente): los dias
    # anteriores al primer repaso y los futuros sin pendientes no son «no
    # estudio»; van en un tono propio, mas apagado que el gris vacio, para que
    # el gris de la leyenda («Menos») signifique solo eso.
    no_data = False
    if days_ago < 0:
        # Pendiente: en cuatro grises segun las tarjetas que vencen, como antes
        # de la 4.0.0 (peticion del cliente, 2026-10-21).
        shown = data.future_counts.get(-days_ago, 0)
        future_level = level_index(shown, future_thresholds) + 1 if shown else 0
        no_data = not future_level
        fill = f"var(--gritmap-f{future_level})" if future_level else "var(--gritmap-nodata)"
        template = _future_template(shown)
        clickable = shown > 0
        kind = "future"
    else:
        activity = data.past.get(days_ago)
        level, shown, template = past_cell(activity, cfg.measure, past_thresholds)
        no_data = days_ago > first_ago
        if no_data:
            template = "nodata"
        empty = "var(--gritmap-nodata)" if no_data else "var(--gritmap-empty)"
        fill = f"var(--gritmap-p{level})" if level else empty
        # Explorar se abre igual sea cual sea la medida: basta con que haya
        # repasos ese dia.
        clickable = activity is not None and activity.reviews > 0
        kind = "past"
    attrs = ""
    if clickable:
        attrs += f' data-gritmap-cmd="{kind}:{day.isoformat()}"'
    label = key_labels.get(day)
    if label:
        attrs += f' data-gritmap-key="{html.escape(label, quote=True)}"'
        # Fecha clave: un rombo de hito (4.8.0, en lugar de la estrella de la
        # 4.2.0, que se leia como «favorito» o «premio»). Es la marca con que
        # los cronogramas senalan una fecha, y cuatro vertices se leen hasta
        # con cuadritos de 10 px, asi que vale una sola regla para todos los
        # tamanos. Las que vienen (y la de hoy), llenas en el color del texto
        # con un filo del color de la tarjeta; las pasadas, huecas en gris:
        # lleno frente a hueco se distingue sin color.
        past_class = " gritmap-kpast" if days_ago > 0 else ""
        extra = (
            f'<polygon class="gritmap-kmark{past_class}"'
            f' points="{diamond_points(x + cell / 2, y + cell / 2, cell * 0.34)}" aria-hidden="true"></polygon>'
        )
    if days_ago == 0:
        attrs += ' data-gritmap-today="1"'
    reason = forgiven.get(days_ago)
    css = "gritmap-cell gritmap-nodata" if no_data else "gritmap-cell"
    if reason:
        # Un dia perdonado queda vacio, porque no se estudio, con un borde
        # fino discontinuo.
        css += " gritmap-forgiven"
        attrs += f' data-gritmap-forgiven="{reason}"'
    if focusable:
        attrs += ' tabindex="0"'
    return (
        f'<rect class="{css}" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="{_radius_units(cfg):g}"'
        f' fill="{fill}" data-gritmap-tip="1" data-d="{day.isoformat()}" data-v="{shown}"'
        f' data-t="{template}"{attrs}></rect>{extra}'
    )


def diamond_points(cx: float, cy: float, radius: float) -> str:
    """Vertices de un rombo (cuadrado girado 45°) centrado en (cx, cy)."""
    return (
        f"{cx:.2f},{cy - radius:.2f} {cx + radius:.2f},{cy:.2f} "
        f"{cx:.2f},{cy + radius:.2f} {cx - radius:.2f},{cy:.2f}"
    )


def grid_width(year: int) -> int:
    """Ancho del ano en unidades del dibujo."""
    return _week_count(year) * _STEP - _GAP


def _year_style(cfg: Config, width: int) -> str:
    """Ancho del dibujo: todo el de la tarjeta (sin bajar de 10 px por
    cuadrito) o el dibujo entero a escala del tamano elegido."""
    if _fit(cfg):
        return f"min-width:{width * _FIT_MIN / _CELL:.0f}px"
    return f"width:{width * cfg.cell_size / _CELL:.0f}px"


def _year_classes(cfg: Config) -> str:
    """Clases del ano: con o sin ajuste al ancho. (La fila aparte para las
    marcas de los cuadritos pequenos de la 4.7.0 ya no hace falta: el rombo
    se lee a cualquier tamano.)"""
    return "gritmap-year gritmap-fit" if _fit(cfg) else "gritmap-year"


def _weekday_column() -> str:
    """Iniciales de lunes, miercoles y viernes a la izquierda de sus filas,
    como en GitHub (4.7.0). Las pone el navegador en el idioma activo."""
    rows = "".join(
        f'<span data-gritmap-dayname="{row}"></span>' if row in (0, 2, 4) else "<span></span>" for row in range(7)
    )
    return f'<div class="gritmap-days" aria-hidden="true">{rows}</div>'


def build_year(
    data: HeatmapData,
    cfg: Config,
    year: int,
    thresholds: tuple[list[float], list[float]],
    forgiven: dict[int, str],
    key_labels: dict[date, str],
) -> str:
    """Meses y rejilla del ano, a escala: si no cabe, se desplaza de lado.

    Los meses son texto de la pagina colocado en porcentaje del ancho, asi
    que conservan su tamano de letra aunque la rejilla se estire.
    """
    width = grid_width(year)
    height = 7 * _STEP - _GAP
    focus_day = data.today if data.today.year == year else date(year, 1, 1)

    months: list[str] = []
    last_week = -3
    for month in range(1, 13):
        week, _row = _cell_position(date(year, month, 1))
        # La etiqueta va en la primera semana que empieza en ese mes.
        if _row:
            week += 1
        if week - last_week < 3 or week >= _week_count(year):
            continue
        last_week = week
        # El texto que va aqui es solo la reserva: el navegador lo reescribe
        # con el nombre de mes del idioma activo.
        months.append(
            f'<span class="gritmap-month" data-gritmap-month="{month}"'
            f' style="left:{100 * week * _STEP / width:.3f}%">{html.escape(month_abbrev(month))}</span>'
        )

    cells: list[str] = []
    day = date(year, 1, 1)
    first_ago = first_study_ago(data)
    while day.year == year:
        cells.append(
            _build_cell(
                day, data, cfg, thresholds, forgiven, key_labels, focusable=day == focus_day, first_ago=first_ago
            )
        )
        day += timedelta(days=1)
    # Rejilla de dos columnas (4.7.0): las iniciales de los dias a la
    # izquierda y, a la derecha, los meses, la fila de estrellas (solo con
    # cuadritos pequenos) y el dibujo, que lleva el ancho.
    return (
        f'<div class="{_year_classes(cfg)}">{_weekday_column()}'
        f'<div class="gritmap-months">{"".join(months)}</div>'
        f'<svg viewBox="0 0 {width} {height}" style="{_year_style(cfg, width)}" xmlns="http://www.w3.org/2000/svg"'
        f' role="group" aria-label="{year}">{"".join(cells)}</svg></div>'
    )


def legend_ranges(thresholds: list[float]) -> list[tuple[int, int | None]]:
    """Cifras que cubre cada tono: (desde, hasta); el ultimo no tiene techo.

    Un tono cubre las cifras mayores que el limite anterior y hasta el suyo
    (level_index). Con cuatro tonos, cada cuadrito de la leyenda es
    exactamente uno del mapa.
    """
    ranges: list[tuple[int, int | None]] = []
    low = 1
    for threshold in thresholds:
        high = max(low, int(threshold))
        ranges.append((low, high))
        low = high + 1
    ranges.append((low, None))
    return ranges


def _range_html(low: int, high: int | None, measure: str) -> str:
    if high is None:
        return fill_html("legend_atleast", count=num_html(low), unit=html.escape(unit_text(low, measure)))
    if high == low:
        return num_html(low) + " " + html.escape(unit_text(low, measure))
    values = {"from": num_html(low), "to": num_html(high), "unit": html.escape(unit_text(high, measure))}
    return fill_html("legend_range", **values)


def _legend_cell(css_class: str, info_html: str, radius: float) -> str:
    plain = html.unescape(re.sub(r"<[^>]+>", "", info_html))
    return (
        f'<span class="gritmap-lg-cell {css_class}" style="border-radius:{radius:.1f}px"'
        f' role="img" aria-label="{html.escape(plain, quote=True)}"'
        f' data-gritmap-tip="1" data-gritmap-info="{html.escape(info_html, quote=True)}"></span>'
    )


def build_legend(
    data: HeatmapData, cfg: Config, year: int, thresholds: list[float], forgiven: dict[int, str]
) -> str:
    """«Menos ▢▣▣▣▣ Mas»: los cinco cuadritos del mapa, cada uno con sus cifras
    en el globo, y las muestras de lo que salga en el ano que se ve."""
    # El redondeo de la leyenda sigue al del mapa, a escala de su cuadrito.
    radius = min(_radius_units(cfg) * 11 / _CELL, 5.5)
    cells = [_legend_cell("gritmap-lg-c0", _zero_text(cfg.measure), radius)]
    for index, (low, high) in enumerate(legend_ranges(thresholds)):
        cells.append(_legend_cell(f"gritmap-lg-c{index + 1}", _range_html(low, high, cfg.measure), radius))
    parts = [
        '<div class="gritmap-legend">',
        f'<span class="gritmap-lg-word">{html.escape(lt("legend_less"))}</span>',
        "".join(cells),
        f'<span class="gritmap-lg-word">{html.escape(lt("legend_more"))}</span>',
    ]
    in_year = data.today.year == year
    samples: list[tuple[str, str]] = []
    if data.future_counts and (in_year or year > data.today.year):
        samples.append(("gritmap-lg-due", "legend_due"))
    if any(kd.day.year == year for kd in cfg.key_dates):
        samples.append(("gritmap-lg-key", "legend_key"))
    for css_class, key in samples:
        parts.append(
            f'<span class="gritmap-lg-sample"><span class="gritmap-lg-cell {css_class}" aria-hidden="true">'
            f"</span>{html.escape(lt(key))}</span>"
        )
    if any((data.today - timedelta(days=d)).year == year for d in forgiven):
        parts.append(
            '<span class="gritmap-lg-sample"><span class="gritmap-lg-cell gritmap-lg-forgiven" aria-hidden="true">'
            f'</span>{html.escape(lt("legend_forgiven"))}</span>'
        )
    parts.append("</div>")
    return "".join(parts)


def _surprise_html(found: tuple[str, int] | None, measure: str, year: int) -> str:
    """La sorpresa del dia, si la hay: una linea, con datos reales."""
    if found is None:
        return ""
    key, value = found
    # En minuscula, como todo el pie del mapa (4.15.0).
    if key == "year_total":
        text = fill_low("surprise_year", total=count_html(value, measure))
    elif key == "year_close":
        text = fill_low("year_close", year=html.escape(str(year)), days=_days_html(value))
    elif key == "year_streak":
        text = html.escape(lt("year_streak"))
    else:
        text = html.escape(lt(f"surprise_{key}"))
    return f'<span class="gritmap-surprise">{text}</span>'


def build_activity(
    data: HeatmapData,
    cfg: Config,
    offset: int,
    stats: FullStats | None,
    message: str = "",
) -> str:
    """Tarjeta «Actividad»: titulo con lo hecho en el ano, «‹ 2026 ›», «Hoy» y
    Opciones a la derecha; el mapa; la leyenda abajo a la derecha."""
    key_labels = _key_labels(cfg.key_dates, data.today)
    key_days = tuple(kd.day for kd in cfg.key_dates)
    min_year, max_year = year_bounds(data, key_days)
    year = max(min_year, min(max_year, data.today.year - offset))
    thresholds = legend_thresholds(scale_reference(data, cfg.measure))
    # Los dias futuros no dependen de la medida: siguen en gris segun las
    # tarjetas que vencen, con la escala de siempre (la de los repasos).
    future_thresholds = due_thresholds(scale_reference(data, "reviews"))
    forgiven = stats.forgiven if stats is not None else {}
    # Sin boton «Hoy» (4.4.0, peticion del cliente): el mapa ya se abre en la
    # semana de hoy. «‹ 2026 ›» va centrado y el boton de opciones, aparte,
    # en la esquina de arriba (4.7.0): navegar y configurar son cosas
    # distintas.
    # En el mapa vacio no hay otro ano al que ir.
    first, last = (True, True) if message else (year <= min_year, year >= max_year)
    tools = (
        '<div class="gritmap-yearnav">'
        + _icon_button("prev", t("nav_back"), "left", first)
        + f'<span class="gritmap-yv">{year}</span>'
        + _icon_button("next", t("nav_forward"), "right", last)
        + "</div>"
        + _icon_button("opts", t("nav_opts"), "sliders", extra=' data-gritmap-corner="1"')
    )
    grid = build_year(data, cfg, year, (thresholds, future_thresholds), forgiven, key_labels)
    left = (
        f'<span class="gritmap-empty-hint">{message}</span>'
        if message
        else _surprise_html(surprise(data, cfg.measure, stats) if stats else None, cfg.measure, data.today.year)
    )
    legend = "" if message else build_legend(data, cfg, year, thresholds, forgiven)
    body = (
        f'<div class="gritmap-grid">{grid}</div>'
        f'<div class="gritmap-foot"><div class="gritmap-foot-left">{left}</div>{legend}</div>'
    )
    # Sin titulo ni cifra del ano encima (peticion del cliente, 4.3.0).
    return _card("gritmap-activity", "", tools, body)


# Promedio diario
# ---------------------------------------------------------------------------


def _average_html(average: float | None, measure: str, window: int) -> tuple[str, str]:
    """(dato, motivo): el motivo solo cuando el dato es «N/A»; va en la linea
    gris en lugar del periodo (4.14.0, peticion del cliente: sin globos en
    las tarjetas)."""
    # --- FIX-010 (2026-10-08) --------------------------------------
    # Sintoma: «Promedio diario: 0 repasos» cuando la ventana no tenia ningun
    #          dia completo estudiado, un dato falso.
    # Causa: el promedio sin dias se trataba como 0 y se escribia como cifra.
    # Regla: sin dias que promediar se escribe «N/A» en gris, con el mismo
    #        estilo que la retencion, y solo entonces el globo explica por que.
    #        (Desde la 4.14.0, a peticion del cliente, lo explica la linea
    #        gris de la tarjeta, no un globo; desde la 4.15.0, sin dato la
    #        tarjeta no se muestra.)
    # ---------------------------------------------------------------
    if average is None:
        if window > 0:
            reason = fill_html("avg_na_days", count=num_html(window))
        else:
            reason = html.escape(t("avg_na_all"))
        return _not_available_html(), reason
    rounded = round_half_up(average)
    if measure == "new" and rounded == 0:
        # Decision del cliente (2026-10-09): con «Nuevas», un promedio que se
        # queda en 0 se escribe «N/A» en lugar de «0 nuevas». Es una excepcion
        # pedida de forma expresa a la idea de FIX-010 (cero y sin datos son
        # cosas distintas): aqui si hubo dias estudiados, asi que el globo da
        # el motivo real (menos de una nueva por dia estudiado), no el de
        # FIX-010.
        if window > 0:
            reason = fill_html("avg_na_new_days", count=num_html(window))
        else:
            reason = html.escape(t("avg_na_new_all"))
        return _not_available_html(), reason
    return count_html(rounded, measure), ""


# Pagina completa y estados
# ---------------------------------------------------------------------------


def _message_card(key: str, action: str = "") -> str:
    """Aviso en una tarjeta, con el boton de opciones para poder cambiarlas."""
    tools = _icon_button("opts", t("nav_opts"), "sliders", extra=' data-gritmap-corner="1"')
    body = f'<div class="gritmap-msg">{html.escape(t(key))}{action}</div>'
    return _card("gritmap-activity", "", tools, body) + _TIP


def build_widget_html(
    data: HeatmapData, cfg: Config, offset: int, deck_only: bool = False, celebrate: bool = False
) -> str:
    if data.deck_excluded:
        # Mazo excluido: el aviso y un enlace que lleva directo a la lista de
        # mazos excluidos.
        return _message_card("deck_excluded")
    paused = paused_days(cfg.pause, data.today)
    stats = full_stats(data, cfg.measure, cfg.avg_window, cfg.freezes, paused)
    summary = build_summary(data, cfg, stats, deck_only, celebrate)
    # Sin nada que dibujar, el mapa se ensena igual, vacio y con hoy marcado,
    # y una frase explica que se ira pintando: el estado vacio ensena lo que
    # hara el complemento en lugar de parecer un error.
    if not data.past and not data.future_counts and not cfg.key_dates:
        return build_activity(data, cfg, offset, None, html.escape(lt("empty_hint"))) + summary + _TIP
    # El mapa arriba, a todo el ancho, y las tarjetas debajo (4.1.0).
    return build_activity(data, cfg, offset, stats) + summary + _TIP


def error_html() -> str:
    # Debajo, que hacer (4.9.0): el fallo no deja a nadie sin salida.
    hint = f'<span class="gritmap-msg-hint">{html.escape(t("load_error_hint"))}</span>'
    return _message_card("load_error", hint)


# Contenedor y paleta
# ---------------------------------------------------------------------------


def placeholder_html(cfg: Config) -> str:
    """Las tarjetas ya dibujadas, con huecos grises donde iran los datos y la
    rejilla con su alto final, mientras se calcula la primera vez: nada salta
    cuando llegan los datos."""
    bones = '<span class="gritmap-bone"></span>'
    # Las mismas tarjetas que tendra el resumen: sin racha ni meta, una
    # menos; sin fechas clave por venir, otra menos (4.8.0).
    today = date.today()
    count = 3 + int(cfg.show_streak) + int(any(kd.day >= today for kd in cfg.key_dates))
    minis = "".join(
        f'<section class="gritmap-card gritmap-mini">{bones}{bones}{bones}</section>' for _ in range(count)
    )
    year = date.today().year
    width, height = grid_width(year), 7 * _STEP - _GAP
    bone = f"aspect-ratio:{width}/{height};{_year_style(cfg, width)}"
    grid = (
        f'<div class="{_year_classes(cfg)}"><div class="gritmap-days"></div>'
        '<div class="gritmap-months"></div>'
        f'<div class="gritmap-bone gritmap-bone-grid" style="{bone}"></div></div>'
    )
    activity = (
        '<section class="gritmap-card gritmap-activity"><div class="gritmap-card-head">'
        f'{bones}</div><div class="gritmap-card-body"><div class="gritmap-grid">{grid}</div></div></section>'
    )
    return (
        f'<div id="{ROOT_ID}" aria-busy="true">{activity}'
        f'<div class="gritmap-summary gritmap-n{count}"><div class="gritmap-cards">{minis}</div></div></div>'
    )


def _script_safe(payload: str) -> str:
    """JSON que se puede poner dentro de <script> sin cerrarlo antes de tiempo."""
    return payload.replace("</", "<\\/").replace("<!--", "<\\u0021--")


def container_html(cfg: Config, remembered: str | None) -> str:
    """Contenedor del mapa para una pagina que Anki esta construyendo.

    Con un mapa recordado de esa pantalla, se dibuja mientras la pagina se
    lee, antes de ensenarse: al volver a la lista de mazos o a un mazo el
    mapa ya esta ahi. gritmap.js ya esta cargado en ese punto, porque Anki
    pone los guiones antes del contenido.
    """
    if remembered is None:
        return placeholder_html(cfg)
    return (
        f'<div id="{ROOT_ID}"></div>'
        "<script>if (typeof GritMap !== 'undefined') { GritMap.render("
        + _script_safe(remembered)
        + "); }</script>"
    )


def palette_style_tag(cfg: Config) -> str:
    """Bloque de colores para la cabecera de la pagina."""
    return f'<style id="{STYLE_ID}">{palette_css(cfg.theme)}</style>'


# Envio a la pagina
# ---------------------------------------------------------------------------


def _zero_text(measure: str) -> str:
    """Lo hecho un dia sin estudio, en la unidad de la medida: «0 tarjetas»
    (4.11.0; antes «Ningún repaso»)."""
    if measure == "new":
        return t("tt_new_none")
    base = "tt_cards" if measure == "cards" else "tt_reviews"
    return plural_form(base, plural_category(lang(), 0)).replace("{count}", "0")


def _texts(measure: str) -> dict[str, str]:
    """Plantillas del globo de los dias, segun lo que mide el color."""
    # --- FIX-006 (2026-10-08) --------------------------------------
    # Sintoma: el globo decia «37 tarjetas repasadas» y el promedio «85
    #          tarjetas», pero al pulsar el dia Explorar mostraba menos.
    # Causa: las cifras contaban respuestas (una tarjeta repetida cuenta
    #        varias veces) y los textos hablaban de tarjetas.
    # Regla: cada cifra se escribe en la unidad de lo que cuenta: «repasos»
    #        para respuestas y «tarjetas» para tarjetas distintas (el cliente
    #        pidio el 2026-10-08 que el globo diga solo «tarjetas»). Nunca
    #        «tarjetas» para contar respuestas.
    # ---------------------------------------------------------------
    # --- FIX-022 (2026-10-13) --------------------------------------
    # Sintoma: en ruso, polaco, checo, arabe y otros nueve idiomas salia, por
    #          ejemplo, «22 повторений» en lugar de «22 повторения».
    # Causa: fuera de «Nuevas» solo habia dos formas (una y varias), y esos
    #        idiomas tienen tres o mas.
    # Regla: toda cifra con unidad elige su forma con las reglas de plural del
    #        idioma (plural_category), como ya hacia «Nuevas».
    # ---------------------------------------------------------------
    base = "tt_cards" if measure == "cards" else "tt_reviews"
    texts = {
        # «0 tarjetas», como en «Hoy», no «Ningún repaso» (4.11.0).
        "none": _zero_text(measure),
        # Dias anteriores al primer repaso (4.15.0): el globo solo dice la
        # fecha; «0 tarjetas» seria «no estudio», y ahi no hay dato.
        "nodata": "",
        "fnone": t("tt_no_due"),
        # Dias perdonados (4.0.0).
        "forgiven_freeze": t("tt_forgiven_freeze"),
        "forgiven_pause": t("tt_forgiven_pause"),
    }
    for category in PLURAL_CATEGORIES:
        texts[f"rev_{category}"] = plural_form(base, category)
        texts[f"due_{category}"] = plural_form("tt_due", category)
    if measure == "new":
        # Una plantilla por cada forma de plural del idioma («1 nueva»,
        # «5 nuevas»; en ruso, 1 / 2-4 / 5 o mas...) y la de «Ninguna nueva».
        texts["new_none"] = t("tt_new_none")
        for category in PLURAL_CATEGORIES:
            texts[f"new_{category}"] = plural_form("tt_new", category)
    return texts


def payload_json(inner_html: str, measure: str = "reviews") -> str:
    """Todo lo que necesita GritMap.render, ya convertido en JSON."""
    return json.dumps(
        {
            "html": inner_html,
            "prefix": MSG_PREFIX,
            "locale": locale_code(),
            "texts": _texts(measure),
        }
    )


def error_payload() -> str:
    return payload_json(error_html())


def send(payload: str) -> None:
    """Entrega los datos a la pagina.

    mw.web.eval encola la llamada si la pagina todavia se esta cargando, asi
    que es seguro pedirla en cuanto los datos estan listos.
    """
    mw.web.eval("if (typeof GritMap !== 'undefined') { GritMap.render(" + payload + "); }")


def send_busy() -> None:
    """Avisa a la pagina de que se esta recalculando el mapa (4.12.0).

    La pagina solo ensena «Actualizando…» si el calculo pasa de un segundo, y
    lo quita en cuanto llega el mapa nuevo: lo rapido no se nota.
    """
    mw.web.eval("if (typeof GritMap !== 'undefined' && GritMap.busy) { GritMap.busy(" + busy_json() + "); }")


def busy_json() -> str:
    return json.dumps(t("updating"))


def update_palette(cfg: Config) -> None:
    """Reescribe los colores sin recargar la pagina.

    Solo hace falta al cambiar las opciones: en un dibujado normal la paleta
    ya viene en la cabecera de la pagina. No toca una pagina sin mapa.
    """
    css = palette_css(cfg.theme)
    mw.web.eval(
        "(function(){"
        f"if(!document.getElementById({json.dumps(ROOT_ID)})){{return;}}"
        f"var el=document.getElementById({json.dumps(STYLE_ID)});"
        "if(!el){el=document.createElement('style');"
        f"el.id={json.dumps(STYLE_ID)};"
        "(document.head||document.documentElement).appendChild(el);}"
        f"var css={json.dumps(css)};"
        "if(el.textContent!==css){el.textContent=css;}"
        "})();"
    )
