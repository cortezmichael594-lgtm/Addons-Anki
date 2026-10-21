"""Paleta Nocturne: la única fuente de verdad para todos los colores.

Cada entrada describe un *token* de color con:
  - ``css``   : nombres de variables CSS que ese token alimenta en las páginas
                web de Anki (repaso, editor, gráficas...).
  - ``light`` : valor para el modo día.
  - ``dark``  : valor para el modo noche.

Dos canales consumen esta paleta:
  * El canal nativo (``theming.py``) reescribe ``aqt.colors.<TOKEN>`` con estos
    valores, de modo que los widgets Qt (menús, botones, tablas...) y la propia
    hoja de estilo de Anki adoptan la paleta.
  * El canal web (``webview_style.py``) emite reglas ``--variable: valor;`` a
    partir de ``css``, porque el CSS de las páginas web se compila aparte y no
    lee ``aqt.colors`` en tiempo de ejecución.

Los valores con 8 dígitos hexadecimales incluyen transparencia; ``to_css_rgba``
los convierte al formato ``rgba(...)`` que Anki entiende en el lado Qt.

Los tokens que empiezan por ``NOCTURNE_`` no existen en Anki ni tienen variable
CSS: son propios y solo los usa ``theming.py`` en su retoque de la hoja de estilo.
"""

# Historial de correcciones de este archivo:
# FIX-002 (2026-10-21): de día, cifras de la lista de mazos y rojo de aviso con poco contraste.
# FIX-003 (2026-10-21): casillas sin marcar casi invisibles.
# FIX-004 (2026-10-21): de noche, texto ilegible en las filas de Explorar con bandera.
# FIX-005 (2026-10-21): texto blanco poco legible en el botón azul con el ratón encima.

from __future__ import annotations

from typing import Literal, TypedDict

Mode = Literal["light", "dark"]


class Token(TypedDict):
    css: tuple[str, ...]
    light: str
    dark: str


# Ajustes deliberados sobre la paleta original (contraste y armonía):
#   FG_FAINT dark  #808B9C -> #8894A6  (texto tenue legible sobre superficies
#                                       elevadas en modo noche: AA real)
#   FG_DISABLED dk #566172 -> #5B6676  (deshabilitado algo más legible sin dejar
#                                       de verse claramente inactivo)
#   FG_LINK dark   #82ABFF -> #8DB2FF  (enlaces más cómodos en fondo oscuro)
#   HIGHLIGHT_BG   dark    -> #4066E6  (la selección resalta un punto más)
# El resto conserva la identidad original: azul sereno sobre grises azulados.
#
# Versión 3.0.0: los neutros son un sistema (Refactoring UI, M5; Practical UI, M2 y M3).
#   - Una sola familia de grises azulados (tono 220°), con más saturación en los
#     extremos para que no se vean apagados; sin blanco ni negro puros.
#   - Tres niveles de texto bien separados: FG (principal), FG_SUBTLE (secundario) y
#     FG_FAINT (lo menos importante), todos a 4,5:1 o más sobre cualquier superficie y
#     también medidos con APCA (75, 60 y 45 como mínimo), el método que tiene en
#     cuenta cómo percibe el ojo el texto claro sobre fondo oscuro.
#   - De noche, lo que está más arriba es más claro: hundido (CANVAS_INSET) < fondo
#     (CANVAS) < recuadros (CANVAS_ELEVATED) < botones (BUTTON_BG) < menús
#     (CANVAS_OVERLAY) < botón con el ratón encima (BUTTON_HOVER).
#   - Los acentos de tarjeta y nota (ACCENT_CARD, ACCENT_NOTE) usan de día los mismos
#     tonos que las cifras «Nuevas» y «Para repasar», legibles como texto.
#
# Versión 3.4.0: NOCTURNE_TITLEBAR, la barra de título de las ventanas en Windows 11 (petición
# del cliente, 2026-10-21): del matiz del fondo, más oscura que él de noche (#0B0E13 frente a
# #12161F) y más clara de día (#FCFCFD frente a #F7F8FA, el tono más claro sin llegar al blanco
# puro), para que se distinga de la ventana sin cambiar de familia.
#
# Versión 3.3.0: de noche, FG_DISABLED pasa de #5B6476 a #7C869A, del mismo tono. Lo
# usan los botones y textos desactivados y la cifra de tarjetas enterradas («+3») de la
# pantalla de estudio, y no llegaba al mínimo absoluto de APCA para texto (30, Practical
# UI, cap. 3): ahora llega a 30 o más sobre el fondo, los recuadros y los botones, y
# sigue por debajo de FG_FAINT, para que lo desactivado se vea desactivado.
#
# Versión 2.1.0: de noche, el texto principal (FG y SELECTED_FG) pasa de #E9EDF4 a
# #D6DAE1, del mismo tono, para que no deslumbre en sesiones largas: 13:1 sobre el
# fondo en vez de 15,4:1, y al menos 10,6:1 sobre cualquier superficie.
#
# --- FIX-002 (2026-10-21) ---
# Síntoma: de día, «Aprendiendo» (3,1:1), «Para repasar» (3,0:1), «Nuevas» (4,4:1) y el
#          rojo de aviso (4,0:1) se leían peor de lo recomendado sobre algunas superficies.
# Causa: esos colores se eligieron por su aspecto como iconos y no se midieron como texto.
# Regla: todo color que Anki use como texto llega a 4,5:1 sobre las cuatro superficies; para
#        corregirlo se oscurece sin cambiar el tono (lo comprueba pruebas/nocturne).
#
# --- FIX-003 (2026-10-21) ---
# Síntoma: el borde de una casilla sin marcar casi no se distinguía (1,3:1 de día, 1,5:1 de noche).
# Causa: Anki dibuja ese borde con BORDER, que aquí es muy suave para que campos y listas
#        se vean ligeros.
# Regla: las casillas tienen su propio borde, NOCTURNE_CONTROL_BORDER, a 3:1 o más; BORDER y
#        BORDER_SUBTLE se quedan suaves (aspecto original elegido por el cliente).
#
# --- FIX-004 (2026-10-21) ---
# Síntoma: de noche, en Explorar, el texto de las filas con bandera naranja, verde, azul, rosa,
#          turquesa o morada quedaba entre 2,9:1 y 4,3:1.
# Causa: Anki pinta esas filas con el color de la bandera oscurecido (darker(150)) y los
#        tonos pastel nocturnos seguían siendo demasiado claros detrás del texto.
# Regla: de noche, cada bandera y estado deja su fila a 4,5:1 con FG; se oscurecen sin cambiar
#        el tono y siguen a más de 3:1 como icono (lo comprueba pruebas/nocturne).
#
# --- FIX-005 (2026-10-21) ---
# Síntoma: con el ratón encima del botón azul, su texto blanco bajaba a 3,9:1 (día) y 3,6:1 (noche).
# Causa: el degradado de «pasar el ratón» empezaba en un azul más claro que el del botón.
# Regla: todo el azul de acción, en cualquier estado, da 4,5:1 con texto blanco (APR-061).
PALETTE: dict[str, Token] = {
    "ACCENT_CARD":                   {"css": ("--accent-card",),                                   "light": "#186CB9",   "dark": "#7EBFF4"},  # colores-ok: paleta del tema, origen de todos sus colores
    "ACCENT_DANGER":                 {"css": ("--accent-danger",),                                 "light": "#CA2D2D",   "dark": "#F37777"},  # colores-ok: paleta del tema, origen de todos sus colores
    "ACCENT_NOTE":                   {"css": ("--accent-note",),                                   "light": "#257A35",   "dark": "#57D06B"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BORDER":                        {"css": ("--border",),                                        "light": "#DADEE7",   "dark": "#2C3444"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BORDER_FOCUS":                  {"css": ("--border-focus",),                                  "light": "#3B6FE0",   "dark": "#6390FF"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BORDER_STRONG":                 {"css": ("--border-strong",),                                 "light": "#C0C6D3",   "dark": "#3D475C"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BORDER_SUBTLE":                 {"css": ("--border-subtle",),                                 "light": "#E8EAF0",   "dark": "#1F2635"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_BG":                     {"css": ("--button-bg",),                                     "light": "#FBFCFE",   "dark": "#242C3A"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_DISABLED":               {"css": ("--button-disabled",),                               "light": "#FBFCFE80", "dark": "#242C3A80"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_HOVER":                  {"css": ("--button-gradient-start", "--button-gradient-end"), "light": "#EDF0F5",   "dark": "#2E3747"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_HOVER_BORDER":           {"css": ("--button-hover-border",),                           "light": "#C0C6D3",   "dark": "#3D475C"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_PRIMARY_BG":             {"css": ("--button-primary-bg",),                             "light": "#3B6FE0",   "dark": "#4066E6"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_PRIMARY_DISABLED":       {"css": ("--button-primary-disabled",),                       "light": "#3B6FE059", "dark": "#4066E659"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_PRIMARY_GRADIENT_END":   {"css": ("--button-primary-gradient-end",),                   "light": "#2F5BC7",   "dark": "#3452C8"},  # colores-ok: paleta del tema, origen de todos sus colores
    "BUTTON_PRIMARY_GRADIENT_START": {"css": ("--button-primary-gradient-start",),                 "light": "#3B6FE0",   "dark": "#4066E6"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS":                        {"css": ("--canvas", "--bs-body-bg"),                         "light": "#F7F8FA",   "dark": "#12161F"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS_CODE":                   {"css": ("--canvas-code",),                                   "light": "#F2F4F7",   "dark": "#141924"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS_ELEVATED":               {"css": ("--canvas-elevated",),                               "light": "#FBFCFE",   "dark": "#212836"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS_GLASS":                  {"css": ("--canvas-glass",),                                  "light": "#FBFCFECC", "dark": "#212836CC"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS_INSET":                  {"css": ("--canvas-inset",),                                  "light": "#EEF0F4",   "dark": "#0F131B"},  # colores-ok: paleta del tema, origen de todos sus colores
    "CANVAS_OVERLAY":                {"css": ("--canvas-overlay",),                                "light": "#FBFCFE",   "dark": "#293040"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FG":                            {"css": ("--fg", "--bs-body-color"),                          "light": "#1B2430",   "dark": "#D6DAE1"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FG_DISABLED":                   {"css": ("--fg-disabled",),                                   "light": "#A9AFBC",   "dark": "#7C869A"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FG_FAINT":                      {"css": ("--fg-faint",),                                      "light": "#646C7D",   "dark": "#9AA3B4"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FG_LINK":                       {"css": ("--fg-link",),                                       "light": "#2F63D8",   "dark": "#A3C1F7"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FG_SUBTLE":                     {"css": ("--fg-subtle",),                                     "light": "#4E576A",   "dark": "#B7BECC"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_1":                        {"css": ("--flag-1",),                                        "light": "#D92121",   "dark": "#D13939"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_2":                        {"css": ("--flag-2",),                                        "light": "#E8590C",   "dark": "#C07F3A"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_3":                        {"css": ("--flag-3",),                                        "light": "#2F9E44",   "dark": "#4C9E5A"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_4":                        {"css": ("--flag-4",),                                        "light": "#1971C2",   "dark": "#5993C2"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_5":                        {"css": ("--flag-5",),                                        "light": "#C62FAD",   "dark": "#B378C1"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_6":                        {"css": ("--flag-6",),                                        "light": "#099268",   "dark": "#439C81"},  # colores-ok: paleta del tema, origen de todos sus colores
    "FLAG_7":                        {"css": ("--flag-7",),                                        "light": "#7048E8",   "dark": "#9680D6"},  # colores-ok: paleta del tema, origen de todos sus colores
    "HIGHLIGHT_BG":                  {"css": ("--highlight-bg",),                                  "light": "#3B6FE0",   "dark": "#4066E6"},  # colores-ok: paleta del tema, origen de todos sus colores
    "HIGHLIGHT_FG":                  {"css": ("--highlight-fg",),                                  "light": "#FFFFFF",   "dark": "#FFFFFF"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SCROLLBAR_BG":                  {"css": ("--scrollbar-bg",),                                  "light": "#D5D9E2",   "dark": "#272F3F"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SCROLLBAR_BG_ACTIVE":           {"css": ("--scrollbar-bg-active",),                           "light": "#AAB1C0",   "dark": "#3D475C"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SCROLLBAR_BG_HOVER":            {"css": ("--scrollbar-bg-hover",),                            "light": "#C0C6D3",   "dark": "#353E50"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SELECTED_BG":                   {"css": ("--selected-bg",),                                   "light": "#3B6FE038", "dark": "#6390FF40"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SELECTED_FG":                   {"css": ("--selected-fg",),                                   "light": "#1B2430",   "dark": "#D6DAE1"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SHADOW":                        {"css": ("--shadow",),                                        "light": "#1B243026", "dark": "#05080F66"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SHADOW_FOCUS":                  {"css": ("--shadow-focus",),                                  "light": "#3B6FE040", "dark": "#6390FF4D"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SHADOW_INSET":                  {"css": ("--shadow-inset",),                                  "light": "#1B24301A", "dark": "#05080F4D"},  # colores-ok: paleta del tema, origen de todos sus colores
    "SHADOW_SUBTLE":                 {"css": ("--shadow-subtle",),                                 "light": "#1B243012", "dark": "#05080F33"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_BURIED":                  {"css": ("--state-buried",),                                  "light": "#9A7B3F",   "dark": "#A98754"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_LEARN":                   {"css": ("--state-learn",),                                   "light": "#B8460A",   "dark": "#F1A95B"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_MARKED":                  {"css": ("--state-marked",),                                  "light": "#7048E8",   "dark": "#9680D6"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_NEW":                     {"css": ("--state-new",),                                     "light": "#186CB9",   "dark": "#7EBFF4"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_REVIEW":                  {"css": ("--state-review",),                                  "light": "#257A35",   "dark": "#57D06B"},  # colores-ok: paleta del tema, origen de todos sus colores
    "STATE_SUSPENDED":               {"css": ("--state-suspended",),                              "light": "#868E96",   "dark": "#848E9C"},  # colores-ok: paleta del tema, origen de todos sus colores
    "NOCTURNE_CONTROL_BORDER":       {"css": (),                                                   "light": "#878C97",   "dark": "#727B8C"},  # colores-ok: paleta del tema, origen de todos sus colores
    "NOCTURNE_ROW_HIGHLIGHT":        {"css": ("--nocturne-row-highlight",),                          "light": "#EAEEF8",   "dark": "#19233F"},  # colores-ok: paleta del tema, origen de todos sus colores
    "NOCTURNE_PRIMARY_PRESSED":      {"css": (),                                                     "light": "#284EAA",   "dark": "#2B45AA"},  # colores-ok: paleta del tema, origen de todos sus colores
    "NOCTURNE_PRIMARY_RING":         {"css": (),                                                     "light": "#1C3A8A",   "dark": "#A9C4FF"},  # colores-ok: paleta del tema, origen de todos sus colores
    "NOCTURNE_TITLEBAR":             {"css": (),                                                     "light": "#FCFCFD",   "dark": "#0B0E13"},  # colores-ok: paleta del tema, origen de todos sus colores
}

# Anki mantiene dos alias de gradiente que deben seguir al color de hover.
GRADIENT_ALIASES: tuple[str, ...] = ("BUTTON_GRADIENT_START", "BUTTON_GRADIENT_END")


def to_css_rgba(color: str) -> str:
    """Convierte ``#RRGGBBAA`` a ``rgba(r, g, b, a)``; deja el resto igual.

    El lado Qt de Anki solo interpreta la transparencia mediante ``rgba(...)``,
    no con hexadecimal de 8 dígitos.
    """
    if color.startswith("#") and len(color) == 9:
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        a = round(int(color[7:9], 16) / 255, 3)
        return f"rgba({r}, {g}, {b}, {a})"
    return color
