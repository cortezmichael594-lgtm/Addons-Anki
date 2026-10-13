"""Ventanas de opciones del complemento.

Criterio de idiomas: todo lo que Anki (o Qt, que Anki configura con el mismo
idioma) ya trae traducido se toma de ahi y no se vuelve a escribir aqui. Eso
incluye los botones normales de una ventana -- Aceptar, Cancelar y Restaurar
valores predeterminados -- y el formato en que se escriben las fechas. En los
idiomas para los que Qt no trae traduccion, esos tres botones toman el texto
propio del complemento.

La lista de mazos y la configuracion se leen en segundo plano antes de abrir
la ventana, y lo que se guarda en la coleccion tambien se escribe en segundo
plano: Anki nunca se queda esperando a la coleccion por esta ventana.
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-10-08) — En modo noche, la muestra de color de cada tema
#                        ensenaba el tono del modo dia.
# FIX-016 (2026-10-13) — La ventana de excluir mazos no ensenaba lo que se
#                        excluye de verdad: contaba mazos que ya no existen y
#                        dejaba sin marcar los submazos excluidos.
# FIX-017 (2026-10-13) — Intro sobre un boton con el foco no lo pulsaba:
#                        cerraba Opciones o anadia una fecha.
# FIX-018 (2026-10-13) — Las muestras de color de los temas no cambiaban al
#                        pasar entre modo dia y noche con la ventana abierta.

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from anki.collection import Collection
from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.qt import (
    QCheckBox,
    QColor,
    QComboBox,
    QCoreApplication,
    QDate,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QIcon,
    QKeySequence,
    QLineEdit,
    QLocale,
    QPainter,
    QPixmap,
    QPushButton,
    QRectF,
    QShortcut,
    QSize,
    QSpinBox,
    Qt,
    QTreeWidget,
    QTreeWidgetItem,
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
    save_appearance,
    save_scoped,
)
from .data import MEASURES, WINDOWS
from .decks import DeckEntry, all_deck_entries
from .errors import guarded, log_exception
from .i18n import anki_text, fill, lang, plural_key, t
from .palettes import PAST_DARK, PAST_LIGHT, THEME_NAMES
from .state import state

# Muestra de cada tema: cinco tonos de su escala, de claro a oscuro.
_SWATCH_SIZE = QSize(44, 12)
# Nombres que caben en el globo del boton de mazos excluidos.
_TOOLTIP_MAX_NAMES = 15
_SPIN_WIDTH = 110
_DECK_ROLE = Qt.ItemDataRole.UserRole
_OWN_STATE_ROLE = Qt.ItemDataRole.UserRole + 1


@dataclass(frozen=True)
class _Decks:
    """Mazos leidos de la coleccion al abrir la ventana."""

    # Los que se pueden elegir, en el orden de la pantalla principal.
    selectable: list[DeckEntry]
    # Nombre de cada mazo que existe (tambien filtrados y el predeterminado
    # vacio): lo que de verdad puede excluir el mapa.
    existing: dict[int, str]


def _count_text(base: str, count: int) -> str:
    """«3 mazos excluidos», con la cifra a la manera del idioma."""
    if lang() == "es":
        number = f"{count:,}".replace(",", ".")
    else:
        number = QLocale().toString(count)
    return fill(plural_key(base, count), count=number)


def _date_format() -> str:
    """Formato corto de fecha del idioma, siempre con el ano en cuatro cifras."""
    fmt = QLocale().dateFormat(QLocale.FormatType.ShortFormat)
    if "yyyy" not in fmt:
        fmt = fmt.replace("yy", "yyyy")
    return fmt


def _format_day(day: date) -> str:
    """Fecha escrita como la escribe Anki en el idioma activo."""
    qdate = QDate(day.year, day.month, day.day)
    try:
        return QLocale().toString(qdate, _date_format())
    except Exception:
        return day.isoformat()


def _theme_swatch(name: str) -> QIcon:
    """Muestra del tema con los tonos que se veran en el mapa ahora mismo."""
    # --- FIX-007 (2026-10-08) --------------------------------------
    # Sintoma: con Anki en modo noche, la muestra de cada tema en el desplegable
    #          ensenaba el tono de dia, distinto del que luego se ve en el mapa.
    # Causa: la muestra se tomaba siempre de la escala de dia.
    # Regla: toda muestra de color se toma de la escala del modo activo, leido
    #        en el momento de construir la ventana.
    # ---------------------------------------------------------------
    scale = PAST_DARK if theme_manager.night_mode else PAST_LIGHT
    tones = scale.get(name, scale[DEFAULT_CONFIG.theme])[1::2]
    ratio = mw.devicePixelRatioF() if mw is not None else 1.0
    pixmap = QPixmap(round(_SWATCH_SIZE.width() * ratio), round(_SWATCH_SIZE.height() * ratio))
    pixmap.setDevicePixelRatio(ratio)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    segment = _SWATCH_SIZE.width() / len(tones)
    for index, tone in enumerate(tones):
        painter.fillRect(
            QRectF(index * segment, 0, segment, _SWATCH_SIZE.height()), QColor(tone)
        )
    painter.end()
    return QIcon(pixmap)


def _sorted_theme_names() -> list[str]:
    return sorted(THEME_NAMES, key=lambda name: t(f"theme_{name}").casefold())


def _spin_box(minimum: int, maximum: int) -> QSpinBox:
    box = QSpinBox()
    box.setRange(minimum, maximum)
    box.setSingleStep(1)
    box.setAccelerated(True)
    box.setSuffix(" px")
    box.setMaximumWidth(_SPIN_WIDTH)
    return box


def _without_px(key: str) -> str:
    """Rotulo sin «(px)»: la unidad ya la lleva el propio campo."""
    return re.sub(r"\s*\(px\)", "", t(key))


def _standard_buttons(
    dialog: QDialog, buttons: QDialogButtonBox.StandardButton
) -> QDialogButtonBox:
    """Botonera con los textos que ya trae traducidos Qt.

    Si Qt no trae traduccion para el idioma de Anki (unos 25 idiomas), los
    botones toman el texto propio del complemento en lugar de salir en ingles.
    """
    box = QDialogButtonBox(buttons)
    qconnect(box.accepted, dialog.accept)
    qconnect(box.rejected, dialog.reject)
    if lang() != "en" and QCoreApplication.translate("QPlatformTheme", "Cancel") == "Cancel":
        for standard, key in (
            (QDialogButtonBox.StandardButton.Ok, "opt_save"),
            (QDialogButtonBox.StandardButton.Cancel, "opt_cancel"),
            (QDialogButtonBox.StandardButton.RestoreDefaults, "opt_defaults"),
        ):
            button = box.button(standard)
            if button is not None:
                button.setText(t(key))
    return box


class ExcludeDecksDialog(QDialog):
    """Arbol de mazos con casillas, como en la pantalla principal, y buscador."""

    def __init__(self, parent: QWidget, excluded: tuple[int, ...], decks: _Decks) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_exclude"))
        disable_help_button(self)
        self.setMinimumWidth(360)
        self._decks = decks
        shown = {entry.deck_id for entry in decks.selectable}
        # Excluidos que existen pero no salen en la lista (un mazo filtrado o
        # el predeterminado vacio): se conservan tal cual al aceptar.
        self._hidden_excluded = tuple(
            deck_id for deck_id in excluded if deck_id in decks.existing and deck_id not in shown
        )

        # Sin textos explicativos: la ventana es solo la lista de mazos y su
        # buscador. Es una decision del cliente; no anadir frases de ayuda.
        self._search = QLineEdit()
        self._search.setPlaceholderText(anki_text("actions_search", "opt_exclude_btn"))
        self._search.setClearButtonEnabled(True)
        qconnect(self._search.textChanged, self._filter)

        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setUniformRowHeights(True)
        self._tree.setMinimumHeight(220)
        excluded_set = set(excluded)
        items: dict[str, QTreeWidgetItem] = {}
        for entry in decks.selectable:
            parent_name = entry.name.rpartition("::")[0]
            parent_item = items.get(parent_name)
            item = QTreeWidgetItem([entry.leaf_name])
            item.setToolTip(0, entry.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            own = Qt.CheckState.Checked if entry.deck_id in excluded_set else Qt.CheckState.Unchecked
            item.setCheckState(0, own)
            item.setData(0, _DECK_ROLE, entry.deck_id)
            item.setData(0, _OWN_STATE_ROLE, own == Qt.CheckState.Checked)
            if parent_item is not None:
                parent_item.addChild(item)
            else:
                self._tree.addTopLevelItem(item)
            items[entry.name] = item
        self._tree.expandAll()
        for index in range(self._tree.topLevelItemCount()):
            top = self._tree.topLevelItem(index)
            if top is not None:
                self._sync_children(top)
        qconnect(self._tree.itemChanged, self._on_item_changed)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
        )

        layout = QVBoxLayout()
        layout.addWidget(self._search)
        layout.addWidget(self._tree)
        layout.addWidget(buttons)
        self.setLayout(layout)
        restoreGeom(self, "gritmapDecks", default_size=(400, 480))
        self._search.setFocus()

    # --- FIX-016 (2026-10-13) --------------------------------------
    # Sintoma: al excluir «Idiomas», sus submazos seguian sin marcar en la
    #          lista aunque el mapa ya no los contaba, y el boton decia «3
    #          mazos excluidos» cuando uno de ellos ya no existia.
    # Causa: cada mazo tenia su casilla suelta, sin reflejar a sus submazos, y
    #        la cifra contaba los identificadores guardados, no los mazos que
    #        existen.
    # Regla: lo que ensena la ventana es exactamente lo que excluye el mapa:
    #        un mazo marcado marca y bloquea a sus submazos, y solo se cuentan
    #        y se nombran mazos que existen.
    # ---------------------------------------------------------------
    def _sync_children(self, item: QTreeWidgetItem, locked: bool = False) -> None:
        """Marca y bloquea los submazos de un mazo marcado; si no, les devuelve
        su propia casilla."""
        if locked:
            item.setCheckState(0, Qt.CheckState.Checked)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
        else:
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)
            own = bool(item.data(0, _OWN_STATE_ROLE))
            item.setCheckState(0, Qt.CheckState.Checked if own else Qt.CheckState.Unchecked)
        child_locked = locked or item.checkState(0) == Qt.CheckState.Checked
        for index in range(item.childCount()):
            child = item.child(index)
            if child is not None:
                self._sync_children(child, child_locked)

    def _on_item_changed(self, item: QTreeWidgetItem, _column: int) -> None:
        if not item.flags() & Qt.ItemFlag.ItemIsEnabled:
            return
        item.setData(0, _OWN_STATE_ROLE, item.checkState(0) == Qt.CheckState.Checked)
        self._tree.blockSignals(True)
        try:
            self._sync_children(item)
        finally:
            self._tree.blockSignals(False)

    def _filter(self, text: str) -> None:
        """Deja a la vista los mazos cuyo nombre contiene el texto, con sus padres."""
        wanted = text.strip().casefold()

        def show(item: QTreeWidgetItem) -> bool:
            name = str(item.toolTip(0)).casefold()
            visible = not wanted or wanted in name
            for index in range(item.childCount()):
                child = item.child(index)
                if child is not None and show(child):
                    visible = True
            item.setHidden(not visible)
            return visible

        for index in range(self._tree.topLevelItemCount()):
            top = self._tree.topLevelItem(index)
            if top is not None:
                show(top)

    def checked_decks(self) -> tuple[int, ...]:
        """Mazos marcados por la persona (los submazos bloqueados ya van con su padre)."""
        ids: list[int] = list(self._hidden_excluded)
        pending = [self._tree.topLevelItem(i) for i in range(self._tree.topLevelItemCount())]
        while pending:
            item = pending.pop()
            if item is None:
                continue
            raw_id = item.data(0, _DECK_ROLE)
            enabled = bool(item.flags() & Qt.ItemFlag.ItemIsEnabled)
            if enabled and item.checkState(0) == Qt.CheckState.Checked and isinstance(raw_id, int):
                ids.append(raw_id)
            pending.extend(item.child(i) for i in range(item.childCount()))
        return tuple(ids)

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
        self.setMinimumWidth(420)
        self._dates: list[KeyDate] = list(key_dates)

        # Sin textos explicativos: solo la lista y los controles para anadir y
        # quitar. Es una decision del cliente; no anadir aqui frases de ayuda.
        self._list = QTreeWidget()
        self._list.setColumnCount(2)
        self._list.setHeaderHidden(True)
        self._list.setRootIsDecorated(False)
        self._list.setUniformRowHeights(True)
        self._list.setMinimumHeight(160)

        self._name = QLineEdit()
        self._name.setPlaceholderText(t("kd_name_ph"))
        self._name.setMaxLength(MAX_LABEL_LEN)
        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDisplayFormat(_date_format())
        self._date.setDateRange(_qdate(KEY_DATE_MIN), _qdate(KEY_DATE_MAX))
        self._date.setDate(QDate.currentDate())

        # «Anadir» es el boton por defecto: Intro tras escribir un nombre anade
        # la fecha. Con el foco en otro boton, Intro pulsa ese boton.
        add_button = QPushButton(anki_text("actions_add", "kd_add"))
        add_button.setDefault(True)
        qconnect(add_button.clicked, self._add)
        add_row = QHBoxLayout()
        add_row.addWidget(self._name, 1)
        add_row.addWidget(self._date)
        add_row.addWidget(add_button)

        self._remove_button = QPushButton(anki_text("actions_delete", "kd_remove"))
        self._remove_button.setEnabled(False)
        qconnect(self._remove_button.clicked, self._remove)
        qconnect(self._list.itemSelectionChanged, self._update_remove_state)
        # La tecla Supr borra solo con el foco en la lista, nunca mientras se
        # escribe o con el foco en otro boton.
        delete = QShortcut(QKeySequence(QKeySequence.StandardKey.Delete), self._list)
        delete.setContext(Qt.ShortcutContext.WidgetShortcut)
        qconnect(delete.activated, self._remove)
        remove_row = QHBoxLayout()
        remove_row.addStretch(1)
        remove_row.addWidget(self._remove_button)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
        )

        layout = QVBoxLayout()
        layout.addWidget(self._list)
        layout.addLayout(remove_row)
        layout.addLayout(add_row)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self._rebuild()
        restoreGeom(self, "gritmapKeyDates", default_size=(460, 420))
        self._name.setFocus()

    def _sort_dates(self) -> None:
        self._dates.sort(key=lambda kd: (kd.day, kd.label.casefold()))

    def _rebuild(self, select: KeyDate | None = None) -> None:
        self._sort_dates()
        self._list.clear()
        for key_date in self._dates:
            item = QTreeWidgetItem([_format_day(key_date.day), key_date.label])
            self._list.addTopLevelItem(item)
            if select is not None and key_date == select:
                self._list.setCurrentItem(item)
        self._list.resizeColumnToContents(0)
        self._update_remove_state()

    def _current_row(self) -> int:
        item = self._list.currentItem()
        return self._list.indexOfTopLevelItem(item) if item is not None else -1

    def _update_remove_state(self) -> None:
        self._remove_button.setEnabled(self._current_row() >= 0)

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
        row = self._current_row()
        if 0 <= row < len(self._dates):
            del self._dates[row]
            # Queda seleccionada la siguiente, para poder borrar varias seguidas.
            following = self._dates[min(row, len(self._dates) - 1)] if self._dates else None
            self._rebuild(select=following)

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
    def __init__(self, parent: QWidget, cfg: Config, decks: _Decks) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_title"))
        disable_help_button(self)
        self.setMinimumWidth(440)
        self._decks = decks

        self._theme = QComboBox()
        self._theme.setIconSize(_SWATCH_SIZE)
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

        # --- FIX-017 (2026-10-13) --------------------------------------
        # Sintoma: con el foco en «Seleccionar mazos» o en Restaurar, Intro
        #          cerraba Opciones y guardaba; en Fechas clave, con el foco en
        #          Aceptar, Intro intentaba anadir una fecha.
        # Causa: se les habia quitado a esos botones la respuesta a Intro
        #        (autoDefault), y entonces Intro iba al boton por defecto.
        # Regla: los botones conservan la respuesta a Intro que les da Qt; solo
        #        se elige cual es el boton por defecto.
        # ---------------------------------------------------------------
        self._excluded: tuple[int, ...] = ()
        self._exclude_button = QPushButton()
        qconnect(self._exclude_button.clicked, self._open_exclude)

        self._key_dates: tuple[KeyDate, ...] = ()
        self._key_dates_button = QPushButton()
        qconnect(self._key_dates_button.clicked, self._open_key_dates)

        form = QFormLayout()
        form.addRow(t("opt_theme"), self._theme)
        form.addRow(t("opt_measure"), self._measure)
        form.addRow(_without_px("opt_cell"), self._cell_size)
        form.addRow(_without_px("opt_radius"), self._border_radius)
        form.addRow(t("opt_window"), self._avg_window)
        form.addRow(t("opt_exclude"), self._exclude_button)
        form.addRow(t("opt_key_dates"), self._key_dates_button)
        form.addRow("", self._show_week)

        buttons = _standard_buttons(
            self,
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults,
        )
        restore_button = buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore_button is not None:
            qconnect(restore_button.clicked, self._restore_defaults)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addSpacing(6)
        layout.addWidget(buttons)
        self.setLayout(layout)

        self._apply(cfg)
        restoreGeom(self, "gritmapOptions")
        gui_hooks.theme_did_change.append(self._refresh_swatches)

    # --- FIX-018 (2026-10-13) --------------------------------------
    # Sintoma: con la ventana abierta, al pasar Anki de modo dia a noche (o al
    #          reves) las muestras de los temas seguian con los tonos del modo
    #          anterior.
    # Causa: las muestras se pintaban una sola vez, al construir la ventana.
    # Regla: todo color que dependa del modo se vuelve a pintar con
    #        gui_hooks.theme_did_change, y el gancho se quita al cerrar la
    #        ventana (nunca desde dentro del propio gancho).
    # ---------------------------------------------------------------
    @guarded()
    def _refresh_swatches(self) -> None:
        for index in range(self._theme.count()):
            name = self._theme.itemData(index)
            if isinstance(name, str):
                self._theme.setItemIcon(index, _theme_swatch(name))

    # Sub-ventanas
    def _open_exclude(self, _checked: bool = False) -> None:
        dialog = ExcludeDecksDialog(self, self._excluded, self._decks)
        try:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._excluded = dialog.checked_decks()
                self._update_exclude_label()
        finally:
            dialog.deleteLater()

    def _open_key_dates(self, _checked: bool = False) -> None:
        dialog = KeyDatesDialog(self, self._key_dates)
        try:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._key_dates = dialog.selected_dates()
                self._update_key_dates_label()
        finally:
            dialog.deleteLater()

    # Etiquetas de los dos botones que abren sub-ventanas
    def _update_exclude_label(self) -> None:
        names = [self._decks.existing[d] for d in self._excluded if d in self._decks.existing]
        if names:
            self._exclude_button.setText(_count_text("opt_exclude_count", len(names)))
            shown = names[:_TOOLTIP_MAX_NAMES]
            if len(names) > len(shown):
                shown.append("…")
            self._exclude_button.setToolTip("\n".join(shown))
        else:
            self._exclude_button.setText(t("opt_exclude_btn"))
            self._exclude_button.setToolTip("")

    def _update_key_dates_label(self) -> None:
        count = len(self._key_dates)
        if count:
            self._key_dates_button.setText(_count_text("opt_key_dates_count", count))
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
        # FIX-016: solo los mazos que existen; los demas se dejan de guardar.
        self._excluded = tuple(d for d in cfg.excluded_decks if d in self._decks.existing)
        self._update_exclude_label()
        self._key_dates = cfg.key_dates
        self._update_key_dates_label()

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
        # remove no falla si ya se quito antes.
        gui_hooks.theme_did_change.remove(self._refresh_swatches)
        try:
            saveGeom(self, "gritmapOptions")
        except Exception as exc:
            log_exception("options.HeatmapOptionsDialog.done", exc)
        super().done(result)


# Se conserva una referencia mientras la ventana existe: sin ella Python
# podria destruir el objeto y la ventana desapareceria sola.
_dialog: HeatmapOptionsDialog | None = None
# Lectura de la coleccion en marcha: evita abrir dos ventanas con dos clics.
_opening = False


def open_options() -> None:
    """Lee mazos y opciones en segundo plano y abre la ventana con ellos."""
    global _opening
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    if _opening or mw.col is None:
        return
    _opening = True
    generation = state.generation

    def op(col: Collection) -> tuple[Config, _Decks]:
        selectable = all_deck_entries(col, skip_empty_default=True, include_filtered=False)
        existing = {entry.deck_id: entry.name for entry in all_deck_entries(col)}
        return load_config(col), _Decks(selectable=selectable, existing=existing)

    @guarded()
    def on_success(result: tuple[Config, _Decks]) -> None:
        global _opening
        _opening = False
        if generation != state.generation or mw.col is None:
            return
        # Se aplaza para no abrir una ventana modal dentro de la respuesta
        # de la operacion.
        mw.progress.single_shot(0, lambda: _show(*result), False)

    @guarded()
    def on_failure(exc: Exception) -> None:
        global _opening
        _opening = False
        log_exception("options.open_options", exc)

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()


def _show(cfg: Config, decks: _Decks) -> None:
    global _dialog
    try:
        _dialog = HeatmapOptionsDialog(mw, cfg, decks)
        accepted = _dialog.exec() == QDialog.DialogCode.Accepted
        selected = _dialog.selected_config() if accepted else None
        _dialog.deleteLater()
        _dialog = None
        if selected is not None:
            _save(selected)
    except Exception as exc:
        _dialog = None
        log_exception("options.show", exc)


def _save(selected: Config) -> None:
    """Guarda la apariencia aqui y lo de la coleccion en segundo plano; despues,
    el mapa se redibuja en su sitio."""
    save_appearance(selected)
    generation = state.generation

    def op(col: Collection) -> None:
        save_scoped(col, selected)

    @guarded()
    def on_success(_result: None) -> None:
        if generation == state.generation and state.apply_config_change is not None:
            state.apply_config_change()

    @guarded()
    def on_failure(exc: Exception) -> None:
        log_exception("options.save", exc)

    QueryOp(parent=mw, op=op, success=on_success).failure(on_failure).run_in_background()
