"""Regresión de FIX-003: el atajo cambia todas las ventanas Añadir abiertas, no solo la última.

Sin Anki a la vista: ventanas de Qt vacías, ocultas, en una aplicación sin pantalla.
"""

from __future__ import annotations

import os
import unittest
from unittest import mock

from aqt.qt import QApplication, Qt, QWidget

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
_APP = QApplication.instance() or QApplication([])

from always_on_top import logic  # noqa: E402


class AllAddWindowsTests(unittest.TestCase):
    def test_shortcut_changes_every_open_add_window(self) -> None:
        manager = logic.AlwaysOnTopManager()
        normal, with_shift = QWidget(), QWidget()
        manager.on_add_cards_init(normal)
        manager.on_add_cards_init(with_shift)
        with mock.patch.object(logic, "tooltip"):
            manager._on_shortcut_activated()
            for window in (normal, with_shift):
                self.assertTrue(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
            manager._on_shortcut_activated()
            for window in (normal, with_shift):
                self.assertFalse(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)

    def test_closed_windows_are_forgotten(self) -> None:
        manager = logic.AlwaysOnTopManager()
        first = QWidget()
        manager.on_add_cards_init(first)
        first.deleteLater()
        del first
        _APP.processEvents()
        self.assertEqual(manager._open_windows(), [])


if __name__ == "__main__":
    unittest.main()
