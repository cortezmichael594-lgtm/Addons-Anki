"""Tunable constants and the streak-milestone rule.

Identifiers are in English (like the Anki API); anything the user reads lives in
i18n.py.
"""

from __future__ import annotations

# Streak length at which the fill turns to the gold aura.
GOLD_STREAK_THRESHOLD: int = 5
# Debounce for on-screen refreshes (ms). Coalesces bursts of answers.
UPDATE_INTERVAL_MS: int = 120
# The streak/record label follows the fill edge but never sits closer than this
# to the left border (percent), so it stays readable at 0%.
STREAK_LABEL_MIN_LEFT_PERCENT: float = 2.8
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