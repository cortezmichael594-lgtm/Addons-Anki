"""Ventana de ajustes de ProFeedback.

Versión 2.1.0 (petición del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012). Los mismos ajustes, en cuatro recuadros: el volumen con
un deslizador; el sonido al acertar; los sonidos al terminar, cada uno con su
lista desplegable y su botón «Probar», colgando de su casilla; y el aspecto.
Aceptar y Cancelar llevan el texto de Qt, ya traducido por Anki.

Aquí solo se describe el panel y se lee lo elegido; abrirlo y atender sus
botones está en actions.py.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-10-13): al guardar, «sonido al azar» se convertía en el primer sonido de la lista.

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from . import strings
from .config import VOLUME_MAX, VOLUME_MIN, AddonConfig
from .paths import SoundKind

WINDOW_TITLE = "ProFeedback"
GEOMETRY_KEY = "profeedback_settings"

# Filas de «al terminar de repasar»: tipo de sonido y texto de su etiqueta.
_FINISH_ROWS: tuple[tuple[SoundKind, strings.UIKey], ...] = (
    ("deck_finish", "label_deck_finish"),
    ("all_finish", "label_all_done"),
    ("deck_perfect", "label_deck_perfect"),
    ("all_perfect", "label_all_perfect"),
)

# Clave de la página para cada ajuste de sonido elegido.
SOUND_FIELDS: dict[SoundKind, str] = {
    "correct": "answerSound",
    "deck_finish": "deckFinishSound",
    "all_finish": "allDoneSound",
    "deck_perfect": "deckPerfectSound",
    "all_perfect": "allPerfectSound",
}

_CHECKS: tuple[str, ...] = (
    "answerSoundEnabled",
    "sessionSoundsEnabled",
    "confettiEnabled",
    "styledButtonsEnabled",
    "flagsEnabled",
)


def _label(key: strings.UIKey) -> str:
    """Etiqueta sin los dos puntos finales: en el panel va encima del control."""
    return strings.ui(key).rstrip().rstrip(":：").rstrip()


def _values(config: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]]) -> dict[str, Any]:
    values: dict[str, Any] = {name: getattr(config, name) for name in _CHECKS}
    values["soundVolume"] = config.soundVolume
    for kind, field in SOUND_FIELDS.items():
        chosen = getattr(config, field)
        # --- FIX-001 (2026-10-13) ---
        # Síntoma: al guardar los ajustes, «sonido al azar» (valor vacío) se convertía en el
        #   primer sonido de la lista y ya no volvía a ser al azar.
        # Causa: el desplegable no tenía entrada para «al azar»; al no encontrar el valor
        #   vacío mostraba el primer archivo, y ese era el que se guardaba.
        # Regla: todo desplegable de sonido lleva como primera entrada «Aleatorio» (valor
        #   vacío), y un valor guardado que ya no existe se muestra como esa entrada.
        values[field] = chosen if chosen in sounds.get(kind, ()) else ""
    return values


def _sound_select(kind: SoundKind, label: str, sounds: Mapping[SoundKind, Sequence[str]]) -> dict[str, Any]:
    names = list(sounds.get(kind, ()))
    return {
        "type": "select",
        "key": SOUND_FIELDS[kind],
        "label": label,
        "options": [{"value": "", "label": strings.ui("sound_random")}]
        + [{"value": name, "label": name} for name in names],
        "unavailable": not names,
        "test": {"label": strings.ui("test"), "action": kind},
    }


def page(config: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]]) -> dict[str, Any]:
    """Descripción del panel."""
    answer_children: list[dict[str, Any]] = []
    if not sounds.get("correct"):
        answer_children.append({"type": "note", "text": strings.ui("no_answer_sounds")})
    answer_children.append(_sound_select("correct", _label("label_sound"), sounds))
    finish_children: list[dict[str, Any]] = []
    if not any(sounds.get(kind) for kind, _ in _FINISH_ROWS):
        finish_children.append({"type": "note", "text": strings.ui("no_finish_sounds")})
    finish_children += [_sound_select(kind, _label(key), sounds) for kind, key in _FINISH_ROWS]
    cards = [
        {
            "items": [
                {
                    "type": "slider",
                    "key": "soundVolume",
                    "label": _label("label_volume"),
                    "min": VOLUME_MIN,
                    "max": VOLUME_MAX,
                    "step": 1,
                    "suffix": " %",
                }
            ]
        },
        {
            "title": strings.ui("group_answer_sounds"),
            "items": [
                {
                    "type": "check",
                    "key": "answerSoundEnabled",
                    "label": strings.ui("enable_answer_sound"),
                    "children": answer_children,
                }
            ],
        },
        {
            "title": strings.ui("group_finish_sounds"),
            "items": [
                {
                    "type": "check",
                    "key": "sessionSoundsEnabled",
                    "label": strings.ui("enable_finish_sound"),
                    "children": finish_children,
                }
            ],
        },
        {
            "title": strings.ui("group_appearance"),
            "items": [
                {"type": "check", "key": "confettiEnabled", "label": strings.ui("confetti_option")},
                {"type": "check", "key": "styledButtonsEnabled", "label": strings.ui("styled_buttons")},
                {"type": "check", "key": "flagsEnabled", "label": strings.ui("flags_option")},
                {"type": "note", "text": strings.ui("hint_own_sounds")},
            ],
        },
    ]
    defaults = _values(AddonConfig(), sounds)
    return {
        "title": WINDOW_TITLE,
        "values": _values(config, sounds),
        "defaults": defaults,
        "cards": cards,
        "focus": "soundVolume",
    }


def _volume(value: object, fallback: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return fallback
    return max(VOLUME_MIN, min(VOLUME_MAX, value))


def config_from_page(values: Any, saved: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]]) -> AddonConfig:
    """Los ajustes elegidos en la página, con cada valor comprobado: un sonido
    que no está en su lista pasa a «Aleatorio» (regla de FIX-001)."""
    raw = values if isinstance(values, dict) else {}
    data: dict[str, Any] = {}
    for name in _CHECKS:
        value = raw.get(name)
        data[name] = value if isinstance(value, bool) else getattr(saved, name)
    for kind, field in SOUND_FIELDS.items():
        value = raw.get(field)
        data[field] = value if isinstance(value, str) and value in sounds.get(kind, ()) else ""
    data["soundVolume"] = _volume(raw.get("soundVolume"), saved.soundVolume)
    return AddonConfig(**data)


def test_request(arg: Any, sounds: Mapping[SoundKind, Sequence[str]]) -> tuple[SoundKind, str, int] | None:
    """Qué hay que tocar al pulsar «Probar»: tipo, sonido elegido y volumen."""
    if not isinstance(arg, dict):
        return None
    kind = arg.get("name")
    values = arg.get("values")
    if kind not in SOUND_FIELDS or not isinstance(values, dict):
        return None
    name = values.get(SOUND_FIELDS[kind])
    chosen = name if isinstance(name, str) and name in sounds.get(kind, ()) else ""
    return kind, chosen, _volume(values.get("soundVolume"), VOLUME_MAX)
