"""Panel de opciones del complemento.

Los botones Aceptar, Cancelar y Restaurar los valores predeterminados no
llevan texto propio: son los botones estandar, con el texto que ya trae
traducido el propio Anki. Los widgets son los normales de Qt, de modo que el
modo dia y el modo noche los adapta la hoja de estilos de Anki.

Regla: aqui no se guarda un atajo que Anki ya use, ni uno sin Ctrl ni Alt. Si
dos atajos se pelean por la misma tecla el resultado es impredecible, asi que
se avisa a la persona y no se cierra el panel hasta que elija otro.
"""

from __future__ import annotations

from aqt import mw
from aqt.qt import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QKeySequence,
    QKeySequenceEdit,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.utils import disable_help_button, showWarning, tooltip
from aqt.utils import tr as anki_tr

from . import config, constants, shortcuts
from .errors import guarded
from .logic import AlwaysOnTopManager
from .strings import tr


class ConfigDialog(QDialog):
    def __init__(self, manager: AlwaysOnTopManager, parent: QWidget) -> None:
        super().__init__(parent)
        self._manager = manager
        self._saved_shortcut = config.load().shortcut

        self.setWindowTitle(constants.ADDON_DISPLAY_NAME)
        disable_help_button(self)
        self.setModal(True)

        self._prefix = QLabel(tr("shortcut_prefix"), self)
        self._edit = QKeySequenceEdit(QKeySequence(self._saved_shortcut), self)
        self._edit.setMaximumSequenceLength(1)
        self._edit.setClearButtonEnabled(True)
        # QKeySequenceEdit no expone texto de ayuda: se aplica a su campo interno.
        inner_field = self._edit.findChild(QLineEdit)
        if inner_field is not None:
            inner_field.setPlaceholderText(tr("placeholder"))
        self._prefix.setBuddy(self._edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults,
            self,
        )
        restore_button = buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore_button is not None:
            restore_button.setAutoDefault(False)
            qconnect(restore_button.clicked, self._on_restore_defaults)
        qconnect(buttons.accepted, self._on_accept)
        qconnect(buttons.rejected, self.reject)

        layout = QVBoxLayout(self)
        shortcut_line = QHBoxLayout()
        shortcut_line.addWidget(self._prefix)
        shortcut_line.addWidget(self._edit, stretch=1)
        layout.addLayout(shortcut_line)
        layout.addSpacing(6)
        layout.addWidget(buttons)

        self.setMinimumWidth(420)
        self._edit.setFocus()

    @guarded
    def _on_restore_defaults(self) -> None:
        self._edit.setKeySequence(QKeySequence(constants.DEFAULT_SHORTCUT))
        tooltip(anki_tr.addons_restored_defaults(), parent=self)

    @guarded
    def _on_accept(self) -> None:
        sequence = self._edit.keySequence()
        chosen = sequence.toString(QKeySequence.SequenceFormat.PortableText)

        if not chosen:
            chosen = constants.DEFAULT_SHORTCUT
        elif not shortcuts.is_usable(chosen):
            # El nombre se muestra tal como lo ve la persona en su teclado.
            showWarning(
                tr("conflict", shortcut=sequence.toString()),
                parent=self,
                title=constants.ADDON_DISPLAY_NAME,
            )
            self._edit.setFocus()
            return

        if chosen != self._saved_shortcut:
            config.save(config.Settings(shortcut=chosen))
            self._manager.apply_shortcut(chosen, notify=False)
            self._saved_shortcut = chosen
        self.accept()


@guarded
def open_config_dialog(manager: AlwaysOnTopManager) -> None:
    # El panel se cuelga de la ventana que este activa -normalmente la lista de
    # complementos- para que aparezca centrado sobre ella y nunca por detras.
    parent = mw.app.activeWindow() or mw
    ConfigDialog(manager, parent).exec()
