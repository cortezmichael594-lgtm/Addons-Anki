"""Valores fijos del complemento: claves de configuracion, estados y CSS.

Aqui no hay logica: solo lo que necesita ser el mismo dato en varios modulos.
"""

from __future__ import annotations

from typing import Final

from aqt.qt import QEvent

ADDON_NAME: Final[str] = "Hider"
PACKAGE_NAME: Final[str] = "hider"

# Estados de la ventana principal (aqt/main.py, MainWindowState).
REVIEW_STATE: Final[str] = "review"
DECK_BROWSER_STATE: Final[str] = "deckBrowser"
OVERVIEW_STATE: Final[str] = "overview"

# Atributos de la ventana principal donde viven las dos barras web.
TOOLBAR_ATTR: Final[str] = "toolbarWeb"
BOTTOM_BAR_ATTR: Final[str] = "bottomWeb"
MAIN_WEB_ATTR: Final[str] = "web"

KEY_HIDE_MENU_BAR: Final[str] = "hide_menu_bar"
KEY_HIDE_TOOLBAR: Final[str] = "hide_toolbar"
KEY_HIDE_BOTTOM_BAR: Final[str] = "hide_bottom_bar"
KEY_HIDE_CURSOR: Final[str] = "hide_cursor"
KEY_CURSOR_IDLE_SECONDS: Final[str] = "cursor_idle_seconds"
KEY_HIDE_SCROLLBAR: Final[str] = "hide_scrollbar"
KEY_HIDE_HARD_EASY_BUTTONS: Final[str] = "hide_hard_easy_buttons"
KEY_AUTO_START_STUDY: Final[str] = "auto_start_study"

DEFAULT_CURSOR_IDLE_SECONDS: Final[int] = 3
MIN_CURSOR_IDLE_SECONDS: Final[int] = 1
MAX_CURSOR_IDLE_SECONDS: Final[int] = 60

# Margen para dar por cumplido el tiempo de inactividad del puntero: evita
# rearmar el temporizador por unos pocos milisegundos de diferencia.
CURSOR_TOLERANCE_MS: Final[int] = 30

AGAIN_EASE: Final[int] = 1
GOOD_EASE: Final[int] = 3

# Al entrar en un mazo, Anki repinta el resumen dos veces (una por Overview.show()
# y otra por la operacion que selecciona el mazo). Se espera este margen sin
# repintados antes de saltar al repaso, para no saltar entre los dos y que el
# segundo repintado caiga encima del repasador.
AUTO_START_SETTLE_MS: Final[int] = 120

# Al salir del repaso, las barras esperan a que Anki pida el contenido de la
# pantalla siguiente. Si ese aviso no llegara, vuelven igualmente pasado esto.
CHROME_RESTORE_FALLBACK_MS: Final[int] = 400

MOUSE_EVENT_TYPES: Final[frozenset[QEvent.Type]] = frozenset(
    {QEvent.Type.MouseMove, QEvent.Type.HoverMove}
)

SCROLLBAR_STYLE_ID: Final[str] = "hider-hide-scrollbar"
TOOLBAR_STYLE_ID: Final[str] = "hider-toolbar-collapse"
BOTTOM_STYLE_ID: Final[str] = "hider-bottom-collapse"

# Colapsa el CONTENIDO de una barra web a altura cero. Anki decide la altura del
# widget midiendo document.documentElement.offsetHeight de esa pagina; con estas
# reglas toda medicion devuelve 0 y es el propio Anki quien mantiene la barra
# plegada cada vez que la remide (cambio de tema, de preferencias, de estado),
# sin que haya que pelear con sus temporizadores ni animaciones.
# !important: deben ganar a las reglas de tamano de css/toolbar.css de Anki.
COLLAPSE_RULES: Final[str] = (
    "html{height:0 !important;min-height:0 !important;overflow:hidden !important}"
    "body{display:none !important}"
)

# Solo estetico: la rueda del raton sigue desplazando la tarjeta.
SCROLLBAR_RULES: Final[str] = (
    "html{scrollbar-width:none !important}"
    "::-webkit-scrollbar{width:0 !important;height:0 !important;display:none !important}"
)


def style_tag(style_id: str, rules: str) -> str:
    """Etiqueta <style> para paginas que aun no existen (webview_will_set_content)."""
    return f'<style id="{style_id}">{rules}</style>'


def inject_style_js(style_id: str, rules: str) -> str:
    """JS idempotente para paginas ya cargadas: no duplica el estilo si ya esta."""
    return (
        "(function(){"
        f"if(document.getElementById('{style_id}'))return;"
        "var s=document.createElement('style');"
        f"s.id='{style_id}';"
        f"s.textContent='{rules}';"
        "(document.head||document.documentElement).appendChild(s);"
        "})();"
    )


def remove_style_js(style_id: str) -> str:
    return f"(function(){{var s=document.getElementById('{style_id}');if(s)s.remove();}})();"
