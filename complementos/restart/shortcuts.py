"""Qué combinaciones de teclas puede usar el complemento y cuáles están cogidas.

Dos atajos idénticos sobre la ventana principal dejan a Qt en estado ambiguo y
entonces no responde ninguno de los dos: ni el de Anki ni el del complemento.
Por eso la combinación se comprueba antes de guardarla y antes de registrarla.

Las combinaciones ocupadas no se copian a mano: se le preguntan a la propia
ventana principal en el momento de comprobar, así la lista siempre está al día
e incluye también las de otros complementos instalados.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-28) — Un atajo en Ctrl+W no hacía nada en macOS ni Linux.

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Final

from aqt import mw
from aqt.qt import QAction, QKeySequence, QShortcut

# Atajos del repaso y del resumen de mazo. Solo existen mientras esa pantalla
# está activa, así que no se detectan preguntando a la ventana; se enumeran
# aquí los que llevan tecla modificadora (los de tecla suelta ya quedan fuera
# por la regla del modificador). Origen: qt/aqt/reviewer.py, _shortcutKeys y
# korean_shortcuts.
_STATE_SHORTCUTS: Final[tuple[str, ...]] = (
    *(f"Ctrl+{index}" for index in range(1, 8)),  # marcas de color
    "Ctrl+Alt+N",
    "Ctrl+Alt+E",
    "Ctrl+Alt+I",
    "Ctrl+Shift+D",
    "Ctrl+Delete",
    "Ctrl+Backspace",
    "Ctrl+Alt+ㅜ",
    "Ctrl+Alt+ㅑ",
)

# Una combinación sin Ctrl, Alt o Meta sería una tecla suelta, y las teclas
# sueltas están repartidas por toda la interfaz de Anki (repaso, listas...).
_REQUIRED_MODIFIERS: Final[tuple[str, ...]] = ("ctrl+", "alt+", "meta+")


def portable_text(sequence: QKeySequence) -> str:
    """Forma estable de la combinación, la misma en cualquier sistema."""
    return sequence.toString(QKeySequence.SequenceFormat.PortableText)


def display_text(sequence: QKeySequence) -> str:
    """Forma que se le enseña a la persona, con los símbolos de su sistema."""
    return sequence.toString(QKeySequence.SequenceFormat.NativeText)


def _key(value: str | QKeySequence) -> str:
    sequence = value if isinstance(value, QKeySequence) else QKeySequence(value)
    return portable_text(sequence).lower()


def _close_window_keys() -> Iterator[str]:
    # --- FIX-001 (2026-07-28) --------------------------------------
    # Síntoma: un atajo puesto en Ctrl+W no hacía nada en macOS ni en Linux.
    # Causa: en esos dos sistemas Anki intercepta la combinación de "cerrar
    #        ventana" (Ctrl+W, o Cmd+W en macOS) desde la propia aplicación,
    #        antes de que llegue a ningún atajo. Ver qt/aqt/__init__.py,
    #        AnkiApp.eventFilter.
    # Regla: no aceptar nunca como atajo propio una combinación que Qt declare
    #        estándar para cerrar ventana; se le preguntan a Qt en lugar de
    #        escribirlas a mano, porque cambian según el sistema.
    # ---------------------------------------------------------------
    for binding in QKeySequence.keyBindings(QKeySequence.StandardKey.Close):
        if key := _key(binding):
            yield key


def _keys_registered_on_main_window(exclude: Iterable[QShortcut]) -> Iterator[str]:
    """Combinaciones que la ventana principal tiene cogidas ahora mismo.

    Incluye las entradas de menú de Anki, sus atajos globales y los de otros
    complementos. Se dejan fuera los del propio complemento, que si no se
    tomarían a sí mismos por un conflicto.
    """
    excluded = {id(shortcut) for shortcut in exclude}
    for action in mw.findChildren(QAction):
        for sequence in action.shortcuts():
            if key := _key(sequence):
                yield key
    for shortcut in mw.findChildren(QShortcut):
        if id(shortcut) in excluded:
            continue
        if key := _key(shortcut.key()):
            yield key


def keys_in_use(exclude: Iterable[QShortcut] = ()) -> frozenset[str]:
    return frozenset(
        (
            *(_key(text) for text in _STATE_SHORTCUTS),
            *_close_window_keys(),
            *_keys_registered_on_main_window(exclude),
        )
    )


def is_well_formed(sequence: QKeySequence) -> bool:
    """True si es una sola pulsación y lleva tecla modificadora."""
    if sequence.isEmpty() or sequence.count() != 1:
        return False
    text = portable_text(sequence).lower()
    # "Ctrl+" a secas significa que solo se pulsó la tecla modificadora.
    if not text or text.endswith("+"):
        return False
    return any(modifier in text for modifier in _REQUIRED_MODIFIERS)


def is_allowed(sequence: QKeySequence, exclude: Iterable[QShortcut] = ()) -> bool:
    """True si la combinación se puede asignar sin pisar nada de Anki."""
    if not is_well_formed(sequence):
        return False
    return _key(sequence) not in keys_in_use(exclude)
