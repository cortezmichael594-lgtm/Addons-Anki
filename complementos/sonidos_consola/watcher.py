"""Vigila la interfaz de Anki para saber cuándo sonar: menús, ventanas, globos y avisos.

No hay ganchos de Anki para estos momentos, así que se observa lo que Qt ya anuncia: un
«filtro de eventos» de la aplicación que mira, sin tocarlos, unos pocos tipos de evento y
deja pasar todo lo demás de inmediato. Nunca consume un evento (siempre devuelve False).
"""

from __future__ import annotations

from aqt import mw
from aqt.addons import AddonManager
from aqt.qt import (
    QAction,
    QApplication,
    QDialog,
    QElapsedTimer,
    QEvent,
    QKeyEvent,
    QMenu,
    QMenuBar,
    QMessageBox,
    QMouseEvent,
    QObject,
    Qt,
    QWidget,
    qconnect,
)

from . import config, logic
from .player import bank

# Propiedad que marca un menú o una barra de menús ya conectados (prefijo del paquete).
_HOOKED_PROPERTY = "sonidos_consola_hooked"
# Un cierre cuenta como «cancelar» solo si la persona tocó esa ventana justo antes: así no
# suenan las ventanas de progreso ni las que Anki cierra por su cuenta.
_USER_INPUT_WINDOW_MS = 600

_WATCHED = frozenset(
    {
        QEvent.Type.Show,
        QEvent.Type.Hide,
        QEvent.Type.Close,
        QEvent.Type.KeyPress,
        QEvent.Type.MouseButtonPress,
        QEvent.Type.MouseButtonRelease,
    }
)


def _is_tooltip(obj: QObject) -> bool:
    """El globo de Anki es una etiqueta «CustomLabel» creada por aqt.utils.tooltip."""
    cls = type(obj)
    return cls.__name__ == "CustomLabel" and cls.__module__ == "aqt.utils"


class InterfaceWatcher(QObject):
    def __init__(self) -> None:
        super().__init__(mw)
        self._clock = QElapsedTimer()
        self._clock.start()
        self._last_input_window: QWidget | None = None
        self._last_input_ms = -(10**9)
        self._last_hovered: dict[int, QAction] = {}
        self._failed = False

    # Filtro de eventos
    ###########################################################################

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 is None or a1 is None or self._failed:
            return False
        if a1.type() not in _WATCHED:
            return False
        try:
            self._handle(a0, a1)
        except Exception:
            # Un fallo aquí se repetiría en cada evento: se anota una vez y el vigilante se
            # retira. Anki sigue funcionando, sin sonidos de interfaz hasta reiniciar.
            self._failed = True
            AddonManager.get_logger(__name__).exception("El vigilante de la interfaz falló y se ha desactivado")
        return False

    def _handle(self, obj: QObject, event: QEvent) -> None:
        kind = event.type()
        if kind in (QEvent.Type.MouseButtonRelease, QEvent.Type.KeyPress) and isinstance(obj, QWidget):
            self._last_input_window = obj.window()
            self._last_input_ms = self._clock.elapsed()

        if isinstance(obj, QMenu):
            self._handle_menu(obj, event)
        elif isinstance(obj, QMenuBar):
            self._handle_menubar(obj, event)
        elif kind == QEvent.Type.Show and _is_tooltip(obj):
            bank.play("gameboot")
        elif isinstance(obj, QMessageBox):
            self._handle_message_box(obj, event)
        elif isinstance(obj, QDialog):
            self._handle_dialog(obj, event)
        elif (
            kind == QEvent.Type.Close
            and event.spontaneous()
            and isinstance(obj, QWidget)
            and obj.isWindow()
            and obj is not mw
        ):
            # La X o Alt+F4 de una ventana que no es un diálogo (Explorar, Añadir...).
            bank.play("cancel")

    # Menús
    ###########################################################################

    def _hook_signals(self, widget: QMenu | QMenuBar) -> None:
        if widget.property(_HOOKED_PROPERTY):
            return
        widget.setProperty(_HOOKED_PROPERTY, True)
        qconnect(widget.hovered, lambda action, w=widget: self._on_hovered(w, action))
        if isinstance(widget, QMenu):
            qconnect(widget.triggered, self._on_triggered)
            qconnect(widget.aboutToHide, lambda w=widget: self._last_hovered.pop(id(w), None))

    def _handle_menu(self, menu: QMenu, event: QEvent) -> None:
        kind = event.type()
        if kind == QEvent.Type.Show:
            self._hook_signals(menu)
        elif kind == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Escape:
                bank.play("cancel")
        elif kind == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
            if menu.rect().contains(event.position().toPoint()):
                return
            # Clic fuera del menú: se cierra sin elegir nada, salvo que el clic caiga en otro
            # menú abierto o en otro título de la barra (eso es seguir navegando).
            global_pos = event.globalPosition().toPoint()
            target = QApplication.widgetAt(global_pos)
            if isinstance(target, QMenu):
                return
            if isinstance(target, QMenuBar):
                clicked = target.actionAt(target.mapFromGlobal(global_pos))
                if clicked is None or clicked is not target.activeAction():
                    return
            bank.play("cancel")

    def _handle_menubar(self, bar: QMenuBar, event: QEvent) -> None:
        kind = event.type()
        if kind == QEvent.Type.Show:
            self._hook_signals(bar)
        elif kind == QEvent.Type.MouseButtonPress and config.load()["navigation"] == logic.NAV_CLICK:
            if isinstance(event, QMouseEvent) and bar.actionAt(event.position().toPoint()) is not None:
                bank.play("option")

    def _on_hovered(self, widget: QMenu | QMenuBar, action: QAction | None) -> None:
        if self._failed or action is None or action.isSeparator():
            return
        if self._last_hovered.get(id(widget)) is action:
            return
        self._last_hovered[id(widget)] = action
        if config.load()["navigation"] == logic.NAV_HOVER:
            bank.play("option")

    def _on_triggered(self, _action: QAction) -> None:
        if not self._failed and config.load()["navigation"] == logic.NAV_CLICK:
            bank.play("option")

    # Ventanas
    ###########################################################################

    def _user_closed(self, window: QWidget) -> bool:
        recent = self._clock.elapsed() - self._last_input_ms < _USER_INPUT_WINDOW_MS
        return recent and self._last_input_window is window

    def _handle_message_box(self, box: QMessageBox, event: QEvent) -> None:
        kind = event.type()
        if kind == QEvent.Type.Show:
            if box.icon() in (QMessageBox.Icon.Warning, QMessageBox.Icon.Critical):
                bank.play("error")
                _sync_tracker.error_seen = True
        elif kind == QEvent.Type.Close and event.spontaneous():
            bank.play("cancel")
        elif kind == QEvent.Type.Hide and not event.spontaneous() and len(box.buttons()) > 1:
            if not self._user_closed(box):
                return
            clicked = box.clickedButton()
            role = box.buttonRole(clicked) if clicked is not None else None
            if role in (QMessageBox.ButtonRole.YesRole, QMessageBox.ButtonRole.AcceptRole):
                bank.play("system_ok")
            elif role is None or role in (QMessageBox.ButtonRole.NoRole, QMessageBox.ButtonRole.RejectRole):
                bank.play("cancel")

    def _handle_dialog(self, dialog: QDialog, event: QEvent) -> None:
        kind = event.type()
        if kind == QEvent.Type.Hide and not event.spontaneous():
            if dialog.result() == QDialog.DialogCode.Rejected and self._user_closed(dialog):
                bank.play("cancel")
        elif kind == QEvent.Type.Close and event.spontaneous():
            bank.play("cancel")


class _SyncTracker:
    """Recuerda si durante la sincronización Anki mostró un aviso de error."""

    def __init__(self) -> None:
        self.error_seen = False


_sync_tracker = _SyncTracker()


def on_sync_will_start() -> None:
    _sync_tracker.error_seen = False


def on_sync_did_finish() -> None:
    if not _sync_tracker.error_seen:
        bank.play("system_ok")
