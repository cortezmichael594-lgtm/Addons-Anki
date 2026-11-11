"""Lo que ocurre cuando la persona pulsa algo, y los avisos de abrir y cerrar perfil.

Todo lo que Anki llama por nuestra cuenta va envuelto con @guarded: un fallo nunca abre la
ventana de errores de Anki ni deja el complemento a medias.
"""

from __future__ import annotations

from typing import Any

from aqt import mw

from . import audio, celebration, config, dialogs, feedback, paths
from .errors import guarded, log_error
from .paths import SoundKind


# Se conserva una referencia mientras la ventana existe: sin ella Python podría destruirla
# y la ventana desaparecería sola.
_dialog: Any = None


@guarded
def open_settings() -> None:
    """Abre la ventana de ajustes del complemento.

    Se registra con setConfigAction y debe devolver None: si devolviera False, Anki abriría
    en su lugar el editor de JSON, que para esta persona también es código.
    """
    global _dialog
    if mw is None:
        return
    if _dialog is not None and _dialog.isVisible():
        _dialog.raise_()
        _dialog.activateWindow()
        return
    from .panel import PanelDialog, parent_window

    # Las carpetas de sonidos propios, a la vista desde el primer día (FIX-004).
    paths.ensure_user_sound_folders()
    # Por si la persona ha dejado sonidos nuevos en user_files desde la última vez.
    audio.refresh()
    sounds: dict[SoundKind, list[str]] = {
        kind: audio.list_sound_names(kind) for kind in paths.SOUND_SUBFOLDERS
    }

    def handle(action: str, arg: Any) -> Any:
        if action == "action":
            request = dialogs.test_request(arg, sounds)
            if request is not None:
                audio.play(*request)
            return None
        if action == "accept":
            config.save(dialogs.config_from_page(arg, config.get(), sounds))
            feedback.reset()
        if action in ("accept", "cancel"):
            # «Probar» deja puesto el volumen del deslizador aunque se cancele: se vuelve
            # al guardado.
            audio.set_volume(config.get().soundVolume)
        return None

    package = mw.addonManager.addon_from_module(__name__)
    _dialog = PanelDialog(
        parent_window(),
        package,
        dialogs.page(config.get(), sounds),
        handle,
        lambda where, error: log_error(where, error),
        dialogs.GEOMETRY_KEY,
    )
    _dialog.open()


@guarded
def on_profile_open() -> None:
    """Perfil recién abierto: ya hay colección, se puede preparar todo."""
    feedback.reset()
    celebration.reset()


@guarded
def on_profile_close() -> None:
    celebration.reset()
    audio.dispose()
