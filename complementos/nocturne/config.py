"""Configuración del complemento: solo la paleta elegida.

Se guarda con el sistema de configuración de Anki (config.json y meta.json de la
carpeta del complemento). Una configuración antigua, vacía o escrita a mano con
un valor que no existe vuelve a Nocturne sin fallar.
"""

from __future__ import annotations

from typing import Any

from .themes import DEFAULT_THEME, valid_id

KEY = "palette"


def palette_from(config: Any) -> str:
    """La paleta guardada en un diccionario de configuración, ya comprobada."""
    if not isinstance(config, dict):
        return DEFAULT_THEME
    return valid_id(config.get(KEY))


def load() -> str:
    from aqt import mw

    if mw is None:
        return DEFAULT_THEME
    return palette_from(mw.addonManager.getConfig(__name__))


def save(theme_id: str) -> None:
    from aqt import mw

    if mw is None:
        return
    config = mw.addonManager.getConfig(__name__)
    if not isinstance(config, dict):
        config = {}
    config[KEY] = valid_id(theme_id)
    mw.addonManager.writeConfig(__name__, config)
