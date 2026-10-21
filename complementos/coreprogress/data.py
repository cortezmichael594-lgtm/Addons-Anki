"""Read-only helpers over the collection. Nothing here writes to the collection.

Progress is driven purely by the scheduler's live counts, which is the source
of truth for "how much work is left today". A card only counts as done once it
truly leaves today's queue (it graduates, or a review card is pushed to a
future day). A failed card re-enters learning (Anki reshows it ~10 min later)
and stays inside `remaining` until you finally clear it, so failing never
advances the bar and never desyncs it: the card is counted exactly once, when
it is genuinely finished.

Because of that, each checkpoint is placed at the exact spot its own card count
reaches: the ball labelled N sits at N / total, and the fill also equals
N / total when N cards are done, so the fill lands precisely on the ball.

The counts come from the scheduler in one batch call, never per card, so the
bar stays cheap even with a huge collection.
"""

from __future__ import annotations

from aqt import mw

from .errors import report

# Checkpoints are taken at these fractions of the session's initial card count.
_CHECKPOINT_FRACTIONS: tuple[float, float, float, float] = (0.2, 0.4, 0.6, 0.8)


def _log(exc: Exception) -> None:
    report(exc, "data")


def remaining_count() -> int:
    try:
        if mw and mw.col and hasattr(mw.col, "sched"):
            counts = mw.col.sched.counts()
            return int(counts[0]) + int(counts[1]) + int(counts[2])
    except Exception as exc:
        _log(exc)
    return 0


def compute_progress(initial_total: int, remaining: int) -> float:
    """Percent of today's initial pile that has genuinely been cleared.

    HISTORIAL: esta funcion recibia ademas un recuento propio de tarjetas
    despachadas que ya no se usaba, porque el avance es
    (total_inicial - restantes) / total_inicial: solo sube cuando una tarjeta
    sale de verdad de la cola, y una fallada que vuelve a aprendizaje no
    descuadra la barra. El parametro sobrante se ha retirado.
    """
    if initial_total <= 0:
        return 0.0
    done = initial_total - remaining
    if done < 0:
        done = 0
    return min(100.0, done / initial_total * 100.0)


def checkpoint_marks(initial_total: int) -> list[dict[str, float]]:
    """Return the checkpoints as {pos, num} pairs for the given session.

    Each ball's number is a rounded card count; its position is that exact count
    as a percentage (num / initial_total), so the fill stops right on the ball
    when that many cards are done. Numbers that would collide, land at 0, or
    reach the end are skipped.
    """
    marks: list[dict[str, float]] = []
    seen: set[int] = set()
    for fraction in _CHECKPOINT_FRACTIONS:
        num = round(initial_total * fraction)
        if num <= 0 or num >= initial_total or num in seen:
            continue
        seen.add(num)
        marks.append({"pos": num / initial_total * 100.0, "num": float(num)})
    return marks