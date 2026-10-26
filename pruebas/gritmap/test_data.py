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

    def test_daily_average_counts_natural_days(self) -> None:
        # 4.8.0: 4 dias estudiados de 7 con 70 repasos: 280 / 7 = 40.
        sample = self.make({0: 999, 1: 70, 3: 70, 5: 70, 7: 70})
        self.assertEqual(data.daily_average(sample, "reviews", 30), 40)
        # Desde el primer dia estudiado: quien empezo hace 2 dias no se divide
        # entre 30.
        self.assertEqual(data.daily_average(self.make({1: 10, 2: 30}), "reviews", 30), 20)
        # Los dias de pausa no cuentan en el divisor; los de comodin, si.
        self.assertEqual(data.daily_average(sample, "reviews", 30, frozenset({2, 4, 6})), 70)
        # Regla de FIX-010: sin dias completos estudiados, None.
        self.assertIsNone(data.daily_average(self.make({0: 40}), "reviews", 30))

    def test_average_uses_complete_days_only(self) -> None:
        self.assertEqual(data.window_average(self.make({0: 999, 1: 10, 2: 30}), "reviews", 30), 20)

    def test_week_diff_compares_two_complete_weeks(self) -> None:
        # Regresion de FIX-001: hoy no cuenta; 7 dias contra los 7 anteriores.
        sample = self.make({0: 500, **{d: 10 for d in range(1, 8)}, **{d: 5 for d in range(8, 15)}})
        self.assertEqual(data.week_diff(sample, "reviews"), (35.0, True))

    def test_streaks_do_not_break_before_studying_today(self) -> None:
        self.assertEqual(data.streaks({1, 2, 3, 10, 11}), (3, 3))
        self.assertEqual(data.streaks({0, 1, 5, 6, 7, 8}), (2, 4))

    def test_stats_follow_the_measure(self) -> None:
        """Con «Nuevas», un dia cuenta como estudiado solo si empezo alguna nueva
        (peticion del cliente, 2026-10-13)."""
        sample = HeatmapData(
            past={
                1: DayActivity(reviews=50, cards=40, new=5),
                2: DayActivity(reviews=30, cards=20, new=0),
                3: DayActivity(reviews=10, cards=10, new=3),
            },
            future_counts={},
            today=date(2026, 10, 13),
        )
        new = data.full_stats(sample, "new", 30)
        # 4.7.0 (cliente, 2026-10-22): la racha cuenta cualquier respuesta;
        # la medida sigue en el promedio y los dias estudiados.
        self.assertEqual(new.current_streak, 3)
        self.assertEqual(new.longest_streak, 3)
        # 4.8.0: promedio por dia natural desde el primer dia estudiado del
        # periodo (dia 3): 8 nuevas en 3 dias.
        self.assertAlmostEqual(new.average, 8 / 3)
        self.assertEqual(new.studied_pct, 67)
        reviews = data.full_stats(sample, "reviews", 30)
        self.assertEqual(reviews.current_streak, 3)
        self.assertEqual(reviews.studied_pct, 100)

    def test_week_totals_give_the_reference(self) -> None:
        # 3.6.0: el total de los 7 dias acompana a la diferencia (FIX-001: hoy no entra).
        sample = self.make({0: 500, **{d: 10 for d in range(1, 8)}, **{d: 5 for d in range(8, 15)}})
        self.assertEqual(data.week_totals(sample, "reviews"), (70.0, 35.0, True))

    def test_today_done_and_previous_best(self) -> None:
        # Racha actual 0-1-2 (3 dias, hoy incluido) y otra anterior de 2.
        stats = data.full_stats(self.make({0: 5, 1: 5, 2: 5, 6: 5, 7: 5}), "reviews", 30)
        self.assertEqual((stats.current_streak, stats.longest_streak), (3, 3))
        self.assertTrue(stats.today_done)
        self.assertEqual(stats.previous_best, 2)
        # Sin estudiar hoy, la racha sigue (1-2) y hoy queda pendiente.
        pending = data.full_stats(self.make({1: 5, 2: 5, 6: 5, 7: 5, 8: 5}), "reviews", 30)
        self.assertEqual((pending.current_streak, pending.previous_best), (2, 3))
        self.assertFalse(pending.today_done)

    def test_studied_fraction(self) -> None:
        self.assertEqual(data.studied_fraction(self.make({1: 50, 2: 10, 3: 60}), 30, "reviews"), (3, 3))

    def test_freezes_forgive_single_days(self) -> None:
        # 8 dias seguidos (12 a 5) ganan un comodin; el dia 4 lo gasta.
        studied = {1, 2, 3, *range(5, 13)}
        self.assertEqual(data.streak_state(studied, False).current, 3)
        state = data.streak_state(studied, True)
        self.assertEqual((state.current, state.forgiven), (11, {4: "freeze"}))
        # Sin comodines guardados, el dia sin estudiar rompe la racha.
        self.assertEqual(data.streak_state({1, 2, 4, 5}, True).current, 2)

    def test_freeze_count_restarts_after_a_gap(self) -> None:
        # 4.7.0: los 7 dias para ganar un comodin se cuentan desde el ultimo
        # dia sin estudio, aunque lo cubriera un comodin: no se ganan
        # comodines mientras se gastan.
        studied = set(range(1, 30)) - {10, 20}
        state = data.streak_state(studied, True)
        self.assertEqual(state.current, 29 - 2)
        self.assertEqual(state.forgiven, {20: "freeze", 10: "freeze"})
        # Del dia 9 al 1 hay 9 seguidos: gana uno; quedan 0 + 1.
        self.assertEqual(state.freezes_left, 1)

    def test_freezes_are_capped_at_two(self) -> None:
        state = data.streak_state(set(range(1, 30)), True)
        self.assertEqual(state.freezes_left, data.MAX_FREEZES)

    def test_pause_neither_adds_nor_breaks(self) -> None:
        paused = data.paused_days((date(2026, 10, 10), date(2026, 10, 11)), date(2026, 10, 13))
        self.assertEqual(paused, frozenset({2, 3}))
        state = data.streak_state({0, 1, 4, 5}, False, paused)
        self.assertEqual((state.current, state.forgiven), (4, {2: "pause", 3: "pause"}))

    def test_surprises_are_real_and_one_at_a_time(self) -> None:
        # Nueva racha mas larga: hoy supera la mejor anterior.
        sample = self.make({0: 5, 1: 5, 2: 5, 10: 5, 11: 5})
        stats = data.full_stats(sample, "reviews", 30)
        self.assertEqual(data.surprise(sample, "reviews", stats), ("record", 0))
        # 4.7.0: mejor semana del ano, no mejor dia. Un dia enorme dentro de
        # una semana floja no es sorpresa.
        steady = {d: 10 for d in range(0, 60, 2)}
        best = self.make({**steady, **{d: 30 for d in range(0, 7)}})
        self.assertEqual(data.surprise(best, "reviews", data.full_stats(best)), ("best_week", 0))
        binge = self.make({**{d: 20 for d in range(7, 60)}, 0: 90, **{d: 5 for d in range(1, 7)}})
        self.assertIsNone(data.surprise(binge, "reviews", data.full_stats(binge)))
        # 4.8.0: «Un año seguido» es la primera sorpresa del dia.
        year = self.make({d: 10 for d in range(365)})
        self.assertEqual(data.surprise(year, "reviews", data.full_stats(year)), ("year_streak", 0))
        # Sin estudiar hoy no hay sorpresa.
        quiet = self.make({1: 90})
        self.assertIsNone(data.surprise(quiet, "reviews", data.full_stats(quiet)))
        # Cifra redonda del ano cruzada hoy.
        milestone = self.make({0: 30, 30: 980})
        self.assertEqual(data.surprise(milestone, "reviews", data.full_stats(milestone)), ("year_total", 1000))

    def test_three_periods(self) -> None:
        self.assertEqual(data.WINDOWS, (30, 365, 0))

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
