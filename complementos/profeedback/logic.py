"""Lógica del complemento, sin ventanas.

Este módulo importa solo `anki` (nunca `aqt` ni Qt) y recibe la colección como parámetro:
así se puede probar con una colección temporal, sin abrir Anki y sin tocar jamás la
colección real de la persona.

Qué decide:
- qué insignia lleva una tarjeta (nueva, ejercicio difícil, error anterior);
- cuándo termina una sesión de repaso y qué celebración toca (de mazo o de todo el día,
  normal o perfecta).
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-10-13): la celebración podía saltar al abrir un mazo ya terminado.
# FIX-003 (2026-10-13): el «día perfecto» se contaba mal (medianoche, perfiles, otros dispositivos).

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final, Literal

from anki.cards import Card, CardId
from anki.collection import Collection, SearchNode
from anki.consts import CARD_TYPE_NEW

from .strings import FlagKey

# Respuestas de Anki: 1 = Otra vez, 2 = Difícil, 3 = Bien, 4 = Fácil.
AGAIN: Final[int] = 1
HARD: Final[int] = 2
# Las que cuentan como acierto: «Bien» y «Fácil». «Difícil» ya no es sesión perfecta.
CORRECT_EASES: Final[frozenset[int]] = frozenset({3, 4})

# Cuántas respuestas (mazo) o tarjetas distintas (todo el día) hacen falta para que el
# confeti y el brillo dorado tengan sentido. El sonido de fin suena siempre.
DECK_MIN_ANSWERS: Final[int] = 5
DAY_MIN_CARDS: Final[int] = 20

HISTORY_FOR_BADGES: Final[int] = 3


# ── insignias de la tarjeta ──────────────────────────────────────────────────
def classify(is_new: bool, recent: Sequence[int]) -> FlagKey | None:
    """Qué insignia toca, a partir de si es nueva y de sus últimas respuestas.

    `recent` va de la respuesta más reciente a la más antigua.
    - Tarjeta nueva: nunca se ha respondido.
    - Ejercicio difícil: las tres últimas respuestas fueron «Otra vez».
    - Error anterior: «Otra vez» en alguna de las dos últimas.
    """
    if is_new:
        return "new_card"
    if len(recent) >= HISTORY_FOR_BADGES and all(ease == AGAIN for ease in recent):
        return "hard_exercise"
    if any(ease == AGAIN for ease in recent[:2]):
        return "previous_mistake"
    return None


def recent_eases(
    col: Collection, card_id: CardId, limit: int = HISTORY_FOR_BADGES
) -> tuple[int, ...]:
    """Últimas respuestas de una tarjeta, de la más reciente a la más antigua.

    Se descartan las entradas sin botón (button_chosen == 0): son cambios manuales de
    fecha o reprogramaciones, no respuestas de la persona.
    """
    # La API de la colección da el historial con lo más reciente primero (APR-032).
    entries = col.get_review_logs(card_id)
    eases = [entry.button_chosen for entry in entries if entry.button_chosen > 0]
    return tuple(eases[:limit])


def classify_card(col: Collection, card: Card) -> FlagKey | None:
    """Insignia de una tarjeta; solo lee el historial si hace falta."""
    if card.type == CARD_TYPE_NEW:
        return "new_card"
    return classify(False, recent_eases(col, card.id))


# ── sesión de repaso ─────────────────────────────────────────────────────────
@dataclass(slots=True)
class ReviewSession:
    """Lo que ha pasado desde que se entró a repasar, y si acaba de terminar.

    Una sesión empieza al entrar en el repaso y termina, a efectos de celebración, solo
    cuando se vuelve a la pantalla del mazo (overview) habiendo respondido tarjetas.
    """

    answers: int = 0
    perfect: bool = True
    _ended_on_overview: bool = False

    def state_changed(self, new_state: str, old_state: str) -> None:
        if new_state == "review":
            self.answers = 0
            self.perfect = True
            self._ended_on_overview = False
        elif old_state == "review":
            # --- FIX-002 (2026-10-13) ---
            # Síntoma: tras repasar y salir a la lista de mazos (sin terminar), al abrir
            #   más tarde un mazo ya terminado saltaban el sonido y el confeti.
            # Causa: la bandera «acabo de repasar» no se apagaba al salir por otro camino.
            # Regla: solo la vuelta del repaso a la pantalla del mazo puede celebrar; salir
            #   por cualquier otra pantalla descarta la sesión.
            self._ended_on_overview = new_state == "overview" and self.answers > 0
            if not self._ended_on_overview:
                self.reset()

    def record(self, ease: int) -> None:
        self.answers += 1
        if ease not in CORRECT_EASES:
            self.perfect = False

    def take_ended(self) -> bool:
        """¿Acaba de terminar una sesión? Devuelve True una sola vez por sesión."""
        ended = self._ended_on_overview
        self._ended_on_overview = False
        return ended

    def reset(self) -> None:
        self.answers = 0
        self.perfect = True
        self._ended_on_overview = False


# ── lo que queda por repasar y lo repasado hoy ───────────────────────────────
@dataclass(frozen=True, slots=True)
class Remaining:
    """Cuántas tarjetas quedan en el mazo actual y en toda la colección."""

    deck: int
    total: int


@dataclass(frozen=True, slots=True)
class DaySummary:
    """Lo repasado hoy en toda la colección, según el historial de Anki."""

    cards: int
    slips: int  # tarjetas con alguna respuesta «Otra vez» o «Difícil» hoy


def remaining_cards(col: Collection) -> Remaining:
    tree = col.sched.deck_due_tree()
    total = tree.new_count + tree.learn_count + tree.review_count
    return Remaining(deck=sum(col.sched.counts()), total=total)


def day_summary(col: Collection) -> DaySummary:
    """Tarjetas repasadas hoy y cuántas tuvieron algún fallo («Otra vez» o «Difícil»)."""
    # --- FIX-003 (2026-10-13) ---
    # Síntoma: el «día perfecto» empezaba a medianoche en vez de al cambiar de día Anki,
    #   mezclaba los perfiles, se perdía si Anki se cerraba de golpe y no contaba lo
    #   repasado en otros dispositivos.
    # Causa: el complemento llevaba su propia cuenta (en la configuración, común a todos los
    #   perfiles) en vez de preguntar al historial de Anki.
    # Regla: lo que ya está en el historial de la colección se lee de ahí (búsqueda rated:1),
    #   que respeta el cambio de día de Anki, es de cada perfil y viaja con la sincronización.
    today = SearchNode.Rated(days=1, rating=SearchNode.RATING_ANY)
    again = SearchNode.Rated(days=1, rating=SearchNode.RATING_AGAIN)
    hard = SearchNode.Rated(days=1, rating=SearchNode.RATING_HARD)
    answered = col.build_search_string(SearchNode(rated=today))
    slipped = col.build_search_string(SearchNode(rated=again), SearchNode(rated=hard), joiner="OR")
    return DaySummary(cards=len(col.find_cards(answered)), slips=len(col.find_cards(slipped)))


# ── qué celebración toca ─────────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class Celebration:
    scope: Literal["deck", "all"]
    # Sesión sin fallos con repaso suficiente: sonido y brillo dorados.
    perfect: bool
    # Hay repaso suficiente para el confeti (el sonido de fin suena aunque no).
    confetti: bool


def decide(
    remaining: Remaining, session_answers: int, session_perfect: bool, day: DaySummary
) -> Celebration | None:
    """Qué celebrar al volver a la pantalla del mazo, o None si aún queda por repasar."""
    if remaining.total == 0:
        enough = day.cards >= DAY_MIN_CARDS
        return Celebration("all", perfect=enough and day.slips == 0, confetti=enough)
    if remaining.deck == 0:
        enough = session_answers >= DECK_MIN_ANSWERS
        return Celebration("deck", perfect=enough and session_perfect, confetti=enough)
    return None
