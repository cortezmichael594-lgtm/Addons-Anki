"""Diálogo de opciones del complemento.

Se abre desde Herramientas → Complementos → Configuración, en lugar del editor
de texto JSON de Anki, para que las opciones se cambien con casillas y campos
normales. No fija ningún color propio: así hereda el tema de Anki y se ve
correctamente en modo día y en modo noche.

Los botones (Aceptar, Cancelar y Restaurar valores predeterminados) los pone
Anki, que ya los trae traducidos a todos sus idiomas; el complemento no
inventa esos textos.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-28) — Un atajo podía chocar con otro que Anki ya usaba.
# FIX-003 (2026-07-28) — Se retiró el atajo para cerrar Anki, que duplicaba Ctrl+Q.

from __future__ import annotations

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QKeySequence,
    QKeySequenceEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.utils import current_window, disable_help_button, showWarning

from . import constants, shortcuts
from .errors import report_errors
from .logic import registered_shortcuts, reload_shortcuts
from .settings import AddonSettings, load_settings, save_settings
from .strings import tr


class _ShortcutRow:
    def __init__(self, checkbox_text: str, enabled: bool, sequence: str) -> None:
        self._saved_sequence = sequence
        self.checkbox = QCheckBox(checkbox_text)
        self.checkbox.setChecked(enabled)
        self.edit = QKeySequenceEdit(QKeySequence(sequence))
        self.edit.setMaximumSequenceLength(1)
        self.edit.setClearButtonEnabled(True)
        self.edit.setEnabled(enabled)
        qconnect(self.checkbox.toggled, self.edit.setEnabled)

    def apply(self, enabled: bool, sequence: str) -> None:
        # El atajo guardado se actualiza también, para que vaciar el campo
        # después de restaurar los valores recomendados devuelva el recomendado
        # y no el que hubiera antes.
        self._saved_sequence = sequence
        self.checkbox.setChecked(enabled)
        self.edit.setKeySequence(QKeySequence(sequence))
        self.edit.setEnabled(enabled)

    def is_enabled(self) -> bool:
        return self.checkbox.isChecked()

    def sequence_text(self) -> str:
        # Si la persona deja el campo vacío, se conserva el atajo ya guardado.
        return self.edit.keySequence().toString() or self._saved_sequence

    def sequence(self) -> QKeySequence:
        return QKeySequence(self.sequence_text())

    def label(self) -> str:
        """Cómo se nombra este atajo dentro de un aviso."""
        return shortcuts.display_text(self.sequence()) or self.sequence_text() or "—"


class ConfigDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent or mw)
        # El título es el nombre del complemento, igual que aparece en la lista
        # de complementos de Anki, para que se sepa de quién son las opciones.
        self.setWindowTitle(constants.ADDON_NAME)
        disable_help_button(self)
        settings = load_settings()

        self._restart_row = _ShortcutRow(
            tr("restart_checkbox"),
            settings.restart_enabled,
            settings.restart_shortcut,
        )

        # Botones estándar de Qt: sus textos los traduce Anki junto con el
        # resto de su interfaz, así que salen en el idioma de cada persona.
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        restore_button = buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore_button is not None:
            restore_button.setAutoDefault(False)
            qconnect(restore_button.clicked, self._on_restore_defaults)
        qconnect(buttons.accepted, self._on_accept)
        qconnect(buttons.rejected, self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self._restart_row.checkbox)
        shortcut_line = QHBoxLayout()
        shortcut_line.addSpacing(24)
        shortcut_line.addWidget(QLabel(tr("shortcut_label")))
        shortcut_line.addWidget(self._restart_row.edit, stretch=1)
        layout.addLayout(shortcut_line)
        layout.addSpacing(6)
        layout.addWidget(buttons)

        self.setMinimumWidth(420)
        self._restart_row.checkbox.setFocus()

    def _warn(self, message: str) -> None:
        showWarning(message, parent=self, title=constants.ADDON_NAME)

    def _on_restore_defaults(self) -> None:
        self._restart_row.apply(
            constants.DEFAULT_RESTART_ENABLED, constants.DEFAULT_SHORTCUT_RESTART
        )

    def _on_accept(self) -> None:
        # --- FIX-001 (2026-07-28) --------------------------------------
        # Síntoma: se podía guardar un atajo que Anki ya estaba usando, y
        #          entonces no respondía ni el de Anki ni el del complemento.
        # Causa: la comprobación se hacía contra una lista escrita a mano, que
        #        se quedaba corta y anticuada.
        # Regla: preguntar siempre a la ventana principal qué combinaciones
        #        tiene cogidas en ese momento, incluidas las que el sistema
        #        reserva para cerrar ventana, y excluir del cotejo los atajos
        #        del propio complemento.
        # ---------------------------------------------------------------
        if self._restart_row.is_enabled() and not shortcuts.is_allowed(
            self._restart_row.sequence(), registered_shortcuts()
        ):
            self._warn(tr("shortcut_not_allowed", shortcut=self._restart_row.label()))
            return

        save_settings(
            AddonSettings(
                restart_enabled=self._restart_row.is_enabled(),
                restart_shortcut=self._restart_row.sequence_text(),
            )
        )
        reload_shortcuts()
        self.accept()


@report_errors
def open_config_dialog() -> None:
    # Se cuelga de la ventana que esté delante (normalmente la de complementos)
    # para que no quede escondida detrás de ella.
    parent = current_window() or mw
    dialog = ConfigDialog(parent)
    dialog.exec()
