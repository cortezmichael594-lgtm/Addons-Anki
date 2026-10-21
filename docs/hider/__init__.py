"""Punto de entrada: conecta el complemento a Anki y nada mas.

Toda la logica esta en logic.py; aqui solo se registran los avisos de Anki y la
accion del boton "Configuracion".
"""

from __future__ import annotations

from typing import Any

from aqt import gui_hooks, mw

from . import logic
from .dialogs import open_options
from .errors import guarded
from .logic import HiderManager

__version__ = "4.0.3"


@guarded
def _on_config_updated(_config: Any) -> None:
    # Solo salta si la configuracion se cambia por fuera del dialogo propio.
    logic.reload_active_manager()


def _register(manager: HiderManager) -> None:
    gui_hooks.state_will_change.append(manager.on_state_will_change)
    gui_hooks.overview_will_render_content.append(manager.on_overview_will_render_content)
    gui_hooks.overview_did_refresh.append(manager.on_overview_did_refresh)
    gui_hooks.webview_will_set_content.append(manager.on_webview_will_set_content)
    gui_hooks.reviewer_did_show_question.append(manager.on_reviewer_did_show_question)
    gui_hooks.reviewer_will_init_answer_buttons.append(
        manager.on_reviewer_will_init_answer_buttons
    )
    gui_hooks.reviewer_will_answer_card.append(manager.on_reviewer_will_answer_card)
    gui_hooks.profile_did_open.append(manager.on_profile_did_open)
    gui_hooks.profile_will_close.append(manager.on_profile_will_close)

    logic.set_active_manager(manager)
    # setConfigAction hace que Anki abra este dialogo en lugar del editor de JSON.
    mw.addonManager.setConfigAction(__name__, open_options)
    mw.addonManager.setConfigUpdatedAction(__name__, _on_config_updated)


_register(HiderManager())
