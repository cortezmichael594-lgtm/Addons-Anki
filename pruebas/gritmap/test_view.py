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
        # Leyenda (3.6.0, el cliente la recupero el 2026-10-21): seis cuadritos.
        self.assertEqual(html.count('class="gritmap-lg-cell gritmap-lg-c'), 6)
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
                 ("Rachas", "Racha actual", "Racha más larga", "gritmap-periods",
                  "Promedio diario", "Días estudiados", "Retención")]
        self.assertEqual(order, sorted(order))
        # El selector de periodo ya no va junto al ano, sino sobre sus cifras.
        self.assertNotIn("gritmap-periods", html[:html.index('class="gritmap-stats"')])
        # La unidad va aparte para poder ir mas pequena que el numero.
        self.assertIn('<span class="gritmap-unit">repasos</span>', stats)

    def test_tooltip_texts_have_no_date(self) -> None:
        # La fecha va en su propia linea, la pone el navegador (peticion del cliente).
        for code, texts in i18n.STRINGS.items():
            for key, text in texts.items():
                self.assertNotIn("{date}", text, f"{code}.{key}")

    def test_warm_themes_mark_key_dates_in_blue(self) -> None:
        self.assertIn("--gritmap-key:var(--flag-4", palettes.palette_css("sunset_orange"))
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
                           (sample(past={}, future_counts={}), "Cada día que estudie se pintará aquí.")):
            html = view.build_widget_html(data, DEFAULT_CONFIG, 0)
            self.assertIn(text, html)
            self.assertIn('data-gritmap-cmd="opts"', html)
        self.assertIn('data-gritmap-cmd="opts:exclude"', view.build_widget_html(sample(deck_excluded=True), DEFAULT_CONFIG, 0))

    def test_empty_map_shows_the_year_with_today(self) -> None:
        html = view.build_widget_html(sample(past={}, future_counts={}), DEFAULT_CONFIG, 0)
        self.assertRegex(html, r'data-d="2026-10-13"[^>]*data-gritmap-today="1"')
        self.assertNotIn("gritmap-stats", html)
        self.assertNotIn("gritmap-legend", html)

    def test_legend_ranges_cover_every_count(self) -> None:
        thresholds = palettes.legend_thresholds(40.0)
        ranges = view.legend_ranges(thresholds)
        self.assertEqual(ranges[0][0], 1)
        self.assertIsNone(ranges[-1][1])
        for (low, high), (next_low, _next_high) in zip(ranges, ranges[1:]):
            self.assertEqual(next_low, (high or 0) + 1)
        # Cada cifra cae en el tono que dice su cuadrito de la leyenda.
        for count in range(1, 400):
            group = next(i for i, (low, high) in enumerate(ranges) if count >= low and (high is None or count <= high))
            level = palettes.level_index(count, thresholds) + 1
            self.assertIn(level, (2 * group + 1, 2 * group + 2), count)
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn("de &lt;span class=&quot;gritmap-n&quot;", html)

    def test_next_key_date_line(self) -> None:
        key_dates = (KeyDate(date(2026, 11, 5), "Anatomía"), KeyDate(date(2026, 1, 2), "Pasada"))
        line = view.next_key_html(key_dates, TODAY)
        self.assertIn('data-gritmap-cmd="key:2026-11-05"', line)
        self.assertIn("Anatomía · faltan", line)
        self.assertNotIn("Pasada", line)
        self.assertEqual(view.next_key_html((KeyDate(date(2026, 1, 2), "Pasada"),), TODAY), "")

    def test_streak_notes(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn("hoy hecho", html)
        stats = view.build_stats(
            replace(view.full_stats(sample()), current_streak=12, longest_streak=15, today_done=False),
            "reviews",
        )
        self.assertIn("hoy pendiente", stats)
        self.assertIn("a <span class=\"gritmap-n\" data-n=\"3\">3</span>", stats)
        record = view.build_stats(
            replace(view.full_stats(sample()), current_streak=16, longest_streak=16, previous_best=15, today_done=True),
            "reviews",
        )
        self.assertIn("nuevo récord", record)

    def test_week_line_has_its_reference(self) -> None:
        past = {**{d: DayActivity(10, 10, 0) for d in range(1, 8)}, **{d: DayActivity(5, 5, 0) for d in range(8, 15)}}
        week = view.week_payload(sample(past=past), "reviews", True)
        assert week is not None
        self.assertEqual(week["cls"], "up")
        self.assertIn("en 7 días", week["html"])
        self.assertIn("más que los 7 anteriores", week["html"])
        self.assertIn('data-n="70"', week["html"])

    def test_click_hint_texts(self) -> None:
        texts = json.loads(view.payload_json("", "reviews"))["texts"]
        self.assertEqual(texts["click_past"], "Pulse para ver estas tarjetas")

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
