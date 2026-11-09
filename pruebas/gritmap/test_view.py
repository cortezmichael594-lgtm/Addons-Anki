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
            (sample(past={}, future_counts={}), "cada día de estudio se pintará aquí."),
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

    def test_due_greys_follow_the_palette(self) -> None:
        # 4.13.0 (informe de Atelier del 2026-11-04, apartado 1.6): los grises de los días
        # pendientes se calculan con el texto y la tarjeta de la paleta, no son fijos.
        css = palettes.palette_css("classic_green")
        for level, (day, night) in enumerate(zip(palettes.FUTURE_TEXT_LIGHT, palettes.FUTURE_TEXT_DARK, strict=True)):
            self.assertIn(
                f"--gritmap-f{level + 1}:color-mix(in srgb, var(--gritmap-fg) {day}%, var(--gritmap-card));", css
            )
            self.assertIn(
                f"--gritmap-f{level + 1}:color-mix(in srgb, var(--gritmap-fg) {night}%, var(--gritmap-card));", css
            )
        self.assertNotRegex(css, r"--gritmap-f\d:#")
        self.assertEqual(list(palettes.FUTURE_TEXT_LIGHT), sorted(palettes.FUTURE_TEXT_LIGHT))

    def test_cards_take_the_anki_container_corner(self) -> None:
        # 4.13.0: la esquina de los recuadros de Anki (o de la paleta de Atelier), no 10 px.
        block = CSS[CSS.index("#gritmap-root .gritmap-card {") :]
        self.assertIn("border-radius: var(--border-radius-medium, 12px);", block[: block.index("}")])

    def test_card_titles_are_muted(self) -> None:
        block = CSS[CSS.index("#gritmap-root .gritmap-mini .gritmap-card-title {") :]
        self.assertIn("color: var(--gritmap-muted);", block[: block.index("}")])

    def test_updating_text_exists_in_every_language(self) -> None:
        for code, texts in i18n.STRINGS.items():
            self.assertTrue(texts.get("updating", "").endswith("…"), code)


class NoCardTipsTest(unittest.TestCase):
    """4.14.0: las tarjetas no tienen globos ni subrayados de puntos."""

    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def streak_sample(self) -> HeatmapData:
        # Racha de 18 dias (hasta ayer) y record de 21, hace mas de un mes.
        past = {d: DayActivity(10, 10, 0) for d in range(1, 19)}
        past.update({d: DayActivity(10, 10, 0) for d in range(30, 51)})
        return HeatmapData(past=past, future_counts={}, today=TODAY, retention_days={})

    def summary(self, data: HeatmapData, **changes: object) -> str:
        cfg = replace(DEFAULT_CONFIG, **changes)
        html = view.build_widget_html(data, cfg, 0)
        return html[html.index('class="gritmap-summary') :]

    def test_cards_have_no_tips_and_no_tab_stops(self) -> None:
        summary = self.summary(self.streak_sample(), goal_mode="number", goal=2, freezes=True)
        self.assertNotIn("data-gritmap-info", summary)
        self.assertNotIn("data-gritmap-tip", summary)
        self.assertNotIn("tabindex", summary)
        self.assertNotIn("gritmap-tipped", summary)
        self.assertNotIn(" title=", summary)

    def test_record_goes_before_freezes(self) -> None:
        summary = self.summary(self.streak_sample(), freezes=True)
        streak = summary[summary.index(">Racha<") :]
        line = streak[
            streak.index('class="gritmap-line"') : streak.index("</div>", streak.index('class="gritmap-line"'))
        ]
        self.assertIn("del récord", line)
        self.assertIn("comod", line)
        self.assertLess(line.index("del récord"), line.index("comod"))

    def test_goal_left_agrees_with_the_number(self) -> None:
        one = self.summary(sample(past={0: DayActivity(1, 1, 0)}), goal_mode="number", goal=2)
        self.assertIn("falta <span", one)
        self.assertNotIn("faltan <span", one)
        two = self.summary(sample(past={}), goal_mode="number", goal=2)
        self.assertIn("faltan <span", two)

    def test_cards_without_data_are_not_shown(self) -> None:
        # 4.15.0: primer dia; sin promedio ni retencion, solo «Hoy» y «Racha».
        summary = self.summary(sample(past={0: DayActivity(5, 5, 0)}, retention_days={}))
        self.assertIn("gritmap-n2", summary)
        self.assertNotIn("Promedio diario", summary)
        self.assertNotIn("Retención", summary)
        self.assertNotIn("N/A", summary)
        only_today = self.summary(sample(past={0: DayActivity(5, 5, 0)}, retention_days={}), show_streak=False)
        self.assertIn("gritmap-n1", only_today)

    def test_retention_has_no_fsrs_target(self) -> None:
        summary = self.summary(sample())
        self.assertNotIn("Objetivo", summary)

    def test_grey_line_is_never_cut(self) -> None:
        # 4.15.0, accesibilidad: la linea se ve entera, sin «…» ni globo.
        summary = self.summary(sample())
        self.assertNotIn("data-gritmap-full", summary)
        block = CSS[CSS.index("#gritmap-root .gritmap-line {") :]
        block = block[: block.index("}")]
        self.assertNotIn("line-clamp", block)
        self.assertNotIn("overflow: hidden", block)

    def test_goal_left_has_a_general_form_in_every_language(self) -> None:
        for code, texts in i18n.STRINGS.items():
            self.assertIn("{count}", texts.get("goal_left_other", ""), code)


class HabitTextsTest(unittest.TestCase):
    """4.15.0: textos, habito y abandono (informe del cliente del 2026-11-09)."""

    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def summary(self, data: HeatmapData, **changes: object) -> str:
        html = view.build_widget_html(data, replace(DEFAULT_CONFIG, **changes), 0)
        return html[html.index('class="gritmap-summary') :]

    def test_broken_streak_looks_ahead_with_the_plan(self) -> None:
        # Estudio hace 4 dias; hoy, nada: racha a cero.
        data = sample(past={4: DayActivity(10, 10, 0), 5: DayActivity(10, 10, 0)}, retention_days={})
        summary = self.summary(data, study_plan="al levantarme")
        self.assertNotIn("Última sesión", summary)
        self.assertNotIn("hace", summary)
        self.assertIn("hoy pendiente" + view.SEP + "al levantarme", summary)

    def test_first_day_streak_shows_the_plan_too(self) -> None:
        summary = self.summary(sample(past={}, future_counts={1: 3}), study_plan="al levantarme")
        self.assertIn("hoy pendiente" + view.SEP + "al levantarme", summary)

    def test_today_without_week_has_no_zero_line(self) -> None:
        summary = self.summary(sample(past={}, future_counts={1: 3}))
        self.assertNotIn("en 7 días", summary)

    def test_grey_lines_and_map_foot_start_in_lowercase(self) -> None:
        data = sample(past={0: DayActivity(5, 5, 0), 1: DayActivity(5, 5, 0)})
        summary = self.summary(data, goal_mode="number", goal=2)
        self.assertIn("✓</span> meta cumplida", summary)
        html = view.build_widget_html(data, DEFAULT_CONFIG, 0)
        self.assertIn(">menos<", html)
        self.assertIn(">más<", html)
        self.assertIn(">pendientes</span>", html)

    def test_lowercase_respects_german_nouns_and_turkish_i(self) -> None:
        anki.lang.current_lang = "de"
        i18n.reset()
        self.assertEqual(view.lt("goal_done"), "Ziel erreicht")
        self.assertEqual(view.lt("legend_less"), "weniger")
        anki.lang.current_lang = "tr"
        i18n.reset()
        i18n.STRINGS["tr"]["gritmap_test"] = "Ilık"
        try:
            self.assertEqual(view.lt("gritmap_test"), "ılık")
        finally:
            del i18n.STRINGS["tr"]["gritmap_test"]

    def test_screen_reader_hears_commas_and_done(self) -> None:
        data = sample(past={0: DayActivity(5, 5, 0), 1: DayActivity(5, 5, 0)})
        summary = self.summary(data)
        self.assertIn('<span class="gritmap-sr">hoy hecho</span>', summary)
        self.assertNotIn("✓ hoy</span> · ", summary)

    def test_days_before_first_review_tip_only_the_date(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertIn('data-t="nodata"', cell(html, "2026-09-02"))
        self.assertEqual(view._texts("cards")["nodata"], "")

    def test_covered_replaces_forgiven(self) -> None:
        self.assertEqual(i18n.STRINGS["es"]["legend_forgiven"], "Cubierto")
        self.assertEqual(i18n.STRINGS["es"]["tt_forgiven_freeze"], "Cubierto con un comodín")
        self.assertEqual(i18n.STRINGS["es"]["opt_freezes"], "Cubrir días sueltos con comodines")
        self.assertEqual(i18n.STRINGS["es"]["surprise_best_week"], "Mejor semana del año")


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
