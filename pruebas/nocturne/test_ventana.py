"""Pruebas de la ventana de configuración, de sus textos y del color de la barra
de título, con Qt sin pantalla (QT_QPA_PLATFORM=offscreen) y sin Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import types
import unittest

import anki.lang
from aqt.qt import QApplication, QDialog, QLabel, QMainWindow, QMenu, QPushButton, QRadioButton, Qt, QWidget
from nocturne import contrast, dialogs, errors, strings, themes, titlebar

_app = QApplication.instance() or QApplication([])
anki.lang.set_lang("es")  # el título de la ventana sale de las traducciones de Anki


class OwnerWindowTest(unittest.TestCase):
    """Regresión de FIX-007: la ventana de paletas se abría con la ventana principal
    de padre y quedaba detrás de la de complementos, que es desde donde se pide."""

    def setUp(self) -> None:
        self._mw = dialogs.mw
        self.main = QMainWindow()
        self.addons = QDialog(self.main)  # hace de ventana de complementos
        self.addons.show()
        dialogs.mw = types.SimpleNamespace(  # type: ignore[assignment]
            app=types.SimpleNamespace(activeWindow=lambda: self.addons)
        )

    def tearDown(self) -> None:
        if dialogs._dialog is not None:
            dialogs._dialog.reject()
        dialogs.mw = self._mw  # type: ignore[assignment]
        dialogs._dialog = None
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
        self.assertEqual(dialog.windowTitle(), "Configurar 'Nocturne'")
        self.assertFalse(dialog.windowFlags() & Qt.WindowType.WindowContextHelpButtonHint)

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
    """Versión 3.5.0 (informe de 2026-10-26, apartados 2.3, 3.1, 3.2 y 3.3): las tres
    paletas a la vista, la predeterminada marcada, vista previa y vuelta atrás."""

    def setUp(self) -> None:
        self.owner = QDialog()
        themes.select("nocturne")

    def tearDown(self) -> None:
        errors._failures = 0
        contrast._stepped_aside = False
        themes.select("nocturne")
        self.owner.close()

    def dialog(self) -> dialogs.PaletteDialog:
        return dialogs.PaletteDialog(self.owner)

    def test_three_options_with_descriptions(self) -> None:
        dialog = self.dialog()
        radios = [b.text() for b in dialog.findChildren(QRadioButton)]
        self.assertEqual(radios, ["Nocturne" + strings.DEFAULT_SUFFIX, "Papel", "Bosque"])
        texts = [label.text() for label in dialog.findChildren(QLabel)]
        for description in strings.THEME_DESCRIPTIONS.values():
            self.assertIn(description, texts)
        self.assertIn(strings.DAY_AND_NIGHT, texts)
        self.assertNotIn(strings.HIGH_CONTRAST, texts)
        self.assertNotIn(strings.FAILURES, texts)

    def test_clicking_a_description_picks_its_palette(self) -> None:
        dialog = self.dialog()
        label = next(l for l in dialog.findChildren(QLabel) if l.text() == strings.THEME_DESCRIPTIONS["bosque"])
        label.mousePressEvent(None)
        self.assertEqual(dialog.selected_id(), "bosque")

    def test_preview_then_cancel_goes_back(self) -> None:
        dialog = self.dialog()
        dialog._buttons["papel"].setChecked(True)
        dialog._preview()  # lo que hace el temporizador
        self.assertEqual(themes.current_id(), "papel")
        dialog.reject()
        self.assertEqual(themes.current_id(), "nocturne")

    def test_accept_keeps_the_choice(self) -> None:
        dialog = self.dialog()
        dialog._buttons["bosque"].setChecked(True)
        dialog.accept()
        self.assertEqual(themes.current_id(), "bosque")

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

    def test_high_contrast_no_preview(self) -> None:
        contrast.step_aside()
        dialog = self.dialog()
        self.assertIn(strings.HIGH_CONTRAST, [label.text() for label in dialog.findChildren(QLabel)])
        dialog._buttons["papel"].setChecked(True)
        self.assertFalse(dialog._timer.isActive())
        dialog.accept()
        # Se guarda (para cuando vuelva el contraste normal), pero no se pinta.
        self.assertEqual(themes.current_id(), "nocturne")

    def test_contrast_check_is_safe(self) -> None:
        self.assertIsInstance(contrast.system_wants_more_contrast(), bool)


class DescriptionTest(unittest.TestCase):
    """Petición del cliente (2026-10-21): una sola línea por paleta y las tres con la
    misma estructura: colores y acento, y después su forma."""

    def test_one_line_same_structure(self) -> None:
        for theme_id in themes.THEMES:
            text = strings.THEME_DESCRIPTIONS[theme_id]
            self.assertLessEqual(len(text), 80, theme_id)
            self.assertEqual(text.count(". "), 1, theme_id)
            self.assertTrue(text.endswith("."), theme_id)
            self.assertIn("botones", text, theme_id)
            self.assertNotIn("acento", text, theme_id)
            for word in ("noche", "día"):
                self.assertNotIn(word, text.casefold(), theme_id)


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
