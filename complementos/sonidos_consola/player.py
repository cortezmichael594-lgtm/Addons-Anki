"""Reproductor de los siete sonidos.

Cada sonido tiene un único «altavoz» (QSoundEffect) cargado de antemano: suena al momento,
no espera al disco y, si vuelve a sonar, corta el anterior en lugar de amontonarse. No usa
el reproductor de las tarjetas de Anki, así que nunca interrumpe su audio.

QSoundEffect está en PyQt6.QtMultimedia, que aqt.qt no reexporta; Anki la trae y la usa él
mismo para grabar la voz (aqt/sound.py). Es la excepción aprobada por la persona el 2026-11-13.
"""

from __future__ import annotations

from pathlib import Path

from aqt import mw
from aqt.addons import AddonManager
from aqt.qt import QElapsedTimer, QUrl, qconnect

from . import config, logic

try:
    from PyQt6.QtMultimedia import QSoundEffect
except ImportError:  # Una instalación de Anki sin la parte de sonido de Qt.
    QSoundEffect = None  # type: ignore[assignment,misc]

SOUNDS_DIR = Path(__file__).parent / "user_files"


def audio_available() -> bool:
    return QSoundEffect is not None


def present_files() -> set[str]:
    """Nombres de los archivos de sonido que hay en la carpeta de sonidos."""
    if not SOUNDS_DIR.is_dir():
        return set()
    return {path.name for path in SOUNDS_DIR.iterdir() if path.is_file()}


class SoundBank:
    def __init__(self) -> None:
        self._effects: dict[str, QSoundEffect] = {}
        self._loaded_mtimes: dict[str, float] = {}
        self._pending: set[str] = set()
        self._gate = logic.SoundGate()
        self._clock = QElapsedTimer()
        self._clock.start()

    def reload(self) -> None:
        """Carga los archivos nuevos o cambiados; olvida los que ya no están."""
        if QSoundEffect is None:
            return
        for key, file_name in logic.SOUND_FILES.items():
            path = SOUNDS_DIR / file_name
            try:
                mtime = path.stat().st_mtime if path.is_file() else None
            except OSError:
                mtime = None
            if mtime is None:
                self._drop(key)
                continue
            loaded = self._effects.get(key)
            if (
                loaded is not None
                and self._loaded_mtimes.get(key) == mtime
                and loaded.status() != QSoundEffect.Status.Error
            ):
                continue  # Ya cargado y sin fallo; uno que falló se vuelve a intentar.
            self._drop(key)
            effect = QSoundEffect(mw)
            qconnect(effect.statusChanged, lambda k=key: self._on_status(k))
            effect.setSource(QUrl.fromLocalFile(str(path)))
            self._effects[key] = effect
            self._loaded_mtimes[key] = mtime

    def _drop(self, key: str) -> None:
        effect = self._effects.pop(key, None)
        self._loaded_mtimes.pop(key, None)
        self._pending.discard(key)
        if effect is not None:
            effect.stop()
            effect.deleteLater()

    def _on_status(self, key: str) -> None:
        effect = self._effects.get(key)
        if effect is None or QSoundEffect is None:
            return
        status = effect.status()
        if status == QSoundEffect.Status.Error:
            self._pending.discard(key)
            AddonManager.get_logger(__name__).warning("No se pudo cargar %s", logic.SOUND_FILES[key])
        elif status == QSoundEffect.Status.Ready and key in self._pending:
            self._pending.discard(key)
            self._start(key, effect)

    def play(self, key: str, *, ignore_switch: bool = False, volume: int | None = None) -> None:
        """Hace sonar «key» si está encendido, su archivo existe y no pisa a otro sonido.

        ignore_switch y volume sirven al botón «Probar» de la ventana, que suena aunque la
        casilla esté desmarcada y con el volumen que marca la barra en ese momento.
        """
        settings = config.load()
        if not ignore_switch and not settings["enabled"].get(key, False):
            return
        effect = self._effects.get(key)
        if effect is None:
            return
        if not ignore_switch and not self._gate.allow(key, self._clock.elapsed()):
            return
        for other in logic.sounds_to_stop(key):
            other_effect = self._effects.get(other)
            if other_effect is not None:
                other_effect.stop()
            self._pending.discard(other)
        effect.setVolume(logic.linear_volume(settings["volume"] if volume is None else volume))
        if QSoundEffect is not None and effect.status() == QSoundEffect.Status.Ready:
            self._start(key, effect)
        else:
            # Aún se está cargando (por ejemplo, el de arranque): suena en cuanto esté listo.
            self._pending.add(key)

    def _start(self, key: str, effect: QSoundEffect) -> None:
        effect.stop()
        effect.play()

    def stop_all(self) -> None:
        self._pending.clear()
        for effect in self._effects.values():
            effect.stop()


bank = SoundBank()
