"""Reinicio de Anki desde un atajo de teclado.

El reinicio se hace en dos tiempos: primero se le pide a Anki un cierre
idéntico al normal (guarda la colección, sincroniza si procede y termina la
copia de seguridad) y solo cuando el programa ya se está apagando de verdad se
lanza la nueva instancia. Así la colección nunca queda abierta por dos
procesos a la vez.

El complemento no ofrece atajo para cerrar Anki: eso ya lo hace Anki con
Ctrl+Q. Ver FIX-003 en constants.py.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-07-28) — Anki se volvía a abrir sola en un cierre posterior.
# FIX-003 (2026-07-28) — Se retiró el atajo para cerrar Anki, que duplicaba Ctrl+Q.

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from collections.abc import Iterator
from dataclasses import dataclass, field

from aqt import mw
from aqt.qt import (
    QApplication,
    QKeySequence,
    QLocalServer,
    QShortcut,
    QTimer,
    qconnect,
    sip,
)
from aqt.utils import tooltip

from . import constants, shortcuts
from .errors import log, report_errors, warn_user
from .settings import load_settings
from .strings import tr

_IS_WINDOWS = sys.platform == "win32"

# En Windows el arrancador de Anki se instala como ankiw.exe (sin ventana de
# consola) y anki.exe (con ella); en macOS y Linux, como un único "anki".
_LAUNCHER_NAMES: tuple[str, ...] = (
    ("ankiw.exe", "anki.exe") if _IS_WINDOWS else ("anki",)
)


@dataclass(slots=True)
class _AddonState:
    registered: list[QShortcut] = field(default_factory=list)
    # Orden de arranque de la nueva instancia, o None si no hay reinicio en curso.
    pending_command: list[str] | None = None
    # Momento en que se pidió el reinicio, en segundos de reloj monótono.
    pending_since: float = 0.0
    abort_timer: QTimer | None = None
    quit_hook_connected: bool = False


_state: _AddonState = _AddonState()


# Localizar el programa de Anki
# ---------------------------------------------------------------------------


def _looks_like_anki(path: str) -> bool:
    return os.path.basename(path).lower().startswith("anki") and os.path.isfile(path)


def _executable_candidates() -> Iterator[str]:
    # 1. El propio programa con el que arrancó esta sesión. El arrancador de
    #    Windows recorta el ".exe" de sys.argv[0], así que se prueban las dos.
    argv0 = sys.argv[0] if sys.argv else ""
    if argv0:
        yield argv0
        if _IS_WINDOWS:
            yield f"{argv0}.exe"
    # 2. Instalaciones empaquetadas, donde el intérprete es Anki mismo.
    if sys.executable:
        yield sys.executable
    # 3. Instalaciones sobre un entorno de Python: el arrancador de Anki queda
    #    en la misma carpeta que el intérprete.
    if folder := os.path.dirname(sys.executable or ""):
        for name in _LAUNCHER_NAMES:
            yield os.path.join(folder, name)
    # 4. Último recurso: lo que esté accesible desde el sistema.
    if found := shutil.which("anki"):
        yield found


def _resolve_anki_executable() -> str | None:
    """Ruta del programa de Anki, o None si no se puede identificar con certeza.

    Nunca devuelve el intérprete de Python a secas: arrancarlo cerraría Anki
    sin volver a abrirlo, y eso es peor que no reiniciar.
    """
    for candidate in _executable_candidates():
        path = os.path.abspath(candidate)
        if _looks_like_anki(path):
            return path
    return None


def _relaunch_arguments() -> list[str]:
    """Conserva la carpeta de datos y el perfil que están abiertos ahora mismo.

    Sin esto, quien use una carpeta de datos propia o varios perfiles se
    encontraría otra colección distinta después de reiniciar.
    """
    arguments: list[str] = []
    base = getattr(mw.pm, "base", "")
    if isinstance(base, str) and base:
        arguments += ["-b", base]
    profile = getattr(mw.pm, "name", None)
    if isinstance(profile, str) and profile:
        arguments += ["-p", profile]
    return arguments


# Arrancar la nueva instancia
# ---------------------------------------------------------------------------


def _release_single_instance_lock() -> None:
    # Anki reserva un canal local para detectar segundas instancias; si sigue
    # abierto, la nueva instancia se cerraría creyendo que Anki ya está en marcha.
    app = mw.app
    server = getattr(app, "_srv", None)
    if isinstance(server, QLocalServer):
        server.close()
    key = getattr(type(app), "KEY", None)
    if isinstance(key, str):
        QLocalServer.removeServer(key)


def _spawn_detached(command: list[str]) -> None:
    # El proceso nuevo tiene que sobrevivir a la muerte del actual, y cada
    # sistema lo expresa con banderas distintas.
    if _IS_WINDOWS:
        subprocess.Popen(
            command,
            close_fds=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS,
        )
    else:
        subprocess.Popen(command, close_fds=True, start_new_session=True)


def _clear_pending(reason: str) -> None:
    if _state.pending_command is None:
        return
    _state.pending_command = None
    log().info("reinicio descartado: %s", reason)


def _on_about_to_quit() -> None:
    # Se ejecuta al salir: la colección ya está guardada y cerrada y la copia
    # de seguridad terminada, así que la nueva instancia no puede pisar nada.
    command = _state.pending_command
    _state.pending_command = None
    if not command:
        # Cierre normal, sin reinicio pedido: no hay nada que hacer.
        return
    # --- FIX-002 (2026-07-28) --------------------------------------
    # Síntoma: Anki se volvía a abrir sola al cerrarla mucho después, sin que
    #          se hubiera pedido ningún reinicio.
    # Causa: si el cierre pedido se quedaba a medias (por ejemplo, una ventana
    #        preguntaba si descartar cambios y se respondía que no), la orden
    #        de reinicio seguía guardada y la ejecutaba el siguiente cierre.
    # Regla: una orden aplazada caduca; comprobar siempre que se ejecuta dentro
    #        del plazo previsto, y nunca dar por hecho que el aviso que llega
    #        corresponde a la petición que la dejó guardada.
    # ---------------------------------------------------------------
    waited = time.monotonic() - _state.pending_since
    if waited > constants.RELAUNCH_WINDOW_SECONDS:
        log().info("reinicio caducado tras %.0f s; se cierra sin volver a abrir", waited)
        return
    try:
        _release_single_instance_lock()
        _spawn_detached(command)
    except Exception:
        log().exception("no se pudo lanzar la nueva instancia de Anki")


def _connect_quit_hook() -> None:
    # Una sola conexión para toda la sesión: quien decide si hay reinicio es el
    # dato guardado, no la cantidad de conexiones acumuladas.
    if not _state.quit_hook_connected:
        qconnect(mw.app.aboutToQuit, _on_about_to_quit)
        _state.quit_hook_connected = True


def _on_abort_check() -> None:
    # --- FIX-002 (2026-07-28) --------------------------------------
    # Segunda mitad de la corrección: además de caducar, la orden se retira en
    # cuanto se nota que el cierre no siguió adelante. Anki deshabilita la
    # ventana principal en cuanto el cierre es irreversible, así que si sigue
    # habilitada y no hay ninguna pregunta en pantalla, el cierre se abortó.
    # ---------------------------------------------------------------
    if _state.pending_command is None or sip.isdeleted(mw):
        return
    if not mw.isEnabled():
        # El cierre va en serio; a partir de aquí manda el aviso de salida.
        return
    if QApplication.activeModalWidget() is not None:
        # Hay una pregunta esperando respuesta: todavía puede seguir adelante.
        _schedule_abort_check()
        return
    _clear_pending("el cierre de Anki no llegó a completarse")


def _schedule_abort_check() -> None:
    timer = _state.abort_timer
    if timer is None or sip.isdeleted(timer):
        # Colgado de la ventana principal: si Anki se cierra, Qt lo destruye
        # con ella y nunca dispara sobre objetos que ya no existen.
        timer = QTimer(mw)
        timer.setSingleShot(True)
        qconnect(timer.timeout, _on_abort_check)
        _state.abort_timer = timer
    timer.start(constants.ABORT_CHECK_MS)


# Acciones
# ---------------------------------------------------------------------------


def _ready_to_restart() -> bool:
    """Comprueba que interrumpir a Anki ahora mismo no le hace perder trabajo."""
    if mw.col is None or mw.state in ("startup", "profileManager"):
        return False
    if mw.progress.busy():
        tooltip(tr("busy_warning"), parent=mw)
        return False
    return True


@report_errors
def restart_anki() -> None:
    if _state.pending_command is not None:
        return
    if not _ready_to_restart():
        return

    executable = _resolve_anki_executable()
    if executable is None:
        log().warning(
            "no se identificó el programa de Anki (ejecutable=%r, argv0=%r)",
            sys.executable,
            sys.argv[0] if sys.argv else "",
        )
        warn_user(tr("executable_not_found"))
        return

    # Los datos de la sesión se leen ahora, con todo aún en pie, y no durante
    # el cierre, cuando el perfil ya podría estar descargado.
    _state.pending_command = [executable, *_relaunch_arguments()]
    _state.pending_since = time.monotonic()
    _connect_quit_hook()
    _schedule_abort_check()
    log().info("reinicio solicitado: %r", _state.pending_command)

    tooltip(tr("restarting"), parent=mw)
    try:
        # Cierre idéntico al de un cierre normal de Anki: guarda la colección,
        # respeta la sincronización al cerrar y espera a la copia de seguridad.
        mw.unloadProfileAndExit()
    except Exception:
        # Si el cierre ni siquiera arrancó, no puede quedar un reinicio a medias.
        _clear_pending("el cierre de Anki no llegó a empezar")
        raise


# Registro de los atajos
# ---------------------------------------------------------------------------


def _on_ambiguous_shortcut() -> None:
    log().warning("atajo ambiguo: hay otra acción con la misma combinación")


def registered_shortcuts() -> list[QShortcut]:
    """Atajos que el complemento tiene puestos ahora mismo.

    El diálogo de opciones los necesita para no tomarlos por un conflicto
    consigo mismos al comprobar una combinación.
    """
    return list(_state.registered)


def unregister_shortcuts() -> None:
    # Se destruyen de inmediato, como hace Anki con los suyos: si solo se
    # marcaran para borrar, seguirían respondiendo hasta el siguiente ciclo y
    # se solaparían con los recién creados.
    for shortcut in _state.registered:
        try:
            sip.delete(shortcut)
        except (RuntimeError, TypeError):
            log().debug("no se pudo destruir un atajo ya inexistente")
    _state.registered.clear()


def register_shortcuts() -> None:
    settings = load_settings()
    if not settings.restart_enabled:
        return
    sequence = QKeySequence(settings.restart_shortcut)
    if not shortcuts.is_allowed(sequence, _state.registered):
        # Puede venir de una versión anterior del complemento, o de otro
        # complemento instalado después. Se avisa en lugar de dejar el atajo
        # muerto sin explicación.
        log().warning(
            "atajo descartado por no estar disponible: %r", settings.restart_shortcut
        )
        tooltip(
            tr(
                "shortcut_not_allowed",
                shortcut=shortcuts.display_text(sequence) or settings.restart_shortcut,
            ),
            period=6000,
        )
        return
    shortcut = QShortcut(sequence, mw)
    # Sin esto, dejar la tecla pulsada repetiría la acción.
    shortcut.setAutoRepeat(False)
    qconnect(shortcut.activated, restart_anki)
    qconnect(shortcut.activatedAmbiguously, _on_ambiguous_shortcut)
    _state.registered.append(shortcut)


def reload_shortcuts() -> None:
    unregister_shortcuts()
    register_shortcuts()


@report_errors
def on_main_window_did_init() -> None:
    register_shortcuts()


@report_errors
def on_config_updated(_config: object) -> None:
    # Por si la configuración se cambia desde fuera del diálogo de opciones.
    reload_shortcuts()
