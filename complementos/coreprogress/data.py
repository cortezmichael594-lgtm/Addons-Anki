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

from anki.collection import Collection, SearchNode
from aqt import mw

from .effects import round_marks
from .errors import report



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


def done_today_search(col: Collection, deck_name: str) -> str:
    """Búsqueda de las tarjetas de un mazo (con sus submazos) que hoy ya salieron
    de la cola: respondidas hoy y que no siguen en aprendizaje.

    1.2.0 (informe del 2026-11-09): el 100 % de la barra es todo lo de hoy en ese
    mazo, lo hecho más lo que queda, para que al volver a un mazo a medias la
    barra empiece donde lo dejó y no en 0 %. «rated:1» sigue el cambio de día de
    Anki. Solo se lee: nunca se cambia nada.
    """
    return col.build_search_string(SearchNode(deck=deck_name), "rated:1", "-is:learn")


def done_today(col: Collection, deck_name: str) -> int:
    """Cuántas tarjetas del mazo salieron hoy de la cola (ver done_today_search)."""
    return len(col.find_cards(done_today_search(col, deck_name)))


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
    """Los hitos como pares {pos, num}, más la marca final con el total.

    1.3.0 (informe del 2026-11-16, decisión 2): números redondos (5, 10, 15,
    20 con 27 tarjetas) en lugar del 20, 40, 60 y 80 % (5, 11, 16, 22), y una
    marca final con el total al 100 %, que cierra la escala y dice cuántas son
    hoy. Cada marca está donde llega el relleno al despachar ese número. La
    regla y el paso se fijan al entrar al repaso (effects.round_marks).
    """
    marks = [{"pos": num / initial_total * 100.0, "num": float(num)} for num in round_marks(initial_total)]
    if marks:
        marks.append({"pos": 100.0, "num": float(initial_total), "final": 1.0})
    return marks
