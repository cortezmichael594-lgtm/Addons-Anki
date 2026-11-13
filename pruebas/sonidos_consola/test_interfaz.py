"""Pruebas de la ventana y del vigilante de la interfaz, con Qt sin pantalla («offscreen»).

El reproductor se sustituye por uno que solo anota qué sonidos se pidieron: aquí se prueba
cuándo suena cada cosa, no el audio.
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest
from pathlib import Path

from aqt.qt import (
    QAction,
    QApplication,
    QDialog,
    QEvent,
    QKeyEvent,
    QMenu,
    QMessageBox,
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
    def test_warning_box_plays_error(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Warning, "Anki", "Fallo")
        box.show()
        self.assertEqual(self.recorder.played, ["error"])
        box.close()

    def _press(self, box: QMessageBox, button: QMessageBox.StandardButton) -> None:
        widget = box.button(button)
        assert widget is not None
        QApplication.sendEvent(box, QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier))
        widget.click()

    def test_yes_in_a_question_plays_ok(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Question, "Anki", "¿Seguro?")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.show()
        self._press(box, QMessageBox.StandardButton.Yes)
        self.assertEqual(self.recorder.played, ["system_ok"])

    def test_no_in_a_question_plays_cancel(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Question, "Anki", "¿Seguro?")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.show()
        self._press(box, QMessageBox.StandardButton.No)
        self.assertEqual(self.recorder.played, ["cancel"])

    def test_ok_on_information_plays_ok(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Information, "Anki", "Hecho")
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.show()
        self._press(box, QMessageBox.StandardButton.Ok)
        self.assertEqual(self.recorder.played, ["system_ok"])

    def test_ok_on_a_warning_only_plays_error(self) -> None:
        box = QMessageBox(QMessageBox.Icon.Warning, "Anki", "Fallo")
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.show()
        self._press(box, QMessageBox.StandardButton.Ok)
        self.assertEqual(self.recorder.played, ["error"])

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

    def test_dialog_accepted_by_person_plays_ok(self) -> None:
        dialog = QDialog()
        dialog.show()
        QApplication.sendEvent(
            dialog, QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Return, Qt.KeyboardModifier.NoModifier)
        )
        dialog.accept()
        self.assertEqual(self.recorder.played, ["system_ok"])

    def test_dialog_accepted_by_anki_is_silent(self) -> None:
        dialog = QDialog()
        dialog.show()
        dialog.accept()
        self.assertEqual(self.recorder.played, [])


def _all_items(items: list[dict]) -> list[dict]:
    found: list[dict] = []
    for item in items:
        found.append(item)
        found.extend(_all_items(item.get("children", [])))
    return found


ALL_FILES = set(logic.SOUND_FILES.values())


class PanelPageTest(unittest.TestCase):
    """Regla de FIX-001: las opciones son una página del panel modelo."""

    def _items(self, page: dict) -> list[dict]:
        return _all_items([item for card in page["cards"] for item in card["items"]])

    def test_every_control_has_value_and_default(self) -> None:
        page = dialogs.page(logic.default_config(), ALL_FILES, True)
        for item in self._items(page):
            if item.get("key"):
                self.assertIn(item["key"], page["values"])
                self.assertIn(item["key"], page["defaults"])

    def test_seven_switches_and_navigation_hangs_from_its_switch(self) -> None:
        page = dialogs.page(logic.default_config(), ALL_FILES, True)
        checks = [i for i in self._items(page) if i["type"] == "check"]
        self.assertEqual([c["key"] for c in checks], [dialogs.switch_key(k) for k in logic.SOUND_KEYS])
        option = next(c for c in checks if c["key"] == dialogs.switch_key("option"))
        self.assertEqual(option["children"][0]["key"], dialogs.NAVIGATION_KEY)

    def test_round_trip(self) -> None:
        config = logic.normalize_config({"volume": 40, "navigation": "click", "enabled": {"error": False}})
        page = dialogs.page(config, ALL_FILES, True)
        self.assertEqual(dialogs.config_from_page(page["values"]), config)

    def test_bad_values_fall_back(self) -> None:
        values = {"volume": "alto", "navigation": "x", dialogs.switch_key("cancel"): "no"}
        self.assertEqual(dialogs.config_from_page(values), logic.default_config())
        self.assertEqual(dialogs.config_from_page(None), logic.default_config())

    def test_missing_file_is_named_and_left_out_of_test_list(self) -> None:
        present = ALL_FILES - {"snd_error.wav"}
        page = dialogs.page(logic.default_config(), present, True)
        items = self._items(page)
        error_check = next(i for i in items if i.get("key") == dialogs.switch_key("error"))
        self.assertEqual(error_check["note"], strings.FILE_MISSING.format(file="snd_error.wav"))
        test = next(i for i in items if i.get("key") == dialogs.TEST_KEY)
        self.assertNotIn("error", [o["value"] for o in test["options"]])
        self.assertFalse(test["unavailable"])
        self.assertEqual(page["cards"][2]["note"], strings.missing_summary(1))

    def test_without_sounds_the_test_list_is_off(self) -> None:
        page = dialogs.page(logic.default_config(), set(), True)
        test = next(i for i in self._items(page) if i.get("key") == dialogs.TEST_KEY)
        self.assertTrue(test["unavailable"])
        self.assertEqual(page["values"][dialogs.TEST_KEY], "")

    def test_without_audio_there_is_a_notice(self) -> None:
        page = dialogs.page(logic.default_config(), ALL_FILES, False)
        self.assertIn(strings.NO_AUDIO, [i.get("text") for i in self._items(page)])

    def test_test_request_uses_panel_volume(self) -> None:
        values = {dialogs.TEST_KEY: "cancel", dialogs.VOLUME_KEY: 35}
        self.assertEqual(dialogs.test_request({"name": "test", "values": values}), ("cancel", 35))
        self.assertIsNone(dialogs.test_request({"name": "folder", "values": values}))
        self.assertIsNone(dialogs.test_request({"name": "test", "values": {dialogs.TEST_KEY: "otro"}}))

    def test_kit_carries_the_package_prefix(self) -> None:
        addon = Path(dialogs.__file__).parent
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (addon / name).read_text(encoding="utf-8")
            self.assertNotIn("restart", text.lower())
        self.assertIn("var SonidosConsolaPanel", (addon / "web/panel.js").read_text(encoding="utf-8"))


class SummaryTextTest(unittest.TestCase):
    def test_singular_and_plural(self) -> None:
        self.assertEqual(strings.missing_summary(0), "Están los siete sonidos.")
        self.assertIn("Falta 1 sonido", strings.missing_summary(1))
        self.assertIn("Faltan 3 sonidos", strings.missing_summary(3))


class PlayerFilesTest(unittest.TestCase):
    def test_present_files_reads_the_sounds_folder(self) -> None:
        import tempfile

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
