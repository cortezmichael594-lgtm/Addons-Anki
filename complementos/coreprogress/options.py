"""El panel de opciones.

Version 1.5.0 (informe «Rediseño de color y forma» del 2026-11-17, aplicado
entero, 8.9): las muestras de tema son minibarras con el degradado del modo
activo; el grosor pasa a tres tamaños (Fina, Normal, Gruesa) en un control
segmentado, como los de GritMap; la vista previa enseña la barra nueva (cortes,
próximo hito con número y total en gris).

Version 1.3.0 (informe del cliente del 2026-11-16, aplicado entero, 8.8): dos
recuadros en lugar de tres, con lo que se viene a cambiar primero. El primero,
el aspecto de la barra: vista previa, tema (con «Restaurar…» en su fila),
altura y espacio en paralelo con su margen a la vista, hitos y celebraciones.
El segundo, el récord entero: la mejor racha de 30 días y el récord, «Poner a
cero» (oculto si no hay récord) y los mazos que no cuentan. Sin la cabecera
«CoreProgress», que ya está en la barra de título (decisión 4). Cabe entera,
sin desplazar, en unos 656 px.

Version 1.1.0 (peticion del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012). Las mismas opciones, en tres recuadros: el record con
«Restablecer»; el aspecto de la barra (tema en fichas con su muestra, altura y
espacio con «−» y «+», y las dos casillas), con «Restaurar»; y la fila de los
mazos excluidos, que abre su lista con buscador dentro de la misma ventana.

Lo ESTRUCTURAL del panel (Aceptar, Cancelar, Restaurar, Si, No) no se traduce
aqui: son los textos de los botones estandar de Qt, que Anki localiza al fijar
el idioma de la aplicacion. Asi esos textos son siempre correctos y no hay nada
inventado.

El TITULO de la ventana es solo el nombre del complemento, tal como lo declara
manifest.json. Es un nombre propio: no se traduce y no lleva ninguna formula
alrededor (ver _addon_title).

La tabla propia de i18n.py se reserva para lo exclusivo del complemento (los
nombres de los temas de color, el record, los mazos excluidos).
"""

# Historial de correcciones de este archivo:
# FIX-003 (2026-11-09) — «Restablecer» borraba el récord sin vuelta atrás con un Intro de más.

from __future__ import annotations

import re
from typing import Any

from aqt import mw
from aqt.qt import QDialogButtonBox
from aqt.theme import theme_manager

from .errors import report
from .effects import round_marks
from .i18n import record_value_label, t
from .palettes import DEFAULT_THEME, RETIRED_THEMES, THEME_KEYS, neutral, preview_style, swatch
from .panel import PanelDialog, button_text, parent_window
from .settings import (
    BAR_HEIGHTS,
    BAR_WIDTHS,
    DEFAULT_CONFIG,
    PUSH_MAX,
    PUSH_MIN,
    Config,
    load_config,
    reset_best_streak,
    save_config,
)

_RESET_KEY = "reset_record"
_EXCLUDE_KEY = "excluded_decks"
_VISUAL_KEYS: tuple[str, ...] = (
    "theme",
    "bar_height",
    "bar_width",
    "push_down",
    "effects_enabled",
    "checkpoints_enabled",
)


def _log(exc: BaseException) -> None:
    report(exc, "options")


def _addon_title() -> str:
    """El nombre del complemento, y nada mas.

    HISTORIAL: llego a componerse como "Configurar 'CoreProgress'" con la
    formula traducida de Anki. El cliente quiere en el titulo solo el nombre.
    Regla: el titulo de la ventana de opciones es el nombre del complemento tal
    como lo declara manifest.json, sin formula alrededor y sin traducir.
    """
    name = "CoreProgress"
    try:
        if mw is not None:
            package = mw.addonManager.addon_from_module(__name__)
            name = mw.addonManager.addon_meta(package).human_name() or name
    except Exception as exc:
        _log(exc)
    return name


def _without_px(text: str) -> str:
    """«Altura de la barra (px)» → «Altura de la barra»: la unidad va al lado
    del campo, como en GritMap."""
    return re.sub(r"\s*\(px\)\s*$", "", text)


def _record_parts(record: int, window: int = 0) -> dict[str, str]:
    """«Récord: 7 aciertos seguidos», con la cifra en negrita, o «Sin récord
    todavía».

    1.2.0 (informe del 2026-11-09, aprobado por el cliente sabiendo que antes
    pidió «Tu récord actual: 7 seguidas!» y el guion): forma impersonal, el
    plural de cada idioma y sin el «!» suelto.

    1.3.0 (informe del 2026-11-16, decisión 1): con una mejor racha de 30 días
    por debajo del récord, «Mejor racha en 30 días: 41 · récord: 90».
    """
    if record <= 0:
        return {"before": t("record_none")}
    if 0 < window < record:
        before, _sep, after = t("best30").partition("{count}")
        return {
            "before": before,
            "strong": str(window),
            "after": after + " · " + t("record_inline").format(count=record),
        }
    return {"before": f"{t('opt_record')}: ", "strong": record_value_label(record)}


def sorted_themes() -> list[str]:
    """Los temas por orden alfabético de su nombre en el idioma de Anki, como en
    GritMap (1.2.0)."""
    return sorted(THEME_KEYS, key=lambda key: t(f"theme_{key}").casefold())


def _visual_values(cfg: Config) -> dict[str, Any]:
    return {
        "theme": cfg.theme,
        "bar_height": cfg.bar_height,
        "bar_width": cfg.bar_width,
        "push_down": cfg.push_down,
        "effects_enabled": cfg.effects_enabled,
        "checkpoints_enabled": cfg.checkpoints_enabled,
    }


_PREVIEW_TOTAL = 50
_PREVIEW_PROGRESS = 60


def page(cfg: Config, record: int, title: str = "CoreProgress", window: int = 0) -> dict[str, Any]:
    """Descripcion del panel: el aspecto de la barra y el record con sus mazos."""
    dark = bool(theme_manager.night_mode)
    values = {**_visual_values(cfg), _EXCLUDE_KEY: list(cfg.excluded_decks), _RESET_KEY: False}
    defaults = {**_visual_values(DEFAULT_CONFIG), _EXCLUDE_KEY: [], _RESET_KEY: False}
    # --- FIX-003 (2026-11-09) ---
    # Síntoma: al pulsar «Restablecer», la pregunta traía «Sí» marcado de
    #          antemano y el récord se borraba en el acto, aunque después se
    #          pulsara Cancelar.
    # Causa: se usaba la pregunta de Anki sin «No» por defecto y el borrado se
    #        aplicaba antes de guardar.
    # Regla: lo que borra sin vuelta atrás pregunta con el foco en «No» y solo
    #        se aplica al pulsar Aceptar; Cancelar lo deja como estaba.
    record_card: dict[str, Any] = {
        "items": [
            {
                "type": "stat",
                "key": _RESET_KEY,
                "parts": _record_parts(record, window),
                "done": _record_parts(0),
                "action": {
                    "label": t("opt_record_reset"),
                    "disabled": record <= 0,
                    "confirm": {
                        "title": t("opt_record_reset_confirm"),
                        # 1.2.0: botones con verbo, no «Sí» y «No».
                        "yes": t("opt_record_reset"),
                        "no": button_text(QDialogButtonBox.StandardButton.Cancel) or "Cancel",
                    },
                },
            }
        ]
    }
    look_card: dict[str, Any] = {
        "restore": True,
        # «Restaurar…» en la fila de «Tema de color» (1.3.0).
        "restoreInline": "theme",
        "items": [
            {
                "type": "preview",
                "theme": "theme",
                "height": "bar_height",
                "checks": "checkpoints_enabled",
                "themes": {key: preview_style(key, dark) for key in THEME_KEYS},
                "neutral": neutral(dark),
                "total": _PREVIEW_TOTAL,
                "progress": _PREVIEW_PROGRESS,
                "marks": [*round_marks(_PREVIEW_TOTAL), _PREVIEW_TOTAL],
            },
            {
                "type": "chips",
                "key": "theme",
                "label": t("opt_theme"),
                "options": [
                    {
                        "value": key,
                        "label": t(f"theme_{key}"),
                        "swatch": swatch(key, dark),
                    }
                    for key in sorted_themes()
                ],
            },
            {
                "type": "pair",
                "children": [
                    {
                        "type": "segmented",
                        "key": "bar_height",
                        "label": t("opt_thickness"),
                        "options": [
                            {"value": size, "label": t(name)}
                            for size, name in zip(
                                BAR_HEIGHTS, ("thickness_thin", "thickness_normal", "thickness_thick")
                            )
                        ],
                    },
                    # 1.6.0 (petición de la persona): «Tarjeta», 720 px centrada, o «Ventana»,
                    # de lado a lado como hasta la 1.4.0.
                    {
                        "type": "segmented",
                        "key": "bar_width",
                        "label": t("opt_width"),
                        "options": [
                            {"value": value, "label": t(f"width_{value}")} for value in BAR_WIDTHS
                        ],
                    },
                ],
            },
            {
                "type": "stepper",
                "key": "push_down",
                "label": _without_px(t("opt_push")),
                "min": PUSH_MIN,
                "max": PUSH_MAX,
                "step": 4,
                "unit": f"px · {PUSH_MIN}–{PUSH_MAX}",
            },
            {"type": "check", "key": "checkpoints_enabled", "label": t("opt_checkpoints")},
            {"type": "check", "key": "effects_enabled", "label": t("opt_effects")},
        ],
    }
    # HISTORIAL: la lista de excluir mazos tuvo una frase explicativa que el
    # cliente retiro. En la 1.2.0 (informe del 2026-11-09) aprobo una linea
    # breve que dice para que sirve, sabiendo que antes la habia retirado.
    decks_row = {
        "type": "row",
        "key": _EXCLUDE_KEY,
        "label": t("opt_exclude"),
        "note": t("opt_exclude_note"),
        "empty": t("no_match"),
    }
    # 1.3.0: el récord entero en un recuadro, al final: el dato, su puesta a
    # cero y los mazos que no cuentan para él.
    record_card["items"].append(decks_row)
    if cfg.retired_theme in RETIRED_THEMES:
        old = t(f"theme_{cfg.retired_theme}")
        new = t(f"theme_{RETIRED_THEMES[cfg.retired_theme]}")
        look_card["items"].insert(0, {"type": "notice", "text": t("theme_retired").format(old=old, new=new)})
    return {
        "title": title,
        # El título ya está en la barra de la ventana (decisión 4).
        "hideTitle": True,
        "values": values,
        "defaults": defaults,
        "cards": [look_card, record_card],
        "focus": "theme",
    }


def _int(value: object, fallback: int, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return fallback
    return max(low, min(high, value))


def _height(value: object) -> int:
    """Solo uno de los tres grosores; cualquier otra cosa, el de serie."""
    if isinstance(value, int) and not isinstance(value, bool) and value in BAR_HEIGHTS:
        return value
    return DEFAULT_CONFIG.bar_height


def config_from_page(values: Any, existing: set[int] | None = None) -> Config:
    """Lo elegido en la pagina, con cada valor comprobado. Los mazos que ya no
    existen dejan de guardarse."""
    raw = values if isinstance(values, dict) else {}
    theme = raw.get("theme")
    decks: list[int] = []
    for value in raw.get(_EXCLUDE_KEY) or []:
        if isinstance(value, int) and not isinstance(value, bool) and value not in decks:
            if existing is None or value in existing:
                decks.append(value)
    effects = raw.get("effects_enabled")
    checkpoints = raw.get("checkpoints_enabled")
    return Config(
        theme=theme if isinstance(theme, str) and theme in THEME_KEYS else DEFAULT_THEME,
        effects_enabled=effects if isinstance(effects, bool) else DEFAULT_CONFIG.effects_enabled,
        checkpoints_enabled=checkpoints if isinstance(checkpoints, bool) else DEFAULT_CONFIG.checkpoints_enabled,
        bar_height=_height(raw.get("bar_height")),
        bar_width=raw["bar_width"] if raw.get("bar_width") in BAR_WIDTHS else DEFAULT_CONFIG.bar_width,
        push_down=_int(raw.get("push_down"), DEFAULT_CONFIG.push_down, PUSH_MIN, PUSH_MAX),
        excluded_decks=tuple(decks),
    )


def _deck_list() -> list[dict[str, Any]]:
    """Todos los mazos, con su nombre completo (los submazos, con «::»),
    incluidos los filtrados y el predeterminado."""
    if mw is None or mw.col is None:
        return []
    return [{"value": int(entry.id), "label": entry.name} for entry in mw.col.decks.all_names_and_ids()]


def _summary(values: Any) -> str:
    """Los mazos excluidos, por su nombre; «Ninguno» si no hay ninguno (1.3.0:
    antes un guion, que no dice nada y el lector de pantalla no lee)."""
    chosen = values.get(_EXCLUDE_KEY) if isinstance(values, dict) else None
    ids = {value for value in chosen or [] if isinstance(value, int)}
    names = [entry["label"] for entry in _deck_list() if entry["value"] in ids]
    return ", ".join(names) if names else t("none")


def _handle(action: str, arg: Any) -> Any:
    if action == "options":
        return _deck_list()
    if action == "summary":
        return _summary(arg.get("values") if isinstance(arg, dict) else None)
    if action != "accept":
        return None
    from .controller import notify_config_changed, notify_record_reset

    existing = {entry["value"] for entry in _deck_list()} if mw is not None and mw.col is not None else None
    if isinstance(arg, dict) and arg.get(_RESET_KEY) is True:
        reset_best_streak()
        notify_record_reset()
    save_config(config_from_page(arg, existing))
    notify_config_changed()
    return None


def _log_panel(where: str, exc: BaseException) -> None:
    _log(exc)


# Se conserva una referencia mientras la ventana existe: sin ella Python podria
# destruirla y la ventana desapareceria sola.
_dialog: PanelDialog | None = None


def open_options() -> None:
    global _dialog
    try:
        if _dialog is not None and _dialog.isVisible():
            _dialog.raise_()
            _dialog.activateWindow()
            return
        package = mw.addonManager.addon_from_module(__name__)
        from .controller import current_best, current_window_best

        content = page(load_config(), current_best(), _addon_title(), current_window_best())
        dialog = PanelDialog(parent_window(), package, content, _handle, _log_panel, "coreprogressPanel")
        _dialog = dialog
        dialog.open()
    except Exception as exc:
        _log(exc)


def setup_menu() -> None:
    try:
        if mw is not None:
            mw.addonManager.setConfigAction(__name__, open_options)
    except Exception as exc:
        _log(exc)
