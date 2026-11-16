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

SoundKind = Literal["correct", "wrong", "deck_finish", "all_finish"]

# Subcarpetas de cada tipo de sonido. Se mantienen los nombres en español de las
# versiones anteriores para no obligar a nadie a mover sus archivos. Desde la 2.5.0 no hay
# celebración «perfecta» (informe 2.4.0, opción B): los sonidos de «perfecto-mazo» y
# «perfecto-todo» son variantes más de los dos finales.
SOUND_SUBFOLDERS: Final[dict[SoundKind, tuple[str, ...]]] = {
    "correct": ("correcto",),
    "wrong": ("fallo",),
    "deck_finish": ("finalizado/mazo", "perfecto-mazo"),
    "all_finish": ("finalizado/todo", "perfecto-todo"),
}


# --- FIX-004 (2026-11-09) ---
# Síntoma: un .mp3 copiado en «user_files/sonidos», como decía la nota de la ventana de
#          ajustes, no aparecía en ningún desplegable y no sonaba nunca.
# Causa: el complemento solo busca en una subcarpeta por tipo de sonido, que no venían
#        creadas, y la nota no las nombraba.
# Regla: las subcarpetas de sonidos propios se crean vacías al abrir los ajustes, y la ventana
#        lleva a la de cada tipo (desde la 2.5.0, «Abrir la carpeta de estos sonidos…» en cada
#        lista sustituye a la nota, como pidió el informe 2.4.0 aprobado por la persona).
def ensure_user_sound_folders() -> None:
    """Crea, si faltan, las subcarpetas de sonidos propios (una por tipo)."""
    for subfolders in SOUND_SUBFOLDERS.values():
        for subfolder in subfolders:
            (USER_SOUNDS_DIR / subfolder).mkdir(parents=True, exist_ok=True)


def user_sound_folder(kind: SoundKind) -> Path:
    """Carpeta propia principal de un tipo de sonido (la que abre «Abrir la carpeta…»)."""
    return USER_SOUNDS_DIR / SOUND_SUBFOLDERS[kind][0]
