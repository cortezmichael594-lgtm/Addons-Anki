"""Cambiar de paleta con Anki en marcha, sin reiniciar."""

from __future__ import annotations

from . import config, theming, themes, webview_style


def apply_palette(theme_id: str) -> str:
    """Aplica la paleta a ventanas y páginas sin guardarla (vista previa) y devuelve
    su identificador.

    Orden: primero los colores y medidas de Anki, después su hoja de estilo (que
    avisa a las páginas para que repinten su fondo) y por último el estilo de cada
    página abierta. Las que se abran después ya nacen con la paleta nueva.
    """
    selected = themes.select(theme_id)
    webview_style.reset()
    theming.write_theme_colors()
    theming.restyle()
    webview_style.refresh_open_pages()
    return selected


def choose_palette(theme_id: str) -> str:
    """Aplica la paleta y la guarda."""
    selected = apply_palette(theme_id)
    config.save(selected)
    return selected
