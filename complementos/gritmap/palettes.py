"""Escalas de color del mapa.

Los siete temas (diez tonos para los dias pasados) y los diez grises de los
dias futuros son una excepcion a la paleta Nocturne aprobada por el cliente el
2026-10-08: Nocturne no tiene escalas de diez tonos y cada escala ya trae su
pareja de dia y de noche. El resto de colores del mapa (botones, globo, borde
de hoy y de las fechas clave, comparativa) sale de los tokens de Nocturne, en
web/gritmap.css.
"""

# Historial de correcciones de este archivo:
# FIX-008 (2026-10-08) — Las variables y clases de color usaban el prefijo
#                        "shm", que no es el nombre del paquete.

from __future__ import annotations

PAST_LIGHT: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#a6d99e", "#8fd08a", "#77c476", "#60b763", "#4aa852",  # colores-ok: escala aprobada (2026-10-08)
        "#379a45", "#278a39", "#1a782e", "#106425", "#0a511d",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "fire_red": (
        "#f4a9a0", "#f09287", "#ea7b6e", "#e36557", "#d95043",  # colores-ok: escala aprobada (2026-10-08)
        "#cb3f33", "#b93327", "#a2281f", "#881e19", "#6d1613",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "ocean_blue": (
        "#a3cfec", "#88c1e6", "#6db2df", "#54a2d6", "#4090ca",  # colores-ok: escala aprobada (2026-10-08)
        "#2f7ebc", "#226cab", "#185a97", "#104a80", "#0b3a68",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "royal_purple": (
        "#c9b4ea", "#b8a0e3", "#a78bdb", "#9676d1", "#8562c6",  # colores-ok: escala aprobada (2026-10-08)
        "#7450b8", "#6440a8", "#543295", "#452680", "#371c6a",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "sunset_orange": (
        "#f6bd8b", "#f3ab70", "#ef9958", "#e98643", "#e07331",  # colores-ok: escala aprobada (2026-10-08)
        "#d36123", "#c25118", "#ab4210", "#90350b", "#762b08",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "rose_pink": (
        "#f7b3cd", "#f39cbe", "#ee85af", "#e76e9f", "#dd598f",  # colores-ok: escala aprobada (2026-10-08)
        "#cf477e", "#bd386c", "#a62c5b", "#8c214a", "#71183a",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "lagoon_turquoise": (
        "#9adcd6", "#7dd1cb", "#61c4bf", "#48b5b1", "#35a4a1",  # colores-ok: escala aprobada (2026-10-08)
        "#279290", "#1c7f7e", "#146a6a", "#0e5757", "#0a4444",  # colores-ok: escala aprobada (2026-10-08)
    ),
}

PAST_DARK: dict[str, tuple[str, ...]] = {
    "classic_green": (
        "#12482c", "#125532", "#136337", "#15723c", "#1a8340",  # colores-ok: escala aprobada (2026-10-08)
        "#219544", "#2ba74a", "#3aba54", "#4ecd62", "#69df78",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "fire_red": (
        "#521712", "#621c15", "#742118", "#88281b", "#9c301f",  # colores-ok: escala aprobada (2026-10-08)
        "#b13a24", "#c6462b", "#da5535", "#ec6743", "#fb7d55",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "ocean_blue": (
        "#123a58", "#154668", "#185378", "#1c6189", "#22709b",  # colores-ok: escala aprobada (2026-10-08)
        "#2a80ad", "#3491bf", "#42a3d1", "#55b6e2", "#6fc9f1",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "royal_purple": (
        "#31205c", "#3a276c", "#44307c", "#4f3a8d", "#5b459e",  # colores-ok: escala aprobada (2026-10-08)
        "#6851af", "#775fc1", "#886fd2", "#9a81e2", "#ae95f1",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "sunset_orange": (
        "#54260e", "#642d10", "#753512", "#883e15", "#9c4817",  # colores-ok: escala aprobada (2026-10-08)
        "#b0531a", "#c45f1e", "#d76d26", "#e97d33", "#f99046",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "rose_pink": (
        "#5a1734", "#6b1c3e", "#7e2249", "#922955", "#a73162",  # colores-ok: escala aprobada (2026-10-08)
        "#bc3b70", "#d0497f", "#e05b91", "#ec73a5", "#f58fba",  # colores-ok: escala aprobada (2026-10-08)
    ),
    "lagoon_turquoise": (
        "#0d3c3c", "#11494a", "#155758", "#1a6667", "#207677",  # colores-ok: escala aprobada (2026-10-08)
        "#288788", "#33999a", "#41abac", "#55bdbe", "#70cfd0",  # colores-ok: escala aprobada (2026-10-08)
    ),
}

FUTURE_LIGHT: tuple[str, ...] = (
    "#dadde2", "#ced2d8", "#c2c7ce", "#b6bbc4", "#aab0ba",  # colores-ok: escala aprobada (2026-10-08)
    "#9ea5b0", "#929aa6", "#858e9b", "#788290", "#6a7484",  # colores-ok: escala aprobada (2026-10-08)
)

FUTURE_DARK: tuple[str, ...] = (
    "#31353a", "#363b40", "#3c4147", "#42474e", "#484e55",  # colores-ok: escala aprobada (2026-10-08)
    "#4f555d", "#565c64", "#5d646c", "#646b74", "#6c737d",  # colores-ok: escala aprobada (2026-10-08)
)

THEME_NAMES: tuple[str, ...] = tuple(PAST_LIGHT)
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
    color_classes = "".join(
        f"#gritmap-root .gritmap-c{i}{{color:var(--gritmap-p{i});}}" for i in range(1, 11)
    )
    return f"#gritmap-root{{{light}}}{dark_selector}{{{dark}}}{color_classes}"
