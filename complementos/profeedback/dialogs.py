"""Ventana de ajustes de ProFeedback.

Versión 2.1.0 (petición del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012). Aceptar y Cancelar llevan el texto de Qt, ya traducido
por Anki.

Versión 2.5.0 (informe 2.4.0, aprobado entero el 2026-11-16, apartado 8.7):
dos recuadros, «Sonido» y «Aspecto», sin desplazamiento ni título repetido.
Cada lista de sonido decide sola si suena y cuál: «Sin sonido», los de serie
(«1 · Madera»…), los propios, «Aleatorio» y «Abrir la carpeta de estos
sonidos…». Las casillas de sonido desaparecen. Cada recuadro lleva
«Restaurar», como pide el modelo de opciones.

Aquí solo se describe el panel y se lee lo elegido; abrirlo y atender sus
botones está en actions.py.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-10-13): al guardar, «sonido al azar» se convertía en el primer sonido de la lista.

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from . import strings
from .config import SOUND_OFF, VOLUME_MAX, VOLUME_MIN, AddonConfig
from .paths import SoundKind

WINDOW_TITLE = "ProFeedback"
GEOMETRY_KEY = "profeedback_settings"
# Valor de la entrada «Abrir la carpeta de estos sonidos…»: abre la carpeta y la lista vuelve
# a lo que tenía.
OPEN_FOLDER = "open-folder"

# Filas de sonido, en orden: tipo, ajuste, etiqueta y nombre de «Probar» para el lector de
# pantalla. Un hueco de 16 px separa las dos de cada tarjeta de las dos del final.
SOUND_ROWS: tuple[tuple[SoundKind, str, strings.UIKey, strings.UIKey], ...] = (
    ("correct", "answerSound", "label_on_correct", "test_correct"),
    ("wrong", "wrongSound", "label_on_again", "test_again"),
    ("deck_finish", "deckFinishSound", "label_deck_finish", "test_deck_finish"),
    ("all_finish", "allDoneSound", "label_day_finish", "test_day_finish"),
)
SOUND_FIELDS: dict[SoundKind, str] = {kind: field for kind, field, _, _ in SOUND_ROWS}

# Orden de «Ver» (2.6.0): enseña el confeti de mazo en la propia ventana de opciones.
PREVIEW_CONFETTI = "preview:confetti"

_CHECKS: tuple[tuple[str, strings.UIKey], ...] = (
    ("styledButtonsEnabled", "styled_buttons"),
    ("flagsEnabled", "flags_option"),
    ("confettiEnabled", "confetti_option"),
)

LabelFor = Callable[[SoundKind, str], str]


def _plain_label(kind: SoundKind, name: str) -> str:
    return name


def _sound_value(chosen: str, names: Sequence[str]) -> str:
    """Lo que muestra la lista para un ajuste guardado."""
    # --- FIX-001 (2026-10-13) ---
    # Síntoma: al guardar los ajustes, «sonido al azar» (valor vacío) se convertía en el
    #   primer sonido de la lista y ya no volvía a ser al azar.
    # Causa: el desplegable no tenía entrada para «al azar»; al no encontrar el valor
    #   vacío mostraba el primer archivo, y ese era el que se guardaba.
    # Regla: todo desplegable de sonido lleva una entrada «Aleatorio» (valor vacío) que se
    #   guarda tal cual. Desde la 2.5.0 (informe 2.4.0, aprobado por la persona) la lista
    #   empieza por «Sin sonido» y un sonido guardado que ya no existe se muestra como el
    #   n.º 1 de la lista, no como «Aleatorio».
    if chosen in ("", SOUND_OFF) or chosen in names:
        return chosen
    return names[0] if names else ""


def _values(config: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]]) -> dict[str, Any]:
    values: dict[str, Any] = {name: getattr(config, name) for name, _ in _CHECKS}
    values["soundVolume"] = config.soundVolume
    for kind, field in SOUND_FIELDS.items():
        values[field] = _sound_value(getattr(config, field), sounds.get(kind, ()))
    return values


def _sound_select(
    kind: SoundKind,
    field: str,
    label: strings.UIKey,
    test: strings.UIKey,
    sounds: Mapping[SoundKind, Sequence[str]],
    label_for: LabelFor,
    gap: bool = False,
) -> dict[str, Any]:
    names = list(sounds.get(kind, ()))
    options: list[dict[str, Any]] = [{"value": SOUND_OFF, "label": strings.ui("sound_off")}]
    options += [{"value": name, "label": label_for(kind, name)} for name in names]
    if names:
        options.append({"value": "", "label": strings.ui("sound_random")})
    options.append({"separator": True})
    options.append({"value": OPEN_FOLDER, "label": strings.ui("open_folder"), "action": f"open:{kind}"})
    return {
        "type": "select",
        "key": field,
        "label": strings.ui(label),
        "inline": True,
        "gap": gap,
        "options": options,
        "off": SOUND_OFF,
        "test": {"label": strings.ui("test"), "aria": strings.ui(test), "action": kind},
    }


def _check(key: str, label: strings.UIKey) -> dict[str, Any]:
    """Una casilla del aspecto. «Confeti al terminar» lleva «Ver» al lado (2.6.0, informe del
    2026-11-17, 2.7), como «Probar» junto a cada sonido: enseña la celebración sin terminar un
    mazo y sin guardar nada."""
    item: dict[str, Any] = {"type": "check", "key": key, "label": strings.ui(label)}
    if key == "confettiEnabled":
        item["test"] = {
            "label": strings.ui("preview"),
            "aria": strings.ui("preview_confetti"),
            "action": PREVIEW_CONFETTI,
        }
    return item


def page(
    config: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]], label_for: LabelFor = _plain_label
) -> dict[str, Any]:
    """Descripción del panel."""
    sound_items: list[dict[str, Any]] = [
        {
            "type": "slider",
            "key": "soundVolume",
            "label": strings.ui("label_volume"),
            "inline": True,
            "min": VOLUME_MIN,
            "max": VOLUME_MAX,
            "step": 1,
            "suffix": " %",
        }
    ]
    for index, (kind, field, label, test) in enumerate(SOUND_ROWS):
        sound_items.append(_sound_select(kind, field, label, test, sounds, label_for, gap=index in (0, 2)))
    cards = [
        {"title": strings.ui("group_sound"), "restore": True, "items": sound_items},
        {
            "title": strings.ui("group_appearance"),
            "restore": True,
            "items": [_check(key, label) for key, label in _CHECKS],
        },
    ]
    return {
        "title": WINDOW_TITLE,
        # El título ya está en la barra de la ventana: no se repite dentro (informe 2.4.0, 2.5).
        "hideTitle": True,
        "values": _values(config, sounds),
        "defaults": _values(AddonConfig(), sounds),
        "cards": cards,
        "focus": "soundVolume",
    }


def _volume(value: object, fallback: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return fallback
    return max(VOLUME_MIN, min(VOLUME_MAX, value))


def _chosen(value: object, names: Sequence[str]) -> str:
    """Un sonido elegido en la página, comprobado: si no es «Sin sonido», «Aleatorio» ni uno
    de la lista, pasa a «Aleatorio» (regla de FIX-001)."""
    if isinstance(value, str) and (value in (SOUND_OFF, "") or value in names):
        return value
    return ""


def config_from_page(values: Any, saved: AddonConfig, sounds: Mapping[SoundKind, Sequence[str]]) -> AddonConfig:
    """Los ajustes elegidos en la página, con cada valor comprobado."""
    raw = values if isinstance(values, dict) else {}
    data: dict[str, Any] = {}
    for name, _ in _CHECKS:
        value = raw.get(name)
        data[name] = value if isinstance(value, bool) else getattr(saved, name)
    for kind, field in SOUND_FIELDS.items():
        data[field] = _chosen(raw.get(field), sounds.get(kind, ()))
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
    chosen = _chosen(values.get(SOUND_FIELDS[kind]), sounds.get(kind, ()))
    if chosen == SOUND_OFF:
        return None
    return kind, chosen, _volume(values.get("soundVolume"), VOLUME_MAX)


def folder_request(arg: Any) -> SoundKind | None:
    """Tipo de sonido cuya carpeta propia hay que abrir («open:correct»), o None."""
    if not isinstance(arg, dict):
        return None
    name = arg.get("name")
    if isinstance(name, str) and name.startswith("open:") and name[5:] in SOUND_FIELDS:
        kind: SoundKind = name[5:]  # type: ignore[assignment]
        return kind
    return None
