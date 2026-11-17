"""HTML de la insignia que se antepone a la tarjeta durante el repaso.

No usa Qt ni la colección: recibe qué insignia toca y devuelve el HTML, así que se puede
probar suelto. La forma y los colores están en web/flags.css; aquí solo el contenido.
"""

from __future__ import annotations

import html
from typing import Final

from .strings import FlagKey, flag_label

# 2.6.0 (informe «Rediseño de color y forma» del 2026-11-17, apartado 8.6): cada icono es un
# círculo de 24 px del color de su insignia con un dibujo encima, en blanco de día y en el
# tono oscuro de su color de noche (web/flags.css). Los dibujos toman currentColor, para que
# el contraste alto de Windows los pinte con el color del texto.
_DISC: Final[str] = '<circle class="profeedback-badge-disc" cx="12" cy="12" r="12"/>'
_SVG_OPEN: Final[str] = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
_STROKE: Final[str] = (
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
)

_ICONS: Final[dict[FlagKey, str]] = {
    # «OTRA OPORTUNIDAD»: una flecha en bucle, de trazo de 2 px.
    "previous_mistake": (
        _SVG_OPEN + _DISC + f'<g class="profeedback-badge-draw" {_STROKE}>'
        '<path d="M16.6 13.6A4.8 4.8 0 1 1 15.8 8.6"/><path d="M16.4 5.6v3.4h-3.4"/></g></svg>'
    ),
    # «SE RESISTE»: una pesa, de trazo de 2 px.
    "hard_exercise": (
        _SVG_OPEN + _DISC + f'<g class="profeedback-badge-draw" {_STROKE}>'
        '<path d="M9 12h6M8 8.5v7M16 8.5v7M5.5 10.5v3M18.5 10.5v3"/></g></svg>'
    ),
    # «TARJETA NUEVA»: el destello de cuatro puntas de CoreProgress, de 11 px.
    "new_card": (
        _SVG_OPEN + _DISC + '<g class="profeedback-badge-draw">'
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
