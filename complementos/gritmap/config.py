"""Unica capa sobre la configuracion del complemento.

Hay dos almacenes, y cada ajuste vive donde le corresponde:

  * Apariencia y metas (tema, medida del color, tamano de celda, redondeo,
    periodo de las cifras, meta diaria, comodines y mostrar racha y meta) -> configuracion del complemento (mw.addonManager). Es comun a
    todos los perfiles del equipo, que es justo lo que se espera de un ajuste
    visual.

  * Mazos excluidos, fechas clave y pausa de la racha -> configuracion de la coleccion
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
# FIX-014 (2026-10-13) — Tras sincronizar, Opciones podia borrar fechas clave
#                        y mazos excluidos puestos en otro ordenador.

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from typing import TypeGuard

from anki.collection import Collection
from aqt import mw

from .data import WINDOWS
from .errors import log_exception
from .palettes import RETIRED_THEMES, THEME_NAMES

MAX_KEY_DATES = 50
MAX_LABEL_LEN = 60
KEY_DATE_MIN = date(2000, 1, 1)
KEY_DATE_MAX = date(2100, 12, 31)

# Tamano de celda y redondeo de esquinas, en pixeles (vuelven en la 4.2.0,
# peticion del cliente del 2026-10-21, en lugar de «Tamano» y «Forma»). Un
# tamano FIT_WIDTH es «Ajustado al ancho» (de serie en la 4.4 y la 4.5); desde
# la 4.6.0 el de serie es 24 px (peticion del cliente).
FIT_WIDTH = 0
# Desde la 4.7.0 el tamano empieza en 10 px, como el minimo del ajustado al
# ancho (por debajo no se distinguen los cuadritos).
CELL_SIZE_MIN, CELL_SIZE_MAX = 10, 60
# El redondeo va en pixeles reales del cuadrito (4.6.0); por encima de la
# mitad del cuadrito ya es un circulo.
BORDER_RADIUS_MIN, BORDER_RADIUS_MAX = 0, 15
# Orden de los botones de la meta (4.11.0, informe aprobado por el cliente):
# «Terminar lo de hoy» antes que «Un numero», porque sigue el calendario de
# repasos de Anki y lo que va antes se considera antes.
GOAL_MODES: tuple[str, ...] = ("none", "due", "number")
GOAL_MIN, GOAL_MAX = 1, 9999
MAX_PAUSE_DAYS = 30

# Clave unica dentro de la configuracion de la coleccion. Guarda un diccionario
# pequeno (mazos excluidos y fechas clave); la configuracion de la coleccion se
# envia entera en cada sincronizacion, por eso no debe crecer.
COL_KEY = "gritmap"
# Dias con meta que se guardan en la coleccion (4.11.0): los 14 del historial
# de Opciones y la semana en curso, con margen. Lo mas antiguo se borra.
GOAL_DAYS_KEEP = 21

APPEARANCE_KEYS = (
    "theme",
    "measure",
    "map_size",
    "map_radius",
    "avg_window",
    "goal_mode",
    "goal",
    "freezes",
    "show_streak",
    "study_plan",
)
# Claves de versiones anteriores que se dejan de guardar (3.x, y el tamano y
# el redondeo de la 4.2 y la 4.3, que se guardaban en pixeles fijos: la 4.4.0
# los lee con otro nombre para que todos vuelvan al mapa de la 4.1.0; y los de
# la 4.4 y la 4.5, para que todos pasen a los 24 px de serie de la 4.6.0).
_OLD_APPEARANCE_KEYS = (
    "size", "shape", "show_week_diff", "stats_open", "cell_size", "border_radius", "map_cell", "map_corners",
)
COLLECTION_KEYS = ("excluded_decks", "key_dates", "pause")


@dataclass(frozen=True)
class KeyDate:
    day: date
    label: str


@dataclass(frozen=True)
class Config:
    theme: str
    # Que mide el color. Desde la 4.10.0, siempre "cards" (tarjetas distintas
    # respondidas cada dia); data.MEASURES conserva las otras para los calculos.
    measure: str
    # Lado de cada cuadrito en pixeles (FIT_WIDTH: ajustado al ancho; el
    # dibujo se escala entero, 4.5.0) y redondeo de sus esquinas en pixeles
    # (con el ajustado al ancho, los de un cuadrito de 14).
    cell_size: int
    border_radius: int
    # Dias de la ventana del promedio; 0 = todo el historial (data.WINDOWS).
    avg_window: int
    # Meta diaria: "none", "number" (goal en la unidad de la medida) o "due"
    # (terminar lo que vence hoy).
    goal_mode: str
    goal: int
    # Comodines: perdonar dias sueltos sin estudiar.
    freezes: bool
    # Mostrar la tarjeta de la racha y la meta.
    show_streak: bool
    excluded_decks: tuple[int, ...]
    key_dates: tuple[KeyDate, ...]
    # Pausa de la racha: (primer dia, ultimo dia), o None.
    pause: tuple[date, date] | None = None
    # Tema retirado que tenia guardado (4.0.0), para avisar en Opciones; no
    # se guarda.
    retired_theme: str = ""
    # Plan «Suelo estudiar…» (4.11.0): cuando suele estudiar, en sus palabras;
    # vacio si no lo ha escrito.
    study_plan: str = ""


DEFAULT_CONFIG = Config(
    theme="classic_green",
    measure="cards",
    cell_size=24,
    border_radius=3,
    avg_window=30,
    goal_mode="none",
    goal=50,
    freezes=True,
    show_streak=True,
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
    # Desde la 4.10.0 solo hay una medida, «Tarjetas» (peticion del cliente,
    # 2026-10-26): lo guardado por versiones anteriores pasa a ella.
    return DEFAULT_CONFIG.measure


def _as_window(value: object) -> int:
    if not _is_number(value) or int(value) != value or int(value) not in WINDOWS:
        return DEFAULT_CONFIG.avg_window
    return int(value)


def _as_bool(value: object, fallback: bool) -> bool:
    return value if isinstance(value, bool) else fallback


def _as_theme(value: object) -> str:
    if isinstance(value, str) and value in RETIRED_THEMES:
        return RETIRED_THEMES[value]
    return value if isinstance(value, str) and value in THEME_NAMES else DEFAULT_CONFIG.theme


def _as_choice(value: object, choices: tuple[str, ...], fallback: str) -> str:
    return value if isinstance(value, str) and value in choices else fallback


def _as_cell(value: object) -> int:
    """Tamano de celda: FIT_WIDTH (ajustado al ancho) o de 8 a 60 px."""
    if _is_number(value) and int(value) == FIT_WIDTH:
        return FIT_WIDTH
    return _as_int(value, DEFAULT_CONFIG.cell_size, CELL_SIZE_MIN, CELL_SIZE_MAX)


def _as_radius(stored: dict[str, object]) -> int:
    """Redondeo; quien eligio «Redondeado» en la 4.0 o la 4.1 conserva esquinas
    redondeadas (8 px) hasta que guarde las opciones.

    Anki mezcla los valores por defecto de config.json con los guardados
    (APR-065), asi que «map_radius» siempre esta; «shape», que ya no viene
    por defecto, solo existe si la guardo una de esas versiones.
    """
    radius = _as_int(
        stored.get("map_radius"), DEFAULT_CONFIG.border_radius, BORDER_RADIUS_MIN, BORDER_RADIUS_MAX
    )
    if stored.get("shape") == "rounded" and radius == DEFAULT_CONFIG.border_radius:
        return 8
    return radius


def _as_pause(value: object) -> tuple[date, date] | None:
    """Pausa valida (de 1 a 30 dias, con el fin despues del principio) o None."""
    if not isinstance(value, dict):
        return None
    try:
        start = date.fromisoformat(str(value.get("start")))
        end = date.fromisoformat(str(value.get("end")))
    except ValueError:
        return None
    if not (KEY_DATE_MIN <= start <= end <= KEY_DATE_MAX):
        return None
    if (end - start).days + 1 > MAX_PAUSE_DAYS:
        return None
    return start, end


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


def _collection_config(col: Collection | None = None) -> dict[str, object] | None:
    """Ajustes propios de la coleccion (la abierta si no se indica otra), o None."""
    if col is None:
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
# muchas veces por sesion. Se guarda la apariencia y se invalida al guardar
# opciones y al abrir o cerrar un perfil.
# --- FIX-014 (2026-10-13) --------------------------------------
# Sintoma: tras sincronizar, el mapa no mostraba una fecha clave anadida en
#          otro ordenador y, al pulsar Aceptar en Opciones, se borraba aqui y
#          despues tambien en el otro ordenador.
# Causa: la cache guardaba tambien los mazos excluidos y las fechas clave, que
#        viven en la coleccion y cambian al sincronizar, sin que nada la
#        vaciara.
# Regla: en cache solo va lo que no cambia por debajo (la apariencia, que
#        esta en este ordenador); lo de la coleccion se lee de ella cada vez.
# ---------------------------------------------------------------
_addon_cache: dict[str, object] | None = None


def invalidate_cache() -> None:
    global _addon_cache
    _addon_cache = None


def load_config(col: Collection | None = None) -> Config:
    """Configuracion validada. Con col, lee la coleccion indicada (por ejemplo,
    la que recibe una operacion en segundo plano)."""
    global _addon_cache
    if _addon_cache is None:
        _addon_cache = _addon_config()
    collection = _collection_config(col)
    # Sin coleccion abierta no hay mazos ni fechas que aplicar: mejor vacio
    # que arrastrar los del perfil anterior.
    scoped: dict[str, object] = collection if collection is not None else {}
    return build_config(_addon_cache, scoped)


def build_config(stored: dict[str, object], scoped: dict[str, object]) -> Config:
    """Configuracion validada a partir de los dos almacenes ya leidos."""
    raw_theme = stored.get("theme")
    return Config(
        theme=_as_theme(raw_theme),
        measure=_as_measure(stored.get("measure")),
        cell_size=_as_cell(stored.get("map_size")),
        border_radius=_as_radius(stored),
        avg_window=_as_window(stored.get("avg_window")),
        goal_mode=_as_choice(stored.get("goal_mode"), GOAL_MODES, DEFAULT_CONFIG.goal_mode),
        goal=_as_int(stored.get("goal"), DEFAULT_CONFIG.goal, GOAL_MIN, GOAL_MAX),
        freezes=_as_bool(stored.get("freezes"), DEFAULT_CONFIG.freezes),
        show_streak=_as_bool(stored.get("show_streak"), DEFAULT_CONFIG.show_streak),
        excluded_decks=_as_deck_ids(scoped.get("excluded_decks")),
        key_dates=_as_key_dates(scoped.get("key_dates")),
        pause=_as_pause(scoped.get("pause")),
        retired_theme=raw_theme if isinstance(raw_theme, str) and raw_theme in RETIRED_THEMES else "",
        study_plan=clean_label(stored.get("study_plan")),
    )


def save_appearance(cfg: Config) -> None:
    """Guarda la apariencia en la configuracion del complemento y vacia la cache."""
    appearance: dict[str, object] = dict(_addon_config())
    appearance.update(
        {
            "theme": cfg.theme,
            "measure": cfg.measure,
            "map_size": cfg.cell_size,
            "map_radius": cfg.border_radius,
            "avg_window": cfg.avg_window,
            "goal_mode": cfg.goal_mode,
            "goal": cfg.goal,
            "freezes": cfg.freezes,
            "show_streak": cfg.show_streak,
            "study_plan": cfg.study_plan,
        }
    )
    for key in _OLD_APPEARANCE_KEYS:
        appearance.pop(key, None)
    # Las claves de versiones antiguas (mazos y fechas guardados fuera de la
    # coleccion) se quitan cuando ya no guardan nada que copiar a un perfil:
    # asi no se arrastran para siempre, y lo que si guardan sigue a salvo
    # para los perfiles que aun no se hayan abierto.
    if not _as_deck_ids(appearance.get("excluded_decks")):
        appearance.pop("excluded_decks", None)
    if not _as_key_dates(appearance.get("key_dates")):
        appearance.pop("key_dates", None)
    try:
        mw.addonManager.writeConfig(__name__, appearance)
    except Exception as exc:
        log_exception("config.save_appearance", exc)
    invalidate_cache()


def save_scoped(col: Collection, cfg: Config) -> None:
    """Guarda en la coleccion los mazos excluidos y las fechas clave.

    Se llama desde una operacion en segundo plano, que recibe la coleccion.
    """
    # set_config directo, sin CollectionOp, y sin entrada de deshacer: es un
    # ajuste de la interfaz, no contenido de estudio. Es lo mismo que hace
    # Anki con las busquedas guardadas, el orden de columnas del navegador o
    # los nombres de las banderas. Envolverlo en una operacion deshacible
    # ensuciaria el menu Editar -> Deshacer con un paso que la persona no
    # espera poder revertir.
    scoped: dict[str, object] = {
        "excluded_decks": list(cfg.excluded_decks),
        "key_dates": _key_dates_to_json(cfg.key_dates),
    }
    if cfg.pause is not None:
        scoped["pause"] = {"start": cfg.pause[0].isoformat(), "end": cfg.pause[1].isoformat()}
    # Los dias con meta (4.11.0) no se tocan desde Opciones: se conservan.
    previous = _collection_config(col) or {}
    if "goal_days" in previous:
        scoped["goal_days"] = previous["goal_days"]
    col.set_config(COL_KEY, scoped)


def goal_days_from(scoped: dict[str, object] | None) -> dict[str, tuple[str, bool]]:
    """Dias con meta guardados: fecha ISO -> (tipo de meta, cumplida).

    Lo que no sirva (escrito a mano, de otra version) se descarta.
    """
    raw = scoped.get("goal_days") if scoped else None
    out: dict[str, tuple[str, bool]] = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        if (
            isinstance(key, str)
            and _as_day_iso(key)
            and isinstance(value, list)
            and len(value) == 2
            and value[0] in GOAL_MODES[1:]
            and isinstance(value[1], (bool, int))
        ):
            out[key] = (str(value[0]), bool(value[1]))
    return out


def read_goal_days(col: Collection) -> dict[str, tuple[str, bool]]:
    """Dias con meta de la coleccion indicada (desde una operacion)."""
    return goal_days_from(_collection_config(col))


def record_goal_day(col: Collection, day: date, mode: str, met: bool) -> None:
    """Apunta en la coleccion el dia de hoy con su meta y si se cumplio.

    Mismo criterio que save_scoped: set_config directo y sin entrada de
    deshacer, porque es un dato de la interfaz, no estudio. Solo se guardan
    los ultimos GOAL_DAYS_KEEP dias, para que no crezca.
    """
    stored = _collection_config(col)
    scoped: dict[str, object] = dict(stored) if stored else {}
    days = goal_days_from(scoped)
    days[day.isoformat()] = (mode, met)
    keep = sorted(days)[-GOAL_DAYS_KEEP:]
    scoped["goal_days"] = {key: [days[key][0], days[key][1]] for key in keep}
    col.set_config(COL_KEY, scoped)


def _as_day_iso(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


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
