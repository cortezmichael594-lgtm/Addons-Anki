from __future__ import annotations

import re

PACKAGE: str = __name__.split(".")[0]

# Nombre visible (coincide con "name" de manifest.json). Los nombres de
# complemento no se traducen; lo estructural del panel de opciones (título,
# botones) sí, porque viene del catálogo de Anki.
ADDON_NAME: str = "Edit field during review"

WEB_EXPORTS: str = r"web/.*\.(css|js)"
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
