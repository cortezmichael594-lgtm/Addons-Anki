"""Unico punto por el que pasan los textos visibles.

Reparto:
- Lo que Anki ya traduce a todos sus idiomas (titulo de la ventana de opciones,
  aviso de valores restaurados, nombres de los botones de respuesta) se le pide a
  Anki. Los botones Aceptar / Cancelar / Restaurar valores predeterminados los
  traduce Qt por su cuenta, asi que el dialogo no les pone texto.
- Las frases propias del complemento salen de i18n.py.
"""

from __future__ import annotations

from anki.lang import without_unicode_isolation
from aqt.utils import tr as anki_tr

from . import constants, i18n

# Reserva por si se pide un texto antes de que Anki tenga listo su traductor.
_FALLBACK_BUTTONS: dict[str, str] = {
    "again": "Again",
    "good": "Good",
    "hard": "Hard",
    "easy": "Easy",
}


def answer_button_names() -> dict[str, str]:
    """Nombres de los botones de respuesta tal y como los escribe Anki."""
    try:
        return {
            "again": anki_tr.studying_again(),
            "good": anki_tr.studying_good(),
            "hard": anki_tr.studying_hard(),
            "easy": anki_tr.studying_easy(),
        }
    except Exception:
        return dict(_FALLBACK_BUTTONS)


def tr(key: str, **values: str) -> str:
    """Frase propia del complemento en el idioma activo de Anki."""
    text = i18n.text(key)
    if "{" not in text:
        return text
    data = answer_button_names()
    data.update(values)
    try:
        return text.format(**data)
    except (KeyError, IndexError, ValueError):
        return text


def options_title() -> str:
    """Titulo de la ventana de opciones, con el mismo texto que usa Anki."""
    try:
        return without_unicode_isolation(
            anki_tr.addons_config_window_title(name=constants.ADDON_NAME)
        )
    except Exception:
        return constants.ADDON_NAME


def restored_defaults() -> str:
    """Aviso de "valores restaurados", el mismo que muestra Anki."""
    try:
        return anki_tr.addons_restored_defaults()
    except Exception:
        return "Restored defaults."
