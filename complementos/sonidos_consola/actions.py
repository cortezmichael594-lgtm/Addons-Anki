"""Lo que ocurre al abrir la ventana de opciones y al pulsar sus botones."""

from __future__ import annotations

from aqt import mw
from aqt.qt import qconnect
from aqt.utils import openFolder, tooltip

from . import config, dialogs, player, strings
from .errors import guarded

# La ventana abierta se guarda aquí: si no, el recolector de basura la cerraría.
_dialog: dialogs.OptionsDialog | None = None


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
    parent = mw.app.activeWindow() or mw
    _dialog = dialogs.OptionsDialog(
        parent,
        config.load(),
        player.present_files(),
        player.audio_available(),
        on_test=_test_sound,
        on_open_folder=_open_folder,
    )
    qconnect(_dialog.accepted, _on_accepted)
    qconnect(_dialog.finished, _on_finished)
    _dialog.open()


@guarded
def _test_sound(key: str, volume: int) -> None:
    player.bank.play(key, ignore_switch=True, volume=volume)


@guarded
def _open_folder() -> None:
    player.SOUNDS_DIR.mkdir(exist_ok=True)
    openFolder(str(player.SOUNDS_DIR))


@guarded
def _on_accepted() -> None:
    if _dialog is None:
        return
    config.save(_dialog.values())
    tooltip(strings.OPTIONS_SAVED, parent=mw)


@guarded
def _on_finished(_result: int = 0) -> None:
    global _dialog
    # Recoge los sonidos que se hayan copiado mientras la ventana estaba abierta.
    player.bank.reload()
    _dialog = None
