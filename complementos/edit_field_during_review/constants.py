# Historial de correcciones de este archivo:
# FIX-004 (2026-11-09) — Una tarjeta podía cargar archivos de otros complementos.

from __future__ import annotations

import re

PACKAGE: str = __name__.split(".")[0]

# Nombre visible (coincide con "name" de manifest.json). Los nombres de
# complemento no se traducen; lo estructural del panel de opciones (título,
# botones) sí, porque viene del catálogo de Anki.
ADDON_NAME: str = "Edit field during review"

# --- FIX-004 (2026-11-09) ---
# Síntoma: una tarjeta preparada a propósito podía hacer que el repaso cargara
#          archivos de estilo o de código de otros complementos.
# Causa: el patrón «web/.*» aceptaba «..» y cualquier carpeta.
# Regla: el patrón de setWebExports es cerrado: solo los dos archivos que usa
#        el repaso, sin «/» ni «.» libres (como en GritMap y el ejemplo).
WEB_EXPORTS: str = r"web/editor\.(css|js)"
CSS_URL: str = f"/_addons/{PACKAGE}/web/editor.css"
JS_URL: str = f"/_addons/{PACKAGE}/web/editor.js"

MSG_PREFIX: str = "lfe:"

REVIEW_CONTEXTS: frozenset[str] = frozenset(
    {"reviewQuestion", "reviewAnswer", "previewQuestion", "previewAnswer"}
)
QUESTION_CONTEXTS: frozenset[str] = frozenset({"reviewQuestion", "previewQuestion"})

SIDE_QUESTION: str = "question"
SIDE_ANSWER: str = "answer"

KIND_FIELD: str = "field"
KIND_TAGS: str = "tags"
TAGS_LABEL: str = "Tags"

CLOZE_RE: re.Pattern[str] = re.compile(r"\{\{c\d+::")
AV_REF_RE: re.Pattern[str] = re.compile(r"\[anki:play:[^\]]*\]")
