"""Canal web: aplica la paleta y el acabado en las páginas web de Anki.

Las páginas web de Anki (repaso, mazos, editor, gráficas...) usan un CSS que se
compila por separado y no lee ``aqt.colors`` en tiempo de ejecución: define sus
colores como variables CSS en ``:root``. Para teñirlas inyectamos un bloque
``<style>`` que redefine esas variables y añade un acabado de superficie
(tipografía y un leve degradado anclado a la ventana), sin tocar el contenido de
las tarjetas.

El estilo entra por tres vías, todas con el mismo CSS:

1. En el ``<head>`` de las páginas internas (repaso, lista de mazos, editor),
   a través de ``webview_will_set_content``. Anki coloca ese ``head`` después
   de sus propias hojas, así que nuestros valores son los últimos en hablar.
2. En las páginas "externas" (gráficas, felicitación, opciones de mazo), que
   Anki carga aparte, mediante ``webview_did_inject_style_into_page``.
3. Como *estilo temprano*, un script registrado en el perfil web de Chromium
   que se ejecuta en cuanto nace el documento, antes del primer pintado. Es lo
   que evita el fogonazo claro al abrir las gráficas en modo noche: la vía 2
   llega, por fuerza, un fotograma tarde.

Por qué las variables se declaran sobre ``body`` y no solo sobre ``:root``:
Anki declara las suyas en ``:root`` y sus hojas se cargan después de nuestro
estilo temprano, de modo que en ``:root`` ganarían ellas. Una declaración en
``body`` la heredan todos los elementos de la página y no compite con ``:root``,
así que la paleta se respeta siempre, llegue nuestro estilo antes o después.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-24) — En modo oscuro el degradado de fondo aparecía repetido,
#                        apilado, en vez de uno solo anclado a la esquina.
# FIX-006 (2026-10-21) — En la pantalla de estudio, los datos del mazo se resaltaban
#                        al pasar el ratón, como si fueran una fila de la lista de mazos.
# FIX-010 (2026-10-28) — Al pasar el ratón por un botón de respuesta salía una raya de
#                        color arriba, además de la de abajo.
# FIX-015 (2026-11-11) — Lo que se escribe en el editor salía en blanco puro de noche (y en
#                        negro puro de día), y no en el color del texto.

from __future__ import annotations

import json
import re
from typing import Any

from anki.utils import is_mac, is_win
from aqt import mw
from aqt.qt import QWebEngineScript
from aqt.utils import tr
from aqt.webview import AnkiWebView, WebContent

from .errors import guard, note_failure
from . import themes
from .palette import Mode

# Identificadores separados para el estilo definitivo y el temprano: los dos
# pueden convivir en la misma página (el definitivo, más tardío, es el que
# manda) y con identificadores distintos ninguno pisa al otro.
_STYLE_ID = "nocturne_theme"
_EARLY_STYLE_ID = "nocturne_theme_early"
_SCRIPT_NAME = "nocturne_early_style"

# Selectores de la paleta.
#   - Modo día: la raíz y el cuerpo de la página.
#   - Modo noche: Anki marca la raíz con "night-mode" nada más nacer la página y
#     el cuerpo con "night_mode" algo después. Contemplamos las dos marcas para
#     que no haya ni un instante con los colores del modo día.
_LIGHT_SELECTOR = ":root, body"
_DARK_SELECTOR = ":root.night-mode, :root.night-mode body, body.night_mode"

# El acabado de superficie (tipografía y degradado) se aplica a la interfaz,
# nunca a las tarjetas (body.card): el aspecto de una tarjeta lo decide su propia
# plantilla. El degradado del modo noche usa la marca "night_mode" del cuerpo,
# igual que el original.
_SURFACE = "body:not(.card)"
_DARK_SURFACE = "body.night_mode:not(.card)"
# Versión 3.9.0 (informe del 2026-11-11, apartado 8.7): el degradado, solo en el fondo de las
# páginas, nunca en las barras: la superior (.toolbar) y las inferiores de la lista de mazos, de
# la pantalla de un mazo y del repaso (#outer). Dentro de la barra inferior dejaba un corte
# horizontal y, durante el repaso, un adorno donde se estudia.
_GLOW = "body:not(.card):not(:has(#outer, .toolbar))"
_DARK_GLOW = "body.night_mode:not(.card):not(:has(#outer, .toolbar))"

# Pila tipográfica: en cada sistema recae en su letra de interfaz nativa, de modo
# que Anki se ve integrado en Windows, macOS y Linux sin instalar nada. La letra
# que Anki elige para el idioma activo se añade al final en ``_ui_font_stack``.
_PREFERRED_FAMILIES = (
    "-apple-system",
    "BlinkMacSystemFont",
    "'Segoe UI Variable Text'",
    "'Segoe UI'",
    "'Inter'",
    "'Cantarell'",
    "'Ubuntu'",
    "'Noto Sans'",
    "system-ui",
)

# El CSS no cambia durante la sesión, así que se arma una sola vez y se reparte:
# las páginas se dibujan muchas veces y no tiene sentido rehacerlo cada vez.
# Duración de las transiciones de las páginas de Anki, en milisegundos.
TRANSITION_MS = 100

_css_cache: str | None = None
_style_block_cache: str | None = None
_inject_js_cache: str | None = None
_early_script: QWebEngineScript | None = None


# Paleta y acabado
######################################################################


def _anki_ui_font() -> str:
    """La letra que Anki elige para el sistema y el idioma activos.

    En Windows, Anki traduce esta familia en cada idioma precisamente para que
    el japonés, el chino o el coreano se vean con una letra que tenga sus
    caracteres. Se añade al final de nuestra pila: los idiomas de alfabeto
    latino siguen viéndose con la letra moderna del sistema y los demás caen en
    la que Anki considera correcta, carácter a carácter.
    """
    if is_win:
        return tr.qt_misc_segoe_ui()
    if is_mac:
        return '"Helvetica"'
    family = mw.font().family() if mw is not None else ""
    return f'"{family}"' if family else ""


def _ui_font_stack() -> str:
    families = list(_PREFERRED_FAMILIES)
    try:
        anki_families = _anki_ui_font()
    except Exception:
        note_failure("no se pudo leer la letra de interfaz de Anki")
        anki_families = ""

    # Anki puede nombrar varias familias separadas por comas. Se añaden las que
    # no estén ya en la pila, comparando sin comillas ni mayúsculas.
    seen = {family.strip("'\"").casefold() for family in families}
    for family in anki_families.split(","):
        family = family.strip()
        key = family.strip("'\"").casefold()
        if family and key not in seen:
            families.append(family)
            seen.add(key)

    families.append("sans-serif")
    return ", ".join(families)


def _var_block(selector: str, mode: Mode) -> str:
    lines = [f"{selector} {{"]
    for entry in themes.colors().values():
        for css_name in entry["css"]:
            lines.append(f"  {css_name}: {entry[mode]};")
    # Esquinas de la paleta: las mismas variables que usan las páginas de Anki.
    look = themes.look()
    lines.append(f"  --border-radius: {look['radius']}px;")
    lines.append(f"  --border-radius-medium: {look['radius_medium']}px;")
    lines.append(f"  --border-radius-large: {look['radius_large']}px;")
    # Versión 3.7.0: la esquina de botones y campos, para el panel de configuración.
    lines.append(f"  --nocturne-control-radius: {look['button_radius']}px;")
    # Versión 3.3.0: los cambios al pasar el ratón, en 100 ms en vez de 180: así se
    # perciben instantáneos (Saffer, P4; Norman, retroalimentación). Solo esta
    # duración: el fundido de las tarjetas (--transition-medium) es de Anki y no cambia.
    lines.append(f"  --transition: {TRANSITION_MS}ms;")
    lines.append("}")
    return "\n".join(lines)


def _surface_css() -> str:
    """Acabado de superficie: tipografía y el degradado suave del original.

    # --- FIX-001 (2026-07-24) --------------------------------------
    # Síntoma: en modo oscuro el degradado de fondo se veía repetido, apilado
    #          (varias manchas, una debajo de otra), en vez de uno solo en la
    #          esquina como en el original.
    # Causa: al "optimizar" se le quitó ``background-attachment: fixed``. Ese
    #        anclaje es lo que fija el degradado a la ventana como una sola
    #        mancha; sin él, el degradado se recalcula por cada zona de la
    #        interfaz y aparece repetido.
    # Regla: el degradado de superficie SIEMPRE lleva
    #        ``background-attachment: fixed``. Y, en general, no quitar
    #        propiedades de algo que ya funcionaba sin una prueba visual real
    #        que confirme que el aspecto no cambia: aquí el ahorro supuesto no
    #        compensó la regresión.
    # ---------------------------------------------------------------

    El degradado se ancla a la ventana con ``background-attachment: fixed`` para
    que sea una sola mancha en la esquina superior derecha. ``fixed`` solo hace
    falta declararlo en la primera regla: como no lo pisa la regla del modo
    noche, sigue vigente cuando esta solo cambia el color del degradado. Una
    paleta sin degradado no llevaría ninguna de las dos.
    Todo sale de la paleta elegida (``themes``).
    """
    look = themes.look()
    rules = [
        "html button { background: var(--button-bg); }",
        (
            f"{_SURFACE} {{"
            f" font-family: {_ui_font_stack()};"
            " -webkit-font-smoothing: antialiased;"
            " text-rendering: optimizeLegibility;"
            "}"
        ),
    ]
    gradient = look["gradient"]
    if gradient is not None:
        light, dark = gradient
        rules.append(
            f"{_GLOW} {{"
            f" background-image: radial-gradient(1100px 700px at 82% -8%, {light}, transparent 60%);"
            " background-attachment: fixed;"
            "}"
            f"{_DARK_GLOW} {{"
            f" background-image: radial-gradient(1100px 700px at 82% -8%, {dark}, transparent 60%);"
            "}"
        )
    heading_family = look["heading_family"]
    family = f" font-family: {heading_family};" if heading_family else ""
    rules += [
        # Tipografía (versión 3.0.0). Cifras de igual ancho en tablas y
        # recuentos, para que se alineen en columna (Practical UI, C12).
        (
            f"{_SURFACE} :is(table, .new-count, .learn-count, .review-count,"
            " .bury-count, .zero-count) { font-variant-numeric: tabular-nums; }"
        ),
        # Títulos con el peso, la separación entre letras y, en Papel, la letra de
        # la paleta (Refactoring UI, R2 y M4; vídeo de Tim Gabe sobre tipografía, P2).
        (
            f"{_SURFACE} :is(h1, h2, h3) {{{family}"
            f" font-weight: {look['heading_weight']};"
            f" letter-spacing: {look['heading_tracking']}; }}"
        ),
        # Descripción del mazo: interlineado cómodo y líneas de 70 caracteres como
        # mucho (Practical UI, P15; Refactoring UI, R8). Versión 3.4.0: sin palabras
        # sueltas en la última línea (text-wrap: pretty).
        (
            f"{_SURFACE} .description {{ line-height: {look['reading_line_height']};"
            " max-width: 70ch; margin-inline: auto; text-wrap: pretty; }"
        ),
        # Versión 3.4.0: títulos de varias líneas repartidos en líneas parecidas, sin una
        # palabra sola debajo (text-wrap: balance), y casillas, botones de opción y barras
        # nativas de las páginas en el color de acción de la paleta (accent-color): un
        # solo color de acción en todo Anki (Practical UI, P10).
        f"{_SURFACE} :is(h1, h2, h3) {{ text-wrap: balance; }}",
        # Versión 3.5.0: el tono de trazo (el del foco), que de noche es más claro que
        # el de los rellenos y se ve a 3:1 o más sobre cualquier fondo (WCAG 1.4.11).
        f"{_SURFACE} {{ accent-color: var(--border-focus); }}",
        # Versión 3.4.0: con «Reducir movimiento» en las preferencias de Anki, que marca la
        # página con reduce-motion, los cambios de color son inmediatos (WCAG 2.3.3). Gana
        # a la duración de la paleta en los dos modos por ser más específica.
        "html body.reduce-motion:not(.card) { --transition: 0ms; }",
        # Versión 3.5.0: lo mismo con la opción del sistema (en Windows, «Efectos de
        # animación» desactivados), como hace GritMap.
        "@media (prefers-reduced-motion: reduce) { html body:not(.card) { --transition: 0ms; } }",
        # Versión 3.5.0: los intervalos sobre los botones de respuesta («10 min», «4 d»)
        # en el texto secundario y con cifras de igual ancho, como las de las tablas.
        f"html {_SURFACE} :is(.nobold, .stattxt) {{ color: var(--fg-subtle); font-variant-numeric: tabular-nums; }}",
        # Lista de mazos (versión 3.1.0): separación de las filas según la paleta y
        # resaltado del mazo actual y del que tiene el ratón encima con un tinte del
        # color de acción en vez de gris (Practical UI, M5 y M7).
        #
        # --- FIX-006 (2026-10-21) ---
        # Síntoma: en la pantalla de estudio, la tabla con Nuevas, Aprendiendo y A repasar
        #          se teñía de azul al pasar el ratón por encima.
        # Causa: el resaltado se aplicaba a cualquier fila de tabla con el ratón encima
        #        («tr:hover»), y esa pantalla también usa tablas; la separación de filas
        #        («tr[id]») tenía el mismo defecto.
        # Regla: todo lo que se inyecta para una pantalla concreta se limita a sus propios
        #        elementos (aquí, las filas de mazo: «tr.deck»), nunca a etiquetas genéricas.
        f"{_SURFACE} tr.deck > td {{ padding-block: {look['row_padding']}px; }}",
        # Versión 3.7.1 (petición del cliente, 2026-10-28): la tabla de la lista de mazos con
        # el fondo de los recuadros (capa elevada), el mismo que las tarjetas de GritMap, en
        # vez del cristal semitransparente de Anki: un solo material para todo lo que está
        # «encima» del fondo. Limitado a esa tabla (regla de FIX-006).
        f"html {_SURFACE} table:has(tr.deck) {{ background: var(--canvas-elevated); }}",
        (
            f"html {_SURFACE} tr.deck:is(.current, :hover) > td"
            " { background: var(--nocturne-row-highlight); }"
        ),
        # Versión 3.8.0 (informe del 2026-11-04, apartados 1.5 y 2.1), todo limitado a la
        # tabla de la lista de mazos (regla de FIX-006):
        # - La fila resaltada, con la esquina de botones y campos y no con la de los
        #   recuadros: un elemento dentro de un recuadro redondeado lleva una esquina menor
        #   (Pixsel, M3). Se cambia la variable que usa Anki solo en esas celdas, así vale
        #   también para los idiomas que se escriben de derecha a izquierda.
        f"html {_SURFACE} tr.deck > td {{ --border-radius-medium: var(--nocturne-control-radius); }}",
        # - La fila vacía bajo la cabecera, donde se suelta un mazo para sacarlo al nivel
        #   superior, de 10 px en vez de una línea entera: separaba la cabecera de sus filas
        #   más que una fila de otra. Sigue ahí y sigue admitiendo mazos.
        (
            f"html {_SURFACE} table:has(tr.deck) tr.top-level-drag-row > td"
            " { padding-block: 0; height: 10px; font-size: 0; line-height: 0; }"
        ),
        # - Rótulos de las columnas con el mismo margen lateral que sus cifras (12 px a cada
        #   lado): quedan alineados con ellas y separados entre sí 24 px, en vez de 6
        #   (Jeliazkov, M10); y «Mazo», alineado con los nombres, que llevan delante el
        #   hueco de 1em del «+/−» para plegar.
        f"html {_SURFACE} table:has(tr.deck) th {{ padding-inline: 12px; }}",
        f"html {_SURFACE} table:has(tr.deck) th:first-child {{ padding-inline-start: calc(12px + 1em); }}",
        # Versión 3.8.0: la línea «Estudiadas N tarjetas…» en el texto secundario: es un dato
        # de apoyo y no compite con los nombres de los mazos (Practical UI, M6).
        f"html {_SURFACE} #studiedToday {{ color: var(--fg-subtle); }}",
        # Versión 3.8.0: los botones de la barra inferior de la lista de mazos y de la
        # pantalla de un mazo («Crear mazo», «Importar archivo», «Opciones»...) con la
        # esquina de botones y campos, no media píldora (la regla de esquinas de 3.5.0).
        (
            f"html {_SURFACE} center#outer > table#header button"
            " { border-radius: var(--nocturne-control-radius); }"
        ),
        # Versión 3.8.0: en el editor, los nombres de los campos en el texto secundario: lo
        # que se escribe es el dato y el nombre, su rótulo (Refactoring UI, P10).
        f"html {_SURFACE} .label-container .label-name {{ color: var(--fg-subtle); }}",
        # Barra superior (versión 3.2.0): Mazos, Añadir, Explorar... con un fondo suave
        # y redondeado al pasar el ratón, en lugar del subrayado, para que se vea qué
        # se va a pulsar (Practical UI, M5). Solo color y esquinas: no cambia el tamaño
        # ni la posición, y nada va en posición absoluta (APR-060).
        (
            f"html {_SURFACE} .toolbar .hitem:hover {{"
            " background: var(--button-gradient-start);"
            " border-radius: var(--border-radius);"
            " text-decoration: none; }"
        ),
        # Versión 3.8.0 (informe del 2026-11-04, apartado 1.1): la barra superior en
        # seminegrita y no en negrita: es navegación, y no debe pesar más que los nombres
        # de los mazos, que es lo que se viene a mirar (Refactoring UI, P8).
        f"html {_SURFACE} .toolbar .hitem {{ font-weight: 600; }}",
        # Botones de respuesta del repaso (versión 3.2.0): una raya fina de color al pie
        # de «Otra vez», «Difícil», «Bien» y «Fácil». El texto sigue diciendo lo mismo;
        # el color solo ayuda a reconocerlos de un vistazo (Norman, mapeo; Practical UI,
        # P9). Va como capa de fondo para no tocar el tamaño ni las sombras de Anki.
        *_answer_marks(),
        # Cabeceras de la lista de mazos (Mazo, Nuevas...) y etiquetas de la pantalla
        # de estudio (Nuevas:, Aprendiendo:, A repasar:) en el texto secundario, para
        # que destaquen las cifras, que es lo que se viene a mirar (versión 3.3.0;
        # Refactoring UI, P8 y P9). Cada regla, limitada a su tabla (regla de FIX-006).
        (
            f"html {_SURFACE} table:has(tr.deck) th"
            " { color: var(--fg-subtle); font-weight: 600; }"
        ),
        (
            f"html {_SURFACE} tr:has(> td > b > :is(.new-count, .learn-count, .review-count))"
            " > td:first-child { color: var(--fg-subtle); }"
        ),
        # Versión 3.7.0: «Editar» y «Más» del repaso como botones discretos (sin fondo
        # ni borde; fondo suave al pasar el ratón, como la barra superior), para que los
        # botones de respuesta sean lo único con forma de botón (Refactoring UI, P11). El
        # borde queda transparente, no se quita: nada cambia de tamaño.
        (
            f"html {_SURFACE} td.stat > button {{ background: transparent;"
            " border-color: transparent; box-shadow: none; }"
        ),
        (
            f"html {_SURFACE} td.stat > button:hover"
            " { background: var(--button-gradient-start); }"
        ),
        # Texto seleccionado en las páginas de Anki (no en las tarjetas).
        f"{_SURFACE} ::selection {{ background: var(--selected-bg); }}",
        # Foco del teclado visible en los botones de las páginas clásicas: Anki lo
        # quita a todos con outline: none !important (APR-061).
        (
            f"html {_SURFACE} button:is(:not([class]), .but):focus-visible {{"
            f" outline: {look['focus_width']}px solid var(--border-focus) !important;"
            " outline-offset: 2px;"
            "}"
        ),
        # Versión 3.4.0: el mismo contorno en los enlaces (nombres de mazo, engranaje de
        # opciones) y en la barra superior, donde Anki lo quita (.hitem:focus { outline: 0 }),
        # para saber siempre dónde está el teclado (Practical UI, estados; WCAG 2.4.7). El
        # contorno no ocupa sitio: nada se mueve. Y el subrayado de los enlaces, algo
        # separado de las letras para que no tape sus colas.
        (
            f"html {_SURFACE} a:focus-visible {{"
            f" outline: {look['focus_width']}px solid var(--border-focus) !important;"
            " outline-offset: 2px; border-radius: var(--border-radius);"
            "}"
        ),
        f"html {_SURFACE} a {{ text-underline-offset: 0.18em; }}",
    ]
    return "\n".join(rules)


# Color de la raya de cada botón de respuesta (data-ease de Anki: 1 a 4). El naranja
# de «Difícil» lleva un 15 % del color del texto para verse a 3:1 sobre el botón en
# todas las paletas (las pruebas lo miden).
_ANSWER_COLORS = {
    1: "var(--accent-danger)",
    2: "color-mix(in srgb, var(--flag-2) 85%, var(--fg))",
    3: "var(--state-review)",
    4: "var(--state-new)",
}


def _answer_marks() -> list[str]:
    # --- FIX-010 (2026-10-28) ---
    # Síntoma: con el ratón encima de un botón de respuesta (por ejemplo «Fácil») salía una
    #          raya fina de su color arriba del botón, además de la de abajo.
    # Causa: el navegador repite como un mosaico las imágenes de fondo también bajo el borde, y
    #        con el ratón encima Anki pone un borde semitransparente: asomaba la repetición de
    #        la raya de abajo.
    # Regla: toda raya o dibujo hecho con imágenes de fondo lleva background-repeat: no-repeat.
    rules = []
    for ease, value in _ANSWER_COLORS.items():
        mark = f"linear-gradient(to top, {value} 0 3px, transparent 3px)"
        button = f"html {_SURFACE} button[data-ease='{ease}']"
        rules.append(f"{button} {{ background-image: {mark}; background-repeat: no-repeat; }}")
        rules.append(
            f"{button}:hover {{ background-image: {mark},"
            " linear-gradient(180deg, var(--button-gradient-start), var(--button-gradient-end)); }"
        )
    return rules


# Botones de las páginas clásicas de Anki (barras inferiores, repaso y el editor clásico): los
# que no llevan clase, los de mw.button («but») y los del editor clásico («linkb»). Fuera, el
# botón relleno («Comenzar a estudiar», #study) y «Editar» y «Más» del repaso, que van sin borde.
_PAGE_BUTTON = "button:is(:not([class]), .but, .linkb):not([id=study], td.stat > button)"
_STUDY_BUTTONS = "button:is([data-ease], #ansbut)"


def _redesign_css() -> str:
    """Versión 3.9.0 (informe del 2026-11-11, apartado 8): las reglas del rediseño en las
    páginas. Todo sale de las variables de la paleta; nada cambia de sitio.

    - Un borde para todo lo que se pulsa o se rellena (8.6): los botones, el de control, a
      3:1 o más sobre el fondo y los recuadros (antes, 1,29 y 1,05:1). Con el ratón encima,
      el borde de botón con el ratón; pulsado, un escalón más hundido y sin la sombra interior
      de Anki; desactivado, el borde suave. Los campos del editor y el de etiquetas, el mismo
      borde que los campos de las ventanas (antes, 1,18:1: WCAG 1.4.11).
    - Una sola familia de esquinas (8.4): ningún botón en píldora. «Comenzar a estudiar» y los
      botones de respuesta llevan la esquina de los botones, como los demás; la raya de color
      de las respuestas se ve entera, de lado a lado.
    - Botones de estudio a 36 px de alto (8.6): los de respuesta, con 96 px de ancho mínimo y
      16 px entre ellos; «Comenzar a estudiar», con 24 px a los lados. Su rótulo, del tamaño
      del texto de la página, y el título de la pantalla de un mazo, un tercio mayor (8.11,
      decisión 2): son proporciones, así que siguen la letra que se elija en Anki.
    - Un gris para todos los iconos (8.2, regla 4): el engranaje de la lista de mazos y los
      iconos de la barra del editor, en el texto secundario; el engranaje, con 24 px de zona
      pulsable y el dibujo del mismo tamaño.
    - Barra de desplazamiento con el tirador de 8 px, centrado y redondo, en un carril de 12.
    """
    page_button = f"html {_SURFACE} {_PAGE_BUTTON}"
    study = f"html {_SURFACE} {_STUDY_BUTTONS}"
    rules = [
        f"{page_button} {{ border-color: var(--nocturne-control-border); }}",
        f"{page_button}:hover {{ border-color: var(--button-hover-border); }}",
        (
            f"{page_button}:active {{ background: var(--nocturne-button-pressed);"
            " border-color: var(--button-hover-border); box-shadow: none; }"
        ),
        f"{page_button}[disabled] {{ border-color: var(--border); }}",
        # Esquinas: la de botones también en las páginas con aspecto «fancy», que las hace
        # píldoras. Los del editor clásico («linkb») van en grupos con sus propias esquinas.
        f"html {_SURFACE} button:is(:not([class]), .but) {{ border-radius: var(--nocturne-control-radius); }}",
        # Botones de respuesta y «Mostrar respuesta». La raya de color va por dentro, pegada al
        # borde inferior y de lado a lado: ocupa el sitio del borde de abajo, que queda
        # transparente en todos los estados (FIX-010: la raya no se repite).
        (
            f"{study} {{ box-sizing: border-box; min-height: 36px; min-width: 96px;"
            " margin-inline: 8px; font-size: 1rem; background-origin: border-box; }"
        ),
        f"{page_button}[data-ease] {{ border-bottom-color: transparent; }}",
        f"{page_button}[data-ease]:is(:hover, :active) {{ border-bottom-color: transparent; }}",
        # «Comenzar a estudiar»: el botón relleno, con la esquina de botones y 36 px de alto.
        # Con el ratón, más oscuro; pulsado, más aún; con el teclado, el anillo (8.5).
        (
            f"html {_SURFACE} button#study {{ box-sizing: border-box; min-height: 36px;"
            " padding-inline: 24px; font-size: 1rem; border-radius: var(--nocturne-control-radius); }"
        ),
        f"html {_SURFACE} button#study:hover {{ background: var(--button-primary-gradient-end); }}",
        (
            f"html {_SURFACE} button#study:active"
            " { background: var(--nocturne-primary-pressed); box-shadow: none; }"
        ),
        f"html {_SURFACE} button#study:focus-visible {{ outline-color: var(--nocturne-primary-ring) !important; }}",
        # Título de la pantalla de un mazo, un tercio mayor que el texto (antes, un 13 %).
        f"html {_SURFACE}:has(#study) center > h3 {{ font-size: calc(1rem * 4 / 3); }}",
        # Los ceros de la pantalla de un mazo, en el texto tenue, como en la lista de mazos
        # (la clase la pone on_overview_content).
        f"html {_SURFACE} .zero-count {{ color: var(--fg-faint); }}",
        # Barras inferiores de la lista de mazos y de la pantalla de un mazo: 16 px entre
        # botones (antes, 14), contando el espacio que Anki deja entre ellos.
        f"html {_SURFACE} center#outer > table#header button {{ margin-inline: 5.5px; }}",
        # Editor: campos y etiquetas con el borde de control; el foco ya lo marca Anki con el
        # trazo de acción, por dentro. Los iconos de su barra, en el texto secundario.
        f"html {_SURFACE} :is(.editor-field, .tag-editor) {{ border-color: var(--nocturne-control-border); }}",
        f"html {_SURFACE} .icon-button:not(.active, .primary, [disabled]) {{ color: var(--fg-subtle); }}",
        # Engranaje de la lista de mazos: Anki pinta su dibujo oscuro, invertido de noche y a
        # media opacidad (un gris que no es de la paleta). Se pinta con la máscara del mismo
        # dibujo en el texto secundario y se aparta el de Anki; 24 px de zona pulsable sin
        # mover nada (el margen negativo devuelve el relleno).
        (
            f"html {_SURFACE} img.gears {{ opacity: 1; filter: none; object-position: -9999px 0;"
            " background: var(--fg-subtle);"
            " -webkit-mask: url(/_anki/imgs/gears.svg) center / 1em 1em no-repeat content-box;"
            " mask: url(/_anki/imgs/gears.svg) center / 1em 1em no-repeat content-box;"
            " padding: calc((24px - 1em) / 2);"
            " margin: calc((1em - 24px) / 2 + 0.2em) calc((1em - 24px) / 2) calc((1em - 24px) / 2); }"
        ),
        # Tirador de las barras de desplazamiento: 8 px dentro del carril de 12 (un borde
        # transparente de 2 px), redondo. Los colores ya llegan a 3:1.
        (
            "html:root body:not(.isMac)::-webkit-scrollbar-thumb,"
            " html:root body:not(.isMac) *::-webkit-scrollbar-thumb"
            " { border: 2px solid transparent; background-clip: padding-box; border-radius: 6px; }"
        ),
    ]
    return "\n".join(rules)


def _css_text() -> str:
    """CSS completo (sin la etiqueta ``<style>``), armado una vez por paleta."""
    global _css_cache
    if _css_cache is None:
        _css_cache = "\n".join(
            [
                _var_block(_LIGHT_SELECTOR, "light"),
                _var_block(_DARK_SELECTOR, "dark"),
                _surface_css(),
                _redesign_css(),
            ]
        )
    return _css_cache


def _style_block() -> str:
    """Bloque ``<style>`` listo para insertar en el ``<head>`` de una página."""
    global _style_block_cache
    if _style_block_cache is None:
        _style_block_cache = f"<style id='{_STYLE_ID}'>\n{_css_text()}\n</style>"
    return _style_block_cache


# Estilo temprano (script del perfil web)
######################################################################


def _install_js(style_id: str, guard_existing: bool) -> str:
    """JS que inserta el ``<style>``; idempotente en los dos modos de uso.

    Con ``guard_existing`` no hace nada si el bloque ya está (estilo temprano,
    que solo debe llegar el primero); sin él retira el bloque anterior
    (y el temprano, que podría ser de otra paleta) y añade el nuevo al final, de
    modo que Anki puede reinyectar el contenido sin dejar copias sueltas y
    nuestro estilo queda siempre el último de la página.
    """
    id_json = json.dumps(style_id)
    css_json = json.dumps(_css_text())
    action = (
        "if (document.getElementById(id)) { return; }"
        if guard_existing
        else (
            "for (const oldId of [id, " + json.dumps(_EARLY_STYLE_ID) + "]) {"
            "const old = document.getElementById(oldId); if (old) { old.remove(); } }"
        )
    )
    return (
        "(() => {"
        "try {"
        # Solo las páginas que sirve el propio Anki: si un complemento cargara
        # una página de internet en un webview, no la tocamos.
        "const host = location.hostname;"
        "if (host && host !== '127.0.0.1' && host !== 'localhost') { return; }"
        f"const id = {id_json};"
        f"const css = {css_json};"
        "const install = () => {"
        f"{action}"
        "const parent = document.head || document.documentElement;"
        "if (!parent) { return; }"
        "const el = document.createElement('style');"
        "el.id = id;"
        "el.textContent = css;"
        "parent.appendChild(el);"
        "};"
        # En el nacimiento del documento la raíz ya existe; el respaldo cubre
        # cualquier caso raro en el que aún no estuviera.
        "if (document.documentElement) { install(); }"
        "else { document.addEventListener('DOMContentLoaded', install, {once: true}); }"
        f"{_EDITABLE_JS}"
        "} catch (e) {}"
        "})();"
    )


# --- FIX-015 (2026-11-11) ---
# Síntoma: de noche, lo que se escribe en los campos del editor salía en blanco puro (14,8:1, por
#          encima del techo de 13,5) y de día en negro puro; la descripción decía «en el color del
#          texto».
# Causa: Anki fija ese color dentro de cada campo, en una zona aislada de la página (shadow DOM)
#        a la que no llega el estilo de fuera: «anki-editable { color: white }» o «black».
# Regla: lo que Anki pinta dentro de una zona aislada se cambia dentro de ella, con una regla más
#        específica y var(--fg), que sigue la paleta y el modo; y se mide en la página dibujada,
#        no solo en el CSS de fuera.
# Las zonas nuevas reciben la regla al crearse (se envuelve attachShadow una vez por página,
# antes de que el editor cree sus campos) y las que ya existían, al instalarse el estilo. La
# regla solo afecta a anki-editable: en cualquier otra zona aislada no hace nada.
_EDITABLE_JS = (
    "if (!window.nocturneEditable && window.CSSStyleSheet && Element.prototype.attachShadow) {"
    "const sheet = new CSSStyleSheet();"
    "sheet.replaceSync(':host anki-editable { color: var(--fg); }');"
    "window.nocturneEditable = sheet;"
    "const adopt = (root) => {"
    "if (root && !root.adoptedStyleSheets.includes(sheet)) {"
    "root.adoptedStyleSheets = [...root.adoptedStyleSheets, sheet]; } };"
    "const original = Element.prototype.attachShadow;"
    "Element.prototype.attachShadow = function (init) {"
    "const root = original.call(this, init);"
    "try { adopt(root); } catch (e) {}"
    "return root; };"
    "}"
    "if (window.nocturneEditable && document.querySelectorAll) {"
    "document.querySelectorAll('.rich-text-editable').forEach((host) => {"
    "const root = host.shadowRoot;"
    "if (root && !root.adoptedStyleSheets.includes(window.nocturneEditable)) {"
    "root.adoptedStyleSheets = [...root.adoptedStyleSheets, window.nocturneEditable]; } });"
    "}"
)


def _inject_js() -> str:
    """JS que coloca el estilo definitivo en una página ya cargada."""
    global _inject_js_cache
    if _inject_js_cache is None:
        _inject_js_cache = _install_js(_STYLE_ID, guard_existing=False)
    return _inject_js_cache


def _get_early_script() -> QWebEngineScript:
    """Script de perfil que aplica la paleta antes del primer pintado."""
    global _early_script
    if _early_script is None:
        script = QWebEngineScript()
        script.setName(_SCRIPT_NAME)
        script.setSourceCode(_install_js(_EARLY_STYLE_ID, guard_existing=True))
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        # Solo el documento principal: si una tarjeta incrusta una página ajena,
        # se queda como su autor la hizo.
        script.setRunsOnSubFrames(False)
        _early_script = script
    return _early_script


def ensure_early_style(webview: AnkiWebView) -> None:
    """Registra el estilo temprano en el perfil web al que pertenece el webview.

    Anki reparte sus pantallas entre dos perfiles de Chromium y los crea sobre
    la marcha, así que se comprueba al vuelo en vez de una sola vez al arrancar.
    La comprobación es una búsqueda en una lista de dos o tres elementos.
    """
    page = webview.page()
    if page is None:
        return
    profile = page.profile()
    if profile is None:
        return
    scripts = profile.scripts()
    if scripts is None:
        return
    script = _get_early_script()
    current = scripts.find(_SCRIPT_NAME)
    if len(current) == 1 and current[0].sourceCode() == script.sourceCode():
        return
    # Falta, o es de una paleta anterior: se sustituye.
    for old in current:
        scripts.remove(old)
    scripts.insert(script)


def reset() -> None:
    """Olvida el CSS armado, para que se rehaga con la paleta elegida."""
    global _css_cache, _style_block_cache, _inject_js_cache, _early_script
    _css_cache = _style_block_cache = _inject_js_cache = None
    _early_script = None


def refresh_open_pages() -> None:
    """Aplica la paleta elegida a las páginas abiertas, sin recargarlas.

    Sustituye el estilo de cada página (lista de mazos, repaso, editor, Explorar,
    estadísticas...) y el estilo temprano de su perfil web, para que las páginas
    que se abran después nazcan ya con la paleta nueva.
    """
    from aqt.qt import QApplication

    for widget in QApplication.allWidgets():
        if not isinstance(widget, AnkiWebView):
            continue
        try:
            ensure_early_style(widget)
            widget.eval(_inject_js())
        except Exception:
            note_failure("no se pudo cambiar la paleta de una página")


def install_early_style() -> None:
    """Registra el estilo temprano en los webviews que ya existen al arrancar."""
    if mw is None:
        return
    for webview in mw.findChildren(AnkiWebView):
        try:
            ensure_early_style(webview)
        except Exception:
            note_failure("no se pudo registrar el estilo temprano")


# Enganches
######################################################################


@guard
def on_will_set_content(web_content: WebContent, context: object) -> None:
    """Añade el estilo al HTML inicial de las páginas internas de Anki."""
    web_content.head += _style_block()

    # La pantalla que está dibujando (editor, navegador...) puede pertenecer a
    # un perfil web que aún no tenga el estilo temprano; se aprovecha para
    # registrarlo y que sus páginas externas no parpadeen.
    webview = getattr(context, "web", None)
    if isinstance(webview, AnkiWebView):
        ensure_early_style(webview)


# Versión 3.9.0 (informe del 2026-11-11, apartado 4.4): en la pantalla de un mazo, una cifra a
# cero no lleva color. Anki pinta «Aprendiendo: 0» en rojo, al nivel de las cifras que piden
# algo, mientras que en la lista de mazos ya pone los ceros en el texto tenue (zero-count).
# Aquí se añade esa misma clase a las cifras a cero; la de su tipo se queda, para que su
# etiqueta siga en el texto secundario.
_ZERO_COUNT = re.compile(r"<span class=(new-count|learn-count|review-count)>0</span>")


@guard
def on_overview_content(overview: object, content: Any) -> None:
    """Marca las cifras a cero de la pantalla de un mazo con la clase de Anki para los ceros."""
    table = getattr(content, "table", None)
    if isinstance(table, str):
        content.table = _ZERO_COUNT.sub(r'<span class="\1 zero-count">0</span>', table)


@guard
def on_did_inject_style(webview: AnkiWebView) -> None:
    """Inserta el estilo en páginas externas (gráficas, felicitación...)."""
    ensure_early_style(webview)
    webview.eval(_inject_js())
