"""Captura de fallos: aviso breve para la persona, detalle para el registro.

Regla: toda funcion enganchada a un hook de Anki, y toda respuesta a un
boton, se decora con @guarded. Un error sin capturar dentro de un hook le
planta a la persona un volcado tecnico en pantalla y puede dejar el
complemento inservible hasta reiniciar Anki.

El detalle tecnico va al registro propio del complemento
(mw.addonManager.get_logger), nunca a la salida de error: Anki convierte en
ventana de error todo lo que llega a stderr.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar, cast

from aqt import mw
from aqt.utils import tooltip

from . import constants
from .strings import tr

_F = TypeVar("_F", bound=Callable[..., Any])

# Un mismo punto de fallo avisa una sola vez por sesion: si algo se rompe en
# un hook que corre a menudo, la persona no queda sepultada bajo avisos.
_already_notified: set[str] = set()


def logger() -> logging.Logger:
    """Registro propio del complemento."""
    try:
        return mw.addonManager.get_logger(__name__)
    except Exception:
        return logging.getLogger(__name__)


def report(context: str, error: BaseException) -> None:
    """Anota el fallo y avisa a la persona con una frase corta."""
    try:
        logger().exception("fallo en %s: %r", context, error)
    except Exception:
        pass

    if context in _already_notified:
        return
    _already_notified.add(context)
    try:
        tooltip(
            f"{constants.ADDON_DISPLAY_NAME}: {tr('error')}",
            period=constants.TOOLTIP_PERIOD_MS,
        )
    except Exception:
        pass


def guarded(func: _F) -> _F:
    """Envuelve la funcion para que ningun fallo suyo escape hacia Anki."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as error:
            report(getattr(func, "__qualname__", repr(func)), error)
            return None

    return cast(_F, wrapper)
