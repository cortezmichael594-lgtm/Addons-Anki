"""Combinaciones de teclas que Anki ya tiene ocupadas.

La lista se saco leyendo el codigo del propio Anki 25.09: los menus generados
de sus ventanas, los atajos que registra en el navegador de tarjetas, el
repaso y la pantalla de plantillas, y los del editor de notas, que viven en su
parte web. Va agrupada por procedencia para que se pueda revisar y ampliar.

Regla: si Anki anade un atajo nuevo en una version futura, se anade aqui, en el
grupo que le corresponda. Nunca se quita uno sin comprobar antes en el codigo
de Anki que de verdad ya no lo usa.

Ademas de esta lista fija se miran en vivo los atajos que la ventana principal
tenga puestos en ese momento, de modo que tambien se detectan los que hayan
anadido otros complementos.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-28) — El atajo por defecto era uno que Anki ya usaba.
#   Parte de este archivo: la lista contra la que ahora se comprueba todo
#   atajo, y que impide volver a elegir uno ocupado. Regla completa en
#   constants.py.

from __future__ import annotations

from functools import lru_cache

from aqt import mw
from aqt.qt import QAction, QKeySequence

# Menus de la ventana principal y de los dialogos de Anki.
_MENUS: tuple[str, ...] = (
    "Ctrl+0", "Ctrl+1", "Ctrl+2", "Ctrl+3", "Ctrl+4", "Ctrl+5", "Ctrl+6", "Ctrl+7",
    "Ctrl+D", "Ctrl+E", "Ctrl+F", "Ctrl+G", "Ctrl+J", "Ctrl+K", "Ctrl+N", "Ctrl+P",
    "Ctrl+Q", "Ctrl+W", "Ctrl+Z", "Ctrl+Del", "Ctrl+Delete", "Ctrl+Backspace",
    "Ctrl+Alt+A", "Ctrl+Alt+E", "Ctrl+Alt+F", "Ctrl+Alt+N", "Ctrl+Alt+S",
    "Ctrl+Alt+T", "Ctrl+Alt+Shift+A",
    "Ctrl+Shift+A", "Ctrl+Shift+D", "Ctrl+Shift+E", "Ctrl+Shift+F", "Ctrl+Shift+G",
    "Ctrl+Shift+I", "Ctrl+Shift+J", "Ctrl+Shift+L", "Ctrl+Shift+M", "Ctrl+Shift+N",
    "Ctrl+Shift+P", "Ctrl+Shift+R", "Ctrl+Shift+S", "Ctrl+Shift+Z",
)

# Repaso, navegador de tarjetas, plantillas y barra lateral.
_WINDOWS: tuple[str, ...] = (
    "Ctrl+:", "Ctrl+Alt+G", "Ctrl+Alt+I", "Ctrl+Enter", "Ctrl+Return",
    "Ctrl+H", "Ctrl+M", "Ctrl+T", "Ctrl+Shift+H", "Ctrl+Shift+X",
    "Shift+Home", "Shift+End",
    "Alt+1", "Alt+2", "Alt+3", "Alt+4", "Alt+5",
    "Alt+6", "Alt+7", "Alt+8", "Alt+9",
    "F11",
)

# Editor de notas. Aqui esta "Ctrl+Shift+T", que en Anki salta al campo de
# etiquetas: justo dentro de la ventana en la que trabaja este complemento.
_EDITOR: tuple[str, ...] = (
    "Ctrl+A", "Ctrl+B", "Ctrl+C", "Ctrl+I", "Ctrl+L", "Ctrl+R", "Ctrl+U", "Ctrl+Y",
    "Ctrl+Shift+C", "Ctrl+Shift+T", "Ctrl+Shift+V",
    "Ctrl+Alt+Shift+C", "Ctrl+Alt+Shift+M",
)

# Edicion de toda la vida: robarlas dejaria a la persona sin cortar ni pegar
# mientras escribe una tarjeta.
_EDITING: tuple[str, ...] = ("Ctrl+X", "Ctrl+V", "Ctrl+S")

_RESERVED: tuple[str, ...] = _MENUS + _WINDOWS + _EDITOR + _EDITING


def normalize(sequence_text: str) -> str:
    """Texto canonico de una combinacion, para poder compararlas entre si."""
    return QKeySequence(sequence_text).toString(QKeySequence.SequenceFormat.PortableText)


@lru_cache(maxsize=1)
def _reserved_by_anki() -> frozenset[str]:
    return frozenset(
        normalized for text in _RESERVED if (normalized := normalize(text))
    )


def _reserved_by_menus() -> set[str]:
    """Atajos que la ventana principal tiene puestos ahora mismo."""
    found: set[str] = set()
    try:
        for action in mw.findChildren(QAction):
            for sequence in action.shortcuts():
                if normalized := sequence.toString(QKeySequence.SequenceFormat.PortableText):
                    found.add(normalized)
    except Exception:
        # Si la ventana principal aun no tiene menus, basta con la lista fija.
        return set()
    return found


def has_required_modifier(sequence_text: str) -> bool:
    """La combinacion incluye Ctrl o Alt."""
    normalized = normalize(sequence_text)
    return "Ctrl+" in normalized or "Alt+" in normalized


def used_by_anki(sequence_text: str) -> bool:
    """Anki ya usa esa combinacion, segun la lista fija."""
    normalized = normalize(sequence_text)
    return bool(normalized) and normalized in _reserved_by_anki()


def is_taken(sequence_text: str) -> bool:
    """Anki ya la usa, o la tiene puesta ahora mismo un menu suyo."""
    if used_by_anki(sequence_text):
        return True
    return normalize(sequence_text) in _reserved_by_menus()


def is_usable(sequence_text: str) -> bool:
    """La combinacion sirve como atajo propio del complemento."""
    if not normalize(sequence_text):
        return False
    return has_required_modifier(sequence_text) and not is_taken(sequence_text)
