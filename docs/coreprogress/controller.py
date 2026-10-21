"""Registro de enganches y coordinacion de la barra durante el repaso."""

# Historial de correcciones de este archivo:
# FIX-002 (2026-07-27) — El record se mezclaba entre usuarios y podia fallar al
#                        cambiar de perfil.

from __future__ import annotations

from typing import TYPE_CHECKING

from anki.cards import Card
from anki.collection import OpChanges, OpChangesAfterUndo
from aqt import gui_hooks, mw
from aqt.qt import QTimer
from aqt.theme import theme_manager

from .data import checkpoint_marks
from .effects import (
    CELEBRATION_SPARKLE_MIN_STREAK,
    MIN_CARDS_FOR_CHECKPOINTS,
    RECORD_MIN_STREAK,
    STREAK_MIN_VISIBLE_MS,
    UPDATE_INTERVAL_MS,
    is_celebration_milestone,
)
from .errors import guard, report
from .i18n import record_label, streak_label
from .palettes import StyleBundle, fill_bundle
from .settings import (
    Config,
    load_best_streak,
    load_config,
    migrate_best_streak,
    rollback_best_streak,
    save_best_streak,
)
from .state import SessionState
from .view import (
    build_apply_js,
    build_celebrate_js,
    build_ensure_js,
    build_enter_js,
    build_hide_label_js,
    build_set_dark_js,
    build_show_label_js,
    reviewer_eval,
    reviewer_page_body,
    reviewer_page_head,
)

if TYPE_CHECKING:
    from aqt.reviewer import Reviewer
    from aqt.webview import WebContent


def _log(exc: Exception) -> None:
    report(exc, "controller")


class ProgressBarTracker:
    def __init__(self) -> None:
        self._state = SessionState()
        self._config: Config = load_config()
        self._pending_label: str | None = None
        self._pending_sparkle: bool = False
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.setInterval(UPDATE_INTERVAL_MS)
        self._timer.timeout.connect(self._flush_update)
        self._setup_hooks()
        self._register_config_action()

    def _setup_hooks(self) -> None:
        gui_hooks.state_did_change.append(self._on_state_change)
        gui_hooks.reviewer_did_answer_card.append(self._on_answer_card)
        gui_hooks.reviewer_did_show_question.append(self._on_show_question)
        gui_hooks.reviewer_did_show_answer.append(self._on_show_answer)
        gui_hooks.operation_did_execute.append(self._on_operation_did_execute)
        gui_hooks.state_did_undo.append(self._on_undo)
        gui_hooks.theme_did_change.append(self._on_theme_change)
        gui_hooks.webview_will_set_content.append(self._on_webview_will_set_content)
        gui_hooks.profile_did_open.append(self._on_profile_open)
        gui_hooks.profile_will_close.append(self._on_profile_close)

    def _register_config_action(self) -> None:
        try:
            if mw:
                mw.addonManager.setConfigUpdatedAction(__name__, self._on_config_updated)
        except Exception as exc:
            _log(exc)

    @guard
    def _on_config_updated(self, _new_config: dict[str, object]) -> None:
        self._config = load_config()
        if self._state.active:
            try:
                current = mw.col.decks.current()
                self._state.record_enabled = not self._deck_excluded(
                    int(current["id"]), str(current.get("name", ""))
                )
            except Exception as exc:
                _log(exc)
            self._state.bar_injected = False
            QTimer.singleShot(0, self._do_enter)

    @guard
    def _on_webview_will_set_content(self, web_content: WebContent, context: object | None) -> None:
        """Put the bar's stylesheet and functions inside the reviewer page.

        HISTORIAL: llegaban en un eval posterior a la carga de la pagina; en un
        arranque en frio esa carga tarda y todo aterrizaba tarde sobre la
        primera tarjeta. Solo se toca la ventana de repaso: la vista previa del
        navegador de tarjetas y la pantalla de plantillas se quedan como estan.
        """
        import aqt.reviewer

        if not isinstance(context, aqt.reviewer.Reviewer):
            return
        web_content.head += reviewer_page_head()
        web_content.body += reviewer_page_body()

    @guard
    def _on_profile_open(self) -> None:
        # HISTORIAL: cambiar de perfil no siempre pasa por un cambio de
        # pantalla, y la sesion anterior podia quedar "viva"; si el mazo actual
        # del perfil nuevo tenia el mismo numero interno, la barra reutilizaba
        # los totales del perfil anterior. Cada perfil empieza limpio.
        self._timer.stop()
        self._state.reset()
        self._config = load_config()
        # FIX-002: el record de una version anterior vivia en la configuracion
        # del complemento; aqui pasa a la coleccion recien abierta, que es de
        # este perfil y solo de el.
        migrate_best_streak()

    # --- FIX-002 (2026-07-27) --------------------------------------
    # Sintoma: al cambiar de usuario podia perderse el record de la sesion en
    #   marcha, o intentar guardarse cuando la coleccion ya no estaba.
    # Causa: el record solo se guardaba al SALIR del repaso; cerrar el perfil
    #   (o cambiar de usuario) desde la propia ventana de repaso se saltaba ese
    #   momento.
    # Regla: todo dato que viva en la coleccion se persiste en
    #   profile_will_close, que Anki emite ANTES de cerrarla, y nunca despues.
    # ---------------------------------------------------------------
    @guard
    def _on_profile_close(self) -> None:
        if self._state.active and self._state.record_enabled:
            save_best_streak(self._state.session_max)
        self._timer.stop()
        self._state.reset()

    def _gold_for_style(self) -> bool:
        return self._state.gold_active if self._config.effects_enabled else False

    def _bundle(self) -> StyleBundle:
        return fill_bundle(self._config.theme, self._gold_for_style())

    @guard
    def _on_state_change(self, new_state: str, old_state: str) -> None:
        # HISTORIAL: la sesion solo se cerraba al volver a la lista de mazos o
        # al resumen. Saliendo por otra puerta (cambio de perfil, pantalla de
        # reinicio) la sesion quedaba "viva" con totales viejos, y al volver al
        # mismo mazo la barra seguia con las cuentas de antes. Ahora se cierra
        # al salir del repaso, sea cual sea el destino.
        if new_state == "review":
            self._handle_review_enter()
        elif old_state == "review":
            self._handle_review_exit()

    def _deck_excluded(self, deck_id: int, deck_name: str) -> bool:
        excluded = set(self._config.excluded_decks)
        if not excluded:
            return False
        if deck_id in excluded:
            return True
        try:
            id_to_name = {int(d.id): d.name for d in mw.col.decks.all_names_and_ids()}
            for ex_id in excluded:
                name = id_to_name.get(ex_id)
                if name and (deck_name == name or deck_name.startswith(name + "::")):
                    return True
        except Exception as exc:
            _log(exc)
        return False

    def _handle_review_enter(self) -> None:
        if not (mw and mw.col):
            return
        current = mw.col.decks.current()
        deck_id = int(current["id"])
        deck_name = str(current.get("name", ""))
        if self._state.active and self._state.deck_id == deck_id:
            return
        self._state.reset()
        self._state.deck_id = deck_id
        self._state.active = True
        self._state.best_at_start = load_best_streak()
        self._state.record_enabled = not self._deck_excluded(deck_id, deck_name)
        try:
            counts = mw.col.sched.counts()
            self._state.initial_total = int(counts[0]) + int(counts[1]) + int(counts[2])
        except Exception as exc:
            _log(exc)
            self._state.initial_total = 0
        QTimer.singleShot(0, self._do_enter)

    def _handle_review_exit(self) -> None:
        try:
            if self._state.record_enabled:
                save_best_streak(self._state.session_max)
        except Exception as exc:
            _log(exc)
        self._timer.stop()
        self._state.reset()

    @guard
    def _on_theme_change(self) -> None:
        # HISTORIAL: la barra "adivinaba" el modo mirando la pagina y fallaba
        # cuando el SO y Anki no coincidian (colores del modo contrario,
        # numeros invisibles). Anki emite theme_did_change al alternar el modo
        # noche: se empuja el modo real y el JS solo re-muestrea y repinta.
        if self._state.active and self._state.bar_injected:
            reviewer_eval(build_set_dark_js(bool(theme_manager.night_mode)))

    @guard
    def _do_enter(self) -> None:
        if not self._state.active or self._state.bar_injected:
            return
        if self._state.initial_total == 0:
            return
        cfg = self._config
        show_cp = cfg.checkpoints_enabled and self._state.initial_total >= MIN_CARDS_FOR_CHECKPOINTS
        marks = checkpoint_marks(self._state.initial_total) if show_cp else []
        js = build_enter_js(
            bundle=self._bundle(),
            progress=self._state.progress(),
            bar_height=cfg.bar_height,
            push_down=cfg.push_down,
            show_checkpoints=bool(marks),
            marks=marks,
            dark=bool(theme_manager.night_mode),
            effects=cfg.effects_enabled,
        )
        reviewer_eval(js)
        self._state.bar_injected = True

    @guard
    def _on_show_question(self, card: Card) -> None:
        # HISTORIAL: aqui vivia una deteccion de "tarjeta repetida = deshacer"
        # con falsos positivos en tarjetas de aprendizaje (una fallada
        # reaparece a los ~10 min). El progreso viene de los contadores vivos
        # del planificador y el deshacer tiene su aviso oficial; aqui solo se
        # garantiza que la barra exista y se re-muestrea el fondo (ensure).
        if self._state.bar_injected:
            reviewer_eval(build_ensure_js())
        elif self._state.active:
            self._do_enter()

    @guard
    def _on_show_answer(self, _card: Card) -> None:
        if self._state.active and self._state.bar_injected:
            reviewer_eval(build_hide_label_js(STREAK_MIN_VISIBLE_MS))

    @guard
    def _on_answer_card(self, _reviewer: Reviewer, card: Card, ease: int) -> None:
        if not self._state.active or self._state.initial_total == 0:
            return
        was_correct = ease >= 3
        self._state.register_answer(card.id, was_correct)
        if self._config.effects_enabled and was_correct:
            streak = self._state.correct_streak
            milestone = is_celebration_milestone(streak)
            # HISTORIAL: el record se celebra UNA sola vez por sesion: en
            # el momento exacto de batirlo (max(best+1, minimo), p. ej. 4
            # si el record era 3). Si ese momento coincide con un hito de
            # racha, el record PREVALECE; los hitos posteriores vuelven a
            # mostrar "N seguidas" normal aunque se siga batiendo.
            first_beat = max(self._state.best_at_start + 1, RECORD_MIN_STREAK)
            is_record = (
                self._state.record_enabled
                and streak > self._state.best_at_start
                and streak == first_beat
            )
            if milestone or is_record:
                self._state.pending_celebration = True
                self._pending_label = record_label(streak) if is_record else streak_label(streak)
                self._pending_sparkle = streak >= CELEBRATION_SPARKLE_MIN_STREAK
                if is_record:
                    save_best_streak(self._state.session_max)
        self._schedule_flush()

    @guard
    def _on_operation_did_execute(self, _changes: OpChanges, _handler: object | None) -> None:
        if self._state.active:
            self._schedule_flush()

    @guard
    def _on_undo(self, changes: OpChangesAfterUndo) -> None:
        # HISTORIAL: gui_hooks.state_did_undo se emite exactamente una vez por
        # Ctrl+Z (verificado en aqt/operations/collection.py). Rehacer NO tiene
        # aviso propio, asi que la racha queda conservadora tras un redo.
        # HISTORIAL: este aviso llega al deshacer CUALQUIER cosa, tambien un
        # cambio de nota hecho desde el navegador de tarjetas mientras se
        # repasa. Sin este filtro se descontaba una respuesta que nadie habia
        # deshecho y la racha se rompia sin motivo; solo cuentan las
        # operaciones que tocan la cola de estudio.
        if not self._state.active:
            return
        if not changes.changes.study_queues:
            return
        self._state.pop_last_answer()
        self._state.pending_celebration = False
        self._pending_label = None
        self._pending_sparkle = False
        # Los records se persisten al instante (proteccion anticierre); al
        # deshacer deben bajar tambien, con suelo en el valor con el que
        # empezo la sesion y sin tocar nada desde mazos excluidos.
        if self._state.record_enabled:
            rollback_best_streak(
                max(self._state.best_at_start, self._state.session_max)
            )
        if self._state.bar_injected:
            reviewer_eval(build_hide_label_js(0))
        self._schedule_flush()

    def _schedule_flush(self) -> None:
        if not self._timer.isActive():
            self._timer.start()

    @guard
    def _flush_update(self) -> None:
        if not self._state.active or not self._state.bar_injected:
            return
        progress = self._state.progress()
        bundle = self._bundle()
        reviewer_eval(build_apply_js(bundle, progress))
        if self._state.pending_celebration:
            self._state.pending_celebration = False
            label = self._pending_label
            sparkle = self._pending_sparkle
            self._pending_label = None
            self._pending_sparkle = False
            if self._config.effects_enabled:
                if sparkle:
                    reviewer_eval(build_celebrate_js())
                if label:
                    reviewer_eval(build_show_label_js(label, bundle))

    def config_changed(self) -> None:
        """Re-read the settings and redraw the bar if a session is running."""
        self._on_config_updated({})

    def record_was_reset(self) -> None:
        """Keep a running session coherent after the record is set back to zero.

        Without this, leaving the reviewer would write the old session best
        back into the record the person just cleared.
        """
        self._state.best_at_start = 0
        self._state.session_max = self._state.correct_streak

    def teardown(self) -> None:
        gui_hooks.state_did_change.remove(self._on_state_change)
        gui_hooks.reviewer_did_answer_card.remove(self._on_answer_card)
        gui_hooks.reviewer_did_show_question.remove(self._on_show_question)
        gui_hooks.reviewer_did_show_answer.remove(self._on_show_answer)
        gui_hooks.operation_did_execute.remove(self._on_operation_did_execute)
        gui_hooks.state_did_undo.remove(self._on_undo)
        gui_hooks.theme_did_change.remove(self._on_theme_change)
        gui_hooks.webview_will_set_content.remove(self._on_webview_will_set_content)
        gui_hooks.profile_did_open.remove(self._on_profile_open)
        gui_hooks.profile_will_close.remove(self._on_profile_close)
        self._timer.stop()


_tracker: ProgressBarTracker | None = None


def notify_config_changed() -> None:
    """Called by the settings dialog once new values are saved."""
    if _tracker is not None:
        _tracker.config_changed()


def notify_record_reset() -> None:
    """Called by the settings dialog when the record is cleared."""
    if _tracker is not None:
        _tracker.record_was_reset()


def register() -> None:
    global _tracker
    from .options import setup_menu

    _tracker = ProgressBarTracker()
    setup_menu()