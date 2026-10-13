"""Pruebas de la lectura de datos y las cifras con una coleccion TEMPORAL
(nunca la de la persona).

Se ejecutan con herramientas/empaquetar.py, que anade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from anki.collection import Collection
from gritmap import data, decks
from gritmap.data import DayActivity, HeatmapData


def _utc(text: str) -> int:
    return int(datetime.fromisoformat(text).replace(tzinfo=timezone.utc).timestamp())


class AnkiTodayTest(unittest.TestCase):
    """Regresion de FIX-012: con la hora de cambio a las 12 o mas tarde, el dia
    iba un dia por delante. Cortes y desfases fijos, nunca leidos del reloj."""

    def check(self, cutoff_utc: str, offset_hours: int, expected: str) -> None:
        got = data.anki_today(_utc(cutoff_utc), timedelta(hours=offset_hours))
        self.assertEqual(got, date.fromisoformat(expected), cutoff_utc)

    def test_rollover_before_noon(self) -> None:
        # Corte el 14 a las 00:00, 04:00 y 11:00 locales (+2): hoy es el 13.
        self.check("2026-10-13T22:00:00", 2, "2026-10-13")
        self.check("2026-10-14T02:00:00", 2, "2026-10-13")
        self.check("2026-10-14T09:00:00", 2, "2026-10-13")

    def test_rollover_after_noon(self) -> None:
        # Corte el 13 a las 12:00 y a las 23:00 locales (+2): hoy es el 12.
        self.check("2026-10-13T10:00:00", 2, "2026-10-12")
        self.check("2026-10-13T21:00:00", 2, "2026-10-12")

    def test_daylight_saving_changes(self) -> None:
        # Hora de cambio 23 con desfase +1: el corte cae el 13 a las 23:00.
        self.check("2026-10-13T22:00:00", 1, "2026-10-12")
        self.check("2026-10-14T03:00:00", -3, "2026-10-13")
        # Madrid tras el cambio de horario, hora de cambio 11.
        self.check("2026-10-25T10:00:00", 1, "2026-10-24")


class StatsTest(unittest.TestCase):
    def make(self, past: dict[int, int]) -> HeatmapData:
        return HeatmapData(
            past={d: DayActivity(reviews=r, cards=r, new=0) for d, r in past.items()},
            future_counts={},
            today=date(2026, 10, 13),
        )

    def test_average_without_complete_days_is_none(self) -> None:
        # Regresion de FIX-010: solo hoy estudiado no es un promedio de 0.
        self.assertIsNone(data.window_average(self.make({0: 40}), "reviews", 30))

    def test_average_uses_complete_days_only(self) -> None:
        self.assertEqual(data.window_average(self.make({0: 999, 1: 10, 2: 30}), "reviews", 30), 20)

    def test_week_diff_compares_two_complete_weeks(self) -> None:
        # Regresion de FIX-001: hoy no cuenta; 7 dias contra los 7 anteriores.
        sample = self.make({0: 500, **{d: 10 for d in range(1, 8)}, **{d: 5 for d in range(8, 15)}})
        self.assertEqual(data.week_diff(sample, "reviews"), (35.0, True))

    def test_streaks_do_not_break_before_studying_today(self) -> None:
        self.assertEqual(data.streaks({1, 2, 3, 10, 11}), (3, 3))
        self.assertEqual(data.streaks({0, 1, 5, 6, 7, 8}), (2, 4))

    def test_retention_needs_enough_reviews(self) -> None:
        # Regresion de FIX-002: sin repasos que medir es N/A, no 0 %.
        sample = HeatmapData(past={}, future_counts={}, today=date(2026, 10, 13), retention_days={1: (5, 0)})
        self.assertIsNone(data.full_stats(sample).retention)


class CollectionDataTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.col = Collection(str(Path(self._tmp.name) / "prueba.anki2"))
        self.deck_a = self.col.decks.id("Idiomas")
        self.deck_b = self.col.decks.id("Idiomas::Aleman")
        self.other = self.col.decks.id("Otro")
        notetype = self.col.models.by_name("Basic")
        assert notetype is not None  # en una prueba, assert es lo adecuado
        self.cards: list[int] = []
        for index in range(12):
            note = self.col.new_note(notetype)
            note["Front"] = f"<b>pregunta</b> {index}"
            note["Back"] = "respuesta"
            deck = (self.deck_a, self.deck_b, self.other)[index % 3]
            self.col.add_note(note, deck)
            self.cards.extend(int(cid) for cid in note.card_ids())
        self.cutoff = int(self.col.sched.day_cutoff)

    def tearDown(self) -> None:
        self.col.close()
        self._tmp.cleanup()

    def add_revlog(self, cid: int, days_ago: int, ease: int, last_ivl: int, kind: int, offset: int = 0) -> None:
        stamp = (self.cutoff - days_ago * 86400 - 3600) * 1000 + offset
        db = self.col.db
        assert db is not None
        db.execute(
            "insert into revlog (id, cid, usn, ease, ivl, lastIvl, factor, time, type)"
            " values (?, ?, -1, ?, 1, ?, 2500, 6000, ?)",
            stamp, cid, ease, last_ivl, kind,
        )

    def test_empty_collection(self) -> None:
        result = data.fetch_data(self.col, decks.WHOLE_COLLECTION)
        self.assertEqual(result.past, {})
        self.assertEqual(result.future_counts, {})

    def test_new_cards_before_v3(self) -> None:
        """Regresion de FIX-011: con v1 y v2 la primera respuesta llevaba lastIvl
        negativo y la medida «Nuevas» daba 0."""
        for offset, cid in enumerate(self.cards[:4]):
            self.add_revlog(cid, 900, 3, -60, 0, offset)  # primera respuesta, estilo v2
            self.add_revlog(cid, 900, 3, -600, 0, offset + 100)  # segundo paso: no es nueva
        self.add_revlog(self.cards[5], 2, 3, 0, 0)  # primera respuesta, estilo v3
        result = data.fetch_data(self.col, decks.WHOLE_COLLECTION, "new")
        self.assertEqual(result.past[900].new, 4)
        self.assertEqual(result.past[900].reviews, 8)
        self.assertEqual(result.past[2].new, 1)

    def test_chunks_give_the_same_days(self) -> None:
        # Repasos repartidos en mas de dos anos, en los bordes de los tramos.
        for index, days_ago in enumerate((0, 1, 364, 365, 366, 729, 730, 731, 1500)):
            self.add_revlog(self.cards[index % len(self.cards)], days_ago, 3, 1, 1, index)
        self.add_revlog(self.cards[0], 365, 1, 1, 1, 50)
        result = data.fetch_data(self.col, decks.WHOLE_COLLECTION, "cards")
        self.assertEqual(sorted(result.past), [0, 1, 364, 365, 366, 729, 730, 731, 1500])
        self.assertEqual(result.past[365].reviews, 2)
        self.assertEqual(result.past[365].cards, 2)
        self.assertEqual(result.retention_days[365], (2, 1))

    def test_deck_scope_and_deleted_cards(self) -> None:
        """FIX-013 (+cid) da lo mismo que antes, y FIX-004: las tarjetas borradas
        cuentan en el mapa general pero no en el de un mazo."""
        for index, cid in enumerate(self.cards):
            self.add_revlog(cid, 3, 3, 1, 1, index)
        deleted = self.cards[0]  # esta en «Idiomas»
        self.col.remove_notes([self.col.get_card(deleted).nid])
        everything = data.fetch_data(self.col, decks.WHOLE_COLLECTION)
        self.assertEqual(everything.past[3].reviews, 12)
        self.col.decks.select(self.deck_a)
        scope = decks.build_scope(self.col, (), True)
        in_deck = data.fetch_data(self.col, scope)
        self.assertEqual(in_deck.past[3].reviews, 7)  # Idiomas y Aleman, sin la borrada
        excluded = decks.build_scope(self.col, (self.deck_b,), False)
        self.assertEqual(data.fetch_data(self.col, excluded).past[3].reviews, 8)

    def test_excluded_current_deck(self) -> None:
        self.col.decks.select(self.deck_b)
        scope = decks.build_scope(self.col, (self.deck_a,), True)
        self.assertTrue(scope.current_excluded)
        self.assertTrue(data.fetch_data(self.col, scope).deck_excluded)
        self.col.decks.select(self.other)
        self.assertFalse(decks.build_scope(self.col, (self.deck_a,), True).current_excluded)


if __name__ == "__main__":
    unittest.main()
