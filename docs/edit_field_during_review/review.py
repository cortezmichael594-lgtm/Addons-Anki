"""Enganches con la ventana de repaso y la vista previa."""

# Historial de correcciones de este archivo:
# FIX-003 (2026-07-24) — Al contestar la tarjeta justo después de editar, el
#                        complemento seguía trabajando sobre la tarjeta nueva.

from __future__ import annotations

import json
import logging
from typing import Any

from anki.cards import Card
from anki.template import TemplateRenderContext
from aqt import mw
from aqt.browser.previewer import Previewer
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from aqt.webview import AnkiWebView, WebContent

from . import config, constants, logic
from .logic import SaveRequest
from .strings import tr

ReviewContext = Reviewer | Previewer

_logger: logging.Logger | None = None


def _log(where: str, exc: Exception) -> None:
    """Anota el detalle técnico en el registro propio del complemento.

    Se usa el registro de Anki (un archivo por complemento) en lugar de
    imprimir: en Windows la salida de un programa con ventana no se ve, y lo
    que llega a la salida de error Anki lo convierte en un aviso emergente.
    Nunca lanza: si el registro no está disponible, el fallo se ignora en
    silencio para no romper el hook que llamó aquí.
    """
    global _logger
    try:
        if _logger is None:
            _logger = mw.addonManager.get_logger(__name__)
        _logger.error("%s: %r", where, exc)
    except Exception:
        pass


def _webview(context: ReviewContext) -> AnkiWebView | None:
    if isinstance(context, Reviewer):
        return context.web
    return getattr(context, "_web", None)


def _card(context: ReviewContext) -> Card | None:
    if isinstance(context, Reviewer):
        return context.card
    return context.card()


def on_field_filter(
    text: str, field_name: str, filter_name: str, context: TemplateRenderContext
) -> str:
    """Keep templates that use {{edit:Field}} working: the field renders as usual
    and this add-on makes it editable by itself.

    A field_filter runs for every field of every render, so we only claim our
    own "edit" filter and hand back everything else untouched, as the API docs
    recommend. Either way the field text is returned unchanged."""
    if filter_name != "edit":
        return text
    return text


def on_webview_will_set_content(
    web_content: WebContent, context: object | None
) -> None:
    try:
        if not isinstance(context, (Reviewer, Previewer)):
            return
        web_content.css.append(constants.CSS_URL)
        web_content.js.append(constants.JS_URL)
    except Exception as exc:
        _log("webview_will_set_content", exc)


def on_card_will_show(text: str, card: Card, kind: str) -> str:
    try:
        if kind not in constants.REVIEW_CONTEXTS:
            return text
        side = (
            constants.SIDE_QUESTION
            if kind in constants.QUESTION_CONTEXTS
            else constants.SIDE_ANSWER
        )
        data = logic.build_payload(card, side)
        # Preferencia leída aquí, no cacheada, para reflejar un cambio en las
        # opciones sin reiniciar. Con esto el lado web sabe si debe exigir la tecla.
        data["requireModifier"] = config.require_modifier()
        payload = json.dumps(data, ensure_ascii=False)
        # "</" is escaped so a field containing </script> cannot close this tag early.
        payload = payload.replace("</", "<\\/")
        # Prepended: it must run before the card's own scripts rewrite the DOM.
        return f"<script>window.LFE && window.LFE.init({payload});</script>{text}"
    except Exception as exc:
        _log("card_will_show", exc)
        return text


def on_js_message(
    handled: tuple[bool, Any], message: str, context: Any
) -> tuple[bool, Any]:
    if not isinstance(message, str) or not message.startswith(constants.MSG_PREFIX):
        return handled
    if not isinstance(context, (Reviewer, Previewer)):
        return handled
    try:
        request = logic.parse_save_request(message)
    except Exception as exc:
        _log("parse_save_request", exc)
        tooltip(tr("bad_message"))
        return (True, None)
    if request is None:
        return handled

    try:
        _save(request, context)
    except Exception as exc:
        _log("save", exc)
        tooltip(tr("save_failed", error=str(exc)))
    return (True, None)


def _save(request: SaveRequest, context: ReviewContext) -> None:
    def on_saved() -> None:
        try:
            card = _card(context)
            # --- FIX-003 (2026-07-24) --------------------------------------
            # Síntoma: al contestar la tarjeta justo después de editar, el
            #          complemento seguía trabajando sobre la tarjeta nueva.
            # Causa: el guardado termina más tarde que la pulsación, y para
            #        entonces la tarjeta en pantalla ya podía ser otra.
            # Regla: al terminar un trabajo en segundo plano, comprobar que lo
            #        que hay en pantalla sigue siendo aquello sobre lo que se
            #        trabajaba, en vez de dar por hecho que no ha cambiado.
            # ---------------------------------------------------------------
            if card is None or int(card.nid) != int(request.note_id):
                return
            logic.forget_render_cache(card)
            if request.patch:
                _patch(request, context)
        except Exception as exc:
            _log("on_saved", exc)
            tooltip(tr("render_failed"))

    logic.run_save(
        request=request,
        initiator=context,
        on_saved=on_saved,
        on_error=lambda text: tooltip(text),
    )


def _patch(request: SaveRequest, context: ReviewContext) -> None:
    """Send the freshly rendered HTML back so the webview can refresh just the
    edited region, instead of redrawing (and re-running) the whole card."""
    web = _webview(context)
    if web is None:
        return
    try:
        html, stored = logic.render_source(request)
    except Exception as exc:
        _log("render_source", exc)
        tooltip(tr("render_failed"))
        return
    args = ", ".join(
        json.dumps(value)
        for value in (request.index, html, stored, int(request.note_id))
    )
    web.eval(f"window.LFE && window.LFE.patch({args});")
