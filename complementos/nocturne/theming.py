"""Canal nativo: tiñe los widgets Qt reescribiendo los tokens de color de Anki.

Anki guarda sus colores en ``aqt.colors`` como diccionarios ``{"light", "dark"}``
y los lee en todas partes: la paleta Qt, los menús, las tablas y su propia hoja
de estilo. Si reescribimos esos diccionarios con la paleta elegida y pedimos a
Anki que vuelva a aplicar su estilo, toda la interfaz nativa adopta los colores.
Lo mismo con sus medidas (``aqt.props``): el radio de las esquinas.

Reescribir tokens (en vez de mantener una paleta Qt propia y paralela) hace el
complemento más resistente a futuras versiones: Anki sigue encargándose de armar
la paleta con sus reglas, nosotros solo cambiamos los valores de origen. Y como
esos valores quedan escritos en el módulo de Anki, cada vez que Anki rehace su
estilo por su cuenta —al cambiar de día a noche, o al cambiar el estilo de los
controles en las preferencias— vuelve a leer los nuestros sin que hagamos nada.
"""

# Historial de correcciones de este archivo:
# FIX-003 (2026-10-21): casillas sin marcar casi invisibles.
# FIX-012 (2026-11-04): texto de la fila seleccionada de Explorar por debajo de 4,5:1.
# FIX-013 (2026-11-04): «Restablecer tamaños de las ventanas» relleno como botón principal.

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

import aqt.colors
import aqt.props
from anki.hooks import wrap
from anki.utils import is_win
from aqt import mw
from aqt.qt import QColor, QIcon, QPainter
from aqt.theme import ThemeManager, WidgetStyle, theme_manager

from . import themes
from .errors import guard, guard_filter, note_failure
from .palette import GRADIENT_ALIASES, to_css_rgba

# Medidas de Anki que fija cada paleta (aqt.props) y la clave de su «Look».
PROPS = {
    "BORDER_RADIUS": "radius",
    "BORDER_RADIUS_MEDIUM": "radius_medium",
    "BORDER_RADIUS_LARGE": "radius_large",
}

# Versión 3.8.0: iconos de Anki repintados con los colores de la paleta (ver _icons_css).
_ICON_DIR = Path(__file__).parent / "user_files" / "iconos"

# Versión 3.8.0 (informe del 2026-11-04, apartado 2.1): color del lado «Tarjetas» del
# interruptor Tarjetas/Notas de Explorar. Anki lo pinta con ACCENT_CARD, un azul claro
# distinto del de acción (el mismo de «Nuevas»): dos azules para lo que se pulsa. Se usa el
# de acción: de día, el de botón con el ratón encima, y de noche el tono de trazo, para que
# su rótulo (en el color del fondo) se lea a 4,5:1 o más (lo miden las pruebas). El lado
# «Notas» sigue en verde. Lo rellena write_theme_colors; on_browser_will_show lo conecta.
SWITCH_CARDS: dict[str, str] = {"light": "", "dark": ""}


def write_theme_colors() -> None:
    """Vuelca la paleta elegida sobre los tokens de color y las medidas de Anki.

    Es idempotente: puede llamarse varias veces (arranque, cambio de perfil o de
    paleta) sin efectos secundarios. Si algún token no existiera en esta versión de
    Anki, se omite sin fallar.
    """
    palette = themes.colors()
    for name, entry in palette.items():
        token = getattr(aqt.colors, name, None)
        if not isinstance(token, dict):
            continue
        token["light"] = to_css_rgba(entry["light"])
        token["dark"] = to_css_rgba(entry["dark"])

    # Los dos alias de gradiente siguen al color de hover de los botones.
    hover = palette["BUTTON_HOVER"]
    for alias in GRADIENT_ALIASES:
        token = getattr(aqt.colors, alias, None)
        if not isinstance(token, dict):
            continue
        token["light"] = hover["light"]
        token["dark"] = hover["dark"]

    # Versión 3.8.0: el lado «Tarjetas» del interruptor de Explorar, en el color de acción.
    SWITCH_CARDS["light"] = to_css_rgba(palette["BUTTON_PRIMARY_GRADIENT_END"]["light"])
    SWITCH_CARDS["dark"] = to_css_rgba(palette["BORDER_FOCUS"]["dark"])

    look = themes.look()
    for name, key in PROPS.items():
        token = getattr(aqt.props, name, None)
        if not isinstance(token, dict):
            continue
        token["light"] = token["dark"] = f"{look[key]}px"  # type: ignore[literal-required]


def _clear_icon_caches() -> None:
    """Tira los iconos que Anki hubiera teñido con los colores anteriores.

    Anki guarda cada icono coloreado en una caché propia. Los que preparó antes
    de que cargara el complemento llevan su color original; vaciando la caché se
    vuelven a generar con la paleta nueva.
    """
    for name in ("_icon_cache_light", "_icon_cache_dark"):
        cache = getattr(theme_manager, name, None)
        if isinstance(cache, dict):
            cache.clear()


def restyle() -> bool:
    """Pide a Anki que reconstruya paleta y hoja de estilo con los colores nuevos.

    Se usa la vía pública de Anki (``theme_manager.apply_style``) en lugar de
    llamar a sus piezas internas una por una. Esa función se salta el trabajo si
    cree que nada ha cambiado, así que antes se invalida esa comprobación; a
    cambio, Anki hace por nosotros todo lo demás, siempre a su manera y por tanto
    al día con futuras versiones: rehace la paleta y la hoja de estilo, pone al
    día los colores de las gráficas y avisa a sus pantallas web, que repintan su
    fondo solas (que es lo que evita destellos al cargar una página).

    Devuelve ``True`` si la interfaz quedó al día y ``False`` si algo lo impidió
    (en cuyo caso Anki conserva su apariencia y el complemento no rompe nada).
    """
    if mw is None or mw.app is None:
        return False

    try:
        _clear_icon_caches()
        # Marca de "esto ya no vale" para que Anki no se ahorre el trabajo.
        theme_manager._current_widget_style = None
        theme_manager.apply_style()
    except Exception:
        note_failure("no se pudo reaplicar el estilo de Qt")
        return False
    return True


@guard_filter
def on_style_did_init(style: str) -> str:
    """Añade al final de la hoja de estilo de Anki el borde propio de las casillas.

    # --- FIX-003 (2026-10-21) ---
    # Síntoma: el borde de una casilla o botón de opción sin marcar casi no se distinguía
    #          del fondo (1,3:1 de día y 1,5:1 de noche).
    # Causa: Anki dibuja ese borde con BORDER, el mismo de la línea de la barra del repaso y
    #        otros detalles, y en Nocturne es muy suave a propósito.
    # Regla: el borde de las casillas se cambia aquí, solo para ellas, con
    #        NOCTURNE_CONTROL_BORDER (3:1 o más); con el ratón o el foco, BORDER_FOCUS, que
    #        destaca más. Solo se cambia el color, nunca el grosor, para que nada salte.

    Anki pasa la hoja por este filtro cada vez que la rehace, también al cambiar
    de día a noche, y ya ha decidido el modo. Con un estilo de controles que no sea
    el de Anki, su hoja no tiene estas reglas y se devuelve tal cual.
    """
    if mw is None or mw.pm.get_widget_style() != WidgetStyle.ANKI:
        return style
    palette = themes.colors()

    def pick(name: str) -> str:
        entry = palette[name]
        return to_css_rgba(entry["dark"] if theme_manager.night_mode else entry["light"])

    border, focus = pick("NOCTURNE_CONTROL_BORDER"), pick("BORDER_FOCUS")
    return (
        style
        + f"""
    QCheckBox::indicator,
    QRadioButton::indicator,
    QMenu::indicator {{
        border-color: {border};
    }}
    QCheckBox::indicator:focus:!disabled,
    QCheckBox::indicator:hover:!disabled,
    QCheckBox::indicator:checked:hover:!disabled,
    QRadioButton::indicator:focus:!disabled,
    QRadioButton::indicator:hover:!disabled {{
        border-color: {focus};
    }}
"""
        + _buttons_css(pick)
        + _tooltip_css(pick)
        + _selection_css(pick)
        + _fields_css(pick)
        + _tabs_css(pick)
        + _icons_css(pick)
        + _controls_css(pick)
        + _scrollbar_css()
    )


def _buttons_css(pick: Callable[[str], str]) -> str:
    """Botones de las ventanas (versión 3.1.0): esquinas de la paleta y el botón
    principal relleno del color de acción.

    Versión 3.5.0: botones y campos con la misma esquina, para que 6 y 7 px no se
    lean como un descuido (Refactoring UI, M2 y P4), y las casillas con una menor
    (4 px), para que no parezcan botones de opción.

    Un solo botón principal por ventana, relleno y con el mayor contraste, y el
    resto con su aspecto normal (Practical UI, P17; Refactoring UI, P11). En Qt, el
    botón «por defecto» es el que se pulsa con Intro, así que el relleno sigue a esa
    tecla. Como en la regla de FIX-003, borde más margen se mantienen: 1px sin
    foco y 2px (margen 0, que pone Anki) con el ratón encima o con el foco.

    Versión 3.8.0 (informe del 2026-11-04, apartado 2.1): solo se rellena el botón por
    defecto de la fila de botones del pie (QDialogButtonBox: Aceptar, Añadir, Guardar).
    Qt da ese papel a cualquier botón con el foco, y en Preferencias se lo daba a
    «Restablecer tamaños de las ventanas», que salía como la acción principal. Un botón
    del cuerpo conserva el aspecto de Anki: fondo normal y, si responde a Intro, el borde
    azul fino de Anki.

    Versión 3.9.0 (informe del 2026-11-11, apartado 8.5): con el ratón encima, el botón
    principal se oscurece sin anillo; el anillo queda para el foco, para que signifique una
    sola cosa («aquí está el teclado»). Pulsado, más oscuro y sin anillo. El borde sigue en
    2 px en esos estados, del color del relleno: nada salta (APR-059).
    """
    # --- FIX-013 (2026-11-04) ---
    # Síntoma: en Preferencias, «Restablecer tamaños de las ventanas» salía relleno del color de
    #          acción, como si fuera la acción principal, y «Cerrar» en gris.
    # Causa: el relleno seguía a cualquier botón «por defecto», y Qt da ese papel al botón del
    #        cuerpo que tiene el foco cuando la ventana no marca uno en el pie.
    # Regla: el relleno de acción es solo para el botón por defecto de la fila de botones del pie
    #        (QDialogButtonBox); un botón del cuerpo nunca se rellena.
    radius = themes.look()["button_radius"]
    side = getattr(theme_manager, "right", lambda: "right")()
    return f"""
    QPushButton {{
        border-radius: {radius}px;
    }}
    QComboBox,
    QSpinBox,
    QDateTimeEdit,
    QLineEdit,
    QListWidget,
    QTreeWidget,
    QListView,
    QTextEdit,
    QPlainTextEdit {{
        border-radius: {radius}px;
    }}
    QComboBox::drop-down {{
        border-top-{side}-radius: {radius}px;
        border-bottom-{side}-radius: {radius}px;
    }}
    QCheckBox::indicator,
    QMenu::indicator:non-exclusive {{
        border-radius: 4px;
    }}
    QDialogButtonBox QPushButton:default {{
        background: {pick("BUTTON_PRIMARY_BG")};
        color: {pick("HIGHLIGHT_FG")};
        border: 1px solid {pick("BUTTON_PRIMARY_BG")};
    }}
    QDialogButtonBox QPushButton:default:hover {{
        background: {pick("BUTTON_PRIMARY_GRADIENT_END")};
        border: 2px solid {pick("BUTTON_PRIMARY_GRADIENT_END")};
    }}
    QDialogButtonBox QPushButton:default:focus {{
        background: {pick("BUTTON_PRIMARY_GRADIENT_END")};
        border: 2px solid {pick("NOCTURNE_PRIMARY_RING")};
    }}
    QDialogButtonBox QPushButton:default:pressed {{
        background: {pick("NOCTURNE_PRIMARY_PRESSED")};
        border: 2px solid {pick("NOCTURNE_PRIMARY_PRESSED")};
    }}
    QDialogButtonBox QPushButton:default:disabled {{
        background: {pick("BUTTON_BG")};
        color: {pick("FG_DISABLED")};
        border: 1px solid {pick("BORDER")};
    }}
"""


def _tooltip_css(pick: Callable[[str], str]) -> str:
    """Ayudas emergentes (versión 3.3.0): el mismo fondo y borde que los menús.

    Anki las pinta con el color del fondo de la ventana y sin borde, de modo que se
    confunden con lo que tapan. Como los menús, flotan sobre la ventana: fondo de
    superposición, borde suave y algo de aire alrededor del texto (Refactoring UI,
    profundidad; Practical UI, M3).

    Versión 3.9.0 (informe del 2026-11-11, apartados 2.4 y 8.6): globos y menús con el borde
    fuerte (BORDER_STRONG), que se ve sobre el propio globo y sobre el fondo; el suave se
    confundía con los dos (1,06:1). Relleno de 6 por 8 px en los globos y opciones de menú de
    28 px de alto con 12 px a los lados.
    """
    return f"""
    QToolTip {{
        background-color: {pick("CANVAS_OVERLAY")};
        border: 1px solid {pick("BORDER_STRONG")};
        padding: 6px 8px;
    }}
    QMenu {{
        border-color: {pick("BORDER_STRONG")};
    }}
    QMenu::item {{
        padding: 6px 12px;
    }}
"""


def _selection_css(pick: Callable[[str], str]) -> str:
    """Versión 3.7.0 (informe del 2026-10-28, apartado 9): una sola forma de marcar lo
    seleccionado en todo Anki, el tinte de acción con el texto normal, como la fila del
    mazo actual y las filas de Explorar. El relleno de acción con texto blanco queda
    para el botón principal (Practical UI, P17). Y las cabeceras de las columnas de
    Explorar en el texto secundario, como las de la lista de mazos (Refactoring UI, P8).
    Solo color y grosor de letra: nada cambia de tamaño ni de sitio."""
    # --- FIX-012 (2026-11-04) ---
    # Síntoma: en Explorar, el texto de la fila seleccionada se leía a 4,46:1 en Nocturne de noche
    #          (y a 3,1-4,1 en Papel, Bosque y Atardecer), por debajo del 4,5 prometido.
    # Causa: Anki marca la selección con SELECTED_BG, que es transparente, y Explorar lo pinta
    #        tres veces encima de la fila; nadie había medido el color que resulta.
    # Regla: el fondo de lo seleccionado en las tablas es opaco (NOCTURNE_TABLE_SELECTED) y se
    #        mide con el texto encima tal como se ve (lo comprueba TableSelectionTest).
    return f"""
    QMenu::item:selected,
    QComboBox::item:selected {{
        background-color: {pick("NOCTURNE_ROW_HIGHLIGHT")};
        color: {pick("FG")};
    }}
    QHeaderView::section {{
        color: {pick("FG_SUBTLE")};
    }}
    QTableView {{
        selection-background-color: {pick("NOCTURNE_TABLE_SELECTED")};
        selection-color: {pick("SELECTED_FG")};
    }}
    QCheckBox::indicator:checked:!disabled {{
        background: {pick("BUTTON_PRIMARY_BG")};
        border-color: {pick("BUTTON_PRIMARY_BG")};
    }}
"""


def _fields_css(pick: Callable[[str], str]) -> str:
    """Versión 3.8.0 (informe del 2026-11-04, apartado 2.2): campos de texto, campos
    numéricos y listas desplegables con un borde visible, el mismo de las casillas
    (NOCTURNE_CONTROL_BORDER, a 3:1 o más sobre cualquier fondo; WCAG 1.4.11). Antes se
    distinguían del fondo a 1,04, 1,05 o 1,19:1 y el filtro de Explorar casi no se veía
    como campo. Solo cambia el color, no el grosor: nada se mueve. Con el foco, Anki ya
    pone el color de acción (sus reglas :focus ganan a esta). Las listas, las tablas y
    los separadores siguen suaves, como eligió el cliente en octubre.

    El campo de texto de dentro de una lista desplegable editable (el buscador de
    Explorar) no lleva borde propio: ya lo tiene la lista que lo rodea.
    """
    border = pick("NOCTURNE_CONTROL_BORDER")
    return f"""
    QLineEdit,
    QComboBox,
    QComboBox:!editable,
    QSpinBox,
    QDateTimeEdit,
    QTextEdit,
    QPlainTextEdit {{
        border-color: {border};
    }}
    QComboBox QLineEdit {{
        border-color: transparent;
    }}
    QComboBox:!editable:focus {{
        border-color: {pick("BORDER_FOCUS")};
    }}
"""


def _tabs_css(pick: Callable[[str], str]) -> str:
    """Versión 3.8.0 (informe del 2026-11-04, apartado 2.1): la pestaña activa, con el
    tinte de acción, el texto normal y una raya de 2 px en el tono de trazo, en vez de
    rellena de azul con texto blanco: era otra superficie azul que competía con el botón
    principal, y así se marca como lo demás seleccionado (menús, listas y lista de mazos).

    La raya ocupa el borde inferior: pasa de 1 a 2 px y el relleno de abajo baja 1 px, de
    modo que la pestaña mide lo mismo y nada salta (APR-059). La letra no pasa a
    seminegrita: Qt mediría la pestaña más ancha y la barra se movería al cambiar de una a
    otra.
    """
    return f"""
    QTabBar::tab:selected,
    QTabBar::tab:selected:hover {{
        color: {pick("FG")};
        background: {pick("NOCTURNE_ROW_HIGHLIGHT")};
        border-bottom: 2px solid {pick("BORDER_FOCUS")};
        padding-bottom: 3px;
    }}
    QTabBar::tab:selected:disabled,
    QTabBar::tab:selected:hover:disabled {{
        color: {pick("FG_DISABLED")};
        background: {pick("BUTTON_DISABLED")};
    }}
"""


def _controls_css(pick: Callable[[str], str]) -> str:
    """Versión 3.9.0 (informe del 2026-11-11, apartados 2.1, 2.3, 2.5 y 8.6): las reglas
    del rediseño en las ventanas.

    - Un borde para todo lo que se pulsa o se rellena: los botones llevan el borde de control
      (NOCTURNE_CONTROL_BORDER), el de los campos y las casillas, en sus cuatro lados (Anki
      pone el inferior en SHADOW). Antes se distinguían del fondo a 1,29:1 y de un recuadro a
      1,05:1. Con el ratón encima, BUTTON_HOVER_BORDER (sobre el botón con el ratón, el de
      control bajaría de 3:1); pulsado, el fondo baja un escalón (NOCTURNE_BUTTON_PRESSED);
      desactivado, el borde suave. El botón con el foco y el que responde a Intro conservan el
      borde azul de Anki (sus reglas son más específicas). Solo cambia el color: nada salta.
    - Un tamaño de control: botones, listas desplegables, campos y pestañas miden 28 px de
      alto en las ventanas (antes 21, 23, 26 y 27). En la hoja de Qt, min-height mide solo el
      contenido: se le resta el relleno, el borde y el margen que pone Anki (medido dibujando
      cada control con la hoja de Anki). Los botones del pie, 88 px de ancho como mínimo.
    - Lo inactivo se atenúa: las pestañas que no están elegidas van sin relleno y en el texto
      secundario; con el ratón encima, con el fondo de botón y el texto normal. Así la activa
      es la única con relleno (antes las demás eran más claras que ella).
    - El texto de ejemplo de los campos, en el texto tenue: en el secundario parecía escrito.
    """
    pad = 25 if is_win else 15  # relleno lateral de los botones en la hoja de Anki
    return f"""
    QPushButton {{
        border-color: {pick("NOCTURNE_CONTROL_BORDER")};
        min-height: 22px;
    }}
    QPushButton:hover:!focus:!default {{
        border-color: {pick("BUTTON_HOVER_BORDER")};
    }}
    QPushButton:pressed:!default {{
        background: {pick("NOCTURNE_BUTTON_PRESSED")};
    }}
    QPushButton:disabled {{
        border-color: {pick("BORDER")};
    }}
    QDialogButtonBox QPushButton {{
        min-width: {86 - 2 * pad}px;
    }}
    QLineEdit {{
        min-height: 22px;
    }}
    QComboBox {{
        min-height: 23px;
    }}
    QSpinBox,
    QDateTimeEdit {{
        min-height: 19px;
    }}
    QComboBox QLineEdit,
    QAbstractSpinBox QLineEdit {{
        min-height: 0px;
    }}
    QLineEdit,
    QTextEdit,
    QPlainTextEdit {{
        placeholder-text-color: {pick("FG_FAINT")};
    }}
    QTabBar::tab {{
        min-height: 18px;
    }}
    QTabBar::tab:!selected {{
        background: transparent;
        color: {pick("FG_SUBTLE")};
    }}
    QTabBar::tab:!selected:hover {{
        background: {pick("BUTTON_BG")};
        color: {pick("FG")};
    }}
    QTabBar::tab:!selected:disabled {{
        background: transparent;
        color: {pick("FG_DISABLED")};
    }}
"""


def _scrollbar_css() -> str:
    """Versión 3.9.0 (informe del 2026-11-11, apartado 8.6): barra de desplazamiento con el
    carril de 12 px sin fondo, como en Anki, y el tirador de 8 px, centrado y redondo. Los
    colores del tirador (SCROLLBAR_BG y sus estados) ya llegan a 3:1. No cambia de ancho en
    ningún estado: nada se mueve."""
    return """
    QScrollBar:vertical {
        padding: 0px 2px;
    }
    QScrollBar:horizontal {
        padding: 2px 0px;
    }
    QScrollBar::handle {
        border-radius: 4px;
    }
"""


def _icons_css(pick: Callable[[str], str]) -> str:
    """Versión 3.8.0 (informe del 2026-11-04, apartado 1.4): las flechas de las listas
    desplegables, de los campos numéricos y de orden de las columnas, en el texto
    secundario, y la marca de las casillas marcadas, en blanco sobre el color de acción.

    Anki trae estos iconos ya pintados en un blanco casi puro (de noche) o casi negro (de
    día), así que no siguen la paleta; se repintan copiando su dibujo con otro color en
    user_files. Si algo falla, quedan los de Anki.
    """
    subtle, on_action = pick("FG_SUBTLE"), pick("HIGHLIGHT_FG")
    icons = {
        "QComboBox::down-arrow": _tinted_icon("chevron-down", subtle),
        "QSpinBox::up-arrow, QDateTimeEdit::up-arrow": _tinted_icon("chevron-up", subtle),
        "QSpinBox::down-arrow, QDateTimeEdit::down-arrow": _tinted_icon("chevron-down", subtle),
        "QHeaderView::up-arrow": _tinted_icon("menu-up", subtle),
        "QHeaderView::down-arrow": _tinted_icon("menu-down", subtle),
        "QCheckBox::indicator:checked:!disabled": _tinted_icon("check", on_action),
    }
    return "".join(
        f"""
    {selector} {{
        image: url({path});
    }}"""
        for selector, path in icons.items()
        if path
    )


def _tinted_icon(name: str, color: str) -> str:
    """Copia el icono «name» de Anki con el color dado y devuelve su ruta para la hoja de
    estilo, o "" si no se pudo. El color solo puede ser hexadecimal (#RRGGBB): con otro
    formato no se toca nada. Cada archivo lleva el color en el nombre, así que no se
    reescribe si ya existe."""
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
        return ""
    try:
        from aqt.utils import aqt_data_folder

        source = Path(aqt_data_folder()) / "qt" / "icons" / f"{name}-dark.svg"
        target = _ICON_DIR / f"{name}-{color[1:].lower()}.svg"
        if not target.exists():
            svg = source.read_text(encoding="utf-8")
            tinted, count = re.subn(r'fill="#[0-9A-Fa-f]{3,8}"', f'fill="{color}"', svg, count=1)
            if count != 1:
                return ""
            _ICON_DIR.mkdir(parents=True, exist_ok=True)
            target.write_text(tinted, encoding="utf-8")
    except Exception:
        note_failure(f"no se pudo preparar el icono «{name}»")
        return ""
    # Como hace Anki en theme_manager.themed_icon: barras normales y, por un fallo de Qt,
    # comillas y letras acentuadas de la ruta escapadas con «\».
    path = target.as_posix().replace("\\\\?\\", "")
    return re.sub(r"(['¡-ÿ])", r"\\\1", path)


# Versión 3.9.0 (informe del 2026-11-11, apartado 1.4): un gris para todos los iconos, el texto
# secundario. Anki dibuja en negro los iconos sin color propio (la barra lateral de Explorar, sus
# herramientas) y de noche los invierte: salían en blanco puro, a 18:1, más fuertes que el texto
# que acompañan. Los iconos con color propio (banderas, estados) no se tocan. Anki no ofrece un
# gancho para esto: se envuelve su función (APR-015; está en «Así a propósito»). Si falla una
# vez, se deja de teñir hasta el próximo arranque y quedan los iconos de Anki.
_TINTED_ICONS: dict[tuple[str, str], QIcon] = {}
_ICON_TINT = {"installed": False, "active": True}
_ICON_PIXELS = 64  # se dibuja grande y Qt lo reduce: nítido con cualquier tamaño de interfaz


def install_icon_tint() -> None:
    """Envuelve ThemeManager.icon_from_resources una sola vez."""
    if _ICON_TINT["installed"]:
        return
    ThemeManager.icon_from_resources = wrap(  # type: ignore[method-assign]
        ThemeManager.icon_from_resources, _icon_from_resources, "around"
    )
    _ICON_TINT["installed"] = True


def _icon_from_resources(self: ThemeManager, path: object, _old: Callable[..., QIcon]) -> QIcon:
    if _ICON_TINT["active"] and isinstance(path, str):
        try:
            entry = themes.colors()["FG_SUBTLE"]
            color = entry["dark"] if self.night_mode else entry["light"]
            key = (path, color)
            icon = _TINTED_ICONS.get(key)
            if icon is None:
                source = self.themed_icon(path) if path.startswith("mdi:") else path
                pixmap = QIcon(source).pixmap(_ICON_PIXELS, _ICON_PIXELS)
                if pixmap.isNull():
                    return _old(self, path)
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter.fillRect(pixmap.rect(), QColor(color))
                painter.end()
                icon = _TINTED_ICONS.setdefault(key, QIcon(pixmap))
            return icon
        except Exception:
            _ICON_TINT["active"] = False
            note_failure("no se pudieron teñir los iconos")
    return _old(self, path)


@guard
def on_browser_will_show(browser: object) -> None:
    """Conecta el interruptor de Explorar a SWITCH_CARDS. Anki no ofrece forma de elegir su
    color, así que se cambia su atributo interno; si en otra versión de Anki no existe, el
    interruptor queda como lo dibuje Anki (está en «Así a propósito», APR-015)."""
    switch = getattr(browser, "_switch", None)
    if switch is None or not hasattr(switch, "_left_color"):
        return
    switch._left_color = SWITCH_CARDS
    switch.update()


@guard
def on_profile_open() -> None:
    """Reafirma los colores al abrir un perfil (cubre el cambio de perfil).

    Basta con reafirmar los valores: nada borra la hoja de estilo de Qt al
    cambiar de perfil, y rehacerla obligaría a repintar todas las ventanas para
    dejarlas exactamente igual, con el parpadeo que eso supone.
    """
    write_theme_colors()
