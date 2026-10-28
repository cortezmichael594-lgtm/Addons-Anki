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


RENAMED_KEY = "renamed_shown"


def notice_for(config: Any) -> str | None:
    """Qué aviso único toca: «welcome» a quien instala por primera vez, «renamed» a quien
    ya tenía el complemento con el nombre de Nocturne (vio su bienvenida) y nada si ya
    vio el que le toca."""
    if not isinstance(config, dict):
        return "welcome"
    if config.get(WELCOME_KEY) is not True:
        return "welcome"
    if config.get(RENAMED_KEY) is not True:
        return "renamed"
    return None


def take_notice() -> str | None:
    """El aviso único que toca (y lo anota para que no se repita). Quien lo recibe por
    primera vez ya conoce el nombre nuevo, así que queda anotado también el de nombre."""
    from aqt import mw

    if mw is None:
        return None
    config = mw.addonManager.getConfig(__name__)
    notice = notice_for(config)
    if notice is None:
        return None
    data = dict(config) if isinstance(config, dict) else {}
    data[WELCOME_KEY] = True
    data[RENAMED_KEY] = True
    mw.addonManager.writeConfig(__name__, data)
    return notice
