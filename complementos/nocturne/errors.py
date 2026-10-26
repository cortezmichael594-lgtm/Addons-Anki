"""Registro técnico y protección de los enganches con Anki.

Cada función que Anki llama en nuestro nombre pasa por el decorador ``guard``:
si algo falla, el detalle va al registro propio del complemento (un archivo que
Anki reserva para él) y Anki sigue funcionando con su apariencia habitual.

Aquí no se abren ventanas de aviso a propósito: un tema de colores no debe
interrumpir jamás un repaso por un fallo cosmético. Desde la versión 3.5.0 se
cuentan los fallos de la sesión, y la ventana de configuración lo dice en una
línea, con un botón para abrir la carpeta del registro, solo si hubo alguno.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_logger: logging.Logger | None = None
_failures = 0


def failures() -> int:
    """Fallos registrados desde que arrancó Anki."""
    return _failures


def note_failure(message: str, *args: Any) -> None:
    """Anota un fallo en el registro y lo cuenta."""
    global _failures
    _failures += 1
    get_logger().exception(message, *args)


def logs_folder() -> str | None:
    """Carpeta donde Anki guarda el registro de este complemento, si se sabe."""
    try:
        from aqt import mw

        return str(mw.addonManager.logs_folder(__name__))
    except Exception:
        return None


def get_logger() -> logging.Logger:
    """Registro propio del complemento, con reserva si Anki no está presente.

    ``mw.addonManager.get_logger`` escribe en un archivo del complemento en vez
    de en la salida de error, que Anki convertiría en una ventana de error.
    """
    global _logger
    if _logger is None:
        try:
            from aqt import mw

            _logger = mw.addonManager.get_logger(__name__)
        except Exception:
            # Importado fuera de Anki, o API cambiada: un registro normal basta.
            _logger = logging.getLogger(__name__)
    return _logger


def guard(func: F) -> F:
    """Envuelve una función de enganche para que nunca propague una excepción.

    Solo debe usarse en enganches que no devuelven valor: si el enganche fuera
    un filtro, devolver ``None`` tras un fallo rompería la cadena de Anki.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            note_failure("fallo en %s", func.__name__)
            return None

    return wrapper  # type: ignore[return-value]


def guard_filter(func: F) -> F:
    """Como ``guard``, pero para filtros: si algo falla, devuelve intacto el primer
    argumento, para que la cadena de Anki siga con el valor que recibió."""

    @functools.wraps(func)
    def wrapper(value: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(value, *args, **kwargs)
        except Exception:
            note_failure("fallo en %s", func.__name__)
            return value

    return wrapper  # type: ignore[return-value]
