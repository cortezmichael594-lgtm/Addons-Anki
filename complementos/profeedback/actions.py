"""Lo que ocurre cuando la persona pulsa algo, y los avisos de abrir y cerrar perfil.

Todo lo que Anki llama por nuestra cuenta va envuelto con @guarded: un fallo nunca abre la
ventana de errores de Anki ni deja el complemento a medias.
"""

from __future__ import annotations

from aqt import mw

from . import audio, celebration, config, dialogs, feedback, paths
from .errors import guarded
from .paths import SoundKind


@guarded
def open_settings() -> None:
    """Abre la ventana de ajustes del complemento.

    Se registra con setConfigAction y debe devolver None: si devolviera False, Anki abriría
    en su lugar el editor de JSON, que para esta persona también es código.
    """
    if mw is None:
        return
    # Por si la persona ha dejado sonidos nuevos en user_files desde la última vez.
    audio.refresh()
    sounds: dict[SoundKind, list[str]] = {
        kind: audio.list_sound_names(kind) for kind in paths.SOUND_SUBFOLDERS
    }
    dialog = dialogs.SettingsDialog(mw, config.get(), sounds, _test_sound)
    if dialog.exec():
        config.save(dialog.values())
        feedback.reset()
    # «Probar» deja puesto el volumen del deslizador aunque se cancele: se vuelve al guardado.
    audio.set_volume(config.get().soundVolume)


def _test_sound(kind: SoundKind, name: str, volume: int) -> None:
    audio.play(kind, name, volume)


@guarded
def on_profile_open() -> None:
    """Perfil recién abierto: ya hay colección, se puede preparar todo."""
    feedback.reset()
    celebration.reset()


@guarded
def on_profile_close() -> None:
    celebration.reset()
    audio.dispose()
