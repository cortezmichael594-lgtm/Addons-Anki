"""Single configuration layer wrapping addonManager.getConfig/writeConfig.

The rest of the code only talks to this module. Values are validated at this
boundary and clamped to safe ranges.

Two different stores, on purpose:

- The VISIBLE options (theme, height, spacing, checkpoints, effects, excluded
  decks) live in the add-on config, which is one per installation.
- The personal RECORD lives in the collection (mw.col.get_config /
  set_config), so it belongs to the profile that earned it and travels with a
  sync. See FIX-002 below.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-07-27) — El record se mezclaba entre usuarios y podia fallar al
#                        cambiar de perfil.

from __future__ import annotations

from dataclasses import dataclass

from aqt import mw

from .errors import report
from .palettes import DEFAULT_THEME, THEME_KEYS

# --- FIX-002 (2026-07-27) --------------------------------------
# Sintoma: con dos usuarios en el mismo Anki, el record de uno aparecia en el
#   perfil del otro; ademas, guardar al cerrar podia llegar con la coleccion
#   ya cerrada.
# Causa: el record vivia en la configuracion del complemento, que es UNICA
#   para toda la instalacion y no depende del perfil abierto.
# Regla: lo que pertenece a UNA coleccion (progreso, records, marcas de
#   estudio) se guarda con mw.col.set_config / get_config, nunca en la
#   configuracion del complemento; y toda lectura o escritura de la coleccion
#   comprueba antes que mw.col exista.
# ---------------------------------------------------------------
COL_BEST_STREAK_KEY: str = "coreprogress_best_streak"
LEGACY_BEST_STREAK_KEY: str = "best_streak"
_MAX_STREAK: int = 1_000_000

BAR_HEIGHT_MIN: int = 12
BAR_HEIGHT_MAX: int = 22
PUSH_MIN: int = 0
PUSH_MAX: int = 300


@dataclass(frozen=True)
class Config:
    theme: str
    effects_enabled: bool
    checkpoints_enabled: bool
    bar_height: int
    push_down: int
    excluded_decks: tuple[int, ...]


DEFAULT_CONFIG = Config(
    theme=DEFAULT_THEME,
    effects_enabled=True,
    checkpoints_enabled=True,
    bar_height=16,
    push_down=0,
    excluded_decks=(),
)


def _log(exc: Exception) -> None:
    report(exc, "settings")


def _as_int(value: object, fallback: int, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return fallback
    return max(minimum, min(maximum, int(value)))


def _as_bool(value: object, fallback: bool) -> bool:
    return value if isinstance(value, bool) else fallback


def _theme_from_legacy(stored: dict[str, object]) -> str | None:
    for key in THEME_KEYS:
        if stored.get(key) is True:
            return key
    return None


def _as_theme(stored: dict[str, object]) -> str:
    value = stored.get("theme")
    if isinstance(value, str) and value in THEME_KEYS:
        return value
    legacy = _theme_from_legacy(stored)
    return legacy if legacy is not None else DEFAULT_THEME


def _as_deck_ids(value: object) -> tuple[int, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    ids: list[int] = []
    for item in value:
        if isinstance(item, bool):
            continue
        if isinstance(item, int):
            ids.append(int(item))
        elif isinstance(item, str) and item.lstrip("-").isdigit():
            ids.append(int(item))
    return tuple(dict.fromkeys(ids))


def _raw() -> dict[str, object]:
    try:
        loaded = mw.addonManager.getConfig(__name__)
        if isinstance(loaded, dict):
            return dict(loaded)
    except Exception as exc:
        _log(exc)
    return {}


def load_config() -> Config:
    stored = _raw()
    return Config(
        theme=_as_theme(stored),
        effects_enabled=_as_bool(stored.get("effects_enabled"), DEFAULT_CONFIG.effects_enabled),
        checkpoints_enabled=_as_bool(
            stored.get("checkpoints_enabled"), DEFAULT_CONFIG.checkpoints_enabled
        ),
        bar_height=_as_int(
            stored.get("bar_height"), DEFAULT_CONFIG.bar_height, BAR_HEIGHT_MIN, BAR_HEIGHT_MAX
        ),
        push_down=_as_int(stored.get("push_down"), DEFAULT_CONFIG.push_down, PUSH_MIN, PUSH_MAX),
        excluded_decks=_as_deck_ids(stored.get("excluded_decks")),
    )


def save_config(cfg: Config) -> None:
    # HISTORIAL: escribir un dict "limpio" borraba el record al guardar ajustes
    # (entonces vivía aquí; hoy vive en la colección, ver FIX-002). La regla que
    # dejó ese fallo sigue en pie: siempre merge sobre lo almacenado, para que
    # cualquier clave ajena al diálogo sobreviva a Guardar y a Restaurar los
    # valores predeterminados.
    data = _raw()
    data.update(
        {
            "theme": cfg.theme,
            "effects_enabled": cfg.effects_enabled,
            "checkpoints_enabled": cfg.checkpoints_enabled,
            "bar_height": cfg.bar_height,
            "push_down": cfg.push_down,
            "excluded_decks": list(dict.fromkeys(cfg.excluded_decks)),
        }
    )
    try:
        mw.addonManager.writeConfig(__name__, data)
    except Exception as exc:
        _log(exc)


# --- El record, guardado en la coleccion (ver FIX-002 arriba) ---------------
# set_config no crea una entrada de deshacer y CONSERVA el historial existente
# (pylib/anki/collection.py). Es justo lo que interesa: el record es una
# preferencia, no contenido de estudio; meterlo en Editar -> Deshacer taparia
# el "deshacer respuesta" que la persona si necesita.
def _col_available() -> bool:
    return bool(mw and mw.col)


def _write_best_streak(value: int) -> None:
    try:
        if _col_available():
            mw.col.set_config(COL_BEST_STREAK_KEY, int(value))
    except Exception as exc:
        _log(exc)


def load_best_streak() -> int:
    try:
        if _col_available():
            return _as_int(mw.col.get_config(COL_BEST_STREAK_KEY, 0), 0, 0, _MAX_STREAK)
    except Exception as exc:
        _log(exc)
    return 0


def save_best_streak(value: int) -> None:
    if value <= 0 or not _col_available():
        return
    if load_best_streak() >= value:
        return
    _write_best_streak(value)


def reset_best_streak() -> None:
    """Explicit user action: set the stored record back to zero."""
    _write_best_streak(0)


def rollback_best_streak(value: int) -> None:
    """Lower the stored record after an undo.

    HISTORIAL: los récords se guardan en el momento de lograrse (protección
    ante cierres bruscos); al deshacer esas respuestas, el valor guardado debe
    bajar con ellas. Esta función solo baja; subir sigue siendo trabajo de
    save_best_streak.
    """
    target = max(0, int(value))
    if not _col_available() or load_best_streak() <= target:
        return
    _write_best_streak(target)


def migrate_best_streak() -> None:
    """Move a record saved by an older version into the open collection.

    FIX-002: las versiones anteriores guardaban el record en la configuracion
    del complemento. Al abrir un perfil se traslada a su coleccion (se queda el
    valor mas alto de los dos) y se retira la clave antigua, para que dejen de
    mezclarse los records de distintos usuarios y para que la configuracion del
    complemento contenga solo las opciones visibles.
    """
    if not _col_available():
        return
    data = _raw()
    if LEGACY_BEST_STREAK_KEY not in data:
        return
    legacy = _as_int(data.get(LEGACY_BEST_STREAK_KEY), 0, 0, _MAX_STREAK)
    if legacy > load_best_streak():
        _write_best_streak(legacy)
    data.pop(LEGACY_BEST_STREAK_KEY, None)
    try:
        mw.addonManager.writeConfig(__name__, data)
    except Exception as exc:
        _log(exc)