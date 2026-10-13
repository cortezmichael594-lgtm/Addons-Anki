"""Construccion del HTML del mapa y envio a la pagina de Anki.

El reparto de trabajo con la parte web es deliberado:

  * web/gritmap.css y web/gritmap.js se cargan una sola vez junto con la
    pagina, asi que no hay un instante en que el mapa se vea sin estilo.
  * La paleta de colores viaja en la cabecera de la pagina, porque es lo unico
    que depende de las opciones.
  * En cada dibujado solo se envia una llamada con los datos ya preparados.
    Antes se reenviaba en cada ocasion la hoja de estilos y todo el codigo de
    los detectores de eventos, que es lo que producia parpadeos.

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

from __future__ import annotations

import html
import json
import re
from datetime import date, timedelta

from aqt import mw

from .config import Config, KeyDate
from .data import (
    WINDOWS,
    DayActivity,
    FullStats,
    HeatmapData,
    full_stats,
    measure_value,
    round_half_up,
    scale_reference,
    week_diff,
    year_bounds,
)
from .i18n import (
    PLURAL_CATEGORIES,
    STRINGS,
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
from .palettes import avg_level, legend_thresholds, level_class, level_index, palette_css, pct_level, streak_level

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
_CELL_GAP = 3
_TOP_MARGIN = 20
_LEFT_MARGIN = 2


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
    text = html.escape(t(key), quote=False)
    for name, value in values.items():
        text = text.replace("{" + name + "}", value)
    return text


def count_html(count: int, measure: str) -> str:
    """Cantidad entera con su unidad: 85 repasos, 60 tarjetas, 8 nuevas."""
    if measure == "new":
        return num_html(count) + " " + html.escape(plural_text("unit_new", count))
    unit = "card" if measure == "cards" else "review"
    return num_html(count) + " " + html.escape(unit_label(count, unit))


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


# Piezas del mapa
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


def _icon(kind: str) -> str:
    stroke = (
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round"'
        ' stroke-linejoin="round" fill="none"'
    )
    if kind == "left":
        body = f'<path d="M8.7 2.6 L4.6 7 L8.7 11.4" {stroke}/>'
    elif kind == "right":
        body = f'<path d="M5.3 2.6 L9.4 7 L5.3 11.4" {stroke}/>'
    elif kind == "circle":
        body = f'<circle cx="7" cy="7" r="4" {stroke}/>'
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


def _nav_button(cmd: str, label: str, icon_kind: str, disabled: bool) -> str:
    """Boton de navegacion.

    Es un <button> real para que se pueda alcanzar con el tabulador y para que
    un lector de pantalla lo anuncie.
    """
    safe_label = html.escape(label, quote=True)
    attrs = f' title="{safe_label}" aria-label="{safe_label}" data-gritmap-btn="{cmd}"'
    if disabled:
        attrs += " disabled"
    else:
        attrs += f' data-gritmap-cmd="{cmd}"'
    return f'<button type="button" class="gritmap-btn"{attrs}>{_icon(icon_kind)}</button>'


def _build_nav(prev_disabled: bool, next_disabled: bool, only_options: bool = False) -> str:
    """Los cuatro botones centrados encima del mapa (solo Opciones si no hay mapa)."""
    if only_options:
        buttons = _nav_button("opts", t("nav_opts"), "sliders", False)
    else:
        buttons = (
            _nav_button("prev", t("nav_back"), "left", prev_disabled)
            + _nav_button("today", t("nav_today"), "circle", False)
            + _nav_button("next", t("nav_forward"), "right", next_disabled)
            + _nav_button("opts", t("nav_opts"), "sliders", False)
        )
    return f'<div class="gritmap-nav">{buttons}</div>'


def past_cell(
    day: DayActivity | None, measure: str, thresholds: list[float]
) -> tuple[int, int, str]:
    """Datos de un dia pasado (o de hoy) en la medida elegida.

    Devuelve el tono (0 = sin estudio, 1-10), la cifra del globo y la
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


def _future_template(count: int) -> str:
    if count == 0:
        return "fnone"
    return "due_" + plural_category(lang(), count)


def _build_cell(
    day: date,
    data: HeatmapData,
    cfg: Config,
    past_thresholds: list[float],
    future_thresholds: list[float],
    key_labels: dict[date, str],
    x: int,
    y: int,
    focusable: bool,
) -> str:
    days_ago = (data.today - day).days
    if days_ago < 0:
        shown = data.future_counts.get(-days_ago, 0)
        level = level_index(shown, future_thresholds) + 1 if shown else 0
        fill = f"var(--gritmap-f{level})" if level else "var(--gritmap-empty)"
        template = _future_template(shown)
        clickable = shown > 0
        kind = "future"
    else:
        activity = data.past.get(days_ago)
        level, shown, template = past_cell(activity, cfg.measure, past_thresholds)
        fill = f"var(--gritmap-p{level})" if level else "var(--gritmap-empty)"
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
    if days_ago == 0:
        attrs += ' data-gritmap-today="1"'
    if focusable:
        attrs += ' tabindex="0"'
    return (
        f'<rect class="gritmap-cell" x="{x}" y="{y}" width="{cfg.cell_size}"'
        f' height="{cfg.cell_size}" rx="{cfg.border_radius}" fill="{fill}"'
        f' data-gritmap-tip="1" data-d="{day.isoformat()}" data-v="{shown}" data-t="{template}"'
        f"{attrs}></rect>"
    )


def _build_year_svg(
    data: HeatmapData,
    cfg: Config,
    year: int,
    past_thresholds: list[float],
    future_thresholds: list[float],
    key_labels: dict[date, str],
) -> str:
    step = cfg.cell_size + _CELL_GAP
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    start_row = start_date.weekday()
    total_days = (end_date - start_date).days + 1
    num_weeks = (start_row + total_days + 6) // 7
    left_margin = _LEFT_MARGIN
    width = left_margin + num_weeks * step
    height = _TOP_MARGIN + 7 * step
    # El dia que recibe el tabulador: hoy si esta en este ano, si no el 1 de enero.
    focus_day = data.today if data.today.year == year else start_date
    parts: list[str] = [
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}"'
        f' xmlns="http://www.w3.org/2000/svg" role="group" aria-label="{year}">'
    ]
    row = start_row
    week = 0
    last_label_month = 0
    last_label_week = -3
    day = start_date
    while day <= end_date:
        x = left_margin + week * step
        y = _TOP_MARGIN + row * step
        first_cell = week == 0 and row == start_row
        if (row == 0 or first_cell) and day.month != last_label_month and week - last_label_week >= 3:
            # El texto que va aqui es solo la reserva: el navegador lo
            # reescribe con el nombre de mes del idioma activo.
            parts.append(
                f'<text class="gritmap-month" data-gritmap-month="{day.month}" x="{x}"'
                f' y="{_TOP_MARGIN - 7}">{html.escape(month_abbrev(day.month))}</text>'
            )
            last_label_month = day.month
            last_label_week = week
        parts.append(
            _build_cell(
                day, data, cfg, past_thresholds, future_thresholds, key_labels, x, y,
                focusable=day == focus_day,
            )
        )
        row += 1
        if row > 6:
            row = 0
            week += 1
        day += timedelta(days=1)
    parts.append("</svg>")
    return "".join(parts)


def year_total(data: HeatmapData, year: int, measure: str) -> int:
    """Lo hecho en un ano, en la unidad de la medida (los dias futuros no cuentan)."""
    total = 0.0
    for days_ago, day in data.past.items():
        if (data.today - timedelta(days=days_ago)).year == year:
            total += measure_value(day, measure)
    return int(total)


def _year_label(data: HeatmapData, year: int, cfg: Config) -> str:
    """El ano, debajo del mapa, con los botones de periodo a su lado.

    Al pasar el raton por el ano, lo hecho ese ano con el signo de
    exclamacion de cada idioma: «¡12.480 repasos!».
    """
    total = count_html(year_total(data, year, cfg.measure), cfg.measure)
    info = fill_html("year_total", total=total)
    return (
        f'<div class="gritmap-yl"><span class="gritmap-yv" data-gritmap-tip="1"'
        f' data-gritmap-info="{html.escape(info, quote=True)}" tabindex="0">{year}</span>'
        + _build_periods(cfg.avg_window)
        + "</div>"
    )


def _period_label(days: int) -> str:
    """Texto corto de cada boton de periodo: «7 días», «Todo»."""
    if days == 365 and STRINGS[lang()].get("window_year"):
        return html.escape(t("window_year"))
    if days:
        return fill_html("window_days", count=num_html(days))
    own = STRINGS[lang()].get("window_all_short") or t("window_all")
    return html.escape(own)


def _build_periods(window: int) -> str:
    """Botones rapidos del periodo de las cifras: texto pequeno junto al ano."""
    buttons = []
    for days in WINDOWS:
        chosen = days == window
        cmd = f"window:{days}"
        buttons.append(
            f'<button type="button" class="gritmap-period{" gritmap-on" if chosen else ""}"'
            f' data-gritmap-btn="{cmd}" data-gritmap-cmd="{cmd}"'
            f' aria-pressed="{"true" if chosen else "false"}">{_period_label(days)}</button>'
        )
    label = html.escape(t("opt_window"), quote=True)
    return (
        f'<div class="gritmap-periods" role="group" aria-label="{label}" title="{label}">'
        + "".join(buttons)
        + "</div>"
    )


def _stat_entry(label: str, value_html: str, level: int, info_html: str = "") -> str:
    """Una cifra de la fila de estadisticas: la cifra arriba y su rotulo debajo.

    value_html ya viene escapado. La cifra va en el color del texto, con un
    cuadrito del tono que le corresponde delante (level_class). Si hay
    info_html, la cifra muestra un globo con ese texto al pasar el raton.
    """
    info = (
        f' data-gritmap-tip="1" data-gritmap-info="{html.escape(info_html, quote=True)}" tabindex="0"'
        if info_html
        else ""
    )
    return (
        f'<div class="gritmap-stat"{info}>'
        f'<span class="gritmap-value {level_class(level)}">{value_html}</span>'
        f'<span class="gritmap-label">{html.escape(label)}</span>'
        "</div>"
    )


def _retention_entry(retention: int | None) -> str:
    """Retencion, sin globo (el cliente lo retiro el 2026-10-09)."""
    # --- FIX-002 (2026-07-27) --------------------------------------
    # Sintoma: la retencion aparecia como 0%, como si se hubiera fallado todo,
    #          en cuentas recien empezadas o que solo tienen tarjetas nuevas.
    # Causa: no se distinguia "no hay repasos que contar" de "los fallaste
    #        todos"; ambos casos acababan escribiendo 0%.
    # Regla: cuando no hay dato que ensenar se escribe "N/A" en gris apagado,
    #        tomando el texto del propio Anki para que este en todos los
    #        idiomas. Un porcentaje solo se escribe si se ha calculado.
    # ---------------------------------------------------------------
    if retention is None:
        return _stat_entry(
            _label("retention"),
            html.escape(anki_text("statistics_true_retention_not_applicable", "not_available")),
            -1,
        )
    return _stat_entry(_label("retention"), pct_html(retention), pct_level(retention))


def _days_html(count: int) -> str:
    return num_html(count) + " " + html.escape(unit_label(count, "day"))


def _current_streak_entry(stats: FullStats) -> str:
    """Racha actual; si es cero, cuanto hace de la ultima sesion, en gris."""
    if stats.current_streak == 0 and stats.last_session is not None:
        days = stats.last_session
        return _stat_entry(
            _label("last_session"), fill_html(plural_key("ago", days), count=num_html(days)), -1
        )
    return _stat_entry(
        _label("current_streak"), _days_html(stats.current_streak), streak_level(stats.current_streak)
    )


def _not_available_html() -> str:
    """«N/A» con el texto del propio Anki, el mismo que usa la retencion."""
    return html.escape(anki_text("statistics_true_retention_not_applicable", "not_available"))


def _average_entry(average: float | None, measure: str, window: int) -> str:
    # --- FIX-010 (2026-10-08) --------------------------------------
    # Sintoma: «Promedio diario: 0 repasos» cuando la ventana no tenia ningun
    #          dia completo estudiado, un dato falso.
    # Causa: el promedio sin dias se trataba como 0 y se escribia como cifra.
    # Regla: sin dias que promediar se escribe «N/A» en gris, con el mismo
    #        estilo que la retencion, y solo entonces el globo explica por que.
    # ---------------------------------------------------------------
    if average is None:
        if window > 0:
            reason = fill_html("avg_na_days", count=num_html(window))
        else:
            reason = html.escape(t("avg_na_all"))
        return _stat_entry(_label("daily_avg"), _not_available_html(), -1, reason)
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
        return _stat_entry(_label("daily_avg"), _not_available_html(), -1, reason)
    return _stat_entry(_label("daily_avg"), count_html(rounded, measure), avg_level(rounded))


def build_stats(stats: FullStats, measure: str, window: int = 30) -> str:
    return (
        '<div class="gritmap-stats">'
        + _average_entry(stats.average, measure, window)
        + _stat_entry(_label("days_learned"), pct_html(stats.studied_pct), pct_level(stats.studied_pct))
        + _retention_entry(stats.retention)
        + _stat_entry(
            _label("longest_streak"), _days_html(stats.longest_streak), streak_level(stats.longest_streak)
        )
        + _current_streak_entry(stats)
        + "</div>"
    )


_TIP = '<div id="gritmap-tip" role="tooltip"></div>'


def _message(key: str) -> str:
    """Aviso en lugar del mapa, con el boton de opciones para poder cambiarlas."""
    return _build_nav(True, True, only_options=True) + f'<div class="gritmap-msg">{html.escape(t(key))}</div>' + _TIP


def build_widget_html(data: HeatmapData, cfg: Config, offset: int) -> str:
    if data.deck_excluded:
        return _message("deck_excluded")
    key_labels = _key_labels(cfg.key_dates, data.today)
    if not data.past and not data.future_counts and not key_labels:
        return _message("no_data")
    key_days = tuple(kd.day for kd in cfg.key_dates)
    min_year, max_year = year_bounds(data, key_days)
    year = max(min_year, min(max_year, data.today.year - offset))
    stats = full_stats(data, cfg.measure, cfg.avg_window)
    past_thresholds = legend_thresholds(scale_reference(data, cfg.measure))
    # Los dias futuros no dependen de la medida: siguen en gris segun las
    # tarjetas que vencen, con la escala de siempre (la de los repasos).
    future_thresholds = legend_thresholds(scale_reference(data, "reviews"))
    return (
        _build_nav(year <= min_year, year >= max_year)
        + '<div class="gritmap-grid">'
        + _build_year_svg(data, cfg, year, past_thresholds, future_thresholds, key_labels)
        + "</div>"
        + _year_label(data, year, cfg)
        + build_stats(stats, cfg.measure, cfg.avg_window)
        + _TIP
    )


def error_html() -> str:
    return _message("load_error")


# Contenedor y paleta
# ---------------------------------------------------------------------------


def _estimated_height(cfg: Config) -> int:
    """Alto aproximado del mapa terminado.

    Sirve para que el contenedor reserve el hueco y la lista de mazos no de un
    salto cuando llegan los datos: botones (29 px mas 10 de margen), rejilla
    (20 de meses y siete filas de cuadritos), ano con los periodos (25), cifras
    (52) y un margen por si aparece la barra de desplazamiento (6).
    """
    svg_height = _TOP_MARGIN + 7 * (cfg.cell_size + _CELL_GAP)
    return 39 + svg_height + 25 + 52 + 6


def placeholder_html(cfg: Config) -> str:
    """Hueco donde despues se dibuja el mapa, mientras se calcula la primera vez."""
    return (
        f'<div id="{ROOT_ID}" style="min-height:{_estimated_height(cfg)}px;">'
        '<div class="gritmap-wait">&hellip;</div></div>'
    )


def _script_safe(payload: str) -> str:
    """JSON que se puede poner dentro de <script> sin cerrarlo antes de tiempo."""
    return payload.replace("</", "<\\/").replace("<!--", "<\\u0021--")


def container_html(cfg: Config, remembered: str | None) -> str:
    """Contenedor del mapa para una pagina que Anki esta construyendo.

    Con un mapa recordado de esa pantalla, se dibuja mientras la pagina se
    lee, antes de ensenarse: al volver a la lista de mazos o a un mazo el
    mapa ya esta ahi, sin hueco con «…». gritmap.js ya esta cargado en ese
    punto, porque Anki pone los guiones antes del contenido.
    """
    if remembered is None:
        return placeholder_html(cfg)
    return (
        f'<div id="{ROOT_ID}" style="min-height:{_estimated_height(cfg)}px;"></div>'
        "<script>if (typeof GritMap !== 'undefined') { GritMap.render("
        + _script_safe(remembered)
        + "); }</script>"
    )


def palette_style_tag(cfg: Config) -> str:
    """Bloque de colores para la cabecera de la pagina."""
    return f'<style id="{STYLE_ID}">{palette_css(cfg.theme)}</style>'


# Envio a la pagina
# ---------------------------------------------------------------------------


def week_payload(data: HeatmapData, measure: str, show: bool) -> dict[str, str] | None:
    """Comparativa de los 7 ultimos dias completos con los 7 anteriores."""
    if not show:
        return None
    diff, had_previous = week_diff(data, measure)
    if not had_previous:
        return None
    rounded = round_half_up(diff)
    if rounded > 0:
        cls, arrow = "up", "▲"
    elif rounded < 0:
        cls, arrow = "down", "▼"
    else:
        cls, arrow = "flat", "●"
    return {
        "cls": cls,
        "html": f' <span aria-hidden="true">{arrow}</span> ' + count_html(abs(rounded), measure),
        "title": t("week_tip"),
    }


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
    texts = {"none": t("tt_no_reviews"), "fnone": t("tt_no_due")}
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


def payload_json(
    inner_html: str,
    measure: str = "reviews",
    week: dict[str, str] | None = None,
) -> str:
    """Todo lo que necesita GritMap.render, ya convertido en JSON."""
    return json.dumps(
        {
            "html": inner_html,
            "prefix": MSG_PREFIX,
            "locale": locale_code(),
            "texts": _texts(measure),
            "week": week,
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
