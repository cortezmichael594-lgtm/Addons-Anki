"""Registro en Anki y coordinacion de todo lo demas.

Este modulo es el unico que habla con los hooks de Anki. Todas las funciones
conectadas a un hook van protegidas con @guarded: si algo fallara, queda
anotado en el registro del complemento y Anki sigue funcionando con
normalidad, en lugar de mostrar un volcado tecnico.

El calculo del mapa siempre ocurre en segundo plano (QueryOp), nunca en el
hilo de la interfaz, de modo que la ventana no se queda congelada ni con una
coleccion muy grande. Los datos calculados se reutilizan para cambiar de ano
o de aspecto, y el ultimo mapa de cada pantalla se vuelve a ensenar al
instante cuando Anki la redibuja, mientras se calculan los datos al dia.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import date

import aqt
from anki.collection import Collection
from anki.decks import DeckId, DeckTreeNode
from aqt import gui_hooks, mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserContent
from aqt.operations import QueryOp
from aqt.overview import Overview, OverviewContent
from aqt.webview import WebContent

from . import config, i18n, view
from .config import DEFAULT_CONFIG, Config, load_config
from .data import WINDOWS, HeatmapData, days_offset, fetch_data, window_average, year_bounds
from .decks import DeckScope, build_scope, day_search
from .errors import guarded, guarded_filter, log_exception
from .options import open_goal_dialog, open_options
from .state import DataEntry, state
from .view import MSG_PREFIX, WEB_PATTERN


def _package() -> str:
    return mw.addonManager.addon_from_module(__name__)


# Dibujado del mapa
# ---------------------------------------------------------------------------


def _current_deck_only() -> bool | None:
    """True en la pantalla de un mazo, False en la lista, None fuera de ambas."""
    if mw.state == "deckBrowser":
        return False
    if mw.state == "overview":
        return True
    return None


def _usable(entry: DataEntry | None, current_deck_only: bool, cfg: Config) -> bool:
    """Si los datos guardados sirven para dibujar esta pantalla con estas opciones."""
    return (
        entry is not None
        and entry.generation == state.generation
        and entry.current_deck_only == current_deck_only
        and set(entry.excluded_decks) == set(cfg.excluded_decks)
        and entry.measure == cfg.measure
    )


def _draw(entry: DataEntry, cfg: Config) -> None:
    """Dibuja el ano que toca con datos ya calculados, sin leer la coleccion."""
    data = entry.data
    try:
        key_days = tuple(kd.day for kd in cfg.key_dates)
        min_year, max_year = year_bounds(data, key_days)
        state.year_offset = max(
            data.today.year - max_year,
            min(state.year_offset, data.today.year - min_year),
        )
        deck_only = entry.current_deck_only
        # La meta cumplida se celebra una vez: la primera vez que se dibuja
        # despues de cruzarla (al volver a la lista de mazos tras repasar).
        met = not deck_only and cfg.show_streak and view.goal_met(data, cfg)
        celebrate = met and state.goal_celebrated != data.today
        goal = cfg.goal if cfg.goal_mode == "number" and cfg.show_streak and not deck_only else 0
        inner = view.build_widget_html(data, cfg, state.year_offset, deck_only, celebrate)
        payload = view.payload_json(inner, measure=cfg.measure, goal=goal)
        # Lo recordado no lleva la celebracion: al volver a la pantalla no se
        # repite.
        remembered = (
            view.payload_json(inner.replace(" gritmap-celebrate", ""), measure=cfg.measure, goal=goal)
            if celebrate
            else payload
        )
        if met:
            state.goal_celebrated = data.today
    except Exception as exc:
        log_exception("controller.draw", exc)
        payload = remembered = view.error_payload()
    view.send(payload)
    state.remember_page((entry.current_deck_only, entry.deck_id), remembered)


def _request_data(current_deck_only: bool, cfg: Config) -> None:
    """Pide los datos en segundo plano y dibuja el mapa cuando lleguen."""
    if mw.col is None:
        return
    token, generation = state.new_render_token()
    screen = mw.state
    excluded = cfg.excluded_decks
    measure = cfg.measure

    def op(col: Collection) -> tuple[HeatmapData, int]:
        deck_id = int(col.decks.get_current_id()) if current_deck_only else 0
        scope = build_scope(col, excluded, current_deck_only)
        data = fetch_data(col, scope, measure)
        if current_deck_only:
            data = replace(data, fsrs_target=_fsrs_target(col, deck_id))
        else:
            data = replace(data, due_remaining=_due_remaining(col.sched.deck_due_tree(), scope))
        return data, deck_id

    @guarded()
    def on_success(result: tuple[HeatmapData, int]) -> None:
        state.finish(token)
        # Descarta el resultado si entretanto se pidio otro dibujado, si se
        # cambio de perfil o si la persona ya no esta en la misma pantalla.
        if not state.is_current(token, generation) or mw.col is None or mw.state != screen:
            return
        data, deck_id = result
        entry = DataEntry(generation, current_deck_only, deck_id, excluded, measure, data)
        # Las opciones se leen de nuevo: pudieron cambiar durante el calculo.
        cfg_now = load_config()
        if not _usable(entry, current_deck_only, cfg_now):
            # Cambiaron la medida o los mazos excluidos: estos datos ya no
            # valen y se calculan otra vez, con el mapa anterior a la vista.
            _request_data(current_deck_only, cfg_now)
            return
        state.data = entry
        _draw(entry, cfg_now)

    @guarded()
    def on_failure(exc: Exception) -> None:
        state.finish(token)
        log_exception("controller.fetch_data", exc)
        if state.is_current(token, generation) and mw.state == screen:
            view.send(view.error_payload())

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()


def _due_remaining(root: DeckTreeNode, scope: DeckScope) -> int:
    """Tarjetas que aun vencen hoy fuera de los mazos excluidos (meta
    «Terminar lo de hoy»), con los limites diarios que aplica Anki.

    Un mazo sin excluidos dentro cuenta con su cifra, que ya suma la de sus
    submazos; uno que contiene excluidos se cuenta por sus submazos.
    """
    excluded = set(scope.exclude_ids)

    def contains_excluded(node: DeckTreeNode) -> bool:
        return int(node.deck_id) in excluded or any(contains_excluded(c) for c in node.children)

    def remaining(node: DeckTreeNode) -> int:
        if int(node.deck_id) in excluded:
            return 0
        if not contains_excluded(node):
            return int(node.review_count + node.learn_count + node.new_count)
        return sum(remaining(child) for child in node.children)

    return sum(remaining(child) for child in root.children)


def _fsrs_target(col: Collection, deck_id: int) -> float | None:
    """Retencion deseada del mazo si FSRS esta activado; si no, None."""
    if not deck_id or not col.get_config("fsrs", False):
        return None
    target = col.decks.config_dict_for_deck_id(DeckId(deck_id)).get("desiredRetention")
    return float(target) if isinstance(target, (int, float)) and 0 < target < 1 else None


def _redraw_in_place() -> None:
    """Redibuja el mapa en el hueco que ya ocupa.

    El mapa anterior sigue a la vista y se sustituye de una vez. Si los datos
    guardados sirven, ni siquiera se lee la coleccion; si hay un calculo en
    marcha, sera el quien dibuje al terminar.
    """
    if mw.col is None:
        return
    current_deck_only = _current_deck_only()
    if current_deck_only is None:
        return
    cfg = load_config()
    if state.data is not None and _usable(state.data, current_deck_only, cfg):
        _draw(state.data, cfg)
    elif state.pending_token is None:
        _request_data(current_deck_only, cfg)


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


def _page_html(current_deck_only: bool, cfg: Config) -> str:
    """Contenedor del mapa para una pantalla que Anki esta construyendo.

    Lleva dentro el ultimo mapa de esa pantalla, si lo hay, y pide los datos
    al dia: el cambio, si lo hay, es de mapa a mapa y sin hueco intermedio.
    """
    deck_id = int(mw.col.decks.get_current_id()) if current_deck_only and mw.col else 0
    remembered = state.pages.get((current_deck_only, deck_id))
    # Una pantalla nueva puede traer datos nuevos (tras repasar, sincronizar
    # o deshacer): los guardados ya no valen.
    state.data = None
    _request_data(current_deck_only, cfg)
    return view.container_html(cfg, remembered)


@guarded()
def _on_deck_browser_render(_deck_browser: DeckBrowser, content: DeckBrowserContent) -> None:
    if mw.col is None:
        return
    content.stats += _page_html(False, load_config())


@guarded()
def _on_overview_render(_overview: Overview, content: OverviewContent) -> None:
    if mw.col is None:
        return
    content.table += _page_html(True, load_config())


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

    @guarded()
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

    @guarded()
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
    if current_deck_only != _current_deck_only():
        # Mensaje de una pagina que ya no es la que se ve.
        return (True, None)

    if action in ("prev", "next", "today"):
        if action == "prev":
            state.year_offset += 1
        elif action == "next":
            state.year_offset -= 1
        else:
            state.year_offset = 0
        _redraw_in_place()
        return (True, None)

    if action.startswith("window:"):
        _set_window(action[len("window:"):])
        return (True, None)

    if action in ("opts", "opts:exclude", "opts:keydates"):
        # Se aplaza para que el mensaje de la pagina termine antes de abrir
        # una ventana modal. Desde el aviso de mazo excluido se abre ademas
        # la lista de mazos excluidos, y desde «Anadir», la de fechas clave.
        start = action.partition(":")[2]
        mw.progress.single_shot(0, lambda: open_options(start=start))
        return (True, None)

    if action == "goal:set":
        mw.progress.single_shot(0, _set_goal)
        return (True, None)

    if action == "stats:toggle":
        # La pagina ya la plego o desplego al instante; aqui solo se guarda.
        cfg = load_config()
        config.save_appearance(replace(cfg, stats_open=not cfg.stats_open))
        state.pages.clear()
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
def _set_goal() -> None:
    """«Fijar meta»: un selector minimo con un numero ya propuesto, el 80 % de
    su promedio diario de los ultimos 30 dias, redondeado a 5 (criterio del
    informe para que sea alcanzable casi siempre)."""
    cfg = load_config()
    average = None
    if state.data is not None:
        average = window_average(state.data.data, cfg.measure, 30)
    proposal = max(5, int(round(0.8 * average / 5)) * 5) if average else DEFAULT_CONFIG.goal
    chosen = open_goal_dialog(proposal, cfg.measure)
    if chosen is None:
        return
    config.save_appearance(replace(cfg, goal_mode="number", goal=chosen))
    _apply_config_change()


def _set_window(raw: str) -> None:
    """Boton rapido de periodo: guarda la eleccion y redibuja sin recalcular.

    El texto llega de la pagina, asi que se comprueba antes de usarlo.
    """
    try:
        days = int(raw)
    except ValueError:
        return
    cfg = load_config()
    if days not in WINDOWS or days == cfg.avg_window:
        return
    config.save_appearance(replace(cfg, avg_window=days))
    state.pages.clear()
    _redraw_in_place()


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

    Si en ese momento no se ve el mapa (otra pantalla, o la de «Has terminado
    este mazo», que es de Anki) no hay nada que hacer: al volver, la pagina se
    construye ya con las opciones nuevas.
    """
    config.invalidate_cache()
    state.year_offset = 0
    state.pages.clear()
    if mw.col is None or _current_deck_only() is None:
        return
    mw.web.evalWithCallback(
        f"!!document.getElementById({json.dumps(view.ROOT_ID)})", _on_map_presence
    )


@guarded()
def _on_map_presence(has_map: object) -> None:
    if has_map is not True:
        return
    view.update_palette(load_config())
    _redraw_in_place()


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
    # Con su propia ventana de opciones, Anki nunca abre su editor de JSON
    # para este complemento.
    mw.addonManager.setConfigAction(__name__, open_options)
