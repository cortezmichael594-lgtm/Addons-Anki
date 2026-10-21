"""Lo que ocurre en la pantalla de repaso: botones, insignias de la tarjeta y sonido de acierto.

El estilo y el código de la web entran por webview_will_set_content, incrustados en la
página y antes del primer pintado (nada se inyecta después con JavaScript, para que no haya
un instante con los botones sin estilo).
"""

from __future__ import annotations

import base64
from typing import Final

from anki.cards import Card, CardId
from aqt import gui_hooks
from aqt.reviewer import Reviewer, ReviewerBottomBar
from aqt.webview import WebContent

from . import audio, badges, config, logic
from .errors import guarded, guarded_filter, log_error
from .paths import ADDON_ROOT, USER_FILES_DIR, WEB_DIR

# Contextos de card_will_show que son una tarjeta del repaso (no vista previa ni editor).
_CARD_CONTEXTS: Final[tuple[str, ...]] = ("reviewQuestion", "reviewAnswer")

# Nombre con el que el CSS del complemento pide la tipografía propia, si la hay.
FONT_FAMILY: Final[str] = "ProFeedbackDisplay"
# Archivos aceptados, por orden de preferencia. Si no hay ninguno se usa la tipografía del
# sistema y todo sigue igual de bien.
_FONT_FILENAMES: Final[tuple[str, ...]] = ("ProFeedback.ttf", "Feather Bold.ttf")
# Una tipografía enorme (por ejemplo, una con miles de caracteres CJK) se incrustaría en
# cada página de repaso: por encima de este tamaño se ignora.
_FONT_MAX_BYTES: Final[int] = 1_500_000

_font_css: str | None = None
# Contenido de los archivos de web/, leído una sola vez.
_assets: dict[str, str] = {}
# Insignia ya calculada de la tarjeta que se está mostrando: se guarda para no releer el
# historial al pasar de la pregunta a la respuesta.
_badge_card_id: CardId | None = None
_badge_html: str = ""


# ── tipografía propia (opcional) ─────────────────────────────────────────────
def _build_font_css() -> str:
    for root in (USER_FILES_DIR, ADDON_ROOT):
        for name in _FONT_FILENAMES:
            path = root / name
            try:
                if not path.is_file() or path.stat().st_size > _FONT_MAX_BYTES:
                    continue
                encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            except OSError as error:
                log_error(f"feedback.font[{path.name}]", error)
                continue
            return (
                f"@font-face{{font-family:'{FONT_FAMILY}';"
                f"src:url('data:font/truetype;base64,{encoded}') format('truetype');"
                "font-weight:700;font-style:normal;font-display:swap}"
            )
    return ""


def _font_style_tag() -> str:
    global _font_css
    if _font_css is None:
        _font_css = _build_font_css()
    return f"<style>{_font_css}</style>" if _font_css else ""


# ── ciclo de vida ────────────────────────────────────────────────────────────
def reset() -> None:
    """Olvida lo guardado en memoria y deja listos los sonidos.

    Se llama al abrir un perfil y al guardar los ajustes: lo que dependía de ellos (la
    insignia calculada, la tipografía, los sonidos preparados) se recalcula.
    """
    global _font_css, _badge_card_id
    _font_css = None
    _badge_card_id = None
    audio.refresh()
    settings = config.reload()
    audio.set_volume(settings.soundVolume)
    audio.preload("correct", settings.answerSound)
    audio.preload("deck_finish", settings.deckFinishSound)
    audio.preload("all_finish", settings.allDoneSound)
    audio.preload("deck_perfect", settings.deckPerfectSound)
    audio.preload("all_perfect", settings.allPerfectSound)


def register() -> None:
    gui_hooks.webview_will_set_content.append(_on_webview_will_set_content)
    gui_hooks.reviewer_did_answer_card.append(_on_did_answer)
    gui_hooks.card_will_show.append(_on_card_will_show)


# ── enganches ────────────────────────────────────────────────────────────────
def _read_asset(name: str) -> str:
    """Contenido de web/<name>. Se lee del disco una sola vez."""
    cached = _assets.get(name)
    if cached is None:
        try:
            cached = (WEB_DIR / name).read_text(encoding="utf-8")
        except OSError as error:
            log_error(f"feedback.asset[{name}]", error)
            cached = ""
        _assets[name] = cached
    return cached


def _style_tag(name: str) -> str:
    css = _read_asset(name)
    return f"<style>{css}</style>" if css.strip() else ""


def _script_tag(name: str) -> str:
    js = _read_asset(name)
    return f"<script>{js}</script>" if js.strip() else ""


@guarded
def _on_webview_will_set_content(web_content: WebContent, context: object | None) -> None:
    # --- Incrustado, no enlazado ---
    # El estilo y el código van dentro de la propia página (web_content.head) y no como
    # archivos que Anki sirve por su servidor local: así no dependen de ninguna petición
    # (un bloqueador de anuncios del equipo puede cortar una hoja llamada «buttons.css»
    # servida desde 127.0.0.1), están listos en el primer pintado y la barra inferior mide
    # bien su altura desde el principio.
    settings = config.get()
    if isinstance(context, ReviewerBottomBar):
        if settings.styledButtonsEnabled:
            web_content.head += (
                _font_style_tag() + _style_tag("buttons.css") + _script_tag("buttons.js")
            )
    elif isinstance(context, Reviewer) and settings.flagsEnabled:
        # Solo el repaso: en la vista previa y en el editor de tarjetas no se pone insignia.
        web_content.head += _font_style_tag() + _style_tag("flags.css")


@guarded
def _on_did_answer(reviewer: Reviewer, card: Card, ease: int) -> None:
    global _badge_card_id
    # Respondida la tarjeta, su historial cambia: si vuelve a aparecer, se recalcula.
    _badge_card_id = None
    if config.get().answerSoundEnabled and ease in logic.CORRECT_EASES:
        audio.play("correct", config.get().answerSound)


@guarded_filter
def _on_card_will_show(text: str, card: Card, kind: str) -> str:
    global _badge_card_id, _badge_html
    if kind not in _CARD_CONTEXTS or not config.get().flagsEnabled:
        return text
    # Pregunta y respuesta de la misma tarjeta llevan la misma insignia: el historial se
    # lee solo la primera vez y se reutiliza.
    if card.id != _badge_card_id:
        flag = logic.classify_card(card.col, card)
        _badge_html = badges.badge_html(flag) if flag is not None else ""
        _badge_card_id = card.id
    return _badge_html + text if _badge_html else text
