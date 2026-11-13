"""Pruebas de la ventana y del vigilante de la interfaz, con Qt sin pantalla («offscreen»).

El reproductor se sustituye por uno que solo anota qué sonidos se pidieron: aquí se prueba
cuándo suena cada cosa, no el audio.
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest

from aqt.qt import (
    QAction,
    QApplication,
    QDialog,
    QEvent,
    QKeyEvent,
    QMenu,
    QMessageBox,
    QPushButton,
    Qt,
)

from sonidos_consola import dialogs, logic, player, strings, watcher


class _Recorder:
    def __init__(self) -> None:
        self.played: list[str] = []

    def play(self, key: str, **_kwargs: object) -> None:
        self.played.append(key)


class _QtTest(unittest.TestCase):
    app: QApplication

    @classmethod
    def setUpClass(cls) -> None:
        existing = QApplication.instance()
        cls.app = existing if isinstance(existing, QApplication) else QApplication([])

    def setUp(self) -> None:
        self.recorder = _Recorder()
        self._original_bank = watcher.bank
        watcher.bank = self.recorder  # type: ignore[assignment]
        self.watcher = watcher.InterfaceWatcher()
        self.app.installEventFilter(self.watcher)

    def tearDown(self) -> None:
        self.app.removeEventFilter(self.watcher)
        watcher.bank = self._original_bank


class MenuTest(_QtTest):
    def _menu(self) -> tuple[QMenu, QAction, QAction]:
        menu = QMenu()
        first = menu.addAction("Uno")
        menu.addSeparator()
        second = menu.addAction("Dos")
        menu.show()
        assert first is not None and second is not None
        return menu, first, second

    def test_hover_between_options_ticks_once_per_change(self) -> None:
        menu, first, second = self._menu()
        menu.hovered.emit(first)
        menu.hovered.emit(first)  # mismo elemento: no repite
        menu.hovered.emit(second)
        self.assertEqual(self.recorder.played, ["option", "option"])
        menu.close()

    def test_separator_is_silent(self) -> None:
        menu, _first, _second = self._menu()
        separator = next(a for a in menu.actions() if a.isSeparator())
        menu.hovered.emit(separator)
        self.assertEqual(self.recorder.played, [])
        menu.close()

    def test_escape_in_menu_cancels(self) -> None:
        menu, _first, _second = self._menu()
        QApplication.sendEvent(menu, QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier))
        self.assertIn("cancel", self.recorder.played)


class WindowTest(_QtTest):
    def test_warning_box_plays_error_and_marks_sync(self) -> None:
        watcher.on_sync_will_start()
        box = QMessageBox(QMessageBox.Icon.Warning, "Anki", "Fallo")
        box.show()
        self.assertEqual(self.recorder.played, ["error"])
        self.assertTrue(watcher._sync_tracker.error_seen)
        box.close()

    def test_info_box_is_silent_on_show(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Information, "Anki", "Hola")
        box.show()
        self.assertEqual(self.recorder.played, [])
        box.close()

    def test_dialog_cancelled_by_person_plays_cancel(self) -> None:
        dialog = QDialog()
        dialog.show()
        QApplication.sendEvent(
            dialog, QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier)
        )
        self.assertIn("cancel", self.recorder.played)

    def test_dialog_closed_by_anki_is_silent(self) -> None:
        dialog = QDialog()
        dialog.show()
        dialog.reject()  # como una ventana de progreso que Anki cierra sola
        self.assertEqual(self.recorder.played, [])

    def test_dialog_accepted_is_silent(self) -> None:
        dialog = QDialog()
        dialog.show()
        QApplication.sendEvent(
            dialog, QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Return, Qt.KeyboardModifier.NoModifier)
        )
        dialog.accept()
        self.assertEqual(self.recorder.played, [])


class SyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.recorder = _Recorder()
        self._original_bank = watcher.bank
        watcher.bank = self.recorder  # type: ignore[assignment]

    def tearDown(self) -> None:
        watcher.bank = self._original_bank

    def test_sync_without_error_plays_ok(self) -> None:
        watcher.on_sync_will_start()
        watcher.on_sync_did_finish()
        self.assertEqual(self.recorder.played, ["system_ok"])

    def test_sync_with_error_does_not_play_ok(self) -> None:
        watcher.on_sync_will_start()
        watcher._sync_tracker.error_seen = True
        watcher.on_sync_did_finish()
        self.assertEqual(self.recorder.played, [])


class OptionsDialogTest(unittest.TestCase):
    app: QApplication

    @classmethod
    def setUpClass(cls) -> None:
        existing = QApplication.instance()
        cls.app = existing if isinstance(existing, QApplication) else QApplication([])

    def _dialog(self, present: set[str] | None = None) -> tuple[dialogs.OptionsDialog, list[tuple[str, int]]]:
        tests: list[tuple[str, int]] = []
        values = logic.normalize_config({"volume": 40, "navigation": "click", "enabled": {"error": False}})
        dialog = dialogs.OptionsDialog(
            None,
            values,
            present if present is not None else set(logic.SOUND_FILES.values()),
            True,
            on_test=lambda key, volume: tests.append((key, volume)),
            on_open_folder=lambda: None,
        )
        return dialog, tests

    def test_values_round_trip(self) -> None:
        dialog, _tests = self._dialog()
        self.assertEqual(
            dialog.values(),
            logic.normalize_config({"volume": 40, "navigation": "click", "enabled": {"error": False}}),
        )

    def test_controls_change_values(self) -> None:
        dialog, _tests = self._dialog()
        dialog.volume.setValue(85)
        dialog.navigation.setCurrentIndex(dialog.navigation.findData("off"))
        dialog.switches["coldboot"].setChecked(False)
        values = dialog.values()
        self.assertEqual(values["volume"], 85)
        self.assertEqual(values["navigation"], "off")
        self.assertFalse(values["enabled"]["coldboot"])

    def test_keyboard_volume_change_previews_with_new_volume(self) -> None:
        dialog, tests = self._dialog()
        dialog.volume.setValue(55)
        self.assertEqual(tests[-1], ("option", 55))
        self.assertEqual(dialog.volume_value.text(), "55 %")

    def test_test_button_uses_slider_volume(self) -> None:
        dialog, tests = self._dialog()
        dialog.test_buttons["cancel"].click()
        self.assertEqual(tests[-1], ("cancel", 40))

    def test_missing_file_disables_test_and_says_so(self) -> None:
        present = set(logic.SOUND_FILES.values()) - {"snd_error.wav"}
        dialog, _tests = self._dialog(present)
        self.assertFalse(dialog.test_buttons["error"].isEnabled())
        self.assertTrue(dialog.test_buttons["cancel"].isEnabled())
        self.assertEqual(dialog.summary.text(), strings.missing_summary(1))

    def test_every_test_button_has_accessible_name(self) -> None:
        dialog, _tests = self._dialog()
        for key, button in dialog.test_buttons.items():
            self.assertIsInstance(button, QPushButton)
            self.assertIn(strings.SOUND_LABELS[key], button.accessibleName())


class SummaryTextTest(unittest.TestCase):
    def test_singular_and_plural(self) -> None:
        self.assertEqual(strings.missing_summary(0), "Están los siete sonidos.")
        self.assertIn("Falta 1 sonido", strings.missing_summary(1))
        self.assertIn("Faltan 3 sonidos", strings.missing_summary(3))


class PlayerFilesTest(unittest.TestCase):
    def test_present_files_reads_the_sounds_folder(self) -> None:
        import tempfile
        from pathlib import Path

        original = player.SOUNDS_DIR
        with tempfile.TemporaryDirectory() as folder:
            player.SOUNDS_DIR = Path(folder)
            try:
                (Path(folder) / "snd_option.wav").write_bytes(b"")
                self.assertEqual(player.present_files(), {"snd_option.wav"})
            finally:
                player.SOUNDS_DIR = original


if __name__ == "__main__":
    unittest.main()
