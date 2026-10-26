"""Pruebas de lo que valida y resume el panel de opciones (sin Anki en marcha)."""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import date, timedelta

import anki.lang
from gritmap import i18n, options
from gritmap.config import DEFAULT_CONFIG, FIT_WIDTH, KeyDate
from gritmap.data import DayActivity, HeatmapData
from gritmap.state import DataEntry, state

TODAY = date.today()
EXISTING = {1: "Idiomas", 2: "Idiomas::Inglés", 3: "Idiomas::Japonés", 4: "Medicina", 9: "Oposiciones"}


class ConfigFromPageTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_values_are_checked(self) -> None:
        # Nada de la pagina se usa sin comprobarlo.
        cfg = options.config_from_page(DEFAULT_CONFIG, {
            "theme": "no_existe",
            "cell_size": 999,
            "border_radius": 40,
            "measure": "minutos",
            "avg_window": 7,
            "goal_mode": "otra",
            "goal": -5,
        }, EXISTING)
        self.assertEqual(cfg.theme, DEFAULT_CONFIG.theme)
        self.assertEqual(cfg.cell_size, 60)
        self.assertEqual(cfg.border_radius, 15)
        self.assertEqual(cfg.measure, DEFAULT_CONFIG.measure)
        self.assertEqual(cfg.avg_window, DEFAULT_CONFIG.avg_window)
        self.assertEqual(cfg.goal_mode, DEFAULT_CONFIG.goal_mode)
        self.assertEqual(cfg.goal, 1)
        # Con «Ajustado al ancho», el redondeo llega a la mitad de 14.
        fit = options.config_from_page(DEFAULT_CONFIG, {"cell_size": 0, "border_radius": 12}, EXISTING)
        self.assertEqual((fit.cell_size, fit.border_radius), (FIT_WIDTH, 7))

    def test_only_existing_decks_are_saved(self) -> None:
        # Regla de FIX-016.
        cfg = options.config_from_page(DEFAULT_CONFIG, {"excluded": [2, 77, 2, "x"]}, EXISTING)
        self.assertEqual(cfg.excluded_decks, (2,))
        # Sin la lista de mazos leida, se conserva lo guardado.
        base = replace(DEFAULT_CONFIG, excluded_decks=(3,))
        self.assertEqual(options.config_from_page(base, {"excluded": None}, None).excluded_decks, (3,))

    def test_key_dates_are_cleaned_sorted_and_capped(self) -> None:
        raw = [
            {"day": "2026-12-01", "label": "  Final  "},
            {"day": "2026-11-01", "label": "Parcial"},
            {"day": "2026-11-01", "label": "Parcial"},
            {"day": "no", "label": "Malo"},
            {"day": "2026-11-05", "label": ""},
        ]
        cfg = options.config_from_page(DEFAULT_CONFIG, {"key_dates": raw}, EXISTING)
        self.assertEqual(
            cfg.key_dates,
            (KeyDate(date(2026, 11, 1), "Parcial"), KeyDate(date(2026, 12, 1), "Final")),
        )
        many = [{"day": "2027-01-01", "label": f"F{i}"} for i in range(60)]
        self.assertEqual(len(options.config_from_page(DEFAULT_CONFIG, {"key_dates": many}, EXISTING).key_dates), 50)

    def test_pause_starts_today_at_the_earliest(self) -> None:
        # Decision del cliente (4.7.0): la pausa no empieza en el pasado, y
        # dura 30 dias como mucho.
        past = {"start": (TODAY - timedelta(days=3)).isoformat(), "end": TODAY.isoformat()}
        self.assertIsNone(options.config_from_page(DEFAULT_CONFIG, {"pause": past}, EXISTING).pause)
        long = {"start": TODAY.isoformat(), "end": (TODAY + timedelta(days=90)).isoformat()}
        cfg = options.config_from_page(DEFAULT_CONFIG, {"pause": long}, EXISTING)
        self.assertEqual(cfg.pause, (TODAY, TODAY + timedelta(days=29)))
        # Una pausa guardada que ya empezo conserva su inicio.
        base = replace(DEFAULT_CONFIG, pause=(TODAY - timedelta(days=3), TODAY + timedelta(days=2)))
        kept = options.config_from_page(base, {"pause": past}, EXISTING)
        self.assertEqual(kept.pause, (TODAY - timedelta(days=3), TODAY))


class SummaryTextsTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()

    def test_deck_summary_names_the_decks(self) -> None:
        texts = options.summary_texts({"excluded": [2, 3]}, EXISTING)
        self.assertEqual(texts["decks"], "2 mazos excluidos: Inglés, Japonés")
        self.assertEqual(options.summary_texts({"excluded": []}, EXISTING)["decks"], "Ninguno")
        # Sin la lista de mazos, nada: la fila ensena un hueco gris.
        self.assertIsNone(options.summary_texts({"excluded": [2]}, None)["decks"])
        many = options.summary_texts({"excluded": [1, 2, 3, 4, 9]}, EXISTING)["decks"]
        self.assertTrue(many.endswith("y 2 más"), many)

    def test_key_date_summary_and_countdowns(self) -> None:
        soon = (TODAY + timedelta(days=23)).isoformat()
        gone = (TODAY - timedelta(days=5)).isoformat()
        texts = options.summary_texts({"key_dates": [{"day": soon, "label": "Examen"}, {"day": gone, "label": "Parcial"}]}, EXISTING)
        self.assertEqual(texts["dates"], "2 fechas marcadas · próxima: Examen, faltan 23 días")
        self.assertEqual(texts["countdowns"][gone], "(pasada)")
        past_only = options.summary_texts({"key_dates": [{"day": gone, "label": "Parcial"}]}, EXISTING)
        self.assertEqual(past_only["dates"], "1 fecha marcada, todas pasadas")
        self.assertEqual(options.summary_texts({"key_dates": []}, EXISTING)["dates"], "Ninguna")

    def test_pause_length(self) -> None:
        pause = {"start": TODAY.isoformat(), "end": (TODAY + timedelta(days=14)).isoformat()}
        self.assertEqual(options.summary_texts({"pause": pause}, EXISTING)["pause_days"], "15 días")


class GoalProposalTest(unittest.TestCase):
    def setUp(self) -> None:
        anki.lang.current_lang = "es"
        i18n.reset()
        self._saved = state.data

    def tearDown(self) -> None:
        state.data = self._saved

    def test_proposal_uses_the_daily_average_of_the_card(self) -> None:
        # 4.9.0: 4 dias de cada 7 con 72 repasos dan un promedio diario de 41
        # (el de la tarjeta), y la meta propuesta es su 80 % redondeado a 5.
        past = {d: DayActivity(72, 72, 0) for d in range(1, 29) if d % 7 in (0, 1, 2, 3)}
        data = HeatmapData(past=past, future_counts={}, today=TODAY)
        state.data = DataEntry(0, False, 0, (), "reviews", data)
        value, average = options.goal_proposal("reviews", DEFAULT_CONFIG)
        self.assertEqual(average, 41)
        self.assertEqual(value, 35)
        # Sin historial en esa medida, un valor prudente y sin promedio.
        self.assertEqual(options.goal_proposal("new", DEFAULT_CONFIG), (10, None))


if __name__ == "__main__":
    unittest.main()
