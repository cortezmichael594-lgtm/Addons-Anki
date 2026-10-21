"""Registro tecnico y proteccion de las funciones enganchadas a Anki.

Dos motivos para que este modulo exista:

1. Anki convierte TODO lo que llega a la salida de error en una ventana de
   error para la persona. Un complemento que imprime ahi le planta un volcado
   tecnico en pantalla por algo que no puede resolver. El detalle tecnico va a
   un archivo de registro propio del complemento
   (mw.addonManager.get_logger, qt/aqt/addons.py), que ella puede abrir por
   curiosidad y nosotros por diagnostico.
2. Una excepcion sin capturar dentro de un enganche puede dejar el
   complemento inservible hasta reiniciar. El decorador de aqui evita repetir
   el mismo try/except en cada funcion.

El aviso visible es UNO por sesion, no uno por tarjeta: la barra es un adorno
y un fallo repetido no debe convertirse en una lluvia de avisos encima del
repaso. El texto es el propio de Anki (tr.errors_may_be_addon), ya traducido a
todos sus idiomas, asi que aqui no se inventa ningun texto.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from aqt import mw

# Reserva para el caso improbable de que el registro de Anki no este
# disponible todavia (arranque muy temprano): nunca dejar que el propio
# registro sea la causa de un fallo.
_FALLBACK_LOGGER = logging.getLogger("coreprogress")

_notified = False

F = TypeVar("F", bound=Callable[..., Any])


def logger() -> logging.Logger:
    """El registro propio del complemento, con reserva si aun no existe."""
    try:
        if mw is not None:
            return mw.addonManager.get_logger(__name__)
    except Exception:
        pass
    return _FALLBACK_LOGGER


def _notify_once() -> None:
    """Un unico aviso breve por sesion, con el texto traducido de Anki."""
    global _notified
    if _notified:
        return
    _notified = True
    try:
        from aqt.utils import tooltip, tr

        tooltip(tr.errors_may_be_addon())
    except Exception:
        pass


def report(exc: BaseException, where: str = "") -> None:
    """Manda el detalle tecnico al registro y avisa una sola vez."""
    try:
        logger().exception("error en %s: %r", where or "coreprogress", exc)
    except Exception:
        pass
    _notify_once()


def guard(func: F) -> F:
    """Envuelve una funcion enganchada a Anki con su try/except.

    Solo para funciones cuyo valor de retorno no usa Anki (los enganches de
    aviso). Los filtros, que deben devolver su primer argumento, no pueden
    envolverse asi.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            report(exc, getattr(func, "__qualname__", ""))
            return None

    return wrapper  # type: ignore[return-value]
