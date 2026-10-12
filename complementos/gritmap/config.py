"""Unica capa sobre la configuracion del complemento.

Hay dos almacenes, y cada ajuste vive donde le corresponde:

  * Apariencia (tema, medida del color, tamano de celda, redondeo, ventana del
    promedio, comparativa semanal) -> configuracion del complemento
    (mw.addonManager). Es comun a todos los perfiles del equipo, que es justo
    lo que se espera de un ajuste visual.

  * Mazos excluidos y fechas clave -> configuracion de la coleccion
    (mw.col.set_config / get_config). Los identificadores de mazo solo tienen
    sentido dentro de una coleccion, asi que guardarlos en el complemento
    hacia que al cambiar de usuario se aplicaran exclusiones ajenas. Ademas,
    guardados aqui viajan con la sincronizacion a los demas dispositivos.

Todo valor que entra se valida: si falta o esta corrupto se usa el valor por
defecto, de modo que un primer arranque, una actualizacion con opciones nuevas
o un meta.json editado a mano nunca provocan un error.
"""

# Historial de correcciones de este archivo:
# FIX-005 (2026-10-08) — Un valor imposible escrito a mano en la configuracion
#                        (Infinity o NaN) hacia desaparecer el mapa sin aviso.

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from typing import TypeGuard

from aqt import mw

from .data import MEASURES, WINDOWS
from .errors import log_exception
from .palettes import THEME_NAMES

MAX_KEY_DATES = 50
MAX_LABEL_LEN = 60
KEY_DATE_MIN = date(2000, 1, 1)
KEY_DATE_MAX = date(2100, 12, 31)

CELL_SIZE_MIN, CELL_SIZE_MAX = 8, 60
BORDER_RADIUS_MIN, BORDER_RADIUS_MAX = 0, 15

# Clave unica dentro de la configuracion de la coleccion. Guarda un diccionario
# pequeno (mazos excluidos y fechas clave); la configuracion de la coleccion se
# envia entera en cada sincronizacion, por eso no debe crecer.
COL_KEY = "gritmap"

APPEARANCE_KEYS = (
    "theme",
    "measure",
    "cell_size",
    "border_radius",
    "avg_window",
    "show_week_diff",
)
COLLECTION_KEYS = ("excluded_decks", "key_dates")


@dataclass(frozen=True)
class KeyDate:
    day: date
    label: str


@dataclass(frozen=True)
class Config:
    theme: str
    # Que mide el color: "reviews", "cards" o "new" (data.MEASURES). Un "minutes"
    # guardado por la version 3.0.0 vuelve a "reviews" al leerse.
    measure: str
    cell_size: int
    border_radius: int
    # Dias de la ventana del promedio; 0 = todo el historial (data.WINDOWS).
    avg_window: int
    show_week_diff: bool
    excluded_decks: tuple[int, ...]
    key_dates: tuple[KeyDate, ...]


DEFAULT_CONFIG = Config(
    theme="classic_green",
    measure="reviews",
    cell_size=25,
    border_radius=1,
    avg_window=30,
    show_week_diff=True,
    excluded_decks=(),
    key_dates=(),
)


# Lectura y validacion de valores sueltos
# ---------------------------------------------------------------------------


def _is_number(value: object) -> TypeGuard[int | float]:
    """Numero de verdad: ni booleano, ni Infinity, ni NaN."""
    # --- FIX-005 (2026-10-08) --------------------------------------
    # Sintoma: con «Infinity» o «NaN» escrito a mano en la configuracion, el
    #          mapa desaparecia sin ningun aviso.
    # Causa: el editor de configuracion de Anki acepta esos valores como
    #        numeros, e int() falla con ellos; el fallo tumbaba la lectura de
    #        toda la configuracion.
    # Regla: todo numero que entra se comprueba con math.isfinite antes de
    #        convertirlo; si no lo es, se usa el valor por defecto.
    # ---------------------------------------------------------------
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def _as_int(value: object, fallback: int, minimum: int, maximum: int) -> int:
    if not _is_number(value):
        return fallback
    return max(minimum, min(maximum, int(value)))


def _as_measure(value: object) -> str:
    return value if isinstance(value, str) and value in MEASURES else DEFAULT_CONFIG.measure


def _as_window(value: object) -> int:
    if not _is_number(value) or int(value) != value or int(value) not in WINDOWS:
        return DEFAULT_CONFIG.avg_window
    return int(value)


def _as_bool(value: object, fallback: bool) -> bool:
    return value if isinstance(value, bool) else fallback


def _as_theme(value: object) -> str:
    return value if isinstance(value, str) and value in THEME_NAMES else DEFAULT_CONFIG.theme


def _as_deck_ids(value: object) -> tuple[int, ...]:
    if not isinstance(value, list):
        return ()
    ids: list[int] = []
    seen: set[int] = set()
    for item in value:
        # FIX-005: Infinity o NaN no son identificadores de mazo.
        if not _is_number(item):
            continue
        deck_id = int(item)
        if deck_id in seen:
            continue
        seen.add(deck_id)
        ids.append(deck_id)
    return tuple(ids)


def clean_label(value: object) -> str:
    if not isinstance(value, str):
        return ""
    cleaned = "".join(ch for ch in value if ch >= " " and ch != "\x7f")
    return cleaned.strip()[:MAX_LABEL_LEN]


def _as_key_dates(value: object) -> tuple[KeyDate, ...]:
    if not isinstance(value, list):
        return ()
    out: list[KeyDate] = []
    seen: set[KeyDate] = set()
    for item in value:
        if not isinstance(item, dict):
            continue
        raw_day = item.get("date")
        if not isinstance(raw_day, str):
            continue
        try:
            day = date.fromisoformat(raw_day.strip())
        except ValueError:
            continue
        if not (KEY_DATE_MIN <= day <= KEY_DATE_MAX):
            continue
        label = clean_label(item.get("label"))
        if not label:
            continue
        key_date = KeyDate(day=day, label=label)
        if key_date in seen:
            continue
        seen.add(key_date)
        out.append(key_date)
        if len(out) >= MAX_KEY_DATES:
            break
    out.sort(key=lambda kd: (kd.day, kd.label.casefold()))
    return tuple(out)


def _key_dates_to_json(key_dates: tuple[KeyDate, ...]) -> list[dict[str, str]]:
    return [{"date": kd.day.isoformat(), "label": kd.label} for kd in key_dates]


# Acceso a los dos almacenes
# ---------------------------------------------------------------------------


def _addon_config() -> dict[str, object]:
    try:
        loaded = mw.addonManager.getConfig(__name__)
        if isinstance(loaded, dict):
            return loaded
    except Exception as exc:
        log_exception("config._addon_config", exc)
    return {}


def _collection_config() -> dict[str, object] | None:
    """Ajustes propios de la coleccion abierta, o None si no hay ninguna."""
    col = mw.col
    if col is None:
        return None
    try:
        stored = col.get_config(COL_KEY, default=None)
    except Exception as exc:
        log_exception("config._collection_config", exc)
        return None
    return stored if isinstance(stored, dict) else {}


# Cache
# ---------------------------------------------------------------------------
# getConfig abre dos archivos del disco en cada llamada, y el mapa se dibuja
# muchas veces por sesion. Se guarda el resultado ya validado y se invalida al
# guardar opciones, al editar la configuracion desde Anki y al abrir o cerrar
# un perfil.
_cache: Config | None = None


def invalidate_cache() -> None:
    global _cache
    _cache = None


def load_config() -> Config:
    global _cache
    if _cache is not None:
        return _cache

    stored = _addon_config()
    collection = _collection_config()
    # Sin coleccion abierta no hay mazos ni fechas que aplicar: mejor vacio
    # que arrastrar los del perfil anterior.
    scoped: dict[str, object] = collection if collection is not None else {}

    config = build_config(stored, scoped)
    _cache = config
    return config


def build_config(stored: dict[str, object], scoped: dict[str, object]) -> Config:
    """Configuracion validada a partir de los dos almacenes ya leidos."""
    return Config(
        theme=_as_theme(stored.get("theme")),
        measure=_as_measure(stored.get("measure")),
        avg_window=_as_window(stored.get("avg_window")),
        cell_size=_as_int(
            stored.get("cell_size"), DEFAULT_CONFIG.cell_size, CELL_SIZE_MIN, CELL_SIZE_MAX
        ),
        border_radius=_as_int(
            stored.get("border_radius"),
            DEFAULT_CONFIG.border_radius,
            BORDER_RADIUS_MIN,
            BORDER_RADIUS_MAX,
        ),
        show_week_diff=_as_bool(stored.get("show_week_diff"), DEFAULT_CONFIG.show_week_diff),
        excluded_decks=_as_deck_ids(scoped.get("excluded_decks")),
        key_dates=_as_key_dates(scoped.get("key_dates")),
    )


def save_config(cfg: Config) -> None:
    """Guarda cada ajuste en su almacen y refresca la cache."""
    appearance: dict[str, object] = dict(_addon_config())
    appearance.update(
        {
            "theme": cfg.theme,
            "measure": cfg.measure,
            "cell_size": cfg.cell_size,
            "border_radius": cfg.border_radius,
            "avg_window": cfg.avg_window,
            "show_week_diff": cfg.show_week_diff,
        }
    )
    try:
        mw.addonManager.writeConfig(__name__, appearance)
    except Exception as exc:
        log_exception("config.save_config/addon", exc)

    col = mw.col
    if col is not None:
        try:
            # set_config directo, sin CollectionOp, y sin entrada de deshacer:
            # es un ajuste de la interfaz, no contenido de estudio. Es lo mismo
            # que hace Anki con las busquedas guardadas, el orden de columnas
            # del navegador o los nombres de las banderas. Envolverlo en una
            # operacion deshacible ensuciaria el menu Editar -> Deshacer con
            # un paso que la persona no espera poder revertir.
            col.set_config(
                COL_KEY,
                {
                    "excluded_decks": list(cfg.excluded_decks),
                    "key_dates": _key_dates_to_json(cfg.key_dates),
                },
            )
        except Exception as exc:
            log_exception("config.save_config/collection", exc)

    invalidate_cache()


def migrate_to_collection() -> None:
    """Traslada ajustes de versiones anteriores a la coleccion abierta.

    Hasta ahora los mazos excluidos y las fechas clave se guardaban junto a la
    apariencia, fuera de la coleccion. Al abrir un perfil que todavia no tiene
    sus propios ajustes se copian alli una sola vez, de modo que nadie pierde
    lo que ya tenia configurado. Los valores antiguos se dejan donde estaban:
    los identificadores de mazo de otra coleccion simplemente no coinciden con
    ningun mazo y se descartan al filtrar.
    """
    col = mw.col
    if col is None:
        return
    try:
        if col.get_config(COL_KEY, default=None) is not None:
            return
        legacy = _addon_config()
        excluded = _as_deck_ids(legacy.get("excluded_decks"))
        key_dates = _as_key_dates(legacy.get("key_dates"))
        if not excluded and not key_dates:
            return
        col.set_config(
            COL_KEY,
            {
                "excluded_decks": list(excluded),
                "key_dates": _key_dates_to_json(key_dates),
            },
        )
    except Exception as exc:
        log_exception("config.migrate_to_collection", exc)
    finally:
        invalidate_cache()
