"""Única capa sobre la configuración del complemento.

El resto del código lee y guarda ajustes solo a través de este módulo. Así un ajuste que
falte (primer arranque, o una versión anterior que no lo tenía) o que traiga un valor que no
sirve nunca rompe nada: se usa el valor por defecto.

Anki guarda la configuración en el meta.json del complemento, que es común a todos los
perfiles de ese ordenador y no viaja con la sincronización.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Final

from aqt import mw

VOLUME_MIN: Final[int] = 0
VOLUME_MAX: Final[int] = 100

# Claves que usaba la versión anterior para guardar «el día de hoy» dentro de la
# configuración. Ya no se usan (ahora el día sale del historial de Anki): se quitan al guardar
# para no dejar basura en el meta.json.
_OBSOLETE_KEYS: Final[tuple[str, ...]] = (
    "confettiDayDate",
    "confettiDayAnswers",
    "confettiDayPerfect",
)


@dataclass(slots=True, frozen=True)
class AddonConfig:
    """Ajustes que la persona cambia desde la ventana de configuración.

    Los nombres coinciden con las claves de config.json (y con las que ya guardaron las
    versiones anteriores): no se cambian para no perder lo que la persona eligió.
    """

    answerSoundEnabled: bool = True
    sessionSoundsEnabled: bool = True
    confettiEnabled: bool = True
    styledButtonsEnabled: bool = True
    flagsEnabled: bool = True
    answerSound: str = ""
    deckFinishSound: str = ""
    allDoneSound: str = ""
    deckPerfectSound: str = ""
    allPerfectSound: str = ""
    soundVolume: int = VOLUME_MAX

    @classmethod
    def from_stored(cls, stored: object) -> AddonConfig:
        """Construye los ajustes desde lo guardado, descartando lo que no sirva.

        Validación en la frontera: el archivo lo puede haber tocado cualquiera, así que un
        valor de tipo raro se descarta y se queda el valor por defecto; una clave
        desconocida se ignora; y el volumen se limita al rango válido.
        """
        defaults = cls()
        if not isinstance(stored, dict):
            return defaults
        data: dict[str, object] = {}
        for field in fields(cls):
            value = stored.get(field.name)
            expected = type(getattr(defaults, field.name))
            # bool es un caso especial de int en Python: un true no es un volumen.
            if isinstance(value, bool) != (expected is bool):
                continue
            if isinstance(value, expected):
                data[field.name] = value
        volume = data.get("soundVolume")
        if isinstance(volume, int):
            data["soundVolume"] = max(VOLUME_MIN, min(VOLUME_MAX, volume))
        return cls(**data)  # type: ignore[arg-type]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_cached: AddonConfig | None = None


def _read_stored() -> object:
    if mw is None:
        return None
    return mw.addonManager.getConfig(__name__.split(".")[0])


def get() -> AddonConfig:
    """Ajustes actuales. Se leen del disco una vez y se reutilizan; véase reload()."""
    global _cached
    if _cached is None:
        _cached = AddonConfig.from_stored(_read_stored())
    return _cached


def reload() -> AddonConfig:
    """Vuelve a leer los ajustes (al abrir un perfil o tras guardarlos)."""
    global _cached
    _cached = None
    return get()


def save(config: AddonConfig) -> None:
    """Guarda los ajustes y deja la caché al día."""
    global _cached
    if mw is None:
        return
    package = __name__.split(".")[0]
    stored = _read_stored()
    merged: dict[str, object] = dict(stored) if isinstance(stored, dict) else {}
    for key in _OBSOLETE_KEYS:
        merged.pop(key, None)
    merged.update(config.to_dict())
    mw.addonManager.writeConfig(package, merged)
    _cached = config
