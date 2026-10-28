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

from __future__ import annotations

import json

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
            f"{_SURFACE} {{"
            f" background-image: radial-gradient(1100px 700px at 82% -8%, {light}, transparent 60%);"
            " background-attachment: fixed;"
            "}"
            f"{_DARK_SURFACE} {{"
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


def _css_text() -> str:
    """CSS completo (sin la etiqueta ``<style>``), armado una vez por paleta."""
    global _css_cache
    if _css_cache is None:
        _css_cache = "\n".join(
            [
                _var_block(_LIGHT_SELECTOR, "light"),
                _var_block(_DARK_SELECTOR, "dark"),
                _surface_css(),
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
        "} catch (e) {}"
        "})();"
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


@guard
def on_did_inject_style(webview: AnkiWebView) -> None:
    """Inserta el estilo en páginas externas (gráficas, felicitación...)."""
    ensure_early_style(webview)
    webview.eval(_inject_js())
