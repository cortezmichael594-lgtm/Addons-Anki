"""GritMap - mapa de calor del estudio en la pantalla principal de Anki.

Este archivo solo engancha el complemento a Anki. Toda la logica vive en los
demas modulos del paquete.

La comprobacion de mw evita trabajar cuando el modulo se importa fuera de la
interfaz de Anki (por ejemplo, desde una herramienta de linea de ordenes).
"""

from __future__ import annotations

from aqt import mw

if mw is not None:
    from . import controller

    controller.register()
