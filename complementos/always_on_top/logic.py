"""Mantiene la ventana de Anadir por encima de las demas ventanas del sistema.

Reglas de esta parte, por si se vuelve a tocar mas adelante:

1. Cambiar los indicadores de ventana de Qt (setWindowFlags) en una ventana
   que ya esta a la vista la oculta y la vuelve a mostrar: eso es el parpadeo.
   Por eso solo se usa esa via cuando la ventana todavia esta oculta, que es
   justo el momento en que Anki dispara add_cards_did_init.
2. Para encender o apagar el efecto con la ventana ya a la vista, en Windows
   se usa la llamada nativa del sistema, que reordena la ventana sin ocultarla
   y por tanto no parpadea.
3. Nada de lanzar programas externos desde aqui. Una llamada a un programa del
   sistema bloquea la interfaz de Anki mientras responde, y una interfaz que no
   responde se percibe como que Anki se ha colgado.
"""

from __future__ import annotations

import ctypes
import weakref
from typing import Any

from anki.utils import is_win
from aqt import mw
from aqt.qt import QKeySequence, QShortcut, Qt, QWidget, qconnect, sip
from aqt.utils import tooltip

from . import config, constants
from .errors import guarded, logger
from .strings import tr

_STAY_ON_TOP: Qt.WindowType = Qt.WindowType.WindowStaysOnTopHint

# Constantes de la API de ventanas de Windows (SetWindowPos).
_HWND_TOPMOST = -1
_HWND_NOTOPMOST = -2
_SWP_NOSIZE = 0x0001
_SWP_NOMOVE = 0x0002
_SWP_NOACTIVATE = 0x0010
_SWP_KEEP_PLACE = _SWP_NOMOVE | _SWP_NOSIZE | _SWP_NOACTIVATE

# ctypes expone tipos dinamicos de Windows sin firma estatica: Any es inevitable.
_user32: Any = None
if is_win:
    from ctypes import wintypes

    try:
        _user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        _user32.SetWindowPos.restype = wintypes.BOOL
        _user32.SetWindowPos.argtypes = [
            wintypes.HWND, wintypes.HWND,
            ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
            wintypes.UINT,
        ]
    except Exception:
        _user32 = None


def _win_set_topmost(window_handle: int, topmost: bool) -> bool:
    """Reordena la ventana sin ocultarla. Devuelve si lo consiguio."""
    if _user32 is None:
        return False
    try:
        insert_after = _HWND_TOPMOST if topmost else _HWND_NOTOPMOST
        done = _user32.SetWindowPos(
            wintypes.HWND(window_handle),
            wintypes.HWND(insert_after),
            0, 0, 0, 0,
            _SWP_KEEP_PLACE,
        )
        return bool(done)
    except Exception as error:
        logger().exception("SetWindowPos: %r", error)
        return False


class AlwaysOnTopManager:
    """Estado del efecto y atajo de teclado que lo enciende y lo apaga."""

    def __init__(self) -> None:
        self._enabled: bool = False
        self._window: weakref.ReferenceType[QWidget] | None = None
        self._shortcut: QShortcut | None = None

    # Arranque y atajo de teclado
    # ------------------------------------------------------------------

    @guarded
    def start(self) -> None:
        self.apply_shortcut(config.load().shortcut, notify=False)

    def apply_shortcut(self, sequence_text: str, notify: bool) -> None:
        sequence = QKeySequence(sequence_text)
        if sequence.isEmpty():
            sequence = QKeySequence(constants.DEFAULT_SHORTCUT)

        if self._shortcut is None:
            # El atajo cuelga de la ventana principal, que vive toda la sesion:
            # asi sigue funcionando despues de cambiar de usuario, porque esa
            # ventana no se destruye al cambiar de perfil.
            self._shortcut = QShortcut(sequence, mw)
            self._shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
            qconnect(self._shortcut.activated, self._on_shortcut_activated)
        else:
            # Reutilizar el atajo existente evita dejar atajos duplicados vivos.
            self._shortcut.setKey(sequence)

        if notify:
            tooltip(tr("shortcut_updated"), period=constants.TOOLTIP_PERIOD_MS)

    @guarded
    def on_config_updated(self, _new_config: dict[str, Any]) -> None:
        self.apply_shortcut(config.load().shortcut, notify=True)

    # Ventana de Anadir
    # ------------------------------------------------------------------

    @guarded
    def on_add_cards_init(self, add_cards: QWidget) -> None:
        # Anki dispara este hook antes de mostrar la ventana, asi que aqui el
        # efecto se aplica sin parpadeo ninguno.
        self._window = weakref.ref(add_cards)
        if self._enabled:
            self._apply(add_cards, True)

    @guarded
    def _on_shortcut_activated(self) -> None:
        self._enabled = not self._enabled
        window = self._current_window()
        if window is not None:
            self._apply(window, self._enabled)
        tooltip(
            tr("on") if self._enabled else tr("off"),
            period=constants.TOOLTIP_PERIOD_MS,
        )

    def _current_window(self) -> QWidget | None:
        """La ventana de Anadir viva, o nada si ya se cerro."""
        window = self._window() if self._window is not None else None
        if window is None or sip.isdeleted(window):
            self._window = None
            return None
        return window

    def _apply(self, window: QWidget, enabled: bool) -> None:
        try:
            if window.isVisible() and is_win:
                if _win_set_topmost(int(window.winId()), enabled):
                    return
            self._apply_qt_flag(window, enabled)
        except RuntimeError:
            # La ventana de Qt pudo destruirse entre la comprobacion y la llamada.
            self._window = None

    def _apply_qt_flag(self, window: QWidget, enabled: bool) -> None:
        flags = window.windowFlags()
        new_flags = flags | _STAY_ON_TOP if enabled else flags & ~_STAY_ON_TOP
        if new_flags == flags:
            return

        was_visible = window.isVisible()
        was_active = window.isActiveWindow()
        geometry = window.geometry()

        window.setWindowFlags(new_flags)

        if was_visible:
            # Qt oculta la ventana al cambiarle los indicadores: hay que
            # devolverle su sitio y, si la tenia, tambien el foco.
            window.setGeometry(geometry)
            window.show()
            if was_active:
                window.raise_()
                window.activateWindow()
