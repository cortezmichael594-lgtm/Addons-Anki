"""Ventanas de opciones del complemento.

Criterio de idiomas: todo lo que Anki (o Qt, que Anki configura con el mismo
idioma) ya trae traducido se toma de ahi y no se vuelve a escribir aqui. Eso
incluye los botones normales de una ventana -- Aceptar, Cancelar y Restaurar
valores predeterminados -- y el formato en que se escriben las fechas. Asi el
texto es correcto en todos los idiomas en que se puede usar Anki, no solo en
los que este complemento tenga traducidos.
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-08) — En modo noche, la muestra de color de cada tema
#                        ensenaba el tono del modo dia.

from __future__ import annotations

from datetime import date

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QColor,
    QComboBox,
    QDate,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QIcon,
    QKeySequence,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QLocale,
    QPixmap,
    QPushButton,
    Qt,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.theme import theme_manager
from aqt.utils import disable_help_button, restoreGeom, saveGeom, tooltip

from .config import (
    BORDER_RADIUS_MAX,
    BORDER_RADIUS_MIN,
    CELL_SIZE_MAX,
    CELL_SIZE_MIN,
    DEFAULT_CONFIG,
    KEY_DATE_MAX,
    KEY_DATE_MIN,
    MAX_KEY_DATES,
    MAX_LABEL_LEN,
    Config,
    KeyDate,
    clean_label,
    load_config,
    save_config,
)
from .data import MEASURES, WINDOWS
from .decks import DeckEntry, all_deck_entries
from .errors import log_exception
from .i18n import anki_text, fill, t
from .palettes import PAST_DARK, PAST_LIGHT, THEME_NAMES
from .state import state

INDENT = "    "  # sangria por nivel, para escalonar los submazos en la lista


def _format_day(day: date) -> str:
    """Fecha escrita como la escribe Anki en el idioma activo."""
    qdate = QDate(day.year, day.month, day.day)
    try:
        return QLocale().toString(qdate, QLocale.FormatType.ShortFormat)
    except Exception:
        return day.isoformat()


def _color_icon(color_hex: str) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(QColor(color_hex))
    return QIcon(pixmap)


def _theme_swatch(name: str) -> QIcon:
    """Muestra del tema con el tono que se vera en el mapa ahora mismo."""
    # --- FIX-007 (2026-10-08) --------------------------------------
    # Sintoma: con Anki en modo noche, la muestra de cada tema en el desplegable
    #          ensenaba el tono de dia, distinto del que luego se ve en el mapa.
    # Causa: la muestra se tomaba siempre de la escala de dia.
    # Regla: toda muestra de color se toma de la escala del modo activo, leido
    #        en el momento de construir la ventana.
    # ---------------------------------------------------------------
    scale = PAST_DARK if theme_manager.night_mode else PAST_LIGHT
    return _color_icon(scale[name][5])


def _sorted_theme_names() -> list[str]:
    return sorted(THEME_NAMES, key=lambda name: t(f"theme_{name}").casefold())


def _spin_box(minimum: int, maximum: int) -> QSpinBox:
    box = QSpinBox()
    box.setRange(minimum, maximum)
    box.setSingleStep(1)
    box.setAccelerated(True)
    return box


def _standard_buttons(
    dialog: QDialog, buttons: QDialogButtonBox.StandardButton
) -> QDialogButtonBox:
    """Botonera con los textos que ya trae traducidos el propio programa.

    A proposito no se les cambia el texto: Aceptar, Cancelar y Restaurar
    valores predeterminados salen tal cual en el idioma de Anki.
    """
    box = QDialogButtonBox(buttons)
    qconnect(box.accepted, dialog.accept)
    qconnect(box.rejected, dialog.reject)
    return box


def _selection_decks() -> list[DeckEntry]:
    if mw.col is None:
        return []
    return all_deck_entries(mw.col, skip_empty_default=True, include_filtered=False)


class ExcludeDecksDialog(QDialog):
    """Lista de mazos con casillas, escalonada como en la pantalla principal."""

    def __init__(self, parent: QWidget, excluded: tuple[int, ...]) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_exclude"))
        disable_help_button(self)
        self.setMinimumWidth(360)

        # Sin textos explicativos: la ventana es solo la lista de mazos. Es una
        # decision del cliente; no anadir aqui frases de ayuda.
        self._list = QListWidget()
        self._list.setMinimumHeight(200)
        excluded_set = set(excluded)
        for entry in _selection_decks():
            item = QListWidgetItem(INDENT * entry.depth + entry.leaf_name)
            item.setToolTip(entry.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked
                if entry.deck_id in excluded_set
                else Qt.CheckState.Unchecked
            )
            item.setData(Qt.ItemDataRole.UserRole, entry.deck_id)
            self._list.addItem(item)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
        )

        layout = QVBoxLayout()
        layout.addWidget(self._list)
        layout.addWidget(buttons)
        self.setLayout(layout)
        restoreGeom(self, "gritmapDecks", default_size=(380, 440))

    def checked_decks(self) -> tuple[int, ...]:
        ids: list[int] = []
        for index in range(self._list.count()):
            item = self._list.item(index)
            if item is None or item.checkState() != Qt.CheckState.Checked:
                continue
            raw_id = item.data(Qt.ItemDataRole.UserRole)
            if isinstance(raw_id, int):
                ids.append(raw_id)
        return tuple(ids)

    def deck_names(self) -> list[str]:
        checked = set(self.checked_decks())
        return [entry.name for entry in _selection_decks() if entry.deck_id in checked]

    def done(self, result: int) -> None:
        try:
            saveGeom(self, "gritmapDecks")
        except Exception as exc:
            log_exception("options.ExcludeDecksDialog.done", exc)
        super().done(result)


def _qdate(day: date) -> QDate:
    return QDate(day.year, day.month, day.day)


class KeyDatesDialog(QDialog):
    """Dias senalados que se resaltan en el mapa."""

    def __init__(self, parent: QWidget, key_dates: tuple[KeyDate, ...]) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_key_dates"))
        disable_help_button(self)
        self.setMinimumWidth(400)
        self._dates: list[KeyDate] = list(key_dates)

        # Sin textos explicativos: solo la lista y los controles para anadir y
        # quitar. Es una decision del cliente; no anadir aqui frases de ayuda.
        self._list = QListWidget()
        self._list.setMinimumHeight(160)

        self._name = QLineEdit()
        self._name.setPlaceholderText(t("kd_name_ph"))
        self._name.setMaxLength(MAX_LABEL_LEN)
        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDateRange(_qdate(KEY_DATE_MIN), _qdate(KEY_DATE_MAX))
        self._date.setDate(QDate.currentDate())

        add_button = QPushButton(anki_text("actions_add", "kd_add"))
        add_button.setAutoDefault(True)
        add_button.setDefault(True)
        qconnect(add_button.clicked, self._add)
        add_row = QHBoxLayout()
        add_row.addWidget(self._name, 1)
        add_row.addWidget(self._date)
        add_row.addWidget(add_button)

        self._remove_button = QPushButton(anki_text("actions_delete", "kd_remove"))
        self._remove_button.setEnabled(False)
        self._remove_button.setAutoDefault(False)
        self._remove_button.setShortcut(QKeySequence(QKeySequence.StandardKey.Delete))
        qconnect(self._remove_button.clicked, self._remove)
        qconnect(self._list.itemSelectionChanged, self._update_remove_state)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
        )
        # El boton por defecto es "Anadir": pulsar Intro tras escribir un
        # nombre anade la fecha en vez de cerrar la ventana.
        for standard in (
            QDialogButtonBox.StandardButton.Ok,
            QDialogButtonBox.StandardButton.Cancel,
        ):
            button = buttons.button(standard)
            if button is not None:
                button.setAutoDefault(False)
                button.setDefault(False)

        layout = QVBoxLayout()
        layout.addWidget(self._list)
        layout.addLayout(add_row)
        layout.addWidget(self._remove_button)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self._rebuild()
        restoreGeom(self, "gritmapKeyDates", default_size=(440, 420))

    def _sort_dates(self) -> None:
        self._dates.sort(key=lambda kd: (kd.day, kd.label.casefold()))

    def _rebuild(self, select: KeyDate | None = None) -> None:
        self._sort_dates()
        self._list.clear()
        for key_date in self._dates:
            item = QListWidgetItem(f"{_format_day(key_date.day)}  —  {key_date.label}")
            self._list.addItem(item)
            if select is not None and key_date == select:
                self._list.setCurrentItem(item)
        self._update_remove_state()

    def _update_remove_state(self) -> None:
        self._remove_button.setEnabled(self._list.currentRow() >= 0)

    def _add(self, _checked: bool = False) -> None:
        label = clean_label(self._name.text())
        if not label:
            tooltip(t("kd_name_required"), parent=self)
            self._name.setFocus()
            return
        if len(self._dates) >= MAX_KEY_DATES:
            tooltip(fill("kd_limit", count=MAX_KEY_DATES), parent=self)
            return
        key_date = KeyDate(day=self._date.date().toPyDate(), label=label)
        if key_date in self._dates:
            tooltip(t("kd_duplicate"), parent=self)
            return
        self._dates.append(key_date)
        self._rebuild(select=key_date)
        self._name.clear()
        self._name.setFocus()

    def _remove(self, _checked: bool = False) -> None:
        row = self._list.currentRow()
        if 0 <= row < len(self._dates):
            del self._dates[row]
            self._rebuild()

    def selected_dates(self) -> tuple[KeyDate, ...]:
        self._sort_dates()
        return tuple(self._dates)

    def done(self, result: int) -> None:
        try:
            saveGeom(self, "gritmapKeyDates")
        except Exception as exc:
            log_exception("options.KeyDatesDialog.done", exc)
        super().done(result)


class HeatmapOptionsDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_title"))
        disable_help_button(self)
        self.setMinimumWidth(420)

        self._theme = QComboBox()
        for name in _sorted_theme_names():
            self._theme.addItem(_theme_swatch(name), t(f"theme_{name}"), name)
        self._measure = QComboBox()
        for measure in MEASURES:
            self._measure.addItem(t(f"measure_{measure}"), measure)
        self._cell_size = _spin_box(CELL_SIZE_MIN, CELL_SIZE_MAX)
        self._border_radius = _spin_box(BORDER_RADIUS_MIN, BORDER_RADIUS_MAX)
        self._avg_window = QComboBox()
        for days in WINDOWS:
            label = t("window_all") if days == 0 else fill("window_days", count=days)
            self._avg_window.addItem(label, days)
        self._show_week = QCheckBox(t("opt_show_week"))

        self._excluded: tuple[int, ...] = ()
        self._excluded_names: list[str] = []
        self._exclude_button = QPushButton()
        self._exclude_button.setAutoDefault(False)
        qconnect(self._exclude_button.clicked, self._open_exclude)

        self._key_dates: tuple[KeyDate, ...] = ()
        self._key_dates_button = QPushButton()
        self._key_dates_button.setAutoDefault(False)
        qconnect(self._key_dates_button.clicked, self._open_key_dates)

        form = QFormLayout()
        form.addRow(t("opt_theme"), self._theme)
        form.addRow(t("opt_measure"), self._measure)
        form.addRow(t("opt_cell"), self._cell_size)
        form.addRow(t("opt_radius"), self._border_radius)
        form.addRow(t("opt_window"), self._avg_window)
        form.addRow(t("opt_exclude"), self._exclude_button)
        form.addRow(t("opt_key_dates"), self._key_dates_button)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults,
        )
        restore_button = buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore_button is not None:
            restore_button.setAutoDefault(False)
            qconnect(restore_button.clicked, self._restore_defaults)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self._show_week)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self._apply(load_config())
        restoreGeom(self, "gritmapOptions")

    # Sub-ventanas
    def _open_exclude(self, _checked: bool = False) -> None:
        dialog = ExcludeDecksDialog(self, self._excluded)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._excluded = dialog.checked_decks()
            self._excluded_names = dialog.deck_names()
            self._update_exclude_label()

    def _open_key_dates(self, _checked: bool = False) -> None:
        dialog = KeyDatesDialog(self, self._key_dates)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._key_dates = dialog.selected_dates()
            self._update_key_dates_label()

    # Etiquetas de los dos botones que abren sub-ventanas
    def _update_exclude_label(self) -> None:
        count = len(self._excluded)
        if count:
            self._exclude_button.setText(fill("opt_exclude_count", count=count))
            self._exclude_button.setToolTip("\n".join(self._excluded_names))
        else:
            self._exclude_button.setText(t("opt_exclude_btn"))
            self._exclude_button.setToolTip("")

    def _update_key_dates_label(self) -> None:
        count = len(self._key_dates)
        if count:
            self._key_dates_button.setText(fill("opt_key_dates_count", count=count))
            self._key_dates_button.setToolTip(
                "\n".join(f"{_format_day(kd.day)} — {kd.label}" for kd in self._key_dates)
            )
        else:
            self._key_dates_button.setText(t("opt_key_dates_btn"))
            self._key_dates_button.setToolTip("")

    def _apply(self, cfg: Config) -> None:
        self._theme.setCurrentIndex(max(self._theme.findData(cfg.theme), 0))
        self._measure.setCurrentIndex(max(self._measure.findData(cfg.measure), 0))
        self._cell_size.setValue(cfg.cell_size)
        self._border_radius.setValue(cfg.border_radius)
        self._avg_window.setCurrentIndex(max(self._avg_window.findData(cfg.avg_window), 0))
        self._show_week.setChecked(cfg.show_week_diff)
        self._excluded = cfg.excluded_decks
        self._excluded_names = self._names_for(cfg.excluded_decks)
        self._update_exclude_label()
        self._key_dates = cfg.key_dates
        self._update_key_dates_label()

    @staticmethod
    def _names_for(deck_ids: tuple[int, ...]) -> list[str]:
        wanted = set(deck_ids)
        return [entry.name for entry in _selection_decks() if entry.deck_id in wanted]

    def _restore_defaults(self, _checked: bool = False) -> None:
        """Vuelve a los valores recomendados.

        Solo repone la apariencia: los mazos excluidos y las fechas clave son
        datos que la persona ha introducido y se quedan como estaban, para que
        pulsar este boton nunca borre trabajo suyo.
        """
        self._theme.setCurrentIndex(max(self._theme.findData(DEFAULT_CONFIG.theme), 0))
        self._measure.setCurrentIndex(max(self._measure.findData(DEFAULT_CONFIG.measure), 0))
        self._cell_size.setValue(DEFAULT_CONFIG.cell_size)
        self._border_radius.setValue(DEFAULT_CONFIG.border_radius)
        self._avg_window.setCurrentIndex(
            max(self._avg_window.findData(DEFAULT_CONFIG.avg_window), 0)
        )
        self._show_week.setChecked(DEFAULT_CONFIG.show_week_diff)

    def selected_config(self) -> Config:
        theme_data = self._theme.currentData()
        theme = theme_data if isinstance(theme_data, str) else DEFAULT_CONFIG.theme
        measure_data = self._measure.currentData()
        measure = measure_data if measure_data in MEASURES else DEFAULT_CONFIG.measure
        window_data = self._avg_window.currentData()
        avg_window = window_data if window_data in WINDOWS else DEFAULT_CONFIG.avg_window
        return Config(
            theme=theme,
            measure=str(measure),
            cell_size=self._cell_size.value(),
            border_radius=self._border_radius.value(),
            avg_window=int(avg_window),
            show_week_diff=self._show_week.isChecked(),
            excluded_decks=self._excluded,
            key_dates=self._key_dates,
        )

    def done(self, result: int) -> None:
        try:
            saveGeom(self, "gritmapOptions")
        except Exception as exc:
            log_exception("options.HeatmapOptionsDialog.done", exc)
        super().done(result)


# Se conserva una referencia mientras la ventana existe: sin ella Python
# podria destruir el objeto y la ventana desapareceria sola.
_dialog: HeatmapOptionsDialog | None = None


def open_options() -> None:
    global _dialog
    try:
        if _dialog is not None and _dialog.isVisible():
            _dialog.raise_()
            _dialog.activateWindow()
            return
        _dialog = HeatmapOptionsDialog(mw)
        accepted = _dialog.exec() == QDialog.DialogCode.Accepted
        selected = _dialog.selected_config() if accepted else None
        _dialog = None
        if selected is None:
            return
        save_config(selected)
        if state.apply_config_change is not None:
            state.apply_config_change()
    except Exception as exc:
        _dialog = None
        log_exception("options.open_options", exc)
