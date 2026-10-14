"""Pruebas del HTML del mapa (sin Anki en marcha)."""

from __future__ import annotations

import json
import re
import unittest
from dataclasses import replace
from datetime import date

import anki.lang
from gritmap import i18n, palettes, view
from gritmap.config import DEFAULT_CONFIG, KeyDate
from gritmap.data import DayActivity, HeatmapData

TODAY = date(2026, 10, 13)


def sample(**changes: object) -> HeatmapData:
    base = HeatmapData(
        past={0: DayActivity(5, 5, 1), 1: DayActivity(1240, 900, 0), 40: DayActivity(30, 20, 3)},
        future_counts={1: 12, 30: 1},
        today=TODAY,
        retention_days={1: (40, 36)},
    )
    return replace(base, **changes)


class WidgetTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_map_has_nav_year_and_stats(self) -> None:
        cfg = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 11, 20), "Examen <b>"),))
        html = view.build_widget_html(sample(), cfg, 0)
        self.assertEqual(html.count('class="gritmap-btn"'), 4)
        self.assertNotIn("legend", html)
        self.assertNotIn("data-gritmap-wd", html)
        self.assertEqual(html.count('class="gritmap-stat"'), 5)
        # El dia de hoy se marca y es el que recibe el tabulador.
        self.assertRegex(html, r'data-d="2026-10-13"[^>]*data-gritmap-today="1"[^>]*tabindex="0"')
        # La fecha clave lleva su borde (atributo) y su nombre escapado.
        self.assertRegex(html, r'data-d="2026-11-20"[^>]*data-gritmap-key=')
        self.assertIn("Examen &amp;lt;b&amp;gt;", html)
        self.assertNotIn("<b>Examen", html)

    def test_year_label_shows_the_year_total(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        # 5 + 1240 + 30 repasos en 2026, en la unidad de la medida.
        self.assertIn('data-n=&quot;1275&quot;', html)
        self.assertIn("repasos", html[html.index("gritmap-yv"):html.index("gritmap-yv") + 300])
        self.assertEqual(view.year_total(sample(), 2026, "new"), 4)
        self.assertEqual(view.year_total(sample(), 2025, "reviews"), 0)

    def test_period_buttons(self) -> None:
        html = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, avg_window=365), 0)
        self.assertEqual(len(re.findall(r'class="gritmap-period[ "]', html)), 3)
        self.assertIn('class="gritmap-period gritmap-on" data-gritmap-btn="window:365"', html)
        self.assertIn(">Todo<", html)
        self.assertIn(">1 año<", html)
        self.assertIn("¡", html[html.index("gritmap-yv"):html.index("gritmap-periods")])
        self.assertNotIn("window:90", html)

    def test_stats_in_two_groups_with_streak_first(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        stats = html[html.index('class="gritmap-stats"'):]
        self.assertEqual(stats.count('class="gritmap-group"'), 2)
        order = [stats.index(label) for label in
                 ("Racha actual", "Racha más larga", "Días estudiados", "Promedio diario", "Retención")]
        self.assertEqual(order, sorted(order))
        # La unidad va aparte para poder ir mas pequena que el numero.
        self.assertIn('<span class="gritmap-unit">repasos</span>', stats)

    def test_tooltip_texts_have_no_date(self) -> None:
        # La fecha va en su propia linea, la pone el navegador (peticion del cliente).
        for code, texts in i18n.STRINGS.items():
            for key, text in texts.items():
                self.assertNotIn("{date}", text, f"{code}.{key}")

    def test_warm_themes_mark_key_dates_in_blue(self) -> None:
        self.assertIn("--gritmap-key:var(--state-new", palettes.palette_css("sunset_orange"))
        self.assertNotIn("--gritmap-key", palettes.palette_css("classic_green"))

    def test_all_injected_names_start_with_gritmap(self) -> None:
        # Regla de FIX-008.
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        for name in re.findall(r'class="([^"]+)"', html.replace("&quot;", '"')):
            for part in name.split():
                self.assertTrue(part.startswith("gritmap"), part)
        for attr in re.findall(r"\sdata-([a-z-]+)=", html):
            self.assertTrue(attr.startswith("gritmap") or attr in ("d", "v", "t", "n", "p"), attr)

    def test_excluded_deck_and_no_data_keep_the_options_button(self) -> None:
        for data, text in ((sample(deck_excluded=True), "Este mazo está excluido del mapa."),
                           (sample(past={}, future_counts={}), "No hay datos de actividad para mostrar.")):
            html = view.build_widget_html(data, DEFAULT_CONFIG, 0)
            self.assertIn(text, html)
            self.assertIn('data-gritmap-cmd="opts"', html)

    def test_numbers_and_percentages_are_left_for_the_browser(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn('class="gritmap-pct" data-p="90"', html)
        self.assertNotIn("1.240", html)  # el punto de millar lo pone el navegador

    def test_payload_in_script_cannot_close_it(self) -> None:
        payload = view.payload_json('<div></script><!-- x --></div>')
        page = view.container_html(DEFAULT_CONFIG, payload)
        self.assertEqual(page.count("</script>"), 1)
        self.assertNotIn("<!--", page)
        inner = page[page.index("GritMap.render(") + len("GritMap.render("):page.rindex("); }")]
        self.assertEqual(json.loads(inner)["html"], '<div></script><!-- x --></div>')

    def test_palette_has_swatches_and_no_text_colour(self) -> None:
        css = palettes.palette_css("classic_green")
        self.assertIn(".gritmap-c10::before{background:var(--gritmap-p10);}", css)
        self.assertNotIn("{color:", css)

    def test_every_theme_has_ten_tones_per_mode(self) -> None:
        for scales in (palettes.PAST_LIGHT, palettes.PAST_DARK):
            self.assertEqual(set(scales), set(palettes.THEME_NAMES))
            for tones in scales.values():
                self.assertEqual(len(tones), 10)
        self.assertEqual(len(palettes.FUTURE_LIGHT), 10)
        self.assertEqual(len(palettes.FUTURE_DARK), 10)


class WebExportsPatternTest(unittest.TestCase):
    """Regresion de FIX-015: el patron dejaba leer archivos de otros complementos."""

    def test_own_assets_are_served(self) -> None:
        for path in ("web/gritmap.css", "web/gritmap.js"):
            self.assertIsNotNone(re.fullmatch(view.WEB_PATTERN, path), path)

    def test_paths_leaving_the_folder_are_refused(self) -> None:
        for path in ("web/../../otro/x.js", "web/sub/../../../otro/x.css", "web/../meta.json", "web/x.json"):
            self.assertIsNone(re.fullmatch(view.WEB_PATTERN, path), path)


if __name__ == "__main__":
    unittest.main()
