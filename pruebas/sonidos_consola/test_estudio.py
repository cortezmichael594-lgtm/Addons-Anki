"""Sonidos del estudio: comenzar (snd_system_ng), salir a mitad (cancelar) y terminar el mazo (trofeo)."""

from __future__ import annotations

import types
import unittest

import sonidos_consola
from sonidos_consola import player


class _Recorder:
    def __init__(self) -> None:
        self.played: list[str] = []

    def play(self, key: str, **_kwargs: object) -> None:
        self.played.append(key)


class StudySoundsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.recorder = _Recorder()
        self._bank = player.bank
        self._mw = sonidos_consola.mw
        player.bank = self.recorder  # type: ignore[assignment]
        self.reviewer = types.SimpleNamespace(card=None)
        sonidos_consola.mw = types.SimpleNamespace(reviewer=self.reviewer)  # type: ignore[assignment]

    def tearDown(self) -> None:
        player.bank = self._bank
        sonidos_consola.mw = self._mw

    def _start(self) -> None:
        sonidos_consola._on_state_did_change("review", "overview")

    def test_start_plays_ng(self) -> None:
        self._start()
        self.assertEqual(self.recorder.played, ["system_ng"])

    def test_refresh_is_not_a_start(self) -> None:
        sonidos_consola._on_state_did_change("review", "resetRequired")
        self.assertEqual(self.recorder.played, [])

    def test_leaving_halfway_plays_cancel(self) -> None:
        self._start()
        sonidos_consola._on_reviewer_did_answer_card(None, None, 3)
        self.reviewer.card = object()
        sonidos_consola._on_reviewer_will_end()
        self.assertEqual(self.recorder.played, ["system_ng", "cancel"])

    def test_finishing_the_deck_plays_trophy(self) -> None:
        self._start()
        sonidos_consola._on_reviewer_did_answer_card(None, None, 3)
        self.reviewer.card = None
        sonidos_consola._on_reviewer_will_end()
        self.assertEqual(self.recorder.played, ["system_ng", "trophy"])

    def test_no_trophy_without_studying(self) -> None:
        self._start()
        self.reviewer.card = None
        sonidos_consola._on_reviewer_will_end()
        self.assertEqual(self.recorder.played, ["system_ng"])

    def test_counter_restarts_with_each_session(self) -> None:
        self._start()
        sonidos_consola._on_reviewer_did_answer_card(None, None, 3)
        sonidos_consola._on_reviewer_will_end()
        self._start()
        sonidos_consola._on_reviewer_will_end()
        self.assertEqual(self.recorder.played, ["system_ng", "trophy", "system_ng"])


if __name__ == "__main__":
    unittest.main()
