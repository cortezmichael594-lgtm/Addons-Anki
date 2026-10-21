"""Identidad del complemento, claves de configuración y valores por defecto."""

# Historial de correcciones de este archivo:
# FIX-003 (2026-07-28) — Se retiró el atajo para cerrar Anki, que duplicaba Ctrl+Q.

from __future__ import annotations

from typing import Final

# Nombre de la carpeta del complemento dentro de Anki. Es el identificador que
# esperan getConfig, writeConfig, setConfigAction y get_logger; se deduce del
# módulo raíz para que siga siendo correcto aunque la carpeta se renombre.
ADDON_MODULE: Final[str] = __name__.split(".", 1)[0]

# Nombre visible. Coincide con "name" en manifest.json, que es como aparece el
# complemento en la lista de Anki y como se titula su panel de opciones.
ADDON_NAME: Final[str] = "Restart"

# --- FIX-003 (2026-07-28) --------------------------------------
# Síntoma: el complemento ofrecía un segundo atajo para cerrar Anki que no
#          aportaba nada.
# Causa: se añadió sin comprobar antes que Anki ya trae Ctrl+Q para salir, así
#        que eran dos maneras de hacer lo mismo y una opción de más que
#        mantener.
# Regla: antes de añadir una acción al complemento, comprobar si Anki ya la
#        hace de serie; si la hace, no duplicarla. Aquí en concreto: no volver
#        a añadir un atajo para cerrar Anki.
# ---------------------------------------------------------------
CONFIG_KEY_RESTART_ENABLED: Final[str] = "restart_enabled"
CONFIG_KEY_RESTART_SHORTCUT: Final[str] = "restart_shortcut"

DEFAULT_RESTART_ENABLED: Final[bool] = True
DEFAULT_SHORTCUT_RESTART: Final[str] = "Ctrl+R"

# Margen máximo entre pedir el reinicio y que Anki empiece a apagarse de
# verdad. Cubre de sobra una sincronización y una copia de seguridad largas;
# pasado ese tiempo, un cierre ya no cuenta como parte de aquel reinicio.
RELAUNCH_WINDOW_SECONDS: Final[float] = 300.0

# Cada cuánto se comprueba si el cierre pedido se quedó a medias.
ABORT_CHECK_MS: Final[int] = 5_000
