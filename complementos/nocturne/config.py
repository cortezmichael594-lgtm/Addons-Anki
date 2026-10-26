"""Configuración del complemento: la paleta elegida y, desde la versión 3.5.0, si ya
se vio el aviso de bienvenida (no es un ajuste: no aparece en ninguna ventana).

Se guarda con el sistema de configuración de Anki (config.json y meta.json de la
carpeta del complemento). Una configuración antigua, vacía o escrita a mano con
un valor que no existe vuelve a Nocturne sin fallar.
"""

from __future__ import annotations

from typing import Any

from .themes import DEFAULT_THEME, valid_id

KEY = "palette"
WELCOME_KEY = "welcome_shown"


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


def welcome_shown(config: Any) -> bool:
    """True si el aviso de bienvenida ya se mostró."""
    return isinstance(config, dict) and config.get(WELCOME_KEY) is True


def take_welcome() -> bool:
    """True la primera vez que se pide; lo anota para que no se repita."""
    from aqt import mw

    if mw is None:
        return False
    config = mw.addonManager.getConfig(__name__)
    if welcome_shown(config):
        return False
    data = dict(config) if isinstance(config, dict) else {}
    data[WELCOME_KEY] = True
    mw.addonManager.writeConfig(__name__, data)
    return True
