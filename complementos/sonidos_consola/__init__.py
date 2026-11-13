"""Sonidos de consola: sonidos al abrir Anki, al navegar por los menús, al cancelar, al aceptar, etc.

Este módulo solo registra: la entrada de menú, la acción de configuración, los ganchos y el
vigilante de la interfaz. Las reglas están en logic.py; el reproductor, en player.py; la
vigilancia de menús y ventanas, en watcher.py; la ventana, en dialogs.py.
"""

from __future__ import annotations

from aqt import gui_hooks, mw
from aqt.qt import QAction, qconnect

from . import actions, player, strings, watcher
from .errors import guarded

_watcher: watcher.InterfaceWatcher | None = None


@guarded
def _on_profile_did_open() -> None:
    player.SOUNDS_DIR.mkdir(exist_ok=True)
    player.bank.reload()
    player.bank.play("coldboot")


@guarded
def _on_profile_will_close() -> None:
    player.bank.stop_all()


@guarded
def _on_state_did_change(new_state: str, old_state: str) -> None:
    # Al pulsar «Comenzar a estudiar» (o entrar a estudiar por otra vía). Anki pasa por
    # «resetRequired» al refrescarse sin que la persona haya hecho nada: ese regreso no cuenta.
    if new_state == "review" and old_state not in ("review", "resetRequired"):
        player.bank.play("system_ng")


@guarded
def _on_reviewer_will_end() -> None:
    # Se sale del estudio a mitad (Mazos, Esc, otro mazo...): todavía hay tarjeta en pantalla.
    # Cuando se acaban las tarjetas, Anki ya la ha quitado y no suena «cancelar».
    if mw is not None and mw.reviewer.card is not None:
        player.bank.play("cancel")


def _register() -> None:
    global _watcher
    # Fuera de Anki (pruebas, comprobaciones) no hay ventana principal: no se registra nada.
    if mw is None:
        return

    action = QAction(strings.MENU_OPTIONS, mw)
    qconnect(action.triggered, actions.open_options)
    mw.form.menuTools.addAction(action)
    mw.addonManager.setConfigAction(__name__, actions.open_options)

    gui_hooks.profile_did_open.append(_on_profile_did_open)
    gui_hooks.profile_will_close.append(_on_profile_will_close)
    gui_hooks.state_did_change.append(_on_state_did_change)
    gui_hooks.reviewer_will_end.append(_on_reviewer_will_end)

    if player.audio_available():
        _watcher = watcher.InterfaceWatcher()
        mw.app.installEventFilter(_watcher)


_register()
