"""Las cinco paletas del complemento (Nocturne, Papel, Bosque, Lavanda y Atardecer) y la
que está elegida.

Cada paleta es un estilo completo para el modo día y el modo noche: sus colores
(los mismos tokens que ``palette.PALETTE``, que es la de Nocturne) y su
«aspecto» (``Look``): letra de los títulos, esquinas, botones, separación de las
filas de la lista de mazos, contorno del foco y degradado del fondo.

En qué se apoya cada decisión (resúmenes en docs/referencias):
  - Una función fija para cada color, un solo color de acción y neutros del mismo
    matiz que el acento (Webflow, P2-P4; Practical UI, P10 y M2).
  - El radio de las esquinas y la letra dan la «personalidad» (Refactoring UI, P3):
    suaves en Nocturne y Papel, redondeadas en Bosque.
  - Títulos con remates solo en Papel; el resto del texto, en la letra del sistema
    (Practical UI, P14; Refactoring UI, M4; Weinschenk, P12).
  - De noche, colores con significado menos saturados (Orbix, M3 y C3) y fondos que
    se aclaran cuanto más arriba están (Practical UI, M3).
  - En Bosque (día y noche) y en Papel de noche, esos colores giran un poco su tono
    hacia el carácter de la paleta: azul petróleo, rojo ladrillo y verde musgo, sin
    dejar de ser azul, rojo y verde (Refactoring UI, M6). Nocturne y Papel de día
    conservan los suyos.
  - Papel de noche («Tinta»): fondo azul petróleo muy oscuro, de la familia del color
    de acción, y texto crema (Webflow, P4), elegido por el cliente el 2026-10-21.
Todas pasan las mismas pruebas de legibilidad (pruebas/nocturne).
"""

from __future__ import annotations

from typing import TypedDict

from .palette import PALETTE, Token


class Look(TypedDict):
    heading_family: str | None  # None: la letra de la interfaz
    heading_weight: int
    heading_tracking: str  # separación entre letras de los títulos
    reading_line_height: str  # interlineado de la descripción de un mazo
    radius: int  # px, esquinas pequeñas de ventanas y páginas; como mucho 6 (APR-059)
    radius_medium: int  # px, recuadros de las páginas
    radius_large: int  # px, botones redondeados de las páginas
    button_radius: int  # px, botones y campos de las ventanas; como mucho 9 (si no, Qt los dibuja
    # cuadrados). Regla de la versión 3.5.0: los recuadros (radius_medium) llevan el doble.
    # Versión 3.7.0: dos familias, suaves (6 y 12) y redondeadas (8 y 16), separadas un 33 %.
    row_padding: int  # px arriba y abajo de cada fila de la lista de mazos
    focus_width: int  # px del contorno de foco en las páginas
    gradient: tuple[str, str] | None  # degradado del fondo (día, noche), o ninguno


class Theme(TypedDict):
    colors: dict[str, Token]
    look: Look


def _colors(values: dict[str, tuple[str, str]]) -> dict[str, Token]:
    """Tabla de colores de una paleta, con las variables CSS de la de Nocturne."""
    return {
        name: {"css": PALETTE[name]["css"], "light": light, "dark": dark}
        for name, (light, dark) in values.items()
    }


NOCTURNE_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.01em",
    "reading_line_height": "1.5",
    "radius": 6,
    "radius_medium": 12,
    "radius_large": 16,
    "button_radius": 6,
    "row_padding": 4,
    "focus_width": 2,
    "gradient": ("rgba(59, 111, 224, 0.04)", "rgba(99, 144, 255, 0.07)"),  # colores-ok: degradado del acabado
}

PAPEL_LOOK: Look = {
    "heading_family": "Georgia, Cambria, 'Noto Serif', serif",
    "heading_weight": 700,
    "heading_tracking": "0",
    "reading_line_height": "1.6",
    "radius": 6,
    "radius_medium": 12,
    "radius_large": 16,
    "button_radius": 6,
    "row_padding": 5,
    "focus_width": 2,
    "gradient": ("rgba(31, 106, 128, 0.035)", "rgba(95, 179, 204, 0.06)"),  # colores-ok: degradado del acabado
}

BOSQUE_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.01em",
    "reading_line_height": "1.6",
    "radius": 6,
    "radius_medium": 16,
    "radius_large": 20,
    "button_radius": 8,
    "row_padding": 6,
    "focus_width": 2,
    "gradient": ("rgba(15, 118, 110, 0.04)", "rgba(63, 179, 165, 0.07)"),  # colores-ok: degradado del acabado
}

PAPEL: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#2269C1", "#89C5E8"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#CD2424", "#D78174"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#15793A", "#41C853"),  # colores-ok: paleta del tema
        "BORDER": ("#DFD6C6", "#24323A"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#1F6A80", "#5FB6CE"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#C9BEAA", "#34454F"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#ECE5D8", "#19242A"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FEFCF8", "#1C2930"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FEFCF880", "#1C293080"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#F0EADF", "#28363F"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#C9BEAA", "#34454F"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#1F6A80", "#1F6E85"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#1F6A8059", "#1F6E8559"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#1A5A6D", "#1A5E72"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#1F6A80", "#1F6E85"),  # colores-ok: paleta del tema
        "CANVAS": ("#FAF7F1", "#10171A"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#F4F0E8", "#121A1E"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FEFCF8", "#18232A"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FEFCF8CC", "#18232ACC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#F1ECE2", "#0C1215"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FEFCF8", "#223139"),  # colores-ok: paleta del tema
        "FG": ("#2A2520", "#E3DAC9"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#B0A796", "#718893"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#6E6557", "#ABA496"),  # colores-ok: paleta del tema
        "FG_LINK": ("#1B6378", "#8FCDE0"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#544C40", "#C4BBAB"),  # colores-ok: paleta del tema
        "FLAG_1": ("#C02121", "#B34534"),  # colores-ok: paleta del tema
        "FLAG_2": ("#D47425", "#C08138"),  # colores-ok: paleta del tema
        "FLAG_3": ("#1EA24E", "#30A43F"),  # colores-ok: paleta del tema
        "FLAG_4": ("#5187E0", "#4196C8"),  # colores-ok: paleta del tema
        "FLAG_5": ("#D05CE2", "#D263D2"),  # colores-ok: paleta del tema
        "FLAG_6": ("#209D8E", "#2E9F90"),  # colores-ok: paleta del tema
        "FLAG_7": ("#A868E4", "#A47BD9"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#1F6A80", "#1F6E85"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#DED5C5", "#1F2C33"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#B2A68F", "#34454F"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#C9BEAA", "#2B3B44"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#1F6A8033", "#5FB6CE40"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#2A2520", "#E3DAC9"),  # colores-ok: paleta del tema
        "SHADOW": ("#2A252026", "#04070866"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#1F6A8040", "#5FB6CE4D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#2A25201A", "#0407084D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#2A252012", "#04070833"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#BB8221", "#855E27"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#CD2424", "#D78174"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#6F71E6", "#5D6DD0"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#2565CF", "#89C5E8"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#15793A", "#32AE43"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#A68B1D", "#AA8C31"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#8E8574", "#71858F"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#EBEDE9", "#13272D"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#154B5B", "#164F60"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#0E3440", "#9FD6E4"),  # colores-ok: paleta del tema
        "NOCTURNE_TITLEBAR": ("#FFFCF7", "#070F12"),  # colores-ok: paleta del tema
    }
)

BOSQUE: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#246F9B", "#89C5E8"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#BA3F2C", "#D78174"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#1C7929", "#41C853"),  # colores-ok: paleta del tema
        "BORDER": ("#CED9D1", "#2A362D"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#0F766E", "#3FB3A5"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#B1C0B5", "#3B4A3F"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#DEE6E0", "#1E2821"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#F9FCFA", "#1F2922"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#F9FCFA80", "#1F292280"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#E6EDE7", "#2D3931"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#B1C0B5", "#3B4A3F"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#0F766E", "#0E7068"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#0F766E59", "#0E706859"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#0D635C", "#0C5F58"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#0F766E", "#0E7068"),  # colores-ok: paleta del tema
        "CANVAS": ("#F3F7F4", "#111814"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#EEF3EF", "#141C17"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#F9FCFA", "#1B241E"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#F9FCFACC", "#1B241ECC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#E9EFEA", "#0D130F"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#F9FCFA", "#26312A"),  # colores-ok: paleta del tema
        "FG": ("#17251C", "#D5E0D8"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#A2AFA6", "#778A7C"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#5E6E63", "#98A99E"),  # colores-ok: paleta del tema
        "FG_LINK": ("#0D6B64", "#7FD0C3"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#45554A", "#B0BEB4"),  # colores-ok: paleta del tema
        "FLAG_1": ("#B23C2A", "#B74635"),  # colores-ok: paleta del tema
        "FLAG_2": ("#C17C2D", "#C48339"),  # colores-ok: paleta del tema
        "FLAG_3": ("#26A136", "#31A741"),  # colores-ok: paleta del tema
        "FLAG_4": ("#3094CE", "#4699C9"),  # colores-ok: paleta del tema
        "FLAG_5": ("#D756D7", "#D366D3"),  # colores-ok: paleta del tema
        "FLAG_6": ("#259C8C", "#2FA192"),  # colores-ok: paleta del tema
        "FLAG_7": ("#9F6FDD", "#A67EDA"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#0F766E", "#0E7068"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#CCD7CF", "#28332B"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#98A99D", "#3B4A3F"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#B1C0B5", "#35423A"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#0F766E33", "#3FB3A540"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#17251C", "#D5E0D8"),  # colores-ok: paleta del tema
        "SHADOW": ("#17251C26", "#05080666"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#0F766E40", "#3FB3A54D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#17251C1A", "#0508064D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#17251C12", "#05080633"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#BC802C", "#855E27"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#BA3F2C", "#D78174"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#7583DF", "#5D6DD0"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#246F9B", "#89C5E8"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#1C7929", "#32AD42"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#A98828", "#AC8D32"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#7E8C82", "#6F8075"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#E3EEEB", "#112521"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#0A524C", "#0A4F4A"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#063A36", "#7FD6C9"),  # colores-ok: paleta del tema
        "NOCTURNE_TITLEBAR": ("#F8FEFA", "#08100C"),  # colores-ok: paleta del tema
    }
)

LAVANDA_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.01em",
    "reading_line_height": "1.55",
    "radius": 6,
    "radius_medium": 12,
    "radius_large": 16,
    "button_radius": 6,
    "row_padding": 5,
    "focus_width": 2,
    "gradient": ("rgba(123, 71, 212, 0.04)", "rgba(159, 111, 243, 0.07)"),  # colores-ok: degradado del acabado
}

ATARDECER_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.01em",
    "reading_line_height": "1.6",
    "radius": 6,
    "radius_medium": 16,
    "radius_large": 20,
    "button_radius": 8,
    "row_padding": 5,
    "focus_width": 2,
    "gradient": ("rgba(132, 87, 39, 0.045)", "rgba(236, 179, 118, 0.06)"),  # colores-ok: degradado del acabado
}

# >>> Lavanda y Atardecer (versión 3.6.0)
# Elegidas por el cliente el 2026-10-28 entre las propuestas sacadas de las fuentes: Lavanda
# (grises lila y violeta; el morado de HueHive, P1, y el «Púrpura real» de GritMap) y
# Atardecer (melocotón y marrón cálido con botones cobre; «Resplandor del atardecer» de
# Webflow, M6). Se obtienen girando el matiz de los neutros y del color de acción de
# Nocturne, que ya cumple todas las pruebas, y afinando lo que las pruebas pedían: el
# cobre más oscuro, para llevar texto blanco y separarse por claridad del naranja de
# «Difícil» (a 31° del rojo de «Aprendiendo»), y las banderas roja y verde de Lavanda de
# noche, para que se distingan también con daltonismo. Los colores con significado son
# los de Nocturne. Ningún valor se toca a mano: si hay que cambiarlos, se rehacen todos.
LAVANDA: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#186CB9", "#7EBFF4"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#CA2D2D", "#F37777"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#257A35", "#57D06B"),  # colores-ok: paleta del tema
        "BORDER": ("#DFDAE7", "#352C44"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#7B47D4", "#9F6FF3"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#C7C0D3", "#483D5C"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#EBE8F0", "#271F35"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FCFBFE", "#2C243A"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FCFBFE80", "#2C243A80"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#F0EDF5", "#372E47"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#C7C0D3", "#483D5C"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#7B47D4", "#804CDA"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#7B47D459", "#804CDA59"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#6A3ABC", "#6D3FBD"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#7B47D4", "#804CDA"),  # colores-ok: paleta del tema
        "CANVAS": ("#F8F7FA", "#17121F"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#F4F2F7", "#1A1424"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FCFBFE", "#292136"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FCFBFECC", "#292136CC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#F0EEF4", "#130F1B"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FCFBFE", "#312940"),  # colores-ok: paleta del tema
        "FG": ("#231B30", "#DAD6E1"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#B0A9BC", "#8A7F9D"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#6D647D", "#A49AB4"),  # colores-ok: paleta del tema
        "FG_LINK": ("#703CCB", "#C9B2F2"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#584E6A", "#BFB7CC"),  # colores-ok: paleta del tema
        "FLAG_1": ("#BE1D1D", "#B43C3C"),  # colores-ok: paleta del tema
        "FLAG_2": ("#E8590C", "#C07F3A"),  # colores-ok: paleta del tema
        "FLAG_3": ("#2F9E44", "#4C9E5A"),  # colores-ok: paleta del tema
        "FLAG_4": ("#1971C2", "#5993C2"),  # colores-ok: paleta del tema
        "FLAG_5": ("#C62FAD", "#B378C1"),  # colores-ok: paleta del tema
        "FLAG_6": ("#099268", "#439C81"),  # colores-ok: paleta del tema
        "FLAG_7": ("#7048E8", "#9680D6"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#7B47D4", "#804CDA"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#8D8797", "#7C728C"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#5A32A0", "#5C35A0"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#472482", "#CAAFF9"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#EFEBF7", "#281C3C"),  # colores-ok: paleta del tema
        "NOCTURNE_TITLEBAR": ("#FBFAFE", "#0C0716"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#DAD5E2", "#30273F"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#B2AAC0", "#483D5C"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#C7C0D3", "#3F3550"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#7B47D438", "#9F6FF340"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#231B30", "#DAD6E1"),  # colores-ok: paleta del tema
        "SHADOW": ("#231B3026", "#09050F66"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#7B47D440", "#9F6FF34D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#231B301A", "#09050F4D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#231B3012", "#09050F33"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#9A7B3F", "#A98754"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#CA2D2D", "#F37777"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#7048E8", "#9680D6"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#186CB9", "#7EBFF4"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#257A35", "#57D06B"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#8C8696", "#8D849C"),  # colores-ok: paleta del tema
    }
)

ATARDECER: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#186CB9", "#7EBFF4"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#CA2D2D", "#F37777"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#257A35", "#57D06B"),  # colores-ok: paleta del tema
        "BORDER": ("#EFDED2", "#44362C"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#7C5225", "#ECB376"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#E0C5B3", "#5C493D"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#F5EAE3", "#35281F"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FFFCFA", "#3A2D24"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FEFCFB80", "#3A2D2480"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#F9F0E9", "#47382E"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#E0C5B3", "#5C493D"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#845727", "#8F5D27"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#84572759", "#8F5D2759"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#624424", "#654727"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#845727", "#8F5D27"),  # colores-ok: paleta del tema
        "CANVAS": ("#FCF8F5", "#1F1712"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#FAF3EF", "#241A14"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FFFCFA", "#362921"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FFFCFACC", "#362921CC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#F8F0EA", "#1B140F"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FFFCFA", "#403229"),  # colores-ok: paleta del tema
        "FG": ("#261C15", "#E1DAD6"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#BCB1A9", "#9A887C"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#76685E", "#B4A49A"),  # colores-ok: paleta del tema
        "FG_LINK": ("#6A4822", "#ECCEAE"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#6A594E", "#CCBFB7"),  # colores-ok: paleta del tema
        "FLAG_1": ("#BE1D1D", "#C12D2D"),  # colores-ok: paleta del tema
        "FLAG_2": ("#E8590C", "#C07F3A"),  # colores-ok: paleta del tema
        "FLAG_3": ("#2F9E44", "#4DA05B"),  # colores-ok: paleta del tema
        "FLAG_4": ("#1971C2", "#5993C2"),  # colores-ok: paleta del tema
        "FLAG_5": ("#C62FAD", "#B378C1"),  # colores-ok: paleta del tema
        "FLAG_6": ("#099268", "#439C81"),  # colores-ok: paleta del tema
        "FLAG_7": ("#7048E8", "#9680D6"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#845727", "#8F5D27"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#978D87", "#8C7C72"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#48321A", "#49331C"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#21160B", "#F4D5B4"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#F6F1EC", "#3A2C1E"),  # colores-ok: paleta del tema
        "NOCTURNE_TITLEBAR": ("#FFFBF9", "#160D07"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#E2DAD5", "#3F3127"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#C0B3AA", "#5C493D"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#D3C8C0", "#504035"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#CB905038", "#ECB37640"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#261C15", "#E1DAD6"),  # colores-ok: paleta del tema
        "SHADOW": ("#30231B26", "#0F090566"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#7C522540", "#ECB3764D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#30231B1A", "#0F09054D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#30231B12", "#0F090533"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#9A7B3F", "#A98754"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#CA2D2D", "#F37777"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#7048E8", "#9680D6"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#186CB9", "#7EBFF4"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#257A35", "#57D06B"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#968C86", "#9C8E84"),  # colores-ok: paleta del tema
    }
)

# <<< Lavanda y Atardecer

# Orden en que aparecen en la ventana de configuración.
THEMES: dict[str, Theme] = {
    "nocturne": {"colors": PALETTE, "look": NOCTURNE_LOOK},
    "papel": {"colors": PAPEL, "look": PAPEL_LOOK},
    "bosque": {"colors": BOSQUE, "look": BOSQUE_LOOK},
    "lavanda": {"colors": LAVANDA, "look": LAVANDA_LOOK},
    "atardecer": {"colors": ATARDECER, "look": ATARDECER_LOOK},
}
DEFAULT_THEME = "nocturne"

_current = DEFAULT_THEME


def valid_id(theme_id: object) -> str:
    """El identificador si existe; si no (configuración antigua o escrita a mano), Nocturne."""
    return theme_id if isinstance(theme_id, str) and theme_id in THEMES else DEFAULT_THEME


def select(theme_id: object) -> str:
    """Elige la paleta activa y devuelve su identificador ya comprobado."""
    global _current
    _current = valid_id(theme_id)
    return _current


def current_id() -> str:
    return _current


def colors() -> dict[str, Token]:
    return THEMES[_current]["colors"]


def look() -> Look:
    return THEMES[_current]["look"]
