"""Escalas de color del mapa.

Los siete temas (diez tonos para los dias pasados) y los diez grises de los
dias futuros son una excepcion a la paleta Nocturne aprobada por el cliente el
2026-10-08: Nocturne no tiene escalas de diez tonos y cada escala ya trae su
pareja de dia y de noche. El resto de colores del mapa (botones, globo, borde
de hoy y marca de las fechas clave, comparativa) sale de los tokens de
Nocturne, en web/gritmap.css.

Version 3.2.0 (aprobada por el cliente el 2026-10-13): las escalas se rehacen
a partir de los tonos de Nocturne. Cada tema toma el matiz de su token
(ACCENT_NOTE, STATE_NEW, STATE_MARKED, ACCENT_DANGER, STATE_LEARN, FLAG_5 y
FLAG_6) y reparte sus diez tonos en escalones iguales de luminosidad
percibida (OKLCH): de dia, de claro (0,82) a oscuro (0,34); de noche, al
reves (0,40 a 0,88), para que mas estudio sea siempre mas contraste con el
fondo. Los grises de los dias futuros siguen la misma idea, con el matiz
azulado de los grises de Nocturne.
"""

# Historial de correcciones de este archivo:
# FIX-008 (2026-10-08) — Las variables y clases de color usaban el prefijo
#                        "shm", que no es el nombre del paquete.

from __future__ import annotations

PAST_LIGHT: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#a8d1aa", "#8fc392", "#75b57a", "#5aa663", "#3c984a",  # colores-ok: escala aprobada (2026-10-13)
        "#0f8a30", "#007826", "#00671f", "#005619", "#004512",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "fire_red": (
        "#f8aea6", "#f3968d", "#ec7e73", "#e4645a", "#dc4640",  # colores-ok: escala aprobada (2026-10-13)
        "#d11e24", "#bb0617", "#a10011", "#88000c", "#6f0008",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "ocean_blue": (
        "#a7c8ec", "#8eb7e6", "#74a7de", "#5a96d7", "#3e85cf",  # colores-ok: escala aprobada (2026-10-13)
        "#1c74c6", "#0b64b1", "#00559a", "#004682", "#00386a",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "royal_purple": (
        "#c0bbff", "#afa6fc", "#9f92f9", "#8f7cf6", "#8065f1",  # colores-ok: escala aprobada (2026-10-13)
        "#734cec", "#643dd4", "#562ebd", "#481ea6", "#3b0a8f",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "sunset_orange": (
        "#f2b39c", "#eb9d7f", "#e48662", "#db6f43", "#d2561c",  # colores-ok: escala aprobada (2026-10-13)
        "#bf4600", "#a63c00", "#8f3200", "#782800", "#611f00",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "rose_pink": (
        "#f3afbb", "#ec97a8", "#e47f96", "#db6683", "#d24b71",  # colores-ok: escala aprobada (2026-10-13)
        "#c72b60", "#b11c52", "#9c0744", "#840038", "#6c002c",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "lagoon_turquoise": (
        "#9bd2bf", "#7cc4ad", "#5ab79b", "#2da98a", "#00987a",  # colores-ok: escala aprobada (2026-10-13)
        "#00866b", "#00755d", "#00644f", "#005341", "#004334",  # colores-ok: escala aprobada (2026-10-13)
    ),
}

PAST_DARK: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#2a522f", "#2d6435", "#2f763b", "#318941", "#319c46",  # colores-ok: escala aprobada (2026-10-13)
        "#31b04c", "#4ec061", "#66d075", "#7de189", "#93f19e",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "fire_red": (
        "#6b3634", "#843e3c", "#9e4544", "#b84d4d", "#d35455",  # colores-ok: escala aprobada (2026-10-13)
        "#ef5c5e", "#fe7170", "#ff918d", "#ffaea9", "#ffc8c4",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "ocean_blue": (
        "#274b67", "#2a5b80", "#2b6a99", "#2b7bb3", "#2a8bce",  # colores-ok: escala aprobada (2026-10-13)
        "#299ce8", "#47adf7", "#69beff", "#91ceff", "#b4ddff",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "royal_purple": (
        "#4a4166", "#594d7e", "#695997", "#7965b1", "#8a72cb",  # colores-ok: escala aprobada (2026-10-13)
        "#9b7fe6", "#ab91f4", "#bba4ff", "#cabaff", "#dad0ff",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "sunset_orange": (
        "#5f4021", "#754c20", "#8b581e", "#a2641a", "#ba7011",  # colores-ok: escala aprobada (2026-10-13)
        "#d27d02", "#e18f32", "#f1a14e", "#ffb469", "#ffcd9d",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "rose_pink": (
        "#6b3341", "#843a4d", "#9e4159", "#b94766", "#d44e73",  # colores-ok: escala aprobada (2026-10-13)
        "#f05481", "#ff6b92", "#ff8da7", "#ffabbc", "#ffc6d0",  # colores-ok: escala aprobada (2026-10-13)
    ),
    "lagoon_turquoise": (
        "#1c5344", "#156451", "#00775f", "#00896d", "#009b7c",  # colores-ok: escala aprobada (2026-10-13)
        "#00ad8b", "#00c09b", "#38d1ab", "#5ae1bd", "#76f2ce",  # colores-ok: escala aprobada (2026-10-13)
    ),
}

FUTURE_LIGHT: tuple[str, ...] = (
    "#d3dae4", "#cbd2dc", "#c3cad4", "#bbc2cc", "#b3bac4",  # colores-ok: escala aprobada (2026-10-13)
    "#acb2bc", "#a4abb5", "#9da3ad", "#959ca5", "#8e949e",  # colores-ok: escala aprobada (2026-10-13)
)

FUTURE_DARK: tuple[str, ...] = (
    "#454b53", "#4c515a", "#525861", "#595f68", "#60666f",  # colores-ok: escala aprobada (2026-10-13)
    "#676d76", "#6e747d", "#757b84", "#7c828c", "#838a93",  # colores-ok: escala aprobada (2026-10-13)
)

THEME_NAMES: tuple[str, ...] = tuple(PAST_LIGHT)
# Temas sobre los que el borde naranja de las fechas clave no se distingue.
WARM_THEMES: frozenset[str] = frozenset({"fire_red", "sunset_orange", "rose_pink"})
# Desde 3.6.0 el borde de las fechas clave sale de las banderas de Nocturne:
# naranja (FLAG_2) y, en los temas calidos, azul (FLAG_4), con su pareja de
# noche. Son marcas, como las banderas de Anki, no colores de accion.
KEY_BLUE_LIGHT = "#1971C2"  # colores-ok: reserva de FLAG_4 de Nocturne (dia)
KEY_BLUE_DARK = "#5993C2"  # colores-ok: reserva de FLAG_4 de Nocturne (noche)
# Tonos que ensena la leyenda: los diez se agrupan de dos en dos y cada
# cuadrito lleva el mas intenso de su pareja (3.6.0).
LEGEND_TONES: tuple[int, ...] = (2, 4, 6, 8, 10)
LEGEND_FACTORS: tuple[float, ...] = (0.125, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 4.0)
STREAK_COLOR_LEVELS: tuple[tuple[int, int], ...] = ((14, 1), (30, 3), (90, 5), (180, 8), (365, 9))
AVG_COLOR_LEVELS: tuple[tuple[int, int], ...] = ((10, 1), (25, 3), (60, 5), (150, 7), (300, 8))
PCT_COLOR_THRESHOLDS: tuple[int, ...] = (25, 50, 60, 70, 80, 85, 90, 95, 99)


def legend_thresholds(reference: float) -> list[float]:
    """Limites de los diez tonos a partir de la referencia de la escala."""
    return [factor * reference for factor in LEGEND_FACTORS]


def level_index(count: float, thresholds: list[float]) -> int:
    for index, threshold in enumerate(thresholds):
        if count <= threshold:
            return index
    return len(thresholds)


def streak_level(value: int) -> int:
    if value <= 0:
        return -1
    for threshold, index in STREAK_COLOR_LEVELS:
        if value <= threshold:
            return index
    return 9


def pct_level(value: int) -> int:
    if value <= 0:
        return -1
    for index, threshold in enumerate(PCT_COLOR_THRESHOLDS):
        if value <= threshold:
            return index
    return 9


def avg_level(value: float) -> int:
    if value <= 0:
        return -1
    for threshold, index in AVG_COLOR_LEVELS:
        if value <= threshold:
            return index
    return 9


def level_class(level: int) -> str:
    return "gritmap-cm" if level < 0 else f"gritmap-c{level + 1}"


def _vars_block(theme: str, dark: bool) -> str:
    past = (PAST_DARK if dark else PAST_LIGHT).get(
        theme, (PAST_DARK if dark else PAST_LIGHT)["classic_green"]
    )
    future = FUTURE_DARK if dark else FUTURE_LIGHT
    parts = [f"--gritmap-p{i + 1}:{color};" for i, color in enumerate(past)]
    parts += [f"--gritmap-f{i + 1}:{color};" for i, color in enumerate(future)]
    if theme in WARM_THEMES:
        # El borde naranja de las fechas clave no se distingue sobre estos
        # temas: pasa al azul de Nocturne (decision del cliente, 2026-10-13).
        fallback = KEY_BLUE_DARK if dark else KEY_BLUE_LIGHT
        parts.append(f"--gritmap-key:var(--flag-4,{fallback});")
    return "".join(parts)


# Selectores de modo noche. Anki marca el modo oscuro de dos formas: con la
# clase night-mode en el elemento raiz (la actual) y con night_mode/nightMode
# en el cuerpo (heredadas). Se cubren todas para que el mapa acierte tanto al
# cargar la pagina como al cambiar de tema sin recargarla.
_DARK_SELECTORS = (
    "html.night-mode #gritmap-root",
    "body.night_mode #gritmap-root",
    "body.nightMode #gritmap-root",
)


def palette_css(theme: str) -> str:
    """Solo las escalas del tema: es lo unico que depende de las opciones.

    La estructura y los colores de la interfaz (tokens de Nocturne) viven en
    web/gritmap.css, que se carga junto con la pagina. Separarlas permite que
    un cambio de tema reescriba unicamente esta lista de variables.
    """
    # --- FIX-008 (2026-10-08) --------------------------------------
    # Sintoma: las variables (--shm-p1...) y clases (.shm-c1...) de color
    #          podian chocar con las de otro complemento en la misma pagina.
    # Causa: el prefijo "shm" venia de un nombre antiguo, no del paquete.
    # Regla: variables, clases y selectores inyectados empiezan por "gritmap".
    # ---------------------------------------------------------------
    light = _vars_block(theme, dark=False)
    dark = _vars_block(theme, dark=True)
    dark_selector = ",".join(_DARK_SELECTORS)
    # Las cifras se escriben en el color del texto, que siempre se lee; el
    # tono del tema va en el cuadrito que llevan delante.
    swatches = "".join(
        f"#gritmap-root .gritmap-c{i}::before{{background:var(--gritmap-p{i});}}"
        for i in range(1, 11)
    )
    return f"#gritmap-root{{{light}}}{dark_selector}{{{dark}}}{swatches}"
