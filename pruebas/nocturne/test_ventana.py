"""Pruebas de la ventana de configuración, de sus textos y del color de la barra
de título, con Qt sin pantalla (QT_QPA_PLATFORM=offscreen) y sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path

import anki.lang
from aqt.qt import (
    QApplication,
    QColor,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    Qt,
    QVBoxLayout,
    QWidget,
)
from aqt.theme import WidgetStyle

from nocturne import contrast, dialogs, errors, panel, strings, themes, theming, titlebar

_app = QApplication.instance() or QApplication([])
anki.lang.set_lang("es")  # el título de la ventana sale de las traducciones de Anki


class OwnerWindowTest(unittest.TestCase):
    """Regresión de FIX-007: la ventana de paletas se abría con la ventana principal
    de padre y quedaba detrás de la de complementos, que es desde donde se pide."""

    def setUp(self) -> None:
        self._mw = dialogs.mw
        self._panel_class = panel.PanelDialog
        self.main = QMainWindow()
        self.addons = QDialog(self.main)  # hace de ventana de complementos
        self.addons.show()
        dialogs.mw = types.SimpleNamespace(  # type: ignore[assignment]
            app=types.SimpleNamespace(activeWindow=lambda: self.addons)
        )

        # Sin navegador en las pruebas: el panel falla al crearse y se abre la ventana
        # sencilla, que es la salida de emergencia (versión 3.7.0).
        def no_panel(owner: QWidget, on_timeout: object) -> QDialog:
            raise RuntimeError("sin página en las pruebas")

        panel.PanelDialog = no_panel  # type: ignore[assignment,misc]

    def tearDown(self) -> None:
        if dialogs._dialog is not None:
            dialogs._dialog.reject()
        dialogs.mw = self._mw  # type: ignore[assignment]
        panel.PanelDialog = self._panel_class  # type: ignore[misc]
        dialogs._dialog = None
        errors._failures = 0
        self.addons.close()
        self.main.close()
        themes.select("nocturne")

    def test_opens_over_the_window_that_asks(self) -> None:
        dialogs.open_dialog()
        dialog = dialogs._dialog
        self.assertIsNotNone(dialog)
        assert dialog is not None
        self.assertIs(dialog.parentWidget(), self.addons)
        self.assertEqual(dialog.windowModality(), Qt.WindowModality.WindowModal)
        self.assertTrue(dialog.isVisible())
        # Como la configuración de cualquier complemento en Anki, y sin el botón «?».
        self.assertEqual(dialog.windowTitle(), "Atelier")
        self.assertFalse(dialog.windowFlags() & Qt.WindowType.WindowContextHelpButtonHint)

    def test_panel_opens_over_the_window_that_asks(self) -> None:
        # Con el panel, también sobre la ventana que lo pide (regla de FIX-007).
        received = []

        class FakePanel(QDialog):
            def __init__(self, owner: QWidget, on_timeout: object) -> None:
                super().__init__(owner)
                received.append(owner)

        panel.PanelDialog = FakePanel  # type: ignore[assignment,misc]
        dialogs.open_dialog()
        self.assertEqual(received, [self.addons])
        assert dialogs._dialog is not None
        self.assertIsInstance(dialogs._dialog, FakePanel)

    def test_shows_the_current_palette(self) -> None:
        themes.select("bosque")
        dialogs.open_dialog()
        assert dialogs._dialog is not None
        self.assertEqual(dialogs._dialog.selected_id(), "bosque")

    def test_restore_defaults_picks_nocturne(self) -> None:
        themes.select("papel")
        dialogs.open_dialog()
        dialog = dialogs._dialog
        assert dialog is not None
        dialog.restore_defaults()
        self.assertEqual(dialog.selected_id(), themes.DEFAULT_THEME)
        # La vista previa espera a que la elección lleve un momento quieta.
        self.assertEqual(themes.current_id(), "papel")
        self.assertTrue(dialog._timer.isActive())


class PaletteChoiceTest(unittest.TestCase):
    """Versión 3.5.0 (informe de 2026-10-26): la predeterminada marcada, vista previa y
    vuelta atrás. Versión 3.6.0: lista con muestras, como en GritMap."""

    def setUp(self) -> None:
        self.owner = QDialog()
        self._open_folder = dialogs.openFolder
        themes.select("nocturne")

    def tearDown(self) -> None:
        errors._failures = 0
        contrast._stepped_aside = False
        themes.select("nocturne")
        self.owner.close()

    def dialog(self) -> dialogs.PaletteDialog:
        return dialogs.PaletteDialog(self.owner)

    def test_list_with_swatches_like_gritmap(self) -> None:
        # Versión 3.6.0: el diseño de las opciones de GritMap, con las cinco paletas.
        dialog = self.dialog()
        combo = dialog.findChild(QComboBox)
        assert combo is not None
        names = [combo.itemText(i) for i in range(combo.count())]
        self.assertEqual(names, ["Atardecer", "Bosque", "Lavanda", "Nocturne" + strings.DEFAULT_SUFFIX, "Papel"])
        for i in range(combo.count()):
            self.assertFalse(combo.itemIcon(i).isNull(), names[i])
        texts = [label.text() for label in dialog.findChildren(QLabel)]
        self.assertIn(strings.THEME_DESCRIPTIONS["nocturne"], texts)
        self.assertIn(strings.DAY_AND_NIGHT, texts)
        self.assertNotIn(strings.HIGH_CONTRAST, texts)
        self.assertNotIn(strings.FAILURES, texts)

    def test_description_follows_the_choice(self) -> None:
        dialog = self.dialog()
        dialog.select("lavanda")
        self.assertIn(strings.THEME_DESCRIPTIONS["lavanda"], [label.text() for label in dialog.findChildren(QLabel)])

    def test_swatch_takes_the_palette_colors(self) -> None:
        for theme_id, data in themes.THEMES.items():
            canvas, _border, accent = dialogs.swatch_colors(theme_id, night=True)
            self.assertEqual(canvas, data["colors"]["CANVAS"]["dark"], theme_id)
            self.assertEqual(accent, data["colors"]["BUTTON_PRIMARY_BG"]["dark"], theme_id)

    def test_preview_then_cancel_goes_back(self) -> None:
        dialog = self.dialog()
        dialog.select("papel")
        dialog._preview()  # lo que hace el temporizador
        self.assertEqual(themes.current_id(), "papel")
        dialog.reject()
        self.assertEqual(themes.current_id(), "nocturne")

    def test_accept_keeps_the_choice(self) -> None:
        dialog = self.dialog()
        dialog.select("atardecer")
        dialog.accept()
        self.assertEqual(themes.current_id(), "atardecer")

    def test_failures_line_only_after_a_failure(self) -> None:
        errors._failures = 1
        logs = errors.logs_folder
        errors.logs_folder = lambda: "/registro"  # type: ignore[assignment]
        try:
            dialog = self.dialog()
        finally:
            errors.logs_folder = logs  # type: ignore[assignment]
        self.assertIn(strings.FAILURES, [label.text() for label in dialog.findChildren(QLabel)])
        self.assertIn(strings.OPEN_LOG, [b.text() for b in dialog.findChildren(QPushButton)])
        # Regresión de FIX-008: pulsar el botón no falla (la señal manda un dato).
        before = errors.failures()
        opened = []
        dialogs.openFolder = opened.append  # type: ignore[assignment]
        errors.logs_folder = lambda: "/registro"  # type: ignore[assignment]
        try:
            button = next(b for b in dialog.findChildren(QPushButton) if b.text() == strings.OPEN_LOG)
            button.click()
        finally:
            errors.logs_folder = logs  # type: ignore[assignment]
            dialogs.openFolder = self._open_folder  # type: ignore[assignment]
        self.assertEqual(errors.failures(), before)
        self.assertEqual(opened, ["/registro"])

    def test_high_contrast_no_preview(self) -> None:
        contrast.step_aside()
        dialog = self.dialog()
        self.assertIn(strings.HIGH_CONTRAST, [label.text() for label in dialog.findChildren(QLabel)])
        dialog.select("papel")
        self.assertFalse(dialog._timer.isActive())
        dialog.accept()
        # Se guarda (para cuando vuelva el contraste normal), pero no se pinta.
        self.assertEqual(themes.current_id(), "nocturne")

    def test_contrast_check_is_safe(self) -> None:
        self.assertIsInstance(contrast.system_wants_more_contrast(), bool)


class PanelTest(unittest.TestCase):
    """Versión 3.7.0 (informe del 2026-10-28): panel a medida con las cinco paletas a la
    vista, por orden alfabético, cada una con su miniatura de día y de noche."""

    def test_alphabetical_order(self) -> None:
        self.assertEqual(panel.ordered_ids(), ["atardecer", "bosque", "lavanda", "nocturne", "papel"])

    def test_payload_has_both_thumbnails_and_texts(self) -> None:
        data = panel.payload("bosque", night=True, failures=False, stepped_aside=False)
        self.assertEqual([p["id"] for p in data["palettes"]], panel.ordered_ids())
        self.assertEqual(data["current"], "bosque")
        self.assertEqual(data["texts"]["modeNote"], strings.MODE_NOTE_NIGHT)
        for entry in data["palettes"]:
            colors = themes.THEMES[entry["id"]]["colors"]
            self.assertEqual(entry["day"]["canvas"], colors["CANVAS"]["light"][:7])
            self.assertEqual(entry["night"]["action"], colors["BUTTON_PRIMARY_BG"]["dark"][:7])
            self.assertEqual(entry["isDefault"], entry["id"] == "nocturne")
        papel = next(p for p in data["palettes"] if p["id"] == "papel")
        self.assertIn("Georgia", papel["headingFont"])

    def test_script_safe(self) -> None:
        self.assertNotIn("</", panel._script_safe('{"a": "</script>"}'))

    def test_web_exports_are_closed(self) -> None:
        import re

        pattern = re.compile(panel.WEB_PATTERN)
        self.assertTrue(pattern.fullmatch("web/panel.css"))
        self.assertTrue(pattern.fullmatch("web/panel.js"))
        for bad in ("web/../../otro/x.js", "web/panel.css/../x.js", "web/otro.js", "web/sub/panel.js"):
            self.assertIsNone(pattern.fullmatch(bad), bad)

    def test_page_waits_for_pycmd(self) -> None:
        # Regresión de FIX-011: Anki crea pycmd tarde; la página solo lo usa cuando existe.
        import re
        from pathlib import Path

        js = (Path(panel.__file__).parent / "web" / "panel.js").read_text(encoding="utf-8")
        calls = re.findall(r"[\w.]*pycmd\(", js)
        self.assertEqual(calls, ["window.pycmd("], calls)
        self.assertIn('typeof window.pycmd !== "function"', js)

    def test_wait_cursor_is_released_once(self) -> None:
        # Versión 3.8.0 (informe del 2026-11-04, apartado 3.2): cursor de espera hasta que
        # se ve el panel; se quita una sola vez aunque se cierre después.
        dialog = panel.PanelDialog.__new__(panel.PanelDialog)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        dialog._waiting = True
        dialog._stop_waiting()
        dialog._stop_waiting()
        self.assertIsNone(QApplication.overrideCursor())

    def test_mode_note_names_the_anki_setting(self) -> None:
        # Versión 3.8.0 (informe, apartado 4.3): en Preferencias de Anki el ajuste se llama «Tema».
        for note in (strings.MODE_NOTE_DAY, strings.MODE_NOTE_NIGHT):
            self.assertIn("en Preferencias de Anki, en «Tema».", note)

    def test_report_3_8_panel(self) -> None:
        # Versión 3.9.0 (informe del 2026-11-11, apartado 8.9): Intro acepta desde la lista,
        # miniaturas con el borde fuerte, un solo contorno con el foco y botones de 88 px.
        from pathlib import Path

        web = Path(panel.__file__).parent / "web"
        js = (web / "panel.js").read_text(encoding="utf-8")
        css = (web / "panel.css").read_text(encoding="utf-8")
        self.assertIn('event.key === "Enter" && (event.ctrlKey || event.metaKey || inList())', js)
        data = panel.payload("nocturne", night=True, failures=False, stepped_aside=False)
        for entry in data["palettes"]:
            colors = themes.THEMES[entry["id"]]["colors"]
            self.assertEqual(entry["night"]["edge"], colors["BORDER_STRONG"]["dark"][:7])
        self.assertIn("border: 1px solid var(--t-edge);", css)
        focus = css[css.index(".nocturne-p-row:focus-visible {") :]
        self.assertIn("outline-offset: 0;", focus[: focus.index("}")])
        self.assertIn("min-width: 88px;", css)

    def test_chosen_border_survives_night(self) -> None:
        # Regresión de FIX-014: de noche, la regla que quita la sombra de las filas borraba la
        # segunda línea del borde de la elegida (1 px en vez de 2).
        import re
        from pathlib import Path

        css = (Path(panel.__file__).parent / "web" / "panel.css").read_text(encoding="utf-8")
        for selector, body in re.findall(r"([^{}]*?)\{([^{}]*)\}", css):
            if "night-mode" in selector and ".nocturne-p-row" in selector and "box-shadow: none" in body:
                self.assertIn(':not([aria-checked="true"])', selector)
        chosen = css[css.index('.nocturne-p-row[aria-checked="true"] {') :]
        self.assertIn("box-shadow: inset 0 0 0 1px var(--border-focus);", chosen[: chosen.index("}")])

    def test_bridge_orders(self) -> None:
        # Las órdenes de la página, sin ventana: elegir, vista previa y aceptar.
        dialog = panel.PanelDialog.__new__(panel.PanelDialog)
        self.assertTrue(callable(dialog.handle))


class PrimaryButtonRowTest(unittest.TestCase):
    """Versión 3.8.0 (informe del 2026-11-04, apartado 2.1): en Preferencias, Qt daba el
    papel de botón por defecto a «Restablecer tamaños de las ventanas» (el primero con el
    foco) y salía relleno del color de acción. Dibujado de verdad: el botón del cuerpo
    conserva su fondo y solo se rellena el de la fila de botones del pie."""

    def setUp(self) -> None:
        self._mw, self._tm = theming.mw, theming.theme_manager
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.ANKI)
        )
        theming.theme_manager = types.SimpleNamespace(night_mode=True)  # type: ignore[assignment]
        # Los iconos repintados, en una carpeta temporal y no dentro del complemento.
        self._icons, self._tmp = theming._ICON_DIR, tempfile.TemporaryDirectory()
        theming._ICON_DIR = Path(self._tmp.name) / "iconos"

    def tearDown(self) -> None:
        theming.mw, theming.theme_manager = self._mw, self._tm  # type: ignore[assignment]
        theming._ICON_DIR = self._icons
        self._tmp.cleanup()

    def test_body_button_is_not_filled(self) -> None:
        neutral = "#808080"  # colores-ok: fondo neutro de prueba
        dialog = QDialog()
        layout = QVBoxLayout(dialog)
        body = QPushButton("Restablecer tamaños de las ventanas")
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(body)
        layout.addWidget(box)
        dialog.setStyleSheet(
            f"QPushButton {{ background: {neutral}; padding: 8px 24px; }}" + theming.on_style_did_init("")
        )
        ok = box.button(QDialogButtonBox.StandardButton.Ok)
        assert ok is not None
        for button in (body, ok):
            button.setDefault(True)
            dialog.show()
            QApplication.processEvents()
            # Un punto del fondo, junto al borde izquierdo y lejos del texto.
            painted = QColor(button.grab().toImage().pixel(6, button.height() // 2)).name()
            if button is body:
                self.assertEqual(painted, neutral)
            else:
                self.assertNotEqual(painted, neutral)
            button.setDefault(False)
        dialog.close()


class DescriptionTest(unittest.TestCase):
    """Petición del cliente (2026-10-21): la misma estructura en todas: colores y botones, y
    después su forma. Versión 3.9.0 (informe del 2026-11-11, apartado 8.12): en el panel, dos
    líneas partidas por el punto, en lugar de cortadas a media frase."""

    def test_two_lines_split_at_the_period(self) -> None:
        for theme_id in themes.THEMES:
            first, second = panel.description_lines(theme_id).split("\n")
            self.assertTrue(first.endswith(".") and second.endswith("."), theme_id)
            self.assertIn("botones", first, theme_id)
            self.assertEqual(f"{first} {second}", strings.THEME_DESCRIPTIONS[theme_id])

    def test_same_structure(self) -> None:
        for theme_id in themes.THEMES:
            text = strings.THEME_DESCRIPTIONS[theme_id]
            self.assertLessEqual(len(text), 80, theme_id)
            self.assertEqual(text.count(". "), 1, theme_id)
            self.assertTrue(text.endswith("."), theme_id)
            self.assertIn("botones", text, theme_id)
            self.assertNotIn("acento", text, theme_id)
            for word in ("noche", "día"):
                self.assertNotIn(word, text.casefold(), theme_id)


class ControlSizeTest(unittest.TestCase):
    """Versión 3.9.0 (informe del 2026-11-11, apartado 8.6): en las ventanas, botones, listas,
    campos y pestañas de 28 px de alto (antes 21, 23, 26 y 27) y los botones del pie de 88 px
    de ancho. Dibujados de verdad con la hoja de Anki y la del complemento encima."""

    def setUp(self) -> None:
        self._mw, self._tm = theming.mw, theming.theme_manager
        theming.mw = types.SimpleNamespace(  # type: ignore[assignment]
            pm=types.SimpleNamespace(get_widget_style=lambda: WidgetStyle.ANKI)
        )
        self._icons, self._tmp = theming._ICON_DIR, tempfile.TemporaryDirectory()
        theming._ICON_DIR = Path(self._tmp.name) / "iconos"

    def tearDown(self) -> None:
        theming.mw, theming.theme_manager = self._mw, self._tm  # type: ignore[assignment]
        theming._ICON_DIR = self._icons
        self._tmp.cleanup()

    def test_one_height_for_window_controls(self) -> None:
        from aqt.qt import QLineEdit, QSpinBox, QTabWidget
        from aqt.stylesheets import CustomStyles
        from aqt.theme import theme_manager

        styles = CustomStyles()
        parts = ("general", "button", "checkbox", "menu", "combobox", "tabwidget", "table", "spinbox", "scrollbar")
        anki_sheet = "".join(getattr(styles, name)(theme_manager) for name in parts)  # el orden de Anki
        theming.theme_manager = types.SimpleNamespace(night_mode=True)  # type: ignore[assignment]
        window = QWidget()
        window.setStyleSheet(anki_sheet + theming.on_style_did_init(""))
        layout = QVBoxLayout(window)
        button, combo, spin, line = QPushButton("Cerrar"), QComboBox(), QSpinBox(), QLineEdit()
        combo.addItem("Español")
        editable = QComboBox()
        editable.setEditable(True)
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Apariencia")
        tabs.addTab(QWidget(), "Repasar")
        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        for widget in (button, combo, editable, spin, line, tabs, box):
            layout.addWidget(widget)
        window.show()
        QApplication.processEvents()
        # Los botones llevan 1 px de margen arriba y abajo (Anki): 28 a la vista.
        self.assertEqual(button.height() - 2, 28)
        for widget in (combo, editable, spin, line):
            self.assertEqual(widget.height(), 28, type(widget).__name__)
        bar = tabs.tabBar()
        assert bar is not None
        self.assertEqual(bar.tabRect(0).height(), 28)
        for footer in box.buttons():
            self.assertGreaterEqual(footer.width() - 2, 88, footer.text())
        window.close()


class IconTintTest(unittest.TestCase):
    """Versión 3.9.0 (informe del 2026-11-11, apartado 1.4): los iconos sin color propio de
    Anki (la barra lateral de Explorar) salían en blanco puro de noche; van en el texto
    secundario de la paleta."""

    def test_plain_icons_take_the_subtle_text(self) -> None:
        from aqt.qt import QIcon
        from aqt.theme import ColoredIcon
        from aqt.utils import aqt_data_folder

        svg = str(Path(aqt_data_folder()) / "qt" / "icons" / "chevron-down-dark.svg")
        calls: list[object] = []

        def old(_self: object, path: object) -> QIcon:
            calls.append(path)
            return QIcon()

        for night, mode in ((True, "dark"), (False, "light")):
            manager = types.SimpleNamespace(night_mode=night, themed_icon=lambda path: path)
            icon = theming._icon_from_resources(manager, svg, old)  # type: ignore[arg-type]
            image = icon.pixmap(32, 32).toImage()
            painted = {
                QColor(image.pixel(x, y)).name().upper()
                for x in range(image.width())
                for y in range(image.height())
                if QColor.fromRgba(image.pixel(x, y)).alpha() == 255
            }
            self.assertEqual(painted, {themes.colors()["FG_SUBTLE"][mode]})
        # Los iconos con su propio color (banderas, estados) siguen como los pinta Anki.
        colored = ColoredIcon(path=svg, color={"light": "#123456", "dark": "#123456"})  # colores-ok: prueba
        theming._icon_from_resources(types.SimpleNamespace(night_mode=True), colored, old)  # type: ignore[arg-type]
        self.assertEqual(calls, [colored])


class TitleBarTest(unittest.TestCase):
    """Versión 3.3.0: barra de título del color de la paleta, solo en Windows 11."""

    def tearDown(self) -> None:
        themes.select("nocturne")

    def test_colorref_is_windows_order(self) -> None:
        self.assertEqual(titlebar.colorref("#12161F"), 0x1F1612)
        self.assertEqual(titlebar.colorref("#3B6FE0CC"), 0xE06F3B)  # sin transparencia

    def test_bar_follows_palette_and_mode(self) -> None:
        for theme_id, data in themes.THEMES.items():
            themes.select(theme_id)
            for night, mode in ((False, "light"), (True, "dark")):
                colors = dict(titlebar.bar_colors(night, active=True))
                self.assertEqual(colors[35], titlebar.colorref(data["colors"]["NOCTURNE_TITLEBAR"][mode]), theme_id)
                self.assertEqual(colors[36], titlebar.colorref(data["colors"]["FG"][mode]), theme_id)
                self.assertEqual(colors[34], titlebar.colorref(data["colors"]["BORDER"][mode]), theme_id)
                # La ventana inactiva se distingue por su título, más suave.
                inactive = dict(titlebar.bar_colors(night, active=False))
                self.assertEqual(inactive[36], titlebar.colorref(data["colors"]["FG_SUBTLE"][mode]), theme_id)
                self.assertNotEqual(inactive[36], colors[36], theme_id)
                self.assertEqual(inactive[35], colors[35], theme_id)

    def test_only_windows_with_a_title_bar(self) -> None:
        main, menu, child = QMainWindow(), QMenu(), QWidget()
        dialog = QDialog(main)
        frameless = QDialog(main, Qt.WindowType.FramelessWindowHint)
        widget_in_main = QWidget(main)
        self.assertTrue(titlebar.has_title_bar(main))
        self.assertTrue(titlebar.has_title_bar(dialog))
        self.assertTrue(titlebar.has_title_bar(child))  # sin padre, es una ventana
        self.assertFalse(titlebar.has_title_bar(menu))
        self.assertFalse(titlebar.has_title_bar(frameless))
        self.assertFalse(titlebar.has_title_bar(widget_in_main))

    def test_nothing_happens_outside_windows_11(self) -> None:
        if titlebar.supported():
            self.skipTest("solo se comprueba fuera de Windows 11")
        titlebar.install()
        self.assertIsNone(titlebar._watcher)


if __name__ == "__main__":
    unittest.main()
