"""Pruebas del panel de opciones (1.1.0), sin Anki a la vista: la descripcion
que recibe la pagina, la lectura de lo elegido y que «Restablecer» no borre
nada hasta Aceptar (FIX-003).

Se ejecutan con herramientas/empaquetar.py, que anade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

from aqt.qt import QApplication

from coreprogress import options
from coreprogress.palettes import THEME_KEYS
from coreprogress.settings import BAR_HEIGHT_MAX, DEFAULT_CONFIG, PUSH_MIN

ADDON = Path(options.__file__).parent

# Los textos «Sí» y «No» salen de los botones estándar de Qt: hace falta una
# aplicación Qt, sin pantalla.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
_APP = QApplication.instance() or QApplication([])


def _items(page: dict) -> list[dict]:
    return [item for card in page["cards"] for item in card["items"]]


class PanelPageTests(unittest.TestCase):
    def test_page_lists_every_option(self) -> None:
        page = options.page(DEFAULT_CONFIG, 7)
        keys = {item["key"] for item in _items(page)}
        self.assertEqual(
            keys,
            {
                "reset_record",
                "theme",
                "bar_height",
                "push_down",
                "effects_enabled",
                "checkpoints_enabled",
                "excluded_decks",
            },
        )
        self.assertEqual(set(page["values"]), set(page["defaults"]))
        json.dumps(page)

    def test_theme_chips_have_swatches(self) -> None:
        chips = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["key"] == "theme")
        self.assertEqual([option["value"] for option in chips["options"]], list(THEME_KEYS))
        self.assertTrue(all(option["swatch"].startswith("#") for option in chips["options"]))

    def test_labels_without_px(self) -> None:
        for item in _items(options.page(DEFAULT_CONFIG, 0)):
            if item["type"] == "stepper":
                self.assertNotIn("(px)", item["label"])
                self.assertEqual(item["unit"], "px")

    # FIX-003: sin record no se puede restablecer; la pregunta trae Si y No.
    def test_reset_disabled_without_record(self) -> None:
        stat = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["type"] == "stat")
        self.assertTrue(stat["action"]["disabled"])
        stat = next(item for item in _items(options.page(DEFAULT_CONFIG, 5)) if item["type"] == "stat")
        self.assertFalse(stat["action"]["disabled"])
        self.assertTrue(stat["action"]["confirm"]["yes"])
        self.assertTrue(stat["action"]["confirm"]["no"])
        self.assertEqual(stat["done"]["strong"], "-")


class ConfigFromPageTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        values = options.page(DEFAULT_CONFIG, 0)["values"]
        values.update(theme="ocean_blue", bar_height=20, excluded_decks=[3, 4, 3])
        cfg = options.config_from_page(values)
        self.assertEqual(cfg.theme, "ocean_blue")
        self.assertEqual(cfg.bar_height, 20)
        self.assertEqual(cfg.excluded_decks, (3, 4))

    def test_missing_decks_are_dropped(self) -> None:
        cfg = options.config_from_page({"excluded_decks": [1, 2, True, "3"]}, existing={2})
        self.assertEqual(cfg.excluded_decks, (2,))

    def test_bad_values(self) -> None:
        cfg = options.config_from_page({"theme": "nope", "bar_height": 99, "push_down": -5, "effects_enabled": 1})
        self.assertEqual(cfg.theme, DEFAULT_CONFIG.theme)
        self.assertEqual(cfg.bar_height, BAR_HEIGHT_MAX)
        self.assertEqual(cfg.push_down, PUSH_MIN)
        self.assertEqual(cfg.effects_enabled, DEFAULT_CONFIG.effects_enabled)
        self.assertEqual(options.config_from_page(None).theme, DEFAULT_CONFIG.theme)


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("var CoreprogressPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
