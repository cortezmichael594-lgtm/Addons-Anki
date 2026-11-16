"""Tunable constants and the streak-milestone rule.

Identifiers are in English (like the Anki API); anything the user reads lives in
i18n.py.
"""

from __future__ import annotations

# Streak length at which the fill turns to the gold aura.
GOLD_STREAK_THRESHOLD: int = 5
# Debounce for on-screen refreshes (ms). Coalesces bursts of answers.
UPDATE_INTERVAL_MS: int = 120
# Minimum streak that triggers the sparkle burst (milestones below this only
# get the text label).
CELEBRATION_SPARKLE_MIN_STREAK: int = 5
# The streak/record label is shown this long and then fades out on its own,
# whatever happens with the card (1.2.0, informe del 2026-11-09: antes se
# quedaba hasta mostrar la respuesta, con un minimo de 2 s).
LABEL_VISIBLE_MS: int = 1500
# Below this many cards, checkpoints are hidden (they would be cramped).
MIN_CARDS_FOR_CHECKPOINTS: int = 10
# A broken personal record is celebrated from this streak up.
# HISTORIAL: era 5; el usuario lo bajó a 3. Cuando un récord coincide con un
# hito de racha, el texto de récord PREVALECE (lo decide controller, que
# comprueba is_record antes que el hito).
RECORD_MIN_STREAK: int = 3


def is_celebration_milestone(streak: int) -> bool:
    """Avisos de racha a las 5, 10, 20, 30... (cada diez desde 10).

    1.2.0 (informe del 2026-11-09): antes salian a las 2, 5, 10, 15, 25, 35...,
    uno cada cinco respuestas mas o menos, y el de 2 tras casi cada fallo; lo que
    se repite deja de verse. El primer record (desde 3) sigue avisando.
    """
    if streak == 5:
        return True
    return streak >= 10 and streak % 10 == 0

# --- 1.3.0 (informe del 2026-11-16) -------------------------------------------

# Hitos en números redondos (decisión 2): el paso es el menor de esta serie que
# deja cinco marcas o menos; ninguna más allá del 92 % del ancho, para no tocar
# la marca final con el total.
_MARK_STEPS: tuple[int, ...] = (5, 10, 20, 25, 50, 100, 200, 250, 500)
MAX_MARKS: int = 5
LAST_MARK_FRACTION: float = 0.92


def _steps() -> list[int]:
    steps = list(_MARK_STEPS)
    scale = 1000
    while scale <= 10**9:
        steps += [scale, 2 * scale, int(2.5 * scale), 5 * scale]
        scale *= 10
    return steps


def round_marks(total: int) -> list[int]:
    """Números de los hitos para un total de hoy: 27 → 5, 10, 15, 20.

    Una marca «10» significa siempre diez tarjetas, cada día. Con menos de
    MIN_CARDS_FOR_CHECKPOINTS tarjetas no hay marcas.
    """
    if total < MIN_CARDS_FOR_CHECKPOINTS:
        return []
    for step in _steps():
        marks = [n for n in range(step, total, step) if n / total <= LAST_MARK_FRACTION]
        if len(marks) <= MAX_MARKS:
            return marks
    return []


# Mejor racha de los últimos 30 días (decisión 1): se celebra al superarla,
# una vez por repaso, y el récord histórico queda como dato (y se celebra
# también si se bate). Se guarda la mejor racha de cada día de Anki.
BEST_WINDOW_DAYS: int = 30


def best_in_window(daily: dict[int, int], today: int, days: int = BEST_WINDOW_DAYS) -> int:
    """La mejor racha de los últimos `days` días de Anki, hoy incluido."""
    first = today - days + 1
    return max((value for day, value in daily.items() if first <= day <= today), default=0)


def with_day_best(daily: dict[int, int], today: int, value: int, days: int = BEST_WINDOW_DAYS) -> dict[int, int]:
    """El registro diario con la racha de hoy (si es mayor) y sin los días que
    ya no entran en la ventana."""
    first = today - days + 1
    kept = {day: best for day, best in daily.items() if first <= day <= today and best > 0}
    if value > kept.get(today, 0):
        kept[today] = value
    return kept


def celebration_for(streak: int, best_at_start: int, window_at_start: int, record_enabled: bool) -> str:
    """Qué aviso toca a esta racha: "record", "window", "streak" o "".

    Una sola celebración por respuesta, con este orden: récord, mejor de 30
    días y número de racha. Cada récord se celebra una vez por repaso, en el
    momento exacto de batirlo y desde RECORD_MIN_STREAK.
    """
    if record_enabled:
        if streak == max(best_at_start + 1, RECORD_MIN_STREAK):
            return "record"
        if window_at_start < best_at_start and streak == max(window_at_start + 1, RECORD_MIN_STREAK):
            return "window"
    if is_celebration_milestone(streak):
        return "streak"
    return ""
