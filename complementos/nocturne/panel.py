"""Panel de configuración a medida (versión 3.7.0).

Informe del cliente del 2026-10-28: la ventana para elegir paleta es un panel con
el mismo material y las mismas medidas que el de GritMap 4.11.2 (una página dentro
de la ventana, como las opciones de mazo de Anki). Las cinco paletas a la vista, en
orden alfabético, cada una con una miniatura de día y otra de noche (pequeños
múltiplos de Tufte), su nombre y su descripción. Un clic la aplica al momento a
todo Anki; con las flechas, cuando la elección lleva 200 ms quieta. «Aceptar» la
guarda y «Cancelar», Esc o la X vuelven a la que había.

La guía del taller pide controles estándar en las ventanas: este panel propio lo
pidió el cliente de forma expresa. Salida de emergencia: si el panel no avisa de
que está dibujado en 3 segundos, o falla al crearse, se cierra sin cambiar nada y
se abre la ventana sencilla de controles de Anki (dialogs.PaletteDialog).

Reparto del trabajo: la página (web/panel.js) dibuja y gestiona la elección; aquí
se preparan los datos (colores de las miniaturas, textos, modo activo) y se aplica,
se guarda o se deshace la paleta.
"""

from __future__ import annotations

import json
from typing import Any

from aqt import gui_hooks, mw
from aqt.qt import QApplication, QCloseEvent, QDialog, Qt, QTimer, QVBoxLayout, QWidget
from aqt.theme import theme_manager
from aqt.utils import disable_help_button, openFolder
from aqt.webview import AnkiWebView

from . import actions, config, contrast, errors, strings, themes
from .errors import guard, note_failure

# Prefijo de las órdenes de la página (nombre del paquete: otros complementos
# comparten el canal).
MSG_PREFIX = "nocturne:"
WEB_PATTERN = r"web/panel\.(css|js)$"  # cerrado: solo estos dos archivos (APR-049)
PREVIEW_DELAY_MS = 200
READY_TIMEOUT_MS = 3000
_WIDTH = 560  # como el panel de GritMap
_MAX_HEIGHT = 720
_SCREEN_MARGIN = 80

# Colores de cada miniatura: la lista de mazos reducida a lo que cambia entre paletas.
_THUMB_TOKENS = {
    "canvas": "CANVAS",
    "card": "CANVAS_ELEVATED",
    "line": "BORDER_SUBTLE",
    "edge": "BORDER_STRONG",  # versión 3.9.0: el borde de la miniatura, que se vea en la fila elegida
    "faint": "FG_FAINT",
    "fg": "FG",
    "subtle": "FG_SUBTLE",
    "new": "STATE_NEW",
    "learn": "STATE_LEARN",
    "review": "STATE_REVIEW",
    "action": "BUTTON_PRIMARY_BG",
}


def ordered_ids() -> list[str]:
    """Paletas por orden alfabético de su nombre, como los temas de GritMap."""
    return sorted(themes.THEMES, key=lambda theme_id: strings.THEME_NAMES[theme_id].casefold())


def thumb_colors(theme_id: str, night: bool) -> dict[str, str]:
    palette = themes.THEMES[theme_id]["colors"]
    colors = {}
    for key, name in _THUMB_TOKENS.items():
        entry = palette[name]
        colors[key] = (entry["dark"] if night else entry["light"])[:7]
    return colors


def description_lines(theme_id: str) -> str:
    """La descripción en dos líneas, partida por el punto: colores y botones, y la forma
    (versión 3.9.0, informe del 2026-11-11, apartado 8.12). Antes ocupaba dos líneas
    cortadas a media frase («…Letra y esquinas como / Nocturne.»)."""
    first, _sep, second = strings.THEME_DESCRIPTIONS[theme_id].partition(". ")
    return f"{first}.\n{second}" if second else first


def payload(current: str, night: bool, failures: bool, stepped_aside: bool) -> dict[str, Any]:
    """Todo lo que la página necesita para dibujarse."""
    entries = []
    for theme_id in ordered_ids():
        look = themes.THEMES[theme_id]["look"]
        entries.append(
            {
                "id": theme_id,
                "name": strings.THEME_NAMES[theme_id],
                "isDefault": theme_id == themes.DEFAULT_THEME,
                "description": description_lines(theme_id),
                "headingFont": look["heading_family"] or "",
                "radius": look["button_radius"],
                "day": thumb_colors(theme_id, False),
                "night": thumb_colors(theme_id, True),
            }
        )
    return {
        "palettes": entries,
        "current": current,
        "night": night,
        "failures": failures,
        "steppedAside": stepped_aside,
        "texts": {
            "title": strings.PANEL_TITLE,
            "intro": strings.PANEL_INTRO,
            "day": strings.DAY,
            "night": strings.NIGHT,
            "default": strings.DEFAULT_WORD,
            "modeNote": strings.MODE_NOTE_NIGHT if night else strings.MODE_NOTE_DAY,
            "modeNoteDay": strings.MODE_NOTE_DAY,
            "modeNoteNight": strings.MODE_NOTE_NIGHT,
            "contrast": strings.HIGH_CONTRAST_BANNER,
            "failures": strings.FAILURES,
            "openLog": strings.OPEN_LOG,
            "accept": strings.ACCEPT,
            "cancel": strings.CANCEL,
        },
    }


def _script_safe(text: str) -> str:
    """JSON que se puede meter en un <script> sin cerrarlo antes de tiempo."""
    return text.replace("</", "<\\/")


class PanelDialog(QDialog):
    """Ventana que contiene la página del panel."""

    def __init__(self, parent: QWidget, on_timeout: Any) -> None:
        super().__init__(parent)
        self.setWindowTitle(strings.ADDON_NAME)
        disable_help_button(self)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self._original = themes.current_id()
        self._chosen = self._original
        self._preview_enabled = not contrast.stepped_aside()
        self._ready = False
        self._loaded = False
        self._closing = False
        self._waiting = False
        self._on_timeout = on_timeout
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(PREVIEW_DELAY_MS)
        self._timer.timeout.connect(self._preview)

        self._web = AnkiWebView(self, title="nocturne panel")
        self._web.set_bridge_command(self._on_bridge, self)
        self._web.loadFinished.connect(self._on_load_finished)
        # La página no se enseña hasta que está dibujada entera: sin parpadeos.
        self._web.hide()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._web)
        self.setMinimumWidth(_WIDTH)
        self.resize(_WIDTH, 640)

        package = mw.addonManager.addon_from_module(__name__) if mw is not None else "nocturne"
        data = payload(
            self._original,
            theme_manager.night_mode,
            bool(errors.failures() and errors.logs_folder()),
            contrast.stepped_aside(),
        )
        body = (
            '<div id="nocturne-panel"></div>'
            f"<script>NocturnePanel.init({_script_safe(json.dumps(data, ensure_ascii=False))});</script>"
        )
        # Versión 3.8.0 (informe del 2026-11-04, apartado 3.2): cursor de espera desde el
        # clic en «Configuración» hasta que se ve el panel. La primera vez en una sesión
        # puede tardar hasta 3 s, y sin una señal se vuelve a pulsar.
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self._waiting = True
        try:
            self._web.stdHtml(
                body,
                css=[f"/_addons/{package}/web/panel.css"],
                js=[f"/_addons/{package}/web/panel.js"],
                context=self,
            )
        except Exception:
            # Si falla aquí se abre la ventana sencilla: el cursor no se queda en espera.
            self._stop_waiting()
            raise
        gui_hooks.theme_did_change.append(self._on_theme_change)
        if mw is not None:
            mw.progress.single_shot(READY_TIMEOUT_MS, self._check_ready, False)

    def _on_load_finished(self, ok: bool) -> None:
        self._loaded = ok

    # La página avisa de que está lista. Si a los 3 s no lo ha hecho pero ha cargado (la
    # primera vez en una sesión, el navegador de Anki puede tardar en arrancar), se enseña
    # igualmente, como GritMap; si ni siquiera ha cargado, salida de emergencia.
    @guard
    def _check_ready(self) -> None:
        if self._ready or self._closing:
            return
        if self._loaded:
            self._ready = True
            self._reveal()
            return
        note_failure("el panel no se dibujó en %s ms", READY_TIMEOUT_MS)
        self._close_quietly()
        self._on_timeout()

    def _reveal(self) -> None:
        self._web.show()
        self._web.setFocus()
        self._stop_waiting()

    def _stop_waiting(self) -> None:
        # El cursor de espera se quita una sola vez, al enseñar el panel o al cerrarlo.
        if self._waiting:
            self._waiting = False
            QApplication.restoreOverrideCursor()

    def _close_quietly(self) -> None:
        self._closing = True
        self._timer.stop()
        QDialog.reject(self)

    # Mensajes de la página
    def _on_bridge(self, cmd: str) -> Any:
        if not cmd.startswith(MSG_PREFIX):
            return None
        action, _sep, arg = cmd[len(MSG_PREFIX) :].partition(":")
        try:
            return self.handle(action, arg)
        except Exception:
            note_failure("fallo en la orden %s del panel", action)
            return None

    def handle(self, action: str, arg: str) -> None:
        if action == "ready":
            self._ready = True
            self._fit_height(arg)
            self._reveal()
        elif action == "pick":  # clic: al momento
            self._chosen = themes.valid_id(arg)
            self._timer.stop()
            self._preview()
        elif action == "move":  # flechas: cuando la elección lleva 200 ms quieta
            self._chosen = themes.valid_id(arg)
            if self._preview_enabled:
                self._timer.start()
        elif action == "accept":
            self.accept()
        elif action == "cancel":
            self.reject()
        elif action == "log":
            folder = errors.logs_folder()
            if folder:
                openFolder(folder)

    def _fit_height(self, raw: str) -> None:
        """Alto según el contenido, hasta 720 px o el de la pantalla menos 80; si no
        cabe, la página desplaza el cuerpo y deja fijos la cabecera y el pie."""
        try:
            wanted = int(float(raw))
        except ValueError:
            return
        screen = self.screen()
        limit = screen.availableGeometry().height() - _SCREEN_MARGIN if screen is not None else wanted
        self.resize(self.width(), max(240, min(wanted, limit, _MAX_HEIGHT)))

    @guard
    def _preview(self) -> None:
        if self._preview_enabled and self._chosen != themes.current_id():
            actions.apply_palette(self._chosen)

    @guard
    def _on_theme_change(self) -> None:
        # El modo pudo cambiar: la página resalta el rótulo «Día» o «Noche» activo.
        if self._ready:
            self._web.eval(f"NocturnePanel.setNight({json.dumps(bool(theme_manager.night_mode))});")

    def selected_id(self) -> str:
        return self._chosen

    @guard
    def accept(self) -> None:
        if self._closing:
            return
        self._closing = True
        self._timer.stop()
        if self._preview_enabled and self._chosen != themes.current_id():
            actions.apply_palette(self._chosen)
        config.save(self._chosen)
        super().accept()

    @guard
    def reject(self) -> None:
        if self._closing:
            return
        self._closing = True
        self._timer.stop()
        if self._preview_enabled and themes.current_id() != self._original:
            actions.apply_palette(self._original)
        super().reject()

    def closeEvent(self, event: QCloseEvent | None) -> None:  # noqa: N802 (nombre de Qt)
        # La X pasa por reject, que deshace la vista previa.
        if not self._closing:
            self.reject()
        super().closeEvent(event)

    def done(self, result: int) -> None:
        # Se quita aquí, nunca desde dentro del propio gancho.
        gui_hooks.theme_did_change.remove(self._on_theme_change)
        self._stop_waiting()
        self._web.cleanup()
        super().done(result)
