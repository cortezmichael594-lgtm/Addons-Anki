"""Pruebas de los textos en los 51 idiomas y de las reglas de plural.

Un hueco roto en un idioma solo se veria al pasar el raton con ese idioma
activo; estas pruebas lo detectan sin abrir Anki.
"""

from __future__ import annotations

import re
import unittest

import anki.lang
from gritmap import i18n

PLURAL_BASES = (
    "unit_day", "unit_review", "unit_card", "unit_new", "ago", "kd_left",
    "tt_reviews", "tt_cards", "tt_due", "tt_new", "opt_exclude_count", "opt_key_dates_count",
)


def use(code: str) -> None:
    anki.lang.current_lang = code
    i18n.reset()


class StringsTest(unittest.TestCase):
    def tearDown(self) -> None:
        use("es")

    def test_same_placeholders_as_english(self) -> None:
        english = i18n.STRINGS["en"]
        for code, texts in i18n.STRINGS.items():
            for key, text in texts.items():
                base = re.sub(r"_(zero|one|two|few|many|other)$", "", key)
                reference = english.get(key) or english.get(f"{base}_other") or english.get(base)
                if reference is None:
                    continue
                expected = set(re.findall(r"\{\w+\}", reference))
                got = set(re.findall(r"\{\w+\}", text))
                # «hace dos dias» puede escribirse sin la cifra (arabe, hebreo).
                self.assertTrue(got == expected or (key.endswith("_two") and got < expected), f"{code}.{key}: {text}")

    def test_bold_tags_are_balanced(self) -> None:
        for code, texts in i18n.STRINGS.items():
            for key, text in texts.items():
                self.assertEqual(text.count("<b>"), text.count("</b>"), f"{code}.{key}")

    def test_every_plural_form_has_a_text(self) -> None:
        for code in i18n.STRINGS:
            use(code)
            for base in PLURAL_BASES:
                for count in range(0, 202):
                    key = i18n.plural_key(base, count)
                    self.assertTrue(i18n.t(key) and i18n.t(key) != key, f"{code}.{base} {count}")


class PluralRulesTest(unittest.TestCase):
    """Tabla fija de casos CLDR (las reglas que usa el navegador)."""

    CASES = {
        "ru": {1: "one", 2: "few", 5: "many", 11: "many", 21: "one", 22: "few"},
        "pl": {1: "one", 22: "few", 25: "many", 12: "many"},
        "cs": {1: "one", 3: "few", 5: "other"},
        "ar": {0: "zero", 1: "one", 2: "two", 3: "few", 11: "many", 100: "other"},
        "ro": {0: "few", 1: "one", 19: "few", 20: "other", 101: "few"},
        "fr": {0: "one", 1: "one", 2: "other"},
        "sl": {1: "one", 2: "two", 3: "few", 5: "other", 101: "one"},
        "es": {0: "other", 1: "one", 2: "other"},
    }

    def test_cases(self) -> None:
        for code, cases in self.CASES.items():
            for count, category in cases.items():
                self.assertEqual(i18n.plural_category(code, count), category, f"{code} {count}")


class PluralTextsTest(unittest.TestCase):
    """Regresion de FIX-022: en ruso salia «22 дней» en lugar de «22 дня»."""

    def tearDown(self) -> None:
        use("es")

    def test_russian_units(self) -> None:
        use("ru")
        self.assertEqual(i18n.unit_label(22, "day"), "дня")
        self.assertEqual(i18n.unit_label(25, "day"), "дней")
        self.assertEqual(i18n.unit_label(21, "review"), "повторение")

    def test_spanish_counts(self) -> None:
        use("es")
        self.assertEqual(i18n.unit_label(1, "day"), "día")
        self.assertEqual(i18n.unit_label(0, "day"), "días")
        self.assertEqual(i18n.fill(i18n.plural_key("opt_exclude_count", 1), count=1), "1 mazo excluido")
        self.assertEqual(i18n.fill(i18n.plural_key("opt_key_dates_count", 3), count=3), "3 fechas marcadas")

    def test_romanian_twenty_takes_de(self) -> None:
        use("ro")
        self.assertEqual(i18n.unit_label(20, "day"), "de zile")
        self.assertEqual(i18n.unit_label(5, "day"), "zile")

    def test_language_without_own_text_falls_back_to_english(self) -> None:
        use("kk")
        self.assertEqual(i18n.t("week_tip"), "Last 7 days compared with the previous 7")


if __name__ == "__main__":
    unittest.main()
