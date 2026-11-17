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
from coreprogress.settings import DEFAULT_CONFIG, PUSH_MIN

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
                "bar_width",
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
        # 1.5.0: la muestra es una minibarra con el degradado del tema.
        self.assertTrue(all(option["swatch"].startswith("linear-gradient(") for option in chips["options"]))

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
        # 1.5.0: solo valen los tres grosores; lo demás, el de serie.
        self.assertEqual(cfg.bar_height, DEFAULT_CONFIG.bar_height)
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

    def test_swatches_have_no_border(self) -> None:
        # 1.5.0 (informe del 2026-11-17, 2.6): la minibarra ya da 4,24 a 1 o más
        # contra la ficha y no lleva el contorno que pedía la 1.3.0.
        chips = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["key"] == "theme")
        self.assertTrue(all("swatchBorder" not in option for option in chips["options"]))

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
                # 1.5.0: aro del próximo hito sobre el canal, número sobre la
                # tinta y aviso sobre el fondo.
                self.assertGreaterEqual(ratio(day, "#D5D9E2"), 3, theme)
                self.assertGreaterEqual(ratio(day, "#FBFCFE"), 4.5, theme)
                self.assertGreaterEqual(ratio(day, "#F7F8FA"), 4.5, theme)
                self.assertGreaterEqual(ratio(night, "#272F3F"), 3, theme)
                self.assertGreaterEqual(ratio(night, "#12161F"), 4.5, theme)

    def test_contour_only_on_gold_by_day(self) -> None:
        # 1.5.0 (informe del 2026-11-17, 2.2 y 2.5): sin contorno en los temas
        # ni halo; solo el oro de día lleva contorno, y el oro, la estrella.
        from coreprogress import palettes

        for theme in palettes.THEME_KEYS:
            plain = palettes.fill_bundle(theme, False)
            self.assertEqual((plain.light.contour, plain.dark.contour), ("none", "none"), theme)
            self.assertEqual((plain.light.star, plain.dark.star), ("", ""), theme)
        gold = palettes.fill_bundle("classic_green", True)
        self.assertEqual(gold.light.contour, "inset 0 0 0 1px #845E09")
        self.assertEqual(gold.dark.contour, "none")
        self.assertEqual(gold.light.star, "#845E09")
        self.assertEqual(gold.dark.star, "#12161F")
        self.assertNotIn("glow", gold.to_json())

    def test_new_texts_in_every_language(self) -> None:
        from coreprogress import i18n

        for code, table in i18n.TRANSLATIONS.items():
            for key in ("best30", "record_inline", "none", "bar_name", "no_match"):
                self.assertTrue(table.get(key), f"{code}: {key}")
            self.assertIn("{count}", table["best30"], code)


def _lum(hex_color: str) -> float:
    values = [int(hex_color.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _ratio(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _lab(hex_color: str) -> tuple[float, float, float]:
    values = [int(hex_color.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def _de2000(c1: str, c2: str) -> float:
    """Diferencia de color CIEDE2000 (Sharma, Wu y Dalal, 2005)."""
    import math

    l1, a1, b1 = _lab(c1)
    l2, a2, b2 = _lab(c2)
    cb = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(cb**7 / (cb**7 + 25**7)))
    a1p, a2p = a1 * (1 + g), a2 * (1 + g)
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dl, dc = l2 - l1, c2p - c1p
    dh = h2p - h1p
    if c1p * c2p == 0:
        dh = 0
    elif dh > 180:
        dh -= 360
    elif dh < -180:
        dh += 360
    dhh = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))
    lbp, cbp = (l1 + l2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    t = (
        1
        - 0.17 * math.cos(math.radians(hbp - 30))
        + 0.24 * math.cos(math.radians(2 * hbp))
        + 0.32 * math.cos(math.radians(3 * hbp + 6))
        - 0.20 * math.cos(math.radians(4 * hbp - 63))
    )
    sl = 1 + 0.015 * (lbp - 50) ** 2 / math.sqrt(20 + (lbp - 50) ** 2)
    sc = 1 + 0.045 * cbp
    sh = 1 + 0.015 * cbp * t
    rt = -2 * math.sqrt(cbp**7 / (cbp**7 + 25**7)) * math.sin(math.radians(60 * math.exp(-(((hbp - 275) / 25) ** 2))))
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dhh / sh) ** 2 + rt * (dc / sc) * (dhh / sh))


class Version15Tests(unittest.TestCase):
    """Informe «Rediseño de color y forma: CoreProgress 1.4.0» (2026-11-17)."""

    def test_six_themes_weigh_the_same(self) -> None:
        # 1.3 y 1.4: punta a 3,1 del canal de día y a 7,0 de noche; arranque a
        # 2,0 y a 4,6. Los seis, con la misma medida (±0,1).
        from coreprogress import palettes

        for theme, (day, _ink, _pill, night, _npill) in palettes.THEMES.items():
            self.assertAlmostEqual(_ratio(day[2], "#D5D9E2"), 3.1, delta=0.1, msg=theme)
            self.assertAlmostEqual(_ratio(day[0], "#D5D9E2"), 2.0, delta=0.1, msg=theme)
            self.assertAlmostEqual(_ratio(night[2], "#272F3F"), 7.0, delta=0.1, msg=theme)
            self.assertAlmostEqual(_ratio(night[0], "#272F3F"), 4.6, delta=0.1, msg=theme)

    def test_text_on_pill_and_disc(self) -> None:
        from coreprogress import palettes

        for theme in [*palettes.THEME_KEYS, None]:
            data = palettes.GOLD if theme is None else palettes.THEMES[theme]
            day_ink, day_pill, night_ink, night_pill = data[1], data[2], data[3][2], data[4]
            self.assertGreaterEqual(_ratio(day_ink, day_pill), 5.0, theme)
            self.assertGreaterEqual(_ratio(night_ink, night_pill), 6.9, theme)
            self.assertGreaterEqual(_ratio(day_ink, "#FBFCFE"), 5.5, theme)  # número del próximo hito
            self.assertGreaterEqual(_ratio(night_ink, "#212836"), 7.5, theme)
            self.assertGreaterEqual(_ratio(palettes.ON_INK[0], day_ink), 5.5, theme)  # número del hito alcanzado
            self.assertGreaterEqual(_ratio(palettes.ON_INK[1], night_ink), 4.5, theme)

    def test_gold_contour_and_star_reach_three_to_one(self) -> None:
        from coreprogress import palettes

        self.assertGreaterEqual(_ratio(palettes.GOLD[1], "#D5D9E2"), 3)  # contorno de día
        self.assertGreaterEqual(_ratio(palettes.GOLD[1], palettes.GOLD[0][2]), 3)  # estrella de día
        self.assertGreaterEqual(_ratio("#12161F", palettes.GOLD[3][2]), 3)  # estrella de noche

    def test_no_theme_looks_like_the_action_blue(self) -> None:
        # 1.2 y regla 2: ningún tema a menos de 10 (ΔE2000) del azul de acción.
        from coreprogress import palettes

        for theme, (day, _ink, _pill, night, _npill) in palettes.THEMES.items():
            for color in day:
                self.assertGreaterEqual(_de2000(color, "#3B6FE0"), 10, f"{theme} {color}")
            for color in night:
                self.assertGreaterEqual(_de2000(color, "#4066E6"), 10, f"{theme} {color}")

    def test_soft_night(self) -> None:
        # Regla 3: de noche, ningún relleno con más croma que 0,15 (OKLCH).
        import math

        from coreprogress import palettes

        def chroma(hex_color: str) -> float:
            values = [int(hex_color.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)]
            r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values)
            lc = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
            mc = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
            sc = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
            a = 1.9779984951 * lc - 2.4285922050 * mc + 0.4505937099 * sc
            bb = 0.0259040371 * lc + 0.7827717662 * mc - 0.8086757660 * sc
            return math.hypot(a, bb)

        for theme, (_day, _ink, _pill, night, _npill) in palettes.THEMES.items():
            for color in night:
                self.assertLessEqual(chroma(color), 0.155, f"{theme} {color}")

    def test_three_thicknesses(self) -> None:
        from coreprogress.settings import BAR_HEIGHTS, as_bar_height

        self.assertEqual(BAR_HEIGHTS, (12, 16, 20))
        # Un grosor guardado por una versión anterior pasa al más cercano.
        for old, new in ((12, 12), (13, 12), (14, 16), (16, 16), (17, 16), (18, 20), (22, 20), ("x", 16), (True, 16)):
            self.assertEqual(as_bar_height(old), new, old)
        seg = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["key"] == "bar_height")
        self.assertEqual(seg["type"], "segmented")
        self.assertEqual([option["value"] for option in seg["options"]], [12, 16, 20])
        from coreprogress.i18n import TRANSLATIONS, t

        self.assertEqual(
            [option["label"] for option in seg["options"]],
            [t("thickness_thin"), t("thickness_normal"), t("thickness_thick")],
        )
        es = TRANSLATIONS["es"]
        self.assertEqual(
            (es["opt_thickness"], es["thickness_thin"], es["thickness_thick"]), ("Grosor", "Fina", "Gruesa")
        )
        self.assertEqual(options.config_from_page({"bar_height": 20}).bar_height, 20)

    def test_thin_bar_has_no_discs(self) -> None:
        from coreprogress import view
        from coreprogress.palettes import fill_bundle

        def args(height: int) -> dict:
            return view.build_args(fill_bundle("classic_green", False), 40, height, 0, True, [], False)

        self.assertTrue(args(12)["small"])
        self.assertFalse(args(16)["small"])
        self.assertEqual((args(16)["cpFont"], args(20)["cpFont"]), (11, 12))
        self.assertEqual(args(16)["cpSize"], 20)

    def test_everything_injected_carries_the_package_prefix(self) -> None:
        from coreprogress import view

        page = view.reviewer_page_head() + view.reviewer_page_body()
        self.assertNotIn("_cprog", page)
        self.assertNotIn("cprog-", page.replace("--cprog-track", ""))
        self.assertNotIn("Glow", page)
        self.assertIn("max-width:720px", page)
        self.assertIn("prefers-reduced-motion", page)
        self.assertIn("forced-colors", page)

    def test_thickness_texts_in_every_language(self) -> None:
        from coreprogress import i18n

        for code, table in i18n.TRANSLATIONS.items():
            for key in ("opt_thickness", "thickness_thin", "thickness_normal", "thickness_thick"):
                self.assertTrue(table.get(key), f"{code}: {key}")


class Version16Tests(unittest.TestCase):
    """1.6.0 (petición de la persona, 2026-11-17): ancho elegible y franja opaca al desplazar."""

    def test_width_option(self) -> None:
        from coreprogress.i18n import TRANSLATIONS

        seg = next(item for item in _items(options.page(DEFAULT_CONFIG, 0)) if item["key"] == "bar_width")
        self.assertEqual([option["value"] for option in seg["options"]], ["card", "window"])
        self.assertEqual(DEFAULT_CONFIG.bar_width, "card")
        self.assertEqual(options.config_from_page({"bar_width": "window"}).bar_width, "window")
        self.assertEqual(options.config_from_page({"bar_width": "nope"}).bar_width, "card")
        es = TRANSLATIONS["es"]
        self.assertEqual((es["opt_width"], es["width_card"], es["width_window"]), ("Ancho", "Tarjeta", "Ventana"))
        for code, table in TRANSLATIONS.items():
            for key in ("opt_width", "width_card", "width_window"):
                self.assertTrue(table.get(key), f"{code}: {key}")

    def test_full_width_and_opaque_band(self) -> None:
        from coreprogress import view
        from coreprogress.palettes import fill_bundle

        args = view.build_args(fill_bundle("classic_green", False), 40, 16, 0, True, [], False, full_width=True)
        self.assertTrue(args["fullWidth"])
        page = view.reviewer_page_head()
        # Al bajar por una tarjeta larga, el contenido pasa por debajo de una franja del color
        # del fondo y no se ve a través de la barra.
        self.assertIn("background:var(--coreprogress-cut,transparent)", page)
        self.assertIn(".coreprogress-full #coreprogress-track{max-width:none;}", page)


if __name__ == "__main__":
    unittest.main()
