"""Ventana de configuración: elegir una de las tres paletas.

Se hace como las de Anki (Preferencias > Interfaz de usuario): un recuadro con su
título, controles estándar y los botones estándar, sin colores ni hojas de estilo
propias, para que herede el tema, el teclado y el idioma.

Versión 3.5.0: las tres paletas a la vista, cada una con su botón de opción y su
descripción debajo, para compararlas sin abrir una lista (Practical UI, P19), y vista
previa: al elegir una, se aplica en el acto a todo Anki; «Aceptar» la conserva y
«Cancelar», Esc o la X vuelven a la que había (Norman, golfo de evaluación).
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-21): la ventana de paletas quedaba detrás de la de complementos.

from __future__ import annotations

from typing import Any

from anki.lang import without_unicode_isolation
from aqt import mw
from aqt.qt import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QKeySequence,
    QLabel,
    QLayout,
    QPalette,
    QPushButton,
    QRadioButton,
    QStyle,
    Qt,
    QTimer,
    QVBoxLayout,
    QWidget,
)
from aqt.utils import disable_help_button, openFolder, tr

from . import actions, config, contrast, errors, strings, themes
from .errors import guard

# La vista previa espera a que la elección lleve este tiempo quieta, para que recorrer
# las paletas con las flechas no repinte Anki a cada paso.
PREVIEW_DELAY_MS = 200


class _DescriptionLabel(QLabel):
    """Descripción de una paleta: pulsarla también elige la paleta (objetivo mayor)."""

    def __init__(self, text: str, button: QRadioButton) -> None:
        super().__init__(text)
        self._button = button
        # Texto secundario: el color que Anki da a los textos de ejemplo de los campos,
        # que sigue al tema y a la paleta sin pintar nada a mano.
        self.setForegroundRole(QPalette.ColorRole.PlaceholderText)

    def mousePressEvent(self, event: Any) -> None:
        self._button.setChecked(True)
        self._button.setFocus()


class PaletteDialog(QDialog):
    """Elige la paleta con vista previa. Al abrirla, está elegida la activa."""

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # El mismo título que Anki pone a la configuración de cualquier complemento.
        self.setWindowTitle(
            without_unicode_isolation(tr.addons_config_window_title(name=strings.ADDON_NAME))
        )
        disable_help_button(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self._original = themes.current_id()
        self._preview_enabled = not contrast.stepped_aside()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(PREVIEW_DELAY_MS)
        self._timer.timeout.connect(self._preview)

        group = QGroupBox(strings.GROUP_TITLE)
        options = QVBoxLayout(group)
        options.setSpacing(12)  # entre una paleta y la siguiente (Practical UI, P12)
        style = self.style()
        indent = 0
        if style is not None:
            indent = style.pixelMetric(QStyle.PixelMetric.PM_ExclusiveIndicatorWidth) + style.pixelMetric(
                QStyle.PixelMetric.PM_RadioButtonLabelSpacing
            )
        self._group = QButtonGroup(self)
        self._buttons: dict[str, QRadioButton] = {}
        for theme_id in themes.THEMES:
            name = strings.THEME_NAMES[theme_id]
            if theme_id == themes.DEFAULT_THEME:
                name += strings.DEFAULT_SUFFIX
            button = QRadioButton(name)
            self._group.addButton(button)
            self._buttons[theme_id] = button
            description = _DescriptionLabel(strings.THEME_DESCRIPTIONS[theme_id], button)
            # Alineada con el nombre, no con el círculo.
            description.setContentsMargins(indent, 0, 0, 0)
            option = QVBoxLayout()
            option.setSpacing(4)  # nombre y descripción, juntos
            option.addWidget(button)
            option.addWidget(description)
            options.addLayout(option)
        note = QLabel(strings.DAY_AND_NIGHT)
        note.setWordWrap(True)
        note.setForegroundRole(QPalette.ColorRole.PlaceholderText)
        options.addWidget(note)

        layout = QVBoxLayout(self)
        if not self._preview_enabled:
            notice = QLabel(strings.HIGH_CONTRAST)
            notice.setWordWrap(True)
            layout.addWidget(notice)
        layout.addWidget(group)
        if errors.failures() and errors.logs_folder():
            layout.addLayout(self._failures_row())

        box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        restore = box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore is not None:
            restore.clicked.connect(self.restore_defaults)
        ok = box.button(QDialogButtonBox.StandardButton.Ok)
        if ok is not None:
            ok.setShortcut(QKeySequence("Ctrl+Return"))  # como en la configuración de Anki
        layout.addWidget(box)
        # Tamaño justo para su contenido, como los diálogos pequeños de Anki.
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self._buttons[self._original].setChecked(True)
        self._buttons[self._original].setFocus()  # el teclado empieza en la paleta activa
        self._group.buttonToggled.connect(self._on_toggled)

    def _failures_row(self) -> QHBoxLayout:
        """Solo si hubo fallos en la sesión: una línea y un botón para ver el registro."""
        row = QHBoxLayout()
        text = QLabel(strings.FAILURES)
        text.setWordWrap(True)
        text.setForegroundRole(QPalette.ColorRole.PlaceholderText)
        button = QPushButton(strings.OPEN_LOG)
        button.setAutoDefault(False)
        button.clicked.connect(self._open_log)
        row.addWidget(text, 1)
        row.addWidget(button)
        return row

    @guard
    def _open_log(self) -> None:
        folder = errors.logs_folder()
        if folder:
            openFolder(folder)

    def selected_id(self) -> str:
        for theme_id, button in self._buttons.items():
            if button.isChecked():
                return theme_id
        return themes.current_id()

    def restore_defaults(self) -> None:
        """Elige Nocturne, y la vista previa la muestra."""
        self._buttons[themes.DEFAULT_THEME].setChecked(True)

    def _on_toggled(self, _button: QRadioButton, checked: bool) -> None:
        if checked and self._preview_enabled:
            self._timer.start()

    @guard
    def _preview(self) -> None:
        chosen = self.selected_id()
        if chosen != themes.current_id():
            actions.apply_palette(chosen)

    @guard
    def accept(self) -> None:
        self._timer.stop()
        chosen = self.selected_id()
        if self._preview_enabled and chosen != themes.current_id():
            actions.apply_palette(chosen)
        # La vista previa ya enseñó el cambio: no hace falta otro aviso.
        config.save(chosen)
        super().accept()

    @guard
    def reject(self) -> None:
        self._timer.stop()
        if self._preview_enabled and themes.current_id() != self._original:
            actions.apply_palette(self._original)
        super().reject()


# Referencia a la ventana abierta, para que el recolector de basura no la cierre.
_dialog: PaletteDialog | None = None


def _owner() -> QWidget | None:
    """La ventana desde la que se pide la configuración (la de complementos)."""
    if mw is None:
        return None
    return mw.app.activeWindow() or mw


@guard
def open_dialog() -> None:
    """Abre la ventana (botón «Configuración» de la ventana de complementos).

    # --- FIX-007 (2026-10-21) ---
    # Síntoma: al pulsar «Configuración», la ventana de paletas no aparecía delante: la de
    #          complementos no dejaba elegir nada y solo al cerrarla se veía la de paletas.
    # Causa: la ventana tenía de padre la ventana principal de Anki y se abría sin bloquear,
    #        así que Windows la dejaba detrás de la de complementos, que estaba activa.
    # Regla: toda ventana que se abre desde otra la toma como padre (la ventana activa, no
    #        la principal) y se abre con open(), que la deja delante y bloquea solo a su
    #        padre; se crea en cada apertura, como hace Anki con la suya, porque la ventana
    #        de complementos se destruye al cerrarse y se llevaría una ventana reutilizada.
    """
    global _dialog
    owner = _owner()
    if owner is None:
        return
    _dialog = PaletteDialog(owner)
    _dialog.open()
