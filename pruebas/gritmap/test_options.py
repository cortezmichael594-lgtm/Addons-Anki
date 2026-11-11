"""Pruebas de la ventana de opciones que no necesitan Anki en marcha."""

from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from gritmap import i18n, options
from gritmap.state import state

WEB = Path(options.__file__).parent / "web"


class GoalProposalTest(unittest.TestCase):
    """Desde la 4.16.0 la propuesta es el 80 % exacto del promedio que dice la
    tarjeta, sin redondear a 5 (informe 4.15.1, apartado 4.3)."""

    def proposal(self, average: float) -> tuple[int, int | None]:
        entry = SimpleNamespace(
            current_deck_only=False, measure="cards", data=SimpleNamespace(today=date(2026, 11, 10))
        )
        with mock.patch.object(state, "data", entry), mock.patch.object(options, "daily_average", return_value=average):
            return options.goal_proposal("cards")

    def test_eighty_percent_of_the_shown_average(self) -> None:
        self.assertEqual(self.proposal(20.0), (16, 20))
        # La tarjeta dice 20 aunque el promedio sea 19,6: la propuesta sale de 20.
        self.assertEqual(self.proposal(19.6), (16, 20))
        self.assertEqual(self.proposal(7.0), (6, 7))

    def test_never_below_one(self) -> None:
        self.assertEqual(self.proposal(0.6)[0], 1)

    def test_without_history_keeps_the_fallback(self) -> None:
        self.assertEqual(self.proposal(0.0), (30, None))


class PanelTest(unittest.TestCase):
    """Informe 4.15.1, aplicado en la 4.16.0."""

    css = (WEB / "options.css").read_text(encoding="utf-8")
    js = (WEB / "options.js").read_text(encoding="utf-8")

    def test_groups_ordered_by_use(self) -> None:
        order = [self.js.index(f"page.appendChild({name});") for name in ("goalsCard", "countCard", "lookCard")]
        self.assertEqual(order, sorted(order))

    def test_text_links_use_the_link_colour(self) -> None:
        for selector in (".gritmap-o-link {", ".gritmap-o-back {"):
            block = self.css.split("#gritmap-o-app " + selector, 1)[1].split("}", 1)[0]
            self.assertIn("var(--gritmap-o-link)", block, selector)
        self.assertIn("--gritmap-o-link: var(--fg-link, #A3C1F7)", self.css)

    def test_placeholder_faint_and_stable_scrollbar(self) -> None:
        self.assertIn("input::placeholder", self.css)
        self.assertIn("--gritmap-o-faint: var(--fg-faint, #9AA3B4)", self.css)
        self.assertIn("scrollbar-gutter: stable", self.css)

    def test_empty_key_dates_text_in_every_language(self) -> None:
        for code, texts in i18n.STRINGS.items():
            self.assertIn("kd_empty", texts, code)
            self.assertIn(texts["card_next"], texts["kd_empty"], code)


if __name__ == "__main__":
    unittest.main()
