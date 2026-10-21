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
        cfg = build_config({"map_cell": 40, "map_corners": 8}, {})
        self.assertEqual((cfg.cell_size, cfg.border_radius), (40, 8))
        clipped = build_config({"map_cell": 500, "map_corners": -3}, {})
        self.assertEqual((clipped.cell_size, clipped.border_radius), (60, 0))
        # Quien eligio «Redondeado» en la 4.0 o la 4.1 conserva las esquinas.
        rounded = build_config({"map_cell": 0, "map_corners": 2, "shape": "rounded", "size": "fit"}, {})
        self.assertEqual(rounded.border_radius, 5)

    def test_fit_to_width_is_the_default(self) -> None:
        # 4.4.0: de serie, ajustado al ancho como en la 4.1.0; el tamano y el
        # redondeo guardados por la 4.2 o la 4.3 ya no se leen.
        self.assertEqual((DEFAULT_CONFIG.cell_size, DEFAULT_CONFIG.border_radius), (FIT_WIDTH, 2))
        old = build_config({"map_cell": 0, "map_corners": 2, "cell_size": 25, "border_radius": 1}, {})
        self.assertEqual((old.cell_size, old.border_radius), (FIT_WIDTH, 2))
        self.assertEqual(build_config({"map_cell": 3}, {}).cell_size, 8)

    def test_bad_values_fall_back(self) -> None:
        # Regla de FIX-005: Infinity o NaN no son numeros de verdad.
        cfg = build_config({"goal": float("inf"), "goal_mode": "otra", "map_cell": float("nan"), "freezes": "si"}, {})
        self.assertEqual(
            (cfg.goal, cfg.goal_mode, cfg.cell_size, cfg.freezes),
            (DEFAULT_CONFIG.goal, "none", FIT_WIDTH, True),
        )

    def test_pause_is_checked(self) -> None:
        ok = build_config({}, {"pause": {"start": "2026-10-01", "end": "2026-10-10"}})
        self.assertEqual(ok.pause, (date(2026, 10, 1), date(2026, 10, 10)))
        for bad in ({"start": "2026-10-10", "end": "2026-10-01"}, {"start": "2026-10-01", "end": "2026-12-01"}, {"start": "x"}, "no"):
            self.assertIsNone(build_config({}, {"pause": bad}).pause, bad)


if __name__ == "__main__":
    unittest.main()
