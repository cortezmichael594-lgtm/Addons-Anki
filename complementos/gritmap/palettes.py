"""Escalas de color del mapa.

Version 4.0.0 (informe de rediseno aprobado por el cliente el 2026-10-21):
cinco niveles de un solo color por tema, el gris de los dias sin estudio y
cuatro tonos, en lugar de diez. Asi cada cuadrito del mapa tiene su pareja
exacta en la leyenda y cada tono se distingue del vecino (salto de 1,5 a 1,9
veces en luminosidad, frente a 1,2 con diez). Quedan cuatro temas: Verde,
Azul, Morado y Naranja. Rojo fuego se retira porque en la interfaz el rojo
significa error; Rosa suave y Turquesa laguna duplicaban a Morado y Azul.
Quien tuviera uno de ellos pasa al mas cercano (RETIRED_THEMES).

Los cuatro tonos de cada tema son colores propios, fuera de la paleta
Nocturne, que no tiene escalas: los aprobo el cliente con el informe, con su
pareja de noche (mas luminoso cuanto mas estudio, para que mas estudio sea
siempre mas contraste con el fondo). El resto de colores del mapa sale de los
tokens de Nocturne, en web/gritmap.css. Los dias pendientes ya no tienen
escala de grises: llevan un punto (una forma, no un tono).
"""

# Historial de correcciones de este archivo:
# FIX-008 (2026-10-08) — Las variables y clases de color usaban el prefijo
#                        "shm", que no es el nombre del paquete.

from __future__ import annotations

PAST_LIGHT: dict[str, tuple[str, ...]] = {
    "classic_green": ("#95CF96", "#5DAA61", "#2D8336", "#0E5A1A"),  # colores-ok: escala aprobada (2026-10-21)
    "ocean_blue": ("#8CC3FC", "#519AE2", "#1B71BC", "#004C86"),  # colores-ok: escala aprobada (2026-10-21)
    "royal_purple": ("#C7AFF5", "#A281D9", "#7C58B3", "#553781"),  # colores-ok: escala aprobada (2026-10-21)
    "sunset_orange": ("#F0AD7F", "#D17D3E", "#A75605", "#723902"),  # colores-ok: escala aprobada (2026-10-21)
}

PAST_DARK: dict[str, tuple[str, ...]] = {
    "classic_green": ("#335735", "#4C844F", "#6CB26F", "#9DDE9E"),  # colores-ok: escala aprobada (2026-10-21)
    "ocean_blue": ("#2E5072", "#4378AD", "#61A3E6", "#A2CFFF"),  # colores-ok: escala aprobada (2026-10-21)
    "royal_purple": ("#53446E", "#7E66A6", "#AA8DDE", "#D3BDFE"),  # colores-ok: escala aprobada (2026-10-21)
    "sunset_orange": ("#6A4225", "#A16336", "#D78951", "#FFB98A"),  # colores-ok: escala aprobada (2026-10-21)
}

THEME_NAMES: tuple[str, ...] = tuple(PAST_LIGHT)
# Temas retirados en la 4.0.0 y el tema al que pasa quien los tenia.
RETIRED_THEMES: dict[str, str] = {
    "fire_red": "sunset_orange",
    "rose_pink": "royal_purple",
    "lagoon_turquoise": "ocean_blue",
}
LEVELS = 4
# Cortes de los cuatro tonos, en proporcion a la referencia (su promedio de
# siempre en los dias estudiados): hasta la mitad, hasta el promedio, hasta
# el doble y mas del doble.
LEGEND_FACTORS: tuple[float, ...] = (0.5, 1.0, 2.0)


def legend_thresholds(reference: float) -> list[float]:
    """Limites de los cuatro tonos a partir de la referencia de la escala."""
    return [factor * reference for factor in LEGEND_FACTORS]


def level_index(count: float, thresholds: list[float]) -> int:
    """Tono de una cifra: 0 a 3 (se pinta con --gritmap-p1 a --gritmap-p4)."""
    for index, threshold in enumerate(thresholds):
        if count <= threshold:
            return index
    return len(thresholds)


def _vars_block(theme: str, dark: bool) -> str:
    scales = PAST_DARK if dark else PAST_LIGHT
    past = scales.get(theme, scales["classic_green"])
    return "".join(f"--gritmap-p{i + 1}:{color};" for i, color in enumerate(past))


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
    """Solo la escala del tema: es lo unico que depende de las opciones.

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
    return f"#gritmap-root{{{light}}}{dark_selector}{{{dark}}}"
