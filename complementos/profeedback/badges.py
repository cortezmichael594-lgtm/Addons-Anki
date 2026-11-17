"""HTML de la insignia que se antepone a la tarjeta durante el repaso.

No usa Qt ni la colección: recibe qué insignia toca y devuelve el HTML, así que se puede
probar suelto. La forma y los colores están en web/flags.css; aquí solo el contenido.
"""

from __future__ import annotations

import html
from typing import Final

from .strings import FlagKey, flag_label

# 2.6.1 (petición de la persona, 2026-11-17): el icono es solo el dibujo, del color de su
# insignia, con el fondo transparente, de día y de noche (en la 2.6.0 iba sobre un círculo de
# color). El dibujo ocupa más del cuadro de 24 px (viewBox recortado) y el trazo se queda en
# 2 px. Toma currentColor, para que el contraste alto de Windows lo pinte con el color del
# texto (web/flags.css).
_SVG_OPEN: Final[str] = '<svg viewBox="4 4 16 16" width="24" height="24" aria-hidden="true" focusable="false">'
# El cuadro de 16 se dibuja a 24 px (× 1,5): un trazo de 1,33 queda en 2 px en pantalla.
_STROKE: Final[str] = (
    'fill="none" stroke="currentColor" stroke-width="1.33" stroke-linecap="round" stroke-linejoin="round"'
)

_ICONS: Final[dict[FlagKey, str]] = {
    # «OTRA OPORTUNIDAD»: una flecha en bucle, de trazo de 2 px.
    "previous_mistake": (
        _SVG_OPEN + f'<g class="profeedback-badge-draw" {_STROKE}>'
        '<path d="M16.6 13.6A4.8 4.8 0 1 1 15.8 8.6"/><path d="M16.4 5.6v3.4h-3.4"/></g></svg>'
    ),
    # «SE RESISTE»: una pesa, de trazo de 2 px.
    "hard_exercise": (
        _SVG_OPEN + f'<g class="profeedback-badge-draw" {_STROKE}>'
        '<path d="M9 12h6M8 8.5v7M16 8.5v7M5.5 10.5v3M18.5 10.5v3"/></g></svg>'
    ),
    # «TARJETA NUEVA»: el destello de cuatro puntas de CoreProgress, de 11 px.
    "new_card": (
        _SVG_OPEN + '<g class="profeedback-badge-draw">'
        '<path fill="currentColor" d="M12 6.5l1.5 4 4 1.5-4 1.5-1.5 4-1.5-4-4-1.5 4-1.5z"/></g></svg>'
    ),
}


# Franja vacía del mismo alto que una insignia (2.5.0, informe 2.4.0, apartado 8.6): con ella
# la tarjeta empieza siempre en el mismo sitio, haya insignia o no.
EMPTY_BADGE_HTML: Final[str] = '<div class="profeedback-badge profeedback-badge--none" aria-hidden="true"></div>'


def badge_html(flag: FlagKey) -> str:
    """Insignia lista para anteponer al HTML de la tarjeta."""
    label = html.escape(flag_label(flag))
    modifier = flag.replace("_", "-")
    return (
        f'<div class="profeedback-badge profeedback-badge--{modifier}" role="note">'
        f"{_ICONS[flag]}<span>{label}</span></div>"
    )
