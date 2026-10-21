"""Valores fijos compartidos por el resto de modulos."""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-28) — El atajo por defecto era uno que Anki ya usaba.

from __future__ import annotations

ADDON_DISPLAY_NAME: str = "Always on Top"

# --- FIX-001 (2026-07-28) --------------------------------------
# Sintoma: el atajo por defecto, Ctrl+Shift+T, competia con Anki dentro de la
#          ventana de Anadir, donde Anki lo usa para saltar al campo de
#          etiquetas del editor.
# Causa:   se eligio el atajo por su nombre ("Top") sin comprobar la lista de
#          atajos que Anki ya tiene ocupados.
# Regla:   todo atajo por defecto, y todo atajo que se ofrezca a la persona,
#          pasa antes por shortcuts.is_usable(). Si no lo pasa, no se usa.
# ---------------------------------------------------------------
DEFAULT_SHORTCUT: str = "Ctrl+Shift+O"
CONFIG_KEY_SHORTCUT: str = "shortcut"
TOOLTIP_PERIOD_MS: int = 1500
