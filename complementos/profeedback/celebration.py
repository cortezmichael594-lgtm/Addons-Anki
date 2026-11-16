"""Celebración al terminar de repasar: sonido y confeti (dorado al terminar el día).

La decisión (qué celebrar) está en logic.py y se prueba sin Anki. Este módulo la conecta con
los momentos de Anki: cuándo se entra y se sale del repaso, y cuándo la pantalla del mazo
está lista para mostrar el confeti.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-10-13): la celebración podía saltar al abrir un mazo ya terminado.
# FIX-003 (2026-10-13): el «día perfecto» se contaba mal (medianoche, perfiles, otros dispositivos).

from __future__ import annotations

import json
from typing import Final

from anki.cards import Card
from anki.collection import Collection, OpChangesAfterUndo
from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.overview import Overview
from aqt.reviewer import Reviewer

from . import audio, config, logic
from .errors import guarded, log_error
from .paths import WEB_DIR, SoundKind

# --- FIX-002 (2026-10-13) ---
# Síntoma: tras repasar y salir a la lista de mazos (sin terminar), al abrir más tarde un mazo
#   ya terminado saltaban el sonido y el confeti.
# Causa: la bandera «acabo de repasar» no se apagaba al salir del repaso por otro camino.
# Regla: la sesión (logic.ReviewSession) solo celebra al volver del repaso a la pantalla del
#   mazo; salir por cualquier otra pantalla la descarta.
_session = logic.ReviewSession()

_engine_js: str | None = None
# Días ya celebrados en grande, por perfil y día de Anki: la celebración del día sale una
# vez (2.5.0, informe 2.4.0, apartado 8.11). Si vuelven tarjetas, se celebra como un mazo.
_days_celebrated: set[tuple[str, int]] = set()

# Cómo se suelta cada confeti: al terminar un mazo, dos cañones; al terminar todo, lluvia.
_EFFECT: Final[dict[str, str]] = {"deck": "burst", "all": "rain"}


def _engine() -> str:
    """Código del motor de confeti (web/confetti.js). Se lee del disco una sola vez."""
    global _engine_js
    if _engine_js is None:
        try:
            _engine_js = (WEB_DIR / "confetti.js").read_text(encoding="utf-8")
        except OSError as error:
            log_error("celebration.engine", error)
            _engine_js = ""
    return _engine_js


def register() -> None:
    gui_hooks.state_did_change.append(_on_state_did_change)
    gui_hooks.overview_did_refresh.append(_on_overview_did_refresh)
    gui_hooks.reviewer_did_answer_card.append(_on_did_answer)
    gui_hooks.state_did_undo.append(_on_did_undo)


def reset() -> None:
    """Descarta la sesión en curso (al abrir o cerrar un perfil)."""
    _session.reset()


# ── enganches ────────────────────────────────────────────────────────────────
@guarded
def _on_did_answer(reviewer: Reviewer, card: Card, ease: int) -> None:
    _session.record(ease)


@guarded
def _on_did_undo(changes: OpChangesAfterUndo) -> None:
    # Una respuesta deshecha deja de contar para la sesión (informe 2.4.0, apartado 4.2).
    if mw is None or mw.col is None or mw.state != "review":
        return
    if changes.operation == mw.col.tr.actions_answer_card():
        _session.undo_answer()


@guarded
def _on_state_did_change(new_state: str, old_state: str) -> None:
    _session.state_changed(new_state, old_state)


@guarded
def _on_overview_did_refresh(overview: Overview) -> None:
    if mw is None or mw.col is None:
        return
    if _session.take_ended():
        _evaluate()


# ── decisión y disparo ───────────────────────────────────────────────────────
def _evaluate() -> None:
    settings = config.get()
    off = config.SOUND_OFF
    if settings.deckFinishSound == off and settings.allDoneSound == off and not settings.confettiEnabled:
        return
    answers = _session.answers
    profile = mw.pm.name if mw is not None and mw.pm is not None else ""

    def op(col: Collection) -> tuple[logic.Celebration | None, tuple[str, int]]:
        # La lectura va en segundo plano para que la ventana no se quede bloqueada ni un
        # instante en colecciones grandes.
        remaining = logic.remaining_cards(col)
        # --- FIX-003 (2026-10-13) ---
        # Síntoma: el «día perfecto» empezaba a medianoche, mezclaba los perfiles y se
        #   perdía si Anki se cerraba de golpe.
        # Causa: el complemento llevaba su propia cuenta del día en la configuración.
        # Regla: el resumen del día sale del historial de Anki (logic.day_summary), y solo
        #   se pide cuando ya no queda nada por repasar.
        day = logic.day_summary(col) if remaining.total == 0 else logic.DaySummary(0)
        key = (profile or "", col.sched.day_cutoff)
        return logic.decide(remaining, answers, day, key in _days_celebrated), key

    QueryOp(parent=mw, op=op, success=_on_decided).failure(_on_failed).run_in_background()


def _on_failed(error: Exception) -> None:
    # Una celebración que no se puede decidir no merece interrumpir a nadie: solo se anota.
    log_error("celebration.query", error)


@guarded
def _on_decided(result: tuple[logic.Celebration | None, tuple[str, int]]) -> None:
    celebration, day_key = result
    if celebration is None or mw is None:
        return
    if celebration.scope == "all":
        _days_celebrated.add(day_key)
    settings = config.get()
    _play_finish_sound(celebration, settings)
    if settings.confettiEnabled and celebration.confetti:
        _launch_confetti(celebration)


def _play_finish_sound(celebration: logic.Celebration, settings: config.AddonConfig) -> None:
    kind: SoundKind
    if celebration.scope == "all":
        kind, name = "all_finish", settings.allDoneSound
    else:
        kind, name = "deck_finish", settings.deckFinishSound
    audio.play(kind, name)


def _launch_confetti(celebration: logic.Celebration) -> None:
    engine = _engine()
    if mw is None or not engine:
        return
    kind = "gold" if celebration.gold else "normal"
    effect = _EFFECT[celebration.scope]
    # eval espera a que la página esté lista (Anki lo encola hasta entonces): no hace falta
    # adivinar el momento.
    mw.web.eval(f"{engine}\nwindow.profeedbackConfetti.{effect}({json.dumps(kind)});")
