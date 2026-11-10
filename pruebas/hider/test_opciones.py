"""Pruebas del panel de opciones (4.1.0): la descripcion que recibe la pagina y
la lectura de lo elegido, sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que anade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import unittest
from dataclasses import asdict
from pathlib import Path

from hider import constants, dialogs
from hider.config import DEFAULT_CONFIG

ADDON = Path(dialogs.__file__).parent


def _keys(items: list[dict]) -> list[str]:
    found: list[str] = []
    for item in items:
        if "key" in item:
            found.append(item["key"])
        found.extend(_keys(item.get("children", [])))
    return found


class PanelPageTests(unittest.TestCase):
    def test_every_control_has_value_and_default(self) -> None:
        page = dialogs.page(DEFAULT_CONFIG)
        keys = [key for card in page["cards"] for key in _keys(card["items"])]
        self.assertEqual(sorted(keys), sorted(page["values"]))
        self.assertEqual(page["values"], page["defaults"])
        json.dumps(page)

    def test_group_titles_have_no_trailing_colon(self) -> None:
        for card in dialogs.page(DEFAULT_CONFIG)["cards"]:
            self.assertFalse(card["title"].endswith(":"))

    def test_seconds_depend_on_cursor_box(self) -> None:
        review = dialogs.page(DEFAULT_CONFIG)["cards"][0]
        cursor = next(item for item in review["items"] if item["key"] == "hide_cursor")
        child = cursor["children"][0]
        self.assertEqual(child["key"], "cursor_idle_seconds")
        self.assertEqual(child["min"], constants.MIN_CURSOR_IDLE_SECONDS)
        self.assertEqual(child["max"], constants.MAX_CURSOR_IDLE_SECONDS)


class ConfigFromPageTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        values = dialogs.page(DEFAULT_CONFIG)["values"]
        values["hide_toolbar"] = False
        values["cursor_idle_seconds"] = 12
        config = dialogs.config_from_page(values)
        self.assertFalse(config.hide_toolbar)
        self.assertEqual(config.cursor_idle_seconds, 12)

    def test_bad_values_fall_back_to_defaults(self) -> None:
        config = dialogs.config_from_page({"hide_toolbar": "no", "cursor_idle_seconds": 999, "hide_cursor": 1})
        self.assertEqual(asdict(config), asdict(DEFAULT_CONFIG))
        self.assertEqual(dialogs.config_from_page(None), DEFAULT_CONFIG)
        self.assertEqual(dialogs.config_from_page({"cursor_idle_seconds": True}), DEFAULT_CONFIG)


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("#hider-app", (ADDON / "web/panel.css").read_text(encoding="utf-8"))
        self.assertIn("var HiderPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
