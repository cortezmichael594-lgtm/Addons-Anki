"""Ventana de opciones del complemento.

Version 4.9.0 (informe del cliente del 2026-10-26, aprobado el mismo dia): la
ventana es un panel a medida, hecho del mismo material que las tarjetas del
mapa. Es una pagina web dentro de la ventana (AnkiWebView, como las opciones
de mazo de Anki): tres tarjetas con titulo, controles propios y dos
subpaginas (mazos excluidos y fechas clave) dentro de la misma ventana, en
lugar de ventanas encima. La guia del taller pide controles estandar en
Opciones; este panel propio lo pidio el cliente de forma expresa.

Reparto del trabajo: la pagina (web/options.js) dibuja y gestiona lo que se
elige; aqui se prepara lo que necesita, se escriben los textos que dependen
de plurales y fechas (para que digan lo mismo que el mapa) y se valida y
guarda lo elegido al aceptar. Nada se guarda antes.

Criterio de idiomas: lo que Anki ya trae traducido (Cancelar, Eliminar,
Buscar, Anadir, Deshacer, Descartar) se toma de ahi.

La ventana se abre al instante con las opciones guardadas; la lista de mazos
se lee en segundo plano y llega despues, sin bloquear nada. Lo que se guarda
en la coleccion tambien se escribe en segundo plano.
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-08) — En modo noche, la muestra de color de cada tema
#                        ensenaba el tono del modo dia.
# FIX-016 (2026-10-13) — La ventana de excluir mazos no ensenaba lo que se
#                        excluye de verdad: contaba mazos que ya no existen y
#                        dejaba sin marcar los submazos excluidos.
# FIX-017 (2026-10-13) — Intro sobre un boton con el foco no lo pulsaba:
#                        cerraba Opciones o anadia una fecha.
# FIX-018 (2026-10-13) — Las muestras de color de los temas no cambiaban al
#                        pasar entre modo dia y noche con la ventana abierta.
# FIX-025 (2026-10-21) — Abierta desde la ventana Complementos, Opciones podia
#                        quedar detras de ella en Windows.
# FIX-028 (2026-10-26) — Al entrar en «Fechas clave», la cabecera quedaba fuera
#                        de la ventana y el pie a media altura.

from __future__ import annotations

import html
import json
import re
import unicodedata
from dataclasses import dataclass, replace
from datetime import date, timedelta
from typing import Any

from anki.collection import Collection
from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.qt import QCloseEvent, QDialog, QLocale, Qt, QVBoxLayout, QWidget, sip
from aqt.theme import theme_manager
from aqt.utils import disable_help_button, restoreGeom, saveGeom
from aqt.webview import AnkiWebView

from .config import (
    BORDER_RADIUS_MAX,
    BORDER_RADIUS_MIN,
    CELL_SIZE_MAX,
    CELL_SIZE_MIN,
    DEFAULT_CONFIG,
    FIT_WIDTH,
    GOAL_MAX,
    GOAL_MIN,
    GOAL_MODES,
    KEY_DATE_MAX,
    KEY_DATE_MIN,
    MAX_KEY_DATES,
    MAX_LABEL_LEN,
    MAX_PAUSE_DAYS,
    Config,
    KeyDate,
    clean_label,
    load_config,
    save_appearance,
    save_scoped,
)
from .data import WINDOWS, daily_average, full_stats, paused_days, round_half_up
from .decks import DeckEntry, all_deck_entries
from .errors import guarded, log_exception
from .i18n import anki_text, fill, lang, locale_code, plural_key, t, unit_label
from .palettes import PAST_DARK, PAST_LIGHT, THEME_NAMES
from .state import state
from .view import countdown_html

# Prefijo de los mensajes de la pagina de opciones (FIX-008: todo lo propio
# empieza por el nombre del paquete).
MSG_PREFIX = "gritmapopts:"
# Ancho fijo del panel y margen que se deja respecto al alto de la pantalla.
_WIDTH = 560
_SCREEN_MARGIN = 80
# Alto maximo de la ventana (4.10.0: ocupaba casi toda la pantalla); lo que no
# cabe se desplaza dentro del panel.
_MAX_HEIGHT = 720
# Nombres de mazo que caben en el resumen de «Excluir mazos».
_SUMMARY_NAMES = 3


@dataclass(frozen=True)
class _Decks:
    """Mazos leidos de la coleccion al abrir la ventana."""

    # Los que se pueden elegir, en el orden de la pantalla principal.
    selectable: list[DeckEntry]
    # Nombre de cada mazo que existe (tambien filtrados y el predeterminado
    # vacio): lo que de verdad puede excluir el mapa.
    existing: dict[int, str]


def _count_text(base: str, count: int) -> str:
    """«3 mazos excluidos», con la cifra a la manera del idioma."""
    if lang() == "es":
        number = f"{count:,}".replace(",", ".")
    else:
        number = QLocale().toString(count)
    return fill(plural_key(base, count), count=number)


def _plain(html_text: str) -> str:
    """Texto sin etiquetas (la cuenta atras del mapa viene en HTML)."""
    return html.unescape(re.sub(r"<[^>]+>", "", html_text))


def _theme_swatch_color(name: str) -> str:
    """Muestra del tema con el tono que se vera en el mapa ahora mismo."""
    # --- FIX-007 (2026-10-08) --------------------------------------
    # Sintoma: con Anki en modo noche, la muestra de cada tema en el desplegable
    #          ensenaba el tono de dia, distinto del que luego se ve en el mapa.
    # Causa: la muestra se tomaba siempre de la escala de dia.
    # Regla: toda muestra de color se toma de la escala del modo activo, leido
    #        en el momento de construir la ventana.
    # ---------------------------------------------------------------
    # Un solo cuadrito, como antes de la 4.0 (peticion del cliente, 4.3.0),
    # con el tercero de los cuatro tonos del tema.
    scale = PAST_DARK if theme_manager.night_mode else PAST_LIGHT
    return scale.get(name, scale[DEFAULT_CONFIG.theme])[2]


def _sorted_theme_names() -> list[str]:
    """Temas por orden alfabetico de su nombre en el idioma de Anki (4.10.0,
    peticion del cliente), sin distinguir tildes ni mayusculas."""
    def key(name: str) -> str:
        label = unicodedata.normalize("NFKD", t(f"theme_{name}"))
        return "".join(c for c in label if not unicodedata.combining(c)).casefold()

    return sorted(THEME_NAMES, key=key)


# Meta propuesta sin historial, en la unidad de cada medida (4.7.0).
_GOAL_FALLBACK = {"reviews": 50, "cards": 30, "new": 10}


def goal_proposal(measure: str, cfg: Config | None = None) -> tuple[int, int | None]:
    """Meta que se propone al elegir «Un numero» y el promedio del que sale.

    Desde la 4.9.0 se calcula con el mismo promedio que la tarjeta «Promedio
    diario» (por dia natural de los ultimos 30 dias), y la ventana lo dice:
    el 80 %, redondeado a 5 (Locke y Latham: una meta exigente pero
    alcanzable). Sin historial, un valor prudente y sin promedio.
    """
    entry = state.data
    average = None
    if entry is not None and not entry.current_deck_only and entry.measure == measure:
        pause = cfg.pause if cfg is not None else None
        average = daily_average(entry.data, measure, 30, paused_days(pause, entry.data.today))
    if not average:
        return _GOAL_FALLBACK.get(measure, DEFAULT_CONFIG.goal), None
    value = max(GOAL_MIN, min(GOAL_MAX, 5 * max(1, round(average * 0.8 / 5))))
    return value, round_half_up(average)


# Historial de la meta (4.11.0): 14 dias completos, y solo si hay al menos 7
# con datos de ese tipo de meta (criterio del informe, sin estudio que lo fije).
_HISTORY_DAYS = 14
_HISTORY_MIN = 7


def goal_history(cfg: Config) -> dict[str, dict[str, str]]:
    """Por tipo de meta, «Cumplida 12 de los últimos 14 días.» y, con
    «Terminar lo de hoy» cumplida la mitad de los dias o menos, el consejo
    de bajar las nuevas. Solo cuentan los dias en que GritMap vio esa meta
    (los dias sin datos no son fallos) y no los de pausa."""
    entry = state.data
    if entry is None:
        return {}
    today = entry.data.today
    paused = paused_days(cfg.pause, today)
    out: dict[str, dict[str, str]] = {}
    for mode in GOAL_MODES[1:]:
        marks = []
        for days_ago in range(1, _HISTORY_DAYS + 1):
            if days_ago in paused:
                continue
            mark = entry.data.goal_days.get((today - timedelta(days=days_ago)).isoformat())
            if mark is not None and mark[0] == mode:
                marks.append(mark[1])
        if len(marks) < _HISTORY_MIN:
            continue
        met = sum(marks)
        total = len(marks)
        days = f"{total} {unit_label(total, 'day')}"
        item = {"text": fill("goal_history", met=met, days=days), "advice": ""}
        if mode == "due" and met * 2 <= total:
            item["advice"] = t("goal_advice")
        out[mode] = item
    return out


def _freezes_now(cfg: Config) -> str:
    """«Ahora tiene 1 comodín.», o nada si no se sabe (pantalla de un mazo)."""
    entry = state.data
    if entry is None or entry.current_deck_only:
        return ""
    paused = paused_days(cfg.pause, entry.data.today)
    stats = full_stats(entry.data, entry.measure, cfg.avg_window, True, paused)
    count = stats.freezes_left
    return fill("freezes_now", freezes=fill(plural_key("freeze", count), count=count))


def _unit_word(measure: str) -> str:
    """Unidad de la medida en plural, para el campo de la meta."""
    if measure == "new":
        return t("unit_new_other")
    return t("unit_card_other" if measure == "cards" else "unit_review_other")


def _without_px(key: str) -> str:
    """Rotulo sin «(px)», si el texto ya lo traia."""
    return re.sub(r"\s*\(px\)", "", t(key))


def _texts() -> dict[str, str]:
    """Textos de la pagina: los propios y los que ya trae Anki."""
    own = (
        "nav_opts", "grp_look", "grp_count", "grp_goals", "opt_restore_look", "look_live",
        "opt_theme", "opt_map_size", "size_fit", "radius_max", "fit_note",
        "opt_window", "window_help", "applied_on_ok", "opt_exclude", "opt_show_streak",
        "streak_off_note", "opt_goal", "goal_unit_day", "goal_proposal_line2", "goal_due_note",
        "goal_number_note", "plan_label", "plan_ph",
        "opt_freezes", "freeze_tip", "opt_pause", "pause_from", "pause_to", "pause_rule",
        "opt_key_dates", "opt_save", "opt_cancel", "discard_q", "discard_body", "keep_editing",
        "decks_sub_note", "decks_no_match", "kd_new", "kd_field_name", "kd_field_date", "kd_name_ph",
        "kd_name_required", "kd_duplicate", "kd_limit", "kd_count", "kd_deleted", "kd_edit",
        "month_prev", "month_next", "loading",
    )
    texts = {key: t(key) for key in own}
    texts["opt_radius"] = _without_px("opt_radius")
    texts["undo"] = anki_text("undo_undo", "w_undo")
    texts["search"] = anki_text("actions_search", "opt_exclude_btn")
    texts["add"] = anki_text("actions_add", "kd_add")
    texts["delete"] = anki_text("actions_delete", "kd_remove")
    texts["save"] = anki_text("actions_save", "opt_save")
    texts["discard"] = anki_text("actions_discard", "w_discard")
    return texts


def _payload(cfg: Config, start: str) -> dict[str, Any]:
    """Todo lo que la pagina necesita para dibujarse entera antes de verse."""
    value, average = goal_proposal(cfg.measure, cfg)
    retired = ""
    if cfg.retired_theme:
        # El tema guardado se retiro en la 4.0.0: se dice una vez, sin
        # preguntar (Hopkins, M3: avisar al cambiar las reglas).
        retired = fill("theme_retired", old=t(f"theme_{cfg.retired_theme}"), new=t(f"theme_{cfg.theme}"))
    today = date.today()
    pause = None
    if cfg.pause is not None:
        pause = {"start": cfg.pause[0].isoformat(), "end": cfg.pause[1].isoformat()}
    return {
        "prefix": MSG_PREFIX,
        "locale": locale_code(),
        "today": today.isoformat(),
        "start": start,
        "texts": _texts(),
        "themes": [
            {"name": name, "label": t(f"theme_{name}"), "color": _theme_swatch_color(name)}
            for name in _sorted_theme_names()
        ],
        "unit": _unit_word(cfg.measure),
        "windows": [
            {"id": days, "label": t("window_all") if days == 0 else fill("window_days", count=days)}
            for days in WINDOWS
        ],
        "goal_modes": [{"id": mode, "label": t(f"goal_{mode}")} for mode in GOAL_MODES],
        "proposal": {"value": value, "average": average},
        "freezes_now": _freezes_now(cfg),
        "goal_history": goal_history(cfg),
        "retired": retired,
        "defaults": {
            "theme": DEFAULT_CONFIG.theme,
            "cell_size": DEFAULT_CONFIG.cell_size,
            "border_radius": DEFAULT_CONFIG.border_radius,
        },
        "limits": {
            "cell_min": CELL_SIZE_MIN,
            "cell_max": CELL_SIZE_MAX,
            "radius_min": BORDER_RADIUS_MIN,
            "radius_max": BORDER_RADIUS_MAX,
            "goal_min": GOAL_MIN,
            "goal_max": GOAL_MAX,
            "max_pause": MAX_PAUSE_DAYS,
            "max_key_dates": MAX_KEY_DATES,
            "max_label": MAX_LABEL_LEN,
            "date_min": KEY_DATE_MIN.isoformat(),
            "date_max": KEY_DATE_MAX.isoformat(),
            # La pausa empieza hoy como pronto (4.7.0, decision del cliente);
            # una pausa guardada que ya empezo conserva su inicio.
            "pause_min": min(today, cfg.pause[0]).isoformat() if cfg.pause else today.isoformat(),
        },
        "cfg": {
            "theme": cfg.theme,
            "cell_size": cfg.cell_size,
            "border_radius": cfg.border_radius,
            "avg_window": cfg.avg_window,
            "goal_mode": cfg.goal_mode,
            "goal": cfg.goal,
            "freezes": cfg.freezes,
            "show_streak": cfg.show_streak,
            "study_plan": cfg.study_plan,
            "pause": pause,
            "excluded": list(cfg.excluded_decks),
            "key_dates": [{"day": kd.day.isoformat(), "label": kd.label} for kd in cfg.key_dates],
        },
    }


def _script_safe(payload: str) -> str:
    """JSON que se puede poner dentro de <script> sin cerrarlo antes de tiempo."""
    return payload.replace("</", "<\\/").replace("<!--", "<\\u0021--")


def _as_day(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def _as_int(value: object, fallback: int, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return fallback
    return max(low, min(high, int(value)))


def config_from_page(base: Config, chosen: dict[str, Any], existing: dict[int, str] | None) -> Config:
    """Lo elegido en la pagina, validado, sobre la configuracion con la que se
    abrio (que conserva lo que la pagina no toca). Nada de lo que llega de la
    pagina se usa sin comprobarlo."""
    theme = chosen.get("theme")
    cell = _as_int(chosen.get("cell_size"), base.cell_size, FIT_WIDTH, CELL_SIZE_MAX)
    if cell != FIT_WIDTH:
        cell = max(CELL_SIZE_MIN, cell)
    half = (14 if cell == FIT_WIDTH else cell) // 2
    radius = _as_int(chosen.get("border_radius"), base.border_radius, BORDER_RADIUS_MIN, min(BORDER_RADIUS_MAX, half))
    window = chosen.get("avg_window")
    mode = chosen.get("goal_mode")

    excluded = base.excluded_decks
    raw_excluded = chosen.get("excluded")
    if isinstance(raw_excluded, list) and existing is not None:
        # FIX-016: solo los mazos que existen; los demas se dejan de guardar.
        excluded = tuple(dict.fromkeys(d for d in raw_excluded if isinstance(d, int) and d in existing))

    key_dates = base.key_dates
    raw_dates = chosen.get("key_dates")
    if isinstance(raw_dates, list):
        found: list[KeyDate] = []
        for item in raw_dates:
            if not isinstance(item, dict):
                continue
            day = _as_day(item.get("day"))
            label = clean_label(item.get("label"))
            if day is None or not label or not KEY_DATE_MIN <= day <= KEY_DATE_MAX:
                continue
            key_date = KeyDate(day=day, label=label)
            if key_date not in found:
                found.append(key_date)
        found.sort(key=lambda kd: (kd.day, kd.label.casefold()))
        key_dates = tuple(found[:MAX_KEY_DATES])

    pause = None
    raw_pause = chosen.get("pause")
    if isinstance(raw_pause, dict):
        start = _as_day(raw_pause.get("start"))
        end = _as_day(raw_pause.get("end"))
        earliest = min(date.today(), base.pause[0]) if base.pause else date.today()
        if start is not None and end is not None and start >= earliest:
            end = max(start, min(end, start + timedelta(days=MAX_PAUSE_DAYS - 1)))
            pause = (start, end)

    return replace(
        base,
        theme=theme if isinstance(theme, str) and theme in THEME_NAMES else base.theme,
        cell_size=cell,
        border_radius=radius,
        avg_window=window if isinstance(window, int) and window in WINDOWS else base.avg_window,
        goal_mode=mode if isinstance(mode, str) and mode in GOAL_MODES else base.goal_mode,
        goal=_as_int(chosen.get("goal"), base.goal, GOAL_MIN, GOAL_MAX),
        freezes=bool(chosen.get("freezes", base.freezes)),
        show_streak=bool(chosen.get("show_streak", base.show_streak)),
        study_plan=clean_label(chosen.get("study_plan", base.study_plan)),
        excluded_decks=excluded,
        key_dates=key_dates,
        pause=pause,
        retired_theme="",
    )


def summary_texts(chosen: dict[str, Any], existing: dict[int, str] | None) -> dict[str, Any]:
    """Textos que dependen de plurales y fechas, escritos como en el mapa.

    Los resumenes de «Excluir mazos» y «Fechas clave» quedan escritos en sus
    filas (4.9.0), en lugar de en un globo (Norman: lo que hay que descubrir
    pasando el raton casi no se usa).
    """
    today = date.today()
    result: dict[str, Any] = {"decks": None, "dates": "", "countdowns": {}, "pause_days": ""}
    raw_excluded = chosen.get("excluded")
    if existing is not None and isinstance(raw_excluded, list):
        # FIX-016: solo se cuentan y se nombran mazos que existen.
        # El nombre del mazo, sin la ruta de sus padres («Inglés», no
        # «Idiomas::Inglés»).
        names = [existing[d].split("::")[-1] for d in raw_excluded if isinstance(d, int) and d in existing]
        if not names:
            result["decks"] = t("sum_none_m")
        else:
            shown = ", ".join(names[:_SUMMARY_NAMES])
            if len(names) > _SUMMARY_NAMES:
                shown += " " + fill("deck_more", count=len(names) - _SUMMARY_NAMES)
            result["decks"] = f"{_count_text('opt_exclude_count', len(names))}: {shown}"
    days: list[tuple[date, str]] = []
    for item in chosen.get("key_dates") or []:
        if isinstance(item, dict):
            day = _as_day(item.get("day"))
            if day is not None:
                days.append((day, str(item.get("label", ""))))
                left = (day - today).days
                result["countdowns"][day.isoformat()] = (
                    _plain(countdown_html(left)) if left >= 0 else f"({t('kd_past')})"
                )
    if not days:
        result["dates"] = t("sum_none_f")
    else:
        count = _count_text("opt_key_dates_count", len(days))
        upcoming = sorted((d, label) for d, label in days if d >= today)
        if upcoming:
            day, label = upcoming[0]
            when = _plain(countdown_html((day - today).days))
            result["dates"] = fill("kd_summary_next", dates=count, name=label, when=when)
        else:
            result["dates"] = fill("kd_all_past", dates=count)
    raw_pause = chosen.get("pause")
    if isinstance(raw_pause, dict):
        start, end = _as_day(raw_pause.get("start")), _as_day(raw_pause.get("end"))
        if start is not None and end is not None and end >= start:
            span = (end - start).days + 1
            result["pause_days"] = f"{span} {unit_label(span, 'day')}"
    return result


class HeatmapOptionsDialog(QDialog):
    """Panel de opciones a medida (4.9.0): una pagina dentro de la ventana."""

    def __init__(self, parent: QWidget, cfg: Config, start: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_title"))
        disable_help_button(self)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self._base = cfg
        self._decks: _Decks | None = None
        self._ready = False
        self._closing = False
        # Ordenes para la pagina que llegan antes de que este lista.
        self._pending: list[str] = []
        self.result_config: Config | None = None

        self._web = AnkiWebView(self, title="gritmap options")
        self._web.set_bridge_command(self._on_bridge, self)
        # La pagina no se ensena hasta que esta dibujada entera: sin
        # parpadeos (guia, apartado 4). Mientras, se ve el fondo de Anki.
        self._web.hide()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._web)

        self.setMinimumWidth(_WIDTH)
        restoreGeom(self, "gritmapPanel", default_size=(_WIDTH, 640))
        self.resize(_WIDTH, self.height())

        package = mw.addonManager.addon_from_module(__name__)
        payload = _script_safe(json.dumps(_payload(cfg, start), ensure_ascii=False))
        body = (
            '<div id="gritmap-o-app"></div>'
            f"<script>GritMapOptions.init({payload});</script>"
        )
        self._web.stdHtml(
            body,
            css=[f"/_addons/{package}/web/options.css"],
            js=[f"/_addons/{package}/web/options.js"],
            context=self,
        )
        gui_hooks.theme_did_change.append(self._refresh_swatches)
        # Por si la pagina no llegara a avisar de que esta lista: a los 3 s se
        # ensena igualmente, en lugar de dejar la ventana vacia.
        mw.progress.single_shot(3000, self._show_anyway, False)

    @guarded()
    def _show_anyway(self) -> None:
        if not sip.isdeleted(self) and not self._ready:
            self._ready = True
            for js in self._pending:
                self._web.eval(js)
            self._pending.clear()
            self._web.show()

    # Mazos, leidos en segundo plano
    # --- FIX-016 (2026-10-13) --------------------------------------
    # Sintoma: al excluir «Idiomas», sus submazos seguian sin marcar en la
    #          lista aunque el mapa ya no los contaba, y el boton decia «3
    #          mazos excluidos» cuando uno de ellos ya no existia.
    # Causa: cada mazo tenia su casilla suelta, sin reflejar a sus submazos, y
    #        la cifra contaba los identificadores guardados, no los mazos que
    #        existen.
    # Regla: lo que ensena la ventana es exactamente lo que excluye el mapa:
    #        un mazo marcado marca y bloquea a sus submazos, y solo se cuentan
    #        y se nombran mazos que existen.
    # ---------------------------------------------------------------
    # Desde la 4.9.0 la lista la dibuja la pagina (web/options.js), con la
    # misma regla; aqui se le pasan los mazos que existen y, al aceptar, solo
    # se guardan esos.
    def set_decks(self, decks: _Decks) -> None:
        self._decks = decks
        entries = [
            {"id": e.deck_id, "name": e.name, "leaf": e.leaf_name, "depth": e.depth} for e in decks.selectable
        ]
        selectable = {e.deck_id for e in decks.selectable}
        # Excluidos que existen pero no salen en la lista (un mazo filtrado o
        # el predeterminado vacio): se conservan tal cual al aceptar.
        hidden = [d for d in self._base.excluded_decks if d in decks.existing and d not in selectable]
        data = {"decks": entries, "hidden": hidden, "existing": [int(d) for d in decks.existing]}
        self._run(f"GritMapOptions.setDecks({_script_safe(json.dumps(data, ensure_ascii=False))});")

    def _run(self, js: str) -> None:
        if self._ready:
            self._web.eval(js)
        else:
            self._pending.append(js)

    # Mensajes de la pagina
    def _on_bridge(self, cmd: str) -> Any:
        if not cmd.startswith(MSG_PREFIX):
            return None
        action, _sep, arg = cmd[len(MSG_PREFIX):].partition(":")
        try:
            return self._handle(action, arg)
        except Exception as exc:
            log_exception(f"options.bridge.{action}", exc)
            return None

    def _handle(self, action: str, arg: str) -> Any:
        if action == "ready":
            self._ready = True
            self._fit_height(arg)
            for js in self._pending:
                self._web.eval(js)
            self._pending.clear()
            self._web.show()
            self._web.setFocus()
            return None
        if action == "texts":
            existing = self._decks.existing if self._decks is not None else None
            return summary_texts(json.loads(arg), existing)
        if action == "preview":
            if state.preview_config is not None:
                existing = self._decks.existing if self._decks is not None else None
                state.preview_config(config_from_page(self._base, json.loads(arg), existing))
            return None
        if action == "accept":
            existing = self._decks.existing if self._decks is not None else None
            self.result_config = config_from_page(self._base, json.loads(arg), existing)
            self._closing = True
            self.accept()
            return None
        if action == "cancel":
            self._closing = True
            QDialog.reject(self)
            return None
        return None

    # --- FIX-028 (2026-10-26) ---
    # Sintoma: al pulsar «Fechas clave», la cabecera desaparecia por arriba y
    #          Aceptar y Cancelar quedaban a media ventana, con un hueco vacio
    #          debajo.
    # Causa: la ventana cambiaba de alto al entrar en cada subpagina y la pagina
    #        entera podia desplazarse al llevar el foco a un campo.
    # Regla: el alto de la ventana se fija una vez al abrir y la pagina entera
    #        nunca se desplaza: solo el cuerpo del panel.
    # ---------------------------------------------------------------
    def _fit_height(self, raw: str) -> None:
        """El alto es el de la pagina principal, hasta 720 px o el de la
        pantalla menos 80 px, y se fija una vez al abrir (4.10.0); si algo no
        cabe, la pagina desplaza su cuerpo y deja fijos la cabecera y el pie."""
        try:
            wanted = int(float(raw))
        except ValueError:
            return
        screen = self.screen()
        limit = screen.availableGeometry().height() - _SCREEN_MARGIN if screen is not None else wanted
        limit = min(limit, _MAX_HEIGHT)
        self.resize(self.width(), max(240, min(wanted, limit)))

    # Cerrar: Esc, la cruz de la ventana o Cancelar pasan por la pagina, que
    # pregunta antes de descartar fechas clave escritas (4.9.0).
    def reject(self) -> None:
        if self._closing or not self._ready:
            QDialog.reject(self)
            return
        self._web.eval("GritMapOptions.requestCancel();")

    def closeEvent(self, event: QCloseEvent | None) -> None:  # noqa: N802 (nombre de Qt)
        if self._closing or not self._ready:
            super().closeEvent(event)
            return
        if event is not None:
            event.ignore()
        self.reject()

    # --- FIX-018 (2026-10-13) --------------------------------------
    # Sintoma: con la ventana abierta, al pasar Anki de modo dia a noche (o al
    #          reves) las muestras de los temas seguian con los tonos del modo
    #          anterior.
    # Causa: las muestras se pintaban una sola vez, al construir la ventana.
    # Regla: todo color que dependa del modo se vuelve a pintar con
    #        gui_hooks.theme_did_change, y el gancho se quita al cerrar la
    #        ventana (nunca desde dentro del propio gancho).
    # ---------------------------------------------------------------
    @guarded()
    def _refresh_swatches(self) -> None:
        colors_now = {name: _theme_swatch_color(name) for name in THEME_NAMES}
        self._run(f"GritMapOptions.setSwatches({json.dumps(colors_now)});")

    def done(self, result: int) -> None:
        # remove no falla si ya se quito antes.
        gui_hooks.theme_did_change.remove(self._refresh_swatches)
        try:
            saveGeom(self, "gritmapPanel")
        except Exception as exc:
            log_exception("options.HeatmapOptionsDialog.done", exc)
        self._web.cleanup()
        super().done(result)


# --- FIX-017 (2026-10-13) --------------------------------------
# Sintoma: con el foco en «Seleccionar mazos» o en Restaurar, Intro
#          cerraba Opciones y guardaba; en Fechas clave, con el foco en
#          Aceptar, Intro intentaba anadir una fecha.
# Causa: se les habia quitado a esos botones la respuesta a Intro
#        (autoDefault), y entonces Intro iba al boton por defecto.
# Regla: los botones conservan la respuesta a Intro que les da Qt; solo
#        se elige cual es el boton por defecto.
# ---------------------------------------------------------------
# Desde la 4.9.0 los botones son de la pagina (web/options.js): son <button>
# de verdad, sin ningun manejador de Intro propio, asi que Intro pulsa el que
# tiene el foco; solo en el campo del nombre de una fecha clave Intro anade.

# Se conserva una referencia mientras la ventana existe: sin ella Python
# podria destruir el objeto y la ventana desapareceria sola.
_dialog: HeatmapOptionsDialog | None = None


def _parent_window() -> QWidget:
    """Ventana sobre la que se abre Opciones."""
    # --- FIX-025 (2026-10-21) --------------------------------------
    # Sintoma: abierta desde Herramientas > Complementos > Configuracion, la
    #          ventana de opciones podia quedar detras de la ventana
    #          Complementos en Windows.
    # Causa: se creaba siempre con la ventana principal de Anki como padre.
    # Regla: una ventana que se abre desde otra toma como padre la ventana
    #        activa (mw.app.activeWindow() or mw), comprobando antes de usarla
    #        que no se haya cerrado entretanto (APR-063).
    # ---------------------------------------------------------------
    return mw.app.activeWindow() or mw


def open_options(start: str = "") -> None:
    """Abre el panel al instante con las opciones guardadas y lee los mazos
    en segundo plano.

    Con start, al abrirse muestra ademas una de sus subpaginas: "exclude"
    (mazos excluidos) o "keydates" (fechas clave).
    """
    global _dialog
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    if mw.col is None:
        return
    parent = _parent_window()
    if sip.isdeleted(parent) or not parent.isVisible():
        parent = mw
    try:
        cfg = load_config()
        dialog = HeatmapOptionsDialog(parent, cfg, start)
    except Exception as exc:
        log_exception("options.open_options", exc)
        return
    _dialog = dialog
    dialog.finished.connect(lambda result: _on_finished(dialog, cfg, result))
    dialog.open()
    _read_decks(dialog)


def _read_decks(dialog: HeatmapOptionsDialog) -> None:
    generation = state.generation

    def op(col: Collection) -> _Decks:
        selectable = all_deck_entries(col, skip_empty_default=True, include_filtered=False)
        existing = {entry.deck_id: entry.name for entry in all_deck_entries(col)}
        return _Decks(selectable=selectable, existing=existing)

    @guarded()
    def on_success(decks: _Decks) -> None:
        if generation != state.generation or sip.isdeleted(dialog) or _dialog is not dialog:
            return
        dialog.set_decks(decks)

    @guarded()
    def on_failure(exc: Exception) -> None:
        log_exception("options.read_decks", exc)

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()


@guarded()
def _on_finished(dialog: HeatmapOptionsDialog, cfg: Config, result: int) -> None:
    global _dialog
    selected = dialog.result_config if result == QDialog.DialogCode.Accepted else None
    if _dialog is dialog:
        _dialog = None
    dialog.deleteLater()
    if selected is not None:
        _save(selected)
    elif state.preview_config is not None:
        # Cancelado: el mapa vuelve a como estaba antes de mover nada.
        state.preview_config(None)
    if selected is None and cfg.retired_theme:
        # El aviso del tema retirado sale una sola vez: se guarda el tema
        # nuevo aunque se cancele.
        save_appearance(cfg)


def _save(selected: Config) -> None:
    """Guarda la apariencia aqui y lo de la coleccion en segundo plano; despues,
    el mapa se redibuja en su sitio."""
    save_appearance(selected)
    generation = state.generation

    def op(col: Collection) -> None:
        save_scoped(col, selected)

    @guarded()
    def on_success(_result: None) -> None:
        if generation == state.generation and state.apply_config_change is not None:
            state.apply_config_change()

    @guarded()
    def on_failure(exc: Exception) -> None:
        log_exception("options.save", exc)

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()
