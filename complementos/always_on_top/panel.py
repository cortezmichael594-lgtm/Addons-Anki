"""Ventana de opciones con el panel modelo de GritMap.

El diseno esta descrito en docs/fichas-diseno/09-patron-configuracion.md y es
regla del taller desde el 2026-11-09 (PROP-012): una pagina dentro de la
ventana (AnkiWebView, como las opciones de mazo de Anki), con recuadros,
controles web reales dibujados a medida y Aceptar y Cancelar abajo.

Esta pieza es la misma en todos los complementos: solo cambia el prefijo de lo
que se inyecta («always_on_top»). Cada complemento describe su panel (recuadros y
controles) y atiende los mensajes de la pagina con un manejador:

- "accept" (valores): devuelve None si se puede guardar (la ventana se cierra)
  o {"error": texto, "field": clave} para ensenar el error encima del campo.
- "cancel": la ventana se cierra sin guardar.
- "summary", "options", "action" y "keytext": datos que pide la pagina.

Nada se guarda antes de Aceptar.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from anki.utils import is_mac
from aqt import mw
from aqt.qt import QCloseEvent, QDialog, QDialogButtonBox, QKeySequence, Qt, QVBoxLayout, QWidget, sip
from aqt.utils import disable_help_button, restoreGeom, saveGeom

WIDTH = 560
MAX_HEIGHT = 720
MIN_HEIGHT = 240
SCREEN_MARGIN = 80
SHOW_ANYWAY_MS = 3000
BRIDGE_PREFIX = "always_on_top-panel:"
# El estilo y el codigo del panel van dentro de la propia pagina, no como
# archivos servidos por Anki: asi estan listos antes del primer pintado y no hace
# falta abrir a las tarjetas ningun archivo del complemento (sin setWebExports).
WEB_DIR = Path(__file__).parent / "web"

Handler = Callable[[str, Any], Any]
Logger = Callable[[str, BaseException], None]


def _plain(text: str) -> str:
    """Quita el «&» de los atajos de Qt («&Aceptar» → «Aceptar»)."""
    return text.replace("&&", "\0").replace("&", "").replace("\0", "&")


def button_text(kind: QDialogButtonBox.StandardButton) -> str:
    """Texto de un boton estandar de Qt («Sí», «No»...) en el idioma de Anki."""
    box = QDialogButtonBox(kind)
    button = box.button(kind)
    text = _plain(button.text()) if button is not None else ""
    box.deleteLater()
    return text


def standard_texts() -> dict[str, str]:
    """Aceptar, Cancelar y Restaurar con el texto que Qt pone en el idioma de
    Anki, y Deshacer y Buscar con los de Anki: sin traducciones
    propias, iguales que en el resto del programa."""
    box = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok
        | QDialogButtonBox.StandardButton.Cancel
        | QDialogButtonBox.StandardButton.RestoreDefaults
    )
    texts: dict[str, str] = {}
    for key, kind in (
        ("ok", QDialogButtonBox.StandardButton.Ok),
        ("cancel", QDialogButtonBox.StandardButton.Cancel),
        ("restore", QDialogButtonBox.StandardButton.RestoreDefaults),
    ):
        button = box.button(kind)
        texts[key] = _plain(button.text()) if button is not None else key
    box.deleteLater()
    texts["undo"] = _anki_text("undo_undo", "Undo")
    texts["search"] = _anki_text("actions_search", "Search")
    return texts


def _anki_text(attribute: str, fallback: str) -> str:
    try:
        from aqt.utils import tr

        method = getattr(tr, attribute, None)
        if callable(method):
            value = method()
            if isinstance(value, str) and value.strip():
                return value
    except Exception:
        pass
    return fallback


def key_text(portable: str) -> str:
    """Un atajo escrito con los nombres de teclas del sistema y del idioma."""
    sequence = QKeySequence(portable, QKeySequence.SequenceFormat.PortableText)
    return sequence.toString(QKeySequence.SequenceFormat.NativeText)


def parent_window() -> QWidget:
    """La ventana desde la que se abre (normalmente, Complementos)."""
    window = mw.app.activeWindow()
    if window is None or sip.isdeleted(window) or not window.isVisible():
        return mw
    return window


class PanelDialog(QDialog):
    """Ventana de opciones: una pagina con el panel dentro."""

    def __init__(
        self,
        parent: QWidget,
        package: str,
        page: dict[str, Any],
        handler: Handler,
        log: Logger,
        geometry_key: str,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(str(page.get("title", "")))
        disable_help_button(self)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self._handler = handler
        self._log = log
        self._geometry_key = geometry_key
        self._ready = False
        self._closing = False

        page = dict(page)
        page.setdefault("texts", {})
        page["texts"] = {**standard_texts(), **page["texts"]}
        page["prefix"] = BRIDGE_PREFIX
        page["isMac"] = is_mac

        # Se importa aqui: aqt.webview arrastra pantallas de Anki que no se
        # pueden cargar fuera de Anki (las pruebas importan el paquete).
        from aqt.webview import AnkiWebView

        self._web = AnkiWebView(self, title=f"{package} options")
        self._web.set_bridge_command(self._on_bridge, self)
        # La pagina no se ensena hasta que esta dibujada entera: sin parpadeos.
        self._web.hide()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._web)

        self.setMinimumWidth(WIDTH)
        restoreGeom(self, geometry_key, default_size=(WIDTH, 480))
        self.resize(WIDTH, self.height())

        payload = json.dumps(page, ensure_ascii=False).replace("</", "<\\/")
        style = (WEB_DIR / "panel.css").read_text(encoding="utf-8")
        script = (WEB_DIR / "panel.js").read_text(encoding="utf-8")
        body = (
            '<div id="always_on_top-app"></div>'
            f"<script>{script}</script>"
            f"<script>AlwaysOnTopPanel.init({payload});</script>"
        )
        self._web.stdHtml(body, css=[], js=[], head=f"<style>{style}</style>", context=self)
        # Por si la pagina no llegara a avisar de que esta lista.
        mw.progress.single_shot(SHOW_ANYWAY_MS, self._show_anyway, False)

    def _show_anyway(self) -> None:
        if sip.isdeleted(self) or self._ready:
            return
        self._ready = True
        self._web.show()

    def _on_bridge(self, cmd: str) -> Any:
        if not cmd.startswith(BRIDGE_PREFIX):
            return None
        action, _sep, raw = cmd[len(BRIDGE_PREFIX) :].partition(":")
        try:
            arg = json.loads(raw) if raw else None
            return self._handle(action, arg)
        except Exception as exc:
            self._log(f"panel.{action}", exc)
            return None

    def _handle(self, action: str, arg: Any) -> Any:
        if action == "ready":
            self._ready = True
            self._fit_height(arg)
            self._web.show()
            self._web.setFocus()
            return None
        if action == "keytext":
            return key_text(str(arg)) if arg else ""
        if action == "accept":
            result = self._handler("accept", arg)
            if result:
                return result
            self._closing = True
            self.accept()
            return None
        if action == "cancel":
            self._closing = True
            QDialog.reject(self)
            return None
        return self._handler(action, arg)

    def _fit_height(self, raw: Any) -> None:
        """El alto de la pagina principal, hasta 720 px o el de la pantalla
        menos 80 px; se fija una vez al abrir (regla de FIX-028 de GritMap)."""
        try:
            wanted = int(float(raw))
        except (TypeError, ValueError):
            return
        screen = self.screen()
        limit = screen.availableGeometry().height() - SCREEN_MARGIN if screen is not None else wanted
        limit = min(limit, MAX_HEIGHT)
        self.resize(self.width(), max(MIN_HEIGHT, min(wanted, limit)))

    def reject(self) -> None:
        self._closing = True
        QDialog.reject(self)

    def closeEvent(self, event: QCloseEvent | None) -> None:  # noqa: N802 (nombre de Qt)
        self._closing = True
        super().closeEvent(event)

    def done(self, result: int) -> None:
        try:
            saveGeom(self, self._geometry_key)
        except Exception as exc:
            self._log("panel.done", exc)
        if result != QDialog.DialogCode.Accepted:
            try:
                self._handler("cancel", None)
            except Exception as exc:
                self._log("panel.cancel", exc)
        self._web.cleanup()
        super().done(result)
