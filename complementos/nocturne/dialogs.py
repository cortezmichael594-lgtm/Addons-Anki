"""Ventana de configuración: elegir una de las cinco paletas."""

from __future__ import annotations

from aqt import mw
from aqt.qt import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)
from aqt.utils import restoreGeom, saveGeom, tooltip

from . import actions, strings, themes
from .errors import guard

_GEOMETRY_KEY = "nocturne_palettes"


class PaletteDialog(QDialog):
    """Se crea una vez y se muestra muchas: al abrirla, marca la paleta activa."""

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.setWindowTitle(strings.DIALOG_TITLE)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        intro = QLabel(strings.DIALOG_INTRO)
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._group = QButtonGroup(self)
        self._buttons: dict[str, QRadioButton] = {}
        for theme_id in themes.THEMES:
            button = QRadioButton(strings.THEME_NAMES[theme_id])
            description = QLabel(strings.THEME_DESCRIPTIONS[theme_id])
            description.setWordWrap(True)
            # La descripción, alineada con el texto del botón y no con el círculo.
            description.setContentsMargins(24, 0, 0, 0)
            description.setBuddy(button)
            self._group.addButton(button)
            self._buttons[theme_id] = button
            # Cada descripción, más cerca de su paleta que de la siguiente
            # (Practical UI, P12: espaciar según la relación).
            option = QVBoxLayout()
            option.setSpacing(2)
            option.addWidget(button)
            option.addWidget(description)
            layout.addLayout(option)

        layout.addStretch()  # el espacio sobrante, encima de los botones
        box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        # Ancho suficiente para las descripciones y alto según su texto: así ninguna
        # línea queda cortada aunque se abra por primera vez o se haya estrechado.
        self.setMinimumWidth(460)
        self.setMinimumHeight(self.sizeHint().height())
        restoreGeom(self, _GEOMETRY_KEY)
        self.finished.connect(lambda _result: saveGeom(self, _GEOMETRY_KEY))

    def selected_id(self) -> str:
        for theme_id, button in self._buttons.items():
            if button.isChecked():
                return theme_id
        return themes.current_id()

    def show_current(self) -> None:
        self._buttons[themes.current_id()].setChecked(True)
        self.show()
        self.raise_()
        self.activateWindow()

    @guard
    def accept(self) -> None:
        super().accept()
        chosen = self.selected_id()
        if chosen != themes.current_id():
            applied = actions.choose_palette(chosen)
            tooltip(strings.APPLIED.format(name=strings.THEME_NAMES[applied]))


_dialog: PaletteDialog | None = None


@guard
def open_dialog() -> None:
    """Abre la ventana (desde Herramientas o desde «Configuración» del complemento)."""
    global _dialog
    if mw is None:
        return
    if _dialog is None:
        _dialog = PaletteDialog(mw)
    _dialog.show_current()
