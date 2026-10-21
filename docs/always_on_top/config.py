"""Unica capa sobre la configuracion del complemento.

Regla: nadie fuera de este modulo llama a getConfig ni a writeConfig. Asi
una opcion que falte -primer arranque, o configuracion guardada por una
version anterior del complemento- siempre devuelve un valor por defecto
seguro en lugar de reventar.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aqt import mw
from aqt.qt import QKeySequence

from . import constants, shortcuts


@dataclass(frozen=True)
class Settings:
    shortcut: str


def _sanitize_shortcut(value: object) -> str:
    """Devuelve un atajo utilizable, venga como venga el valor guardado."""
    if not isinstance(value, str):
        return constants.DEFAULT_SHORTCUT
    text = value.strip()
    if not text:
        return constants.DEFAULT_SHORTCUT

    sequence = QKeySequence(text)
    # Qt acepta cadenas sin sentido y las convierte en una tecla "desconocida";
    # el viaje de ida y vuelta a texto es lo que las delata.
    normalized = sequence.toString(QKeySequence.SequenceFormat.PortableText)
    if sequence.isEmpty() or not normalized or "unknown" in normalized.lower():
        return constants.DEFAULT_SHORTCUT

    # Un atajo guardado por una version anterior puede chocar con uno de Anki.
    # En ese caso vuelve al valor por defecto, que si esta libre: dos atajos
    # peleandose por la misma tecla dan un comportamiento impredecible.
    if not shortcuts.has_required_modifier(normalized) or shortcuts.used_by_anki(normalized):
        return constants.DEFAULT_SHORTCUT
    return normalized


def _raw() -> dict[str, Any]:
    try:
        stored = mw.addonManager.getConfig(__name__)
    except Exception:
        return {}
    return dict(stored) if isinstance(stored, dict) else {}


def load() -> Settings:
    return Settings(
        shortcut=_sanitize_shortcut(_raw().get(constants.CONFIG_KEY_SHORTCUT))
    )


def save(settings: Settings) -> None:
    # Se conserva lo demas que hubiera guardado, por si una version futura
    # del complemento anade opciones y esta se ejecuta despues de aquella.
    data = _raw()
    data[constants.CONFIG_KEY_SHORTCUT] = settings.shortcut
    mw.addonManager.writeConfig(__name__, data)
