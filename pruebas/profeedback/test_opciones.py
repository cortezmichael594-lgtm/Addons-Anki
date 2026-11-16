"""Pruebas del panel de ajustes, de los sonidos y del aspecto, sin Anki a la vista: la
descripción que recibe la página, la lectura de lo elegido (regla de FIX-001), «Probar», las
carpetas de sonidos propios (FIX-004) y lo que cambió en la 2.5.0 (informe 2.4.0).

Se ejecutan con herramientas/empaquetar.py, que añade complementos/ al
PYTHONPATH.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from profeedback import dialogs, paths
from profeedback.config import AddonConfig

ADDON = Path(dialogs.__file__).parent
SOUNDS = {
    "correct": ["acierto-1-madera.mp3", "acierto-2-campanilla.mp3", "mio.mp3"],
    "wrong": ["fallo-1-madera.mp3", "fallo-2-campanilla.mp3"],
    "deck_finish": ["mazo-1-madera.mp3"],
    "all_finish": [],
}


def _all_items(items: list[dict]) -> list[dict]:
    found: list[dict] = []
    for item in items:
        found.append(item)
        found.extend(_all_items(item.get("children", [])))
    return found


def _selects(page: dict) -> dict[str, dict]:
    return {
        item["key"]: item for card in page["cards"] for item in _all_items(card["items"]) if item["type"] == "select"
    }


class PanelPageTests(unittest.TestCase):
    """2.5.0 (informe 2.4.0, apartado 8.7): dos recuadros, sin casillas de sonido."""

    def test_every_control_has_value_and_default(self) -> None:
        page = dialogs.page(AddonConfig(), SOUNDS)
        keys = {item["key"] for card in page["cards"] for item in _all_items(card["items"]) if "key" in item}
        self.assertEqual(keys, set(page["values"]))
        self.assertEqual(set(page["defaults"]), set(page["values"]))
        json.dumps(page)

    def test_two_cards_and_sixteen_controls(self) -> None:
        page = dialogs.page(AddonConfig(), SOUNDS)
        self.assertEqual(len(page["cards"]), 2)
        self.assertTrue(page["hideTitle"])
        sound, look = page["cards"]
        self.assertEqual([item["type"] for item in sound["items"]], ["slider"] + ["select"] * 4)
        self.assertEqual([item["type"] for item in look["items"]], ["check"] * 3)
        controls = 1 + 4 * 2 + 3  # deslizador, cuatro listas con «Probar», tres casillas
        self.assertLessEqual(controls, 16)

    def test_list_order_off_sounds_random_open(self) -> None:
        options = _selects(dialogs.page(AddonConfig(), SOUNDS))["answerSound"]["options"]
        values = [opt.get("value") for opt in options]
        self.assertEqual(values[0], "-")
        self.assertEqual(values[1:4], SOUNDS["correct"])
        self.assertEqual(values[4], "")
        self.assertTrue(options[5].get("separator"))
        self.assertEqual(options[6]["action"], "open:correct")

    def test_list_without_sounds_has_no_random(self) -> None:
        values = [opt.get("value") for opt in _selects(dialogs.page(AddonConfig(), SOUNDS))["allDoneSound"]["options"]]
        self.assertNotIn("", values)
        self.assertEqual(values[0], "-")

    def test_missing_saved_sound_shows_number_one(self) -> None:
        page = dialogs.page(AddonConfig(answerSound="gone.mp3"), SOUNDS)
        self.assertEqual(page["values"]["answerSound"], "acierto-1-madera.mp3")

    def test_defaults_are_fixed_for_answers_and_random_for_finishes(self) -> None:
        defaults = dialogs.page(AddonConfig(), SOUNDS)["defaults"]
        self.assertEqual(defaults["answerSound"], "acierto-1-madera.mp3")
        self.assertEqual(defaults["wrongSound"], "fallo-1-madera.mp3")
        self.assertEqual(defaults["deckFinishSound"], "")
        self.assertEqual(defaults["allDoneSound"], "")

    def test_test_buttons_have_their_own_names(self) -> None:
        names = [item["test"]["aria"] for item in _selects(dialogs.page(AddonConfig(), SOUNDS)).values()]
        self.assertEqual(len(set(names)), 4)


class ConfigMigrationTests(unittest.TestCase):
    def test_old_unchecked_boxes_become_no_sound(self) -> None:
        cfg = AddonConfig.from_stored(
            {"answerSoundEnabled": False, "wrongSoundEnabled": True, "sessionSoundsEnabled": False, "answerSound": ""}
        )
        self.assertEqual(cfg.answerSound, "-")
        self.assertEqual(cfg.wrongSound, "fallo-1-madera.mp3")
        self.assertEqual((cfg.deckFinishSound, cfg.allDoneSound), ("-", "-"))

    def test_old_random_answers_become_number_one(self) -> None:
        cfg = AddonConfig.from_stored({"answerSound": "", "wrongSound": ""})
        self.assertEqual((cfg.answerSound, cfg.wrongSound), ("acierto-1-madera.mp3", "fallo-1-madera.mp3"))

    def test_new_config_keeps_random(self) -> None:
        cfg = AddonConfig.from_stored({"answerSound": "", "configVersion": 2})
        self.assertEqual(cfg.answerSound, "")


class AnswerSoundTests(unittest.TestCase):
    """2.5.0: «Difícil» suena como acierto; solo «Otra vez» lleva el otro sonido."""

    def test_answer_dispatch(self) -> None:
        from profeedback import feedback

        with mock.patch.object(feedback.audio, "play") as play:
            for ease in (1, 2, 3, 4):
                feedback._on_did_answer(None, None, ease)  # type: ignore[arg-type]
        kinds = [call.args[0] for call in play.call_args_list]
        self.assertEqual(kinds, ["wrong", "correct", "correct", "correct"])

    def test_bundled_sounds(self) -> None:
        expected = {
            "correct": ["acierto-1-madera.mp3", "acierto-2-campanilla.mp3", "acierto-3-suave.mp3"],
            "wrong": ["fallo-1-madera.mp3", "fallo-2-campanilla.mp3", "fallo-3-suave.mp3"],
            "deck_finish": [
                "mazo-1-madera.mp3",
                "mazo-2-campanilla.mp3",
                "mazo-3-suave.mp3",
                "perfecto-mazo-1-madera.mp3",
                "perfecto-mazo-2-campanilla.mp3",
                "perfecto-mazo-3-suave.mp3",
            ],
            "all_finish": [
                "todo-1-madera.mp3",
                "todo-2-campanilla.mp3",
                "todo-3-suave.mp3",
                "perfecto-todo-1-madera.mp3",
                "perfecto-todo-2-campanilla.mp3",
                "perfecto-todo-3-suave.mp3",
            ],
        }
        for kind, names in expected.items():
            found = [
                p.name for sub in paths.SOUND_SUBFOLDERS[kind] for p in sorted((ADDON / "sonidos" / sub).glob("*.mp3"))
            ]
            self.assertEqual(found, names, kind)
            for name in names:
                size = (
                    (
                        ADDON
                        / "sonidos"
                        / next(s for s in paths.SOUND_SUBFOLDERS[kind] if (ADDON / "sonidos" / s / name).exists())
                        / name
                    )
                    .stat()
                    .st_size
                )
                self.assertLess(size, 60_000, name)

    def test_bundled_labels(self) -> None:
        from profeedback import audio

        with mock.patch.object(
            audio,
            "sound_files",
            return_value={
                "mazo-1-madera.mp3": paths.BUNDLED_SOUNDS_DIR / "finalizado/mazo/mazo-1-madera.mp3",
                "perfecto-mazo-2-campanilla.mp3": paths.BUNDLED_SOUNDS_DIR
                / "perfecto-mazo/perfecto-mazo-2-campanilla.mp3",
                "mio.mp3": paths.USER_SOUNDS_DIR / "finalizado/mazo/mio.mp3",
            },
        ):
            label = lambda voice: voice.capitalize()  # noqa: E731
            self.assertEqual(audio.sound_label("deck_finish", "mazo-1-madera.mp3", label), "1 · Madera")
            self.assertEqual(
                audio.sound_label("deck_finish", "perfecto-mazo-2-campanilla.mp3", label), "2 · Campanilla"
            )
            self.assertEqual(audio.sound_label("deck_finish", "mio.mp3", label), "mio")

    def test_texts_and_badges_in_every_language(self) -> None:
        from profeedback import strings

        with mock.patch.object(strings, "current_lang", return_value="es"):
            self.assertEqual(strings.ui("label_on_again"), "Al pulsar «Otra vez»")
            self.assertEqual(strings.flag_label("hard_exercise"), "SE RESISTE")
            self.assertEqual(strings.flag_label("previous_mistake"), "OTRA OPORTUNIDAD")
        for lang, texts in strings._FLAG_STRINGS.items():
            self.assertNotIn("EJERCICIO", texts["hard_exercise"], lang)
            self.assertTrue(texts["hard_exercise"] and texts["previous_mistake"], lang)


class ButtonStyleTests(unittest.TestCase):
    """2.5.0: mismos colores de cara; forma, letra y grises según el informe 2.4.0 (FIX-006 sigue)."""

    def setUp(self) -> None:
        self.css = (ADDON / "web" / "buttons.css").read_text(encoding="utf-8")
        self.flags = (ADDON / "web" / "flags.css").read_text(encoding="utf-8")
        self.js = (ADDON / "web" / "buttons.js").read_text(encoding="utf-8")

    def test_shape_wins_over_the_theme(self) -> None:
        for declaration in (
            "border-radius: var(--profeedback-radius) !important",
            "background-image: none !important",
            "height: 50px !important",
            "min-width: 130px !important",
        ):
            self.assertIn(declaration, self.css)
        self.assertIn("--profeedback-radius: 16px;", self.css)
        self.assertIn("--profeedback-lip: 4px;", self.css)

    def test_face_colours_unchanged_and_readable_text(self) -> None:
        for value in ("255, 75, 75", "255, 171, 51", "147, 211, 51", "73, 192, 248", "#ffd700"):
            self.assertIn(value, self.css)
        self.assertIn("#5c3700", self.css)
        self.assertNotIn("#ae6802", self.css.split("#ansbut {", 1)[1].split("}", 1)[0])
        self.assertNotIn("#52656d", self.css)
        self.assertIn("var(--fg-subtle, #B7BECC)", self.css)

    def test_good_is_as_wide_as_show_answer(self) -> None:
        good = self.css.split("/* Bien: verde", 1)[1].split("}", 1)[0]
        self.assertIn("min-width: 190px !important", good)
        self.assertIn("min-width: 190px !important", self.css.split("#ansbut {", 1)[1].split("}", 1)[0])

    def test_hover_only_brightens_and_focus_ring_is_apart(self) -> None:
        hover = self.css.split("button:hover {", 1)[1].split("}", 1)[0]
        self.assertIn("filter: var(--profeedback-hover)", hover)
        self.assertNotIn("background", hover)
        self.assertIn("outline-offset: 2px !important", self.css)

    def test_answer_on_release_without_delay(self) -> None:
        self.assertNotIn("setTimeout(function () {\n          button.classList.remove", self.js)
        self.assertNotIn("DELAY", self.js)

    def test_badges(self) -> None:
        for modifier, icon, day in (
            ("new-card", "#ce82ff", "#8f3bd9"),
            ("hard-exercise", "#ff4b4b", "#c92c2c"),
            ("previous-mistake", "#ffab33", "#9e5a00"),
        ):
            self.assertIn(icon, self.flags.split(f".profeedback-badge--{modifier} svg {{", 1)[1].split("}", 1)[0])
            self.assertIn(day, self.flags.split(f".profeedback-badge--{modifier} {{", 1)[1].split("}", 1)[0])
        self.assertIn("height: 24px;", self.flags)
        self.assertIn("margin: 0 0 16px;", self.flags)
        self.assertIn("120ms", self.flags)

    def test_confetti_lasts_four_seconds_and_one_shine(self) -> None:
        confetti = (ADDON / "web" / "confetti.js").read_text(encoding="utf-8")
        self.assertIn("var RAIN_MS = 4000;", confetti)
        self.assertIn("var BURST_MS = 2500;", confetti)
        self.assertIn("ease-in-out 1}", confetti)


class ConfigFromPageTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        values = dialogs.page(AddonConfig(), SOUNDS)["values"]
        values.update(answerSound="mio.mp3", wrongSound="-", soundVolume=40, confettiEnabled=False)
        cfg = dialogs.config_from_page(values, AddonConfig(), SOUNDS)
        self.assertEqual(cfg.answerSound, "mio.mp3")
        self.assertEqual(cfg.wrongSound, "-")
        self.assertEqual(cfg.soundVolume, 40)
        self.assertFalse(cfg.confettiEnabled)

    def test_unknown_sound_becomes_random(self) -> None:
        # Regla de FIX-001: un valor que no está en la lista se guarda como «Aleatorio».
        cfg = dialogs.config_from_page({"answerSound": "nope.mp3", "soundVolume": 500}, AddonConfig(), SOUNDS)
        self.assertEqual(cfg.answerSound, "")
        self.assertEqual(cfg.soundVolume, 100)

    def test_test_and_folder_requests(self) -> None:
        values = {"answerSound": "mio.mp3", "soundVolume": 30}
        self.assertEqual(
            dialogs.test_request({"name": "correct", "values": values}, SOUNDS), ("correct", "mio.mp3", 30)
        )
        self.assertIsNone(dialogs.test_request({"name": "correct", "values": {"answerSound": "-"}}, SOUNDS))
        self.assertIsNone(dialogs.test_request({"name": "nope", "values": values}, SOUNDS))
        self.assertIsNone(dialogs.test_request(None, SOUNDS))
        self.assertEqual(dialogs.folder_request({"name": "open:wrong"}), "wrong")
        self.assertIsNone(dialogs.folder_request({"name": "open:nope"}))


class UserFoldersTests(unittest.TestCase):
    # FIX-004: las subcarpetas de sonidos propios se crean vacías.
    def test_folders_are_created(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sonidos"
            with mock.patch.object(paths, "USER_SOUNDS_DIR", root):
                paths.ensure_user_sound_folders()
                paths.ensure_user_sound_folders()
            for subfolders in paths.SOUND_SUBFOLDERS.values():
                for subfolder in subfolders:
                    self.assertTrue((root / subfolder).is_dir(), subfolder)


class PanelFilesTests(unittest.TestCase):
    def test_kit_carries_the_package_prefix(self) -> None:
        for name in ("web/panel.css", "web/panel.js", "panel.py"):
            text = (ADDON / name).read_text(encoding="utf-8")
            self.assertNotIn("__P__", text)
            self.assertNotIn("__J__", text)
        self.assertIn("var ProfeedbackPanel", (ADDON / "web/panel.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
