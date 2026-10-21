"""El panel de opciones.

Lo ESTRUCTURAL del panel (los botones Guardar, Cancelar, Aceptar y Restaurar
valores predeterminados) no se traduce aqui: son los botones estandar de Qt,
que Anki localiza al fijar el idioma de la aplicacion (QLocale y el traductor
qtbase, en qt/aqt/__init__.py). Asi esos textos son siempre correctos y no hay
nada inventado.

El TITULO de la ventana es solo el nombre del complemento, tal como lo declara
manifest.json. Es un nombre propio: no se traduce y no lleva ninguna formula
alrededor (ver _addon_title).

La tabla propia de i18n.py se reserva para lo exclusivo del complemento (los
nombres de los temas de color, el record, los mazos excluidos).
"""

from __future__ import annotations

from html import escape

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QColor,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QIcon,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPixmap,
    QPushButton,
    QSpinBox,
    Qt,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.utils import askUser

from .errors import report
from .i18n import record_value_label, t
from .palettes import DEFAULT_THEME, THEME_KEYS, swatch
from .settings import (
    BAR_HEIGHT_MAX,
    BAR_HEIGHT_MIN,
    DEFAULT_CONFIG,
    PUSH_MAX,
    PUSH_MIN,
    Config,
    load_best_streak,
    load_config,
    reset_best_streak,
    save_config,
)


def _log(exc: Exception) -> None:
    report(exc, "options")


def _addon_title() -> str:
    """El nombre del complemento, y nada mas.

    HISTORIAL: llego a componerse como "Configurar 'CoreProgress'" con la
    formula traducida de Anki. El cliente quiere en el titulo solo el nombre.
    Regla: el titulo de la ventana de opciones es el nombre del complemento tal
    como lo declara manifest.json, sin formula alrededor y sin traducir.
    """
    name = "CoreProgress"
    try:
        if mw is not None:
            package = mw.addonManager.addon_from_module(__name__)
            name = mw.addonManager.addon_meta(package).human_name() or name
    except Exception as exc:
        _log(exc)
    return name


def _amp(text: str) -> str:
    """Escape ``&`` so Qt does not read it as a keyboard shortcut.

    HISTORIAL: el texto ingles de la casilla se guardaba ya escapado
    ("Streak && record effects"). Los textos deben guardarse tal como se leen;
    el escape pertenece al punto en que se entregan a Qt, que es aqui.
    """
    return text.replace("&", "&&")


def _no_elide(widget: QWidget) -> None:
    """Reserve the width the full text needs.

    HISTORIAL: con traducciones largas, Qt recortaba el texto de los botones y
    lo remataba con puntos suspensivos ("Seleccionar mazos..."), que parecian
    parte de la traduccion. Fijando el ancho minimo al que pide el propio
    texto, el dialogo crece en lugar de recortar, en los 59 idiomas.
    """
    widget.setMinimumWidth(widget.sizeHint().width())


def _standard_button(
    box: QDialogButtonBox, role: QDialogButtonBox.StandardButton
) -> QPushButton | None:
    """Devuelve un boton estandar SIN tocarle el texto.

    HISTORIAL: aqui se les escribia encima el texto de la tabla propia del
    complemento ("Aceptar", "Cancelar", "Restaurar los valores
    predeterminados"). Qt ya trae esos textos traducidos y Anki fija el idioma
    de la aplicacion al arrancar, asi que pisarlos solo podia empeorarlos.
    Regla: los botones estandar de un dialogo se dejan con su texto de Qt; la
    tabla propia es solo para lo que Anki no tiene.
    """
    button = box.button(role)
    if button is not None:
        _no_elide(button)
    return button


def _color_icon(color_hex: str) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(QColor(color_hex))
    return QIcon(pixmap)


def _record_html(record: int) -> str:
    # HISTORIAL: hubo un malentendido con guiones y signos: el estado "sin
    # record" lleva guion CORTO "-" (neutro en cualquier idioma), y el valor
    # con record lleva "!" al final ("7 seguidas!"), todo en negrita igual que
    # el resto (ahora cada idioma trae su forma en i18n.opt_record_value).
    # El texto se escapa: viaja como HTML dentro de la etiqueta.
    value = "-" if record <= 0 else record_value_label(record)
    return f"{escape(t('opt_record'))}: <b>{escape(value)}</b>"


class ExcludeDecksDialog(QDialog):
    """Sub-window with the deck list; the parent keeps the chosen ids."""

    def __init__(self, parent: QWidget, excluded: set[int]) -> None:
        super().__init__(parent)
        self.setWindowTitle(t("opt_exclude"))
        self.setMinimumWidth(340)

        self._decks = QListWidget()
        self._decks.setMinimumHeight(180)
        try:
            if mw and mw.col:
                for entry in mw.col.decks.all_names_and_ids():
                    deck_id = int(entry.id)
                    item = QListWidgetItem(entry.name)
                    item.setData(Qt.ItemDataRole.UserRole, deck_id)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    state = (
                        Qt.CheckState.Checked if deck_id in excluded else Qt.CheckState.Unchecked
                    )
                    item.setCheckState(state)
                    self._decks.addItem(item)
        except Exception as exc:
            _log(exc)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        qconnect(buttons.accepted, self.accept)
        qconnect(buttons.rejected, self.reject)
        _standard_button(buttons, QDialogButtonBox.StandardButton.Ok)
        _standard_button(buttons, QDialogButtonBox.StandardButton.Cancel)

        # HISTORIAL: aqui hubo una frase explicativa ("Los mazos marcados no
        # cuentan para el record"). El cliente la retiro: la ventana ya se
        # titula "Excluir mazos (record)" y la lista se explica sola.
        # Regla: en esta ventana no se anaden textos de ayuda, en ningun idioma.
        layout = QVBoxLayout()
        layout.addWidget(self._decks)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self.setMinimumWidth(max(360, self.sizeHint().width()))

    def selected_ids(self) -> tuple[int, ...]:
        ids: list[int] = []
        for row in range(self._decks.count()):
            item = self._decks.item(row)
            if item is not None and item.checkState() == Qt.CheckState.Checked:
                deck_id = item.data(Qt.ItemDataRole.UserRole)
                if isinstance(deck_id, int):
                    ids.append(deck_id)
        return tuple(ids)


class OptionsDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(_addon_title())
        self.setMinimumWidth(380)

        cfg = load_config()
        self._excluded: tuple[int, ...] = cfg.excluded_decks

        # El record va primero y en negrita, con su boton de restablecer.
        # HISTORIAL: setFlat(True) se veia "artificial" junto a los botones
        # estandar de Anki; los widgets Qt se dejan con su aspecto por defecto.
        self._record_label = QLabel(_record_html(load_best_streak()))
        self._record_label.setTextFormat(Qt.TextFormat.RichText)
        self._reset_button = QPushButton(_amp(t("opt_record_reset")))
        _no_elide(self._reset_button)
        qconnect(self._reset_button.clicked, self._reset_record)
        record_row = QHBoxLayout()
        record_row.addWidget(self._record_label)
        record_row.addStretch(1)
        record_row.addWidget(self._reset_button)

        self._theme = QComboBox()
        for key in THEME_KEYS:
            self._theme.addItem(_color_icon(swatch(key)), t(f"theme_{key}"), key)

        self._bar_height = QSpinBox()
        self._bar_height.setRange(BAR_HEIGHT_MIN, BAR_HEIGHT_MAX)
        self._bar_height.setSingleStep(1)
        self._bar_height.setSuffix(" px")

        self._push_down = QSpinBox()
        # Mismo rango que valida settings.py: un solo sitio donde cambiarlo.
        self._push_down.setRange(PUSH_MIN, PUSH_MAX)
        self._push_down.setSingleStep(4)
        self._push_down.setSuffix(" px")

        self._effects = QCheckBox(_amp(t("opt_effects")))
        self._checkpoints = QCheckBox(_amp(t("opt_checkpoints")))

        self._exclude_button = QPushButton(_amp(t("opt_exclude_pick")))
        _no_elide(self._exclude_button)
        qconnect(self._exclude_button.clicked, self._pick_decks)

        form = QFormLayout()
        form.addRow(_amp(t("opt_theme")), self._theme)
        form.addRow(_amp(t("opt_bar_height")), self._bar_height)
        form.addRow(_amp(t("opt_push")), self._push_down)
        form.addRow(_amp(t("opt_exclude")), self._exclude_button)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.RestoreDefaults
        )
        qconnect(buttons.accepted, self.accept)
        qconnect(buttons.rejected, self.reject)
        _standard_button(buttons, QDialogButtonBox.StandardButton.Save)
        _standard_button(buttons, QDialogButtonBox.StandardButton.Cancel)
        restore_button = _standard_button(
            buttons, QDialogButtonBox.StandardButton.RestoreDefaults
        )
        if restore_button is not None:
            qconnect(restore_button.clicked, self._restore_defaults)

        layout = QVBoxLayout()
        layout.addLayout(record_row)
        layout.addSpacing(6)
        layout.addLayout(form)
        layout.addWidget(self._effects)
        layout.addWidget(self._checkpoints)
        layout.addSpacing(4)
        layout.addWidget(buttons)
        self.setLayout(layout)
        self._apply_visual(cfg)
        # Que la ventana se ajuste al idioma mas largo en vez de recortar texto.
        self.setMinimumWidth(max(400, self.sizeHint().width()))

    def _reset_record(self) -> None:
        try:
            if not askUser(t("opt_record_reset_confirm"), parent=self):
                return
            reset_best_streak()
            self._record_label.setText(_record_html(0))
            from .controller import notify_record_reset

            notify_record_reset()
        except Exception as exc:
            _log(exc)

    def _pick_decks(self) -> None:
        try:
            dialog = ExcludeDecksDialog(self, set(self._excluded))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._excluded = dialog.selected_ids()
        except Exception as exc:
            _log(exc)

    def _apply_visual(self, cfg: Config) -> None:
        self._theme.setCurrentIndex(max(self._theme.findData(cfg.theme), 0))
        self._bar_height.setValue(cfg.bar_height)
        self._push_down.setValue(cfg.push_down)
        self._effects.setChecked(cfg.effects_enabled)
        self._checkpoints.setChecked(cfg.checkpoints_enabled)

    def _restore_defaults(self) -> None:
        # Visual settings only; the record and the excluded decks stay as they are.
        self._apply_visual(DEFAULT_CONFIG)

    def selected_config(self) -> Config:
        theme_data = self._theme.currentData()
        theme = theme_data if isinstance(theme_data, str) and theme_data in THEME_KEYS else DEFAULT_THEME
        return Config(
            theme=theme,
            effects_enabled=self._effects.isChecked(),
            checkpoints_enabled=self._checkpoints.isChecked(),
            bar_height=self._bar_height.value(),
            push_down=self._push_down.value(),
            excluded_decks=self._excluded,
        )


def open_options() -> None:
    try:
        from .controller import notify_config_changed

        dialog = OptionsDialog(mw)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            save_config(dialog.selected_config())
            notify_config_changed()
    except Exception as exc:
        _log(exc)


def setup_menu() -> None:
    try:
        if mw is not None:
            mw.addonManager.setConfigAction(__name__, open_options)
    except Exception as exc:
        _log(exc)