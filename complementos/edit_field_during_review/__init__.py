from __future__ import annotations

from anki.hooks import field_filter
from aqt import gui_hooks, mw

from . import constants
from .dialogs import open_options
from .review import (
    on_card_will_show,
    on_field_filter,
    on_js_message,
    on_webview_will_set_content,
)


def _register() -> None:
    mw.addonManager.setWebExports(__name__, constants.WEB_EXPORTS)
    mw.addonManager.setConfigAction(__name__, open_options)
    field_filter.append(on_field_filter)
    gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
    gui_hooks.card_will_show.append(on_card_will_show)
    gui_hooks.webview_did_receive_js_message.append(on_js_message)


_register()
