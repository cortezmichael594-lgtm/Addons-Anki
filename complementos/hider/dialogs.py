"""Ventana de opciones del complemento.

Se registra con setConfigAction, de modo que el boton "Configuracion" de Anki
abre esto y no el editor de JSON.

Version 4.1.0 (peticion del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012). Las mismas opciones, en dos recuadros con casillas; los
globos de ayuda pasan a notas grises a la vista y los segundos del puntero
cuelgan de su casilla. Aceptar, Cancelar y Restaurar llevan el texto de Qt y el
titulo es el que Anki pone a la configuracion de cualquier complemento: asi
salen ya traducidos a todos los idiomas.
"""

from __future__ import annotations

from typing import Any

from aqt import mw
from aqt.utils import tooltip

from . import constants, strings
from .config import DEFAULT_CONFIG, HiderConfig, load_config, save_config
from .errors import get_logger, guarded
from .panel import PanelDialog, parent_window
from .strings import tr

_FIELDS: tuple[str, ...] = (
    "hide_menu_bar",
    "hide_toolbar",
    "hide_bottom_bar",
    "hide_scrollbar",
    "hide_hard_easy_buttons",
    "hide_cursor",
    "cursor_idle_seconds",
    "auto_start_study",
)


def _title(key: str) -> str:
    """Rotulo de grupo sin los dos puntos finales («Durante el repaso, ocultar»)."""
    return tr(key).rstrip().rstrip(":：").rstrip()


def _values(config: HiderConfig) -> dict[str, Any]:
    return {name: getattr(config, name) for name in _FIELDS}


def page(config: HiderConfig) -> dict[str, Any]:
    """Descripcion del panel: dos recuadros con las mismas opciones de siempre."""
    review = {
        "title": _title("group_review"),
        "note": tr("opt_menu_bar_tip"),
        "restore": True,
        "items": [
            {"type": "check", "key": "hide_menu_bar", "label": tr("opt_menu_bar")},
            {"type": "check", "key": "hide_toolbar", "label": tr("opt_toolbar")},
            {"type": "check", "key": "hide_bottom_bar", "label": tr("opt_bottom_bar")},
            {
                "type": "check",
                "key": "hide_scrollbar",
                "label": tr("opt_scrollbar"),
                "note": tr("opt_scrollbar_tip"),
            },
            {
                "type": "check",
                "key": "hide_hard_easy_buttons",
                "label": tr("opt_hard_easy"),
                "note": tr("opt_hard_easy_tip"),
            },
            {
                "type": "check",
                "key": "hide_cursor",
                "label": tr("opt_cursor").rstrip().rstrip(":：").rstrip(),
                "note": tr("opt_cursor_tip"),
                "children": [
                    {
                        "type": "stepper",
                        "key": "cursor_idle_seconds",
                        "min": constants.MIN_CURSOR_IDLE_SECONDS,
                        "max": constants.MAX_CURSOR_IDLE_SECONDS,
                        "unit": tr("opt_cursor_suffix").strip(),
                    }
                ],
            },
        ],
    }
    behaviour = {
        "title": _title("group_behaviour"),
        "restore": True,
        "items": [
            {
                "type": "check",
                "key": "auto_start_study",
                "label": tr("opt_auto_start"),
                "note": tr("opt_auto_start_tip"),
            }
        ],
    }
    return {
        "title": strings.options_title(),
        "values": _values(config),
        "defaults": _values(DEFAULT_CONFIG),
        "cards": [review, behaviour],
        "focus": "hide_menu_bar",
    }


def config_from_page(values: Any) -> HiderConfig:
    """Lo elegido en la pagina, con cada valor comprobado (lo que no sirva, de serie)."""
    raw = values if isinstance(values, dict) else {}
    data: dict[str, Any] = {}
    for name in _FIELDS:
        default = getattr(DEFAULT_CONFIG, name)
        value = raw.get(name, default)
        if name == "cursor_idle_seconds":
            ok = (
                isinstance(value, int)
                and not isinstance(value, bool)
                and constants.MIN_CURSOR_IDLE_SECONDS <= value <= constants.MAX_CURSOR_IDLE_SECONDS
            )
        else:
            ok = isinstance(value, bool)
        data[name] = value if ok else default
    return HiderConfig(**data)


def _log(where: str, exc: BaseException) -> None:
    try:
        get_logger().error("fallo en %s", where, exc_info=exc)
    except Exception:
        pass


def _handle(action: str, arg: Any) -> Any:
    if action != "accept":
        return None
    try:
        save_config(config_from_page(arg))
    except Exception as exc:
        _log("dialogs.save", exc)
        return {"error": tr("save_failed"), "field": "hide_menu_bar"}
    from . import logic  # con Anki en marcha (vease __init__.py)

    # writeConfig no dispara setConfigUpdatedAction, asi que se avisa al manager
    # para que el cambio se note al momento, incluso en pleno repaso.
    logic.reload_active_manager()
    tooltip(tr("saved"), period=2000)
    return None


# Se conserva una referencia mientras la ventana existe: sin ella Python podria
# destruirla y la ventana desapareceria sola.
_dialog: PanelDialog | None = None


@guarded
def open_options() -> None:
    """Accion del boton "Configuracion".

    Nunca debe devolver False ni dejar escapar un error: lo primero haria que
    Anki abriese ademas su editor de JSON, y lo segundo le plantaria a la persona
    un volcado tecnico en pantalla.
    """
    global _dialog
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    package = mw.addonManager.addon_from_module(__name__)
    dialog = PanelDialog(
        parent_window(), package, page(load_config()), _handle, _log, f"{constants.ADDON_NAME}Panel"
    )
    _dialog = dialog
    dialog.open()
