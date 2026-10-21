"""Única capa sobre getConfig / writeConfig, con valores por defecto seguros.

Toda lectura de configuración pasa por aquí, de modo que si a la
configuración guardada por una versión anterior le falta una clave, se
devuelve el valor por defecto en lugar de fallar.
"""

from __future__ import annotations

from aqt import mw

# Valores por defecto. Deben coincidir con config.json, que es lo que viaja
# en el paquete y lo que Anki muestra si nunca se ha guardado nada.
DEFAULTS: dict[str, object] = {
    # Exigir mantener una tecla (Ctrl / ⌘) al hacer clic para empezar a editar.
    # Activado de fábrica: evita entrar en edición sin querer al seleccionar texto.
    "require_modifier": True,
}

KEY_REQUIRE_MODIFIER = "require_modifier"


def _raw() -> dict[str, object]:
    conf = mw.addonManager.getConfig(__name__)
    if not isinstance(conf, dict):
        # getConfig devuelve None si falta config.json; nunca debería pasar
        # porque viaja en el paquete, pero así el complemento sigue funcionando.
        return dict(DEFAULTS)
    return conf


def get(key: str) -> object:
    return _raw().get(key, DEFAULTS.get(key))


def require_modifier() -> bool:
    return bool(get(KEY_REQUIRE_MODIFIER))


def set_require_modifier(value: bool) -> None:
    conf = _raw()
    conf[KEY_REQUIRE_MODIFIER] = bool(value)
    mw.addonManager.writeConfig(__name__, conf)
