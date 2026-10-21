"""In-memory state for one review session. No persistence here."""

from __future__ import annotations

from dataclasses import dataclass, field

from .data import compute_progress, remaining_count
from .effects import GOLD_STREAK_THRESHOLD


@dataclass(frozen=True)
class AnswerRecord:
    card_id: int
    was_correct: bool


@dataclass
class SessionState:
    # HISTORIAL: aqui se llevaban ademas dos conjuntos de identificadores
    # (tarjetas despachadas y tarjetas vistas). Desde que el avance lo marcan
    # los contadores vivos del planificador, nadie los leia: eran memoria y
    # ocasion de descuadre. La sesion solo guarda ya lo que de verdad usa.
    deck_id: int | None = None
    initial_total: int = 0
    answer_history: list[AnswerRecord] = field(default_factory=list)
    bar_injected: bool = False
    active: bool = False
    correct_streak: int = 0
    pending_celebration: bool = False
    gold_active: bool = False
    best_at_start: int = 0
    session_max: int = 0
    record_enabled: bool = True

    def reset(self) -> None:
        self.deck_id = None
        self.initial_total = 0
        self.answer_history.clear()
        self.bar_injected = False
        self.active = False
        self.correct_streak = 0
        self.pending_celebration = False
        self.gold_active = False
        self.best_at_start = 0
        self.session_max = 0
        self.record_enabled = True

    def progress(self) -> float:
        return compute_progress(self.initial_total, remaining_count())

    def register_answer(self, card_id: int, was_correct: bool) -> None:
        if was_correct:
            self.correct_streak += 1
            self.gold_active = self.correct_streak >= GOLD_STREAK_THRESHOLD
        else:
            self.correct_streak = 0
            self.gold_active = False
        if self.correct_streak > self.session_max:
            self.session_max = self.correct_streak
        self.answer_history.append(AnswerRecord(card_id, was_correct))

    def pop_last_answer(self) -> None:
        """Drop the most recent answer (one per undo) and recompute counters."""
        if self.answer_history:
            del self.answer_history[-1]
        self._recompute_streak()
        self._recompute_session_max()

    def _recompute_session_max(self) -> None:
        running = 0
        best = 0
        for record in self.answer_history:
            if record.was_correct:
                running += 1
                if running > best:
                    best = running
            else:
                running = 0
        self.session_max = best

    def _recompute_streak(self) -> None:
        streak = 0
        for record in reversed(self.answer_history):
            if not record.was_correct:
                break
            streak += 1
        self.correct_streak = streak
        self.gold_active = streak >= GOLD_STREAK_THRESHOLD