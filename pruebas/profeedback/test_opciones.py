"""Pruebas del panel de ajustes (2.1.0), sin Anki a la vista: la descripción
que recibe la página, la lectura de lo elegido (regla de FIX-001), «Probar» y
las carpetas de sonidos propios (FIX-004).

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from profeedback import dialogs, paths
from profeedback.config import AddonConfig

ADDON = Path(dialogs.__file__).parent
SOUNDS = {
    "correct": ["good.mp3", "soft.mp3"],
    "deck_finish": ["khan.mp3"],
    "all_finish": [],
    "deck_perfect": [],
    "all_perfect": [],
}


def _all_items(items: list[dict]) -> list[dict]:
    found: list[dict] = []
    for item in items:
        found.append(item)
        found.extend(_all_items(item.get("children", [])))
    return found


class PanelPageTests(unittest.TestCase):
    def test_every_control_has_value_and_default(self) -> None:
        page = dialogs.page(AddonConfig(), SOUNDS)
        keys = {item["key"] for card in page["cards"] for item in _all_items(card["items"]) if "key" in item}
        self.assertEqual(keys, set(page["values"]))
        self.assertEqual(set(page["defaults"]), set(page["values"]))
        json.dumps(page)

    def test_select_starts_with_random_and_is_off_without_sounds(self) -> None:
        page = dialogs.page(AddonConfig(), SOUNDS)
        selects = {
            item["key"]: item
            for card in page["cards"]
            for item in _all_items(card["items"])
            if item["type"] == "select"
        }
        self.assertEqual(selects["answerSound"]["options"][0]["value"], "")
        self.assertFalse(selects["answerSound"]["unavailable"])
        self.assertTrue(selects["allDoneSound"]["unavailable"])

    def test_missing_saved_sound_shows_random(self) -> None:
        page = dialogs.page(AddonConfig(answerSound="gone.mp3"), SOUNDS)
        self.assertEqual(page["values"]["answerSound"], "")


class ConfigFromPageTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        values = dialogs.page(AddonConfig(), SOUNDS)["values"]
        values.update(answerSound="soft.mp3", soundVolume=40, confettiEnabled=False)
        cfg = dialogs.config_from_page(values, AddonConfig(), SOUNDS)
        self.assertEqual(cfg.answerSound, "soft.mp3")
        self.assertEqual(cfg.soundVolume, 40)
        self.assertFalse(cfg.confettiEnabled)

    def test_unknown_sound_becomes_random(self) -> None:
        cfg = dialogs.config_from_page({"answerSound": "nope.mp3", "soundVolume": 500}, AddonConfig(), SOUNDS)
        self.assertEqual(cfg.answerSound, "")
        self.assertEqual(cfg.soundVolume, 100)

    def test_test_request(self) -> None:
        values = {"answerSound": "good.mp3", "soundVolume": 30}
        self.assertEqual(
            dialogs.test_request({"name": "correct", "values": values}, SOUNDS), ("correct", "good.mp3", 30)
        )
        self.assertIsNone(dialogs.test_request({"name": "nope", "values": values}, SOUNDS))
        self.assertIsNone(dialogs.test_request(None, SOUNDS))


class UserFoldersTests(unittest.TestCase):
    # FIX-004: las subcarpetas de sonidos propios se crean vacías.
    def test_folders_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sonidos"
            with mock.patch.object(paths, "USER_SOUNDS_DIR", root):
                paths.ensure_user_sound_folders()
                paths.ensure_user_sound_folders()
            for subfolder in paths.SOUND_SUBFOLDERS.values():
                self.assertTrue((root / subfolder).is_dir(), subfolder)


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("var ProfeedbackPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
