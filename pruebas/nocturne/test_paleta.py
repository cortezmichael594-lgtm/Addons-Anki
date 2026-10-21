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

    TEXT = ("FG", "FG_SUBTLE", "FG_FAINT", "FG_LINK", "STATE_NEW", "STATE_LEARN", "STATE_REVIEW", "ACCENT_DANGER",
            "ACCENT_CARD", "ACCENT_NOTE")

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


def _apca_y(value: str) -> float:
    r, g, b = _rgb(value)
    y = 0.2126729 * r**2.4 + 0.7151522 * g**2.4 + 0.0721750 * b**2.4
    return y + (0.022 - y) ** 1.414 if y < 0.022 else y


def apca(text: str, background: str) -> float:
    """Contraste APCA (APCA-W3 0.0.98G), en valor absoluto: tiene en cuenta que el
    texto claro sobre fondo oscuro se percibe distinto que al revés."""
    yt, yb = _apca_y(text), _apca_y(background)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        sapc = (yb**0.56 - yt**0.57) * 1.14
        return 0.0 if sapc < 0.1 else (sapc - 0.027) * 100
    sapc = (yb**0.65 - yt**0.62) * 1.14
    return 0.0 if sapc > -0.1 else abs(sapc + 0.027) * 100


class PerceivedContrastTest(unittest.TestCase):
    """Versión 3.0.0: además de WCAG 2, el texto se mide con APCA. Mínimos de
    Practical UI (cifras del cap. 3): 75 para el texto principal, 60 para el
    secundario y 45 para lo menos importante."""

    TEXT_SURFACES = SURFACES + ("CANVAS_CODE",)

    def test_text_levels(self) -> None:
        for mode in MODES:
            for name, minimum in (("FG", 75), ("FG_SUBTLE", 60), ("FG_FAINT", 45), ("FG_LINK", 60)):
                for surface in self.TEXT_SURFACES:
                    value = apca(color(name, mode), color(surface, mode))
                    self.assertGreaterEqual(value, minimum, f"{name} sobre {surface} ({mode}): {value:.1f}")

    def test_text_on_buttons(self) -> None:
        for mode in MODES:
            for surface in ("BUTTON_BG", "BUTTON_HOVER"):
                self.assertGreaterEqual(contrast(color("FG", mode), color(surface, mode)), 4.5, surface)
                self.assertGreaterEqual(apca(color("FG", mode), color(surface, mode)), 75, surface)

    def test_three_distinct_text_levels(self) -> None:
        # La jerarquía se nota: cada nivel de texto pierde contraste frente al anterior.
        for mode in MODES:
            levels = [contrast(color(n, mode), color("CANVAS", mode)) for n in ("FG", "FG_SUBTLE", "FG_FAINT")]
            self.assertGreater(levels[0], levels[1] * 1.15, mode)
            self.assertGreater(levels[1], levels[2] * 1.15, mode)


class NightDepthTest(unittest.TestCase):
    """Versión 3.0.0: de noche, lo que está más arriba es más claro (Practical UI,
    M3; Refactoring UI, P24). Antes, los menús eran más oscuros que los recuadros."""

    ORDER = ("CANVAS_INSET", "CANVAS", "CANVAS_ELEVATED", "BUTTON_BG", "CANVAS_OVERLAY", "BUTTON_HOVER")

    def test_higher_is_lighter(self) -> None:
        values = [_luminance(color(name, "dark")) for name in self.ORDER]
        for lower, upper, a, b in zip(values, values[1:], self.ORDER, self.ORDER[1:]):
            self.assertLess(lower, upper, f"{a} debería ser más oscuro que {b}")

    def test_menu_border_and_boxes_visible(self) -> None:
        for surface in ("CANVAS", "CANVAS_ELEVATED", "CANVAS_OVERLAY"):
            self.assertGreaterEqual(contrast(color("NOCTURNE_CONTROL_BORDER", "dark"), color(surface, "dark")), 3.0, surface)


class IdentityTest(unittest.TestCase):
    """El aspecto original se conserva: mismo fondo, mismo azul de acción y una sola
    familia de grises azulados; los colores con significado mantienen su tono."""

    ORIGINAL = {
        "CANVAS": ("#F7F8FA", "#12161F"),
        "BUTTON_PRIMARY_BG": ("#3B6FE0", "#4066E6"),
        "HIGHLIGHT_BG": ("#3B6FE0", "#4066E6"),
    }
    NEUTRALS = (
        "CANVAS_INSET", "CANVAS_CODE", "CANVAS", "CANVAS_ELEVATED", "CANVAS_OVERLAY", "BUTTON_BG",
        "BUTTON_HOVER", "BORDER_SUBTLE", "BORDER", "BORDER_STRONG", "NOCTURNE_CONTROL_BORDER",
        "SCROLLBAR_BG", "SCROLLBAR_BG_HOVER", "SCROLLBAR_BG_ACTIVE", "FG_DISABLED", "FG_FAINT",
        "FG_SUBTLE", "FG",
    )
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
    }

    def test_background_and_accent_unchanged(self) -> None:
        for name, (light, dark) in self.ORIGINAL.items():
            self.assertEqual((color(name, "light"), color(name, "dark")), (light, dark), name)

    def test_one_family_of_bluish_greys(self) -> None:
        for name in self.NEUTRALS:
            for mode in MODES:
                value = color(name, mode)
                self.assertLessEqual(abs(hue(value) - 220), 6, f"{name} ({mode}): {hue(value):.0f}°")
                self.assertNotIn(value[:7].upper(), ("#FFFFFF", "#000000"), name)

    def test_corrected_colors_keep_their_hue(self) -> None:
        for name, originals in self.HUES.items():
            for mode, original in zip(MODES, originals):
                delta = abs(hue(color(name, mode)) - hue(original))
                delta = min(delta, 360 - delta)
                self.assertLessEqual(delta, 6.0, f"{name} ({mode}): {delta:.1f}°")


if __name__ == "__main__":
    unittest.main()
