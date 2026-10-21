"""Red de seguridad comun a todo el complemento.

Anki descuelga para siempre cualquier funcion conectada a un hook que lance una
excepcion, y ademas planta un volcado tecnico en pantalla. Por eso toda funcion
conectada a un hook pasa por uno de los dos decoradores de este modulo: el
detalle tecnico va al registro del complemento y la persona ve, como mucho, un
aviso breve en su idioma.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Final, ParamSpec, TypeVar

from aqt import mw
from aqt.utils import tooltip

from .strings import tr

P = ParamSpec("P")
T = TypeVar("T")

# Un mismo fallo puede repetirse en cada tarjeta o en cada movimiento del raton:
# se registra siempre, pero solo se avisa una vez por sitio y minuto.
_NOTICE_INTERVAL_SECONDS: Final[float] = 60.0
_last_notice: dict[str, float] = {}


def get_logger() -> logging.Logger:
    """Registro propio del complemento (Herramientas -> Complementos -> Ver ficheros)."""
    try:
        return mw.addonManager.get_logger(__name__)
    except Exception:
        return logging.getLogger(__name__)


_logger: Final[logging.Logger] = get_logger()


def report(where: str, exc: BaseException) -> None:
    """Anota el fallo y avisa a la persona sin abrumarla."""
    try:
        _logger.exception("fallo en %s", where, exc_info=exc)
    except Exception:
        pass
    now = time.monotonic()
    last = _last_notice.get(where)
    if last is not None and now - last < _NOTICE_INTERVAL_SECONDS:
        return
    _last_notice[where] = now
    try:
        tooltip(tr("hook_error"), period=4000)
    except Exception:
        pass


def guarded(func: Callable[P, None]) -> Callable[P, None]:
    """Para funciones de hook que no devuelven nada."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
        try:
            func(*args, **kwargs)
        except Exception as exc:
            report(func.__name__, exc)

    return wrapper


def guarded_filter(func: Callable[..., T]) -> Callable[..., T]:
    """Para metodos que actuan de filtro de Anki.

    Un filtro recibe el valor a modificar como primer argumento (el primero
    despues de self) y tiene que devolver algo si o si; cuando falla, se devuelve
    ese mismo valor sin tocar y Anki sigue como si el complemento no existiera.
    """

    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> T:
        try:
            return func(instance, *args, **kwargs)
        except Exception as exc:
            report(func.__name__, exc)
            return args[0] if args else instance

    return wrapper
