"""Colores de la barra: los seis temas, el dorado y las piezas neutras.

1.5.0 (informe «Rediseño de color y forma: CoreProgress 1.4.0», 2026-11-17,
aplicado entero): una sola receta para los seis temas, calculada en OKLCH por
contraste y no a ojo, para que todos pesen lo mismo. De día, la punta del
relleno queda a 3,1 a 1 del canal y el arranque a 2,0; de noche, a 7,0 y a 4,6.
Croma de 0,16 como máximo de día y 0,15 de noche. Ningún tema queda a menos de
10 de diferencia de color (ΔE2000) del azul de acción de Nocturne. Cada tema
tiene:

- relleno: tres paradas (arranque, centro y punta). De día la punta es el lado
  oscuro; de noche, el claro;
- tinta: texto del aviso, aro y número del próximo hito y chispas. Oscura de
  día (6,5 a 1 contra el fondo) y, de noche, la propia punta;
- píldora: el fondo tintado del aviso.

Sin contorno en los temas: la punta ya da 3,1 a 1 por sí sola. Solo el dorado
de día lo lleva, porque un oro claro no llega a 3 a 1 del canal (1,27; con
contorno, 4,14). La racha dorada lleva además una estrella en la punta.

HISTORIAL: hasta la 1.4.0 cada tema tenía una escala de diez tonos hecha a
mano; pesaban muy distinto (punta de 1,98 a 8,35 a 1 contra el canal de día),
Azul océano era el azul de los botones de Atelier (1,5 de diferencia) y, con
daltonismo, el dorado no se distinguía del verde de serie.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

# Por tema: (relleno de día, tinta de día, píldora de día,
#            relleno de noche, píldora de noche). La tinta de noche es la punta.
_Ramp = tuple[str, str, str]
_Theme = tuple[_Ramp, str, str, _Ramp, str]

THEMES: dict[str, _Theme] = {
    "classic_green": (
        ("#53AD4B", "#329D43", "#0F8B41"), "#09692F", "#E3F6E6",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#3EAC5F", "#5EBD68", "#7BCE73"), "#1C3422",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
    "ocean_blue": (
        ("#16A4DB", "#1391CC", "#0F7FBE"), "#085E8F", "#E3F2FF",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#219EE9", "#26B3F9", "#53C7FD"), "#183042",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
    "lagoon_turquoise": (
        ("#17ACA0", "#139992", "#108784"), "#096462", "#DAF7F5",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#16A8A5", "#1ABCB4", "#1ED1C2"), "#0B3534",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
    "rose_pink": (
        ("#EE7098", "#D95F8F", "#C44E85"), "#943A64", "#FFEAF1",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#E372A3", "#F883AE", "#FDA0BA"), "#3F242F",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
    "royal_purple": (
        ("#B283F0", "#9B74E1", "#8466D1"), "#634C9F", "#F1EEFF",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#A187EE", "#B897FD", "#CCADFD"), "#2F2942",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
    "sunset_orange": (
        ("#E58018", "#D66B12", "#C7570F"), "#96400A", "#FFECE3",  # colores-ok: tema propio (informe del 2026-11-17)
        ("#E67A43", "#F68E4A", "#FDA863"), "#40261A",  # colores-ok: tema propio (informe del 2026-11-17)
    ),
}

# El dorado de la racha (desde 5 aciertos seguidos): claro, más que cualquier
# tema, para que se distinga también por la luminosidad con daltonismo.
GOLD: _Theme = (
    ("#F7D856", "#F6C835", "#F4B81C"), "#845E09", "#FDEFCF",  # colores-ok: dorado propio (informe del 2026-11-17)
    ("#F0BB43", "#F9CD54", "#FEE06D"), "#3C2E0F",  # colores-ok: dorado propio (informe del 2026-11-17)
)

# Piezas neutras de la barra (día, noche), de la tabla Nocturne del informe.
# El canal es el gris que el informe midió como SCROLLBAR_BG; Atelier 3.9.0
# oscureció después ese token (#828893 y #6C7587) para que el tirador llegue a
# 3 a 1, y con él toda la paleta medida dejaría de valer: se queda el valor del
# informe (véase «Así a propósito» en docs/coreprogress/errores.md).
NEUTRAL: dict[str, tuple[str, str]] = {
    "bg": ("#F7F8FA", "#12161F"),  # colores-ok: CANVAS de Nocturne; color del corte de los hitos
    "track": ("#D5D9E2", "#272F3F"),  # colores-ok: canal de la barra (informe del 2026-11-17, 2.1)
    "disc": ("#FBFCFE", "#212836"),  # colores-ok: CANVAS_ELEVATED de Nocturne; fondo de los discos
    "faint": ("#646C7D", "#9AA3B4"),  # colores-ok: FG_FAINT de Nocturne; aro del total
    "subtle": ("#4E576A", "#B7BECC"),  # colores-ok: FG_SUBTLE de Nocturne; número del total
}
# Número sobre la tinta (hito recién alcanzado): casi blanco de día (sin el
# blanco puro) y el fondo de noche.
ON_INK: tuple[str, str] = ("#FBFCFE", "#12161F")  # colores-ok: CANVAS_ELEVATED (día) y CANVAS (noche) de Nocturne

THEME_KEYS: tuple[str, ...] = tuple(THEMES)
# 1.2.0 (informe del 2026-11-09): Rojo fuego se retira, como en GritMap: en Anki
# el rojo significa «Otra vez», aprendiendo y error. Quien lo tenía pasa a
# Naranja atardecer y lo ve avisado en la ventana de opciones.
RETIRED_THEMES: dict[str, str] = {"fire_red": "sunset_orange"}
DEFAULT_THEME: str = "classic_green"


@dataclass(frozen=True)
class ModeStyle:
    gradient: str
    contour: str
    ink: str
    pill: str
    on_ink: str
    # Color de la estrella de la racha dorada; vacío si la barra no es dorada.
    star: str = ""


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
        "contour": mode.contour,
        "ink": mode.ink,
        "pill": mode.pill,
        "onInk": mode.on_ink,
        "star": mode.star,
    }


def _theme(theme: str) -> _Theme:
    return THEMES.get(theme, THEMES[DEFAULT_THEME])


def _gradient(ramp: _Ramp) -> str:
    start, middle, tip = ramp
    return f"linear-gradient(90deg,{start} 0%,{middle} 50%,{tip} 100%)"


def ink(theme: str, dark: bool, gold_active: bool = False) -> str:
    """La tinta del tema (o del dorado) en el modo pedido."""
    data = GOLD if gold_active else _theme(theme)
    return data[3][2] if dark else data[1]


def _mode_style(theme: str, dark: bool, gold_active: bool) -> ModeStyle:
    data = GOLD if gold_active else _theme(theme)
    ramp = data[3] if dark else data[0]
    pill = data[4] if dark else data[2]
    tinta = ink(theme, dark, gold_active)
    contour = f"inset 0 0 0 1px {tinta}" if gold_active and not dark else "none"
    star = (NEUTRAL["bg"][1] if dark else tinta) if gold_active else ""
    return ModeStyle(
        gradient=_gradient(ramp),
        contour=contour,
        ink=tinta,
        pill=pill,
        on_ink=ON_INK[1] if dark else ON_INK[0],
        star=star,
    )


def fill_bundle(theme: str, gold_active: bool) -> StyleBundle:
    return StyleBundle(
        light=_mode_style(theme, dark=False, gold_active=gold_active),
        dark=_mode_style(theme, dark=True, gold_active=gold_active),
    )


def neutral(dark: bool) -> dict[str, str]:
    """Las piezas neutras de la barra en un modo."""
    return {name: pair[1] if dark else pair[0] for name, pair in NEUTRAL.items()}


def swatch(theme: str, dark: bool = False) -> str:
    """Muestra del tema en la ventana de opciones (1.5.0): una minibarra con el
    degradado del modo activo, que enseña lo que se va a ver."""
    return _gradient(_theme(theme)[3] if dark else _theme(theme)[0])


def preview_style(theme: str, dark: bool) -> dict[str, str]:
    """Degradado y tinta de un tema, para la vista previa de las opciones."""
    mode = _mode_style(theme, dark, gold_active=False)
    return {"gradient": mode.gradient, "ink": mode.ink}
