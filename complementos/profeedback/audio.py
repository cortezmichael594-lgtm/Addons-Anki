"""Reproducción de los sonidos de acierto y de fin de repaso.

Se usa un reproductor de Qt propio (un canal por tipo de sonido) y no el de Anki, porque el de
Anki tiene una sola cola y la corta cada vez que aparece una tarjeta con audio: el sonido de
acierto se oiría a medias. Si esta instalación no trae el módulo de multimedia de Qt, se
recurre al reproductor de Anki, que siempre está.
"""

from __future__ import annotations

import importlib
import random
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aqt import mw
from aqt.qt import QUrl, qconnect

from . import paths
from .errors import log_error
from .paths import SoundKind

_EXTENSION = ".mp3"
# Valor de las listas para «Sin sonido» (2.5.0): ningún archivo puede llamarse así.
OFF = "-"
# Nombre de los sonidos de serie desde la 2.5.0: «acierto-1-madera.mp3».
_BUNDLED_NAME = re.compile(r"-(\d+)-([a-z]+)\.mp3$")

# Clases de Qt Multimedia (reproductor y salida de audio) y si ya se intentó cargarlas.
_multimedia: tuple[Any, Any] | None = None
_multimedia_tried: bool = False
_channels: dict[SoundKind, _Channel] = {}
# Archivos de cada tipo, leídos del disco una vez (véase refresh()).
_listing: dict[SoundKind, dict[str, Path]] = {}
# Volumen, de 0 a 100, que se aplica a todos los canales.
_volume: int = 100


def _load_multimedia() -> tuple[Any, Any] | None:
    """Clases de audio de Qt, o None si esta instalación no las trae."""
    global _multimedia, _multimedia_tried
    if not _multimedia_tried:
        _multimedia_tried = True
        try:
            # aqt.qt no reexporta QtMultimedia: el propio Anki 26.09.3 lo carga
            # directamente en aqt/sound.py. Se carga el mismo módulo de la misma
            # instalación de Qt de Anki, por su nombre, porque no hay otra vía.
            module = importlib.import_module("PyQt6.QtMultimedia")
            _multimedia = (module.QMediaPlayer, module.QAudioOutput)
        except Exception as error:
            # Algunas instalaciones de Linux traen PyQt6 sin el módulo de multimedia.
            log_error("audio.multimedia", error)
    return _multimedia


@dataclass(slots=True)
class _Channel:
    """Un reproductor por tipo de sonido, para que cada uno tenga el suyo ya preparado."""

    player: Any
    output: Any
    path: Path | None = None
    # La persona eligió un archivo concreto: no se cambia al terminar de sonar.
    fixed: bool = False


# ── archivos disponibles ─────────────────────────────────────────────────────
def refresh() -> None:
    """Olvida la lista de archivos para volver a leerla (nuevo perfil o ajustes guardados)."""
    _listing.clear()


def _mp3_in(folder: Path) -> list[Path]:
    try:
        items = [item for item in folder.iterdir() if item.suffix.lower() == _EXTENSION and item.is_file()]
    except OSError:
        return []  # la carpeta no existe: ese origen no aporta nada
    return sorted(items, key=lambda item: item.name.lower())


def sound_files(kind: SoundKind) -> dict[str, Path]:
    """Nombre y ruta de los .mp3 disponibles, en el orden de la lista: primero los de serie
    (por carpeta y nombre) y después los de la persona. Uno propio con el mismo nombre que
    uno de serie lo sustituye."""
    cached = _listing.get(kind)
    if cached is not None:
        return cached
    found: dict[str, Path] = {}
    for root in (paths.BUNDLED_SOUNDS_DIR, paths.USER_SOUNDS_DIR):
        for subfolder in paths.SOUND_SUBFOLDERS[kind]:
            for item in _mp3_in(root / subfolder):
                found[item.name] = item
    _listing[kind] = found
    return found


def list_sound_names(kind: SoundKind) -> list[str]:
    """Nombres de archivo disponibles, en el orden en que salen en la lista."""
    return list(sound_files(kind))


def sound_label(kind: SoundKind, name: str, voice_label: Callable[[str], str]) -> str:
    """Lo que se lee en la lista: «1 · Madera» para los de serie (numerados en su lista) y
    el nombre sin «.mp3» para los propios (2.5.0, informe 2.4.0, apartado 8.7)."""
    files = sound_files(kind)
    path = files.get(name)
    match = _BUNDLED_NAME.search(name)
    if path is not None and match and path.is_relative_to(paths.BUNDLED_SOUNDS_DIR):
        bundled = [key for key, value in files.items() if value.is_relative_to(paths.BUNDLED_SOUNDS_DIR)]
        return f"{bundled.index(name) + 1} · {voice_label(match.group(2))}"
    return name[: -len(_EXTENSION)] if name.lower().endswith(_EXTENSION) else name


def has_sounds(kind: SoundKind) -> bool:
    return bool(sound_files(kind))


def _choose(kind: SoundKind, name: str, avoid: Path | None = None) -> Path | None:
    """El archivo elegido por su nombre; con «Aleatorio» (nombre vacío), uno al azar; y si el
    elegido ya no existe, el primero de la lista (2.5.0)."""
    files = sound_files(kind)
    if name == OFF:
        return None
    if name and name in files:
        return files[name]
    if name and files:
        return next(iter(files.values()))
    candidates = [path for path in files.values() if path != avoid] or list(files.values())
    return random.choice(candidates) if candidates else None


# ── canales de Qt ────────────────────────────────────────────────────────────
def _linear(percent: int) -> float:
    """De porcentaje del control a volumen de Qt.

    El oído no percibe el volumen de forma lineal: con el cuadrado, la mitad del control
    suena como «la mitad» y no casi igual de fuerte.
    """
    return (max(0, min(100, percent)) / 100) ** 2


def _channel(kind: SoundKind) -> _Channel | None:
    channel = _channels.get(kind)
    if channel is not None:
        return channel
    classes = _load_multimedia()
    if classes is None or mw is None:
        return None
    player_class, output_class = classes
    try:
        player = player_class(mw)
        output = output_class(mw)
        player.setAudioOutput(output)
        output.setVolume(_linear(_volume))
        channel = _Channel(player, output)
        _channels[kind] = channel
        qconnect(
            player.mediaStatusChanged,
            lambda status, key=kind: _on_status_changed(key, status),
        )
        qconnect(
            player.errorOccurred,
            lambda _error, text, key=kind: log_error(
                f"audio.player[{key}]", RuntimeError(text)
            ),
        )
        return channel
    except Exception as error:
        log_error("audio._channel", error)
        return None


def _set_source(channel: _Channel, path: Path) -> None:
    channel.player.setSource(QUrl.fromLocalFile(str(path)))
    channel.path = path


def _prepare(kind: SoundKind, channel: _Channel, name: str) -> bool:
    """Deja en el canal el archivo que toca. Devuelve False si no hay ninguno."""
    channel.fixed = bool(name)
    current = channel.path
    if not name and current is not None and current in sound_files(kind).values():
        return True  # al azar, y ya hay uno preparado
    path = _choose(kind, name)
    if path is None:
        return False
    if path != current:
        _set_source(channel, path)
    return True


def _on_status_changed(kind: SoundKind, status: object) -> None:
    """Al terminar un sonido al azar, deja otro distinto preparado para la próxima vez."""
    try:
        classes = _load_multimedia()
        channel = _channels.get(kind)
        if classes is None or channel is None or channel.fixed:
            return
        if status != classes[0].MediaStatus.EndOfMedia:
            return
        path = _choose(kind, "", avoid=channel.path)
        if path is not None:
            _set_source(channel, path)
    except Exception as error:
        log_error("audio._on_status_changed", error)


# ── interfaz pública ─────────────────────────────────────────────────────────
def set_volume(percent: int) -> None:
    """Fija el volumen (0 a 100) de todos los sonidos."""
    global _volume
    _volume = max(0, min(100, percent))
    for channel in _channels.values():
        try:
            channel.output.setVolume(_linear(_volume))
        except Exception as error:
            log_error("audio.set_volume", error)


def preload(kind: SoundKind, name: str = "") -> None:
    """Deja un sonido cargado y listo.

    Abrir el archivo es la parte lenta; hacerlo ahora, lejos de cualquier clic, es lo que
    hace que luego suene en el acto.
    """
    try:
        channel = _channel(kind)
        if channel is not None:
            _prepare(kind, channel, name)
    except Exception as error:
        log_error("audio.preload", error)


def play(kind: SoundKind, name: str = "", volume: int | None = None) -> bool:
    """Reproduce el sonido elegido; con «Aleatorio», uno al azar; con «Sin sonido», nada.

    `volume` permite probar un sonido con el volumen que la persona está ajustando aún
    sin haberlo guardado. Devuelve False si no se pudo empezar a reproducir (para que
    «Probar» lo diga).
    """
    if name == OFF:
        return True
    try:
        if volume is not None:
            set_volume(volume)
        channel = _channel(kind)
        if channel is None:
            path = _choose(kind, name)
            if path is None:
                return False
            _play_with_anki(path)
            return True
        if not _prepare(kind, channel, name):
            return False
        channel.player.setPosition(0)
        channel.player.play()
        return True
    except Exception as error:
        log_error("audio.play", error)
        return False


def _play_with_anki(path: Path) -> None:
    from aqt.sound import av_player

    av_player.play_file(str(path))


def dispose() -> None:
    """Detiene y suelta los reproductores (al cambiar de perfil o salir).

    Además de parar el sonido, entrega cada reproductor a Qt para que lo destruya; sin esto,
    tras muchos cambios de perfil se iría acumulando un reproductor muerto tras otro.
    """
    for channel in list(_channels.values()):
        try:
            channel.player.stop()
            channel.player.deleteLater()
            channel.output.deleteLater()
        except Exception as error:
            log_error("audio.dispose", error)
    _channels.clear()
