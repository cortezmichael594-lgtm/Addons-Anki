"""Registro tecnico y proteccion de los puntos de entrada del complemento.

Anki convierte en una ventana de error cualquier cosa que llegue a la salida
de error estandar, y una excepcion sin capturar dentro de un hook puede dejar
el complemento inservible hasta reiniciar. Por eso:

  * el detalle tecnico va al registro propio del complemento
    (mw.addonManager.get_logger), que la persona puede abrir desde
    Herramientas -> Complementos si alguna vez hace falta;
  * cada funcion conectada a un hook se envuelve con @guarded, que atrapa la
    excepcion, la registra y devuelve un valor de reserva.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

_LOGGER_NAME = "addon.gritmap"
_logger: logging.Logger | None = None


def logger() -> logging.Logger:
    """Registro propio del complemento.

    get_logger existe en Anki 26.09; si una version distinta no lo expusiera,
    se cae al logger equivalente por nombre, que es exactamente lo que Anki
    construye internamente ("addon." + nombre del paquete).
    """
    global _logger
    if _logger is not None:
        return _logger
    try:
        from aqt import mw

        get_logger = getattr(mw.addonManager, "get_logger", None)
        if callable(get_logger):
            _logger = get_logger(__name__)
            return _logger
    except Exception:
        pass
    _logger = logging.getLogger(_LOGGER_NAME)
    return _logger


def log_exception(where: str, exc: BaseException) -> None:
    """Anota una excepcion con su traza completa, sin molestar a la persona."""
    try:
        logger().error("%s: %r", where, exc, exc_info=exc)
    except Exception:
        pass


def guarded(default: Any = None) -> Callable[[F], F]:
    """Protege una funcion conectada a un hook.

    Si algo falla, la excepcion queda registrada y la funcion devuelve
    `default`, de modo que Anki sigue funcionando con normalidad aunque el
    complemento no pueda dibujar su parte.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                log_exception(func.__qualname__, exc)
                return default

        return cast(F, wrapper)

    return decorator


def guarded_filter(func: F) -> F:
    """Variante para filtros: ante un fallo devuelve intacto su primer valor.

    Los filtros de Anki (por ejemplo webview_did_receive_js_message) deben
    devolver el valor que recibieron si no lo tratan; devolver otra cosa
    romperia la cadena de complementos.
    """

    @wraps(func)
    def wrapper(first: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(first, *args, **kwargs)
        except Exception as exc:
            log_exception(func.__qualname__, exc)
            return first

    return cast(F, wrapper)
