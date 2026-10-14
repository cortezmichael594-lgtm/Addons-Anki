"""Que mazos entran en el mapa, y como se traduce eso a busquedas de Anki.

Dos ideas gobiernan este modulo:

  * Para contar, se necesitan identificadores de mazo ya expandidos con sus
    submazos (deck_and_child_ids), porque las consultas trabajan contra la
    columna did de las tarjetas.

  * Para abrir el navegador de tarjetas, se usa el buscador propio de Anki.
    Un termino deck:"Nombre" ya incluye los submazos y ya tiene en cuenta las
    tarjetas que estan temporalmente en un mazo filtrado, asi que la busqueda
    resultante es exactamente la que escribiria la persona a mano, y puede
    modificarla desde la barra de busqueda.

Los identificadores que no existen (un mazo borrado, o ajustes heredados de
otro perfil) se descartan al construir el ambito, de modo que el mapa nunca
se queda en blanco por una configuracion vieja.
"""

from __future__ import annotations

from dataclasses import dataclass

from anki.collection import Collection, SearchNode
from anki.decks import DeckId

from .errors import log_exception


@dataclass(frozen=True)
class DeckEntry:
    """Un mazo tal y como se muestra en la lista de opciones."""

    deck_id: int
    name: str
    depth: int
    leaf_name: str


@dataclass(frozen=True)
class DeckScope:
    """Que mazos cuentan y cuales no, en las dos formas que hacen falta."""

    include_ids: tuple[int, ...] | None
    exclude_ids: tuple[int, ...]
    include_names: tuple[str, ...]
    exclude_names: tuple[str, ...]
    # En la pantalla de un mazo: el mazo entero (con sus submazos) esta entre
    # los excluidos, asi que su mapa no puede mostrar nada.
    current_excluded: bool = False


WHOLE_COLLECTION = DeckScope(
    include_ids=None, exclude_ids=(), include_names=(), exclude_names=()
)


def all_deck_entries(
    col: Collection,
    *,
    skip_empty_default: bool = False,
    include_filtered: bool = True,
) -> list[DeckEntry]:
    """Todos los mazos, ordenados como en la pantalla principal de Anki.

    all_names_and_ids ya devuelve la lista ordenada jerarquicamente y con el
    nombre completo, usando "::" como separador entre mazo y submazo.

    La lista que se ensena para elegir mazos omite el mazo "Predeterminado"
    cuando esta vacio y los mazos filtrados, igual que hace Anki: las tarjetas
    de un mazo filtrado siguen perteneciendo a su mazo de origen, asi que
    excluir el filtrado no significaria nada.
    """
    entries: list[DeckEntry] = []
    try:
        for entry in col.decks.all_names_and_ids(
            skip_empty_default=skip_empty_default, include_filtered=include_filtered
        ):
            name = getattr(entry, "name", None)
            deck_id = getattr(entry, "id", None)
            if not isinstance(name, str) or not isinstance(deck_id, int):
                continue
            parts = name.split("::")
            entries.append(
                DeckEntry(
                    deck_id=deck_id,
                    name=name,
                    depth=len(parts) - 1,
                    leaf_name=parts[-1],
                )
            )
    except Exception as exc:
        log_exception("decks.all_deck_entries", exc)
    return entries


def _existing_names(
    entries: list[DeckEntry], deck_ids: tuple[int, ...]
) -> dict[int, str]:
    """Nombre de cada identificador que siga existiendo en esta coleccion.

    Los que ya no existen (un mazo borrado, o ajustes que vienen de otro
    perfil) simplemente no aparecen en el resultado.
    """
    if not deck_ids:
        return {}
    wanted = set(deck_ids)
    return {entry.deck_id: entry.name for entry in entries if entry.deck_id in wanted}


def _expand(col: Collection, deck_ids: tuple[int, ...]) -> tuple[int, ...]:
    """Anade los submazos de cada mazo indicado."""
    expanded: set[int] = set()
    for deck_id in deck_ids:
        try:
            expanded.update(
                int(child) for child in col.decks.deck_and_child_ids(DeckId(deck_id))
            )
        except Exception:
            # El mazo ya no existe: se ignora en lugar de romper el dibujado.
            continue
    return tuple(sorted(expanded))


def _drop_redundant(names: dict[int, str]) -> dict[int, str]:
    """Quita los mazos cuyo padre ya esta en la lista.

    Si estan marcados "Idiomas" y "Idiomas::Aleman", el segundo sobra: el
    termino deck:Idiomas ya lo cubre. Asi la busqueda queda corta y legible.
    """
    selected = set(names.values())
    return {
        deck_id: name
        for deck_id, name in names.items()
        if not any(name.startswith(other + "::") for other in selected if other != name)
    }


def build_scope(
    col: Collection, excluded_decks: tuple[int, ...], current_deck_only: bool
) -> DeckScope:
    """Calcula el ambito del mapa para la pantalla que se esta dibujando.

    current_deck_only distingue las dos pantallas donde aparece el mapa:
    la lista de mazos (toda la coleccion) y la pantalla de un mazo concreto
    (ese mazo y sus submazos).
    """
    # La lista de mazos se pide una sola vez y se reutiliza.
    entries = all_deck_entries(col)
    include_ids: tuple[int, ...] | None = None
    include_names: tuple[str, ...] = ()

    if current_deck_only:
        try:
            current_id = int(col.decks.get_current_id())
        except Exception as exc:
            log_exception("decks.build_scope/current", exc)
            current_id = 0
        if current_id:
            include_ids = _expand(col, (current_id,))
            current_name = _existing_names(entries, (current_id,)).get(current_id)
            if current_name:
                include_names = (current_name,)
        if not include_ids:
            include_ids = (current_id,) if current_id else ()

    exclude_names_map = _drop_redundant(_existing_names(entries, excluded_decks))
    exclude_ids = _expand(col, tuple(exclude_names_map))

    current_excluded = False
    if include_ids is not None and exclude_ids:
        excluded_set = set(exclude_ids)
        had_decks = bool(include_ids)
        include_ids = tuple(did for did in include_ids if did not in excluded_set)
        current_excluded = had_decks and not include_ids

    return DeckScope(
        include_ids=include_ids,
        exclude_ids=exclude_ids,
        include_names=include_names,
        exclude_names=tuple(exclude_names_map.values()),
        current_excluded=current_excluded,
    )


def scope_search_nodes(scope: DeckScope) -> list[SearchNode]:
    """Terminos de busqueda que reproducen el ambito en el navegador."""
    nodes: list[SearchNode] = []
    for name in scope.include_names:
        nodes.append(SearchNode(deck=name))
    for name in scope.exclude_names:
        nodes.append(SearchNode(negated=SearchNode(deck=name)))
    return nodes


def day_search(col: Collection, scope: DeckScope, days_offset: int, future: bool) -> str:
    """Busqueda de un dia concreto del mapa.

    days_offset es la distancia en dias respecto a hoy segun el calendario de
    Anki (que empieza el dia a la hora de reinicio configurada, no a
    medianoche), asi que coincide siempre con lo que muestra el mapa.

      * pasado:  prop:rated=-N  -> tarjetas respondidas ese dia.
      * futuro:  prop:due=N     -> tarjetas que vencen ese dia.
                 El dia de hoy incluye ademas lo atrasado (prop:due<=0),
                 que es lo mismo que cuenta la celda de hoy.
    """
    nodes: list[SearchNode | str] = list(scope_search_nodes(scope))
    if future:
        if days_offset <= 0:
            nodes.append(SearchNode(due_in_days=0))
        else:
            nodes.append(SearchNode(due_on_day=days_offset))
    else:
        # days_offset 0 -> "prop:rated=0" (hoy); 3 -> "prop:rated=-3".
        nodes.append(f"prop:rated={-max(days_offset, 0)}")
    return col.build_search_string(*nodes)
