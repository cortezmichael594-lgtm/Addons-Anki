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
# The label stays on screen at least this long, even on very fast answers.
STREAK_MIN_VISIBLE_MS: int = 2000
# Below this many cards, checkpoints are hidden (they would be cramped).
MIN_CARDS_FOR_CHECKPOINTS: int = 10
# A broken personal record is celebrated from this streak up.
# HISTORIAL: era 5; el usuario lo bajó a 3. Cuando un récord coincide con un
# hito de racha, el texto de récord PREVALECE (lo decide controller, que
# comprueba is_record antes que el hito).
RECORD_MIN_STREAK: int = 3


def is_celebration_milestone(streak: int) -> bool:
    if streak in (2, 5, 10, 15):
        return True
    return streak > 15 and streak % 10 == 5