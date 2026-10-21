"""Ventana de opciones del complemento.

Se registra con setConfigAction, de modo que el boton "Configuracion" de Anki
abre esto y no el editor de JSON.

Los botones son los estandar de Qt (Aceptar, Cancelar, Restaurar valores
predeterminados) y el titulo es el que Anki pone a la configuracion de cualquier
complemento: asi salen ya traducidos a todos los idiomas y con el mismo aspecto
que el resto del programa.
"""

from __future__ import annotations

from aqt import mw
from aqt.qt import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.utils import disable_help_button, showWarning, tooltip

from . import constants, logic, strings
from .config import DEFAULT_CONFIG, HiderConfig, load_config, save_config
from .errors import guarded
from .strings import tr


def _checkbox(label_key: str, tip_key: str) -> QCheckBox:
    box = QCheckBox(tr(label_key))
    box.setToolTip(tr(tip_key))
    return box


def _parent_window() -> QWidget:
    """La ventana desde la que se abrio, para que el dialogo salga encima."""
    window = QApplication.activeWindow()
    return window if isinstance(window, QWidget) else mw


class HiderOptionsDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(strings.options_title())
        self.setMinimumWidth(420)
        disable_help_button(self)

        self._menu_bar = _checkbox("opt_menu_bar", "opt_menu_bar_tip")
        self._toolbar = _checkbox("opt_toolbar", "opt_toolbar_tip")
        self._bottom_bar = _checkbox("opt_bottom_bar", "opt_bottom_bar_tip")
        self._scrollbar = _checkbox("opt_scrollbar", "opt_scrollbar_tip")
        self._hard_easy = _checkbox("opt_hard_easy", "opt_hard_easy_tip")
        self._cursor = _checkbox("opt_cursor", "opt_cursor_tip")
        self._auto_start = _checkbox("opt_auto_start", "opt_auto_start_tip")

        self._idle_seconds = QSpinBox()
        self._idle_seconds.setRange(
            constants.MIN_CURSOR_IDLE_SECONDS, constants.MAX_CURSOR_IDLE_SECONDS
        )
        self._idle_seconds.setSuffix(tr("opt_cursor_suffix"))
        self._idle_seconds.setToolTip(tr("opt_cursor_tip"))
        qconnect(self._cursor.toggled, self._idle_seconds.setEnabled)

        cursor_row = QHBoxLayout()
        cursor_row.addWidget(self._cursor)
        cursor_row.addWidget(self._idle_seconds)
        cursor_row.addStretch()

        review_layout = QVBoxLayout()
        for widget in (self._menu_bar, self._toolbar, self._bottom_bar, self._scrollbar):
            review_layout.addWidget(widget)
        review_layout.addWidget(self._hard_easy)
        review_layout.addLayout(cursor_row)
        review_group = QGroupBox(tr("group_review"))
        review_group.setLayout(review_layout)

        behaviour_layout = QVBoxLayout()
        behaviour_layout.addWidget(self._auto_start)
        behaviour_group = QGroupBox(tr("group_behaviour"))
        behaviour_group.setLayout(behaviour_layout)

        # Sin setText: el texto de estos tres botones lo pone Qt en el idioma de
        # Anki, igual que en los dialogos del propio programa.
        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        qconnect(self._buttons.accepted, self.accept)
        qconnect(self._buttons.rejected, self.reject)
        qconnect(self._buttons.clicked, self._on_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(review_group)
        layout.addWidget(behaviour_group)
        layout.addWidget(self._buttons)
        self.setLayout(layout)

        self._apply(load_config())
        self._menu_bar.setFocus()

    def _on_button_clicked(self, button: QAbstractButton | None) -> None:
        if button is None:
            return
        if self._buttons.buttonRole(button) == QDialogButtonBox.ButtonRole.ResetRole:
            self._apply(DEFAULT_CONFIG)
            tooltip(strings.restored_defaults(), parent=self)

    def _apply(self, config: HiderConfig) -> None:
        self._menu_bar.setChecked(config.hide_menu_bar)
        self._toolbar.setChecked(config.hide_toolbar)
        self._bottom_bar.setChecked(config.hide_bottom_bar)
        self._scrollbar.setChecked(config.hide_scrollbar)
        self._hard_easy.setChecked(config.hide_hard_easy_buttons)
        self._cursor.setChecked(config.hide_cursor)
        self._idle_seconds.setValue(config.cursor_idle_seconds)
        self._idle_seconds.setEnabled(config.hide_cursor)
        self._auto_start.setChecked(config.auto_start_study)

    def selected_config(self) -> HiderConfig:
        return HiderConfig(
            hide_menu_bar=self._menu_bar.isChecked(),
            hide_toolbar=self._toolbar.isChecked(),
            hide_bottom_bar=self._bottom_bar.isChecked(),
            hide_cursor=self._cursor.isChecked(),
            cursor_idle_seconds=self._idle_seconds.value(),
            hide_scrollbar=self._scrollbar.isChecked(),
            hide_hard_easy_buttons=self._hard_easy.isChecked(),
            auto_start_study=self._auto_start.isChecked(),
        )


@guarded
def open_options() -> None:
    """Accion del boton "Configuracion".

    Nunca debe devolver False ni dejar escapar un error: lo primero haria que
    Anki abriese ademas su editor de JSON, y lo segundo le plantaria a la persona
    un volcado tecnico en pantalla.
    """
    dialog = HiderOptionsDialog(_parent_window())
    accepted = dialog.exec() == QDialog.DialogCode.Accepted
    config = dialog.selected_config() if accepted else None
    dialog.deleteLater()
    if config is None:
        return
    try:
        save_config(config)
    except Exception:
        showWarning(tr("save_failed"), parent=mw, title=constants.ADDON_NAME)
        return
    # writeConfig no dispara setConfigUpdatedAction, asi que se avisa al manager
    # para que el cambio se note al momento, incluso en pleno repaso.
    logic.reload_active_manager()
    tooltip(tr("saved"), period=2000)
