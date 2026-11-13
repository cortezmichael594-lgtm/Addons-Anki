"""Ventana de opciones: el panel modelo del taller (docs/fichas-diseno/09-patron-configuracion.md).

Aquí solo se describe el panel (recuadros y controles) y se traducen sus valores a la
configuración y de vuelta. La ventana en sí está en panel.py (pieza común del taller) y lo
que ocurre al pulsar, en actions.py.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-11-13): la ventana de opciones usaba controles estándar y no el panel modelo del taller.

from __future__ import annotations

from typing import Any

from . import logic, strings

TEST_KEY = "testSound"
VOLUME_KEY = "volume"
NAVIGATION_KEY = "navigation"


def switch_key(sound: str) -> str:
    """Clave de la casilla de un sonido en la página («on_cancel»)."""
    return f"on_{sound}"


def _values(config: dict[str, Any], present: set[str]) -> dict[str, Any]:
    values: dict[str, Any] = {
        VOLUME_KEY: config["volume"],
        NAVIGATION_KEY: config["navigation"],
        TEST_KEY: _first_present(present),
    }
    for key in logic.SOUND_KEYS:
        values[switch_key(key)] = bool(config["enabled"].get(key, True))
    return values


def _first_present(present: set[str]) -> str:
    for key, file_name in logic.SOUND_FILES.items():
        if file_name in present:
            return key
    return ""


def _file_note(file_name: str, present: set[str]) -> str:
    if file_name in present:
        return strings.FILE_READY.format(file=file_name)
    return strings.FILE_MISSING.format(file=file_name)


def _sound_check(key: str, present: set[str]) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": "check",
        "key": switch_key(key),
        "label": strings.SOUND_LABELS[key],
        "note": _file_note(logic.SOUND_FILES[key], present),
    }
    if key == "option":
        # Cuándo suena la navegación cuelga de su casilla: desmarcada, se ve apagada.
        item["children"] = [
            {
                "type": "select",
                "key": NAVIGATION_KEY,
                "label": strings.NAVIGATION_LABEL,
                "options": [{"value": mode, "label": strings.NAVIGATION_CHOICES[mode]} for mode in logic.NAV_MODES],
            }
        ]
    return item


# --- FIX-001 (2026-11-13) ---
# Síntoma: la 1.0.0 abría una ventana de controles estándar, distinta de la de los demás complementos.
# Causa: se construyó con la guía anterior; la regla del panel modelo (PROP-012) llegó a la rama principal a la vez.
# Regla: las opciones se describen como página del panel modelo (panel.py y web/), nunca con un QDialog de controles.
def page(config: dict[str, Any], present: set[str], audio_ok: bool) -> dict[str, Any]:
    """Descripción del panel."""
    missing = logic.missing_files(present)
    test_options = [
        {"value": key, "label": strings.TEST_OPTION.format(label=strings.SOUND_LABELS[key], file=file_name)}
        for key, file_name in logic.SOUND_FILES.items()
        if file_name in present
    ]
    files_items: list[dict[str, Any]] = []
    if not audio_ok:
        files_items.append({"type": "notice", "text": strings.NO_AUDIO})
    files_items.append(
        {
            "type": "select",
            "key": TEST_KEY,
            "label": strings.TEST_LABEL,
            "options": test_options,
            "unavailable": not test_options or not audio_ok,
            "empty": strings.TEST_EMPTY,
            "test": {"label": strings.TEST_BUTTON, "action": "test"},
        }
    )
    files_items.append({"type": "button", "label": strings.OPEN_FOLDER, "action": "folder"})

    defaults = _values(logic.default_config(), present)
    return {
        "title": strings.OPTIONS_TITLE,
        "values": _values(config, present),
        "defaults": defaults,
        "cards": [
            {
                "restore": True,
                "items": [
                    {
                        "type": "slider",
                        "key": VOLUME_KEY,
                        "label": strings.VOLUME_LABEL,
                        "min": 0,
                        "max": 100,
                        "step": 1,
                        "suffix": " %",
                        "note": strings.VOLUME_NOTE,
                    }
                ],
            },
            {
                "title": strings.SOUNDS_GROUP,
                "note": strings.SOUNDS_NOTE,
                "restore": True,
                "items": [_sound_check(key, present) for key in logic.SOUND_KEYS],
            },
            {
                "title": strings.FILES_GROUP,
                "note": strings.missing_summary(len(missing)),
                "items": files_items,
            },
        ],
        "focus": VOLUME_KEY,
    }


def config_from_page(values: Any) -> dict[str, Any]:
    """La configuración elegida en la página, comprobada (lo que no sirve vuelve al valor de serie)."""
    raw = values if isinstance(values, dict) else {}
    return logic.normalize_config(
        {
            "volume": raw.get(VOLUME_KEY),
            "navigation": raw.get(NAVIGATION_KEY),
            "enabled": {key: raw.get(switch_key(key)) for key in logic.SOUND_KEYS},
        }
    )


def test_request(arg: Any) -> tuple[str, int] | None:
    """Qué sonido probar y con qué volumen, al pulsar «Probar»."""
    if not isinstance(arg, dict) or arg.get("name") != "test":
        return None
    values = arg.get("values")
    if not isinstance(values, dict):
        return None
    key = values.get(TEST_KEY)
    if key not in logic.SOUND_FILES:
        return None
    return key, config_from_page(values)["volume"]
