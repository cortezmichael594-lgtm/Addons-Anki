"""Estado en memoria del complemento (no se guarda en ningun sitio)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .data import HeatmapData

# Mapas ya dibujados que se recuerdan para volver a ensenarlos al instante.
MAX_REMEMBERED_PAGES = 8


@dataclass(frozen=True)
class DataEntry:
    """Ultimos datos calculados y para que se calcularon."""

    generation: int
    current_deck_only: bool
    deck_id: int
    excluded_decks: tuple[int, ...]
    measure: str
    data: HeatmapData


@dataclass
class ViewState:
    # Ano que se esta mirando, contado hacia atras desde el actual.
    year_offset: int = 0

    # Contador que identifica el ultimo dibujado pedido. Si al terminar un
    # calculo en segundo plano el numero ya no coincide, es que entretanto se
    # pidio otro y el resultado viejo se descarta: asi el mapa nunca muestra
    # datos de una peticion anterior.
    render_token: int = 0

    # Calculo en marcha (su numero), o None. Mientras hay uno, cambiar de ano
    # no lanza otro: el que esta en marcha dibuja el ano que toque al acabar.
    pending_token: int | None = None

    # Se incrementa al abrir y al cerrar un perfil. Un calculo lanzado con la
    # coleccion anterior queda invalidado, que es lo que evitaba errores al
    # cambiar de usuario con el mapa dibujandose.
    generation: int = 0

    # Ultimos datos calculados. Cambiar de ano o de aspecto los reutiliza sin
    # volver a leer la coleccion; se olvidan cada vez que Anki redibuja la
    # pantalla, porque entonces puede haber datos nuevos.
    data: DataEntry | None = None

    # Ultimo mapa enviado a cada pantalla (lista de mazos o un mazo concreto),
    # ya preparado. Al volver a esa pantalla se ensena en el acto, en lugar de
    # un hueco con «…», mientras se calculan los datos al dia.
    pages: dict[tuple[bool, int], str] = field(default_factory=dict)

    # Callback registrado por controller.register(). El dialogo de opciones lo
    # llama tras guardar para que el mapa se actualice en su sitio, sin
    # recargar la pantalla de Anki (que es lo que producia parpadeo). Vive
    # aqui, y no en un import directo, para que el dialogo no dependa del
    # modulo que lo abre.
    apply_config_change: Callable[[], None] | None = field(default=None, repr=False)

    def new_render_token(self) -> tuple[int, int]:
        self.render_token += 1
        self.pending_token = self.render_token
        return self.render_token, self.generation

    def is_current(self, token: int, generation: int) -> bool:
        return token == self.render_token and generation == self.generation

    def finish(self, token: int) -> None:
        if self.pending_token == token:
            self.pending_token = None

    def remember_page(self, key: tuple[bool, int], payload: str) -> None:
        self.pages.pop(key, None)
        self.pages[key] = payload
        while len(self.pages) > MAX_REMEMBERED_PAGES:
            self.pages.pop(next(iter(self.pages)))

    def forget(self) -> None:
        """Olvida datos y mapas recordados (cambio de perfil o de opciones)."""
        self.data = None
        self.pages.clear()

    def start_new_generation(self) -> None:
        self.generation += 1
        self.year_offset = 0
        self.pending_token = None
        self.forget()


state = ViewState()
