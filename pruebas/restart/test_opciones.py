"""Pruebas del panel de opciones (2.1.0): la descripción que recibe la página y
la lectura de lo elegido, sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from aqt.qt import QKeySequence

from restart import constants, shortcuts, ui
from restart.settings import AddonSettings

ADDON = Path(ui.__file__).parent


class PanelPageTests(unittest.TestCase):
    def test_shortcut_depends_on_checkbox(self) -> None:
        page = ui.page(AddonSettings())
        check = page["cards"][0]["items"][0]
        self.assertEqual(check["key"], "restart_enabled")
        self.assertEqual(check["children"][0]["key"], "restart_shortcut")
        self.assertEqual(page["values"], page["defaults"])
        self.assertEqual(page["values"]["restart_shortcut"], constants.DEFAULT_SHORTCUT_RESTART)
        json.dumps(page)

    def test_label_has_no_trailing_colon(self) -> None:
        field = ui.page(AddonSettings())["cards"][0]["items"][0]["children"][0]
        self.assertFalse(field["label"].endswith(":"))


class SettingsFromPageTests(unittest.TestCase):
    def test_empty_field_keeps_saved_shortcut(self) -> None:
        saved = AddonSettings(restart_enabled=True, restart_shortcut="Ctrl+Alt+R")
        result = ui.settings_from_page({"restart_enabled": True, "restart_shortcut": ""}, saved)
        self.assertEqual(result.restart_shortcut, "Ctrl+Alt+R")

    def test_new_shortcut_and_checkbox(self) -> None:
        result = ui.settings_from_page({"restart_enabled": False, "restart_shortcut": "Ctrl+Shift+R"}, AddonSettings())
        self.assertFalse(result.restart_enabled)
        self.assertEqual(result.restart_shortcut, "Ctrl+Shift+R")

    def test_bad_values_keep_saved(self) -> None:
        saved = AddonSettings()
        result = ui.settings_from_page({"restart_enabled": "yes", "restart_shortcut": 5}, saved)
        self.assertEqual(result, saved)
        self.assertEqual(ui.settings_from_page(None, saved), saved)

    def test_page_shortcut_text_is_understood_by_qt(self) -> None:
        # Lo que escribe la página para Ctrl+Mayús+R lo entiende Qt igual.
        sequence = QKeySequence("Ctrl+Shift+R")
        self.assertEqual(shortcuts.portable_text(sequence), "Ctrl+Shift+R")
        self.assertTrue(shortcuts.is_well_formed(sequence))


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("var RestartPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
