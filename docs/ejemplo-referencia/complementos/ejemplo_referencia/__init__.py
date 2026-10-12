"""Complemento de ejemplo: modelo de estructura para los complementos de este proyecto.

Este módulo solo registra: entradas de menú, la acción de configuración y los hooks.
La lógica vive en logic.py, lo que pasa al pulsar en actions.py, los diálogos en
dialogs.py y los textos en strings.py.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-10-12): una tarjeta podía leer archivos .css y .js de otros complementos.

from __future__ import annotations

import html
from typing import Any

from aqt import gui_hooks, mw
from aqt.qt import QAction, qconnect
from aqt.reviewer import Reviewer
from aqt.webview import WebContent

from . import actions, config, strings
from .errors import guarded, guarded_filter

_BRIDGE_COMMAND = "ejemplo_referencia:options"

# --- FIX-002 (2026-10-12) ---
# Síntoma: con «web/..%2F..%2Fotro%2Fx.js», una tarjeta podía leer archivos de otros complementos.
# Causa: Anki compara el patrón antes de resolver los «..», y «.*» los aceptaba.
# Regla: el patrón de setWebExports es cerrado: sin «/» ni «.» libres entre la carpeta y la extensión.
WEB_EXPORTS_PATTERN = r"web/[\w-]+\.(css|js)"


@guarded
def _add_assets_to_reviewer(web_content: WebContent, context: object | None) -> None:
    """Añade CSS, JS e insignia a la pantalla de repaso ANTES de que se pinte por primera vez.

    Si se inyectara después, con JavaScript, la insignia aparecería de golpe y
    desplazaría el contenido: eso es lo que se ve como un parpadeo.
    """
    if mw is None or not isinstance(context, Reviewer) or not config.load()["show_badge"]:
        return
    package = mw.addonManager.addon_from_module(__name__)
    web_content.css.append(f"/_addons/{package}/web/ejemplo.css")
    web_content.js.append(f"/_addons/{package}/web/ejemplo.js")
    web_content.body += (
        '<button type="button" id="ejemplo-referencia-badge" class="ejemplo-referencia-badge" '
        f'title="{html.escape(strings.BADGE_TIP)}">{html.escape(strings.BADGE_LABEL)}</button>'
    )


@guarded_filter
def _on_js_message(handled: tuple[bool, Any], message: str, context: Any) -> tuple[bool, Any]:
    if message != _BRIDGE_COMMAND:
        return handled
    actions.open_options()
    return (True, None)


def _register() -> None:
    # Fuera de Anki (pruebas, comprobaciones) no hay ventana principal: no se registra nada.
    if mw is None:
        return

    for label, callback in (
        (strings.MENU_OPTIONS, actions.open_options),
        (strings.MENU_TAG_NOTES, actions.tag_notes),
    ):
        action = QAction(label, mw)
        qconnect(action.triggered, callback)
        mw.form.menuTools.addAction(action)

    mw.addonManager.setConfigAction(__name__, actions.open_options)
    mw.addonManager.setWebExports(__name__, WEB_EXPORTS_PATTERN)
    gui_hooks.webview_will_set_content.append(_add_assets_to_reviewer)
    gui_hooks.webview_did_receive_js_message.append(_on_js_message)


_register()
