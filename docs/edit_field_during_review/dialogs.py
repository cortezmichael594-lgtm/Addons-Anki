"""Diálogo de opciones del complemento.

Se abre desde Herramientas → Complementos → (seleccionar) → Configuración,
gracias a setConfigAction, de modo que el usuario nunca ve el editor JSON.

Los botones (Aceptar / Cancelar) son los botones estándar de Qt, que Anki ya
traduce a cada idioma. El único texto propio es la casilla, que vive en
strings.py. El título de la ventana es el nombre del complemento (los nombres
de complemento no se traducen).
"""

from __future__ import annotations

from aqt import mw
from aqt.qt import QCheckBox, QDialog, QDialogButtonBox, QVBoxLayout
from aqt.utils import showWarning

from . import config, constants
from .strings import tr as _


def open_options() -> None:
    """Callback de setConfigAction: no recibe argumentos ni necesita devolver nada."""
    try:
        _show_dialog()
    except Exception as exc:
        showWarning(str(exc), parent=mw, title=constants.ADDON_NAME)


def _show_dialog() -> None:
    dialog = QDialog(mw)
    dialog.setWindowTitle(constants.ADDON_NAME)

    layout = QVBoxLayout(dialog)

    checkbox = QCheckBox(_("opt_require_modifier"))
    checkbox.setChecked(config.require_modifier())
    layout.addWidget(checkbox)

    buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    if dialog.exec():
        config.set_require_modifier(checkbox.isChecked())
