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
import unittest.mock
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
    """Todos los controles con clave, también los que van en pareja (1.3.0)."""
    found: list[dict] = []
    for card in page["cards"]:
        for item in card["items"]:
            found.extend(item.get("children", [item]) if item["type"] == "pair" else [item])
    return [item for item in found if "key" in item]


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
        self.assertEqual([option["value"] for option in chips["options"]], options.sorted_themes())
        self.assertEqual(sorted(options.sorted_themes()), sorted(THEME_KEYS))
        self.assertNotIn("fire_red", THEME_KEYS)
        self.assertTrue(all(option["swatch"].startswith("#") for option in chips["options"]))

    def test_labels_without_px(self) -> None:
        for item in _items(options.page(DEFAULT_CONFIG, 0)):
            if item["type"] == "stepper":
                self.assertNotIn("(px)", item["label"])
                # 1.3.0: el margen a la vista, «px · 12–22».
                self.assertEqual(item["unit"], f"px · {item['min']}–{item['max']}")

    # FIX-003: sin record no se puede restablecer; la pregunta trae Si y No.
    # Desde la 1.3.0, sin récord el enlace no se enseña (disabled lo oculta).
    def test_reset_disabled_without_record(self) -> None:
        stat = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["type"] == "stat")
        self.assertTrue(stat["action"]["disabled"])
        stat = next(item for item in _items(options.page(DEFAULT_CONFIG, 5)) if item["type"] == "stat")
        self.assertFalse(stat["action"]["disabled"])
        self.assertTrue(stat["action"]["confirm"]["yes"])
        self.assertTrue(stat["action"]["confirm"]["no"])
        self.assertNotIn("strong", stat["done"])
        self.assertNotIn("-", stat["done"]["before"])


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


class Version12Tests(unittest.TestCase):
    """Informe del 2026-11-09 (1.2.0)."""

    def test_hard_keeps_the_streak(self) -> None:
        from coreprogress.state import SessionState

        state = SessionState()
        for _ in range(3):
            state.register_answer(1, True)
        self.assertEqual(state.correct_streak, 3)
        state.register_answer(1, False)
        self.assertEqual(state.correct_streak, 0)

    def test_milestones(self) -> None:
        from coreprogress.effects import is_celebration_milestone

        shown = [n for n in range(1, 61) if is_celebration_milestone(n)]
        self.assertEqual(shown, [5, 10, 20, 30, 40, 50, 60])

    def test_bar_never_goes_back_except_on_undo(self) -> None:
        from coreprogress.state import SessionState

        state = SessionState()
        state.base_done, state.initial_total = 10, 10
        self.assertEqual(state.real_progress(10), 50.0)  # al volver: donde lo dejó
        self.assertEqual(state.update_shown(state.real_progress(4)), 80.0)
        self.assertEqual(state.update_shown(state.real_progress(7)), 80.0)  # vencen tarjetas: quieta
        self.assertEqual(state.update_shown(state.real_progress(0)), 100.0)
        state.undo_pending = True
        self.assertEqual(state.update_shown(state.real_progress(1)), 95.0)  # deshacer sí retrocede

    def test_auto_space_keeps_the_card_free(self) -> None:
        from coreprogress.settings import auto_space

        self.assertEqual(auto_space(16, celebrate=False), 34)
        self.assertEqual(auto_space(16), 58)
        self.assertGreater(auto_space(12, celebrate=False), 12 + 10)

    def test_plural_forms(self) -> None:
        from coreprogress import i18n

        for code, one, five in (
            ("es", "1 acierto seguido", "5 aciertos seguidos"),
            ("ru", "1 верный ответ подряд", "5 верных ответов подряд"),
        ):
            with unittest.mock.patch.object(i18n, "current_lang", lambda code=code: code):
                self.assertEqual(i18n.record_value_label(1), one)
                self.assertEqual(i18n.streak_label(5), five)
                self.assertEqual(i18n.streak_label(2), "")

    def test_every_language_has_the_new_texts(self) -> None:
        from coreprogress import i18n

        keys = (
            "opt_record",
            "record_none",
            "record",
            "opt_record_reset",
            "opt_record_reset_confirm",
            "opt_effects",
            "opt_push",
            "opt_exclude",
            "opt_exclude_note",
            "theme_retired",
            "progress_of",
            "summary_best",
            "summary_record",
            "in_a_row_other",
            "cards_other",
        )
        self.assertEqual(len(i18n.TRANSLATIONS), 60)
        for code, table in i18n.TRANSLATIONS.items():
            for key in keys:
                self.assertIn(key, table, f"{code}: {key}")
            self.assertIn("{old}", table["theme_retired"])
            self.assertNotIn("streak", table)

    def test_retired_theme_notice(self) -> None:
        from dataclasses import replace

        cfg = replace(DEFAULT_CONFIG, theme="sunset_orange", retired_theme="fire_red")
        look = options.page(cfg, 0)["cards"][0]
        self.assertEqual(look["items"][0]["type"], "notice")


class Version13Tests(unittest.TestCase):
    """Informe del 2026-11-16 (1.3.0), con la opción recomendada en sus cuatro decisiones."""

    def test_two_cards_look_first_and_whole_record(self) -> None:
        page = options.page(DEFAULT_CONFIG, 90, window=41)
        self.assertTrue(page["hideTitle"])
        look, record = page["cards"]
        self.assertEqual(look["items"][0]["type"], "preview")
        self.assertEqual(look["restoreInline"], "theme")
        self.assertEqual([item["type"] for item in record["items"]], ["stat", "row"])
        keys = [item["key"] for card in page["cards"] for item in card["items"] if "key" in item]
        self.assertLess(keys.index("theme"), keys.index("reset_record"))
        order = [item.get("key") for item in _items(page)]
        self.assertLess(order.index("checkpoints_enabled"), order.index("effects_enabled"))

    def test_record_line_with_the_30_day_best(self) -> None:
        stat = next(item for item in _items(options.page(DEFAULT_CONFIG, 90, window=41)) if item["type"] == "stat")
        with unittest.mock.patch.object(
            options,
            "t",
            lambda key: {"best30": "Mejor racha en 30 días: {count}", "record_inline": "récord: {count}"}.get(key, key),
        ):
            parts = options._record_parts(90, 41)
        self.assertEqual(parts["before"] + parts["strong"] + parts["after"], "Mejor racha en 30 días: 41 · récord: 90")
        self.assertIn("strong", stat["parts"])

    def test_swatches_have_an_ink_border(self) -> None:
        chips = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["key"] == "theme")
        self.assertTrue(all(option["swatchBorder"].startswith("#") for option in chips["options"]))

    def test_round_marks(self) -> None:
        from coreprogress.effects import round_marks

        for total, marks in (
            (9, []),
            (12, [5, 10]),
            (27, [5, 10, 15, 20]),
            (36, [10, 20, 30]),
            (48, [10, 20, 30, 40]),
            (75, [20, 40, 60]),
            (130, [20, 40, 60, 80, 100]),
            (240, [50, 100, 150, 200]),
        ):
            self.assertEqual(round_marks(total), marks, total)
        for total in range(10, 3001):
            marks = round_marks(total)
            self.assertLessEqual(len(marks), 5, total)
            self.assertTrue(all(m / total <= 0.92 for m in marks), total)

    def test_final_mark_with_the_total(self) -> None:
        from coreprogress.data import checkpoint_marks

        marks = checkpoint_marks(27)
        self.assertEqual([m["num"] for m in marks], [5, 10, 15, 20, 27])
        self.assertEqual(marks[-1]["pos"], 100.0)
        self.assertEqual(checkpoint_marks(8), [])

    def test_one_celebration_per_answer(self) -> None:
        from coreprogress.effects import celebration_for

        # Récord 90 y mejor de 30 días 41: a las 42 se celebra la de 30 días;
        # a las 91, el récord; a las 50, la racha.
        self.assertEqual(celebration_for(42, 90, 41, True), "window")
        self.assertEqual(celebration_for(91, 90, 41, True), "record")
        self.assertEqual(celebration_for(50, 90, 41, True), "streak")
        self.assertEqual(celebration_for(10, 90, 41, True), "streak")
        self.assertEqual(celebration_for(7, 90, 41, True), "")
        # Récord por debajo del mínimo: desde 3.
        self.assertEqual(celebration_for(3, 0, 0, True), "record")
        # En un mazo que no cuenta, solo la racha.
        self.assertEqual(celebration_for(42, 90, 41, False), "")
        self.assertEqual(celebration_for(5, 90, 41, False), "streak")

    def test_30_day_window(self) -> None:
        from coreprogress.effects import best_in_window, with_day_best

        daily = {100: 41, 80: 60, 120: 12}
        self.assertEqual(best_in_window(daily, 120), 41)
        self.assertEqual(best_in_window(daily, 130), 12)
        kept = with_day_best(daily, 130, 20)
        self.assertEqual(kept, {120: 12, 130: 20})
        self.assertEqual(with_day_best(kept, 130, 5), kept)

    def test_tints_reach_contrast(self) -> None:
        from coreprogress import palettes

        def lum(hex_color: str) -> float:
            values = [int(hex_color.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)]
            lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
            return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

        def ratio(a: str, b: str) -> float:
            la, lb = lum(a), lum(b)
            return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

        for theme in palettes.THEME_KEYS:
            for gold in (False, True):
                day, night = palettes.ink(theme, False, gold), palettes.ink(theme, True, gold)
                self.assertGreaterEqual(ratio(day, "#E4E5E7"), 3, theme)  # contorno sobre el canal
                self.assertGreaterEqual(ratio(day, "#ffffff"), 4.5, theme)  # número blanco
                self.assertGreaterEqual(ratio(day, "#F7F8FA"), 4.5, theme)  # aviso
                self.assertGreaterEqual(ratio(night, "#23262F"), 3, theme)
                self.assertGreaterEqual(ratio(night, "#1b2430"), 4.5, theme)
                self.assertGreaterEqual(ratio(night, "#12161F"), 4.5, theme)

    def test_flat_fill_with_contour(self) -> None:
        from coreprogress import palettes

        mode = palettes.fill_bundle("classic_green", False).light
        self.assertEqual(mode.fill_shadow, "inset 0 0 0 1px #167628")
        self.assertEqual(mode.label_glow, "none")
        gold = palettes.fill_bundle("classic_green", True).light
        self.assertIn("inset 0 0 0 1px #856206", gold.fill_shadow)
        self.assertIn("0 0 6px", gold.fill_shadow)

    def test_new_texts_in_every_language(self) -> None:
        from coreprogress import i18n

        for code, table in i18n.TRANSLATIONS.items():
            for key in ("best30", "record_inline", "none", "bar_name", "no_match"):
                self.assertTrue(table.get(key), f"{code}: {key}")
            self.assertIn("{count}", table["best30"], code)


if __name__ == "__main__":
    unittest.main()
