"""Rutas del complemento (siempre con pathlib, nunca con rutas escritas a mano).

Anki borra la carpeta del complemento al instalar una versión nueva, salvo `user_files`: ahí
es donde la persona puede dejar sus sonidos y su tipografía para no perderlos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

ADDON_ROOT: Final[Path] = Path(__file__).resolve().parent
USER_FILES_DIR: Final[Path] = ADDON_ROOT / "user_files"
WEB_DIR: Final[Path] = ADDON_ROOT / "web"

# Carpeta de sonidos que trae el complemento y carpeta (opcional) de la persona.
BUNDLED_SOUNDS_DIR: Final[Path] = ADDON_ROOT / "sonidos"
USER_SOUNDS_DIR: Final[Path] = USER_FILES_DIR / "sonidos"

SoundKind = Literal["correct", "deck_finish", "all_finish", "deck_perfect", "all_perfect"]

# Subcarpeta de cada tipo de sonido. Se mantienen los nombres en español de las
# versiones anteriores para no obligar a nadie a mover sus archivos.
SOUND_SUBFOLDERS: Final[dict[SoundKind, str]] = {
    "correct": "correcto",
    "deck_finish": "finalizado/mazo",
    "all_finish": "finalizado/todo",
    "deck_perfect": "perfecto-mazo",
    "all_perfect": "perfecto-todo",
}
