"""Pruebas del panel de opciones (1.3) y de la lista de atajos ocupados, sin
Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que anade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from always_on_top import constants, dialogs, shortcuts

ADDON = Path(dialogs.__file__).parent


class PanelPageTests(unittest.TestCase):
    def test_page_has_shortcut_field(self) -> None:
        page = dialogs.page("Ctrl+Alt+K")
        item = page["cards"][0]["items"][0]
        self.assertEqual(item["type"], "shortcut")
        self.assertEqual(page["values"]["shortcut"], "Ctrl+Alt+K")
        self.assertEqual(page["defaults"]["shortcut"], constants.DEFAULT_SHORTCUT)
        self.assertFalse(item["label"].endswith(":"))
        json.dumps(page)


class ChosenShortcutTests(unittest.TestCase):
    def test_empty_means_default(self) -> None:
        self.assertEqual(dialogs.chosen_shortcut({"shortcut": ""}), constants.DEFAULT_SHORTCUT)
        self.assertEqual(dialogs.chosen_shortcut(None), constants.DEFAULT_SHORTCUT)
        self.assertEqual(dialogs.chosen_shortcut({"shortcut": 3}), constants.DEFAULT_SHORTCUT)

    def test_page_text_is_normalized(self) -> None:
        self.assertEqual(dialogs.chosen_shortcut({"shortcut": "Ctrl+Alt+K"}), "Ctrl+Alt+K")


class ReservedShortcutTests(unittest.TestCase):
    # FIX-002: los seis atajos del editor de Anki 26.09.3 que faltaban.
    def test_editor_list_and_indent_keys_are_taken(self) -> None:
        for text in ("Ctrl+.", "Ctrl+,", "Ctrl+Shift+.", "Ctrl+Shift+,", "Ctrl+=", "Ctrl+Shift+="):
            self.assertTrue(shortcuts.used_by_anki(text), text)

    def test_default_is_free(self) -> None:
        self.assertFalse(shortcuts.used_by_anki(constants.DEFAULT_SHORTCUT))


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("var AlwaysOnTopPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
