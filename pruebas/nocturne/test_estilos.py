"""Pruebas de la configuración y de las hojas de estilo que genera cada paleta
(páginas web y ventanas Qt), sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import types
import unittest

from aqt.theme import WidgetStyle
from nocturne import config, theming, themes, webview_style
from nocturne.palette import to_css_rgba


class ConfigTest(unittest.TestCase):
    """Una configuración antigua, vacía o escrita a mano nunca rompe: vuelve a Nocturne."""

    def test_valid_palette_is_kept(self) -> None:
        for theme_id in themes.THEMES:
            self.assertEqual(config.palette_from({"palette": theme_id}), theme_id)

    def test_bad_values_fall_back_to_nocturne(self) -> None:
        for value in (None, {}, {"palette": "rosa"}, {"palette": 3}, [], "papel", {"otra": "papel"}):
            self.assertEqual(config.palette_from(value), "nocturne", repr(value))

    def test_welcome_only_once(self) -> None:
        # Versión 3.5.0: el aviso de bienvenida sale una sola vez.
        self.assertEqual(config.notice_for({"palette": "papel"}), "welcome")
        self.assertEqual(config.notice_for(None), "welcome")
        # Versión 3.7.0: quien vio la bienvenida de Nocturne recibe una vez el aviso de nombre.
        self.assertEqual(config.notice_for({"palette": "papel", "welcome_shown": True}), "renamed")
        self.assertIsNone(config.notice_for({"welcome_shown": True, "renamed_shown": True}))
        self.assertEqual(config.palette_from({"palette": "papel", "welcome_shown": True}), "papel")

    def test_select_validates(self) -> None:
        try:
            self.assertEqual(themes.select("inexistente"), "nocturne")
            self.assertEqual(themes.select("bosque"), "bosque")
            self.assertEqual(themes.current_id(), "bosque")
        finally:
            themes.select("nocturne")


class WebStyleTest(unittest.TestCase):
    def css_for(self, theme_id: str) -> str:
        themes.select(theme_id)
        webview_style.reset()
        return webview_style._css_text()

    def tearDown(self) -> None:
        themes.select("nocturne")
        webview_style.reset()

    def test_each_palette_brings_its_colors_and_corners(self) -> None:
        for theme_id, data in themes.THEMES.items():
            css = self.css_for(theme_id)
            self.assertIn(f"--canvas: {data['colors']['CANVAS']['light']};", css, theme_id)
            self.assertIn(f"--canvas: {data['colors']['CANVAS']['dark']};", css, theme_id)
            self.assertIn(f"--border-radius: {data['look']['radius']}px;", css, theme_id)
            self.assertIn(f"--border-radius-large: {data['look']['radius_large']}px;", css, theme_id)
            self.assertIn("--nocturne-row-highlight:", css, theme_id)
            self.assertNotIn("None", css, theme_id)

    def test_gradient_stays_anchored(self) -> None:
        # Regresión de FIX-001: el degradado del fondo va siempre anclado a la ventana.
        for theme_id, data in themes.THEMES.items():
            css = self.css_for(theme_id)
            if data["look"]["gradient"] is None:
                self.assertNotIn("radial-gradient", css, theme_id)
            else:
                self.assertIn("radial-gradient", css, theme_id)
                self.assertIn("background-attachment: fixed", css, theme_id)

    def test_typography(self) -> None:
        papel = self.css_for("papel")
        self.assertIn("font-family: Georgia", papel)
        nocturne = self.css_for("nocturne")
        self.assertNotIn("Georgia", nocturne)
        self.assertIn("font-variant-numeric: tabular-nums", nocturne)
        self.assertIn("letter-spacing: -0.01em", nocturne)

    def test_row_highlight_only_in_deck_list(self) -> None:
        # Regresión de FIX-006: el resaltado de filas de la lista de mazos alcanzaba
        # la tabla de datos de la pantalla de estudio (sus filas no son de mazos).
        for theme_id in themes.THEMES:
            css = self.css_for(theme_id)
            self.assertNotIn("tr:hover:not(.top-level-drag-row)) td", css, theme_id)
            self.assertNotIn("tr[id] > td", css, theme_id)
            self.assertIn("tr.deck:is(.current, :hover) > td", css, theme_id)
            self.assertIn("tr.deck > td { padding-block:", css, theme_id)

    def test_toolbar_and_answer_buttons(self) -> None:
        css = self.css_for("nocturne")
        self.assertIn(".toolbar .hitem:hover", css)
        for ease, value in ((1, "var(--accent-danger)"), (2, "color-mix(in srgb, var(--flag-2) 85%, var(--fg))"),
                            (3, "var(--state-review)"), (4, "var(--state-new)")):
            self.assertIn(f"button[data-ease='{ease}'] {{ background-image: linear-gradient(to top, {value}", css)
            self.assertIn(f"button[data-ease='{ease}']:hover", css)
        # Regresión de FIX-010: la raya no se repite arriba del botón.
        self.assertIn("background-repeat: no-repeat; }", css)

    def test_quick_transitions_and_quiet_labels(self) -> None:
        # Versión 3.3.0: respuesta en 100 ms y etiquetas en el texto secundario, cada
        # regla limitada a su propia tabla (regla de FIX-006).
        css = self.css_for("bosque")
        self.assertIn(f"--transition: {webview_style.TRANSITION_MS}ms;", css)
        self.assertLessEqual(webview_style.TRANSITION_MS, 150)
        self.assertNotIn("--transition-medium", css)
        self.assertIn("table:has(tr.deck) th { color: var(--fg-subtle);", css)
        self.assertIn("tr:has(> td > b > :is(.new-count, .learn-count, .review-count)) > td:first-child", css)
        self.assertNotIn(" th { color", css.replace("table:has(tr.deck) th { color", ""))

    def test_reading_polish(self) -> None:
        # Versión 3.4.0: títulos equilibrados, descripción sin palabras sueltas, un solo
        # color de acción en los controles nativos y nada de transiciones con «Reducir
        # movimiento».
        for theme_id in themes.THEMES:
            css = self.css_for(theme_id)
            self.assertIn(":is(h1, h2, h3) { text-wrap: balance; }", css, theme_id)
            self.assertIn("text-wrap: pretty;", css, theme_id)
            self.assertIn("accent-color: var(--border-focus);", css, theme_id)
            self.assertIn("@media (prefers-reduced-motion: reduce)", css, theme_id)
            self.assertIn(":is(.nobold, .stattxt) { color: var(--fg-subtle); font-variant-numeric: tabular-nums; }", css, theme_id)
            self.assertIn("html body.reduce-motion:not(.card) { --transition: 0ms; }", css, theme_id)
            # Foco visible también en enlaces y en la barra superior (Anki lo oculta allí).
            self.assertIn("a:focus-visible { outline:", css, theme_id)
            self.assertIn("text-underline-offset: 0.18em;", css, theme_id)

    def test_quiet_review_side_buttons(self) -> None:
        css = self.css_for("nocturne")
        self.assertIn("td.stat > button { background: transparent; border-color: transparent;", css)
        self.assertIn("--nocturne-control-radius:", css)
        self.assertIn("--nocturne-control-border:", css)

    def test_deck_table_same_material_as_cards(self) -> None:
        for theme_id in themes.THEMES:
            css = self.css_for(theme_id)
            self.assertIn("table:has(tr.deck) { background: var(--canvas-elevated); }", css, theme_id)

    def test_switching_changes_the_css(self) -> None:
        first = self.css_for("papel")
        second = self.css_for("nocturne")
        self.assertNotEqual(first, second)
        self.assertIn(themes.THEMES["nocturne"]["colors"]["CANVAS"]["light"], second)


class QtStyleTest(unittest.TestCase):
    """Lo que el complemento añade a la hoja de estilo de las ventanas."""

    def setUp(self) -> None:
        self._mw, self._tm = theming.mw, theming.theme_manager
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.ANKI)
        )

    def tearDown(self) -> None:
        theming.mw, theming.theme_manager = self._mw, self._tm  # type: ignore[assignment]
        themes.select("nocturne")

    def qss(self, theme_id: str, night: bool) -> str:
        themes.select(theme_id)
        theming.theme_manager = types.SimpleNamespace(night_mode=night)  # type: ignore[assignment]
        return theming.on_style_did_init("/* hoja de Anki */")

    def test_keeps_anki_sheet_and_adds_rules(self) -> None:
        sheet = self.qss("nocturne", False)
        self.assertTrue(sheet.startswith("/* hoja de Anki */"))
        self.assertIn("QCheckBox::indicator", sheet)
        self.assertIn("QPushButton:default", sheet)

    def test_primary_button_and_corners_follow_the_palette(self) -> None:
        for theme_id, data in themes.THEMES.items():
            for night, mode in ((False, "light"), (True, "dark")):
                sheet = self.qss(theme_id, night)
                colors = data["colors"]
                self.assertIn(f"border-radius: {data['look']['button_radius']}px;", sheet, theme_id)
                self.assertIn(f"background: {to_css_rgba(colors['BUTTON_PRIMARY_BG'][mode])};", sheet, theme_id)
                self.assertIn(f"border-color: {to_css_rgba(colors['NOCTURNE_CONTROL_BORDER'][mode])};", sheet, theme_id)

    def test_tooltips_float_like_menus(self) -> None:
        for theme_id, data in themes.THEMES.items():
            for night, mode in ((False, "light"), (True, "dark")):
                sheet = self.qss(theme_id, night)
                tooltip = sheet[sheet.index("QToolTip {") :]
                colors = data["colors"]
                self.assertIn(f"background-color: {to_css_rgba(colors['CANVAS_OVERLAY'][mode])};", tooltip, theme_id)
                self.assertIn(f"border: 1px solid {to_css_rgba(colors['BORDER_SUBTLE'][mode])};", tooltip, theme_id)

    def test_same_corner_for_buttons_and_fields(self) -> None:
        # Versión 3.5.0: botones y campos con la misma esquina; casillas, 4 px.
        for theme_id, data in themes.THEMES.items():
            sheet = self.qss(theme_id, False)
            radius = data["look"]["button_radius"]
            fields = sheet[sheet.index("QComboBox,\n    QSpinBox,") :]
            self.assertIn(f"border-radius: {radius}px;", fields[: fields.index("}")], theme_id)
            self.assertIn("QMenu::indicator:non-exclusive {\n        border-radius: 4px;", sheet, theme_id)

    def test_one_way_to_mark_selection(self) -> None:
        # Versión 3.7.0: menús y listas desplegables con el tinte de acción y texto normal.
        for theme_id, data in themes.THEMES.items():
            sheet = self.qss(theme_id, True)
            colors = data["colors"]
            part = sheet[sheet.index("QMenu::item:selected,") :]
            self.assertIn(f"background-color: {to_css_rgba(colors['NOCTURNE_ROW_HIGHLIGHT']['dark'])};", part, theme_id)
            self.assertIn(f"color: {to_css_rgba(colors['FG']['dark'])};", part, theme_id)

    def test_other_widget_styles_untouched(self) -> None:
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.NATIVE)
        )
        self.assertEqual(self.qss("papel", False), "/* hoja de Anki */")


if __name__ == "__main__":
    unittest.main()
