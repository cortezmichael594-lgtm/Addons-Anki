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
"""

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
PALETTE: dict[str, Token] = {
    "ACCENT_CARD":                   {"css": ("--accent-card",),                                   "light": "#1971C2",   "dark": "#74C0FC"},
    "ACCENT_DANGER":                 {"css": ("--accent-danger",),                                 "light": "#E03131",   "dark": "#FF6B6B"},
    "ACCENT_NOTE":                   {"css": ("--accent-note",),                                   "light": "#2F9E44",   "dark": "#57D06B"},
    "BORDER":                        {"css": ("--border",),                                        "light": "#DCE0E6",   "dark": "#2C3545"},
    "BORDER_FOCUS":                  {"css": ("--border-focus",),                                  "light": "#3B6FE0",   "dark": "#6390FF"},
    "BORDER_STRONG":                 {"css": ("--border-strong",),                                 "light": "#C2C9D2",   "dark": "#3D485C"},
    "BORDER_SUBTLE":                 {"css": ("--border-subtle",),                                 "light": "#E9ECF0",   "dark": "#202836"},
    "BUTTON_BG":                     {"css": ("--button-bg",),                                     "light": "#FFFFFF",   "dark": "#212836"},
    "BUTTON_DISABLED":               {"css": ("--button-disabled",),                               "light": "#FFFFFF80", "dark": "#21283680"},
    "BUTTON_HOVER":                  {"css": ("--button-gradient-start", "--button-gradient-end"), "light": "#F0F2F6",   "dark": "#2A3342"},
    "BUTTON_HOVER_BORDER":           {"css": ("--button-hover-border",),                           "light": "#C2C9D2",   "dark": "#3D485C"},
    "BUTTON_PRIMARY_BG":             {"css": ("--button-primary-bg",),                             "light": "#3B6FE0",   "dark": "#4066E6"},
    "BUTTON_PRIMARY_DISABLED":       {"css": ("--button-primary-disabled",),                       "light": "#3B6FE059", "dark": "#4066E659"},
    "BUTTON_PRIMARY_GRADIENT_END":   {"css": ("--button-primary-gradient-end",),                   "light": "#2F5BC7",   "dark": "#3452C8"},
    "BUTTON_PRIMARY_GRADIENT_START": {"css": ("--button-primary-gradient-start",),                 "light": "#4A7CEA",   "dark": "#5480FF"},
    "CANVAS":                        {"css": ("--canvas", "--bs-body-bg"),                         "light": "#F7F8FA",   "dark": "#12161F"},
    "CANVAS_CODE":                   {"css": ("--canvas-code",),                                   "light": "#F1F3F7",   "dark": "#141924"},
    "CANVAS_ELEVATED":               {"css": ("--canvas-elevated",),                               "light": "#FFFFFF",   "dark": "#212836"},
    "CANVAS_GLASS":                  {"css": ("--canvas-glass",),                                  "light": "#FFFFFFCC", "dark": "#212836CC"},
    "CANVAS_INSET":                  {"css": ("--canvas-inset",),                                  "light": "#EEF0F4",   "dark": "#0F131B"},
    "CANVAS_OVERLAY":                {"css": ("--canvas-overlay",),                                "light": "#FFFFFF",   "dark": "#191E2A"},
    "FG":                            {"css": ("--fg", "--bs-body-color"),                          "light": "#1B2430",   "dark": "#E9EDF4"},
    "FG_DISABLED":                   {"css": ("--fg-disabled",),                                   "light": "#A9B1BD",   "dark": "#5B6676"},
    "FG_FAINT":                      {"css": ("--fg-faint",),                                      "light": "#626D7B",   "dark": "#8894A6"},
    "FG_LINK":                       {"css": ("--fg-link",),                                       "light": "#2F63D8",   "dark": "#8DB2FF"},
    "FG_SUBTLE":                     {"css": ("--fg-subtle",),                                     "light": "#5C6675",   "dark": "#9FABBB"},
    "FLAG_1":                        {"css": ("--flag-1",),                                        "light": "#E03131",   "dark": "#FF6B6B"},
    "FLAG_2":                        {"css": ("--flag-2",),                                        "light": "#E8590C",   "dark": "#FFA94D"},
    "FLAG_3":                        {"css": ("--flag-3",),                                        "light": "#2F9E44",   "dark": "#69DB7C"},
    "FLAG_4":                        {"css": ("--flag-4",),                                        "light": "#1971C2",   "dark": "#74C0FC"},
    "FLAG_5":                        {"css": ("--flag-5",),                                        "light": "#C2255C",   "dark": "#E599F7"},
    "FLAG_6":                        {"css": ("--flag-6",),                                        "light": "#099268",   "dark": "#63E6BE"},
    "FLAG_7":                        {"css": ("--flag-7",),                                        "light": "#7048E8",   "dark": "#B197FC"},
    "HIGHLIGHT_BG":                  {"css": ("--highlight-bg",),                                  "light": "#3B6FE0",   "dark": "#4066E6"},
    "HIGHLIGHT_FG":                  {"css": ("--highlight-fg",),                                  "light": "#FFFFFF",   "dark": "#FFFFFF"},
    "SCROLLBAR_BG":                  {"css": ("--scrollbar-bg",),                                  "light": "#D6DBE2",   "dark": "#273040"},
    "SCROLLBAR_BG_ACTIVE":           {"css": ("--scrollbar-bg-active",),                           "light": "#AAB3C0",   "dark": "#3D485C"},
    "SCROLLBAR_BG_HOVER":            {"css": ("--scrollbar-bg-hover",),                            "light": "#C2C9D2",   "dark": "#313C4E"},
    "SELECTED_BG":                   {"css": ("--selected-bg",),                                   "light": "#3B6FE022", "dark": "#6390FF2E"},
    "SELECTED_FG":                   {"css": ("--selected-fg",),                                   "light": "#1B2430",   "dark": "#E9EDF4"},
    "SHADOW":                        {"css": ("--shadow",),                                        "light": "#1B243026", "dark": "#05080F66"},
    "SHADOW_FOCUS":                  {"css": ("--shadow-focus",),                                  "light": "#3B6FE040", "dark": "#6390FF4D"},
    "SHADOW_INSET":                  {"css": ("--shadow-inset",),                                  "light": "#1B24301A", "dark": "#05080F4D"},
    "SHADOW_SUBTLE":                 {"css": ("--shadow-subtle",),                                 "light": "#1B243012", "dark": "#05080F33"},
    "STATE_BURIED":                  {"css": ("--state-buried",),                                  "light": "#9A7B3F",   "dark": "#B08D57"},
    "STATE_LEARN":                   {"css": ("--state-learn",),                                   "light": "#E8590C",   "dark": "#FFA94D"},
    "STATE_MARKED":                  {"css": ("--state-marked",),                                  "light": "#7048E8",   "dark": "#B197FC"},
    "STATE_NEW":                     {"css": ("--state-new",),                                     "light": "#1971C2",   "dark": "#74C0FC"},
    "STATE_REVIEW":                  {"css": ("--state-review",),                                  "light": "#2F9E44",   "dark": "#57D06B"},
    "STATE_SUSPENDED":               {"css": ("--state-suspended",),                              "light": "#868E96",   "dark": "#8A94A3"},
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
