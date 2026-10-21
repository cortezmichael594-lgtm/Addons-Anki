"""Única capa sobre la configuración de Anki.

Toda lectura pasa por aquí y devuelve el valor recomendado cuando la clave
falta o tiene un tipo que no toca: así el complemento arranca igual la primera
vez, con una configuración guardada por una versión anterior o con un archivo
retocado a mano.
"""

# Historial de correcciones de este archivo:
# FIX-003 (2026-07-28) — Se retiró el atajo para cerrar Anki, que duplicaba Ctrl+Q.

from __future__ import annotations

from dataclasses import dataclass

from aqt import mw

from . import constants


@dataclass(slots=True)
class AddonSettings:
    restart_enabled: bool = constants.DEFAULT_RESTART_ENABLED
    restart_shortcut: str = constants.DEFAULT_SHORTCUT_RESTART


def _read_bool(raw: dict[str, object], key: str, default: bool) -> bool:
    value = raw.get(key, default)
    return value if isinstance(value, bool) else default


def _read_str(raw: dict[str, object], key: str, default: str) -> str:
    value = raw.get(key, default)
    return value if isinstance(value, str) else default


def load_settings() -> AddonSettings:
    raw: object = mw.addonManager.getConfig(constants.ADDON_MODULE)
    if not isinstance(raw, dict):
        return AddonSettings()
    return AddonSettings(
        restart_enabled=_read_bool(
            raw,
            constants.CONFIG_KEY_RESTART_ENABLED,
            constants.DEFAULT_RESTART_ENABLED,
        ),
        restart_shortcut=_read_str(
            raw,
            constants.CONFIG_KEY_RESTART_SHORTCUT,
            constants.DEFAULT_SHORTCUT_RESTART,
        ),
    )


# --- FIX-003 (2026-07-28) --------------------------------------
# Síntoma: quedaban guardados los ajustes de un atajo para cerrar Anki que ya
#          no existe.
# Causa: al retirar esa opción, la configuración guardada seguía trayendo sus
#        dos claves.
# Regla: al guardar se escriben solo las claves que el complemento usa hoy;
#        las sobrantes de versiones anteriores desaparecen solas y nunca se
#        leen. No hace falta migrarlas ni conservarlas.
# ---------------------------------------------------------------
def save_settings(settings: AddonSettings) -> None:
    mw.addonManager.writeConfig(
        constants.ADDON_MODULE,
        {
            constants.CONFIG_KEY_RESTART_ENABLED: settings.restart_enabled,
            constants.CONFIG_KEY_RESTART_SHORTCUT: settings.restart_shortcut,
        },
    )
