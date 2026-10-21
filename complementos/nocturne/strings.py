"""Todos los textos visibles del complemento, en español de España.

El título de la ventana y los botones («Aceptar», «Cancelar», «Restaurar los valores
predeterminados») los pone Anki o Qt, traducidos a su idioma.
"""

from __future__ import annotations

ADDON_NAME = "Nocturne"
GROUP_TITLE = "Apariencia"
PALETTE_LABEL = "Paleta"
APPLIED = "Paleta «{name}» aplicada."

# Nombre y descripción de cada paleta, en el orden de themes.THEMES. Una línea cada
# una y la misma estructura (petición del cliente, 2026-10-21): colores y acento,
# y después la forma. Valen para el modo día y para el modo noche.
THEME_NAMES = {
    "nocturne": "Nocturne",
    "papel": "Papel",
    "bosque": "Bosque",
}
THEME_DESCRIPTIONS = {
    "nocturne": "Grises azulados y acento azul. Letra del sistema y esquinas suaves.",
    "papel": "Papel y tinta con acento azul petróleo. Títulos con remates, como un libro.",
    "bosque": "Verdes grisáceos y acento verde azulado. Esquinas redondeadas y filas amplias.",
}
