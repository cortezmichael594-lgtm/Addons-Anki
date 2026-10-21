"""Punto de entrada del complemento: solo registra hooks y acciones."""

from __future__ import annotations

from aqt import gui_hooks, mw

from .logic import on_config_updated, on_main_window_did_init
from .ui import open_config_dialog

# Los atajos se cuelgan de la ventana principal, así que hay que esperar a que
# esté montada del todo.
gui_hooks.main_window_did_init.append(on_main_window_did_init)

# Configuración con casillas y campos normales, en vez del editor JSON de Anki.
mw.addonManager.setConfigAction(__name__, open_config_dialog)
mw.addonManager.setConfigUpdatedAction(__name__, on_config_updated)
