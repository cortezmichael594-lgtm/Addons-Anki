"""Pruebas de legibilidad de las tres paletas de Nocturne (Nocturne, Papel y
Bosque): contraste medido con la fórmula de las WCAG 2 (texto 4,5:1; bordes de
casillas e iconos 3:1) y con APCA.

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import colorsys
import unittest

from aqt.browser.table import adjusted_bg_color
from nocturne.palette import PALETTE
from nocturne.themes import THEMES

MODES = ("light", "dark")
SURFACES = ("CANVAS", "CANVAS_ELEVATED", "CANVAS_INSET", "CANVAS_OVERLAY", "NOCTURNE_ROW_HIGHLIGHT")


def _rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")[:6]
    return (int(value[0:2], 16) / 255, int(value[2:4], 16) / 255, int(value[4:6], 16) / 255)


def _luminance(value: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in _rgb(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def hue(value: str) -> float:
    return colorsys.rgb_to_hls(*_rgb(value))[0] * 360


def saturation(value: str) -> float:
    return colorsys.rgb_to_hls(*_rgb(value))[2] * 100


def blend(top: str, below: str) -> str:
    """Color resultante de un color con transparencia (#RRGGBBAA) sobre otro."""
    alpha = int(top[7:9], 16) / 255 if len(top) > 7 else 1.0
    mixed = (alpha * a + (1 - alpha) * b for a, b in zip(_rgb(top), _rgb(below)))
    return "#" + "".join(f"{round(c * 255):02X}" for c in mixed)


def hue_distance(a: str, b: str) -> float:
    delta = abs(hue(a) - hue(b))
    return min(delta, 360 - delta)


def color(name: str, mode: str, theme: str = "nocturne") -> str:
    return THEMES[theme]["colors"][name][mode]  # type: ignore[literal-required]


def text_min(theme: str) -> float:
    return 4.5


class StructureTest(unittest.TestCase):
    """Todas las paletas definen los mismos colores, con las variables CSS de Nocturne."""

    def test_same_tokens_everywhere(self) -> None:
        for theme, data in THEMES.items():
            self.assertEqual(set(data["colors"]), set(PALETTE), theme)
            for name, entry in data["colors"].items():
                self.assertEqual(entry["css"], PALETTE[name]["css"], f"{theme} {name}")

    def test_corners_fit_small_controls(self) -> None:
        # Las casillas miden 16px y las barras de desplazamiento 12px (APR-059).
        for theme, data in THEMES.items():
            look = data["look"]
            self.assertLessEqual(look["radius"], 6, theme)
            self.assertLessEqual(look["radius"], look["radius_medium"], theme)
            # Qt no redondea un botón si el radio pasa de la mitad de su altura: con
            # botones de unos 20px de alto, 9px como mucho (visto en la muestra de 3.1.0).
            self.assertLessEqual(look["button_radius"], 9, theme)
            # Versión 3.5.0: dos radios por paleta, controles y recuadros (el doble).
            self.assertEqual(look["radius_medium"], 2 * look["button_radius"], theme)


class TextContrastTest(unittest.TestCase):
    """Regresión de FIX-002: de día, «Aprendiendo», «Para repasar», «Nuevas» y el
    rojo de aviso quedaban por debajo de 4,5:1 (hasta 3,0:1). Vale para todas las
    paletas, también sobre el resaltado de la fila del mazo."""

    TEXT = ("FG", "FG_SUBTLE", "FG_FAINT", "FG_LINK", "STATE_NEW", "STATE_LEARN", "STATE_REVIEW", "ACCENT_DANGER",
            "ACCENT_CARD", "ACCENT_NOTE")

    def test_text_reads_on_every_surface(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for name in self.TEXT:
                    for surface in SURFACES:
                        ratio = contrast(color(name, mode, theme), color(surface, mode, theme))
                        self.assertGreaterEqual(
                            ratio, text_min(theme), f"{theme}: {name} sobre {surface} ({mode}): {ratio:.2f}"
                        )


class PrimaryButtonTest(unittest.TestCase):
    """Regresión de FIX-005: con el ratón encima, el botón azul empezaba su degradado
    en un azul más claro y su texto blanco bajaba a 3,9:1 (día) y 3,6:1 (noche).
    Desde 3.1.0 incluye el botón principal relleno de las ventanas (pulsado y anillo)."""

    BLUES = ("BUTTON_PRIMARY_BG", "BUTTON_PRIMARY_GRADIENT_START", "BUTTON_PRIMARY_GRADIENT_END", "HIGHLIGHT_BG",
             "NOCTURNE_PRIMARY_PRESSED")

    def test_white_text_reads_in_every_state(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for name in self.BLUES:
                    ratio = contrast("#FFFFFF", color(name, mode, theme))
                    self.assertGreaterEqual(ratio, text_min(theme), f"{theme}: {name} ({mode}): {ratio:.2f}")

    def test_ring_is_visible(self) -> None:
        # El anillo del botón principal con foco o ratón se ve sobre el fondo (3:1) y
        # se distingue del relleno.
        for theme in THEMES:
            for mode in MODES:
                ring = color("NOCTURNE_PRIMARY_RING", mode, theme)
                self.assertGreaterEqual(contrast(ring, color("CANVAS", mode, theme)), 3.0, f"{theme} ({mode})")
                self.assertGreaterEqual(contrast(ring, color("BUTTON_PRIMARY_BG", mode, theme)), 1.5, f"{theme} ({mode})")

    def test_states_get_darker(self) -> None:
        # Reposo, ratón encima y pulsado se distinguen: cada uno más oscuro.
        for theme in THEMES:
            for mode in MODES:
                levels = [_luminance(color(n, mode, theme)) for n in
                          ("BUTTON_PRIMARY_BG", "BUTTON_PRIMARY_GRADIENT_END", "NOCTURNE_PRIMARY_PRESSED")]
                self.assertGreater(levels[0], levels[1], f"{theme} ({mode})")
                self.assertGreater(levels[1], levels[2], f"{theme} ({mode})")


class CheckboxBorderTest(unittest.TestCase):
    """Regresión de FIX-003: el borde de una casilla sin marcar quedaba en 1,3:1
    de día y 1,5:1 de noche; con el ratón encima, debe destacar aún más."""

    def test_unchecked_box_is_visible(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                border = color("NOCTURNE_CONTROL_BORDER", mode, theme)
                for surface in ("CANVAS", "CANVAS_ELEVATED", "CANVAS_OVERLAY"):
                    ratio = contrast(border, color(surface, mode, theme))
                    self.assertGreaterEqual(ratio, 3.0, f"{theme}: casilla sobre {surface} ({mode}): {ratio:.2f}")

    def test_hover_stands_out_more(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                base = contrast(color("NOCTURNE_CONTROL_BORDER", mode, theme), color("CANVAS_ELEVATED", mode, theme))
                hover = contrast(color("BORDER_FOCUS", mode, theme), color("CANVAS_ELEVATED", mode, theme))
                self.assertGreater(hover, base * 0.95, f"{theme} ({mode})")
                self.assertGreaterEqual(hover, 3.0, f"{theme} ({mode})")

    def test_soft_borders_stay_soft(self) -> None:
        # Aspecto elegido por el cliente: campos, listas, tablas y separadores con
        # bordes suaves.
        for theme in THEMES:
            for mode in MODES:
                for name in ("BORDER_SUBTLE", "BORDER"):
                    ratio = contrast(color(name, mode, theme), color("CANVAS", mode, theme))
                    self.assertLess(ratio, 2.0, f"{theme}: {name} ({mode}): {ratio:.2f}")

    def test_text_reads_on_border_color(self) -> None:
        # Anki usa BORDER como fondo de algún aviso de la lista de mazos.
        for theme in THEMES:
            for mode in MODES:
                self.assertGreaterEqual(contrast(color("FG", mode, theme), color("BORDER", mode, theme)), 4.5, theme)


class ExplorerRowsTest(unittest.TestCase):
    """Regresión de FIX-004: de noche, en Explorar, el texto sobre las filas con
    bandera quedaba entre 2,9:1 y 4,3:1. Anki pinta la fila con el color de la
    bandera aclarado de día y oscurecido de noche (APR-058)."""

    ROWS = ("FLAG_1", "FLAG_2", "FLAG_3", "FLAG_4", "FLAG_5", "FLAG_6", "FLAG_7",
            "STATE_MARKED", "STATE_SUSPENDED", "STATE_BURIED")

    def test_row_text_reads(self) -> None:
        for theme in THEMES:
            for name in self.ROWS:
                adjusted = adjusted_bg_color({"light": color(name, "light", theme), "dark": color(name, "dark", theme)})
                assert adjusted is not None
                for mode in MODES:
                    ratio = contrast(color("FG", mode, theme), adjusted[mode])
                    self.assertGreaterEqual(ratio, 4.5, f"{theme}: fila {name} ({mode}): {ratio:.2f}")

    def test_flags_still_read_as_icons(self) -> None:
        for theme in THEMES:
            for name in self.ROWS:
                for mode in MODES:
                    ratio = contrast(color(name, mode, theme), color("CANVAS", mode, theme))
                    self.assertGreaterEqual(ratio, 3.0, f"{theme}: icono {name} ({mode}): {ratio:.2f}")

    def test_selected_rows_read(self) -> None:
        # Filas seleccionadas en Explorar: SELECTED_BG sobre el fondo de la tabla.
        for theme in THEMES:
            for mode in MODES:
                selected = blend(color("SELECTED_BG", mode, theme), color("CANVAS_CODE", mode, theme))
                ratio = contrast(color("SELECTED_FG", mode, theme), selected)
                self.assertGreaterEqual(ratio, text_min(theme), f"{theme} ({mode}): {ratio:.2f}")


class FlagMeaningTest(unittest.TestCase):
    """Versión 3.1.0. Las banderas conservan el tono de su nombre (la roja sigue
    siendo roja) y la roja y la verde se distinguen también por su claridad, para
    quien no distingue bien el rojo del verde (Refactoring UI, P21 y N7; Tufte, N7;
    Practical UI, P9)."""

    # Colores de Anki 26.09.3 (_aqt/colors.py): día y noche.
    ANKI = {
        "FLAG_1": ("#ef4444", "#f87171"), "FLAG_2": ("#fb923c", "#fdba74"), "FLAG_3": ("#4ade80", "#86efac"),
        "FLAG_4": ("#3b82f6", "#60a5fa"), "FLAG_5": ("#e879f9", "#f0abfc"), "FLAG_6": ("#2dd4bf", "#5eead4"),
        "FLAG_7": ("#a855f7", "#c084fc"),
    }

    def test_red_and_green_differ_in_lightness(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                ratio = contrast(color("FLAG_1", mode, theme), color("FLAG_3", mode, theme))
                self.assertGreaterEqual(ratio, 1.4, f"{theme} ({mode}): {ratio:.2f}")

    def test_flags_keep_their_name(self) -> None:
        for theme in THEMES:
            for name, originals in self.ANKI.items():
                for mode, original in zip(MODES, originals):
                    delta = hue_distance(color(name, mode, theme), original)
                    self.assertLessEqual(delta, 20.0, f"{theme}: {name} ({mode}): {delta:.0f}°")


class NightSaturationTest(unittest.TestCase):
    """Versión 3.1.0: de noche, los colores con significado no van saturados al
    máximo, para que no «vibren» sobre el fondo oscuro (Orbix, M3 y C3)."""

    NAMES = ("STATE_NEW", "STATE_LEARN", "STATE_REVIEW", "STATE_MARKED", "STATE_SUSPENDED", "STATE_BURIED",
             "ACCENT_DANGER", "ACCENT_CARD", "ACCENT_NOTE", "FG_LINK",
             "FLAG_1", "FLAG_2", "FLAG_3", "FLAG_4", "FLAG_5", "FLAG_6", "FLAG_7")

    def test_night_colors_are_not_saturated(self) -> None:
        for theme in THEMES:
            for name in self.NAMES:
                value = saturation(color(name, "dark", theme))
                self.assertLessEqual(value, 86.0, f"{theme}: {name}: {value:.0f} %")


class HighlightTest(unittest.TestCase):
    """Versión 3.1.0: la fila del mazo actual (y la que tiene el ratón encima) se
    resalta con un tinte del color de acción que se nota sin tapar el texto."""

    def test_row_highlight_is_visible(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                ratio = contrast(color("NOCTURNE_ROW_HIGHLIGHT", mode, theme), color("CANVAS", mode, theme))
                self.assertGreaterEqual(ratio, 1.05, f"{theme} ({mode}): {ratio:.2f}")


class NightComfortTest(unittest.TestCase):
    """Mejora de 2.1.0: de noche, el texto principal no deslumbra (como mucho
    13,5:1 sobre el fondo) y sigue muy por encima del mínimo en toda superficie."""

    def test_night_text_is_softer(self) -> None:
        for theme in THEMES:
            ratio = contrast(color("FG", "dark", theme), color("CANVAS", "dark", theme))
            self.assertLessEqual(ratio, 13.5, theme)
            for surface in SURFACES:
                self.assertGreaterEqual(contrast(color("FG", "dark", theme), color(surface, "dark", theme)), 7.0, surface)

    def test_selected_text_matches_text(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                self.assertEqual(color("SELECTED_FG", mode, theme), color("FG", mode, theme), theme)


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

    def minimums(self, theme: str) -> tuple[tuple[str, int], ...]:
        return (("FG", 75), ("FG_SUBTLE", 60), ("FG_FAINT", 45), ("FG_LINK", 60))

    def test_text_levels(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for name, minimum in self.minimums(theme):
                    for surface in self.TEXT_SURFACES:
                        value = apca(color(name, mode, theme), color(surface, mode, theme))
                        self.assertGreaterEqual(value, minimum, f"{theme}: {name} sobre {surface} ({mode}): {value:.1f}")

    def test_text_on_buttons(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for surface in ("BUTTON_BG", "BUTTON_HOVER"):
                    self.assertGreaterEqual(contrast(color("FG", mode, theme), color(surface, mode, theme)), 4.5, surface)
                    self.assertGreaterEqual(apca(color("FG", mode, theme), color(surface, mode, theme)), 75, surface)

    def test_three_distinct_text_levels(self) -> None:
        # La jerarquía se nota: cada nivel de texto pierde contraste frente al anterior.
        for theme in THEMES:
            for mode in MODES:
                levels = [contrast(color(n, mode, theme), color("CANVAS", mode, theme)) for n in ("FG", "FG_SUBTLE", "FG_FAINT")]
                self.assertGreater(levels[0], levels[1] * 1.15, f"{theme} ({mode})")
                self.assertGreater(levels[1], levels[2] * 1.15, f"{theme} ({mode})")


class DisabledTextTest(unittest.TestCase):
    """Versión 3.3.0: el texto desactivado (botones apagados y la cifra de tarjetas
    enterradas de la pantalla de estudio) llega al mínimo absoluto de APCA, 30
    (Practical UI, cap. 3), y sigue por debajo de lo menos importante (FG_FAINT)."""

    BACKGROUNDS = ("CANVAS", "CANVAS_ELEVATED", "BUTTON_BG", "BUTTON_HOVER")

    def test_readable(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for surface in self.BACKGROUNDS:
                    value = apca(color("FG_DISABLED", mode, theme), color(surface, mode, theme)[:7])
                    self.assertGreaterEqual(value, 30, f"{theme}: sobre {surface} ({mode}): {value:.1f}")

    def test_still_looks_disabled(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                canvas = color("CANVAS", mode, theme)
                disabled = apca(color("FG_DISABLED", mode, theme), canvas)
                faint = apca(color("FG_FAINT", mode, theme), canvas)
                self.assertGreater(faint, disabled + 8, f"{theme} ({mode})")


class TitleBarToneTest(unittest.TestCase):
    """Versión 3.4.0 (petición del cliente): la barra de título tiene su propio tono, del
    matiz del fondo: más oscuro de noche y más claro de día, sin negro ni blanco puros, y
    con el título (activo e inactivo) legible."""

    def test_darker_at_night_lighter_by_day(self) -> None:
        for theme in THEMES:
            day, night = color("NOCTURNE_TITLEBAR", "light", theme), color("NOCTURNE_TITLEBAR", "dark", theme)
            self.assertGreater(_luminance(day), _luminance(color("CANVAS", "light", theme)), theme)
            self.assertLess(_luminance(night), _luminance(color("CANVAS", "dark", theme)) * 0.8, theme)
            self.assertNotIn(day.upper(), ("#FFFFFF",), theme)
            self.assertNotIn(night.upper(), ("#000000",), theme)
            self.assertLess(hue_distance(night, color("CANVAS", "dark", theme)), 20, theme)

    def test_each_palette_has_its_own_bar(self) -> None:
        # Petición del cliente: cada paleta, su barra, reconocible por su matiz.
        themes = list(THEMES)
        for mode in MODES:
            for i, first in enumerate(themes):
                for second in themes[i + 1 :]:
                    a, b = color("NOCTURNE_TITLEBAR", mode, first), color("NOCTURNE_TITLEBAR", mode, second)
                    self.assertNotEqual(a, b, f"{first}/{second} ({mode})")
                    self.assertGreaterEqual(hue_distance(a, b), 15, f"{first}/{second} ({mode})")

    def test_title_text_reads(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                bar = color("NOCTURNE_TITLEBAR", mode, theme)
                self.assertGreaterEqual(contrast(color("FG", mode, theme), bar), 7, f"{theme} ({mode})")
                self.assertGreaterEqual(contrast(color("FG_SUBTLE", mode, theme), bar), 4.5, f"{theme} ({mode})")


class ActionStrokeTest(unittest.TestCase):
    """Versión 3.5.0 (informe de 2026-10-26, apartado 4.1): el color de acción hace
    dos trabajos. Los rellenos llevan texto blanco (PrimaryButtonTest); los trazos
    (foco, anillo del botón principal, enlaces) usan un tono propio, más claro de
    noche, que se ve a 3:1 o más sobre cualquier fondo (WCAG 1.4.11) y a 4,5 sobre el
    fondo de la ventana."""

    STROKES = ("BORDER_FOCUS", "NOCTURNE_PRIMARY_RING", "FG_LINK")
    SURFACES = ("CANVAS", "CANVAS_ELEVATED", "BUTTON_BG", "CANVAS_OVERLAY")

    def test_strokes_show_on_every_surface(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for name in self.STROKES:
                    for surface in self.SURFACES:
                        ratio = contrast(color(name, mode, theme), color(surface, mode, theme)[:7])
                        self.assertGreaterEqual(ratio, 3.0, f"{theme}: {name} sobre {surface} ({mode}): {ratio:.2f}")
                    ratio = contrast(color(name, mode, theme), color("CANVAS", mode, theme))
                    self.assertGreaterEqual(ratio, 4.3, f"{theme}: {name} sobre CANVAS ({mode}): {ratio:.2f}")

    def test_stroke_is_lighter_than_fill_at_night(self) -> None:
        for theme in THEMES:
            stroke, fill = color("BORDER_FOCUS", "dark", theme), color("BUTTON_PRIMARY_BG", "dark", theme)
            self.assertGreater(_luminance(stroke), _luminance(fill), theme)


class SecondaryTextOnButtonsTest(unittest.TestCase):
    """Versión 3.7.0: las cabeceras de Explorar van en el texto secundario sobre el
    fondo de botón, y los nombres del panel sobre el tinte de la fila elegida."""

    def test_reads(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for surface in ("BUTTON_BG", "BUTTON_HOVER", "NOCTURNE_ROW_HIGHLIGHT"):
                    ratio = contrast(color("FG_SUBTLE", mode, theme), color(surface, mode, theme))
                    self.assertGreaterEqual(ratio, 4.5, f"{theme} ({mode}) sobre {surface}: {ratio:.2f}")


class ActionVersusMeaningTest(unittest.TestCase):
    """Versión 3.6.0: el color de acción no se confunde con los colores con significado
    de las rayas de respuesta («Otra vez» rojo, «Difícil» naranja). Si tiene un matiz
    parecido (el cobre de Atardecer), se separa por claridad (Webflow, P2)."""

    def test_action_is_not_a_meaning(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                action = color("BUTTON_PRIMARY_BG", mode, theme)
                for name in ("FLAG_2", "STATE_LEARN", "ACCENT_DANGER"):
                    other = color(name, mode, theme)
                    if hue_distance(action, other) < 30:
                        ratio = contrast(action, other)
                        self.assertGreaterEqual(ratio, 1.5, f"{theme} ({mode}): acción y {name}: {ratio:.2f}")


# Simulación de daltonismo de Machado, Oliveira y Fernandes (2009), gravedad máxima,
# sobre valores lineales.
_CVD = {
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
}


def _simulate(value: str, kind: str) -> str:
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    def srgb(c: float) -> float:
        c = min(max(c, 0.0), 1.0)
        return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    rgb = [lin(c) for c in _rgb(value)]
    out = [srgb(sum(m * c for m, c in zip(row, rgb))) for row in _CVD[kind]]
    return "#" + "".join(f"{round(c * 255):02X}" for c in out)


class ColorBlindTest(unittest.TestCase):
    """Versión 3.5.0 (informe, apartado 4.7): lo que se distingue solo por el color
    sigue distinguiéndose con deuteranopía y protanopía, por claridad, en las tres
    paletas (1,4 veces, el mismo criterio que con visión normal). Es el caso de las
    banderas roja y verde en las filas de Explorar. Las cifras de la lista de mazos se
    distinguen además por su columna y las rayas de los botones de respuesta por su
    texto; las gráficas de las estadísticas usan colores propios de Anki."""

    PAIRS = (("FLAG_1", "FLAG_3"),)

    def test_pairs_differ_in_lightness(self) -> None:
        for theme in THEMES:
            for mode in MODES:
                for kind in _CVD:
                    for first, second in self.PAIRS:
                        a = _simulate(color(first, mode, theme), kind)
                        b = _simulate(color(second, mode, theme), kind)
                        ratio = contrast(a, b)
                        self.assertGreaterEqual(ratio, 1.4, f"{theme} {mode} {kind}: {first}/{second}: {ratio:.2f}")


class NightDepthTest(unittest.TestCase):
    """Versión 3.0.0: de noche, lo que está más arriba es más claro (Practical UI,
    M3; Refactoring UI, P24). Antes, los menús eran más oscuros que los recuadros."""

    ORDER = ("CANVAS_INSET", "CANVAS", "CANVAS_ELEVATED", "BUTTON_BG", "CANVAS_OVERLAY", "BUTTON_HOVER")

    def test_higher_is_lighter(self) -> None:
        for theme in THEMES:
            values = [_luminance(color(name, "dark", theme)) for name in self.ORDER]
            for lower, upper, a, b in zip(values, values[1:], self.ORDER, self.ORDER[1:]):
                self.assertLess(lower, upper, f"{theme}: {a} debería ser más oscuro que {b}")


class FamilyTest(unittest.TestCase):
    """Cada paleta tiene una sola familia de neutros (Webflow, P4; Refactoring UI,
    P20): grises azulados en Nocturne, cálidos en Papel de día, verdosos en Bosque,
    lila en Lavanda y melocotón y marrón en Atardecer.
    Papel de noche («Tinta», 3.2.0) une fondos azul petróleo, de la familia del color
    de acción, con texto crema. Ninguno es blanco ni negro puro."""

    SURFACES_AND_LINES = (
        "CANVAS_INSET", "CANVAS_CODE", "CANVAS", "CANVAS_ELEVATED", "CANVAS_OVERLAY", "BUTTON_BG",
        "BUTTON_HOVER", "BORDER_SUBTLE", "BORDER", "BORDER_STRONG", "NOCTURNE_CONTROL_BORDER",
        "SCROLLBAR_BG", "SCROLLBAR_BG_HOVER", "SCROLLBAR_BG_ACTIVE", "FG_DISABLED",
    )
    TEXT = ("FG_FAINT", "FG_SUBTLE", "FG")
    # (paleta, modo): (tono central de fondos y líneas, tono central del texto), con un margen.
    FAMILY = {
        ("nocturne", "light"): (220, 220), ("nocturne", "dark"): (220, 220),
        ("papel", "light"): (36, 36), ("papel", "dark"): (198, 38),
        ("bosque", "light"): (138, 138), ("bosque", "dark"): (138, 138),
        # Versión 3.6.0: grises lila en Lavanda y cálidos (melocotón y marrón) en Atardecer.
        ("lavanda", "light"): (262, 262), ("lavanda", "dark"): (262, 262),
        ("atardecer", "light"): (24, 24), ("atardecer", "dark"): (24, 24),
    }
    MARGIN = {"nocturne": 6, "papel": 12, "bosque": 12, "lavanda": 6, "atardecer": 6}

    def check(self, theme: str, mode: str, names: tuple[str, ...], center: float) -> None:
        for name in names:
            value = color(name, mode, theme)
            self.assertNotIn(value[:7].upper(), ("#FFFFFF", "#000000"), f"{theme}: {name}")
            distance = min(abs(hue(value) - center), 360 - abs(hue(value) - center))
            self.assertLessEqual(distance, self.MARGIN[theme], f"{theme}: {name} ({mode}): {hue(value):.0f}°")

    def test_one_family_of_neutrals(self) -> None:
        self.assertEqual({theme for theme, _mode in self.FAMILY}, set(THEMES))
        for (theme, mode), (lines, text) in self.FAMILY.items():
            self.check(theme, mode, self.SURFACES_AND_LINES, lines)
            self.check(theme, mode, self.TEXT, text)


class AnkiScreensTest(unittest.TestCase):
    """Versión 3.2.0: barra superior y botones de respuesta del repaso."""

    def test_toolbar_hover_is_visible(self) -> None:
        # El fondo al pasar el ratón por Mazos, Añadir... se distingue de la barra
        # y el texto se sigue leyendo.
        for theme in THEMES:
            for mode in MODES:
                hover, bar = color("BUTTON_HOVER", mode, theme), color("CANVAS_ELEVATED", mode, theme)
                self.assertGreaterEqual(contrast(hover, bar), 1.05, f"{theme} ({mode})")
                self.assertGreaterEqual(contrast(color("FG", mode, theme), hover), 4.5, f"{theme} ({mode})")

    def test_answer_marks_are_visible(self) -> None:
        # La raya de color de «Otra vez», «Difícil», «Bien» y «Fácil» se ve sobre el
        # botón, en reposo y con el ratón encima (3:1, como un icono).
        def mark(name: str, mode: str, theme: str) -> str:
            value = color(name, mode, theme)
            if name != "FLAG_2":
                return value
            # color-mix(in srgb, var(--flag-2) 85%, var(--fg)), como en la página.
            mixed = (0.85 * a + 0.15 * b for a, b in zip(_rgb(value), _rgb(color("FG", mode, theme))))
            return "#" + "".join(f"{round(c * 255):02X}" for c in mixed)

        for theme in THEMES:
            for mode in MODES:
                for name in ("ACCENT_DANGER", "FLAG_2", "STATE_REVIEW", "STATE_NEW"):
                    for surface in ("BUTTON_BG", "BUTTON_HOVER"):
                        ratio = contrast(mark(name, mode, theme), color(surface, mode, theme))
                        self.assertGreaterEqual(ratio, 3.0, f"{theme}: {name} sobre {surface} ({mode}): {ratio:.2f}")


class IdentityTest(unittest.TestCase):
    """Nocturne conserva su aspecto original: mismo fondo, mismo azul de acción, y
    los colores con significado mantienen su tono."""

    ORIGINAL = {
        "CANVAS": ("#F7F8FA", "#12161F"),
        "BUTTON_PRIMARY_BG": ("#3B6FE0", "#4066E6"),
        "HIGHLIGHT_BG": ("#3B6FE0", "#4066E6"),
    }
    HUES = {
        "STATE_NEW": ("#1971C2", "#74C0FC"),
        # Versión 3.5.0: «Aprendiendo» en el rojo de la paleta, a petición del cliente.
        "STATE_LEARN": ("#E03131", "#FF6B6B"),
        "STATE_REVIEW": ("#2F9E44", "#57D06B"),
        "ACCENT_DANGER": ("#E03131", "#FF6B6B"),
        "FLAG_1": ("#E03131", "#FF6B6B"),
        "FLAG_2": ("#E8590C", "#FFA94D"),
        "FLAG_3": ("#2F9E44", "#69DB7C"),
        "FLAG_4": ("#1971C2", "#74C0FC"),
        "FLAG_5": ("#C62FAD", "#E599F7"),
        "FLAG_6": ("#099268", "#63E6BE"),
        "FLAG_7": ("#7048E8", "#B197FC"),
        "STATE_MARKED": ("#7048E8", "#B197FC"),
    }

    def test_background_and_accent_unchanged(self) -> None:
        for name, (light, dark) in self.ORIGINAL.items():
            self.assertEqual((color(name, "light"), color(name, "dark")), (light, dark), name)

    def test_corrected_colors_keep_their_hue(self) -> None:
        for name, originals in self.HUES.items():
            for mode, original in zip(MODES, originals):
                delta = hue_distance(color(name, mode), original)
                self.assertLessEqual(delta, 6.0, f"{name} ({mode}): {delta:.1f}°")


if __name__ == "__main__":
    unittest.main()
