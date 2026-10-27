"""Pruebas de la lectura de la configuracion: valores raros y paso de 3.x a 4.0."""

from __future__ import annotations

import unittest
from datetime import date

from gritmap.config import DEFAULT_CONFIG, FIT_WIDTH, build_config


class BuildConfigTest(unittest.TestCase):
    def test_defaults(self) -> None:
        self.assertEqual(build_config({}, {}), DEFAULT_CONFIG)

    def test_retired_themes_move_to_the_closest(self) -> None:
        # Rosa suave y Turquesa laguna vuelven en la 4.10.0: solo Rojo fuego
        # sigue retirado.
        for theme in ("rose_pink", "lagoon_turquoise"):
            self.assertEqual(build_config({"theme": theme}, {}).theme, theme)
        for old, new in (("fire_red", "sunset_orange"),):
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


class GoalDaysTest(unittest.TestCase):
    """4.11.0: dias con meta guardados en una coleccion TEMPORAL."""

    def setUp(self) -> None:
        import tempfile
        from pathlib import Path

        from anki.collection import Collection

        self._tmp = tempfile.TemporaryDirectory()
        self.col = Collection(str(Path(self._tmp.name) / "prueba.anki2"))

    def tearDown(self) -> None:
        self.col.close()
        self._tmp.cleanup()

    def test_marks_are_kept_short_and_survive_saving_options(self) -> None:
        from datetime import timedelta

        from gritmap import config

        start = date(2026, 10, 1)
        for offset in range(30):
            config.record_goal_day(self.col, start + timedelta(days=offset), "due", offset % 2 == 0)
        days = config.read_goal_days(self.col)
        self.assertEqual(len(days), config.GOAL_DAYS_KEEP)
        self.assertEqual(days["2026-10-30"], ("due", False))
        self.assertNotIn("2026-10-01", days)
        # Hoy se puede corregir (al deshacer la respuesta que la cumplio).
        config.record_goal_day(self.col, date(2026, 10, 30), "due", True)
        self.assertEqual(config.read_goal_days(self.col)["2026-10-30"], ("due", True))
        # Guardar las opciones no borra las marcas.
        config.save_scoped(self.col, DEFAULT_CONFIG)
        self.assertEqual(len(config.read_goal_days(self.col)), config.GOAL_DAYS_KEEP)

    def test_bad_marks_are_ignored(self) -> None:
        from gritmap.config import goal_days_from

        raw = {"goal_days": {"2026-10-01": ["due", 1], "malo": ["due", 1], "2026-10-02": ["none", 1], "2026-10-03": "x"}}
        self.assertEqual(goal_days_from(raw), {"2026-10-01": ("due", True)})
