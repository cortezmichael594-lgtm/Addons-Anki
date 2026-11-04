"""Pruebas del HTML del mapa (sin Anki en marcha).

Desde la 4.12.0 describen el mapa de la serie 4 (tarjetas pequenas, anillo de
la meta, rombo de las fechas clave, cuatro tonos por tema); las de la 3.5.0
(cinco cifras en dos grupos, botones de periodo, diez tonos, borde azul de las
fechas clave) probaban piezas que el cliente retiro en la serie 4.
"""

from __future__ import annotations

import json
import re
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

import anki.lang

from gritmap import i18n, palettes, view
from gritmap.config import DEFAULT_CONFIG, KeyDate
from gritmap.data import DayActivity, HeatmapData

TODAY = date(2026, 10, 13)
CSS = (Path(view.__file__).parent / "web" / "gritmap.css").read_text(encoding="utf-8")


def sample(**changes: object) -> HeatmapData:
    base = HeatmapData(
        past={0: DayActivity(5, 5, 1), 1: DayActivity(1240, 900, 0), 40: DayActivity(30, 20, 3)},
        future_counts={1: 12, 30: 1},
        today=TODAY,
        retention_days={1: (40, 36)},
    )
    return replace(base, **changes)


def cell(html: str, iso: str) -> str:
    """La etiqueta <rect> del dia pedido."""
    found = re.search(r'<rect [^>]*data-d="' + iso + r'"[^>]*>', html)
    if found is None:
        raise AssertionError(f"no hay cuadrito para {iso}")
    return found.group(0)


class WidgetTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_map_has_year_nav_options_and_legend(self) -> None:
        cfg = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 11, 20), "Examen <b>"),))
        html = view.build_widget_html(sample(), cfg, 0)
        # «‹ 2026 ›» y el boton de opciones en la esquina.
        self.assertEqual(html.count('class="gritmap-btn"'), 3)
        self.assertIn('data-gritmap-corner="1"', html)
        self.assertIn('class="gritmap-legend"', html)
        # El dia de hoy se marca y es el que recibe el tabulador.
        self.assertRegex(cell(html, "2026-10-13"), r'data-gritmap-today="1"[^>]*tabindex="0"')
        # La fecha clave lleva su rombo y su nombre escapado.
        self.assertIn("data-gritmap-key=", cell(html, "2026-11-20"))
        self.assertIn('class="gritmap-kmark"', html)
        self.assertIn("Examen &amp;lt;b&amp;gt;", html)
        self.assertNotIn("<b>Examen", html)

    def test_card_titles_are_headings(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        for title in ("Hoy", "Racha", "Promedio diario", "Retención"):
            self.assertIn(f'<h3 class="gritmap-card-title">{title}</h3>', html)

    def test_all_injected_names_start_with_gritmap(self) -> None:
        # Regla de FIX-008.
        cfg = replace(DEFAULT_CONFIG, goal_mode="number", goal=2)
        html = view.build_widget_html(sample(), cfg, 0)
        for name in re.findall(r'class="([^"]+)"', html.replace("&quot;", '"')):
            for part in name.split():
                self.assertTrue(part.startswith("gritmap"), part)
        for attr in re.findall(r"\sdata-([a-z-]+)=", html):
            self.assertTrue(attr.startswith("gritmap") or attr in ("d", "v", "t", "n", "p"), attr)

    def test_excluded_deck_and_empty_map_keep_the_options_button(self) -> None:
        for data, text in (
            (sample(deck_excluded=True), "Este mazo está excluido del mapa."),
            (sample(past={}, future_counts={}), "Cada día que estudie se pintará aquí."),
        ):
            html = view.build_widget_html(data, DEFAULT_CONFIG, 0)
            self.assertIn(text, html)
            self.assertIn('data-gritmap-cmd="opts"', html)

    def test_numbers_and_percentages_are_left_for_the_browser(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn('class="gritmap-pct" data-p="90"', html)
        self.assertNotIn("1.240", html)  # el punto de millar lo pone el navegador

    def test_payload_in_script_cannot_close_it(self) -> None:
        payload = view.payload_json("<div></script><!-- x --></div>")
        page = view.container_html(DEFAULT_CONFIG, payload)
        self.assertEqual(page.count("</script>"), 1)
        self.assertNotIn("<!--", page)
        inner = page[page.index("GritMap.render(") + len("GritMap.render(") : page.rindex("); }")]
        self.assertEqual(json.loads(inner)["html"], "<div></script><!-- x --></div>")

    def test_day_tooltips_have_no_date(self) -> None:
        # La fecha del globo va en su propia linea y la pone el navegador.
        for measure in ("reviews", "cards", "new"):
            for key, text in view._texts(measure).items():
                self.assertNotIn("{date}", text, f"{measure}.{key}")


class PaletteTest(unittest.TestCase):
    def test_every_theme_has_four_tones_per_mode(self) -> None:
        for scales in (palettes.PAST_LIGHT, palettes.PAST_DARK):
            self.assertEqual(set(scales), set(palettes.THEME_NAMES))
            for tones in scales.values():
                self.assertEqual(len(tones), 4)

    def test_palette_has_tones_and_due_greys_but_no_text_colour(self) -> None:
        css = palettes.palette_css("classic_green")
        for name in ("p1", "p2", "p3", "p4", "f1", "f2", "f3"):
            self.assertIn(f"--gritmap-{name}:", css)
        self.assertNotIn("color:", css)


class NoDataTest(unittest.TestCase):
    """4.12.0: «sin dato» no es «no estudio» (informe 4.11, apartado 1.3)."""

    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_days_before_the_first_review_have_no_data(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        # El primer repaso fue hace 40 dias (2026-09-03).
        before = cell(html, "2026-09-02")
        self.assertIn("gritmap-nodata", before)
        self.assertIn('fill="var(--gritmap-nodata)"', before)
        self.assertIn('fill="var(--gritmap-p', cell(html, "2026-09-03"))

    def test_days_without_study_after_the_first_review_stay_empty(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        gap = cell(html, "2026-09-20")
        self.assertIn('fill="var(--gritmap-empty)"', gap)
        self.assertNotIn("gritmap-nodata", gap)

    def test_future_days_without_due_cards_have_no_data(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn("gritmap-nodata", cell(html, "2026-10-20"))
        self.assertIn('fill="var(--gritmap-f', cell(html, "2026-10-14"))
        self.assertNotIn("gritmap-nodata", cell(html, "2026-10-14"))

    def test_today_never_has_no_data(self) -> None:
        html = view.build_widget_html(sample(past={}, future_counts={}), DEFAULT_CONFIG, 0)
        today = cell(html, "2026-10-13")
        self.assertNotIn("gritmap-nodata", today)
        self.assertIn('fill="var(--gritmap-empty)"', today)
        self.assertIn("gritmap-nodata", cell(html, "2026-10-12"))

    def test_no_data_is_half_empty_half_card(self) -> None:
        self.assertIn("--gritmap-nodata: color-mix(in srgb, var(--gritmap-empty) 50%, var(--gritmap-card));", CSS)


class TodayCardTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_goal_number_is_big_and_total_is_a_unit(self) -> None:
        html = view.goal_of_html(0, 2)
        self.assertEqual(
            html,
            '<span class="gritmap-big-text"><span class="gritmap-n" data-n="0">0</span>'
            '<span class="gritmap-unit">de <span class="gritmap-n" data-n="2">2</span></span></span>',
        )

    def test_goal_total_first_in_other_word_orders(self) -> None:
        anki.lang.current_lang = "ko"
        i18n.reset()
        html = view.goal_of_html(1, 3)
        self.assertTrue(html.startswith('<span class="gritmap-big-text"><span class="gritmap-unit">'))
        self.assertTrue(html.endswith('<span class="gritmap-n" data-n="1">1</span></span>'))

    def test_today_card_shows_ring_and_goal(self) -> None:
        cfg = replace(DEFAULT_CONFIG, goal_mode="number", goal=2)
        html = view.build_widget_html(sample(past={}), cfg, 0)
        self.assertIn('class="gritmap-ring-track"', html)
        self.assertIn(view.goal_of_html(0, 2), html)

    def test_ring_track_uses_the_due_grey(self) -> None:
        block = CSS[CSS.index("#gritmap-root .gritmap-ring-track {") :]
        self.assertIn("stroke: var(--gritmap-f1);", block[: block.index("}")])

    def test_card_titles_are_muted(self) -> None:
        block = CSS[CSS.index("#gritmap-root .gritmap-mini .gritmap-card-title {") :]
        self.assertIn("color: var(--gritmap-muted);", block[: block.index("}")])

    def test_updating_text_exists_in_every_language(self) -> None:
        for code, texts in i18n.STRINGS.items():
            self.assertTrue(texts.get("updating", "").endswith("…"), code)


class WebExportsPatternTest(unittest.TestCase):
    """Regresion de FIX-015: el patron dejaba leer archivos de otros complementos."""

    def test_own_assets_are_served(self) -> None:
        for path in ("web/gritmap.css", "web/gritmap.js", "web/options.css", "web/options.js"):
            self.assertIsNotNone(re.fullmatch(view.WEB_PATTERN, path), path)

    def test_paths_leaving_the_folder_are_refused(self) -> None:
        for path in ("web/../../otro/x.js", "web/sub/../../../otro/x.css", "web/../meta.json", "web/x.json"):
            self.assertIsNone(re.fullmatch(view.WEB_PATTERN, path), path)


if __name__ == "__main__":
    unittest.main()
