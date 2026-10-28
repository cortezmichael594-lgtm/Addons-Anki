"""Ventana de configuración: elegir una de las cinco paletas.

Se hace como las de Anki (Preferencias > Interfaz de usuario): controles estándar
y los botones estándar, sin hojas de estilo propias, para que herede el tema, el
teclado y el idioma.

Versión 3.5.0: vista previa. Al elegir una paleta se aplica en el acto a todo Anki;
«Aceptar» la conserva y «Cancelar», Esc o la X vuelven a la que había (Norman, golfo
de evaluación).

Versión 3.6.0 (petición del cliente, 2026-10-28): el mismo diseño que las opciones
de GritMap, para que los dos complementos se vean de la misma familia: una fila
«Paleta» con una lista desplegable en la que cada paleta lleva su muestra de color
(el fondo de la paleta con un punto de su color de acción, en el modo activo), y
debajo la descripción de la elegida.
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-21): la ventana de paletas quedaba detrás de la de complementos.

from __future__ import annotations

from anki.lang import without_unicode_isolation
from aqt import gui_hooks, mw
from aqt.qt import (
    QColor,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QIcon,
    QKeySequence,
    QLabel,
    QLayout,
    QPainter,
    QPalette,
    QPixmap,
    QPushButton,
    QSize,
    Qt,
    QTimer,
    QVBoxLayout,
    QWidget,
)
from aqt.theme import theme_manager
from aqt.utils import disable_help_button, openFolder, tr

from . import actions, config, contrast, errors, strings, themes
from .errors import guard

# La vista previa espera a que la elección lleve este tiempo quieta, para que recorrer
# las paletas con las flechas no repinte Anki a cada paso.
PREVIEW_DELAY_MS = 200
_SWATCH = 16  # px, como las muestras de los temas de GritMap


def swatch_colors(theme_id: str, night: bool) -> tuple[str, str, str]:
    """Fondo, borde y color de acción de una paleta en el modo indicado."""
    palette = themes.THEMES[theme_id]["colors"]

    def pick(name: str) -> str:
        entry = palette[name]
        return entry["dark"] if night else entry["light"]

    return pick("CANVAS"), pick("BORDER_STRONG"), pick("BUTTON_PRIMARY_BG")


def _swatch(theme_id: str) -> QIcon:
    """Muestra de la paleta en el modo activo: su fondo con un punto de su acción.

    Regla de FIX-007 de GritMap: toda muestra de color se toma del modo activo, leído
    en el momento de pintarla.
    """
    canvas, border, accent = swatch_colors(theme_id, theme_manager.night_mode)
    pixmap = QPixmap(_SWATCH, _SWATCH)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor(border))
    painter.setBrush(QColor(canvas))
    painter.drawRoundedRect(0, 0, _SWATCH - 1, _SWATCH - 1, 3, 3)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(accent))
    painter.drawEllipse(4, 4, _SWATCH - 9, _SWATCH - 9)
    painter.end()
    return QIcon(pixmap)


def _subtle(label: QLabel) -> QLabel:
    """Texto secundario: el color que Anki da a los textos de ejemplo de los campos,
    que sigue al tema y a la paleta sin pintar nada a mano."""
    label.setForegroundRole(QPalette.ColorRole.PlaceholderText)
    return label


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

        self._combo = QComboBox()
        self._combo.setIconSize(QSize(_SWATCH, _SWATCH))
        for theme_id in themes.THEMES:
            name = strings.THEME_NAMES[theme_id]
            if theme_id == themes.DEFAULT_THEME:
                name += strings.DEFAULT_SUFFIX
            self._combo.addItem(_swatch(theme_id), name, theme_id)
        self._description = _subtle(QLabel())
        # Ancho de la descripción más larga: al cambiar de paleta, la ventana no cambia
        # de tamaño y ninguna línea se corta.
        metrics = self._description.fontMetrics()
        self._description.setMinimumWidth(
            max(metrics.horizontalAdvance(text) for text in strings.THEME_DESCRIPTIONS.values())
        )
        note = _subtle(QLabel(strings.DAY_AND_NIGHT))
        note.setWordWrap(True)

        form = QFormLayout()
        form.addRow(strings.PALETTE_LABEL, self._combo)
        form.addRow("", self._description)
        form.addRow("", note)

        layout = QVBoxLayout(self)
        if not self._preview_enabled:
            notice = QLabel(strings.HIGH_CONTRAST)
            notice.setWordWrap(True)
            layout.addWidget(notice)
        layout.addLayout(form)
        if errors.failures() and errors.logs_folder():
            layout.addLayout(self._failures_row())
        layout.addSpacing(6)

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

        self.select(self._original)
        self._show_description()
        self._combo.currentIndexChanged.connect(self._on_changed)
        self._combo.setFocus()  # el teclado empieza en la lista
        # Regla de FIX-018 de GritMap: las muestras se repintan al cambiar de día a noche,
        # y el gancho se quita al cerrar la ventana.
        gui_hooks.theme_did_change.append(self._refresh_swatches)

    def _failures_row(self) -> QHBoxLayout:
        """Solo si hubo fallos en la sesión: una línea y un botón para ver el registro."""
        row = QHBoxLayout()
        text = _subtle(QLabel(strings.FAILURES))
        text.setWordWrap(True)
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

    @guard
    def _refresh_swatches(self) -> None:
        for index in range(self._combo.count()):
            theme_id = self._combo.itemData(index)
            if isinstance(theme_id, str):
                self._combo.setItemIcon(index, _swatch(theme_id))

    def select(self, theme_id: str) -> None:
        index = self._combo.findData(theme_id)
        if index >= 0:
            self._combo.setCurrentIndex(index)

    def selected_id(self) -> str:
        theme_id = self._combo.currentData()
        return theme_id if isinstance(theme_id, str) else themes.current_id()

    def _show_description(self) -> None:
        self._description.setText(strings.THEME_DESCRIPTIONS[self.selected_id()])

    def restore_defaults(self) -> None:
        """Elige Nocturne, y la vista previa la muestra."""
        self.select(themes.DEFAULT_THEME)

    def _on_changed(self, _index: int) -> None:
        self._show_description()
        if self._preview_enabled:
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

    def done(self, result: int) -> None:
        # Se quita aquí, nunca desde dentro del propio gancho; remove no falla si ya no está.
        gui_hooks.theme_did_change.remove(self._refresh_swatches)
        super().done(result)


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
