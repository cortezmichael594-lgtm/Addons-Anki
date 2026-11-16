"""Color palettes and style-bundle generation for the progress bar.

Each theme ships a 10-step light ramp (light -> dark) and a 10-step dark ramp
(dark -> light), generated with a smooth HLS profile. Neutral parts of the bar
(track, pending checkpoints) are painted in JS from the card's real rendered
background (see view.py), so nothing here needs to know about Anki themes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

ACCENT_LIGHT: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#c9e9cf", "#ace2b6", "#89dc99", "#64d97a", "#3dd65a",  # colores-ok: escala propia del tema (decisión del autor)
        "#25cb44", "#1daf38", "#18932f", "#167628", "#145a21",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "ocean_blue": (
        "#c8d2ea", "#aabce4", "#85a2e0", "#5f87dd", "#376bdd",  # colores-ok: escala propia del tema (decisión del autor)
        "#1e56d2", "#1649b6", "#133d98", "#12337a", "#11295d",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "lagoon_turquoise": (
        "#c7eae6", "#a9e5de", "#84e1d6", "#5de0d0", "#34dfcc",  # colores-ok: escala propia del tema (decisión del autor)
        "#1bd5bf", "#14b8a5", "#119a8a", "#107c70", "#105e55",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "rose_pink": (
        "#eac8d5", "#e4aac0", "#df86a8", "#dd608f", "#db3876",  # colores-ok: escala propia del tema (decisión del autor)
        "#d11f62", "#b41853", "#971445", "#791339", "#5c122e",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "royal_purple": (
        "#d0c8e9", "#b8aae3", "#9c86df", "#7e60dc", "#7450b8",  # colores-ok: escala propia del tema (decisión del autor)
        "#4b20d0", "#3e18b4", "#341496", "#2c1379", "#24125c",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "sunset_orange": (
        "#ead6c7", "#e5c2a9", "#e1aa84", "#e0935d", "#df7b34",  # colores-ok: escala propia del tema (decisión del autor)
        "#d5681b", "#b85814", "#9a4911", "#7c3d10", "#5e3010",  # colores-ok: escala propia del tema (decisión del autor)
    ),
}

ACCENT_DARK: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#21572b", "#256d32", "#288339", "#2a9d40", "#2db947",  # colores-ok: escala propia del tema (decisión del autor)
        "#33d151", "#4bd865", "#68dc7e", "#88e098", "#a7e4b3",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "ocean_blue": (
        "#1e3159", "#223a70", "#244387", "#254ca2", "#2757bf",  # colores-ok: escala propia del tema (decisión del autor)
        "#2c62d8", "#4575de", "#638ae1", "#84a2e4", "#a5b9e7",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "lagoon_turquoise": (
        "#1d5a53", "#207168", "#22897d", "#23a495", "#24c1af",  # colores-ok: escala propia del tema (decisión del autor)
        "#29dbc6", "#42e0ce", "#60e3d4", "#82e5da", "#a4e8e0",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "rose_pink": (
        "#591f35", "#6f223f", "#862449", "#a12654", "#be2860",  # colores-ok: escala propia del tema (decisión del autor)
        "#d72d6d", "#dd467f", "#e06493", "#e385a8", "#e6a5be",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "royal_purple": (
        "#2d1f59", "#35236f", "#3d2586", "#4427a0", "#4d28bd",  # colores-ok: escala propia del tema (decisión del autor)
        "#572ed6", "#6b46dc", "#8264e0", "#9c85e3", "#b5a5e6",  # colores-ok: escala propia del tema (decisión del autor)
    ),
    "sunset_orange": (
        "#5a371d", "#714220", "#894c22", "#a45823", "#c16524",  # colores-ok: escala propia del tema (decisión del autor)
        "#db7329", "#e18442", "#e39660", "#e5ab82", "#e8c0a4",  # colores-ok: escala propia del tema (decisión del autor)
    ),
}

GOLD_LIGHT: tuple[str, ...] = (
    "#ebe1c6", "#e6d5a7", "#e3c882", "#e3bd59", "#e4b230",  # colores-ok: escala propia del tema (decisión del autor)
    "#daa416", "#bc8d10", "#9e760d", "#7f5f0e", "#60490e",  # colores-ok: escala propia del tema (decisión del autor)
)

GOLD_DARK: tuple[str, ...] = (
    "#5c4a1c", "#735c1e", "#8b6e20", "#a78220", "#c59820",  # colores-ok: escala propia del tema (decisión del autor)
    "#dfac25", "#e4b73e", "#e7c15d", "#e8cb80", "#e9d6a2",  # colores-ok: escala propia del tema (decisión del autor)
)

THEME_KEYS: tuple[str, ...] = tuple(ACCENT_LIGHT)
# 1.2.0 (informe del 2026-11-09): Rojo fuego se retira, como en GritMap: en Anki
# el rojo significa «Otra vez», aprendiendo y error, y una barra de avance roja
# decia «error» mientras decia «progreso». Quien lo tenia pasa a Naranja
# atardecer y lo ve avisado en la ventana de opciones.
RETIRED_THEMES: dict[str, str] = {"fire_red": "sunset_orange"}
DEFAULT_THEME: str = "classic_green"

# Indices into a ramp used for the four-stop fill gradient.
# HISTORIAL: en modo claro el degradado usaba (4,5,6,7) y su tramo final era
# casi negro ("demasiado oscuro"); se desplaza a (3,4,5,6): vivo sin apagarse.
# En modo oscuro (5,6,7,8) resultaba demasiado luminoso; (4,5,6,7) lo atenúa
# un punto sin perder identidad. Hitos y textos derivan de estas mismas rampas,
# así que el cambio es coherente en toda la barra.
_FILL_IDX_LIGHT: tuple[int, int, int, int] = (3, 4, 5, 6)
_FILL_IDX_DARK: tuple[int, int, int, int] = (4, 5, 6, 7)

# 1.3.0 (informe del 2026-11-16, 8.2 y 8.3): cada tema tiene una «tinta», el
# color de su aviso (el tono 8 de su rampa: oscuro de día y claro de noche).
# Con ella se pintan el texto del aviso, el contorno del relleno, el disco del
# hito alcanzado y el contorno de la muestra en las opciones. El dorado de día
# lleva un dorado profundo nuevo, solo para texto y contorno: el de antes
# (#BC8D10) daba 2,84 a 1 sobre el fondo claro; este da 5,27.
GOLD_INK_LIGHT: str = "#856206"  # colores-ok: dorado profundo de día (informe del 2026-11-16)
GOLD_INK_DARK: str = "#e7c15d"  # colores-ok: tinta dorada de noche, de la rampa dorada
# Número del hito alcanzado sobre la tinta: blanco de día y FG de noche.
REACHED_TEXT_LIGHT: str = "#ffffff"  # colores-ok: blanco sobre la tinta oscura de día (5,07 a 1 o más)
REACHED_TEXT_DARK: str = "#1b2430"  # colores-ok: FG de día de Nocturne sobre la tinta clara de noche


@dataclass(frozen=True)
class ModeStyle:
    gradient: str
    fill_shadow: str
    solid: str
    label_glow: str
    reached_text: str = REACHED_TEXT_LIGHT


@dataclass(frozen=True)
class StyleBundle:
    light: ModeStyle
    dark: ModeStyle

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {"light": _mode_dict(self.light), "dark": _mode_dict(self.dark)}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"))


def _mode_dict(mode: ModeStyle) -> dict[str, str]:
    return {
        "gradient": mode.gradient,
        "shadow": mode.fill_shadow,
        "solid": mode.solid,
        "glow": mode.label_glow,
        "reached": mode.reached_text,
    }


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgba(hex_color: str, alpha: float) -> str:
    r, g, b = _hex_to_rgb(hex_color)
    return f"rgba({r},{g},{b},{alpha:.2f})"


def _scale(theme: str, dark: bool) -> tuple[str, ...]:
    table = ACCENT_DARK if dark else ACCENT_LIGHT
    return table.get(theme, table[DEFAULT_THEME])


def _gold_scale(dark: bool) -> tuple[str, ...]:
    return GOLD_DARK if dark else GOLD_LIGHT


def _gradient(tones: tuple[str, str, str, str]) -> str:
    a, b, c, d = tones
    return f"linear-gradient(90deg,{a} 0%,{b} 30%,{c} 70%,{d} 100%)"


def _gold_glow(dark: bool) -> str:
    # HISTORIAL: el aura dorada empezó en 12px/0.38 de alfa y "distraía"; se ha
    # rebajado dos veces a petición del usuario. Debe ser un adorno, no un foco.
    scale = _gold_scale(dark)
    outer = scale[7] if dark else scale[5]
    inner = scale[8] if dark else scale[6]
    return f"0 0 6px {_rgba(outer, 0.18)}, 0 0 2px {_rgba(inner, 0.14)}"


def ink(theme: str, dark: bool, gold_active: bool = False) -> str:
    """La tinta del tema (o del dorado) en el modo pedido."""
    if gold_active:
        return GOLD_INK_DARK if dark else GOLD_INK_LIGHT
    return _scale(theme, dark)[8]


def _mode_style(theme: str, dark: bool, gold_active: bool) -> ModeStyle:
    """Relleno plano con contorno (1.3.0, informe del 2026-11-16, decisión 3:
    sin brillo de cristal ni sombra de color). El contorno de 1 px en la tinta
    separa el relleno del canal de día (Verde, Turquesa y dorado quedaban entre
    1,98 y 2,40 a 1). La única luz de la barra es el halo del dorado."""
    tones = _gold_scale(dark) if gold_active else _scale(theme, dark)
    idx = _FILL_IDX_DARK if dark else _FILL_IDX_LIGHT
    picked = (tones[idx[0]], tones[idx[1]], tones[idx[2]], tones[idx[3]])
    solid = ink(theme, dark, gold_active)
    contour = f"inset 0 0 0 1px {solid}"
    fill_shadow = f"{contour}, {_gold_glow(dark)}" if gold_active else contour
    return ModeStyle(
        gradient=_gradient(picked),
        fill_shadow=fill_shadow,
        solid=solid,
        label_glow="none",
        reached_text=REACHED_TEXT_DARK if dark else REACHED_TEXT_LIGHT,
    )


def fill_bundle(theme: str, gold_active: bool) -> StyleBundle:
    return StyleBundle(
        light=_mode_style(theme, dark=False, gold_active=gold_active),
        dark=_mode_style(theme, dark=True, gold_active=gold_active),
    )


def swatch(theme: str, dark: bool = False) -> str:
    """Muestra del tema en la ventana de opciones, en el tono del modo activo
    (1.2.0: se elige lo que se va a ver). El tono central del relleno.

    HISTORIAL: con el índice 6 (tono profundo) el cuadrito morado
    "desaparecía" sobre el diálogo oscuro: se usa la zona media de la rampa.
    """
    return _scale(theme, dark=dark)[5 if dark else 4]

def preview_style(theme: str, dark: bool) -> dict[str, str]:
    """Degradado y tinta de un tema, para la vista previa de las opciones."""
    mode = _mode_style(theme, dark, gold_active=False)
    return {"gradient": mode.gradient, "ink": mode.solid, "reached": mode.reached_text}
