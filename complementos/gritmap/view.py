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
<span class="gritmap-n">: el navegador las reescribe con el formato del idioma de
Anki (Intl.NumberFormat), que conoce las costumbres de cada idioma.
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

from __future__ import annotations

import html
import json
from datetime import date, timedelta

from aqt import mw

from .config import Config, KeyDate
from .data import (
    DayActivity,
    FullStats,
    HeatmapData,
    full_stats,
    round_half_up,
    scale_reference,
    week_diff,
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
STYLE_ID = "gritmap-palette"
_CELL_GAP = 3


# Cifras y textos
# ---------------------------------------------------------------------------


def num_html(value: int) -> str:
    """Cifra que el navegador reescribe con el formato del idioma de Anki.

    La cifra sin separadores se queda como reserva por si el navegador no
    conociera el idioma. En espanol, por ejemplo, saldra 1240 pero 12.240.
    """
    number = int(value)
    return f'<span class="gritmap-n" data-n="{number}">{number}</span>'


def fill_html(key: str, **values: str) -> str:
    """Texto propio escapado, con los huecos rellenos de HTML ya preparado."""
    text = html.escape(t(key), quote=False)
    for name, value in values.items():
        text = text.replace("{" + name + "}", value)
    return text


def _plural_key(base: str, count: int) -> str:
    return f"{base}_one" if abs(count) == 1 else f"{base}_other"


def count_html(count: int, measure: str) -> str:
    """Cantidad entera con su unidad: 85 repasos, 60 tarjetas, 8 nuevas."""
    if measure == "new":
        # Plural con las reglas completas de cada idioma (peticion del cliente).
        return num_html(count) + " " + html.escape(plural_text("unit_new", count))
    unit = "card" if measure == "cards" else "review"
    return num_html(count) + " " + html.escape(unit_label(count, unit))


def countdown_html(days: int) -> str:
    """Cuenta atras de una fecha clave: nada si ya paso."""
    if days < 0:
        return ""
    if days == 0:
        return html.escape(t("kd_today"))
    return fill_html(_plural_key("kd_left", days), count=num_html(days))


# Piezas del mapa
# ---------------------------------------------------------------------------


def _key_labels(key_dates: tuple[KeyDate, ...], today: date) -> dict[date, str]:
    """Cabecera del globo de cada fecha clave, ya en HTML.

    Nombres separados por " · " y, si la fecha no ha pasado, la cuenta atras
    entre parentesis: «Examen mates (faltan 23 dias)».
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
        'stroke="var(--gritmap-icon)" stroke-width="1.8" stroke-linecap="round"'
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
            '<circle cx="9.2" cy="3.8" r="1.7" fill="var(--gritmap-icon)"/>'
            '<circle cx="4.8" cy="7" r="1.7" fill="var(--gritmap-icon)"/>'
            '<circle cx="10" cy="10.2" r="1.7" fill="var(--gritmap-icon)"/>'
        )
    return (
        '<svg width="12" height="12" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg"'
        f' aria-hidden="true" focusable="false" style="display:block;">{body}</svg>'
    )


def _nav_button(cmd: str, label: str, icon_kind: str, disabled: bool) -> str:
    """Boton de navegacion.

    Es un <button> real para que se pueda alcanzar con el tabulador y para que
    un lector de pantalla lo anuncie; el aspecto es el de siempre.
    """
    safe_label = html.escape(label, quote=True)
    attrs = f' title="{safe_label}" aria-label="{safe_label}"'
    if disabled:
        attrs += " disabled"
    else:
        attrs += f' data-gritmap-cmd="{cmd}"'
    return f'<button type="button" class="gritmap-btn"{attrs}>{_icon(icon_kind)}</button>'


def _build_nav(prev_disabled: bool, next_disabled: bool) -> str:
    return (
        '<div class="gritmap-nav">'
        + _nav_button("prev", t("nav_back"), "left", prev_disabled)
        + _nav_button("today", t("nav_today"), "circle", False)
        + _nav_button("next", t("nav_forward"), "right", next_disabled)
        + _nav_button("opts", t("nav_opts"), "sliders", False)
        + "</div>"
    )


def _cell_stroke(days_ago: int, is_key: bool) -> str:
    if is_key:
        return ' stroke="var(--gritmap-key)" stroke-width="2" stroke-opacity="0.95"'
    if days_ago == 0:
        return ' stroke="var(--gritmap-today)" stroke-width="1.5" stroke-opacity="0.8"'
    return ""


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
    return level_index(value, thresholds) + 1, value, "one" if value == 1 else "other"


def _future_template(count: int) -> str:
    if count == 0:
        return "fnone"
    return "fone" if count == 1 else "fother"


def _build_cell(
    day: date,
    data: HeatmapData,
    cfg: Config,
    past_thresholds: list[float],
    future_thresholds: list[float],
    key_labels: dict[date, str],
    x: int,
    y: int,
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
    command = f' data-gritmap-cmd="{kind}:{day.isoformat()}"' if clickable else ""
    label = key_labels.get(day)
    key_attr = f' data-gritmap-key="{html.escape(label, quote=True)}"' if label else ""
    return (
        f'<rect class="gritmap-cell" x="{x}" y="{y}" width="{cfg.cell_size}"'
        f' height="{cfg.cell_size}" rx="{cfg.border_radius}" fill="{fill}"'
        f"{_cell_stroke(days_ago, label is not None)}"
        f' data-gritmap-tip="1" data-d="{day.isoformat()}" data-v="{shown}" data-t="{template}"'
        f"{key_attr}{command}></rect>"
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
    top_margin = 20
    left_margin = 2
    width = left_margin + num_weeks * step
    height = top_margin + 7 * step
    parts: list[str] = [
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}"'
        ' xmlns="http://www.w3.org/2000/svg">'
    ]
    row = start_row
    week = 0
    last_label_month = 0
    last_label_week = -3
    day = start_date
    while day <= end_date:
        x = left_margin + week * step
        y = top_margin + row * step
        first_cell = week == 0 and row == start_row
        if (row == 0 or first_cell) and day.month != last_label_month and week - last_label_week >= 3:
            # El texto que va aqui es solo la reserva: el navegador lo
            # reescribe con el nombre de mes del idioma activo.
            parts.append(
                f'<text data-gritmap-month="{day.month}" x="{x}" y="{top_margin - 7}"'
                ' font-size="10.5" font-weight="600" letter-spacing="0.03em"'
                f' fill="var(--gritmap-muted)">{html.escape(month_abbrev(day.month))}</text>'
            )
            last_label_month = day.month
            last_label_week = week
        parts.append(
            _build_cell(day, data, cfg, past_thresholds, future_thresholds, key_labels, x, y)
        )
        row += 1
        if row > 6:
            row = 0
            week += 1
        day += timedelta(days=1)
    parts.append("</svg>")
    return "".join(parts)


def _stat_entry(label: str, value_html: str, level: int, info_html: str = "") -> str:
    """Una cifra de la fila de estadisticas.

    value_html ya viene escapado. Si hay info_html, la cifra muestra un globo
    con ese texto al pasar el raton.
    """
    info = (
        f' data-gritmap-tip="1" data-gritmap-info="{html.escape(info_html, quote=True)}"'
        if info_html
        else ""
    )
    return (
        f'<span class="gritmap-stat"{info}>'
        f'<span class="gritmap-label">{html.escape(label)}</span>'
        f'<span class="gritmap-value {level_class(level)}">{value_html}</span>'
        "</span>"
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
            t("retention"),
            html.escape(anki_text("statistics_true_retention_not_applicable", "not_available")),
            -1,
        )
    return _stat_entry(t("retention"), f"{retention}%", pct_level(retention))


def _days_html(count: int) -> str:
    return num_html(count) + " " + html.escape(unit_label(count, "day"))


def _current_streak_entry(stats: FullStats) -> str:
    """Racha actual; si es cero, cuanto hace de la ultima sesion, en gris."""
    if stats.current_streak == 0 and stats.last_session is not None:
        days = stats.last_session
        return _stat_entry(
            t("last_session"), fill_html(_plural_key("ago", days), count=num_html(days)), -1
        )
    return _stat_entry(
        t("current_streak"), _days_html(stats.current_streak), streak_level(stats.current_streak)
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
        return _stat_entry(t("daily_avg"), _not_available_html(), -1, reason)
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
        return _stat_entry(t("daily_avg"), _not_available_html(), -1, reason)
    return _stat_entry(t("daily_avg"), count_html(rounded, measure), avg_level(rounded))


def build_stats(stats: FullStats, measure: str, window: int = 30) -> str:
    return (
        '<div class="gritmap-stats">'
        + _average_entry(stats.average, measure, window)
        + _stat_entry(t("days_learned"), f"{stats.studied_pct}%", pct_level(stats.studied_pct))
        + _retention_entry(stats.retention)
        + _stat_entry(t("longest_streak"), _days_html(stats.longest_streak), streak_level(stats.longest_streak))
        + _current_streak_entry(stats)
        + "</div>"
    )


def build_widget_html(data: HeatmapData, cfg: Config, offset: int) -> str:
    key_labels = _key_labels(cfg.key_dates, data.today)
    if not data.past and not data.future_counts and not key_labels:
        return f'<div class="gritmap-msg">{html.escape(t("no_data"))}</div>'
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
        + f'<div class="gritmap-yl">{year}</div>'
        + build_stats(stats, cfg.measure, cfg.avg_window)
        + '<div id="gritmap-tip"></div>'
    )


def error_html() -> str:
    return f'<div class="gritmap-msg">{html.escape(t("load_error"))}</div>'


# Marcador de posicion y paleta
# ---------------------------------------------------------------------------


def _estimated_height(cfg: Config) -> int:
    """Alto aproximado del mapa terminado.

    Sirve para que el marcador de posicion reserve el hueco y la lista de
    mazos no de un salto cuando llegan los datos: navegacion (37 px mas 10 de
    margen), rejilla (20 px de cabecera y siete filas de celdas), etiqueta del
    ano (19 px) y fila de estadisticas (33 px).
    """
    svg_height = 20 + 7 * (cfg.cell_size + _CELL_GAP)
    return 47 + svg_height + 19 + 33


def placeholder_html(cfg: Config) -> str:
    """Hueco donde despues se dibuja el mapa.

    OJO: este texto lo inserta Anki con formateo de porcentaje sobre su
    plantilla, asi que no puede contener el caracter "%" en ninguna forma.
    """
    return (
        f'<div id="{ROOT_ID}" style="min-height:{_estimated_height(cfg)}px;">'
        '<div class="gritmap-wait">&hellip;</div></div>'
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
    return {"cls": cls, "html": f" {arrow} " + count_html(abs(rounded), measure)}


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
    if measure == "cards":
        one, other = t("tt_cards_one"), t("tt_cards_other")
    else:
        one, other = t("tt_reviews_one"), t("tt_reviews_other")
    texts = {
        "none": t("tt_no_reviews"),
        "one": one,
        "other": other,
    }
    if measure == "new":
        # Una plantilla por cada forma de plural del idioma («1 nueva»,
        # «5 nuevas»; en ruso, 1 / 2-4 / 5 o mas...) y la de «Ninguna nueva».
        texts["new_none"] = t("tt_new_none")
        for category in PLURAL_CATEGORIES:
            texts[f"new_{category}"] = plural_form("tt_new", category)
    return {
        **texts,
        "fnone": t("tt_no_due"),
        "fone": t("tt_due_one"),
        "fother": t("tt_due_other"),
    }


def _send(payload: dict[str, object]) -> None:
    """Entrega los datos a la pagina.

    mw.web.eval encola la llamada si la pagina todavia se esta cargando, asi
    que es seguro pedirla en cuanto los datos estan listos.
    """
    mw.web.eval(
        "if (typeof GritMap !== 'undefined') { GritMap.render("
        + json.dumps(payload)
        + "); }"
    )


def render(
    inner_html: str,
    measure: str = "reviews",
    week: dict[str, str] | None = None,
) -> None:
    _send(
        {
            "html": inner_html,
            "prefix": MSG_PREFIX,
            "locale": locale_code(),
            "texts": _texts(measure),
            "week": week,
        }
    )


def render_error() -> None:
    render(error_html())


def update_palette(cfg: Config) -> None:
    """Reescribe los colores sin recargar la pagina.

    Solo hace falta al cambiar las opciones: en un dibujado normal la paleta
    ya viene en la cabecera de la pagina.
    """
    css = palette_css(cfg.theme)
    mw.web.eval(
        "(function(){"
        f"var el=document.getElementById({json.dumps(STYLE_ID)});"
        "if(!el){el=document.createElement('style');"
        f"el.id={json.dumps(STYLE_ID)};"
        "(document.head||document.documentElement).appendChild(el);}"
        f"var css={json.dumps(css)};"
        "if(el.textContent!==css){el.textContent=css;}"
        "})();"
    )
