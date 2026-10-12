"""Registro en Anki y coordinacion de todo lo demas.

Este modulo es el unico que habla con los hooks de Anki. Todas las funciones
conectadas a un hook van protegidas con @guarded: si algo fallara, queda
anotado en el registro del complemento y Anki sigue funcionando con
normalidad, en lugar de mostrar un volcado tecnico.

El calculo del mapa siempre ocurre en segundo plano (QueryOp), nunca en el
hilo de la interfaz, de modo que la ventana no se queda congelada ni con una
coleccion muy grande.
"""

from __future__ import annotations

from datetime import date

import aqt
from anki.collection import Collection
from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.operations import QueryOp
from aqt.overview import Overview, OverviewContent
from aqt.qt import QTimer
from aqt.webview import WebContent

from . import config, i18n, view
from .config import load_config
from .data import HeatmapData, days_offset, fetch_data, year_bounds
from .decks import build_scope, day_search
from .errors import guarded, guarded_filter, log_exception
from .options import open_options
from .state import state
from .view import MSG_PREFIX

WEB_PATTERN = r"web/.*\.(css|js)"


def _package() -> str:
    return mw.addonManager.addon_from_module(__name__)


# Dibujado del mapa
# ---------------------------------------------------------------------------


def _schedule_render(current_deck_only: bool) -> None:
    """Pide los datos en segundo plano y dibuja el mapa cuando lleguen."""
    if mw.col is None:
        return
    cfg = load_config()
    token, generation = state.new_render_token()
    screen = mw.state
    show_week = (not current_deck_only) and cfg.show_week_diff
    excluded = cfg.excluded_decks

    def op(col: Collection) -> HeatmapData:
        scope = build_scope(col, excluded, current_deck_only)
        return fetch_data(col, scope)

    def on_success(data: HeatmapData) -> None:
        # Descarta el resultado si entretanto se pidio otro dibujado, si se
        # cambio de perfil o si la persona ya no esta en la misma pantalla.
        if not state.is_current(token, generation) or mw.col is None or mw.state != screen:
            return
        try:
            key_days = tuple(kd.day for kd in cfg.key_dates)
            min_year, max_year = year_bounds(data, key_days)
            offset = max(
                data.today.year - max_year,
                min(state.year_offset, data.today.year - min_year),
            )
            state.year_offset = offset
            view.render(
                view.build_widget_html(data, cfg, offset),
                measure=cfg.measure,
                week=view.week_payload(data, cfg.measure, show_week),
            )
        except Exception as exc:
            log_exception("controller.on_success", exc)
            view.render_error()

    def on_failure(exc: Exception) -> None:
        log_exception("controller.fetch_data", exc)
        if state.is_current(token, generation) and mw.state == screen:
            view.render_error()

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()


def _current_deck_only() -> bool | None:
    """True en la pantalla de un mazo, False en la lista, None fuera de ambas."""
    if mw.state == "deckBrowser":
        return False
    if mw.state == "overview":
        return True
    return None


def _rerender_in_place() -> None:
    """Redibuja el mapa dentro del hueco que ya ocupa.

    A diferencia de recargar la pantalla completa, el mapa anterior permanece
    visible mientras se calculan los datos nuevos y se sustituye de una vez.
    Asi no hay parpadeo al cambiar de ano, de tema o de cualquier opcion.
    """
    if mw.col is None:
        return
    current_deck_only = _current_deck_only()
    if current_deck_only is None:
        return
    _schedule_render(current_deck_only)


# Hooks de contenido
# ---------------------------------------------------------------------------


@guarded()
def _on_webview_will_set_content(web_content: WebContent, context: object) -> None:
    """Engancha la hoja de estilos, el codigo y la paleta a la pagina.

    Al viajar con la propia pagina, el mapa nunca se ve un instante sin estilo
    y no hace falta reenviar nada en cada dibujado.
    """
    if not isinstance(context, (DeckBrowser, Overview)):
        return
    package = _package()
    web_content.css.append(f"/_addons/{package}/web/gritmap.css")
    web_content.js.append(f"/_addons/{package}/web/gritmap.js")
    web_content.head += view.palette_style_tag(load_config())


@guarded()
def _on_deck_browser_render(_deck_browser: DeckBrowser, content: DeckBrowserContent) -> None:
    if mw.col is None:
        return
    content.stats += view.placeholder_html(load_config())
    _schedule_render(current_deck_only=False)


@guarded()
def _on_overview_render(_overview: Overview, content: OverviewContent) -> None:
    if mw.col is None:
        return
    content.table += view.placeholder_html(load_config())
    _schedule_render(current_deck_only=True)


# Apertura del navegador de tarjetas
# ---------------------------------------------------------------------------


def _open_day_in_browser(day_iso: str, current_deck_only: bool, future: bool) -> None:
    """Abre el navegador con la busqueda propia de Anki para ese dia.

    Se envia una busqueda (prop:rated / prop:due mas los mazos), no una lista
    de tarjetas: no hay limite de resultados y la persona puede leerla y
    retocarla en la barra de busqueda.
    """
    if mw.col is None:
        return
    try:
        day = date.fromisoformat(day_iso)
    except ValueError:
        return
    excluded = load_config().excluded_decks
    generation = state.generation

    def op(col: Collection) -> str:
        scope = build_scope(col, excluded, current_deck_only)
        offset = days_offset(col, day)
        if future:
            return day_search(col, scope, -offset, future=True)
        return day_search(col, scope, offset, future=False)

    def on_success(search: str) -> None:
        # Si entretanto se cambio de usuario, la busqueda pertenece a otra
        # coleccion y no debe abrirse.
        if mw.col is None or generation != state.generation:
            return
        try:
            browser = aqt.dialogs.open("Browser", mw, search=(search,))
            browser.activateWindow()
        except Exception as exc:
            log_exception("controller.open_browser", exc)

    def on_failure(exc: Exception) -> None:
        log_exception("controller.day_search", exc)

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()


# Mensajes desde la pagina
# ---------------------------------------------------------------------------


@guarded_filter
def _on_js_message(
    handled: tuple[bool, object], message: str, context: object
) -> tuple[bool, object]:
    if not message.startswith(MSG_PREFIX):
        return handled
    if not isinstance(context, (DeckBrowser, Overview)):
        return handled

    action = message[len(MSG_PREFIX):]
    current_deck_only = isinstance(context, Overview)

    if action in ("prev", "next", "today"):
        if action == "prev":
            state.year_offset += 1
        elif action == "next":
            state.year_offset -= 1
        else:
            state.year_offset = 0
        _schedule_render(current_deck_only)
        return (True, None)

    if action == "opts":
        # Se aplaza para que el mensaje de la pagina termine antes de abrir
        # una ventana modal.
        QTimer.singleShot(0, open_options)
        return (True, None)

    if action.startswith("past:"):
        _open_day_in_browser(action[len("past:"):], current_deck_only, future=False)
        return (True, None)

    if action.startswith("future:"):
        _open_day_in_browser(action[len("future:"):], current_deck_only, future=True)
        return (True, None)

    return handled


# Perfil y configuracion
# ---------------------------------------------------------------------------


@guarded()
def _on_profile_did_open() -> None:
    """Punto de partida limpio para cada usuario.

    Se olvida todo lo del perfil anterior (idioma, ajustes en cache, ano que
    se estaba mirando) y se invalidan los calculos que pudieran seguir en
    marcha, que es lo que podia provocar errores al cambiar de usuario.
    """
    i18n.reset()
    config.invalidate_cache()
    state.start_new_generation()
    config.migrate_to_collection()


@guarded()
def _on_profile_will_close() -> None:
    state.start_new_generation()
    config.invalidate_cache()


@guarded()
def _apply_config_change() -> None:
    """Aplica un cambio de opciones sin recargar la pantalla.

    Se llama tanto al guardar en el dialogo propio como al editar la
    configuracion desde Anki. Si en ese momento no se esta en una pantalla con
    mapa no hay nada que hacer: al volver, la pagina se construye ya con los
    colores nuevos.
    """
    config.invalidate_cache()
    state.year_offset = 0
    if _current_deck_only() is None:
        return
    view.update_palette(load_config())
    _rerender_in_place()


@guarded()
def _on_config_updated(_new_config: dict[str, object]) -> None:
    _apply_config_change()


# Registro
# ---------------------------------------------------------------------------


def register() -> None:
    state.apply_config_change = _apply_config_change
    mw.addonManager.setWebExports(__name__, WEB_PATTERN)
    gui_hooks.webview_will_set_content.append(_on_webview_will_set_content)
    gui_hooks.deck_browser_will_render_content.append(_on_deck_browser_render)
    gui_hooks.overview_will_render_content.append(_on_overview_render)
    gui_hooks.webview_did_receive_js_message.append(_on_js_message)
    gui_hooks.profile_did_open.append(_on_profile_did_open)
    gui_hooks.profile_will_close.append(_on_profile_will_close)
    mw.addonManager.setConfigAction(__name__, open_options)
    mw.addonManager.setConfigUpdatedAction(__name__, _on_config_updated)
