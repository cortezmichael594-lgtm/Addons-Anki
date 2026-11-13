"""Sonidos de consola: sonidos al abrir Anki, al navegar por los menús, al cancelar, al aceptar, etc.

Este módulo solo registra: la acción de configuración (Herramientas > Complementos), los ganchos y el
vigilante de la interfaz. Las reglas están en logic.py; el reproductor, en player.py; la
vigilancia de menús y ventanas, en watcher.py; la ventana, en dialogs.py.
"""

from __future__ import annotations

from aqt import gui_hooks, mw

from . import actions, player, watcher
from .errors import guarded

_watcher: watcher.InterfaceWatcher | None = None
# Tarjetas respondidas desde que se entró a estudiar: terminar un mazo cuenta solo si se estudió algo.
_answered_this_session = 0


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
    global _answered_this_session
    if new_state == "review" and old_state not in ("review", "resetRequired"):
        _answered_this_session = 0
        player.bank.play("system_ng")


@guarded
def _on_reviewer_did_answer_card(*_args: object) -> None:
    global _answered_this_session
    _answered_this_session += 1


@guarded
def _on_reviewer_will_end() -> None:
    # Se sale del estudio a mitad (Mazos, Esc, otro mazo...): todavía hay tarjeta en pantalla.
    # Cuando se acaban las tarjetas, Anki ya la ha quitado: es el final del mazo y suena el trofeo
    # (si se estudió al menos una tarjeta en esta sesión).
    if mw is None:
        return
    if mw.reviewer.card is not None:
        player.bank.play("cancel")
    elif _answered_this_session > 0:
        player.bank.play("trophy")


def _register() -> None:
    global _watcher
    # Fuera de Anki (pruebas, comprobaciones) no hay ventana principal: no se registra nada.
    if mw is None:
        return

    mw.addonManager.setConfigAction(__name__, actions.open_options)

    gui_hooks.profile_did_open.append(_on_profile_did_open)
    gui_hooks.profile_will_close.append(_on_profile_will_close)
    gui_hooks.state_did_change.append(_on_state_did_change)
    gui_hooks.reviewer_will_end.append(_on_reviewer_will_end)
    gui_hooks.reviewer_did_answer_card.append(_on_reviewer_did_answer_card)

    if player.audio_available():
        _watcher = watcher.InterfaceWatcher()
        mw.app.installEventFilter(_watcher)


_register()
