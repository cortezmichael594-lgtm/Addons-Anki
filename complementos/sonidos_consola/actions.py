"""Lo que ocurre al abrir la ventana de opciones y al pulsar sus botones."""

from __future__ import annotations

from typing import Any

from aqt import mw
from aqt.addons import AddonManager
from aqt.utils import openFolder, tooltip

from . import config, dialogs, player, strings
from .errors import guarded
from .panel import PanelDialog, parent_window

# La ventana abierta se guarda aquí: si no, el recolector de basura la cerraría.
_dialog: PanelDialog | None = None


def _handle(action: str, arg: Any) -> Any:
    if action == "action":
        if isinstance(arg, dict) and arg.get("name") == "folder":
            _open_folder()
            return None
        request = dialogs.test_request(arg)
        if request is not None:
            key, volume = request
            player.bank.play(key, ignore_switch=True, volume=volume)
        return None
    if action == "accept":
        config.save(dialogs.config_from_page(arg))
        # Recoge los sonidos copiados mientras la ventana estaba abierta.
        player.bank.reload()
        tooltip(strings.OPTIONS_SAVED, parent=mw)
        return None
    if action == "cancel":
        player.bank.reload()
    return None


def _log(where: str, exc: BaseException) -> None:
    AddonManager.get_logger(__name__).error("Fallo en %s", where, exc_info=exc)


def _open_folder() -> None:
    player.SOUNDS_DIR.mkdir(exist_ok=True)
    openFolder(str(player.SOUNDS_DIR))


@guarded
def open_options() -> None:
    """Abre la ventana de opciones (menú Herramientas y botón «Configuración» de Complementos).

    Devuelve None: si devolviera False, Anki abriría su editor de JSON.
    """
    global _dialog
    if mw is None:
        return
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    player.SOUNDS_DIR.mkdir(exist_ok=True)
    player.bank.reload()
    package = mw.addonManager.addon_from_module(__name__)
    description = dialogs.page(config.load(), player.present_files(), player.audio_available())
    _dialog = PanelDialog(parent_window(), package, description, _handle, _log, "sonidosConsolaPanel")
    _dialog.open()
