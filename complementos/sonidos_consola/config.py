"""Única capa sobre la configuración del complemento.

Se guarda una copia en memoria: los tics de navegación consultan la configuración muchas
veces por segundo, y leerla del disco cada vez entrecortaría Anki.
"""

from __future__ import annotations

from typing import Any

from aqt import mw

from . import logic

_cache: dict[str, Any] | None = None


def load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        stored = mw.addonManager.getConfig(__name__) if mw is not None else None
        _cache = logic.normalize_config(stored)
    return _cache


def save(values: dict[str, Any]) -> None:
    global _cache
    _cache = logic.normalize_config(values)
    if mw is not None:
        mw.addonManager.writeConfig(__name__, _cache)
