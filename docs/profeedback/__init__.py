"""ProFeedback: sonidos, confeti, botones de respuesta e insignias en el repaso de Anki.

Este módulo solo registra: la ventana de configuración y los hooks. La decisión de qué
celebrar y de qué insignia lleva una tarjeta está en logic.py; el repaso en feedback.py; la
celebración en celebration.py; el sonido en audio.py; la ventana de ajustes en dialogs.py y
los textos en strings.py.

El estilo y el código de web/ van incrustados en las páginas (feedback.py), no servidos como
archivos: por eso no se registra ningún setWebExports y las tarjetas no pueden pedir nada
del complemento.
"""

from __future__ import annotations

from aqt import gui_hooks, mw

from . import actions, celebration, feedback


def _register() -> None:
    # Fuera de Anki (pruebas, comprobaciones) no hay ventana principal: no se registra nada.
    if mw is None:
        return
    mw.addonManager.setConfigAction(__name__, actions.open_settings)
    feedback.register()
    celebration.register()
    gui_hooks.profile_did_open.append(actions.on_profile_open)
    gui_hooks.profile_will_close.append(actions.on_profile_close)


_register()
