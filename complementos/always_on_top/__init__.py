"""Always on Top: mantiene la ventana de Anadir por encima de las demas.

Este archivo solo registra: engancha el complemento a Anki y no contiene
logica propia.
"""

from __future__ import annotations

from aqt import gui_hooks, mw


def _register() -> None:
    from .dialogs import open_config_dialog
    from .logic import AlwaysOnTopManager

    manager = AlwaysOnTopManager()

    def _open_config() -> None:
        open_config_dialog(manager)

    gui_hooks.add_cards_did_init.append(manager.on_add_cards_init)
    mw.addonManager.setConfigAction(__name__, _open_config)
    mw.addonManager.setConfigUpdatedAction(__name__, manager.on_config_updated)
    manager.start()


# Fuera de Anki (pruebas y empaquetar.py) no hay ventana principal: no se
# registra nada.
if mw is not None:
    _register()
