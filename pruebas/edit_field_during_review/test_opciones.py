"""Pruebas del panel de opciones (1.1.0), del patrón de archivos que se
comparten con el repaso (FIX-004) y de los colores del recuadro (FIX-005), sin
Anki a la vista.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from edit_field_during_review import config, constants, dialogs

ADDON = Path(dialogs.__file__).parent


class PanelPageTests(unittest.TestCase):
    def test_page_has_one_checkbox(self) -> None:
        page = dialogs.page(False)
        item = page["cards"][0]["items"][0]
        self.assertEqual(item["type"], "check")
        self.assertEqual(item["key"], config.KEY_REQUIRE_MODIFIER)
        self.assertFalse(page["values"][config.KEY_REQUIRE_MODIFIER])
        self.assertTrue(page["defaults"][config.KEY_REQUIRE_MODIFIER])
        json.dumps(page)

    def test_chosen_value(self) -> None:
        self.assertFalse(dialogs.chosen_require_modifier({config.KEY_REQUIRE_MODIFIER: False}))
        self.assertTrue(dialogs.chosen_require_modifier({config.KEY_REQUIRE_MODIFIER: "no"}))
        self.assertTrue(dialogs.chosen_require_modifier(None))


class WebExportsTests(unittest.TestCase):
    # FIX-004: solo los dos archivos del repaso, nada de otras carpetas.
    def test_pattern_is_closed(self) -> None:
        pattern = re.compile(constants.WEB_EXPORTS)
        self.assertTrue(pattern.fullmatch("web/editor.css"))
        self.assertTrue(pattern.fullmatch("web/editor.js"))
        for path in ("web/../otro/x.js", "web/..%2F..%2Fotro%2Fx.js", "web/panel.js", "web/a/editor.js"):
            self.assertIsNone(pattern.fullmatch(path), path)


class EditorColorTests(unittest.TestCase):
    # FIX-005: el recuadro usa el color de foco de la paleta.
    def test_outline_uses_palette_token(self) -> None:
        css = (ADDON / "web/editor.css").read_text(encoding="utf-8")
        rules = [line for line in css.splitlines() if line.strip().startswith("outline")]
        self.assertEqual(len(rules), 2)
        for line in rules:
            self.assertIn("var(--border-focus", line)


if __name__ == "__main__":
    unittest.main()
