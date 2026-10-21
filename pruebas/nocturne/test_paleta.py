"""Pruebas de legibilidad de la paleta Nocturne: contraste medido con la
fórmula de las WCAG 2 (texto 4,5:1; bordes de casillas e iconos 3:1).

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import colorsys
import unittest

from aqt.browser.table import adjusted_bg_color
from nocturne.palette import PALETTE

MODES = ("light", "dark")
SURFACES = ("CANVAS", "CANVAS_ELEVATED", "CANVAS_INSET", "CANVAS_OVERLAY")


def _rgb(color: str) -> tuple[float, float, float]:
    color = color.lstrip("#")[:6]
    return (int(color[0:2], 16) / 255, int(color[2:4], 16) / 255, int(color[4:6], 16) / 255)


def _luminance(color: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in _rgb(color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def hue(color: str) -> float:
    return colorsys.rgb_to_hls(*_rgb(color))[0] * 360


def color(name: str, mode: str) -> str:
    return PALETTE[name][mode]  # type: ignore[literal-required]


class TextContrastTest(unittest.TestCase):
    """Regresión de FIX-002: de día, «Aprendiendo», «Para repasar», «Nuevas» y el
    rojo de aviso quedaban por debajo de 4,5:1 (hasta 3,0:1)."""

    TEXT = ("FG", "FG_SUBTLE", "FG_FAINT", "FG_LINK", "STATE_NEW", "STATE_LEARN", "STATE_REVIEW", "ACCENT_DANGER")

    def test_text_reads_on_every_surface(self) -> None:
        for mode in MODES:
            for name in self.TEXT:
                for surface in SURFACES:
                    ratio = contrast(color(name, mode), color(surface, mode))
                    self.assertGreaterEqual(ratio, 4.5, f"{name} sobre {surface} ({mode}): {ratio:.2f}")


class PrimaryButtonTest(unittest.TestCase):
    """Regresión de FIX-005: con el ratón encima, el botón azul empezaba su degradado
    en un azul más claro y su texto blanco bajaba a 3,9:1 (día) y 3,6:1 (noche)."""

    BLUES = ("BUTTON_PRIMARY_BG", "BUTTON_PRIMARY_GRADIENT_START", "BUTTON_PRIMARY_GRADIENT_END", "HIGHLIGHT_BG")

    def test_white_text_reads_in_every_state(self) -> None:
        for mode in MODES:
            for name in self.BLUES:
                ratio = contrast("#FFFFFF", color(name, mode))
                self.assertGreaterEqual(ratio, 4.5, f"{name} ({mode}): {ratio:.2f}")


class CheckboxBorderTest(unittest.TestCase):
    """Regresión de FIX-003: el borde de una casilla sin marcar quedaba en 1,3:1
    de día y 1,5:1 de noche; con el ratón encima, debe destacar aún más."""

    def test_unchecked_box_is_visible(self) -> None:
        for mode in MODES:
            border = color("NOCTURNE_CONTROL_BORDER", mode)
            for surface in ("CANVAS", "CANVAS_ELEVATED"):
                ratio = contrast(border, color(surface, mode))
                self.assertGreaterEqual(ratio, 3.0, f"casilla sobre {surface} ({mode}): {ratio:.2f}")

    def test_hover_stands_out_more(self) -> None:
        for mode in MODES:
            base = contrast(color("NOCTURNE_CONTROL_BORDER", mode), color("CANVAS_ELEVATED", mode))
            hover = contrast(color("BORDER_FOCUS", mode), color("CANVAS_ELEVATED", mode))
            self.assertGreater(hover, base, mode)

    def test_soft_borders_stay_soft(self) -> None:
        # Aspecto original: campos, listas, tablas y separadores con bordes suaves.
        for mode in MODES:
            for name in ("BORDER_SUBTLE", "BORDER"):
                ratio = contrast(color(name, mode), color("CANVAS", mode))
                self.assertLess(ratio, 2.0, f"{name} ({mode}): {ratio:.2f}")


class ExplorerRowsTest(unittest.TestCase):
    """Regresión de FIX-004: de noche, en Explorar, el texto sobre las filas con
    bandera quedaba entre 2,9:1 y 4,3:1. Anki pinta la fila con el color de la
    bandera aclarado de día y oscurecido de noche (APR-058)."""

    ROWS = ("FLAG_1", "FLAG_2", "FLAG_3", "FLAG_4", "FLAG_5", "FLAG_6", "FLAG_7",
            "STATE_MARKED", "STATE_SUSPENDED", "STATE_BURIED")

    def test_row_text_reads(self) -> None:
        for name in self.ROWS:
            adjusted = adjusted_bg_color({"light": color(name, "light"), "dark": color(name, "dark")})
            assert adjusted is not None
            for mode in MODES:
                ratio = contrast(color("FG", mode), adjusted[mode])
                self.assertGreaterEqual(ratio, 4.5, f"fila {name} ({mode}): {ratio:.2f}")

    def test_flags_still_read_as_icons(self) -> None:
        for name in self.ROWS:
            for mode in MODES:
                ratio = contrast(color(name, mode), color("CANVAS", mode))
                self.assertGreaterEqual(ratio, 3.0, f"icono {name} ({mode}): {ratio:.2f}")


class NightComfortTest(unittest.TestCase):
    """Mejora de 2.1.0: de noche, el texto principal no deslumbra (como mucho
    13,5:1 sobre el fondo) y sigue muy por encima del mínimo en toda superficie."""

    def test_night_text_is_softer(self) -> None:
        ratio = contrast(color("FG", "dark"), color("CANVAS", "dark"))
        self.assertLessEqual(ratio, 13.5)
        for surface in SURFACES:
            self.assertGreaterEqual(contrast(color("FG", "dark"), color(surface, "dark")), 7.0, surface)

    def test_selected_text_matches_text(self) -> None:
        for mode in MODES:
            self.assertEqual(color("SELECTED_FG", mode), color("FG", mode))


class IdentityTest(unittest.TestCase):
    """El aspecto original se conserva: fondos y azul de acción sin cambios, y los
    colores corregidos mantienen su tono (±6°): solo cambia su luminosidad."""

    ORIGINAL = {
        "CANVAS": ("#F7F8FA", "#12161F"),
        "CANVAS_ELEVATED": ("#FFFFFF", "#212836"),
        "BUTTON_PRIMARY_BG": ("#3B6FE0", "#4066E6"),
        "HIGHLIGHT_BG": ("#3B6FE0", "#4066E6"),
        "BORDER_SUBTLE": ("#E9ECF0", "#202836"),
    }
    HUES = {
        "STATE_NEW": ("#1971C2", "#74C0FC"),
        "STATE_LEARN": ("#E8590C", "#FFA94D"),
        "STATE_REVIEW": ("#2F9E44", "#57D06B"),
        "ACCENT_DANGER": ("#E03131", "#FF6B6B"),
        "FLAG_2": ("#E8590C", "#FFA94D"),
        "FLAG_3": ("#2F9E44", "#69DB7C"),
        "FLAG_4": ("#1971C2", "#74C0FC"),
        "FLAG_5": ("#C2255C", "#E599F7"),
        "FLAG_6": ("#099268", "#63E6BE"),
        "FLAG_7": ("#7048E8", "#B197FC"),
        "STATE_MARKED": ("#7048E8", "#B197FC"),
        "FG": ("#1B2430", "#E9EDF4"),
    }

    def test_surfaces_and_accent_unchanged(self) -> None:
        for name, (light, dark) in self.ORIGINAL.items():
            self.assertEqual((color(name, "light"), color(name, "dark")), (light, dark), name)

    def test_corrected_colors_keep_their_hue(self) -> None:
        for name, originals in self.HUES.items():
            for mode, original in zip(MODES, originals):
                delta = abs(hue(color(name, mode)) - hue(original))
                delta = min(delta, 360 - delta)
                self.assertLessEqual(delta, 6.0, f"{name} ({mode}): {delta:.1f}°")


if __name__ == "__main__":
    unittest.main()
