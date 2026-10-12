"""Estado en memoria del complemento (no se guarda en ningun sitio)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class ViewState:
    # Ano que se esta mirando, contado hacia atras desde el actual.
    year_offset: int = 0

    # Contador que identifica el ultimo dibujado pedido. Si al terminar un
    # calculo en segundo plano el numero ya no coincide, es que entretanto se
    # pidio otro y el resultado viejo se descarta: asi el mapa nunca muestra
    # datos de una peticion anterior.
    render_token: int = 0

    # Se incrementa al abrir y al cerrar un perfil. Un calculo lanzado con la
    # coleccion anterior queda invalidado, que es lo que evitaba errores al
    # cambiar de usuario con el mapa dibujandose.
    generation: int = 0

    # Callback registrado por controller.register(). El dialogo de opciones lo
    # llama tras guardar para que el mapa se actualice en su sitio, sin
    # recargar la pantalla de Anki (que es lo que producia parpadeo). Vive
    # aqui, y no en un import directo, para que el dialogo no dependa del
    # modulo que lo abre.
    apply_config_change: Callable[[], None] | None = field(default=None, repr=False)

    def new_render_token(self) -> tuple[int, int]:
        self.render_token += 1
        return self.render_token, self.generation

    def is_current(self, token: int, generation: int) -> bool:
        return token == self.render_token and generation == self.generation

    def start_new_generation(self) -> None:
        self.generation += 1
        self.year_offset = 0


state = ViewState()
