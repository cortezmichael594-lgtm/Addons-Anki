"""Nocturne — temas de color para Anki (modo día y modo noche).

Este archivo solo orquesta: aplica la paleta elegida y registra los enganches
y la configuración. Toda la lógica vive en los módulos vecinos. Hay tres paletas
(Nocturne por defecto, Papel y Bosque) y una ventana para elegirla, que se abre
solo desde el botón «Configuración» de la ventana de complementos (decisión del
cliente, 2026-10-21). En Windows 11, también la barra de título de las ventanas
toma los colores de la paleta. Sus textos están en español (strings.py).
"""

from __future__ import annotations

from aqt import gui_hooks, mw

from . import config, dialogs, theming, themes, titlebar, webview_style
from .errors import get_logger


def _setup() -> None:
    # 0) La paleta elegida en la configuración (Nocturne si no hay ninguna válida).
    themes.select(config.load())

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
    #    - Barra de título de las ventanas del color de la paleta (solo Windows 11).
    titlebar.install()

    # 3) Dejar preparado el estilo temprano, que aplica la paleta antes del
    #    primer pintado de cada página y evita el fogonazo al abrirlas.
    webview_style.install_early_style()

    # 4) Aplicar la paleta a la interfaz nativa ya mismo. Anki construye su hoja
    #    de estilo antes de cargar los complementos, así que hay que rehacerla.
    theming.restyle()

    # 5) Elegir paleta: solo desde el botón «Configuración» de la ventana de
    #    complementos (Herramientas > «Complementos»).
    mw.addonManager.setConfigAction(__name__, dialogs.open_dialog)


if mw is not None:
    try:
        _setup()
    except Exception:
        # Ante cualquier imprevisto, Anki conserva su apariencia y sigue estable.
        get_logger().exception("la inicialización de Nocturne falló")
