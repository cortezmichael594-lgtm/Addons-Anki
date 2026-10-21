"""Barra de título de las ventanas, del color de la paleta (solo Windows 11).

La barra de título (el nombre de la ventana y los botones de minimizar, maximizar y
cerrar) no la dibujan ni Anki ni Qt, sino Windows: por eso no la tiñen los colores
de Anki y se queda blanca de día y negra de noche. Desde Windows 11 (compilación
22000) se puede pedir a Windows, ventana a ventana, el color de su fondo, de su
texto y de su borde (DwmSetWindowAttribute, de la documentación de Microsoft).

Cada ventana se tiñe justo antes de mostrarse, para que no se vea primero con la
barra blanca, y todas las abiertas se vuelven a teñir al cambiar de día a noche o
de paleta. En Windows 10, macOS y Linux no se hace nada: allí la barra sigue al modo
día o noche, como de costumbre.
"""

from __future__ import annotations

import ctypes
import sys
from typing import Any

from aqt import gui_hooks, mw
from aqt.qt import QApplication, QEvent, QObject, Qt, QWidget
from aqt.theme import theme_manager

from . import themes
from .errors import get_logger, guard

# Atributos de DwmSetWindowAttribute (dwmapi.h, Windows 11).
_DWMWA_USE_IMMERSIVE_DARK_MODE = 20
_DWMWA_BORDER_COLOR = 34
_DWMWA_CAPTION_COLOR = 35
_DWMWA_TEXT_COLOR = 36
_FIRST_BUILD = 22000  # primera compilación de Windows 11

# Color de la paleta para cada parte de la barra: el fondo de la ventana, su texto
# y un borde suave. Con colores propios, Windows ya no distingue la ventana activa
# de las demás y lo deja en manos del programa (documentación de Microsoft): el
# título de las inactivas va en el texto secundario, como el gris que pone Windows.
_PARTS = (
    (_DWMWA_CAPTION_COLOR, "CANVAS", "CANVAS"),
    (_DWMWA_TEXT_COLOR, "FG", "FG_SUBTLE"),
    (_DWMWA_BORDER_COLOR, "BORDER", "BORDER"),
)
# Momentos en que se tiñe una ventana: al mostrarse y al activarse o desactivarse.
_EVENTS = (QEvent.Type.Show, QEvent.Type.ActivationChange)

_set_attribute: Any = None
_watcher: QObject | None = None


def colorref(value: str) -> int:
    """De «#RRGGBB» (o «#RRGGBBAA», sin la transparencia) al formato de Windows,
    0x00BBGGRR."""
    value = value.lstrip("#")
    red, green, blue = (int(value[i : i + 2], 16) for i in (0, 2, 4))
    return red | green << 8 | blue << 16


def bar_colors(night: bool, active: bool) -> list[tuple[int, int]]:
    """Pares (atributo, color) de la paleta elegida para el modo y el estado."""
    palette = themes.colors()
    pairs = []
    for attribute, active_name, inactive_name in _PARTS:
        entry = palette[active_name if active else inactive_name]
        pairs.append((attribute, colorref(entry["dark"] if night else entry["light"])))
    return pairs


def has_title_bar(widget: QWidget) -> bool:
    """Ventanas y diálogos con su barra; no menús, ayudas emergentes ni avisos."""
    if not widget.isWindow():
        return False
    if widget.windowFlags() & Qt.WindowType.FramelessWindowHint:
        return False
    return widget.windowType() in (Qt.WindowType.Window, Qt.WindowType.Dialog)


def supported() -> bool:
    if sys.platform != "win32":
        return False
    return sys.getwindowsversion().build >= _FIRST_BUILD


def _paint(window: QWidget) -> None:
    global _set_attribute
    if sys.platform != "win32":
        return
    if _set_attribute is None:
        from ctypes import wintypes

        function = ctypes.windll.dwmapi.DwmSetWindowAttribute
        function.argtypes = (wintypes.HWND, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD)
        function.restype = ctypes.c_long
        _set_attribute = function
    hwnd = int(window.winId())
    night = theme_manager.night_mode
    # Los botones de la barra (minimizar, cerrar...) los dibuja Windows claros u oscuros
    # según su propio modo, que puede no ser el de Anki: se le indica el de Anki para que
    # se vean sobre el color de la paleta.
    dark = ctypes.c_int(1 if night else 0)
    _set_attribute(hwnd, _DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(dark), ctypes.sizeof(dark))
    for attribute, value in bar_colors(night, window.isActiveWindow()):
        color = ctypes.c_uint32(value)
        # Si Windows no lo admite, devuelve un código de error y la barra queda como estaba.
        _set_attribute(hwnd, attribute, ctypes.byref(color), ctypes.sizeof(color))


class _WindowWatcher(QObject):
    """Tiñe cada ventana en el momento de mostrarse, antes de que se vea, y cada
    vez que pasa a ser la activa o deja de serlo."""

    def eventFilter(self, obj: QObject | None, event: QEvent | None) -> bool:
        if (
            event is not None
            and event.type() in _EVENTS
            and isinstance(obj, QWidget)
            and has_title_bar(obj)
        ):
            try:
                _paint(obj)
            except Exception:
                # Un fallo aquí no debe repetirse en cada ventana: se deja de teñir.
                get_logger().exception("no se pudo teñir la barra de título")
                uninstall()
        return False


@guard
def repaint_open_windows() -> None:
    """Vuelve a teñir las ventanas abiertas (cambio de día a noche o de paleta)."""
    if _watcher is None:
        return
    for widget in QApplication.topLevelWidgets():
        if widget.isVisible() and has_title_bar(widget):
            _paint(widget)


def install() -> None:
    """Empieza a teñir las barras de título, si Windows lo permite."""
    global _watcher
    if mw is None or _watcher is not None or not supported():
        return
    _watcher = _WindowWatcher(mw)
    mw.app.installEventFilter(_watcher)
    # Anki avisa con este gancho al pasar de día a noche y cada vez que se rehace su
    # estilo, también al cambiar de paleta.
    gui_hooks.theme_did_change.append(repaint_open_windows)


def uninstall() -> None:
    global _watcher
    if mw is not None and _watcher is not None:
        mw.app.removeEventFilter(_watcher)
    _watcher = None
