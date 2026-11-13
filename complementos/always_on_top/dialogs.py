"""Panel de opciones del complemento.

Version 1.3 (peticion del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012): un recuadro con el campo que graba el atajo. Aceptar,
Cancelar y Restaurar llevan el texto de Qt, ya traducido por Anki.

Regla: aqui no se guarda un atajo que Anki ya use, ni uno sin Ctrl ni Alt. Si
dos atajos se pelean por la misma tecla el resultado es impredecible, asi que
el aviso sale encima del campo y el panel no se cierra hasta que elija otro.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aqt import mw
from aqt.qt import QKeySequence

from . import config, constants, shortcuts
from .errors import guarded, logger
from .panel import PanelDialog, parent_window
from .strings import tr

if TYPE_CHECKING:
    from .logic import AlwaysOnTopManager

_KEY = "shortcut"


def _anki_text(attribute: str, fallback: str) -> str:
    try:
        from aqt.utils import tr as anki_tr

        value = getattr(anki_tr, attribute)()
        return value if isinstance(value, str) and value else fallback
    except Exception:
        return fallback


def page(saved: str) -> dict[str, Any]:
    """Descripcion del panel: un recuadro con el campo del atajo."""
    return {
        "title": constants.ADDON_DISPLAY_NAME,
        "values": {_KEY: saved},
        "defaults": {_KEY: constants.DEFAULT_SHORTCUT},
        "cards": [
            {
                "restore": True,
                "items": [
                    {
                        "type": "shortcut",
                        "key": _KEY,
                        "label": tr("shortcut_prefix").rstrip().rstrip(":：").rstrip(),
                        "placeholder": tr("placeholder"),
                        "clear": _anki_text("actions_delete", "Delete"),
                    }
                ],
            }
        ],
        "focus": _KEY,
    }


def chosen_shortcut(values: Any) -> str:
    """El atajo elegido, en la forma estable de Qt. Vacio: el de serie (no hay
    manera de dejar el complemento sin atajo)."""
    raw = values.get(_KEY) if isinstance(values, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return constants.DEFAULT_SHORTCUT
    return shortcuts.normalize(raw.strip()) or constants.DEFAULT_SHORTCUT


class _Panel:
    """Lo que el panel necesita del gestor del complemento."""

    def __init__(self, manager: AlwaysOnTopManager) -> None:
        self._manager = manager

    def handle(self, action: str, arg: Any) -> Any:
        if action != "accept":
            return None
        chosen = chosen_shortcut(arg)
        if not shortcuts.is_usable(chosen):
            # El nombre se muestra tal como lo ve la persona en su teclado.
            text = QKeySequence(chosen).toString(QKeySequence.SequenceFormat.NativeText)
            return {"error": tr("conflict", shortcut=text or chosen), "field": _KEY}
        if chosen != config.load().shortcut:
            config.save(config.Settings(shortcut=chosen))
            self._manager.apply_shortcut(chosen, notify=False)
        return None


def _log(where: str, exc: BaseException) -> None:
    try:
        logger().error("fallo en %s", where, exc_info=exc)
    except Exception:
        pass


# Se conserva una referencia mientras la ventana existe: sin ella Python podria
# destruirla y la ventana desapareceria sola.
_dialog: PanelDialog | None = None


@guarded
def open_config_dialog(manager: AlwaysOnTopManager) -> None:
    global _dialog
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    package = mw.addonManager.addon_from_module(__name__)
    panel = _Panel(manager)
    dialog = PanelDialog(
        parent_window(), package, page(config.load().shortcut), panel.handle, _log, "alwaysOnTopPanel"
    )
    _dialog = dialog
    dialog.open()
