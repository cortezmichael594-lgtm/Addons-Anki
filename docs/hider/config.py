"""Unica capa sobre getConfig / writeConfig, con valores por defecto seguros.

Toda lectura pasa por aqui, de modo que una clave que falte (instalacion nueva,
opcion anadida en una version posterior, meta.json editado a mano) nunca provoca
un error: devuelve el valor recomendado.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from aqt import mw

from . import constants


@dataclass(frozen=True, slots=True)
class HiderConfig:
    hide_menu_bar: bool
    hide_toolbar: bool
    hide_bottom_bar: bool
    hide_cursor: bool
    cursor_idle_seconds: int
    hide_scrollbar: bool
    hide_hard_easy_buttons: bool
    auto_start_study: bool

    @property
    def cursor_idle_ms(self) -> int:
        return self.cursor_idle_seconds * 1000


DEFAULT_CONFIG: HiderConfig = HiderConfig(
    hide_menu_bar=True,
    hide_toolbar=True,
    hide_bottom_bar=True,
    hide_cursor=True,
    cursor_idle_seconds=constants.DEFAULT_CURSOR_IDLE_SECONDS,
    hide_scrollbar=True,
    hide_hard_easy_buttons=True,
    auto_start_study=True,
)


def _as_bool(raw: dict[str, Any], key: str, default: bool) -> bool:
    value = raw.get(key, default)
    return value if isinstance(value, bool) else default


def _as_idle_seconds(raw: dict[str, Any], key: str, default: int) -> int:
    value = raw.get(key, default)
    # Un booleano es un int en Python: hay que descartarlo antes de aceptarlo como numero.
    if not isinstance(value, int) or isinstance(value, bool):
        return default
    if value < constants.MIN_CURSOR_IDLE_SECONDS or value > constants.MAX_CURSOR_IDLE_SECONDS:
        return default
    return value


def load_config() -> HiderConfig:
    try:
        stored: dict[str, Any] | None = mw.addonManager.getConfig(__name__)
    except Exception:
        stored = None
    raw: dict[str, Any] = stored if isinstance(stored, dict) else {}
    return HiderConfig(
        hide_menu_bar=_as_bool(raw, constants.KEY_HIDE_MENU_BAR, DEFAULT_CONFIG.hide_menu_bar),
        hide_toolbar=_as_bool(raw, constants.KEY_HIDE_TOOLBAR, DEFAULT_CONFIG.hide_toolbar),
        hide_bottom_bar=_as_bool(
            raw, constants.KEY_HIDE_BOTTOM_BAR, DEFAULT_CONFIG.hide_bottom_bar
        ),
        hide_cursor=_as_bool(raw, constants.KEY_HIDE_CURSOR, DEFAULT_CONFIG.hide_cursor),
        cursor_idle_seconds=_as_idle_seconds(
            raw, constants.KEY_CURSOR_IDLE_SECONDS, DEFAULT_CONFIG.cursor_idle_seconds
        ),
        hide_scrollbar=_as_bool(raw, constants.KEY_HIDE_SCROLLBAR, DEFAULT_CONFIG.hide_scrollbar),
        hide_hard_easy_buttons=_as_bool(
            raw, constants.KEY_HIDE_HARD_EASY_BUTTONS, DEFAULT_CONFIG.hide_hard_easy_buttons
        ),
        auto_start_study=_as_bool(
            raw, constants.KEY_AUTO_START_STUDY, DEFAULT_CONFIG.auto_start_study
        ),
    )


def save_config(config: HiderConfig) -> None:
    # asdict() reproduce exactamente las claves de config.json porque los nombres
    # de los campos y las claves coinciden a proposito.
    data: dict[str, Any] = asdict(config)
    mw.addonManager.writeConfig(__name__, data)
