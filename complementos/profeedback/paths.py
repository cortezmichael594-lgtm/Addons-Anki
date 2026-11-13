"""Rutas del complemento (siempre con pathlib, nunca con rutas escritas a mano).

Anki borra la carpeta del complemento al instalar una versión nueva, salvo `user_files`: ahí
es donde la persona puede dejar sus sonidos y su tipografía para no perderlos.
"""

# Historial de correcciones de este archivo:
# FIX-004 (2026-11-09): un sonido propio copiado donde decía la nota no aparecía nunca.

from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

ADDON_ROOT: Final[Path] = Path(__file__).resolve().parent
USER_FILES_DIR: Final[Path] = ADDON_ROOT / "user_files"
WEB_DIR: Final[Path] = ADDON_ROOT / "web"

# Carpeta de sonidos que trae el complemento y carpeta (opcional) de la persona.
BUNDLED_SOUNDS_DIR: Final[Path] = ADDON_ROOT / "sonidos"
USER_SOUNDS_DIR: Final[Path] = USER_FILES_DIR / "sonidos"

SoundKind = Literal["correct", "wrong", "deck_finish", "all_finish", "deck_perfect", "all_perfect"]

# Subcarpeta de cada tipo de sonido. Se mantienen los nombres en español de las
# versiones anteriores para no obligar a nadie a mover sus archivos.
SOUND_SUBFOLDERS: Final[dict[SoundKind, str]] = {
    "correct": "correcto",
    "wrong": "fallo",
    "deck_finish": "finalizado/mazo",
    "all_finish": "finalizado/todo",
    "deck_perfect": "perfecto-mazo",
    "all_perfect": "perfecto-todo",
}


# --- FIX-004 (2026-11-09) ---
# Síntoma: un .mp3 copiado en «user_files/sonidos», como decía la nota de la ventana de
#          ajustes, no aparecía en ningún desplegable y no sonaba nunca.
# Causa: el complemento solo busca en una subcarpeta por tipo de sonido, que no venían
#        creadas, y la nota no las nombraba.
# Regla: las subcarpetas de sonidos propios se crean vacías al abrir los ajustes, y la nota
#        dice que cada sonido va en la suya.
def ensure_user_sound_folders() -> None:
    """Crea, si faltan, las subcarpetas de sonidos propios (una por tipo)."""
    for subfolder in SOUND_SUBFOLDERS.values():
        (USER_SOUNDS_DIR / subfolder).mkdir(parents=True, exist_ok=True)
