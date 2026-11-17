"""Colores de ProFeedback: botones, insignias, confeti y título del fin del día.

2.6.0 (informe «Rediseño de color y forma: ProFeedback 2.5.0» del 2026-11-17, aplicado entero,
con la opción recomendada en sus tres decisiones): una paleta propia, calculada por contraste
en OKLCH y no a ojo, que sustituye a los colores de Duolingo del original.

- Cuatro familias de siempre (rojo coral, ámbar, verde jade, azul cielo), con el tono muy
  cerca de las franjas de respuesta de Atelier. «Difícil» y «Bien» se separan con daltonismo
  (de 2,3 a 17,0 de diferencia con deuteranopía).
- Cada modo con su paleta: de noche, un 15 % menos de croma.
- La letra es un tono muy oscuro del mismo color, nunca un gris.
- De día, el canto del botón da 3 a 1 contra la barra: el botón se ve como botón.
- Con el ratón encima, la cara se aleja de su letra (+0,03 de luminosidad; en «Mostrar
  respuesta», con letra clara, −0,03).
- «Mostrar respuesta» va en el azul de acción de Atelier (decisión 1): el oro queda solo
  para celebrar haber terminado, como en CoreProgress.

Sin Qt ni colección: se prueba suelto. Todo el CSS de colores sale de aquí (css_vars) y se
incrusta en la página antes del primer pintado; el confeti recibe sus colores en JSON.
"""

from __future__ import annotations

import json
from typing import Final, NamedTuple


class Pair(NamedTuple):
    day: str
    night: str


class ButtonColors(NamedTuple):
    face: Pair
    ink: Pair
    edge: Pair
    hover: Pair


# Botones de respuesta, por número de respuesta de Anki (1 «Otra vez» … 4 «Fácil»).
BUTTONS: Final[dict[int, ButtonColors]] = {
    1: ButtonColors(
        Pair("#F47B72", "#E8847B"),  # colores-ok: cara de «Otra vez» (informe del 2026-11-17)
        Pair("#2F0405", "#2F0404"),  # colores-ok: letra de «Otra vez»
        Pair("#DB655D", "#C05F58"),  # colores-ok: canto de «Otra vez»
        Pair("#FD867C", "#F38D84"),  # colores-ok: ratón encima de «Otra vez»
    ),
    2: ButtonColors(
        Pair("#FDB354", "#F8B564"),  # colores-ok: cara de «Difícil»
        Pair("#311C01", "#311C01"),  # colores-ok: letra de «Difícil»
        Pair("#C78112", "#D08F3C"),  # colores-ok: canto de «Difícil»
        Pair("#FEC178", "#FEC178"),  # colores-ok: ratón encima de «Difícil»
    ),
    3: ButtonColors(
        Pair("#53E2A6", "#70DDAB"),  # colores-ok: cara de «Bien»
        Pair("#01291A", "#01291A"),  # colores-ok: letra de «Bien»
        Pair("#15A472", "#46B686"),  # colores-ok: canto de «Bien»
        Pair("#5FECAF", "#7AE7B5"),  # colores-ok: ratón encima de «Bien»
    ),
    4: ButtonColors(
        Pair("#73C9FB", "#7FC8F3"),  # colores-ok: cara de «Fácil»
        Pair("#012537", "#012537"),  # colores-ok: letra de «Fácil»
        Pair("#4098C9", "#5AA1CB"),  # colores-ok: canto de «Fácil»
        Pair("#88D1FD", "#89D1FD"),  # colores-ok: ratón encima de «Fácil»
    ),
}

# «Mostrar respuesta» (decisión 1, opción A): el azul de acción de Nocturne y su canto
# (BUTTON_PRIMARY_BG y NOCTURNE_PRIMARY_PRESSED). Con el ratón encima oscurece: la letra es
# clara y así gana contraste (de 4,63 a 5,23 de día).
SHOW_ANSWER: Final[ButtonColors] = ButtonColors(
    Pair("#3B6FE0", "#4066E6"),  # colores-ok: BUTTON_PRIMARY_BG de Nocturne
    Pair("#FFFFFF", "#FFFFFF"),  # colores-ok: HIGHLIGHT_FG de Nocturne, la letra sobre el azul de acción
    Pair("#284EAA", "#2B45AA"),  # colores-ok: NOCTURNE_PRIMARY_PRESSED
    Pair("#3366D6", "#385CDC"),  # colores-ok: azul de acción 0,03 más oscuro (informe, 3.1)
)

# Fondo de la barra y de la tarjeta (CANVAS de Nocturne), contra el que se miden los cantos.
CANVAS: Final[Pair] = Pair("#F7F8FA", "#12161F")  # colores-ok: CANVAS de Nocturne


class BadgeColors(NamedTuple):
    text: Pair
    icon: Pair


# Insignias: las tres pesan igual (texto a 6,8 de día y 8,5 de noche; icono a 3,4 de día).
# Desde la 2.6.1 el icono es solo el dibujo, sin círculo de fondo.
BADGES: Final[dict[str, BadgeColors]] = {
    "new_card": BadgeColors(
        Pair("#73428F", "#CDA1E9"),  # colores-ok: texto de «TARJETA NUEVA»
        Pair("#A572C4", "#CDA1E9"),  # colores-ok: icono de «TARJETA NUEVA»
    ),
    "hard_exercise": BadgeColors(
        Pair("#9B322F", "#F9988E"),  # colores-ok: texto de «SE RESISTE»
        Pair("#D3655E", "#F9988E"),  # colores-ok: icono de «SE RESISTE»
    ),
    "previous_mistake": BadgeColors(
        Pair("#7A4D07", "#E0A761"),  # colores-ok: texto de «OTRA OPORTUNIDAD»
        Pair("#BA7816", "#E0A761"),  # colores-ok: icono de «OTRA OPORTUNIDAD»
    ),
}

# Confeti. Fin de mazo: las cuatro caras y sus cantos (día) o su tono de ratón encima
# (noche). Fin del día: oros calculados por contraste; los claros salen el doble.
CONFETTI_DECK: Final[Pair] = Pair(
    "#F47B72 #DB655D #FDB354 #C78112 #53E2A6 #15A472 #73C9FB #4098C9",  # colores-ok: confeti de mazo (día)
    "#E8847B #F38D84 #F8B564 #FEC178 #70DDAB #7AE7B5 #7FC8F3 #89D1FD",  # colores-ok: confeti de mazo (noche)
)
CONFETTI_DAY: Final[Pair] = Pair(
    "#E9AC1A #E9AC1A #CB9515 #CB9515 #AF8110 #845E09",  # colores-ok: lluvia dorada (día)
    "#F0BB43 #F9CD54 #F9CD54 #FEE06D #FEE06D #FFF0C4",  # colores-ok: lluvia dorada (noche), oros de CoreProgress
)
# Destellos fijos con «reducir movimiento»: jade, ámbar y cielo (mazo) u oro (día).
SPARKLES_DECK: Final[Pair] = Pair(
    "#15A472 #C78112 #4098C9",  # colores-ok: destellos fijos de mazo (día), cantos de Bien, Difícil y Fácil
    "#70DDAB #F8B564 #7FC8F3",  # colores-ok: destellos fijos de mazo (noche), caras de Bien, Difícil y Fácil
)
SPARKLES_DAY: Final[Pair] = Pair(
    "#AF8110 #845E09 #AF8110",  # colores-ok: destellos dorados fijos (día)
    "#F9CD54 #FEE06D #F9CD54",  # colores-ok: destellos dorados fijos (noche)
)
# Título del fin del día: el oro de CoreProgress (tinta de día y punta de noche) y la banda
# del brillo, que de día mantiene la letra a 4,6 a 1 durante la pasada.
TITLE: Final[Pair] = Pair("#845E09", "#FEE06D")  # colores-ok: oro de CoreProgress
TITLE_BAND: Final[Pair] = Pair("#926A0C", "#FFF6D6")  # colores-ok: banda del brillo del título

_EASE_NAMES: Final[dict[int, str]] = {1: "again", 2: "hard", 3: "good", 4: "easy"}


def _vars(night: bool) -> str:
    pick = 1 if night else 0
    parts: list[str] = []
    for ease, colors in BUTTONS.items():
        name = _EASE_NAMES[ease]
        for field, pair in zip(("face", "ink", "edge", "hover"), colors):
            parts.append(f"--profeedback-{name}-{field}:{pair[pick]}")
    for field, pair in zip(("face", "ink", "edge", "hover"), SHOW_ANSWER):
        parts.append(f"--profeedback-show-{field}:{pair[pick]}")
    for key, badge in BADGES.items():
        name = key.replace("_", "-")
        for field, pair in zip(("text", "icon"), badge):
            parts.append(f"--profeedback-{name}-{field}:{pair[pick]}")
    return ";".join(parts)


def css_vars() -> str:
    """Las variables de color de la barra de botones y de la insignia, de día y de noche."""
    return f":root{{{_vars(False)}}}:is(.night_mode,.nightMode){{{_vars(True)}}}"


def celebration_colors() -> str:
    """Colores del confeti, de los destellos fijos y del título, en JSON para el motor."""

    def split(pair: Pair) -> dict[str, list[str]]:
        return {"day": pair.day.split(), "night": pair.night.split()}

    return json.dumps(
        {
            "deck": split(CONFETTI_DECK),
            "gold": split(CONFETTI_DAY),
            "sparklesDeck": split(SPARKLES_DECK),
            "sparklesGold": split(SPARKLES_DAY),
            "title": {"day": TITLE.day, "night": TITLE.night},
            "band": {"day": TITLE_BAND.day, "night": TITLE_BAND.night},
        },
        separators=(",", ":"),
    )
