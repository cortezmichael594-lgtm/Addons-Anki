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

    def test_select_validates(self) -> None:
        try:
            self.assertEqual(themes.select("inexistente"), "nocturne")
            self.assertEqual(themes.select("grafito"), "grafito")
            self.assertEqual(themes.current_id(), "grafito")
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

    def test_other_widget_styles_untouched(self) -> None:
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.NATIVE)
        )
        self.assertEqual(self.qss("papel", False), "/* hoja de Anki */")


if __name__ == "__main__":
    unittest.main()
