"""Pruebas de la lectura de la configuracion: valores raros y paso de 3.x a 4.0."""

from __future__ import annotations

import unittest
from datetime import date

from gritmap.config import DEFAULT_CONFIG, FIT_WIDTH, build_config


class BuildConfigTest(unittest.TestCase):
    def test_defaults(self) -> None:
        self.assertEqual(build_config({}, {}), DEFAULT_CONFIG)

    def test_retired_themes_move_to_the_closest(self) -> None:
        for old, new in (("fire_red", "sunset_orange"), ("rose_pink", "royal_purple"), ("lagoon_turquoise", "ocean_blue")):
            cfg = build_config({"theme": old}, {})
            self.assertEqual((cfg.theme, cfg.retired_theme), (new, old))
        self.assertEqual(build_config({"theme": "ocean_blue"}, {}).retired_theme, "")

    def test_pixels_are_back(self) -> None:
        # 4.2.0: tamano de celda y redondeo en pixeles, dentro de sus limites.
        cfg = build_config({"map_size": 40, "map_radius": 6}, {})
        self.assertEqual((cfg.cell_size, cfg.border_radius), (40, 6))
        clipped = build_config({"map_size": 500, "map_radius": -3}, {})
        self.assertEqual((clipped.cell_size, clipped.border_radius), (60, 0))
        self.assertEqual(build_config({"map_radius": 40}, {}).border_radius, 15)
        self.assertEqual(build_config({"map_size": 0}, {}).cell_size, FIT_WIDTH)
        # Quien eligio «Redondeado» en la 4.0 o la 4.1 conserva las esquinas.
        rounded = build_config({"map_size": 24, "map_radius": 3, "shape": "rounded", "size": "fit"}, {})
        self.assertEqual(rounded.border_radius, 8)

    def test_24_px_is_the_default(self) -> None:
        # 4.6.0: de serie, 24 px y 3 px de redondeo; lo guardado por la 4.2
        # a la 4.5 ya no se lee.
        self.assertEqual((DEFAULT_CONFIG.cell_size, DEFAULT_CONFIG.border_radius), (24, 3))
        old = build_config({"map_size": 24, "map_radius": 3, "map_cell": 0, "map_corners": 2, "cell_size": 25}, {})
        self.assertEqual((old.cell_size, old.border_radius), (24, 3))
        self.assertEqual(build_config({"map_size": 3}, {}).cell_size, 10)

    def test_bad_values_fall_back(self) -> None:
        # Regla de FIX-005: Infinity o NaN no son numeros de verdad.
        cfg = build_config({"goal": float("inf"), "goal_mode": "otra", "map_size": float("nan"), "freezes": "si"}, {})
        self.assertEqual(
            (cfg.goal, cfg.goal_mode, cfg.cell_size, cfg.freezes),
            (DEFAULT_CONFIG.goal, "none", 24, True),
        )

    def test_pause_is_checked(self) -> None:
        ok = build_config({}, {"pause": {"start": "2026-10-01", "end": "2026-10-10"}})
        self.assertEqual(ok.pause, (date(2026, 10, 1), date(2026, 10, 10)))
        for bad in ({"start": "2026-10-10", "end": "2026-10-01"}, {"start": "2026-10-01", "end": "2026-12-01"}, {"start": "x"}, "no"):
            self.assertIsNone(build_config({}, {"pause": bad}).pause, bad)


if __name__ == "__main__":
    unittest.main()
