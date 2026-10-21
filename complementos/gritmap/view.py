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
    week_totals,
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
from .palettes import (
    LEGEND_TONES,
    avg_level,
    legend_thresholds,
    level_class,
    level_index,
    palette_css,
    pct_level,
    streak_level,
)

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
# La distancia al record solo se ensena si esta cerca (version 3.6.0): lejos,
# la cifra no anima y solo recuerda lo que falta.
_RECORD_GAP_MAX = 7


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


def unit_html(text: str) -> str:
    """Unidad de una cifra («repasos», «días»): en las cifras de debajo del
    mapa va mas pequena y en gris, para que destaque el numero."""
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


def next_key_html(key_dates: tuple[KeyDate, ...], today: date) -> str:
    """La proxima fecha clave, siempre a la vista bajo los botones (3.6.0).

    «★ Examen de Anatomia · faltan 23 dias»; varias el mismo dia, con sus
    nombres separados por « · ». Es un boton: al pulsarlo, el mapa va a esa
    semana. Sin fechas por venir no se dibuja nada.
    """
    upcoming = sorted(kd.day for kd in key_dates if kd.day >= today)
    if not upcoming:
        return ""
    day = upcoming[0]
    names = " · ".join(html.escape(kd.label) for kd in key_dates if kd.day == day)
    text = f'<span class="gritmap-next-star" aria-hidden="true">★</span> {names} · {countdown_html((day - today).days)}'
    cmd = f"key:{day.isoformat()}"
    return (
        '<div class="gritmap-next">'
        f'<button type="button" class="gritmap-next-btn" data-gritmap-btn="key"'
        f' data-gritmap-cmd="{cmd}">{text}</button></div>'
    )


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


def _year_label(data: HeatmapData, year: int, cfg: Config, legend: str) -> str:
    """El ano, debajo del mapa, con la leyenda a la derecha (3.6.0).

    Al pasar el raton por el ano, lo hecho ese ano con el signo de
    exclamacion de cada idioma: «¡12.480 repasos!». En el mapa vacio el ano
    no lleva globo: no hay nada que contar.
    """
    if legend:
        total = count_html(year_total(data, year, cfg.measure), cfg.measure)
        info = fill_html("year_total", total=total)
        year_html = (
            f'<span class="gritmap-yv" data-gritmap-tip="1"'
            f' data-gritmap-info="{html.escape(info, quote=True)}" tabindex="0">{year}</span>'
        )
    else:
        year_html = f'<span class="gritmap-yv">{year}</span>'
    return f'<div class="gritmap-yl">{year_html}{legend}</div>'


def _legend_cell(css_class: str, info_html: str, radius: int) -> str:
    """Cuadrito de la leyenda con su globo; el lector de pantalla lee su texto."""
    plain = re.sub(r"<[^>]+>", "", info_html)
    return (
        f'<span class="gritmap-lg-cell {css_class}" style="border-radius:{radius}px"'
        f' role="img" aria-label="{html.escape(html.unescape(plain), quote=True)}"'
        f' data-gritmap-tip="1" data-gritmap-info="{html.escape(info_html, quote=True)}"></span>'
    )


def legend_ranges(thresholds: list[float]) -> list[tuple[int, int | None]]:
    """Cifras que cubre cada cuadrito de la leyenda: (desde, hasta).

    Los diez tonos se agrupan de dos en dos, como los cinco cuadritos de
    GitHub; el ultimo no tiene techo (hasta = None). Un tono cubre las
    cifras mayores que el limite anterior y hasta el suyo (level_index).
    """
    ranges: list[tuple[int, int | None]] = []
    for group in range(len(LEGEND_TONES)):
        low = int(thresholds[2 * group - 1]) + 1 if group else 1
        if group == len(LEGEND_TONES) - 1:
            ranges.append((low, None))
        else:
            ranges.append((low, max(low, int(thresholds[2 * group + 1]))))
    return ranges


def _range_html(low: int, high: int | None, measure: str) -> str:
    if high is None:
        return fill_html("legend_atleast", count=num_html(low), unit=html.escape(unit_text(low, measure)))
    if high == low:
        return num_html(low) + " " + html.escape(unit_text(low, measure))
    values = {"from": num_html(low), "to": num_html(high), "unit": html.escape(unit_text(high, measure))}
    return fill_html("legend_range", **values)


def build_legend(
    data: HeatmapData, cfg: Config, year: int, thresholds: list[float]
) -> str:
    """Leyenda del mapa (3.6.0): «Menos ▢▢▢▢▢▢ Mas · repasos», con la cifra de
    cada tono en su globo, y las muestras de pendientes, hoy y fecha clave
    solo si salen en el mapa (lo que no esta, no se explica)."""
    radius = min(cfg.border_radius, 4)
    none_key = "tt_new_none" if cfg.measure == "new" else "tt_no_reviews"
    cells = [_legend_cell("gritmap-lg-c0", t(none_key), radius)]
    for index, (low, high) in enumerate(legend_ranges(thresholds)):
        cells.append(_legend_cell(f"gritmap-lg-c{index + 1}", _range_html(low, high, cfg.measure), radius))
    if cfg.measure == "new":
        unit = plural_form("unit_new", "other")
    else:
        unit = t("unit_card_other" if cfg.measure == "cards" else "unit_review_other")
    parts = [
        '<div class="gritmap-legend">',
        f'<span class="gritmap-lg-word">{html.escape(t("legend_less"))}</span>',
        "".join(cells),
        f'<span class="gritmap-lg-word">{html.escape(t("legend_more"))}</span>',
        f'<span class="gritmap-lg-unit">· {html.escape(unit)}</span>',
    ]
    samples: list[tuple[str, str]] = []
    if data.future_counts:
        samples.append(("gritmap-lg-due", "legend_due"))
    if data.today.year == year:
        samples.append(("gritmap-lg-today", "nav_today"))
    if any(kd.day.year == year for kd in cfg.key_dates):
        samples.append(("gritmap-lg-key", "legend_key"))
    for css_class, key in samples:
        parts.append(
            f'<span class="gritmap-lg-sample"><span class="gritmap-lg-cell {css_class}"'
            f' style="border-radius:{radius}px" aria-hidden="true"></span>'
            f"{html.escape(t(key))}</span>"
        )
    parts.append("</div>")
    return "".join(parts)


def _period_label(days: int) -> str:
    """Texto corto de cada boton de periodo: «7 días», «Todo»."""
    if days == 365 and STRINGS[lang()].get("window_year"):
        return html.escape(t("window_year"))
    if days:
        return fill_html("window_days", count=num_html(days))
    own = STRINGS[lang()].get("window_all_short") or t("window_all")
    return html.escape(own)


def _build_periods(window: int) -> str:
    """Botones rapidos del periodo de las cifras, junto al ano (control segmentado)."""
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


def _stat_entry(
    label: str, value_html: str, level: int, info_html: str = "", note: str = ""
) -> str:
    """Una cifra de la fila de estadisticas: la cifra arriba y su rotulo debajo.

    value_html ya viene escapado. La cifra va en el color del texto, con un
    cuadrito del tono que le corresponde delante (level_class). Si hay
    info_html, la cifra muestra un globo con ese texto al pasar el raton o
    al llegar con el tabulador.
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
        + (f'<span class="gritmap-note">{note}</span>' if note else "")
        + "</div>"
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
    return num_html(count) + " " + unit_html(unit_label(count, "day"))


def _current_streak_entry(stats: FullStats) -> str:
    """Racha actual; si es cero, cuanto hace de la ultima sesion, en gris."""
    if stats.current_streak == 0 and stats.last_session is not None:
        days = stats.last_session
        return _stat_entry(
            _label("last_session"), fill_html(plural_key("ago", days), count=num_html(days)), -1
        )
    # Desde 3.6.0, si hoy ya cuenta: la racha no se rompe por no haber
    # estudiado todavia hoy, asi que la cifra sola no lo dice.
    note = html.escape(t("today_done" if stats.today_done else "today_pending"))
    return _stat_entry(
        _label("current_streak"),
        _days_html(stats.current_streak),
        streak_level(stats.current_streak),
        note=note,
    )


def _longest_streak_entry(stats: FullStats) -> str:
    """Racha mas larga; con la distancia al record si esta cerca, o «nuevo
    record» el dia en que la racha actual lo supera (3.6.0)."""
    note = ""
    current = stats.current_streak
    if current > 0:
        gap = stats.longest_streak - current
        if stats.today_done and stats.previous_best >= 1 and current == stats.previous_best + 1:
            note = html.escape(t("new_record"))
        elif 0 < gap <= _RECORD_GAP_MAX:
            note = fill_html("record_gap", days=_days_html(gap))
    return _stat_entry(
        _label("longest_streak"),
        _days_html(stats.longest_streak),
        streak_level(stats.longest_streak),
        note=note,
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
    """Las cinco cifras en dos grupos, cada uno con su cabecera (3.6.0):

    * «Rachas»: racha actual y racha mas larga, que no dependen del periodo.
    * El selector de periodo encima de las tres cifras que cambia: promedio
      diario, dias estudiados y retencion. El control va junto a lo que
      controla (Norman, mapeo).
    """
    streaks_title = f'<span class="gritmap-gtitle">{html.escape(t("streaks"))}</span>'
    return (
        '<div class="gritmap-stats">'
        f'<div class="gritmap-group"><div class="gritmap-ghead">{streaks_title}</div>'
        '<div class="gritmap-gbody">'
        + _current_streak_entry(stats)
        + _longest_streak_entry(stats)
        + "</div></div>"
        + f'<div class="gritmap-group"><div class="gritmap-ghead">{_build_periods(window)}</div>'
        '<div class="gritmap-gbody">'
        + _average_entry(stats.average, measure, window)
        + _stat_entry(_label("days_learned"), pct_html(stats.studied_pct), pct_level(stats.studied_pct))
        + _retention_entry(stats.retention)
        + "</div></div></div>"
    )


_TIP = '<div id="gritmap-tip" role="tooltip"></div>'


def _message(key: str, action: str = "") -> str:
    """Aviso en lugar del mapa, con el boton de opciones para poder cambiarlas."""
    return (
        _build_nav(True, True, only_options=True)
        + f'<div class="gritmap-msg">{html.escape(t(key))}{action}</div>'
        + _TIP
    )


def _excluded_message() -> str:
    """Mazo excluido: el aviso y un boton que lleva directo a la lista de
    mazos excluidos, para poder deshacerlo sin buscar donde (3.6.0)."""
    button = (
        '<button type="button" class="gritmap-link" data-gritmap-btn="opts:exclude"'
        f' data-gritmap-cmd="opts:exclude">{html.escape(t("deck_excluded_btn"))}</button>'
    )
    return _message("deck_excluded", " " + button)


def build_widget_html(data: HeatmapData, cfg: Config, offset: int) -> str:
    if data.deck_excluded:
        return _excluded_message()
    key_labels = _key_labels(cfg.key_dates, data.today)
    # Sin nada que dibujar, el mapa se ensena igual, vacio y con hoy marcado,
    # y una frase explica que se ira pintando (3.6.0): el estado vacio
    # ensena lo que hara el complemento en lugar de parecer un error.
    empty = not data.past and not data.future_counts and not key_labels
    key_days = tuple(kd.day for kd in cfg.key_dates)
    min_year, max_year = year_bounds(data, key_days)
    year = max(min_year, min(max_year, data.today.year - offset))
    past_thresholds = legend_thresholds(scale_reference(data, cfg.measure))
    # Los dias futuros no dependen de la medida: siguen en gris segun las
    # tarjetas que vencen, con la escala de siempre (la de los repasos).
    future_thresholds = legend_thresholds(scale_reference(data, "reviews"))
    grid = (
        '<div class="gritmap-frame"><div class="gritmap-grid">'
        + _build_year_svg(data, cfg, year, past_thresholds, future_thresholds, key_labels)
        + "</div>"
    )
    if empty:
        return (
            _build_nav(True, True)
            + grid
            + _year_label(data, year, cfg, "")
            + "</div>"
            + f'<div class="gritmap-msg">{html.escape(t("empty_hint"))}</div>'
            + _TIP
        )
    stats = full_stats(data, cfg.measure, cfg.avg_window)
    return (
        _build_nav(year <= min_year, year >= max_year)
        + next_key_html(cfg.key_dates, data.today)
        + grid
        + _year_label(data, year, cfg, build_legend(data, cfg, year, past_thresholds))
        + "</div>"
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
    salto cuando llegan los datos: botones (28 px mas 8 de margen), proxima
    fecha clave si la hay (24), rejilla (20 de meses y siete filas de
    cuadritos), ano con la leyenda (28), cifras con su cabecera y sus notas
    (104) y un margen por si aparece la barra de desplazamiento (6).
    """
    svg_height = _TOP_MARGIN + 7 * (cfg.cell_size + _CELL_GAP)
    upcoming = any(kd.day >= date.today() for kd in cfg.key_dates)
    return 36 + (24 if upcoming else 0) + svg_height + 28 + 104 + 6


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
    """Comparativa de los 7 ultimos dias completos con los 7 anteriores.

    Desde 3.6.0 lleva su punto de referencia en una sola frase: «102 repasos
    en 7 dias · ▲ 15 mas que los 7 anteriores». Solo la diferencia toma el
    color de la subida (verde) o se queda en gris.
    """
    if not show:
        return None
    recent, previous, had_previous = week_totals(data, measure)
    if not had_previous:
        return None
    total = round_half_up(recent)
    rounded = round_half_up(recent - previous)
    if rounded > 0:
        cls, arrow = "up", "▲"
        delta = fill_html("week_more", count=num_html(rounded))
    elif rounded < 0:
        cls, arrow = "down", "▼"
        delta = fill_html("week_less", count=num_html(-rounded))
    else:
        cls, arrow = "flat", "●"
        delta = html.escape(t("week_same"))
    return {
        "cls": cls,
        "html": (
            " · " + fill_html("week_total", total=count_html(total, measure)) + " · "
            f'<span class="gritmap-wd-delta"><span aria-hidden="true">{arrow}</span> {delta}</span>'
        ),
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
    texts = {
        "none": t("tt_no_reviews"),
        "fnone": t("tt_no_due"),
        # Ultima linea del globo de los dias que se pueden pulsar (3.6.0).
        "click_past": t("tt_click_past"),
        "click_future": t("tt_click_future"),
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
