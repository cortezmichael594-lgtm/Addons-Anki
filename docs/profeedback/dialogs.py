"""Ventana de ajustes de ProFeedback.

Se construye solo con controles estándar de Qt (casillas, desplegables, deslizador, botones
Aceptar y Cancelar). Así toma sola el aspecto y los colores del tema activo, también los de
Nocturne, y no hay que fijar ningún color a mano.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-10-13): al guardar, «sonido al azar» se convertía en el primer sonido de la lista.

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    Qt,
    QVBoxLayout,
    QWidget,
    qconnect,
)
from aqt.utils import disable_help_button, restoreGeom, saveGeom

from . import strings
from .config import VOLUME_MAX, VOLUME_MIN, AddonConfig
from .paths import SoundKind

WINDOW_TITLE = "ProFeedback"
_GEOMETRY_KEY = "profeedback_settings"
_INITIAL_WIDTH = 560

# Filas de «al terminar de repasar»: tipo de sonido y texto de su etiqueta.
_FINISH_ROWS: tuple[tuple[SoundKind, strings.UIKey], ...] = (
    ("deck_finish", "label_deck_finish"),
    ("all_finish", "label_all_done"),
    ("deck_perfect", "label_deck_perfect"),
    ("all_perfect", "label_all_perfect"),
)

TestCallback = Callable[[SoundKind, str, int], None]


def _can_remember_geometry() -> bool:
    # Fuera de Anki (pruebas) no hay perfil abierto; dentro de Anki siempre lo hay.
    return mw is not None and mw.pm.profile is not None


class SettingsDialog(QDialog):
    """Todo se cambia con casillas, desplegables y un deslizador; nada de editar JSON."""

    def __init__(
        self,
        parent: QWidget | None,
        config: AddonConfig,
        sounds: Mapping[SoundKind, Sequence[str]],
        on_test: TestCallback,
    ) -> None:
        super().__init__(parent)
        disable_help_button(self)
        self._sounds = sounds
        self._on_test = on_test
        self._combos: dict[SoundKind, QComboBox] = {}
        self._test_buttons: dict[SoundKind, QPushButton] = {}
        self._build_ui()
        self._load_values(config)
        self._sync_enabled()
        self._set_initial_size()
        if _can_remember_geometry():
            restoreGeom(self, _GEOMETRY_KEY)

    # ── construcción ─────────────────────────────────────────────────────────
    def _sound_row(self, kind: SoundKind) -> QHBoxLayout:
        """Desplegable de un tipo de sonido con su botón «Probar»."""
        row = QHBoxLayout()
        combo = QComboBox(self)
        # --- FIX-001 (2026-10-13) ---
        # Síntoma: al guardar los ajustes, «sonido al azar» (valor vacío) se convertía en el
        #   primer sonido de la lista y ya no volvía a ser al azar.
        # Causa: el desplegable no tenía entrada para «al azar»; al no encontrar el valor
        #   vacío mostraba el primer archivo, y ese era el que se guardaba.
        # Regla: todo desplegable de sonido lleva como primera entrada «Aleatorio» (valor
        #   vacío), y un valor guardado que ya no existe se muestra como esa entrada.
        combo.addItem(strings.ui("sound_random"), "")
        for name in self._sounds.get(kind, ()):
            combo.addItem(name, name)
        row.addWidget(combo, stretch=1)
        button = QPushButton(strings.ui("test"), self)
        qconnect(button.clicked, lambda _checked=False, k=kind: self._test(k))
        row.addWidget(button)
        self._combos[kind] = combo
        self._test_buttons[kind] = button
        return row

    def _build_ui(self) -> None:
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumWidth(520)
        root = QVBoxLayout(self)

        # Volumen de todos los sonidos.
        volume_row = QHBoxLayout()
        self.volume = QSlider(Qt.Orientation.Horizontal, self)
        self.volume.setRange(VOLUME_MIN, VOLUME_MAX)
        self.volume.setPageStep(10)
        self.volume_value = QLabel(self)
        self.volume_value.setMinimumWidth(48)
        self.volume_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        qconnect(self.volume.valueChanged, self._show_volume)
        volume_row.addWidget(self.volume, stretch=1)
        volume_row.addWidget(self.volume_value)
        volume_form = QFormLayout()
        volume_form.addRow(strings.ui("label_volume"), volume_row)
        root.addLayout(volume_form)

        # Sonido al responder bien.
        answer_group = QGroupBox(strings.ui("group_answer_sounds"), self)
        answer_layout = QVBoxLayout(answer_group)
        self.answer_enabled = QCheckBox(strings.ui("enable_answer_sound"), self)
        qconnect(self.answer_enabled.toggled, self._sync_enabled)
        answer_layout.addWidget(self.answer_enabled)
        if not self._sounds.get("correct"):
            answer_layout.addWidget(self._note(strings.ui("no_answer_sounds")))
        answer_form = QFormLayout()
        answer_form.addRow(strings.ui("label_sound"), self._sound_row("correct"))
        answer_layout.addLayout(answer_form)
        root.addWidget(answer_group)

        # Sonidos al terminar de repasar.
        finish_group = QGroupBox(strings.ui("group_finish_sounds"), self)
        finish_layout = QVBoxLayout(finish_group)
        self.finish_enabled = QCheckBox(strings.ui("enable_finish_sound"), self)
        qconnect(self.finish_enabled.toggled, self._sync_enabled)
        finish_layout.addWidget(self.finish_enabled)
        if not any(self._sounds.get(kind) for kind, _ in _FINISH_ROWS):
            finish_layout.addWidget(self._note(strings.ui("no_finish_sounds")))
        finish_form = QFormLayout()
        for kind, label_key in _FINISH_ROWS:
            finish_form.addRow(strings.ui(label_key), self._sound_row(kind))
        finish_layout.addLayout(finish_form)
        root.addWidget(finish_group)

        # Aspecto.
        appearance_group = QGroupBox(strings.ui("group_appearance"), self)
        appearance_layout = QVBoxLayout(appearance_group)
        self.confetti = QCheckBox(strings.ui("confetti_option"), self)
        self.styled_buttons = QCheckBox(strings.ui("styled_buttons"), self)
        self.flags = QCheckBox(strings.ui("flags_option"), self)
        for box in (self.confetti, self.styled_buttons, self.flags):
            appearance_layout.addWidget(box)
        root.addWidget(appearance_group)

        root.addWidget(self._note(strings.ui("hint_own_sounds")))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        qconnect(buttons.accepted, self.accept)
        qconnect(buttons.rejected, self.reject)
        root.addWidget(buttons)

    def _set_initial_size(self) -> None:
        """Ancho cómodo y alto justo, aunque las notas largas se partan en varias líneas.

        Sin esto, la ventana abriría tan ancha como la nota más larga en una sola línea.
        """
        width = _INITIAL_WIDTH
        layout = self.layout()
        if layout is not None and layout.hasHeightForWidth():
            height = layout.totalHeightForWidth(width)
        else:
            height = self.sizeHint().height()
        self.resize(width, max(height, self.minimumSizeHint().height()))

    def _note(self, text: str) -> QLabel:
        label = QLabel(text, self)
        label.setWordWrap(True)
        # Texto secundario, con el matiz que el tema le da a «deshabilitado»: sin colores
        # propios, solo el estado nativo del control.
        label.setEnabled(False)
        return label

    # ── valores ──────────────────────────────────────────────────────────────
    @staticmethod
    def _select(combo: QComboBox, value: str) -> None:
        """Elige el valor guardado; si ya no existe, queda «Aleatorio» (la primera entrada)."""
        index = combo.findData(value)
        combo.setCurrentIndex(index if index >= 0 else 0)

    @staticmethod
    def _current(combo: QComboBox) -> str:
        value = combo.currentData()
        return value if isinstance(value, str) else ""

    def _load_values(self, config: AddonConfig) -> None:
        self.answer_enabled.setChecked(config.answerSoundEnabled)
        self.finish_enabled.setChecked(config.sessionSoundsEnabled)
        self.confetti.setChecked(config.confettiEnabled)
        self.styled_buttons.setChecked(config.styledButtonsEnabled)
        self.flags.setChecked(config.flagsEnabled)
        self.volume.setValue(config.soundVolume)
        self._show_volume(config.soundVolume)
        chosen: dict[SoundKind, str] = {
            "correct": config.answerSound,
            "deck_finish": config.deckFinishSound,
            "all_finish": config.allDoneSound,
            "deck_perfect": config.deckPerfectSound,
            "all_perfect": config.allPerfectSound,
        }
        for kind, combo in self._combos.items():
            self._select(combo, chosen[kind])

    def _show_volume(self, value: int) -> None:
        self.volume_value.setText(f"{value} %")

    def _sync_enabled(self) -> None:
        """Un desplegable sin sonidos que ofrecer, o con su opción apagada, se ve apagado."""
        for kind, combo in self._combos.items():
            group_on = (
                self.answer_enabled.isChecked()
                if kind == "correct"
                else self.finish_enabled.isChecked()
            )
            enabled = group_on and bool(self._sounds.get(kind))
            combo.setEnabled(enabled)
            self._test_buttons[kind].setEnabled(enabled)

    def _test(self, kind: SoundKind) -> None:
        self._on_test(kind, self._current(self._combos[kind]), self.volume.value())

    def values(self) -> AddonConfig:
        """Los ajustes tal como están ahora en la ventana."""
        return AddonConfig(
            answerSoundEnabled=self.answer_enabled.isChecked(),
            sessionSoundsEnabled=self.finish_enabled.isChecked(),
            confettiEnabled=self.confetti.isChecked(),
            styledButtonsEnabled=self.styled_buttons.isChecked(),
            flagsEnabled=self.flags.isChecked(),
            answerSound=self._current(self._combos["correct"]),
            deckFinishSound=self._current(self._combos["deck_finish"]),
            allDoneSound=self._current(self._combos["all_finish"]),
            deckPerfectSound=self._current(self._combos["deck_perfect"]),
            allPerfectSound=self._current(self._combos["all_perfect"]),
            soundVolume=self.volume.value(),
        )

    def done(self, a0: int) -> None:
        if _can_remember_geometry():
            saveGeom(self, _GEOMETRY_KEY)
        super().done(a0)
