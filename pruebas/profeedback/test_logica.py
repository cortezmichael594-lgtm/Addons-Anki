"""Pruebas de la lógica de la celebración (2.5.0, informe 2.4.0), sin Anki a la vista."""

from __future__ import annotations

import unittest

from profeedback import logic


class DecideTests(unittest.TestCase):
    def test_day_end_is_gold_with_enough_cards_whatever_the_answers(self) -> None:
        result = logic.decide(logic.Remaining(0, 0), 3, logic.DaySummary(25))
        self.assertEqual(result, logic.Celebration("all", gold=True, confetti=True))

    def test_day_end_without_enough_cards_only_sounds(self) -> None:
        result = logic.decide(logic.Remaining(0, 0), 3, logic.DaySummary(5))
        self.assertEqual(result, logic.Celebration("all", gold=False, confetti=False))

    def test_deck_end_is_never_gold(self) -> None:
        result = logic.decide(logic.Remaining(0, 12), 30, logic.DaySummary(0))
        self.assertEqual(result, logic.Celebration("deck", gold=False, confetti=True))

    def test_day_celebration_once_per_day(self) -> None:
        result = logic.decide(logic.Remaining(0, 0), 6, logic.DaySummary(40), day_already_celebrated=True)
        self.assertEqual(result, logic.Celebration("deck", gold=False, confetti=True))

    def test_nothing_while_cards_remain(self) -> None:
        self.assertIsNone(logic.decide(logic.Remaining(3, 10), 30, logic.DaySummary(0)))

    def test_hard_is_correct_and_only_again_is_different(self) -> None:
        self.assertEqual(logic.CORRECT_EASES, frozenset({2, 3, 4}))
        self.assertEqual(logic.WRONG_EASES, frozenset({1}))


class SessionTests(unittest.TestCase):
    def test_undo_takes_the_answer_back(self) -> None:
        session = logic.ReviewSession()
        session.state_changed("review", "overview")
        for ease in (1, 3, 3):
            session.record(ease)
        session.undo_answer()
        self.assertEqual(session.answers, 2)
        session.undo_answer()
        session.undo_answer()
        session.undo_answer()
        self.assertEqual(session.answers, 0)


if __name__ == "__main__":
    unittest.main()
