"""Ventana de opciones del complemento.

Se abre desde Herramientas → Complementos → Configuración, en lugar del editor
de texto JSON de Anki.

Versión 2.1.0 (petición del cliente, 2026-11-09): la ventana sigue el panel
modelo de GritMap (docs/fichas-diseno/09-patron-configuracion.md, regla del
taller desde PROP-012). Las mismas dos opciones: la casilla y, colgando de
ella, el campo que graba el atajo. Si la combinación no sirve, el aviso sale
encima del campo y la ventana sigue abierta. Aceptar, Cancelar y Restaurar
llevan el texto de Qt, que ya viene traducido a todos los idiomas de Anki.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-28) — Un atajo podía chocar con otro que Anki ya usaba.
# FIX-003 (2026-07-28) — Se retiró el atajo para cerrar Anki, que duplicaba Ctrl+Q.

from __future__ import annotations

from typing import Any

from aqt import mw
from aqt.qt import QKeySequence

from . import constants, shortcuts
from .errors import log, report_errors
from .panel import PanelDialog, parent_window
from .settings import AddonSettings, load_settings, save_settings
from .strings import tr


def _anki_text(attribute: str, fallback: str) -> str:
    try:
        from aqt.utils import tr as anki_tr

        value = getattr(anki_tr, attribute)()
        return value if isinstance(value, str) and value else fallback
    except Exception:
        return fallback


def _values(settings: AddonSettings) -> dict[str, Any]:
    return {
        "restart_enabled": settings.restart_enabled,
        "restart_shortcut": settings.restart_shortcut,
    }


# --- FIX-003 (2026-07-28) --------------------------------------
# Síntoma: el complemento ofrecía un segundo atajo para cerrar Anki que no
#          aportaba nada.
# Causa: se añadió sin comprobar antes que Anki ya trae Ctrl+Q para salir.
# Regla: el panel solo tiene el atajo de reinicio; no volver a añadir uno para
#        cerrar Anki.
# ---------------------------------------------------------------
def page(settings: AddonSettings) -> dict[str, Any]:
    """Descripción del panel: un recuadro con la casilla y su atajo."""
    defaults = AddonSettings()
    return {
        "title": constants.ADDON_NAME,
        "values": _values(settings),
        "defaults": _values(defaults),
        "cards": [
            {
                "restore": True,
                "items": [
                    {
                        "type": "check",
                        "key": "restart_enabled",
                        "label": tr("restart_checkbox"),
                        "children": [
                            {
                                "type": "shortcut",
                                "key": "restart_shortcut",
                                "label": tr("shortcut_label").rstrip().rstrip(":：").rstrip(),
                                "clear": _anki_text("actions_delete", "Delete"),
                            }
                        ],
                    }
                ],
            }
        ],
        "focus": "restart_enabled",
    }


def settings_from_page(values: Any, saved: AddonSettings) -> AddonSettings:
    """Lo elegido en la página. Si el campo del atajo queda vacío, se conserva
    el atajo ya guardado (así lo hacía la ventana anterior)."""
    raw = values if isinstance(values, dict) else {}
    enabled = raw.get("restart_enabled", saved.restart_enabled)
    shortcut = raw.get("restart_shortcut", "")
    return AddonSettings(
        restart_enabled=enabled if isinstance(enabled, bool) else saved.restart_enabled,
        restart_shortcut=shortcut if isinstance(shortcut, str) and shortcut else saved.restart_shortcut,
    )


def _accept(values: Any) -> dict[str, str] | None:
    from .logic import registered_shortcuts, reload_shortcuts

    settings = settings_from_page(values, load_settings())
    sequence = QKeySequence(settings.restart_shortcut)
    # La página escribe la combinación a su manera («Ctrl+Shift+R»); se guarda
    # en la forma estable de Qt, la misma en cualquier sistema.
    settings.restart_shortcut = shortcuts.portable_text(sequence) or settings.restart_shortcut
    # --- FIX-001 (2026-07-28) --------------------------------------
    # Síntoma: se podía guardar un atajo que Anki ya estaba usando, y
    #          entonces no respondía ni el de Anki ni el del complemento.
    # Causa: la comprobación se hacía contra una lista escrita a mano, que
    #        se quedaba corta y anticuada.
    # Regla: preguntar siempre a la ventana principal qué combinaciones
    #        tiene cogidas en ese momento, incluidas las que el sistema
    #        reserva para cerrar ventana, y excluir del cotejo los atajos
    #        del propio complemento.
    # ---------------------------------------------------------------
    if settings.restart_enabled and not shortcuts.is_allowed(sequence, registered_shortcuts()):
        label = shortcuts.display_text(sequence) or settings.restart_shortcut or "—"
        return {"error": tr("shortcut_not_allowed", shortcut=label), "field": "restart_shortcut"}
    save_settings(settings)
    reload_shortcuts()
    return None


def _handle(action: str, arg: Any) -> Any:
    if action == "accept":
        return _accept(arg)
    return None


def _log(where: str, exc: BaseException) -> None:
    try:
        log().error("error en %s", where, exc_info=exc)
    except Exception:
        pass


# Se conserva una referencia mientras la ventana existe: sin ella Python podría
# destruirla y la ventana desaparecería sola.
_dialog: PanelDialog | None = None


@report_errors
def open_config_dialog() -> None:
    global _dialog
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    package = mw.addonManager.addon_from_module(__name__)
    dialog = PanelDialog(parent_window(), package, page(load_settings()), _handle, _log, "restartPanel")
    _dialog = dialog
    dialog.open()
