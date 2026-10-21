"""Canal nativo: tiñe los widgets Qt reescribiendo los tokens de color de Anki.

Anki guarda sus colores en ``aqt.colors`` como diccionarios ``{"light", "dark"}``
y los lee en todas partes: la paleta Qt, los menús, las tablas y su propia hoja
de estilo. Si reescribimos esos diccionarios con la paleta Nocturne y pedimos a
Anki que vuelva a aplicar su estilo, toda la interfaz nativa adopta los colores.

Reescribir tokens (en vez de mantener una paleta Qt propia y paralela) hace el
complemento más resistente a futuras versiones: Anki sigue encargándose de armar
la paleta con sus reglas, nosotros solo cambiamos los valores de origen. Y como
esos valores quedan escritos en el módulo de Anki, cada vez que Anki rehace su
estilo por su cuenta —al cambiar de día a noche, o al cambiar el estilo de los
controles en las preferencias— vuelve a leer los nuestros sin que hagamos nada.
"""

# Historial de correcciones de este archivo:
# FIX-003 (2026-10-21): casillas sin marcar casi invisibles.

from __future__ import annotations

import aqt.colors
from aqt import mw
from aqt.theme import WidgetStyle, theme_manager

from .errors import get_logger, guard, guard_filter
from .palette import GRADIENT_ALIASES, PALETTE, to_css_rgba


def write_theme_colors() -> None:
    """Vuelca la paleta Nocturne sobre los tokens de color de Anki.

    Es idempotente: puede llamarse varias veces (arranque, cambio de perfil) sin
    efectos secundarios. Si algún token no existiera en esta versión de Anki, se
    omite sin fallar.
    """
    for name, entry in PALETTE.items():
        token = getattr(aqt.colors, name, None)
        if not isinstance(token, dict):
            continue
        token["light"] = to_css_rgba(entry["light"])
        token["dark"] = to_css_rgba(entry["dark"])

    # Los dos alias de gradiente siguen al color de hover de los botones.
    hover = PALETTE["BUTTON_HOVER"]
    for alias in GRADIENT_ALIASES:
        token = getattr(aqt.colors, alias, None)
        if not isinstance(token, dict):
            continue
        token["light"] = hover["light"]
        token["dark"] = hover["dark"]


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
        get_logger().exception("no se pudo reaplicar el estilo de Qt")
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
    border_token = PALETTE["NOCTURNE_CONTROL_BORDER"]
    focus_token = PALETTE["BORDER_FOCUS"]
    if theme_manager.night_mode:
        border, focus = border_token["dark"], focus_token["dark"]
    else:
        border, focus = border_token["light"], focus_token["light"]
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
    )


@guard
def on_profile_open() -> None:
    """Reafirma los colores al abrir un perfil (cubre el cambio de perfil).

    Basta con reafirmar los valores: nada borra la hoja de estilo de Qt al
    cambiar de perfil, y rehacerla obligaría a repintar todas las ventanas para
    dejarlas exactamente igual, con el parpadeo que eso supone.
    """
    write_theme_colors()
