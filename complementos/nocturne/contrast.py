"""Alto contraste del sistema (versión 3.5.0): Nocturne se aparta.

Nocturne suaviza a propósito: el texto de noche no pasa de 13,5 de contraste, no
hay blanco ni negro puros y los colores con significado van menos saturados. Es lo
cómodo para casi todos y lo contrario de lo que necesita quien ha pedido a su
sistema más contraste (temas de contraste de Windows 11, «Aumentar contraste» de
macOS, alto contraste de GNOME). Desde Qt 6.10, Qt lo comunica a los programas;
si el sistema lo pide al abrir Anki, Nocturne no pinta nada y deciden Anki y el
sistema. La paleta se puede seguir eligiendo: se guarda y se aplica cuando el
sistema vuelva al contraste normal. Con un Qt anterior, nada cambia.
"""

from __future__ import annotations

from typing import Any

from aqt.qt import QGuiApplication, Qt

_stepped_aside = False


def system_wants_more_contrast() -> bool:
    """True si el sistema pide más contraste (Qt 6.10 o posterior)."""
    try:
        hints: Any = QGuiApplication.styleHints()
        accessibility = getattr(hints, "accessibility", None)
        if accessibility is None:
            return False
        preference = accessibility().contrastPreference()
        return bool(preference == getattr(Qt, "ContrastPreference").HighContrast)
    except Exception:
        return False


def step_aside() -> None:
    global _stepped_aside
    _stepped_aside = True


def stepped_aside() -> bool:
    """True si en esta sesión Nocturne no pinta por el alto contraste del sistema."""
    return _stepped_aside
