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
from aqt.utils import tooltip

from . import config, contrast, dialogs, strings, theming, themes, titlebar, webview_style
from .errors import guard, note_failure


@guard
def _welcome() -> None:
    """La primera vez que Anki arranca con Nocturne, un aviso con el camino para
    cambiar de paleta (Norman, descubribilidad). Solo una vez."""
    if config.take_welcome():
        tooltip(strings.WELCOME, period=6000)


@guard
def _on_profile_open() -> None:
    if mw is not None:
        # Un momento después de abrir el perfil, cuando ya se ve la ventana principal.
        mw.progress.single_shot(1500, _welcome, False)


def _setup() -> None:
    # 0) La paleta elegida en la configuración (Nocturne si no hay ninguna válida).
    themes.select(config.load())

    # Elegir paleta y el aviso de bienvenida, en cualquier caso.
    mw.addonManager.setConfigAction(__name__, dialogs.open_dialog)
    gui_hooks.profile_did_open.append(_on_profile_open)

    # Si el sistema pide más contraste, Nocturne no pinta nada (versión 3.5.0).
    if contrast.system_wants_more_contrast():
        contrast.step_aside()
        return

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


if mw is not None:
    try:
        _setup()
    except Exception:
        # Ante cualquier imprevisto, Anki conserva su apariencia y sigue estable.
        note_failure("la inicialización de Nocturne falló")
