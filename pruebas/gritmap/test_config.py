"""Pruebas de la lectura de la configuracion: valores raros y paso de 3.x a 4.0."""

from __future__ import annotations

import unittest
from datetime import date

from gritmap.config import DEFAULT_CONFIG, build_config


class BuildConfigTest(unittest.TestCase):
    def test_defaults(self) -> None:
        self.assertEqual(build_config({}, {}), DEFAULT_CONFIG)

    def test_retired_themes_move_to_the_closest(self) -> None:
        for old, new in (("fire_red", "sunset_orange"), ("rose_pink", "royal_purple"), ("lagoon_turquoise", "ocean_blue")):
            cfg = build_config({"theme": old}, {})
            self.assertEqual((cfg.theme, cfg.retired_theme), (new, old))
        self.assertEqual(build_config({"theme": "ocean_blue"}, {}).retired_theme, "")

    def test_pixels_of_version_3_become_words(self) -> None:
        # Anki mezcla los valores por defecto (size, shape) con los guardados.
        old_default = build_config({"size": "fit", "shape": "square", "cell_size": 25, "border_radius": 1}, {})
        self.assertEqual((old_default.size, old_default.shape), ("fit", "square"))
        big = build_config({"size": "fit", "shape": "square", "cell_size": 40, "border_radius": 8}, {})
        self.assertEqual((big.size, big.shape), ("large", "rounded"))
        new = build_config({"size": "large", "shape": "rounded"}, {})
        self.assertEqual((new.size, new.shape), ("large", "rounded"))

    def test_bad_values_fall_back(self) -> None:
        # Regla de FIX-005: Infinity o NaN no son numeros de verdad.
        cfg = build_config({"goal": float("inf"), "goal_mode": "otra", "size": 3, "freezes": "si"}, {})
        self.assertEqual(
            (cfg.goal, cfg.goal_mode, cfg.size, cfg.freezes),
            (DEFAULT_CONFIG.goal, "none", "fit", True),
        )

    def test_pause_is_checked(self) -> None:
        ok = build_config({}, {"pause": {"start": "2026-10-01", "end": "2026-10-10"}})
        self.assertEqual(ok.pause, (date(2026, 10, 1), date(2026, 10, 10)))
        for bad in ({"start": "2026-10-10", "end": "2026-10-01"}, {"start": "2026-10-01", "end": "2026-12-01"}, {"start": "x"}, "no"):
            self.assertIsNone(build_config({}, {"pause": bad}).pause, bad)


if __name__ == "__main__":
    unittest.main()
