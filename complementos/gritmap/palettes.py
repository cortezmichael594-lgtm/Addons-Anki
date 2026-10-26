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
tokens de Nocturne, en web/gritmap.css.

Version 4.1.0 (correccion del cliente, 2026-10-21): los dias pendientes
vuelven a marcarse como antes, en grises segun las tarjetas que vencen, pero
con cuatro tonos en lugar de diez (tomados de la escala gris aprobada el
2026-10-13), y sin el punto de la 4.0.0.

Version 4.8.0 (decision del cliente, 2026-10-26): tres grises mas suaves en
lugar de cuatro. Lo que viene no debe pesar a la vista mas que lo hecho: los
tres quedan por debajo del primer tono de cualquier tema (contraste con la
tarjeta de 1,32 a 1,64 de dia y de 1,29 a 1,63 de noche, frente a 1,7-1,9 del
primer tono). Cuatro tan suaves no se distinguirian entre si; tres bastan
para «poca, normal y mucha carga» (la cifra exacta esta en el globo).

Version 4.10.0 (peticion del cliente, 2026-10-26): vuelven Rosa suave y
Turquesa laguna, seis temas en total; Rojo fuego sigue retirado. Sus cuatro
tonos siguen el mismo metodo que los demas: la misma luminosidad percibida
(OKLCH 0,80, 0,67, 0,54 y 0,41 de dia; 0,42, 0,56, 0,70 y 0,84 de noche) y la
misma saturacion, recortada donde la pantalla no llega.
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
    "rose_pink": ("#F2A3C1", "#D27199", "#AA4673", "#79284E"),  # colores-ok: tema recuperado por el cliente (2026-10-26)
    "lagoon_turquoise": ("#67D2CC", "#0DABA5", "#077F7A", "#025653"),  # colores-ok: tema recuperado por el cliente (2026-10-26)
}

PAST_DARK: dict[str, tuple[str, ...]] = {
    "classic_green": ("#335735", "#4C844F", "#6CB26F", "#9DDE9E"),  # colores-ok: escala aprobada (2026-10-21)
    "ocean_blue": ("#2E5072", "#4378AD", "#61A3E6", "#A2CFFF"),  # colores-ok: escala aprobada (2026-10-21)
    "royal_purple": ("#53446E", "#7E66A6", "#AA8DDE", "#D3BDFE"),  # colores-ok: escala aprobada (2026-10-21)
    "sunset_orange": ("#6A4225", "#A16336", "#D78951", "#FFB98A"),  # colores-ok: escala aprobada (2026-10-21)
    "rose_pink": ("#6B3C4F", "#A25A77", "#D87DA2", "#FEB0CE"),  # colores-ok: tema recuperado por el cliente (2026-10-26)
    "lagoon_turquoise": ("#085955", "#048681", "#08B6AF", "#67E2DA"),  # colores-ok: tema recuperado por el cliente (2026-10-26)
}

FUTURE_LIGHT: tuple[str, ...] = ("#D8DEE8", "#CDD3DD", "#C2C8D2")  # colores-ok: tres grises suaves aprobados (2026-10-26)
FUTURE_DARK: tuple[str, ...] = ("#343A44", "#3C424C", "#434953")  # colores-ok: tres grises suaves aprobados (2026-10-26)

THEME_NAMES: tuple[str, ...] = tuple(PAST_LIGHT)
# Temas retirados en la 4.0.0 y el tema al que pasa quien los tenia. Rosa
# suave y Turquesa laguna vuelven en la 4.10.0; Rojo fuego sigue fuera.
RETIRED_THEMES: dict[str, str] = {
    "fire_red": "sunset_orange",
}
LEVELS = 4
# Cortes de los cuatro tonos, en proporcion a la referencia (su promedio de
# siempre en los dias estudiados): hasta la mitad, hasta el promedio, hasta
# el doble y mas del doble.
LEGEND_FACTORS: tuple[float, ...] = (0.5, 1.0, 2.0)
# Tres grises de los dias pendientes (4.8.0): poca carga (hasta la mitad de
# lo normal), normal (hasta vez y media) y mucha.
DUE_FACTORS: tuple[float, ...] = (0.5, 1.5)


def legend_thresholds(reference: float) -> list[float]:
    """Limites de los cuatro tonos a partir de la referencia de la escala."""
    return [factor * reference for factor in LEGEND_FACTORS]


def due_thresholds(reference: float) -> list[float]:
    """Limites de los tres grises de los dias pendientes."""
    return [factor * reference for factor in DUE_FACTORS]


def level_index(count: float, thresholds: list[float]) -> int:
    """Tono de una cifra: 0 a 3 (se pinta con --gritmap-p1 a --gritmap-p4)."""
    for index, threshold in enumerate(thresholds):
        if count <= threshold:
            return index
    return len(thresholds)


def _vars_block(theme: str, dark: bool) -> str:
    scales = PAST_DARK if dark else PAST_LIGHT
    past = scales.get(theme, scales["classic_green"])
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
