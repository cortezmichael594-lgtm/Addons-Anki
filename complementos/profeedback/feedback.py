"""Lo que ocurre en la pantalla de repaso: botones, insignias de la tarjeta y sonidos al responder.

El estilo y el código de la web entran por webview_will_set_content, incrustados en la
página y antes del primer pintado (nada se inyecta después con JavaScript, para que no haya
un instante con los botones sin estilo).
"""

# Historial de correcciones de este archivo:
# FIX-007 (2026-11-17): al activar las insignias en mitad de un repaso salían sin su aspecto.

from __future__ import annotations

import base64
from typing import Final

from anki.cards import Card, CardId
from aqt import gui_hooks
from aqt.reviewer import Reviewer, ReviewerBottomBar
from aqt.webview import WebContent

from . import audio, badges, config, logic, look
from .errors import guarded, guarded_filter, log_error
from .paths import ADDON_ROOT, USER_FILES_DIR, WEB_DIR

# Contextos de card_will_show que son una tarjeta del repaso (no vista previa ni editor).
_CARD_CONTEXTS: Final[tuple[str, ...]] = ("reviewQuestion", "reviewAnswer")

# Nombre con el que el CSS del complemento pide la tipografía propia, si la hay.
FONT_FAMILY: Final[str] = "ProFeedbackDisplay"
# Archivo aceptado. Si no está se usa la tipografía del sistema y todo sigue igual de bien.
# 2.6.0 (informe del 2026-11-17, 1.6): sin el alias «Feather Bold.ttf», que es la letra de
# Duolingo y animaba a vestir el complemento de Duolingo.
_FONT_FILENAMES: Final[tuple[str, ...]] = ("ProFeedback.ttf",)
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
    audio.preload("wrong", settings.wrongSound)
    audio.preload("deck_finish", settings.deckFinishSound)
    audio.preload("all_finish", settings.allDoneSound)


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


def _colors_tag() -> str:
    """Las variables de color de botones e insignias (look.py), de día y de noche."""
    return f"<style>{look.css_vars()}</style>"


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
                _font_style_tag() + _colors_tag() + _style_tag("buttons.css") + _script_tag("buttons.js")
            )
    elif isinstance(context, Reviewer):
        # --- FIX-007 (2026-11-17) ---
        # Síntoma: si «Insignias sobre la tarjeta» estaba desmarcada al entrar a repasar y se
        #   marcaba en ese momento, las tarjetas siguientes mostraban la insignia sin su
        #   aspecto (icono y texto sueltos) hasta salir y volver a entrar.
        # Causa: el estilo de la insignia solo se cargaba en la página del repaso si la opción
        #   estaba marcada al cargarla.
        # Regla: el estilo de la insignia se carga siempre en el repaso (es pequeño y no se ve
        #   si no hay insignia); la opción solo decide si se pone la insignia en la tarjeta.
        # Solo el repaso: en la vista previa y en el editor de tarjetas no se pone insignia.
        web_content.head += _font_style_tag() + _colors_tag() + _style_tag("flags.css")


@guarded
def _on_did_answer(reviewer: Reviewer, card: Card, ease: int) -> None:
    global _badge_card_id
    # Respondida la tarjeta, su historial cambia: si vuelve a aparecer, se recalcula.
    _badge_card_id = None
    settings = config.get()
    # Desde la 2.5.0 «Difícil» suena como acierto: solo «Otra vez» lleva el otro sonido, que
    # no juzga, solo dice que se anotó (informe 2.4.0, apartado 8.8).
    if ease in logic.CORRECT_EASES:
        audio.play("correct", settings.answerSound)
    elif ease in logic.WRONG_EASES:
        audio.play("wrong", settings.wrongSound)


@guarded_filter
def _on_card_will_show(text: str, card: Card, kind: str) -> str:
    global _badge_card_id, _badge_html
    if kind not in _CARD_CONTEXTS or not config.get().flagsEnabled:
        return text
    # Pregunta y respuesta de la misma tarjeta llevan la misma insignia: el historial se
    # lee solo la primera vez y se reutiliza.
    if card.id != _badge_card_id:
        flag = logic.classify_card(card.col, card)
        _badge_html = badges.badge_html(flag) if flag is not None else badges.EMPTY_BADGE_HTML
        _badge_card_id = card.id
    return _badge_html + text
