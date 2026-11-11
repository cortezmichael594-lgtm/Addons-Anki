"""Pruebas de la configuración y de las hojas de estilo que genera cada paleta
(páginas web y ventanas Qt), sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path

from aqt.theme import WidgetStyle

from nocturne import config, themes, theming, webview_style
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
        for ease, value in (
            (1, "var(--accent-danger)"),
            (2, "color-mix(in srgb, var(--flag-2) 85%, var(--fg))"),
            (3, "var(--state-review)"),
            (4, "var(--state-new)"),
        ):
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
            self.assertIn(
                ":is(.nobold, .stattxt) { color: var(--fg-subtle); font-variant-numeric: tabular-nums; }", css, theme_id
            )
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

    def test_report_3_7_deck_list(self) -> None:
        # Versión 3.8.0 (informe del 2026-11-04): barra superior en seminegrita, línea de
        # «Estudiadas...» en el secundario, esquinas pequeñas en la fila resaltada y en los
        # botones de la barra inferior, hueco bajo la cabecera y rótulos alineados. Todo
        # limitado a sus propios elementos (regla de FIX-006).
        for theme_id in themes.THEMES:
            css = self.css_for(theme_id)
            self.assertIn(".toolbar .hitem { font-weight: 600; }", css, theme_id)
            self.assertIn("#studiedToday { color: var(--fg-subtle); }", css, theme_id)
            self.assertIn("tr.deck > td { --border-radius-medium: var(--nocturne-control-radius); }", css, theme_id)
            self.assertIn("center#outer > table#header button { border-radius: var(--nocturne-control-radius); }", css)
            self.assertIn("table:has(tr.deck) tr.top-level-drag-row > td { padding-block: 0; height: 10px;", css)
            self.assertIn("table:has(tr.deck) th { padding-inline: 12px; }", css, theme_id)
            self.assertIn(".label-container .label-name { color: var(--fg-subtle); }", css, theme_id)
            # La barra del repaso (botones de respuesta) no lleva esa esquina.
            self.assertNotIn("#innertable", css, theme_id)

    def test_report_3_8_pages(self) -> None:
        # Versión 3.9.0 (informe del 2026-11-11, apartado 8): bordes, esquinas y alturas de los
        # botones de las páginas, ceros sin color, editor, engranaje y degradado fuera de las barras.
        for theme_id in themes.THEMES:
            css = self.css_for(theme_id)
            page = f"html body:not(.card) {webview_style._PAGE_BUTTON}"
            self.assertIn(f"{page} {{ border-color: var(--nocturne-control-border); }}", css)
            self.assertIn(f"{page}:hover {{ border-color: var(--button-hover-border); }}", css)
            self.assertIn("background: var(--nocturne-button-pressed);", css)
            # Ningún botón en píldora: los de respuesta y «Comenzar a estudiar», con la de botones.
            self.assertIn("button:is(:not([class]), .but) { border-radius: var(--nocturne-control-radius); }", css)
            self.assertIn("min-height: 36px; min-width: 96px; margin-inline: 8px; font-size: 1rem;", css)
            self.assertIn("button#study { box-sizing: border-box; min-height: 36px;", css)
            self.assertIn(f"{page}[data-ease] {{ border-bottom-color: transparent; }}", css)
            self.assertIn("center > h3 { font-size: calc(1rem * 4 / 3); }", css)
            self.assertIn(".zero-count { color: var(--fg-faint); }", css)
            self.assertIn(":is(.editor-field, .tag-editor) { border-color: var(--nocturne-control-border); }", css)
            self.assertIn("img.gears { opacity: 1; filter: none;", css)
            self.assertIn("background: var(--fg-subtle);", css)
            # El selector de los botones no lleva un id: pesaría más que las reglas de cada estado.
            self.assertNotIn("#", webview_style._PAGE_BUTTON)

    def test_glow_only_on_page_backgrounds(self) -> None:
        # Versión 3.9.0 (informe, apartado 8.7): el degradado no entra en las barras ni en el
        # repaso, y sigue anclado a la ventana (FIX-001).
        css = self.css_for("nocturne")
        glow = css[css.index("radial-gradient") - 120 : css.index("radial-gradient")]
        self.assertIn(":not(:has(#outer, .toolbar))", glow)
        self.assertIn("background-attachment: fixed", css)

    def test_zero_counts_on_the_deck_screen(self) -> None:
        # Versión 3.9.0 (informe, apartado 4.4): «Aprendiendo: 0» iba en rojo.
        table = (
            "<span class=new-count>2</span><span class=learn-count>0</span>"
            "<span class=review-count>10</span><span class=review-count>0</span>"
        )
        content = types.SimpleNamespace(table=table)
        webview_style.on_overview_content(None, content)
        self.assertEqual(
            content.table,
            '<span class=new-count>2</span><span class="learn-count zero-count">0</span>'
            '<span class=review-count>10</span><span class="review-count zero-count">0</span>',
        )

    def test_editor_text_in_the_text_color(self) -> None:
        # Regresión de FIX-015: Anki fija «anki-editable { color: white }» dentro de cada campo;
        # la regla de la paleta entra en esa zona aislada, con más peso y var(--fg).
        script = webview_style._install_js("x", guard_existing=False)
        self.assertIn(":host anki-editable { color: var(--fg); }", script)
        self.assertIn("Element.prototype.attachShadow = function", script)
        self.assertIn("querySelectorAll('.rich-text-editable')", script)
        self.assertIn("if (!window.nocturneEditable", script)  # una sola vez por página

    def test_switching_changes_the_css(self) -> None:
        first = self.css_for("papel")
        second = self.css_for("nocturne")
        self.assertNotEqual(first, second)
        self.assertIn(themes.THEMES["nocturne"]["colors"]["CANVAS"]["light"], second)


class QtStyleTest(unittest.TestCase):
    """Lo que el complemento añade a la hoja de estilo de las ventanas."""

    def setUp(self) -> None:
        self._mw, self._tm = theming.mw, theming.theme_manager
        # Los iconos repintados, en una carpeta temporal y no dentro del complemento.
        self._icons, self._tmp = theming._ICON_DIR, tempfile.TemporaryDirectory()
        theming._ICON_DIR = Path(self._tmp.name) / "iconos"
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.ANKI)
        )

    def tearDown(self) -> None:
        theming.mw, theming.theme_manager = self._mw, self._tm  # type: ignore[assignment]
        theming._ICON_DIR = self._icons
        self._tmp.cleanup()
        themes.select("nocturne")

    def test_icons_take_palette_colors(self) -> None:
        # Versión 3.8.0: flechas en el texto secundario y marca blanca en la casilla marcada.
        sheet = self.qss("lavanda", True)
        subtle = themes.THEMES["lavanda"]["colors"]["FG_SUBTLE"]["dark"]
        arrow = theming._ICON_DIR / f"chevron-down-{subtle[1:].lower()}.svg"
        self.assertTrue(arrow.exists())
        self.assertIn(f'fill="{subtle}"', arrow.read_text(encoding="utf-8"))
        self.assertIn(f"QComboBox::down-arrow {{\n        image: url({arrow.as_posix()});", sheet)
        self.assertTrue((theming._ICON_DIR / "check-ffffff.svg").exists())
        # Un color que no sea hexadecimal no se usa: quedan los iconos de Anki.
        self.assertEqual(theming._tinted_icon("chevron-down", "rgba(1, 2, 3, 0.5)"), "")
        self.assertEqual(theming._tinted_icon("no-existe", "#123456"), "")

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
                # Versión 3.9.0 (informe del 2026-11-11, apartado 2.4): el borde fuerte; el
                # suave no se distinguía del propio globo (1,06:1).
                self.assertIn(f"border: 1px solid {to_css_rgba(colors['BORDER_STRONG'][mode])};", tooltip, theme_id)
                self.assertIn("padding: 6px 8px;", tooltip, theme_id)

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

    def test_primary_fill_only_in_button_row(self) -> None:
        # Versión 3.8.0 (informe del 2026-11-04, apartado 2.1): en Preferencias salía relleno
        # «Restablecer tamaños de las ventanas». Solo el de la fila de botones del pie.
        for theme_id in themes.THEMES:
            sheet = self.qss(theme_id, True)
            added = sheet[len("/* hoja de Anki */") :]
            for index in [i for i in range(len(added)) if added.startswith("QPushButton:default", i)]:
                self.assertTrue(added[:index].endswith("QDialogButtonBox "), theme_id)

    def test_tabs_fields_table_and_checkbox(self) -> None:
        # Versión 3.8.0: pestaña activa con tinte y raya (sin cambiar de tamaño), campos con
        # borde visible, fila seleccionada opaca y casilla marcada rellena.
        for theme_id, data in themes.THEMES.items():
            for night, mode in ((False, "light"), (True, "dark")):
                sheet = self.qss(theme_id, night)
                colors = data["colors"]
                tab = sheet[sheet.index("QTabBar::tab:selected,") :]
                tab = tab[: tab.index("}")]
                self.assertIn(f"background: {to_css_rgba(colors['NOCTURNE_ROW_HIGHLIGHT'][mode])};", tab)
                self.assertIn(f"border-bottom: 2px solid {to_css_rgba(colors['BORDER_FOCUS'][mode])};", tab)
                self.assertIn("padding-bottom: 3px;", tab)
                self.assertNotIn("font-weight", tab)
                fields = sheet[sheet.index("QLineEdit,\n    QComboBox,\n    QComboBox:!editable,") :]
                border = to_css_rgba(colors["NOCTURNE_CONTROL_BORDER"][mode])
                self.assertIn(f"border-color: {border};", fields[: fields.index("}")], theme_id)
                self.assertIn("QComboBox QLineEdit {\n        border-color: transparent;", sheet)
                selected = to_css_rgba(colors["NOCTURNE_TABLE_SELECTED"][mode])
                self.assertIn(f"selection-background-color: {selected};", sheet, theme_id)
                checked = sheet[sheet.index("QCheckBox::indicator:checked:!disabled {") :]
                self.assertIn(f"background: {to_css_rgba(colors['BUTTON_PRIMARY_BG'][mode])};", checked)

    def test_report_3_8_window_controls(self) -> None:
        # Versión 3.9.0 (informe del 2026-11-11, apartado 8.6): botones con el borde de control,
        # pestañas inactivas sin relleno, el anillo del botón principal solo con el foco y el
        # tirador de la barra de desplazamiento de 8 px.
        for theme_id, data in themes.THEMES.items():
            for night, mode in ((False, "light"), (True, "dark")):
                sheet = self.qss(theme_id, night)
                colors = data["colors"]

                def rule(selector: str, sheet: str = sheet) -> str:
                    start = sheet.index(selector + " {")
                    return sheet[start : sheet.index("}", start)]

                values = {name: to_css_rgba(entry[mode]) for name, entry in colors.items()}

                def pick(name: str, values: dict[str, str] = values) -> str:
                    return values[name]

                self.assertIn(
                    f"QPushButton {{\n        border-color: {pick('NOCTURNE_CONTROL_BORDER')};\n        min-height: 22px;",
                    sheet,
                )
                self.assertIn(
                    f"border-color: {pick('BUTTON_HOVER_BORDER')};", rule("QPushButton:hover:!focus:!default")
                )
                self.assertIn(f"background: {pick('NOCTURNE_BUTTON_PRESSED')};", rule("QPushButton:pressed:!default"))
                self.assertIn(f"border-color: {pick('BORDER')};", rule("QPushButton:disabled"))
                inactive = rule("QTabBar::tab:!selected")
                self.assertIn("background: transparent;", inactive)
                self.assertIn(f"color: {pick('FG_SUBTLE')};", inactive)
                hover = rule("QDialogButtonBox QPushButton:default:hover")
                self.assertNotIn(pick("NOCTURNE_PRIMARY_RING"), hover, theme_id)
                self.assertIn(pick("NOCTURNE_PRIMARY_RING"), rule("QDialogButtonBox QPushButton:default:focus"))
                self.assertIn(f"placeholder-text-color: {pick('FG_FAINT')};", sheet)
                self.assertIn(f"border-color: {pick('BORDER_STRONG')};", rule("QMenu"))
                self.assertIn("padding: 0px 2px;", rule("QScrollBar:vertical"))

    def test_other_widget_styles_untouched(self) -> None:
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.NATIVE)
        )
        self.assertEqual(self.qss("papel", False), "/* hoja de Anki */")


if __name__ == "__main__":
    unittest.main()
