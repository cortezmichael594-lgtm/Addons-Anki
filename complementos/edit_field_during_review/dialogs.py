"""Ventana de opciones del complemento.

Se abre desde Herramientas → Complementos → (seleccionar) → Configuración,
gracias a setConfigAction, de modo que el usuario nunca ve el editor JSON.

Versión 1.1.0 (petición del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012): un recuadro con la casilla. Aceptar, Cancelar y
Restaurar llevan el texto de Qt, que Anki ya traduce a cada idioma. El único
texto propio es la casilla, que vive en strings.py. El título de la ventana es
el nombre del complemento (los nombres de complemento no se traducen).
"""

from __future__ import annotations

from typing import Any

from aqt import mw
from aqt.utils import showWarning

from . import config, constants
from .panel import PanelDialog, parent_window
from .strings import tr


def page(require_modifier: bool) -> dict[str, Any]:
    """Descripción del panel: un recuadro con la casilla."""
    default = bool(config.DEFAULTS[config.KEY_REQUIRE_MODIFIER])
    return {
        "title": constants.ADDON_NAME,
        "values": {config.KEY_REQUIRE_MODIFIER: require_modifier},
        "defaults": {config.KEY_REQUIRE_MODIFIER: default},
        "cards": [
            {
                "restore": True,
                "items": [
                    {
                        "type": "check",
                        "key": config.KEY_REQUIRE_MODIFIER,
                        "label": tr("opt_require_modifier"),
                    }
                ],
            }
        ],
        "focus": config.KEY_REQUIRE_MODIFIER,
    }


def chosen_require_modifier(values: Any) -> bool:
    """Lo elegido en la página; si no sirve, el valor de serie."""
    raw = values.get(config.KEY_REQUIRE_MODIFIER) if isinstance(values, dict) else None
    if isinstance(raw, bool):
        return raw
    return bool(config.DEFAULTS[config.KEY_REQUIRE_MODIFIER])


def _handle(action: str, arg: Any) -> Any:
    if action == "accept":
        config.set_require_modifier(chosen_require_modifier(arg))
    return None


def _log(where: str, exc: BaseException) -> None:
    try:
        mw.addonManager.get_logger(__name__).error("%s: %r", where, exc)
    except Exception:
        pass


# Se conserva una referencia mientras la ventana existe: sin ella Python podría
# destruirla y la ventana desaparecería sola.
_dialog: PanelDialog | None = None


def open_options() -> None:
    """Callback de setConfigAction: no recibe argumentos ni necesita devolver nada."""
    global _dialog
    try:
        if _dialog is not None and _dialog.isVisible():
            _dialog.raise_()
            _dialog.activateWindow()
            return
        package = mw.addonManager.addon_from_module(__name__)
        dialog = PanelDialog(
            parent_window(), package, page(config.require_modifier()), _handle, _log, "editFieldPanel"
        )
        _dialog = dialog
        dialog.open()
    except Exception as exc:
        showWarning(str(exc), parent=mw, title=constants.ADDON_NAME)
