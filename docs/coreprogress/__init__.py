from __future__ import annotations

from aqt import mw

from . import controller

if mw is not None:
    controller.register()
