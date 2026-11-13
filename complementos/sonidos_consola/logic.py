"""Reglas de los sonidos, sin Qt ni Anki, para poder probarlas.

Aquí se decide qué archivo corresponde a cada sonido, cómo se normaliza la configuración,
cómo se pasa el volumen de la barra a la escala del altavoz y cuándo un sonido debe sonar
o callarse para que no se pisen entre ellos.
"""

from __future__ import annotations

from typing import Any

# Clave interna de cada sonido y el archivo que la persona copia en la carpeta de sonidos.
# El orden es el de la ventana del complemento.
SOUND_FILES: dict[str, str] = {
    "coldboot": "coldboot_stereo.wav",
    "gameboot": "gameboot_stereo.wav",
    "option": "snd_option.wav",
    "cancel": "snd_cancel.wav",
    "system_ok": "snd_system_ok.wav",
    "system_ng": "snd_system_ng.wav",
    "trophy": "snd_trophy.wav",
    "error": "snd_error.wav",
}
SOUND_KEYS: tuple[str, ...] = tuple(SOUND_FILES)

NAV_HOVER = "hover"
NAV_CLICK = "click"
# «Nunca» se retiró en la 1.2.0: para no oír la navegación se desmarca su casilla. Un config.json
# antiguo con este valor se convierte en la casilla desmarcada.
NAV_OFF = "off"
NAV_MODES: tuple[str, ...] = (NAV_HOVER, NAV_CLICK)

DEFAULT_VOLUME = 70

# Sonidos que tienen prioridad: al empezar, callan la navegación y el globo, y durante un
# momento no dejan que la navegación los tape.
PRIORITY_SOUNDS = frozenset({"cancel", "system_ok", "system_ng", "error", "trophy"})
# Sonidos que se callan cuando empieza uno con prioridad.
INTERRUPTIBLE_SOUNDS = ("option", "gameboot")

# Tiempo mínimo entre dos tics de navegación (milisegundos): al pasar el ratón muy rápido se
# oye un tic seguido, no un ruido.
OPTION_MIN_GAP_MS = 60
# Tras un sonido con prioridad, la navegación calla este tiempo para no taparlo.
PRIORITY_QUIET_MS = 250
# Un mismo sonido que llega dos veces casi a la vez (por ejemplo, la X de una ventana avisa
# al cerrarse y al cancelarse) suena una sola vez.
DUPLICATE_GAP_MS = 150


def default_config() -> dict[str, Any]:
    return {
        "volume": DEFAULT_VOLUME,
        "navigation": NAV_HOVER,
        "enabled": dict.fromkeys(SOUND_KEYS, True),
    }


def normalize_config(stored: object) -> dict[str, Any]:
    """Completa y corrige lo guardado: nunca falla, aunque venga de una versión antigua o a mano.

    El volumen se recorta entre 0 y 100; un modo de navegación desconocido vuelve al de
    por defecto; cada sonido sin valor válido queda encendido; lo desconocido se descarta.
    """
    config = default_config()
    if not isinstance(stored, dict):
        return config

    volume = stored.get("volume")
    if isinstance(volume, (int, float)) and not isinstance(volume, bool):
        config["volume"] = max(0, min(100, round(volume)))

    navigation = stored.get("navigation")
    if navigation in NAV_MODES:
        config["navigation"] = navigation
    old_navigation_off = navigation == NAV_OFF

    enabled = stored.get("enabled")
    if isinstance(enabled, dict):
        for key in SOUND_KEYS:
            value = enabled.get(key)
            if isinstance(value, bool):
                config["enabled"][key] = value
    if old_navigation_off:
        config["enabled"]["option"] = False
    return config


def linear_volume(percent: int) -> float:
    """Pasa el volumen de la barra (0-100) a la escala del altavoz (0,0-1,0).

    El oído no percibe el volumen de forma lineal: con la curva al cuadrado, la mitad de
    la barra suena como «la mitad» y no casi igual que el máximo.
    """
    fraction = max(0, min(100, percent)) / 100
    return fraction * fraction


class SoundGate:
    """Decide si un sonido debe sonar ahora, para que no se pisen.

    Recibe la hora en milisegundos desde fuera (un reloj que solo avanza), así que se
    puede probar sin esperar.
    """

    def __init__(self) -> None:
        self._last_played: dict[str, int] = {}
        self._last_priority = -(10**9)

    def allow(self, key: str, now_ms: int) -> bool:
        last = self._last_played.get(key)
        if key == "option":
            if now_ms - self._last_priority < PRIORITY_QUIET_MS:
                return False
            if last is not None and now_ms - last < OPTION_MIN_GAP_MS:
                return False
        elif last is not None and now_ms - last < DUPLICATE_GAP_MS:
            return False
        self._last_played[key] = now_ms
        if key in PRIORITY_SOUNDS:
            self._last_priority = now_ms
        return True


def sounds_to_stop(key: str) -> tuple[str, ...]:
    """Sonidos que se callan cuando empieza «key»."""
    if key in PRIORITY_SOUNDS:
        return INTERRUPTIBLE_SOUNDS
    return ()


def missing_files(present: set[str]) -> list[str]:
    """Archivos de sonido que faltan, en el orden de la ventana."""
    return [name for name in SOUND_FILES.values() if name not in present]
