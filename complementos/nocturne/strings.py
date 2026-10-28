"""Todos los textos visibles del complemento, en español de España.

El título de la ventana y los botones («Aceptar», «Cancelar», «Restaurar los valores
predeterminados») los pone Anki o Qt, traducidos a su idioma.
"""

from __future__ import annotations

ADDON_NAME = "Atelier"
PALETTE_LABEL = "&Paleta"  # Alt+P lleva a la lista
DEFAULT_SUFFIX = " (predeterminada)"
DAY_AND_NIGHT = (
    "Cada paleta tiene versión de día y de noche, y cambia con el modo que elija "
    "en las preferencias de Anki."
)
HIGH_CONTRAST = (
    "Su sistema pide más contraste. Mientras siga así, Atelier deja los colores del "
    "sistema; la paleta que elija se aplicará cuando vuelva al contraste normal y "
    "reinicie Anki."
)
FAILURES = "Alguna parte de Anki no se pudo pintar y conserva su aspecto normal."

# Panel a medida (versión 3.7.0, informe del 2026-10-28).
PANEL_TITLE = "Paleta"
PANEL_INTRO = "Elija una paleta: se ve ya en Anki y se guarda al aceptar."
DAY = "Día"
NIGHT = "Noche"
DEFAULT_WORD = "predeterminada"
MODE_NOTE_DAY = (
    "Cada paleta tiene versión de día y de noche. Anki está ahora en modo día; el modo "
    "se cambia en Preferencias de Anki."
)
MODE_NOTE_NIGHT = (
    "Cada paleta tiene versión de día y de noche. Anki está ahora en modo noche; el modo "
    "se cambia en Preferencias de Anki."
)
HIGH_CONTRAST_BANNER = (
    "Su sistema pide más contraste: Atelier deja sus colores. La paleta que elija se "
    "aplicará cuando vuelva al contraste normal y reinicie Anki."
)
ACCEPT = "Aceptar"
CANCEL = "Cancelar"
OPEN_LOG = "Abrir el registro"

# Aviso que sale una sola vez, la primera vez que Anki arranca con el complemento.
# A quien ya tenía el complemento con el nombre antiguo (3.5.0 o anterior), una vez.
RENAMED = "Nocturne ahora se llama Atelier. Su paleta sigue igual."
WELCOME = (
    "Atelier está activo, con la paleta Nocturne. Para elegir otra: Herramientas > "
    "Complementos > Atelier > Configuración."
)

# Nombre y descripción de cada paleta, en el orden de themes.THEMES. Una línea cada
# una y la misma estructura (petición del cliente, 2026-10-21): colores y botones,
# y después la forma. Valen para el modo día y para el modo noche. Desde la 3.5.0,
# «botones» en lugar de «acento», que es palabra de diseñador.
THEME_NAMES = {
    "nocturne": "Nocturne",
    "papel": "Papel",
    "bosque": "Bosque",
    "lavanda": "Lavanda",
    "atardecer": "Atardecer",
}
THEME_DESCRIPTIONS = {
    "nocturne": "Grises azulados y botones azules. Letra del sistema y esquinas suaves.",
    "papel": "Papel y tinta, con botones azul petróleo. Títulos con remates, como un libro.",
    "bosque": "Verdes grisáceos y botones verde azulado. Esquinas redondeadas y filas amplias.",
    "lavanda": "Grises lila y botones violeta. Letra y esquinas como Nocturne.",
    "atardecer": "Melocotón y marrón cálido, con botones cobre. Esquinas redondeadas.",
}
