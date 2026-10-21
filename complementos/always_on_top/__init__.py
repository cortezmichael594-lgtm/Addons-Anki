"""Always on Top: mantiene la ventana de Anadir por encima de las demas.

Este archivo solo registra: engancha el complemento a Anki y no contiene
logica propia.
"""

from __future__ import annotations

from aqt import gui_hooks, mw

from .dialogs import open_config_dialog
from .logic import AlwaysOnTopManager

_manager = AlwaysOnTopManager()


def _open_config() -> None:
    open_config_dialog(_manager)


gui_hooks.add_cards_did_init.append(_manager.on_add_cards_init)
mw.addonManager.setConfigAction(__name__, _open_config)
mw.addonManager.setConfigUpdatedAction(__name__, _manager.on_config_updated)
_manager.start()
