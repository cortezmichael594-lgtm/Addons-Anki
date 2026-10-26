"""Pruebas del HTML del mapa (sin Anki en marcha)."""

from __future__ import annotations

import json
import re
import unittest
from dataclasses import replace
from datetime import date

import anki.lang
from gritmap import i18n, palettes, view
from gritmap.config import DEFAULT_CONFIG, FIT_WIDTH, KeyDate
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

    def test_map_first_then_five_cards(self) -> None:
        cfg = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 11, 20), "Examen <b>"),))
        html = view.build_widget_html(sample(), cfg, 0)
        # 4.1.0: el mapa arriba y las tarjetas debajo; sin estadisticas.
        self.assertLess(html.index("gritmap-activity"), html.index('class="gritmap-summary'))
        self.assertNotIn("gritmap-statscard", html)
        self.assertEqual(html.count('class="gritmap-card gritmap-mini"'), 5)
        order = [html.index(t) for t in (">Hoy<", ">Racha<", ">Promedio diario<", ">Retención<", ">Próxima fecha<")]
        self.assertNotIn(">Actividad<", html)
        self.assertEqual(order, sorted(order))
        # El dia de hoy se marca y es el que recibe el tabulador.
        self.assertRegex(html, r'data-d="2026-10-13"[^>]*data-gritmap-today="1"[^>]*tabindex="0"')
        # La fecha clave: nombre escapado y rombo en su cuadrito (4.8.0).
        self.assertRegex(html, r'data-d="2026-11-20"[^>]*data-gritmap-key=')
        self.assertIn('class="gritmap-kmark"', html)
        # Sin enlaces (cliente, 2026-10-21).
        self.assertNotIn("gritmap-link", html)
        self.assertIn("Examen &amp;lt;b&amp;gt;", html)
        self.assertNotIn("<b>Examen", html)
        # Sin cuadritos de color delante de las cifras ni comparativa suelta.
        self.assertNotIn("gritmap-c1", html)
        self.assertNotIn("gritmap-wd", html)

    def test_five_levels_and_legend_match(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertEqual(html.count('class="gritmap-lg-cell gritmap-lg-c'), 5)
        levels = set(re.findall(r'fill="var\(--gritmap-p(\d+)\)"', html))
        self.assertTrue(levels <= {"1", "2", "3", "4"}, levels)

    def test_map_card_has_no_title_or_year_total(self) -> None:
        # 4.3.0: sin «Actividad» ni «1.275 repasos en 2026» encima del mapa.
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        head = html[:html.index("gritmap-card-body")]
        self.assertIn("gritmap-notitle", head)
        self.assertNotIn("Actividad", head)
        self.assertNotIn("en 2026", head)

    def test_no_today_button(self) -> None:
        # 4.4.0: sin «Hoy»; quedan las flechas del ano y las opciones.
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertNotIn('data-gritmap-btn="today"', html)
        self.assertIn('data-gritmap-btn="opts"', html)

    def test_fit_to_width_like_4_1(self) -> None:
        # 4.4.0: ajustado al ancho, cuadritos de 14 en el dibujo, esquinas de
        # 2, a todo el ancho (10 px como minimo) y meses en porcentaje.
        cfg = replace(DEFAULT_CONFIG, cell_size=FIT_WIDTH, border_radius=2)
        html = view.build_widget_html(sample(), cfg, 0)
        width = view.grid_width(2026)
        self.assertEqual(width, 53 * 17 - 3)
        self.assertIn('class="gritmap-year gritmap-fit"', html)
        self.assertIn(f'<svg viewBox="0 0 {width} 116" style="min-width:{width * 10 / 14:.0f}px" xmlns=', html)
        self.assertRegex(html, r'<rect class="gritmap-cell" x="\d+" y="\d+" width="14" height="14" rx="2"')
        self.assertRegex(html, r'class="gritmap-month"[^>]*style="left:[\d.]+%"')
        self.assertIn("aspect-ratio:", view.placeholder_html(cfg))

    def test_no_period_buttons_on_the_page(self) -> None:
        # El periodo se elige en Opciones (cliente, 2026-10-21); las tarjetas lo dicen.
        html = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, avg_window=365), 0)
        self.assertNotIn("gritmap-period", html)
        self.assertIn("último año", html)

    def test_average_card(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        card = html[html.index(">Promedio diario<"):html.index(">Retención<")]
        # 4.10.0: una sola medida, tarjetas distintas.
        self.assertIn('data-n="900"', card)
        self.assertIn("tarjetas", card)
        self.assertIn("últimos 30 días", card)
        # Regla de FIX-010: sin dias completos, N/A con el motivo en el globo.
        empty = view.build_widget_html(sample(past={0: DayActivity(5, 5, 1)}), DEFAULT_CONFIG, 0)
        card = empty[empty.index(">Promedio diario<"):empty.index(">Retención<")]
        self.assertIn("N/A", card)
        self.assertIn("Sin días completos", card)

    def test_next_date_card_has_only_the_name(self) -> None:
        cfg = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 11, 20), "Examen"),))
        html = view.build_widget_html(sample(), cfg, 0)
        card = html[html.index(">Próxima fecha<"):]
        # 4.3.0: solo el nombre, sin la fecha al lado.
        self.assertIn('<div class="gritmap-line" title="Examen">Examen</div>', card)
        self.assertNotIn("gritmap-date", card)
        self.assertNotIn("key:", html)

    def test_fixed_size_scales_everything(self) -> None:
        # 4.5.0: con un tamano, el dibujo entero se escala (huecos y esquinas
        # en proporcion), con el mismo dibujo que el ajustado al ancho.
        # 4.6.0: el redondeo va en pixeles reales (6 px a 28 px = 3 a 14).
        fit = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, cell_size=FIT_WIDTH, border_radius=3), 0)
        html = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, cell_size=28, border_radius=6), 0)
        cells = r"<rect.*</svg>"
        self.assertEqual(re.findall(cells, fit), re.findall(cells, html))
        self.assertRegex(html, r'<rect class="gritmap-cell" x="\d+" y="\d+" width="14" height="14" rx="3"')
        self.assertIn(f'style="width:{view.grid_width(2026) * 2}px"', html)
        self.assertNotIn("gritmap-fit", html)

    def test_goal_ring_and_week_line(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        # Sin meta, la linea de Hoy da lo hecho en 7 dias.
        today = html[html.index(">Hoy<"):html.index(">Racha<")]
        self.assertIn("en 7 días", today)
        cfg = replace(DEFAULT_CONFIG, goal_mode="number", goal=8)
        goal = view.build_widget_html(sample(), cfg, 0)
        self.assertIn("gritmap-ring", goal)
        self.assertIn("faltan", goal)
        done = view.build_widget_html(sample(), replace(cfg, goal=5), 0, celebrate=True)
        self.assertIn("Meta cumplida", done)
        self.assertIn("gritmap-celebrate", done)
        # En un mazo no hay meta: es de toda la coleccion.
        deck = view.build_widget_html(sample(), cfg, 0, deck_only=True)
        self.assertIn("Hoy en este mazo", deck)
        self.assertNotIn("gritmap-ring", deck)

    def test_due_goal_uses_remaining_cards(self) -> None:
        cfg = replace(DEFAULT_CONFIG, goal_mode="due")
        self.assertEqual(view.goal_progress(sample(due_remaining=15), cfg), (5, 20))
        self.assertIsNone(view.goal_progress(sample(), cfg))

    def test_due_goal_once_met_stays_met(self) -> None:
        # Regresion de FIX-026: cumplida con 5 tarjetas, vuelven a vencer 3 en
        # aprendizaje y la meta sigue cumplida; si se deshace una, no.
        cfg = replace(DEFAULT_CONFIG, goal_mode="due")
        self.assertEqual(view.goal_progress(sample(due_remaining=3, due_reached=5), cfg), (5, 5))
        undone = sample(past={0: DayActivity(4, 4, 0)}, due_remaining=4, due_reached=5)
        self.assertEqual(view.goal_progress(undone, cfg), (4, 5))

    def test_pause_is_visible_in_streak_card(self) -> None:
        # 4.7.0: mientras dure, «en pausa hasta el …» en la linea de Racha.
        cfg = replace(DEFAULT_CONFIG, pause=(date(2026, 10, 12), date(2026, 11, 5)))
        html = view.build_widget_html(sample(), cfg, 0)
        card = html[html.index(">Racha<"):html.index(">Promedio diario<")]
        self.assertIn('en pausa hasta el <span class="gritmap-date" data-gritmap-date="2026-11-05">', card)
        later = replace(DEFAULT_CONFIG, pause=(date(2026, 10, 20), date(2026, 10, 25)))
        self.assertNotIn("en pausa", view.build_widget_html(sample(), later, 0))

    def test_average_shows_only_the_period_and_retention_explains_na(self) -> None:
        html = view.build_widget_html(sample(retention_days={1: (5, 4)}), DEFAULT_CONFIG, 0)
        card = html[html.index(">Promedio diario<"):html.index(">Retención<")]
        # 4.7.1: sin «por día estudiado» (cliente).
        self.assertNotIn("por día estudiado", card)
        self.assertIn('title="últimos 30 días"', card)
        retention = html[html.index(">Retención<"):]
        self.assertIn("N/A", retention)
        self.assertIn("Menos de", retention)

    def test_next_date_has_no_weekday(self) -> None:
        # 4.7.1: solo el nombre, sin el dia de la semana (cliente).
        soon = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 10, 16), "Examen"),))
        self.assertNotIn("data-gritmap-weekday", view.build_widget_html(sample(), soon, 0))
        far = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 11, 16), "Examen"),))
        self.assertNotIn("data-gritmap-weekday", view.build_widget_html(sample(), far, 0))

    def test_key_marks_are_diamonds_past_hollow(self) -> None:
        # 4.8.0: rombo de hito; las pasadas, huecas (clase kpast); una sola
        # regla a cualquier tamano, sin fila aparte.
        dates = (KeyDate(date(2026, 3, 2), "Parcial"), KeyDate(date(2026, 11, 20), "Final"))
        html = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, key_dates=dates), 0)
        self.assertEqual(html.count('class="gritmap-kmark gritmap-kpast"'), 1)
        self.assertEqual(html.count('class="gritmap-kmark"'), 1)
        self.assertEqual(view.diamond_points(7, 7, 2), "7.00,5.00 9.00,7.00 7.00,9.00 5.00,7.00")
        small = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, cell_size=10, key_dates=dates), 0)
        self.assertNotIn("gritmap-small", small)
        self.assertNotIn("gritmap-kstar", small)

    def test_weekdays_corner_button_and_soft_disabled_arrows(self) -> None:
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertEqual(re.findall(r'data-gritmap-dayname="(\d)"', html), ["0", "2", "4"])
        self.assertIn('data-gritmap-btn="opts" data-gritmap-corner="1"', html)
        # Las flechas apagadas conservan su nombre y no envian nada.
        self.assertIn('data-gritmap-btn="next" aria-disabled="true"', html)
        self.assertNotIn(" disabled", html)

    def test_hidden_streak_and_goal(self) -> None:
        html = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, show_streak=False), 0)
        # Sin racha ni meta y sin fechas clave por venir: tres (4.8.0).
        self.assertEqual(html.count('class="gritmap-card gritmap-mini"'), 3)
        self.assertNotIn(">Racha<", html)

    def test_streak_card_lines(self) -> None:
        stats = view.full_stats(sample())
        card = view._streak_card(replace(stats, current_streak=12, longest_streak=15, today_done=False), DEFAULT_CONFIG, TODAY)
        self.assertIn("hoy pendiente", card)
        self.assertIn("del récord", card)
        back = view._streak_card(replace(stats, current_streak=1, longest_streak=45, previous_best=45), DEFAULT_CONFIG, TODAY)
        self.assertIn("Día 1", back)
        # «récord» en minuscula (cliente, 2026-10-21).
        self.assertIn("récord:", back)
        self.assertNotIn("Récord", back)
        far = view._streak_card(replace(stats, current_streak=3, longest_streak=40), DEFAULT_CONFIG, TODAY)
        self.assertIn("récord:", far)
        # 4.7.0: «a 2 días del récord» solo si el récord es de 7 días o más.
        short = view._streak_card(replace(stats, current_streak=2, longest_streak=4), DEFAULT_CONFIG, TODAY)
        self.assertNotIn("del récord", short)
        freezes = view._streak_card(replace(stats, current_streak=9, longest_streak=9, freezes_left=1), DEFAULT_CONFIG, TODAY)
        self.assertIn('data-n="1">1</span> comodín', freezes)

    def test_retention_card_with_fsrs_target(self) -> None:
        html = view.build_widget_html(sample(fsrs_target=0.9), DEFAULT_CONFIG, 0, deck_only=True)
        # 4.10.0: el objetivo va en el globo del porcentaje, no en la linea.
        card = html[html.index(">Retención<"):]
        card = card[:card.index("</section>")]
        line = card[card.index('class="gritmap-line"'):]
        self.assertIn("Objetivo", card)
        self.assertIn("data-gritmap-info", card)
        self.assertNotIn("objetivo", line.lower())
        self.assertIn('data-p="90"', html)

    def test_next_date_card_only_with_upcoming_dates(self) -> None:
        # 4.8.0: sin fechas de hoy en adelante, no hay tarjeta (cuatro).
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        self.assertNotIn(">Próxima fecha<", html)
        self.assertIn("gritmap-n4", html)
        past = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2026, 3, 2), "Parcial"),))
        self.assertNotIn(">Próxima fecha<", view.build_widget_html(sample(), past, 0))
        # Sin racha ni meta y sin fechas, tres.
        hidden = view.build_widget_html(sample(), replace(DEFAULT_CONFIG, show_streak=False), 0)
        self.assertIn("gritmap-n3", hidden)
        today = replace(DEFAULT_CONFIG, key_dates=(KeyDate(TODAY, "Examen"),))
        self.assertIn(">Próxima fecha<", view.build_widget_html(sample(), today, 0))

    def test_pending_days_in_three_soft_greys(self) -> None:
        # 4.8.0 (cliente): tres grises mas suaves que el primer tono del tema.
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        levels = set(re.findall(r'fill="var\(--gritmap-f(\d+)\)"', html))
        self.assertTrue(levels and levels <= {"1", "2", "3"}, levels)
        self.assertNotIn("gritmap-dot", html)
        css = palettes.palette_css("classic_green")
        self.assertIn("--gritmap-f3:", css)
        self.assertNotIn("--gritmap-f4:", css)

    def test_forgiven_day_is_dashed(self) -> None:
        past = {d: DayActivity(5, 5, 0) for d in range(2, 12)}
        html = view.build_widget_html(sample(past=past), DEFAULT_CONFIG, 0)
        self.assertRegex(html, r'class="gritmap-cell gritmap-forgiven"[^>]*data-d="2026-10-12"')
        self.assertIn("Perdonado", html)

    def test_tooltip_texts_have_no_date(self) -> None:
        # La fecha va en su propia linea, la pone el navegador (peticion del cliente).
        # «en pausa hasta el {date}» (4.7.0) no es un globo: es la linea de la
        # tarjeta Racha, y la fecha tambien la pone el navegador.
        for code, texts in i18n.STRINGS.items():
            for key, text in texts.items():
                if key != "paused_until":
                    self.assertNotIn("{date}", text, f"{code}.{key}")

    def test_all_injected_names_start_with_gritmap(self) -> None:
        # Regla de FIX-008.
        html = view.build_widget_html(sample(), DEFAULT_CONFIG, 0)
        for name in re.findall(r'class="([^"]+)"', html.replace("&quot;", '"')):
            for part in name.split():
                self.assertTrue(part.startswith("gritmap"), part)
        for attr in re.findall(r"\sdata-([a-z-]+)=", html):
            self.assertTrue(attr.startswith("gritmap") or attr in ("d", "v", "t", "n", "p"), attr)

    def test_excluded_deck_and_empty_collection(self) -> None:
        excluded = view.build_widget_html(sample(deck_excluded=True), DEFAULT_CONFIG, 0)
        self.assertIn("Este mazo está excluido del mapa.", excluded)
        self.assertIn('data-gritmap-cmd="opts"', excluded)
        empty = view.build_widget_html(sample(past={}, future_counts={}), DEFAULT_CONFIG, 0)
        self.assertIn("Cada día que estudie se pintará aquí.", empty)
        self.assertRegex(empty, r'data-d="2026-10-13"[^>]*data-gritmap-today="1"')
        self.assertLess(empty.index("gritmap-activity"), empty.index('class="gritmap-summary'))
        self.assertNotIn("gritmap-legend", empty)

    def test_legend_ranges_cover_every_count(self) -> None:
        thresholds = palettes.legend_thresholds(40.0)
        ranges = view.legend_ranges(thresholds)
        self.assertEqual(len(ranges), palettes.LEVELS)
        self.assertEqual(ranges[0][0], 1)
        self.assertIsNone(ranges[-1][1])
        for count in range(1, 400):
            group = next(i for i, (low, high) in enumerate(ranges) if count >= low and (high is None or count <= high))
            self.assertEqual(palettes.level_index(count, thresholds), group, count)

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

    def test_placeholder_reserves_the_cards(self) -> None:
        page = view.placeholder_html(DEFAULT_CONFIG)
        self.assertIn("gritmap-bone-grid", page)
        # Sin fechas clave por venir, cuatro tarjetas (4.8.0); con una, cinco.
        self.assertEqual(page.count('class="gritmap-card gritmap-mini"'), 4)
        soon = replace(DEFAULT_CONFIG, key_dates=(KeyDate(date(2100, 1, 1), "Examen"),))
        self.assertEqual(view.placeholder_html(soon).count('class="gritmap-card gritmap-mini"'), 5)

    def test_payload_has_no_goal_line_for_the_map(self) -> None:
        # «Meta cumplida» ya no sale en el globo del mapa (cliente, 2026-10-21).
        data = json.loads(view.payload_json("", "reviews"))
        self.assertNotIn("goal", data)
        self.assertNotIn("goal_met", data["texts"])
        self.assertEqual(data["texts"]["click_past"], "Pulse para ver estas tarjetas")
        self.assertEqual(data["texts"]["forgiven_freeze"], "Perdonado con un comodín")

    def test_palette_has_four_tones_per_theme(self) -> None:
        css = palettes.palette_css("classic_green")
        self.assertIn("--gritmap-p4:", css)
        self.assertNotIn("--gritmap-p5", css)
        for scales in (palettes.PAST_LIGHT, palettes.PAST_DARK):
            self.assertEqual(set(scales), set(palettes.THEME_NAMES))
            for tones in scales.values():
                self.assertEqual(len(tones), palettes.LEVELS)
        # 4.10.0: vuelven Rosa suave y Turquesa laguna.
        self.assertEqual(len(palettes.THEME_NAMES), 6)


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
