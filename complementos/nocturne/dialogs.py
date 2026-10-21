"""Ventana de configuración: elegir una de las tres paletas.

Se hace como las de Anki (Preferencias > Interfaz de usuario): un recuadro con su
título, una lista desplegable con su etiqueta y los botones estándar, sin colores
ni hojas de estilo propias, para que herede el tema, el teclado y el idioma.
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-21): la ventana de paletas quedaba detrás de la de complementos.

from __future__ import annotations

from anki.lang import without_unicode_isolation
from aqt import mw
from aqt.qt import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QKeySequence,
    QLabel,
    QLayout,
    Qt,
    QVBoxLayout,
    QWidget,
)
from aqt.utils import disable_help_button, tooltip, tr

from . import actions, strings, themes
from .errors import guard


class PaletteDialog(QDialog):
    """Elige la paleta; al abrirla, muestra la activa. Se aplica con «Aceptar»."""

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # El mismo título que Anki pone a la configuración de cualquier complemento.
        self.setWindowTitle(
            without_unicode_isolation(tr.addons_config_window_title(name=strings.ADDON_NAME))
        )
        disable_help_button(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self._combo = QComboBox()
        for theme_id in themes.THEMES:
            self._combo.addItem(strings.THEME_NAMES[theme_id], theme_id)
        self._description = QLabel()
        # Ancho de la descripción más larga: al cambiar de paleta, la ventana no
        # cambia de tamaño y ninguna línea se corta.
        metrics = self._description.fontMetrics()
        self._description.setMinimumWidth(
            max(metrics.horizontalAdvance(text) for text in strings.THEME_DESCRIPTIONS.values())
        )
        self._combo.currentIndexChanged.connect(self._show_description)

        label = QLabel(strings.PALETTE_LABEL)
        label.setBuddy(self._combo)
        form = QFormLayout()
        form.addRow(label, self._combo)
        form.addRow("", self._description)
        group = QGroupBox(strings.GROUP_TITLE)
        group.setLayout(form)

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

        layout = QVBoxLayout(self)
        layout.addWidget(group)
        layout.addWidget(box)
        # Tamaño justo para su contenido, como los diálogos pequeños de Anki.
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self._select(themes.current_id())
        self._show_description()

    def _select(self, theme_id: str) -> None:
        index = self._combo.findData(theme_id)
        if index >= 0:
            self._combo.setCurrentIndex(index)

    def _show_description(self) -> None:
        self._description.setText(strings.THEME_DESCRIPTIONS[self.selected_id()])

    def selected_id(self) -> str:
        theme_id = self._combo.currentData()
        return theme_id if isinstance(theme_id, str) else themes.current_id()

    def restore_defaults(self) -> None:
        """Elige Nocturne en la lista; como en Anki, no se aplica hasta «Aceptar»."""
        self._select(themes.DEFAULT_THEME)

    @guard
    def accept(self) -> None:
        super().accept()
        chosen = self.selected_id()
        if chosen != themes.current_id():
            applied = actions.choose_palette(chosen)
            tooltip(strings.APPLIED.format(name=strings.THEME_NAMES[applied]))


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
