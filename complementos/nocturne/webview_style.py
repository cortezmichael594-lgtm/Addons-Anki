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

from __future__ import annotations

import json

from anki.utils import is_mac, is_win
from aqt import mw
from aqt.qt import QWebEngineScript
from aqt.utils import tr
from aqt.webview import AnkiWebView, WebContent

from .errors import get_logger, guard
from .palette import PALETTE, Mode

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
        get_logger().exception("no se pudo leer la letra de interfaz de Anki")
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
    for entry in PALETTE.values():
        for css_name in entry["css"]:
            lines.append(f"  {css_name}: {entry[mode]};")
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
    noche, sigue vigente cuando esta solo cambia el color del degradado.
    """
    return "\n".join(
        [
            "html button { background: var(--button-bg); }",
            (
                f"{_SURFACE} {{"
                f" font-family: {_ui_font_stack()};"
                " -webkit-font-smoothing: antialiased;"
                " text-rendering: optimizeLegibility;"
                "}"
            ),
            (
                f"{_SURFACE} {{"  # colores-ok: degradado del acabado, el azul de acción casi transparente
                " background-image: radial-gradient(1100px 700px at 82% -8%,"
                " rgba(59, 111, 224, 0.04), transparent 60%);"
                " background-attachment: fixed;"
                "}"
                f"{_DARK_SURFACE} {{"  # colores-ok: degradado del acabado, el azul de acción casi transparente
                " background-image: radial-gradient(1100px 700px at 82% -8%,"
                " rgba(99, 144, 255, 0.07), transparent 60%);"
                "}"
            ),
            # Tipografía (versión 3.0.0). Cifras de igual ancho en tablas y
            # recuentos, para que se alineen en columna (Practical UI, C12).
            (
                f"{_SURFACE} :is(table, .new-count, .learn-count, .review-count,"
                " .bury-count, .zero-count) { font-variant-numeric: tabular-nums; }"
            ),
            # Títulos en seminegrita y algo más ceñidos (Refactoring UI, R2;
            # vídeo de Tim Gabe sobre tipografía, P2).
            f"{_SURFACE} :is(h1, h2, h3) {{ font-weight: 600; letter-spacing: -0.01em; }}",
            # Descripción del mazo: interlineado cómodo y líneas de 70 caracteres como
            # mucho (Practical UI, P15; Refactoring UI, R8).
            f"{_SURFACE} .description {{ line-height: 1.5; max-width: 70ch; margin-inline: auto; }}",
            # Foco del teclado visible en los botones de las páginas clásicas: Anki lo
            # quita a todos con outline: none !important (APR-061).
            (
                f"html {_SURFACE} button:is(:not([class]), .but):focus-visible {{"
                " outline: 2px solid var(--border-focus) !important;"
                " outline-offset: 2px;"
                "}"
            ),
        ]
    )


def _css_text() -> str:
    """CSS completo (sin la etiqueta ``<style>``), armado una sola vez."""
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
    que solo debe llegar el primero); sin él retira el bloque anterior y añade
    el nuevo al final, de modo que Anki puede reinyectar el contenido sin dejar
    copias sueltas y nuestro estilo queda siempre el último de la página.
    """
    id_json = json.dumps(style_id)
    css_json = json.dumps(_css_text())
    action = (
        "if (document.getElementById(id)) { return; }"
        if guard_existing
        else "const old = document.getElementById(id); if (old) { old.remove(); }"
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
    if scripts.contains(script):
        return
    scripts.insert(script)


def install_early_style() -> None:
    """Registra el estilo temprano en los webviews que ya existen al arrancar."""
    if mw is None:
        return
    for webview in mw.findChildren(AnkiWebView):
        try:
            ensure_early_style(webview)
        except Exception:
            get_logger().exception("no se pudo registrar el estilo temprano")


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
