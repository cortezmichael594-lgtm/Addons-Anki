"""Pruebas del aspecto de la 2.6.0 (informe «Rediseño de color y forma: ProFeedback 2.5.0»,
2026-11-17), sin Anki a la vista: contrastes de la paleta, diferencia entre botones con
daltonismo, que las insignias no se parezcan a las banderas de Anki, el CSS de colores que
llega a la página y la regla de FIX-007.
"""

from __future__ import annotations

import json
import math
import unittest
from unittest import mock

from profeedback import badges, feedback, look
from profeedback.config import AddonConfig


def _linear(hex_color: str) -> tuple[float, float, float]:
    values = [int(hex_color.lstrip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values)
    return r, g, b


def _lum(hex_color: str) -> float:
    r, g, b = _linear(hex_color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _ratio(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _lab_from_linear(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (min(1.0, max(0.0, v)) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def _de2000(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    """Diferencia de color CIEDE2000 (Sharma, Wu y Dalal, 2005)."""
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    cb = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(cb**7 / (cb**7 + 25**7)))
    a1p, a2p = a1 * (1 + g), a2 * (1 + g)
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dl, dc = l2 - l1, c2p - c1p
    dh = h2p - h1p
    if c1p * c2p == 0:
        dh = 0
    elif dh > 180:
        dh -= 360
    elif dh < -180:
        dh += 360
    dhh = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))
    lbp, cbp = (l1 + l2) / 2, (c1p + c2p) / 2
    if c1p * c2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    t = (
        1
        - 0.17 * math.cos(math.radians(hbp - 30))
        + 0.24 * math.cos(math.radians(2 * hbp))
        + 0.32 * math.cos(math.radians(3 * hbp + 6))
        - 0.20 * math.cos(math.radians(4 * hbp - 63))
    )
    sl = 1 + 0.015 * (lbp - 50) ** 2 / math.sqrt(20 + (lbp - 50) ** 2)
    sc = 1 + 0.045 * cbp
    sh = 1 + 0.015 * cbp * t
    rt = -2 * math.sqrt(cbp**7 / (cbp**7 + 25**7)) * math.sin(math.radians(60 * math.exp(-(((hbp - 275) / 25) ** 2))))
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dhh / sh) ** 2 + rt * (dc / sc) * (dhh / sh))


# Matrices de Machado, Oliveira y Fernandes (2009), grado máximo, en sRGB lineal.
_CVD = {
    "protanopía": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deuteranopía": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
}


def _seen(hex_color: str, matrix: tuple[tuple[float, float, float], ...] | None = None) -> tuple[float, float, float]:
    rgb = _linear(hex_color)
    if matrix is not None:
        rgb = tuple(sum(row[i] * rgb[i] for i in range(3)) for row in matrix)  # type: ignore[assignment]
    return _lab_from_linear(rgb)


class PaletteTests(unittest.TestCase):
    def test_every_text_reads_well(self) -> None:
        # 1.4: todas las letras quedan iguales o mejor que antes; «Otra vez» pasa de 5,09 a ~7.
        for ease, colors in look.BUTTONS.items():
            for mode in (0, 1):
                self.assertGreaterEqual(_ratio(colors.ink[mode], colors.face[mode]), 6.9, (ease, mode))
                self.assertGreaterEqual(_ratio(colors.ink[mode], colors.hover[mode]), 7.5, (ease, mode))
        show = look.SHOW_ANSWER
        for mode in (0, 1):
            self.assertGreaterEqual(_ratio(show.ink[mode], show.face[mode]), 4.5, mode)
            # Con el ratón encima oscurece: la letra clara gana contraste.
            self.assertGreater(_ratio(show.ink[mode], show.hover[mode]), _ratio(show.ink[mode], show.face[mode]))

    def test_buttons_look_like_buttons_by_day(self) -> None:
        # Regla 4: de día el canto da 3 a 1 contra la barra; de noche, la cara.
        for ease, colors in look.BUTTONS.items():
            self.assertGreaterEqual(_ratio(colors.edge.day, look.CANVAS.day), 2.99, ease)
            self.assertGreaterEqual(_ratio(colors.face.night, look.CANVAS.night), 6.9, ease)

    def test_hard_and_good_apart_with_colour_blindness(self) -> None:
        # 5.2: ningún par de botones baja de 10 con protanopía ni deuteranopía (antes, 2,3).
        for name, matrix in _CVD.items():
            for mode in (0, 1):
                faces = [colors.face[mode] for colors in look.BUTTONS.values()]
                worst = min(
                    _de2000(_seen(a, matrix), _seen(b, matrix)) for i, a in enumerate(faces) for b in faces[i + 1 :]
                )
                self.assertGreaterEqual(worst, 10, (name, mode))

    def test_badges_weigh_the_same_and_are_not_anki_flags(self) -> None:
        # 2.4: texto a 6,8 de día y 8,5 de noche; icono a 3,4 de día; lejos de las banderas 1 y 7.
        for key, badge in look.BADGES.items():
            self.assertGreaterEqual(_ratio(badge.text.day, look.CANVAS.day), 6.7, key)
            self.assertGreaterEqual(_ratio(badge.text.night, look.CANVAS.night), 8.4, key)
            self.assertGreaterEqual(_ratio(badge.icon.day, look.CANVAS.day), 3.0, key)
            self.assertGreaterEqual(_ratio(badge.icon.night, look.CANVAS.night), 3.0, key)
        flag1, flag7 = "#BE1D1D", "#7048E8"
        self.assertGreater(_de2000(_seen(look.BADGES["hard_exercise"].text.day), _seen(flag1)), 7)
        self.assertGreater(_de2000(_seen(look.BADGES["new_card"].text.day), _seen(flag7)), 10)

    def test_gold_only_celebrates(self) -> None:
        # Regla 5: ningún botón es dorado; el título usa el oro de CoreProgress.
        self.assertEqual(look.SHOW_ANSWER.face, ("#3B6FE0", "#4066E6"))
        self.assertEqual(look.TITLE, ("#845E09", "#FEE06D"))
        self.assertGreaterEqual(_ratio(look.TITLE.day, look.CANVAS.day), 4.5)
        self.assertGreaterEqual(_ratio(look.TITLE_BAND.day, look.CANVAS.day), 4.5)

    def test_colours_reach_the_page(self) -> None:
        css = look.css_vars()
        self.assertIn("--profeedback-again-face:#F47B72", css)
        self.assertIn(":is(.night_mode,.nightMode){", css)
        self.assertIn("--profeedback-show-hover:#385CDC", css)
        self.assertIn("--profeedback-new-card-icon:#CDA1E9", css)
        data = json.loads(look.celebration_colors())
        self.assertEqual(len(data["deck"]["day"]), 8)
        self.assertEqual(len(data["gold"]["night"]), 6)
        self.assertEqual(len(data["sparklesDeck"]["day"]), 3)

    def test_badge_icons_draw_with_current_colour(self) -> None:
        for flag in ("new_card", "hard_exercise", "previous_mistake"):
            markup = badges.badge_html(flag)  # type: ignore[arg-type]
            # 2.6.1 (petición de la persona): sin círculo de fondo, solo el dibujo.
            self.assertNotIn("<circle", markup)
            self.assertIn("currentColor", markup)
        self.assertNotIn("Feather Bold.ttf", feedback._FONT_FILENAMES)


class PreviewTests(unittest.TestCase):
    def test_confetti_has_a_preview_button(self) -> None:
        # 2.7: «Ver» junto a «Confeti al terminar», que enseña el confeti de mazo.
        from profeedback import celebration, dialogs

        page = dialogs.page(AddonConfig(), {"correct": [], "wrong": [], "deck_finish": [], "all_finish": []})
        checks = [item for card in page["cards"] for item in card["items"] if item["type"] == "check"]
        confetti = next(item for item in checks if item["key"] == "confettiEnabled")
        self.assertEqual(confetti["test"]["action"], dialogs.PREVIEW_CONFETTI)
        # 2.6.1: con «reducir movimiento», «Ver» explica por qué no hay confeti.
        self.assertTrue(confetti["test"]["reduced"])
        self.assertTrue(all("test" not in item for item in checks if item is not confetti))
        script = celebration.preview_script()
        self.assertIn("window.profeedbackConfetti.burst(", script)
        self.assertIn("#F47B72", script)


class BadgeStyleTests(unittest.TestCase):
    # --- FIX-007: el estilo de la insignia se carga en el repaso aunque esté desactivada.
    def test_badge_style_loads_even_when_badges_are_off(self) -> None:
        from aqt.reviewer import Reviewer
        from aqt.webview import WebContent

        content = WebContent()
        reviewer = object.__new__(Reviewer)
        with mock.patch.object(feedback.config, "get", return_value=AddonConfig(flagsEnabled=False)):
            feedback._on_webview_will_set_content(content, reviewer)
        self.assertIn("profeedback-badge", content.head)
        self.assertIn("--profeedback-hard-exercise-text", content.head)


class BadgeGapTests(unittest.TestCase):
    def test_gap_per_badge(self) -> None:
        # 2.6.2: 6 px entre icono y texto en «TARJETA NUEVA» y «OTRA OPORTUNIDAD»; 8 en «SE RESISTE».
        from pathlib import Path

        css = (Path(badges.__file__).parent / "web" / "flags.css").read_text(encoding="utf-8")
        for modifier, gap in (("new-card", 6), ("previous-mistake", 6), ("hard-exercise", None)):
            block = css.split(f".profeedback-badge--{modifier} {{", 1)[1].split("}", 1)[0]
            if gap is None:
                self.assertNotIn("gap:", block)
            else:
                self.assertIn(f"gap: {gap}px;", block)
        self.assertIn("gap: 8px;", css.split(".profeedback-badge {", 1)[1].split("}", 1)[0])


class PanelOpensLikeAnyWindowTests(unittest.TestCase):
    # --- FIX-009: la ventana de opciones no juega con su opacidad (destello en Windows); solo
    # la página espera oculta.
    def test_no_window_opacity_trick(self) -> None:
        from pathlib import Path

        source = (Path(badges.__file__).parent / "panel.py").read_text(encoding="utf-8")
        code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith("#"))
        self.assertNotIn("setWindowOpacity", code)
        self.assertIn("self._web.hide()", code)


if __name__ == "__main__":
    unittest.main()
