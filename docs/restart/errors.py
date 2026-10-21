"""Captura de errores: aviso breve para la persona y detalle técnico al registro.

Anki convierte cualquier excepción sin capturar dentro de un hook en una ventana
de volcado técnico, y una función de hook que revienta puede dejar el
complemento inservible hasta reiniciar. Todo lo que Anki llame directamente
pasa por el decorador de este módulo.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from aqt import mw
from aqt.utils import showWarning

from . import constants
from .strings import tr

_Func = TypeVar("_Func", bound=Callable[..., Any])


def log() -> logging.Logger:
    """Registro propio del complemento, en la carpeta de registros de Anki.

    Se usa en lugar de escribir a la salida de error, porque Anki convierte lo
    que llega a stderr en una ventana de error para la persona usuaria.
    """
    return mw.addonManager.get_logger(constants.ADDON_MODULE)


def warn_user(message: str) -> None:
    """Aviso breve, con el aspecto de los avisos del propio Anki.

    El título es el nombre del complemento, igual que aparece en la lista de
    complementos, para que se sepa de dónde sale el aviso sin traducir nada.
    """
    showWarning(message, parent=mw, title=constants.ADDON_NAME)


def report_errors(func: _Func) -> _Func:
    """Envuelve una función llamada por Anki (hook, atajo, acción de menú)."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            log().exception("error en %s", func.__qualname__)
            warn_user(tr("unexpected_error", error=str(exc)))
            return None

    return wrapper  # type: ignore[return-value]
