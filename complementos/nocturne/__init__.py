"""Nocturne — tema de colores para Anki (modo día y modo noche).

Este archivo solo orquesta: reafirma la paleta y registra los enganches. Toda la
lógica vive en los módulos vecinos. El complemento no tiene configuración: se
instala y aplica su apariencia, y no muestra ni un texto propio, de modo que
funciona igual con Anki en cualquier idioma.
"""

from __future__ import annotations

from aqt import gui_hooks, mw

from . import theming, webview_style
from .errors import get_logger


def _setup() -> None:
    # 1) Volcar la paleta sobre los tokens de color de Anki. Se hace lo primero,
    #    y al importar el complemento, para que todo lo que Anki construya a
    #    partir de aquí nazca ya con estos colores.
    theming.write_theme_colors()

    # 2) Registrar los enganches del canal web.
    #    - Páginas internas de Anki: estilo en el HTML inicial.
    gui_hooks.webview_will_set_content.append(webview_style.on_will_set_content)
    #    - Páginas externas (gráficas, felicitación): estilo en cuanto cargan.
    gui_hooks.webview_did_inject_style_into_page.append(webview_style.on_did_inject_style)
    #    - Cambio de perfil: reafirmar colores.
    gui_hooks.profile_did_open.append(theming.on_profile_open)
    #    - Hoja de estilo de las ventanas: borde propio de las casillas. Va antes
    #      del paso 4, que es cuando Anki rehace la hoja y pasa por este filtro.
    gui_hooks.style_did_init.append(theming.on_style_did_init)

    # 3) Dejar preparado el estilo temprano, que aplica la paleta antes del
    #    primer pintado de cada página y evita el fogonazo al abrirlas.
    webview_style.install_early_style()

    # 4) Aplicar la paleta a la interfaz nativa ya mismo. Anki construye su hoja
    #    de estilo antes de cargar los complementos, así que hay que rehacerla.
    theming.restyle()


if mw is not None:
    try:
        _setup()
    except Exception:
        # Ante cualquier imprevisto, Anki conserva su apariencia y sigue estable.
        get_logger().exception("la inicialización de Nocturne falló")
