"""Lo que el complemento hace dentro de Anki.

Tres piezas independientes, cada una con la tecnica que su ciclo de vida en Anki
tolera:

- Barra de menu (QMenuBar): se pliega con los metodos propios de Anki
  (hide_menubar / show_menubar). Como Anki vuelve a desplegarla por su cuenta en
  pantalla completa, mientras esta plegada se vigila su tamano y se repliega al
  instante. Ademas, sus acciones con atajo se re-anclan a la ventana principal.
- Barra superior e inferior (vistas web): se colapsa su CONTENIDO con CSS a
  altura cero. Anki decide la altura de cada barra midiendo la pagina, y con ese
  CSS toda medicion suya devuelve 0: es el propio Anki quien las mantiene
  plegadas cuando remide (cambio de tema, de preferencias, de estado), sin
  temporizadores de vigilancia ni peleas con sus animaciones. Al entrar al repaso
  se pliegan ademas a mano para que no haya ni un fotograma con las barras
  puestas.
  Lo que NUNCA se hace es ocultarlas con setVisible(False): entonces la medicion
  de altura devuelve None y Anki programa mw.reset() a 1000 ms, que expulsa del
  repaso.
- Puntero y botones de respuesta: filtro de eventos de la aplicacion y filtros de
  Anki, respectivamente.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-27) - Al abrir un mazo se veia la pantalla de estudio antes de
#                        saltar al repaso automaticamente.
# FIX-002 (2026-07-27) - Al salir del repaso, la ventana daba varios tirones
#                        seguidos mientras volvia cada barra.
# FIX-003 (2026-07-27) - Al salir del mazo se veia aparecer la barra inferior del
#                        repaso (sustituye a parte de FIX-002).
# FIX-004 (2026-07-27) - Al salir del mazo, las barras volvian encima de la
#                        tarjeta, antes de que llegara la pantalla nueva.

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, Literal, override

from anki.cards import Card
from anki.collection import Collection
from aqt import mw
from aqt.deckbrowser import DeckBrowser, DeckBrowserBottomBar
from aqt.overview import Overview, OverviewBottomBar, OverviewContent
from aqt.qt import (
    QWIDGETSIZE_MAX,
    QAction,
    QApplication,
    QEvent,
    QGuiApplication,
    QObject,
    Qt,
    QTimer,
    QWidget,
    qconnect,
)
from aqt.reviewer import Reviewer, ReviewerBottomBar
from aqt.toolbar import BottomWebView, TopToolbar, TopWebView
from aqt.utils import tooltip
from aqt.webview import AnkiWebView, WebContent

from . import constants
from .config import HiderConfig, load_config
from .errors import guarded, guarded_filter, report
from .strings import tr

Ease = Literal[1, 2, 3, 4]
EaseTuple = tuple[bool, Ease]

# Pantallas a las que se sale del repaso. Que Anki les pida contenido significa
# que la pantalla siguiente ya esta lista, que es el momento de devolver las
# barras (FIX-004).
DESTINATION_CONTEXTS: tuple[type, ...] = (
    DeckBrowser,
    DeckBrowserBottomBar,
    Overview,
    OverviewBottomBar,
)


def _webview(attr_name: str) -> AnkiWebView | None:
    view: object = getattr(mw, attr_name, None)
    return view if isinstance(view, AnkiWebView) else None


def _top_bar() -> TopWebView | None:
    view: object = getattr(mw, constants.TOOLBAR_ATTR, None)
    return view if isinstance(view, TopWebView) else None


def _bottom_bar() -> BottomWebView | None:
    view: object = getattr(mw, constants.BOTTOM_BAR_ATTR, None)
    return view if isinstance(view, BottomWebView) else None


def _default_ease(reviewer: Reviewer) -> int:
    """Cual es el boton "Bien" para esta tarjeta, segun el propio repasador."""
    fn = getattr(reviewer, "_defaultEase", None)
    if callable(fn):
        value = fn()
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return constants.GOOD_EASE


class CursorHider(QObject):
    """Oculta el puntero cuando lleva un rato quieto, y lo devuelve al moverlo.

    El filtro se instala en la aplicacion porque es el unico sitio al que llegan
    los movimientos del raton sobre las vistas web. Por eso el trabajo por evento
    se reduce al minimo: mirar el tipo y anotar la hora. El temporizador se rearma
    una vez por periodo de inactividad, no en cada movimiento.
    """

    def __init__(self, idle_ms: int, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._idle_ms: int = max(1, idle_ms)
        self._running: bool = False
        self._cursor_hidden: bool = False
        self._last_activity: float = 0.0
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        qconnect(self._timer.timeout, self._on_timeout)

    def set_idle_ms(self, idle_ms: int) -> None:
        self._idle_ms = max(1, idle_ms)
        if self._running:
            self._note_activity()

    def activate(self) -> None:
        if self._running:
            return
        app = QApplication.instance()
        if app is None:
            return
        app.installEventFilter(self)
        self._running = True
        self._note_activity()

    def deactivate(self) -> None:
        self._timer.stop()
        if self._running:
            app = QApplication.instance()
            if app is not None:
                app.removeEventFilter(self)
            self._running = False
        self._show_cursor()

    def _note_activity(self) -> None:
        self._last_activity = time.monotonic()
        self._timer.start(self._idle_ms)

    @override
    def eventFilter(self, watched: QObject | None, event: QEvent | None) -> bool:
        try:
            if event is not None and event.type() in constants.MOUSE_EVENT_TYPES:
                self._last_activity = time.monotonic()
                if self._cursor_hidden:
                    self._show_cursor()
                if not self._timer.isActive():
                    self._timer.start(self._idle_ms)
        except Exception as exc:
            report("cursor_event_filter", exc)
        return False

    def _on_timeout(self) -> None:
        try:
            idle_ms = int((time.monotonic() - self._last_activity) * 1000)
            remaining = self._idle_ms - idle_ms
            if remaining > constants.CURSOR_TOLERANCE_MS:
                # Hubo movimiento mientras corria: se espera lo que falta.
                self._timer.start(remaining)
                return
            self._hide_cursor()
        except Exception as exc:
            report("cursor_timeout", exc)

    def _hide_cursor(self) -> None:
        if self._cursor_hidden:
            return
        QGuiApplication.setOverrideCursor(Qt.CursorShape.BlankCursor)
        self._cursor_hidden = True

    def _show_cursor(self) -> None:
        # Se retira exactamente el puntero que puso el complemento, ni uno mas:
        # el de espera de Anki durante una operacion larga tambien vive en esa pila.
        if not self._cursor_hidden:
            return
        self._cursor_hidden = False
        QGuiApplication.restoreOverrideCursor()


class MenuBarGuard(QObject):
    """Repliega la barra de menu si Anki la vuelve a desplegar.

    Anki la despliega por su cuenta al salir de pantalla completa o al mover el
    raton fuera de la vista web estando en pantalla completa. Vigilando el propio
    widget se repliega en el mismo instante, sin esperar a la tarjeta siguiente.
    """

    def __init__(self, collapse: Callable[[], None], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._collapse = collapse
        self._bar: QWidget | None = None
        self._busy: bool = False

    def attach(self, bar: QWidget) -> None:
        if self._bar is bar:
            return
        self.detach()
        bar.installEventFilter(self)
        self._bar = bar

    def detach(self) -> None:
        bar, self._bar = self._bar, None
        if bar is None:
            return
        try:
            bar.removeEventFilter(self)
        except Exception:
            # La barra ya no existe; dejar de vigilarla era justo el objetivo.
            pass

    @override
    def eventFilter(self, watched: QObject | None, event: QEvent | None) -> bool:
        try:
            if (
                not self._busy
                and event is not None
                and watched is self._bar
                and event.type() == QEvent.Type.Resize
                and self._bar is not None
                and self._bar.height() > 0
            ):
                self._busy = True
                try:
                    self._collapse()
                finally:
                    self._busy = False
        except Exception as exc:
            report("menu_bar_guard", exc)
        return False


class ChromeHider:
    """Pone y quita las tres barras de la ventana principal."""

    def __init__(self) -> None:
        self._menu_hidden: bool = False
        self._toolbar_hidden: bool = False
        self._bottom_hidden: bool = False
        # Altura de la barra superior justo antes de plegarla, para devolversela
        # al salir sin esperar a que Anki la mida (FIX-002).
        self._toolbar_height: int = 0
        self._menu_actions: list[QAction] = []
        self._menu_guard = MenuBarGuard(self._collapse_menu_bar, mw)

    def apply(self, config: HiderConfig) -> None:
        """Deja las tres barras como pide la configuracion; solo toca lo que cambia."""
        self._set_menu(hidden=config.hide_menu_bar)
        self._set_toolbar(hidden=config.hide_toolbar)
        self._set_bottom(hidden=config.hide_bottom_bar)

    # --- FIX-002 (2026-07-27) --------------------------------------
    # Sintoma: al salir del repaso, la ventana daba varios tirones seguidos.
    # Causa: el menu y la barra superior volvian en momentos distintos: el menu
    #        al instante y la barra superior solo cuando Anki terminaba de medir
    #        su pagina, que es una ida y vuelta a la vista web.
    # Regla: cuando vuelvan varias barras a la vez, hacerlo en la misma vuelta del
    #        bucle de eventos y con la altura que ya tenian guardada. La medicion
    #        de Anki sirve para corregir despues, nunca para decidir cuando
    #        reaparece algo.
    # (La parte de esta correccion que tocaba la barra inferior quedo sustituida
    #  por FIX-003; ver el bloque de _restore_bottom.)
    # ---------------------------------------------------------------
    def leave(self) -> None:
        """Devuelve las tres barras de golpe, en un solo movimiento de ventana.

        Cada una se devuelve a prueba de fallos: si una fallara, las otras tienen
        que volver igualmente. Quedarse sin barra superior en la pantalla
        principal seria mucho peor que el fallo que lo causara.
        """
        for restore in (
            self._restore_bottom,
            lambda: self._set_toolbar(hidden=False),
            lambda: self._set_menu(hidden=False),
        ):
            try:
                restore()
            except Exception as exc:
                report("chrome_leave", exc)

    def reassert(self) -> None:
        """Red de seguridad barata, una vez por tarjeta.

        El CSS mantiene las barras web plegadas por si solo; esto solo cubre el
        caso raro de que alguien reconstruya la pagina de la barra superior en
        mitad del repaso, y sirve de segunda red para la barra de menu.
        """
        if self._toolbar_hidden:
            toolbar = _top_bar()
            if toolbar is not None and toolbar.height() > 0:
                self._collapse_toolbar(toolbar)
        if self._menu_hidden:
            bar = mw.menuBar()
            if bar is not None and bar.height() > 0:
                self._collapse_menu_bar()

    # Barra de menu
    ##########################################################################

    def _collapse_menu_bar(self) -> None:
        hide_fn = getattr(mw, "hide_menubar", None)
        if callable(hide_fn):
            hide_fn()
            return
        bar = mw.menuBar()
        if bar is not None:
            bar.setFixedHeight(0)

    def _expand_menu_bar(self) -> None:
        show_fn = getattr(mw, "show_menubar", None)
        if callable(show_fn):
            show_fn()
        else:
            bar = mw.menuBar()
            if bar is None:
                return
            bar.setMinimumHeight(0)
            bar.setMaximumHeight(QWIDGETSIZE_MAX)
        bar = mw.menuBar()
        if bar is not None:
            bar.update()

    def _set_menu(self, *, hidden: bool) -> None:
        if hidden == self._menu_hidden:
            return
        if hidden:
            self._collapse_menu_bar()
            self._grab_menu_shortcuts()
            bar = mw.menuBar()
            if bar is not None:
                self._menu_guard.attach(bar)
        else:
            self._menu_guard.detach()
            self._release_menu_shortcuts()
            self._expand_menu_bar()
        self._menu_hidden = hidden

    def _grab_menu_shortcuts(self) -> None:
        # Con la barra plegada, Qt deja de despachar los atajos que cuelgan del
        # menu en algunos sistemas; anclados a la ventana funcionan siempre que
        # esta este activa, se vea el menu o no. Solo se anclan los que no
        # estuvieran ya en la ventana, y se apunta cuales para soltar solo esos.
        if self._menu_actions:
            return
        bar = mw.menuBar()
        if bar is None:
            return
        already: set[int] = {id(action) for action in mw.actions()}
        seen: set[int] = set()
        pending: list[QAction] = list(bar.actions())
        while pending:
            action = pending.pop()
            if id(action) in seen:
                continue
            seen.add(id(action))
            menu = action.menu()
            if menu is not None:
                pending.extend(menu.actions())
            if action.shortcut().isEmpty() or id(action) in already:
                continue
            mw.addAction(action)
            self._menu_actions.append(action)

    def _release_menu_shortcuts(self) -> None:
        for action in self._menu_actions:
            try:
                mw.removeAction(action)
            except Exception:
                # Si otro complemento rehizo el menu, esa accion ya no existe:
                # no hay nada que soltar y no debe cortar la restauracion.
                pass
        self._menu_actions.clear()

    # Barra superior
    ##########################################################################

    def _collapse_toolbar(self, toolbar: TopWebView) -> None:
        toolbar.eval(
            constants.inject_style_js(constants.TOOLBAR_STYLE_ID, constants.COLLAPSE_RULES)
        )
        # A mano ademas del CSS: el CSS viaja hasta la pagina y vuelve, y sin esto
        # se veria la barra durante esa ida y vuelta al entrar al repaso.
        toolbar.setFixedHeight(0)

    def _set_toolbar(self, *, hidden: bool) -> None:
        if hidden == self._toolbar_hidden:
            return
        toolbar = _top_bar()
        if toolbar is None:
            return
        if hidden:
            height = toolbar.height()
            if height > 0:
                self._toolbar_height = height
            self._collapse_toolbar(toolbar)
        else:
            toolbar.eval(constants.remove_style_js(constants.TOOLBAR_STYLE_ID))
            toolbar.setMinimumHeight(0)
            toolbar.setMaximumHeight(QWIDGETSIZE_MAX)
            # FIX-002: con la altura de antes, la barra vuelve en el acto y en el
            # mismo fotograma que el menu.
            if self._toolbar_height > 0:
                toolbar.setFixedHeight(self._toolbar_height)
            # Y aun asi se le pide a Anki que la mida: si su altura real hubiera
            # cambiado, la corrige el sin que se note.
            toolbar.adjustHeightToFit()
        self._toolbar_hidden = hidden

    # Barra inferior
    ##########################################################################

    # --- FIX-003 (2026-07-27) --------------------------------------
    # Sustituye a la parte de FIX-002 que tocaba la barra inferior al salir.
    # Sintoma: al salir del mazo, la barra de abajo aparecia con los botones del
    #          repaso y se quedaba a la vista un buen rato.
    # Causa: se le quitaba el plegado al salir para que la medicion de Anki no la
    #        cerrara; con el plegado fuera, la pagina del repaso -que sigue
    #        cargada hasta que llega la pantalla siguiente- se veia entera.
    # Regla: a la barra inferior no se le toca al salir del repaso. Es la unica
    #        barra cuyo contenido cambia de pantalla a pantalla, y Anki ya la abre
    #        sola, de una vez y con el contenido correcto, en cuanto dibuja la
    #        pantalla nueva. Cualquier cosa que se haga antes solo puede enseñar
    #        contenido viejo o una barra vacia.
    # ---------------------------------------------------------------
    def _restore_bottom(self) -> None:
        # A proposito no se toca ni el widget ni su pagina: solo se anota que ya
        # no somos nosotros quienes la mantenemos plegada.
        self._bottom_hidden = False

    def _set_bottom(self, *, hidden: bool) -> None:
        if hidden == self._bottom_hidden:
            return
        bottom = _bottom_bar()
        if bottom is None:
            return
        if hidden:
            bottom.eval(
                constants.inject_style_js(constants.BOTTOM_STYLE_ID, constants.COLLAPSE_RULES)
            )
            # FIX-002: se pliega de golpe, como el menu y la barra superior, en
            # vez de con el hide() animado de Anki. Esa animacion se peleaba con
            # la medicion que Anki hace acto seguido (que con nuestro CSS ya da
            # cero): la barra se encogia, rebotaba y se volvia a encoger.
            # "hidden" es un simple indicador que Anki solo escribe; se deja
            # puesto por si algun otro complemento lo consulta.
            bottom.hidden = True
            bottom.setFixedHeight(0)
        else:
            bottom.eval(constants.remove_style_js(constants.BOTTOM_STYLE_ID))
            # show() remide el contenido (ya sin nuestro CSS) y anima la barra
            # hasta su altura real.
            bottom.show()
        self._bottom_hidden = hidden


class HiderManager:
    """Une la configuracion con los hooks de Anki."""

    # Sin __slots__: PyQt necesita crear referencias debiles al conectar senales a
    # metodos de instancia, y es un singleton en el que slots no aporta nada.

    def __init__(self) -> None:
        self._config: HiderConfig = load_config()
        self._chrome = ChromeHider()
        self._cursor_hider = CursorHider(self._config.cursor_idle_ms, mw)
        self._active: bool = False
        self._skip_auto_start: bool = False
        self._auto_starting: bool = False
        self._allowed_eases: frozenset[int] | None = None
        # No arranca solo: se arma al entrar al resumen del mazo y se rearma en
        # cada repintado suyo.
        self._auto_start_timer = QTimer(mw)
        self._auto_start_timer.setSingleShot(True)
        self._auto_start_timer.setInterval(constants.AUTO_START_SETTLE_MS)
        qconnect(self._auto_start_timer.timeout, self._on_auto_start_due)
        # Seguro por si la pantalla siguiente no llegara a pedir su contenido.
        self._restore_pending: bool = False
        self._restore_timer = QTimer(mw)
        self._restore_timer.setSingleShot(True)
        self._restore_timer.setInterval(constants.CHROME_RESTORE_FALLBACK_MS)
        qconnect(self._restore_timer.timeout, self._on_restore_due)

    # Configuracion
    ##########################################################################

    def reload_config(self) -> None:
        previous = self._config
        self._config = load_config()
        self._cursor_hider.set_idle_ms(self._config.cursor_idle_ms)
        if not self._active:
            return
        self._chrome.apply(self._config)
        if self._config.hide_cursor:
            self._cursor_hider.activate()
        else:
            self._cursor_hider.deactivate()
        if self._config.hide_scrollbar != previous.hide_scrollbar:
            self._apply_scrollbar(hidden=self._config.hide_scrollbar)

    # Entrar y salir del repaso
    ##########################################################################

    def _enter_review(self) -> None:
        # Si se vuelve al repaso antes de que las barras hayan llegado a volver,
        # se cancela su vuelta: asi entrar y salir seguido no mueve nada.
        self._restore_pending = False
        self._restore_timer.stop()
        if self._active:
            return
        self._active = True
        self._skip_auto_start = False
        self._allowed_eases = None
        self._auto_start_timer.stop()
        self._chrome.apply(self._config)
        if self._config.hide_cursor:
            self._cursor_hider.activate()

    # --- FIX-004 (2026-07-27) --------------------------------------
    # Sintoma: al salir del mazo, las barras volvian encima de la tarjeta y la
    #          pantalla nueva llegaba despues, con lo que se veia el salto.
    # Causa: se devolvian nada mas cambiar de estado, y Anki todavia tenia que
    #        pedir los datos de la pantalla siguiente en segundo plano antes de
    #        poder dibujarla.
    # Regla: cambiar de estado no es lo mismo que tener la pantalla nueva lista.
    #        Lo que deba coincidir con la pantalla nueva se hace cuando Anki pide
    #        su contenido (webview_will_set_content), con un temporizador de
    #        seguridad por si ese aviso no llegara nunca: quedarse sin barras
    #        seria mucho peor que un salto.
    # ---------------------------------------------------------------
    def _leave_review(self, *, immediate: bool = False) -> None:
        if not self._active:
            # Ya se salio, pero las barras podian estar aun de camino: si hay
            # prisa (cierre de perfil), vuelven ahora mismo.
            if immediate and self._restore_pending:
                self._restore_chrome()
            return
        self._active = False
        self._allowed_eases = None
        self._cursor_hider.deactivate()
        if immediate:
            self._restore_chrome()
            return
        self._restore_pending = True
        self._restore_timer.start()

    def _restore_chrome(self) -> None:
        self._restore_pending = False
        self._restore_timer.stop()
        self._chrome.leave()

    @guarded
    def _on_restore_due(self) -> None:
        # Red de seguridad: la pantalla siguiente no ha pedido contenido.
        if self._restore_pending:
            self._restore_chrome()

    def _apply_scrollbar(self, *, hidden: bool) -> None:
        web = _webview(constants.MAIN_WEB_ATTR)
        if web is None:
            return
        if hidden:
            web.eval(
                constants.inject_style_js(
                    constants.SCROLLBAR_STYLE_ID, constants.SCROLLBAR_RULES
                )
            )
        else:
            web.eval(constants.remove_style_js(constants.SCROLLBAR_STYLE_ID))

    # Hooks
    ##########################################################################

    @guarded
    def on_state_will_change(self, new_state: str, old_state: str) -> None:
        # Se oculta ANTES de que Anki pinte el repaso: asi no hay ni un fotograma
        # con las barras puestas.
        if new_state == constants.REVIEW_STATE:
            self._auto_starting = False
            self._enter_review()
            return
        if old_state == constants.REVIEW_STATE:
            self._leave_review()
            # Si es la persona quien sale del repaso, no se la devuelve a el.
            self._skip_auto_start = True
        elif self._auto_starting:
            # Se abandona el salto al repaso antes de darlo.
            self._cancel_auto_start()
        self._auto_start_timer.stop()
        if new_state == constants.DECK_BROWSER_STATE:
            self._skip_auto_start = False
        if new_state == constants.OVERVIEW_STATE:
            self._prepare_auto_start()

    @guarded
    def on_reviewer_did_show_question(self, card: Card) -> None:
        if self._active:
            self._chrome.reassert()

    @guarded
    def on_webview_will_set_content(self, web_content: WebContent, context: Any) -> None:
        # FIX-004: la pantalla siguiente ya tiene contenido, es el momento de
        # devolver las barras para que todo cambie a la vez.
        if self._restore_pending and isinstance(context, DESTINATION_CONTEXTS):
            self._restore_chrome()
        # El CSS viaja dentro de la pagina: cualquier pagina nueva nace ya
        # plegada y todas las mediciones de Anki devuelven 0 por si solas.
        if isinstance(context, Reviewer):
            if self._config.hide_scrollbar:
                web_content.head += constants.style_tag(
                    constants.SCROLLBAR_STYLE_ID, constants.SCROLLBAR_RULES
                )
        elif isinstance(context, (ReviewerBottomBar, OverviewBottomBar)):
            # Tambien la del resumen: cuando se va a saltar al repaso, esa barra
            # se dibuja de paso y, sin esto, asomaria y se plegaria acto seguido.
            if self._active and self._config.hide_bottom_bar:
                web_content.head += constants.style_tag(
                    constants.BOTTOM_STYLE_ID, constants.COLLAPSE_RULES
                )
        elif isinstance(context, TopToolbar):
            # La barra superior se dibuja una vez al abrir el perfil; esto solo
            # cubre que alguien la reconstruya en mitad del repaso.
            if self._active and self._config.hide_toolbar:
                web_content.head += constants.style_tag(
                    constants.TOOLBAR_STYLE_ID, constants.COLLAPSE_RULES
                )

    @guarded_filter
    def on_reviewer_will_init_answer_buttons(
        self,
        buttons: tuple[tuple[int, str], ...],
        reviewer: Reviewer,
        card: Card,
    ) -> tuple[tuple[int, str], ...]:
        # Se filtra la lista (ease, etiqueta) con la que Anki construye los botones,
        # en vez de esconderlos por CSS: el numero de botones y el significado de
        # cada "ease" dependen de la tarjeta, asi que un selector fijo podria
        # tapar "Bien".
        allowed = self._compute_allowed_eases(buttons, reviewer)
        self._allowed_eases = allowed
        if not self._config.hide_hard_easy_buttons:
            return buttons
        filtered = tuple((ease, label) for ease, label in buttons if ease in allowed)
        return filtered or buttons

    @guarded_filter
    def on_reviewer_will_answer_card(
        self,
        ease_tuple: EaseTuple,
        reviewer: Reviewer,
        card: Card,
    ) -> EaseTuple:
        # Sin esto, los atajos 2 y 4 seguirian respondiendo con botones invisibles.
        proceed, ease = ease_tuple
        if not proceed or not self._config.hide_hard_easy_buttons:
            return ease_tuple
        allowed = self._allowed_eases
        if allowed is None:
            allowed = frozenset({constants.AGAIN_EASE, _default_ease(reviewer)})
        if ease in allowed:
            return ease_tuple
        tooltip(tr("button_hidden"), period=2000)
        return (False, ease)

    @guarded
    def on_overview_will_render_content(
        self, overview: Overview, content: OverviewContent
    ) -> None:
        if not self._auto_starting:
            return
        # FIX-001: la otra mitad de la correccion. Anki tiene que pintar el
        # resumen si o si, porque es su camino al repaso, pero puede pintarlo
        # vacio: queda el fondo de siempre, sin nombre de mazo, ni recuentos, ni
        # boton, y en unas centesimas lo sustituye la primera tarjeta.
        content.deck = ""
        content.shareLink = ""
        content.desc = ""
        content.table = ""

    @guarded
    def on_overview_did_refresh(self, overview: Overview) -> None:
        if mw.state == constants.REVIEW_STATE:
            if self._config.auto_start_study:
                # Repintado rezagado del resumen encima del repasador: la pagina
                # del resumen queda sobre el repaso, con su boton de estudiar
                # muerto (el puente ya es el del repasador). Se repara reentrando
                # en "review": _reviewCleanup no hace nada si el destino es
                # "review" y show() reinicia _reps, con lo que el repasador se
                # repinta entero y su pagina queda la ultima.
                mw.moveToState(constants.REVIEW_STATE)
            return
        if self._auto_starting:
            # Al entrar en un mazo, Anki repinta el resumen dos veces. Se espera a
            # que pare de repintar antes de saltar: si se saltara entre medias, el
            # segundo repintado caeria encima del repasador.
            self._auto_start_timer.start()

    @guarded
    def _on_auto_start_due(self) -> None:
        if not self._auto_starting:
            return
        col = mw.col
        # Entre la decision y este momento pueden haber cambiado las cosas.
        if (
            mw.state != constants.OVERVIEW_STATE
            or col is None
            or not self._has_due_card(col)
        ):
            self._cancel_auto_start()
            return
        self._auto_starting = False
        # Lo mismo que hace el boton "Estudiar ahora" del resumen.
        col.startTimebox()
        mw.moveToState(constants.REVIEW_STATE)

    # Salto automatico al repaso
    ##########################################################################

    @staticmethod
    def _has_due_card(col: Collection) -> bool:
        # counts() anuncia tarjetas de aprendizaje que vencen mas tarde, asi que
        # no sirve para decidir: entrariamos al repaso y el repasador, al no
        # obtener tarjeta, rebotaria al resumen. Se pregunta a la misma fuente
        # que usa el repasador, que ademas la consulta igual de sincrona.
        # Vale igual para un mazo con submazos: mira el mazo seleccionado y todo
        # lo que cuelga de el, como hace Anki.
        if not col.v3_scheduler():
            # Con el planificador antiguo el repaso ni siquiera arranca.
            return False
        return bool(col.sched.get_queued_cards(fetch_limit=1).cards)

    # --- FIX-001 (2026-07-27) --------------------------------------
    # Sintoma: al abrir un mazo con el salto automatico puesto, la pantalla de
    #          estudio (nombre del mazo, recuentos y boton) aparecia cerca de un
    #          segundo antes de la primera tarjeta.
    # Causa: el salto se decidia en overview_did_refresh, que Anki lanza DESPUES
    #        de pintar el resumen; daba tiempo de sobra a verlo entero, con sus
    #        barras, hasta que la pagina del repasador terminaba de cargar.
    # Regla: lo que no deba verse se decide en state_will_change, que corre antes
    #        de que Anki pinte la pantalla nueva. Los hooks con "did" en el nombre
    #        solo sirven para reaccionar a algo que ya esta en pantalla.
    # ---------------------------------------------------------------
    def _prepare_auto_start(self) -> None:
        """Decide, al entrar al resumen, si se va a saltar al repaso.

        Se decide aqui, antes de que Anki pinte nada, para poder esconder ya las
        barras y pintar el resumen vacio: asi la persona pasa de la lista de
        mazos a la tarjeta sin ver por el camino la pantalla de estudio.
        """
        self._auto_starting = False
        if not self._config.auto_start_study or self._skip_auto_start:
            return
        col = mw.col
        if col is None or not self._has_due_card(col):
            return
        self._auto_starting = True
        self._enter_review()
        self._auto_start_timer.start()

    def _cancel_auto_start(self) -> None:
        if not self._auto_starting:
            return
        self._auto_starting = False
        self._auto_start_timer.stop()
        self._leave_review()
        if mw.state == constants.OVERVIEW_STATE and mw.col is not None:
            # El resumen se habia pintado vacio contando con saltar al repaso:
            # como nos quedamos en el, hay que pintarlo de verdad.
            mw.overview.refresh()

    @guarded
    def on_profile_will_close(self) -> None:
        # Aqui no se difiere nada: no va a haber pantalla siguiente que esperar.
        self._auto_start_timer.stop()
        self._auto_starting = False
        self._leave_review(immediate=True)

    @guarded
    def on_profile_did_open(self) -> None:
        # Cambio de usuario: se parte de cero y se relee la configuracion, que es
        # comun a todos los perfiles pero puede haber cambiado por el camino.
        self._auto_start_timer.stop()
        self._auto_starting = False
        self._skip_auto_start = False
        self._leave_review(immediate=True)
        self._config = load_config()
        self._cursor_hider.set_idle_ms(self._config.cursor_idle_ms)

    # Auxiliares
    ##########################################################################

    def _compute_allowed_eases(
        self, buttons: tuple[tuple[int, str], ...], reviewer: Reviewer
    ) -> frozenset[int]:
        """Que botones se quedan: el primero ("De nuevo") y "Bien".

        "Bien" es siempre el penultimo de las listas que arma Anki, tenga la
        tarjeta dos, tres o cuatro botones. Solo si otro complemento ha anadido
        botones se pregunta al repasador cual considera el suyo por defecto.
        """
        eases = [ease for ease, _label in buttons]
        if len(eases) < 3:
            # Con dos botones no hay nada que ocultar.
            return frozenset(eases)
        good = eases[-2]
        if len(eases) > 4:
            default = _default_ease(reviewer)
            if default in eases:
                good = default
        return frozenset({eases[0], good})


_active_manager: HiderManager | None = None


def set_active_manager(manager: HiderManager) -> None:
    global _active_manager
    _active_manager = manager


def reload_active_manager() -> None:
    if _active_manager is not None:
        _active_manager.reload_config()
