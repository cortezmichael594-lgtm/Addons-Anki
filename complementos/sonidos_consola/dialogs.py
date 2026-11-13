"""Ventana de opciones, solo con controles estándar de Qt.

Toman solos el aspecto y los colores del tema activo (también Nocturne): no se fija ningún
color. Cada control tiene su etiqueta asociada, nombre accesible y atajo con Alt, para que
se maneje entero con el teclado y lo lea un lector de pantalla.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aqt import mw
from aqt.qt import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
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

from . import logic, strings

_GEOMETRY_KEY = "sonidos_consola_options"


def _can_remember_geometry() -> bool:
    return mw is not None and mw.pm.profile is not None


class OptionsDialog(QDialog):
    def __init__(
        self,
        parent: QWidget | None,
        values: dict[str, Any],
        present: set[str],
        audio_ok: bool,
        on_test: Callable[[str, int], None],
        on_open_folder: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        disable_help_button(self)
        self.setWindowTitle(strings.OPTIONS_TITLE)
        self._on_test = on_test

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        # Volumen: barra estándar de 0 a 100, con la cifra al lado.
        self.volume = QSlider(Qt.Orientation.Horizontal, self)
        self.volume.setRange(0, 100)
        self.volume.setSingleStep(5)
        self.volume.setPageStep(10)
        self.volume.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume.setTickInterval(10)
        self.volume.setValue(int(values["volume"]))
        self.volume.setAccessibleName(strings.VOLUME_ACCESSIBLE)
        self.volume.setToolTip(strings.VOLUME_TIP)
        self.volume_value = QLabel(self)
        self.volume_value.setMinimumWidth(self.volume_value.fontMetrics().horizontalAdvance("100 %") + 4)
        self._show_volume(self.volume.value())
        qconnect(self.volume.valueChanged, self._show_volume)
        qconnect(self.volume.sliderReleased, self._preview_volume)
        qconnect(self.volume.valueChanged, self._preview_if_keyboard)
        volume_row = QHBoxLayout()
        volume_row.addWidget(self.volume, 1)
        volume_row.addWidget(self.volume_value)
        volume_label = QLabel(strings.VOLUME_LABEL, self)
        volume_label.setBuddy(self.volume)
        form.addRow(volume_label, volume_row)

        # Cuándo suena la navegación.
        self.navigation = QComboBox(self)
        for mode in logic.NAV_MODES:
            self.navigation.addItem(strings.NAVIGATION_CHOICES[mode], mode)
        self.navigation.setCurrentIndex(max(0, self.navigation.findData(values["navigation"])))
        navigation_label = QLabel(strings.NAVIGATION_LABEL, self)
        navigation_label.setBuddy(self.navigation)
        form.addRow(navigation_label, self.navigation)

        # Una fila por sonido: casilla, archivo (o «Falta ...») y botón «Probar».
        group = QGroupBox(strings.SOUNDS_GROUP, self)
        grid = QGridLayout(group)
        self.switches: dict[str, QCheckBox] = {}
        self.test_buttons: dict[str, QPushButton] = {}
        for row, (key, file_name) in enumerate(logic.SOUND_FILES.items()):
            label = strings.SOUND_LABELS[key]
            switch = QCheckBox(label, group)
            switch.setChecked(bool(values["enabled"].get(key, True)))
            exists = file_name in present
            status = QLabel(
                strings.FILE_READY.format(file=file_name)
                if exists
                else strings.FILE_MISSING.format(file=file_name),
                group,
            )
            status.setEnabled(exists)  # Atenuado si falta: el texto «Falta» lo dice también.
            test = QPushButton(strings.TEST_BUTTON, group)
            test.setAutoDefault(False)
            test.setEnabled(exists and audio_ok)
            test.setAccessibleName(strings.TEST_ACCESSIBLE.format(label=label))
            qconnect(test.clicked, lambda _checked=False, k=key: self._on_test(k, self.volume.value()))
            grid.addWidget(switch, row, 0)
            grid.addWidget(status, row, 1)
            grid.addWidget(test, row, 2)
            self.switches[key] = switch
            self.test_buttons[key] = test
        grid.setColumnStretch(1, 1)
        layout.addWidget(group)

        # Carpeta de sonidos y resumen de lo que falta.
        missing = logic.missing_files(present)
        summary = strings.missing_summary(len(missing)) if audio_ok else strings.NO_AUDIO
        self.summary = QLabel(summary, self)
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.open_folder = QPushButton(strings.OPEN_FOLDER, self)
        self.open_folder.setAutoDefault(False)
        self.open_folder.setToolTip(strings.OPEN_FOLDER_TIP)
        qconnect(self.open_folder.clicked, lambda _checked=False: on_open_folder())
        folder_row = QHBoxLayout()
        folder_row.addWidget(self.open_folder)
        folder_row.addStretch(1)
        layout.addLayout(folder_row)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        qconnect(buttons.accepted, self.accept)
        qconnect(buttons.rejected, self.reject)
        layout.addWidget(buttons)

        if _can_remember_geometry():
            restoreGeom(self, _GEOMETRY_KEY)

    def _show_volume(self, value: int) -> None:
        self.volume_value.setText(f"{value} %")

    def _preview_if_keyboard(self, _value: int) -> None:
        # Con el teclado (flechas, RePág, Inicio, Fin) se oye cada paso; arrastrando con el
        # ratón, solo al soltar, para no encadenar decenas de tics.
        if not self.volume.isSliderDown():
            self._preview_volume()

    def _preview_volume(self) -> None:
        self._on_test("option", self.volume.value())

    def done(self, a0: int) -> None:
        if _can_remember_geometry():
            saveGeom(self, _GEOMETRY_KEY)
        super().done(a0)

    def values(self) -> dict[str, Any]:
        return {
            "volume": self.volume.value(),
            "navigation": self.navigation.currentData(),
            "enabled": {key: switch.isChecked() for key, switch in self.switches.items()},
        }
