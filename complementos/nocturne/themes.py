"""Las cinco paletas del complemento y la que está elegida.

Cada paleta es un estilo completo para el modo día y el modo noche: sus colores
(los mismos tokens que ``palette.PALETTE``, que es la de Nocturne) y su
«aspecto» (``Look``): letra de los títulos, esquinas, botones, separación de las
filas de la lista de mazos, contorno del foco y degradado del fondo.

En qué se apoya cada decisión (resúmenes en docs/referencias):
  - Una función fija para cada color, un solo color de acción y neutros del mismo
    matiz que el acento (Webflow, P2-P4; Practical UI, P10 y M2).
  - El radio de las esquinas y la letra dan la «personalidad» (Refactoring UI, P3):
    rectas y sobrias en Grafito, suaves en Nocturne y Papel, redondeadas en Bosque.
  - Títulos con remates solo en Papel; el resto del texto, en la letra del sistema
    (Practical UI, P14; Refactoring UI, M4; Weinschenk, P12).
  - De noche, colores con significado menos saturados (Orbix, M3 y C3) y fondos que
    se aclaran cuanto más arriba están (Practical UI, M3).
  - Alto contraste: texto a 7:1 o más (nivel AAA de las WCAG) y bordes marcados
    (Practical UI, P4).
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
    button_radius: int  # px, botones de las ventanas; como mucho 9 (si no, Qt los dibuja cuadrados)
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
    "button_radius": 7,
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
    "radius_medium": 14,
    "radius_large": 18,
    "button_radius": 8,
    "row_padding": 5,
    "focus_width": 2,
    "gradient": ("rgba(31, 106, 128, 0.035)", "rgba(95, 179, 204, 0.06)"),  # colores-ok: degradado del acabado
}

GRAFITO_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.015em",
    "reading_line_height": "1.5",
    "radius": 2,
    "radius_medium": 4,
    "radius_large": 4,
    "button_radius": 3,
    "row_padding": 2,
    "focus_width": 2,
    "gradient": None,
}

BOSQUE_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 600,
    "heading_tracking": "-0.01em",
    "reading_line_height": "1.6",
    "radius": 6,
    "radius_medium": 16,
    "radius_large": 20,
    "button_radius": 9,
    "row_padding": 6,
    "focus_width": 2,
    "gradient": ("rgba(15, 118, 110, 0.04)", "rgba(63, 179, 165, 0.07)"),  # colores-ok: degradado del acabado
}

CONTRASTE_LOOK: Look = {
    "heading_family": None,
    "heading_weight": 700,
    "heading_tracking": "0",
    "reading_line_height": "1.6",
    "radius": 4,
    "radius_medium": 8,
    "radius_large": 8,
    "button_radius": 6,
    "row_padding": 5,
    "focus_width": 3,
    "gradient": None,
}

PAPEL: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#2269C1", "#A7C6E9"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#CD2424", "#E18888"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#15793A", "#54D483"),  # colores-ok: paleta del tema
        "BORDER": ("#DFD6C6", "#38322B"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#1F6A80", "#5FB3CC"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#C9BEAA", "#4A433A"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#ECE5D8", "#2A2520"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FEFCF8", "#2A2622"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FEFCF880", "#2A262280"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#F0EADF", "#3A352F"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#C9BEAA", "#4A433A"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#1F6A80", "#1F6B82"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#1F6A8059", "#1F6B8259"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#1A5A6D", "#1A5B6F"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#1F6A80", "#1F6B82"),  # colores-ok: paleta del tema
        "CANVAS": ("#FAF7F1", "#1A1714"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#F4F0E8", "#1C1916"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FEFCF8", "#25211D"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FEFCF8CC", "#25211DCC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#F1ECE2", "#13110F"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FEFCF8", "#312C27"),  # colores-ok: paleta del tema
        "FG": ("#2A2520", "#E6DFD3"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#B0A796", "#615A50"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#6E6557", "#ACA193"),  # colores-ok: paleta del tema
        "FG_LINK": ("#1B6378", "#86CADD"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#544C40", "#C3B9AA"),  # colores-ok: paleta del tema
        "FLAG_1": ("#DA2B2B", "#D14747"),  # colores-ok: paleta del tema
        "FLAG_2": ("#D47425", "#CC8235"),  # colores-ok: paleta del tema
        "FLAG_3": ("#1EA24E", "#2AA858"),  # colores-ok: paleta del tema
        "FLAG_4": ("#5187E0", "#6196D7"),  # colores-ok: paleta del tema
        "FLAG_5": ("#D05CE2", "#CB6FDB"),  # colores-ok: paleta del tema
        "FLAG_6": ("#209D8E", "#29A491"),  # colores-ok: paleta del tema
        "FLAG_7": ("#A868E4", "#AE7EDF"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#1F6A80", "#1F6B82"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#DED5C5", "#332E28"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#B2A68F", "#4E463D"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#C9BEAA", "#433C34"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#1F6A8033", "#5FB3CC40"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#2A2520", "#E6DFD3"),  # colores-ok: paleta del tema
        "SHADOW": ("#2A252026", "#0A080766"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#1F6A8040", "#5FB3CC4D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#2A25201A", "#0A08074D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#2A252012", "#0A080733"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#BB8221", "#9B5327"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#CD2424", "#E18888"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#6F71E6", "#A771DB"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#2565CF", "#A7C6E9"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#15793A", "#2EB961"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#A68B1D", "#A09528"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#8E8574", "#857B6D"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#EBEDE9", "#1B2424"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#154B5B", "#164C5D"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#0E3440", "#8FD0E2"),  # colores-ok: paleta del tema
    }
)

GRAFITO: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#2B6AB7", "#AAC6E6"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#C62F2F", "#DD8C8C"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#1C783E", "#59CF84"),  # colores-ok: paleta del tema
        "BORDER": ("#D4D4D4", "#313131"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#4F46E5", "#8F88F0"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#B8B8B8", "#474747"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#E2E2E2", "#262626"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FCFCFC", "#252525"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FCFCFC80", "#25252580"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#EBEBEB", "#333333"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#B8B8B8", "#474747"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#4F46E5", "#5148D9"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#4F46E559", "#5148D959"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#4338CA", "#453CC2"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#4F46E5", "#5148D9"),  # colores-ok: paleta del tema
        "CANVAS": ("#F5F5F5", "#161616"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#F0F0F0", "#191919"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FCFCFC", "#202020"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FCFCFCCC", "#202020CC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#ECECEC", "#101010"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FCFCFC", "#2B2B2B"),  # colores-ok: paleta del tema
        "FG": ("#1C1C1C", "#DCDCDC"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#A6A6A6", "#5E5E5E"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#686868", "#A3A3A3"),  # colores-ok: paleta del tema
        "FG_LINK": ("#4A41D6", "#B9B5F2"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#4D4D4D", "#B9B9B9"),  # colores-ok: paleta del tema
        "FLAG_1": ("#D03535", "#CA4848"),  # colores-ok: paleta del tema
        "FLAG_2": ("#CC7630", "#C58139"),  # colores-ok: paleta del tema
        "FLAG_3": ("#259F52", "#30A45A"),  # colores-ok: paleta del tema
        "FLAG_4": ("#5989D8", "#6092D1"),  # colores-ok: paleta del tema
        "FLAG_5": ("#CA60DA", "#C66ED5"),  # colores-ok: paleta del tema
        "FLAG_6": ("#249B8C", "#2FA18F"),  # colores-ok: paleta del tema
        "FLAG_7": ("#A76FDD", "#AA7BD9"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#4F46E5", "#5148D9"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#D1D1D1", "#2E2E2E"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#A0A0A0", "#474747"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#B8B8B8", "#3D3D3D"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#4F46E533", "#8F88F040"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#1C1C1C", "#DCDCDC"),  # colores-ok: paleta del tema
        "SHADOW": ("#1C1C1C26", "#08080866"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#4F46E540", "#8F88F04D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#1C1C1C1A", "#0808084D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#1C1C1C12", "#08080833"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#B5822B", "#96542B"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#C62F2F", "#DD8C8C"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#7578DF", "#A775D7"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#2E67C3", "#AAC6E6"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#1C783E", "#34B363"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#A28926", "#9C922D"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#868686", "#7C7C7C"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#EBEBF4", "#1E1D31"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#3730A3", "#3A32A6"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#2A2475", "#B4B0F5"),  # colores-ok: paleta del tema
    }
)

BOSQUE: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#2869BA", "#A8C6E8"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#C82A2A", "#E08989"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#1A793D", "#56D283"),  # colores-ok: paleta del tema
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
        "FG_DISABLED": ("#A2AFA6", "#56645A"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#5E6E63", "#98A99E"),  # colores-ok: paleta del tema
        "FG_LINK": ("#0D6B64", "#7FD0C3"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#45554A", "#B0BEB4"),  # colores-ok: paleta del tema
        "FLAG_1": ("#D33232", "#CE4545"),  # colores-ok: paleta del tema
        "FLAG_2": ("#CF752C", "#C88035"),  # colores-ok: paleta del tema
        "FLAG_3": ("#22A050", "#2CA558"),  # colores-ok: paleta del tema
        "FLAG_4": ("#5688DB", "#5F93D4"),  # colores-ok: paleta del tema
        "FLAG_5": ("#CC5FDD", "#C86DD8"),  # colores-ok: paleta del tema
        "FLAG_6": ("#219C8D", "#2BA28F"),  # colores-ok: paleta del tema
        "FLAG_7": ("#A76CE0", "#AC7BDC"),  # colores-ok: paleta del tema
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
        "STATE_BURIED": ("#B88227", "#995329"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#C82A2A", "#E08989"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#7375E1", "#A772DA"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#2A66C8", "#A8C6E8"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#1A793D", "#31B762"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#A58A23", "#9D932A"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#7E8C82", "#6F8075"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#E3EEEB", "#112521"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#0A524C", "#0A4F4A"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#063A36", "#7FD6C9"),  # colores-ok: paleta del tema
    }
)

CONTRASTE: dict[str, Token] = _colors(
    {
        "ACCENT_CARD": ("#0C4995", "#9FC6F1"),  # colores-ok: paleta del tema
        "ACCENT_DANGER": ("#980D0D", "#F09999"),  # colores-ok: paleta del tema
        "ACCENT_NOTE": ("#0F5629", "#4ADE80"),  # colores-ok: paleta del tema
        "BORDER": ("#B9BEC5", "#4A4F57"),  # colores-ok: paleta del tema
        "BORDER_FOCUS": ("#1A44C2", "#8EA9FF"),  # colores-ok: paleta del tema
        "BORDER_STRONG": ("#4B5059", "#A1A7B0"),  # colores-ok: paleta del tema
        "BORDER_SUBTLE": ("#7C828B", "#6E747D"),  # colores-ok: paleta del tema
        "BUTTON_BG": ("#FCFDFE", "#1C1F23"),  # colores-ok: paleta del tema
        "BUTTON_DISABLED": ("#FCFDFE80", "#1C1F2380"),  # colores-ok: paleta del tema
        "BUTTON_HOVER": ("#E4E7EB", "#2A2E34"),  # colores-ok: paleta del tema
        "BUTTON_HOVER_BORDER": ("#4B5059", "#A1A7B0"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_BG": ("#1A44C2", "#1F49CC"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_DISABLED": ("#1A44C259", "#1F49CC59"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_END": ("#1538A3", "#183DAF"),  # colores-ok: paleta del tema
        "BUTTON_PRIMARY_GRADIENT_START": ("#1A44C2", "#1F49CC"),  # colores-ok: paleta del tema
        "CANVAS": ("#F9FAFB", "#0E0F11"),  # colores-ok: paleta del tema
        "CANVAS_CODE": ("#F3F4F6", "#121316"),  # colores-ok: paleta del tema
        "CANVAS_ELEVATED": ("#FCFDFE", "#17191C"),  # colores-ok: paleta del tema
        "CANVAS_GLASS": ("#FCFDFECC", "#17191CCC"),  # colores-ok: paleta del tema
        "CANVAS_INSET": ("#ECEEF1", "#08090A"),  # colores-ok: paleta del tema
        "CANVAS_OVERLAY": ("#FCFDFE", "#22252A"),  # colores-ok: paleta del tema
        "FG": ("#0B0C0E", "#F4F5F7"),  # colores-ok: paleta del tema
        "FG_DISABLED": ("#7C828B", "#7C828B"),  # colores-ok: paleta del tema
        "FG_FAINT": ("#3A3F46", "#BDC2C9"),  # colores-ok: paleta del tema
        "FG_LINK": ("#1A3FB5", "#C6D2F2"),  # colores-ok: paleta del tema
        "FG_SUBTLE": ("#25292E", "#D6D9DE"),  # colores-ok: paleta del tema
        "FLAG_1": ("#E51414", "#E75A5A"),  # colores-ok: paleta del tema
        "FLAG_2": ("#E06F12", "#E49543"),  # colores-ok: paleta del tema
        "FLAG_3": ("#1EA44F", "#1BC057"),  # colores-ok: paleta del tema
        "FLAG_4": ("#4184F0", "#6FA6EA"),  # colores-ok: paleta del tema
        "FLAG_5": ("#DC50F1", "#DE84ED"),  # colores-ok: paleta del tema
        "FLAG_6": ("#219F8F", "#1BBCA3"),  # colores-ok: paleta del tema
        "FLAG_7": ("#A85AF2", "#C091EF"),  # colores-ok: paleta del tema
        "HIGHLIGHT_BG": ("#1A44C2", "#1F49CC"),  # colores-ok: paleta del tema
        "HIGHLIGHT_FG": ("#FFFFFF", "#FFFFFF"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG": ("#9BA1A9", "#5A6069"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_ACTIVE": ("#4B5059", "#A1A7B0"),  # colores-ok: paleta del tema
        "SCROLLBAR_BG_HOVER": ("#6E747D", "#7C828B"),  # colores-ok: paleta del tema
        "SELECTED_BG": ("#1A44C240", "#8EA9FF55"),  # colores-ok: paleta del tema
        "SELECTED_FG": ("#0B0C0E", "#F4F5F7"),  # colores-ok: paleta del tema
        "SHADOW": ("#0B0C0E26", "#00000066"),  # colores-ok: paleta del tema
        "SHADOW_FOCUS": ("#1A44C240", "#8EA9FF4D"),  # colores-ok: paleta del tema
        "SHADOW_INSET": ("#0B0C0E1A", "#0000004D"),  # colores-ok: paleta del tema
        "SHADOW_SUBTLE": ("#0B0C0E12", "#00000033"),  # colores-ok: paleta del tema
        "STATE_BURIED": ("#C38110", "#9D4916"),  # colores-ok: paleta del tema
        "STATE_LEARN": ("#941818", "#F09999"),  # colores-ok: paleta del tema
        "STATE_MARKED": ("#6366F1", "#A863E9"),  # colores-ok: paleta del tema
        "STATE_NEW": ("#0D45A1", "#9FC6F1"),  # colores-ok: paleta del tema
        "STATE_REVIEW": ("#0C5728", "#23CB61"),  # colores-ok: paleta del tema
        "STATE_SUSPENDED": ("#AB8B0E", "#B6A91A"),  # colores-ok: paleta del tema
        "NOCTURNE_CONTROL_BORDER": ("#4B5059", "#A1A7B0"),  # colores-ok: paleta del tema
        "NOCTURNE_ROW_HIGHLIGHT": ("#E3E8F5", "#121C3A"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_PRESSED": ("#112E87", "#143394"),  # colores-ok: paleta del tema
        "NOCTURNE_PRIMARY_RING": ("#0B0C0E", "#F4F5F7"),  # colores-ok: paleta del tema
    }
)

# Orden en que aparecen en la ventana de configuración.
THEMES: dict[str, Theme] = {
    "nocturne": {"colors": PALETTE, "look": NOCTURNE_LOOK},
    "papel": {"colors": PAPEL, "look": PAPEL_LOOK},
    "grafito": {"colors": GRAFITO, "look": GRAFITO_LOOK},
    "bosque": {"colors": BOSQUE, "look": BOSQUE_LOOK},
    "alto_contraste": {"colors": CONTRASTE, "look": CONTRASTE_LOOK},
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
