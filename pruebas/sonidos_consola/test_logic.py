"""Pruebas de las reglas de los sonidos (sin Anki ni Qt)."""

from __future__ import annotations

import unittest

from sonidos_consola import logic


class NormalizeConfigTest(unittest.TestCase):
    def test_first_run_gives_defaults(self) -> None:
        self.assertEqual(logic.normalize_config(None), logic.default_config())

    def test_all_eight_sounds_on_by_default(self) -> None:
        enabled = logic.default_config()["enabled"]
        self.assertEqual(set(enabled), set(logic.SOUND_FILES))
        self.assertTrue(all(enabled.values()))

    def test_volume_is_clamped_and_rounded(self) -> None:
        self.assertEqual(logic.normalize_config({"volume": 250})["volume"], 100)
        self.assertEqual(logic.normalize_config({"volume": -3})["volume"], 0)
        self.assertEqual(logic.normalize_config({"volume": 42.6})["volume"], 43)

    def test_wrong_types_fall_back(self) -> None:
        config = logic.normalize_config({"volume": True, "navigation": "fast", "enabled": {"cancel": "no"}})
        self.assertEqual(config, logic.default_config())

    def test_old_config_without_a_sound_keeps_it_on(self) -> None:
        config = logic.normalize_config({"enabled": {"option": False}})
        self.assertFalse(config["enabled"]["option"])
        self.assertTrue(config["enabled"]["coldboot"])

    def test_unknown_keys_are_dropped(self) -> None:
        config = logic.normalize_config({"other": 1, "enabled": {"trophy": True}})
        self.assertEqual(config, logic.default_config())

    def test_navigation_modes(self) -> None:
        self.assertEqual(logic.NAV_MODES, ("hover", "click"))
        for mode in logic.NAV_MODES:
            self.assertEqual(logic.normalize_config({"navigation": mode})["navigation"], mode)

    def test_old_never_becomes_navigation_switched_off(self) -> None:
        config = logic.normalize_config({"navigation": "off", "enabled": {"option": True}})
        self.assertEqual(config["navigation"], "hover")
        self.assertFalse(config["enabled"]["option"])
        self.assertTrue(config["enabled"]["cancel"])


class VolumeTest(unittest.TestCase):
    def test_ends(self) -> None:
        self.assertEqual(logic.linear_volume(0), 0.0)
        self.assertEqual(logic.linear_volume(100), 1.0)

    def test_curve_is_perceptual_and_clamped(self) -> None:
        self.assertAlmostEqual(logic.linear_volume(50), 0.25)
        self.assertEqual(logic.linear_volume(150), 1.0)
        self.assertEqual(logic.linear_volume(-5), 0.0)


class SoundGateTest(unittest.TestCase):
    def test_fast_navigation_is_throttled(self) -> None:
        gate = logic.SoundGate()
        self.assertTrue(gate.allow("option", 1000))
        self.assertFalse(gate.allow("option", 1000 + logic.OPTION_MIN_GAP_MS - 1))
        self.assertTrue(gate.allow("option", 1000 + logic.OPTION_MIN_GAP_MS))

    def test_navigation_does_not_cover_a_priority_sound(self) -> None:
        gate = logic.SoundGate()
        self.assertTrue(gate.allow("cancel", 1000))
        self.assertFalse(gate.allow("option", 1000 + logic.PRIORITY_QUIET_MS - 1))
        self.assertTrue(gate.allow("option", 1000 + logic.PRIORITY_QUIET_MS))

    def test_duplicate_priority_sound_plays_once(self) -> None:
        gate = logic.SoundGate()
        self.assertTrue(gate.allow("cancel", 1000))
        self.assertFalse(gate.allow("cancel", 1000 + logic.DUPLICATE_GAP_MS - 1))
        self.assertTrue(gate.allow("cancel", 1000 + logic.DUPLICATE_GAP_MS))

    def test_different_sounds_do_not_block_each_other(self) -> None:
        gate = logic.SoundGate()
        self.assertTrue(gate.allow("gameboot", 1000))
        self.assertTrue(gate.allow("system_ok", 1001))
        self.assertTrue(gate.allow("error", 1002))

    def test_rejected_sound_does_not_count_as_played(self) -> None:
        gate = logic.SoundGate()
        gate.allow("option", 1000)
        gate.allow("option", 1030)  # rechazado
        self.assertTrue(gate.allow("option", 1000 + logic.OPTION_MIN_GAP_MS))


class StopAndFilesTest(unittest.TestCase):
    def test_priority_sounds_silence_navigation_and_balloon(self) -> None:
        for key in ("cancel", "error", "system_ok", "system_ng", "trophy"):
            self.assertEqual(set(logic.sounds_to_stop(key)), {"option", "gameboot"})

    def test_other_sounds_silence_nothing(self) -> None:
        for key in ("option", "gameboot", "coldboot"):
            self.assertEqual(logic.sounds_to_stop(key), ())

    def test_only_the_eight_given_files(self) -> None:
        self.assertEqual(
            set(logic.SOUND_FILES.values()),
            {
                "coldboot_stereo.wav",
                "gameboot_stereo.wav",
                "snd_cancel.wav",
                "snd_error.wav",
                "snd_option.wav",
                "snd_system_ng.wav",
                "snd_system_ok.wav",
                "snd_trophy.wav",
            },
        )

    def test_missing_files_in_window_order(self) -> None:
        self.assertEqual(
            logic.missing_files({"snd_option.wav", "coldboot_stereo.wav", "otro.wav"}),
            [
                "gameboot_stereo.wav",
                "snd_cancel.wav",
                "snd_system_ok.wav",
                "snd_system_ng.wav",
                "snd_trophy.wav",
                "snd_error.wav",
            ],
        )
        self.assertEqual(logic.missing_files(set(logic.SOUND_FILES.values())), [])
