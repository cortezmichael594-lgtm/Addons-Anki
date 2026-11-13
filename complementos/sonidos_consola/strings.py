"""Todos los textos que ve la persona, en español y en un solo sitio."""

from __future__ import annotations

# Menú Herramientas y ventana
MENU_OPTIONS = "Sonidos de consola…"
OPTIONS_TITLE = "Sonidos de consola"

VOLUME_LABEL = "Volumen"
VOLUME_NOTE = "Vale para los siete sonidos. Pruébelo con «Probar», más abajo; se guarda al aceptar."

NAVIGATION_LABEL = "Cuándo suena"
NAVIGATION_CHOICES = {
    "hover": "Al pasar el ratón o las flechas por las opciones",
    "click": "Solo al hacer clic",
    "off": "Nunca",
}

SOUNDS_GROUP = "Cuándo suena cada sonido"
SOUNDS_NOTE = "Debajo de cada casilla, el archivo que usa. Desmarcada, ese sonido no suena."
SOUND_LABELS = {
    "coldboot": "Al abrir Anki",
    "gameboot": "Globo de notificación",
    "option": "Navegación por los menús",
    "cancel": "Cancelar, cerrar o salir del estudio",
    "system_ok": "Sincronización correcta o «Sí» en una pregunta",
    "system_ng": "Al comenzar a estudiar",
    "error": "Error o aviso de Anki",
}
FILE_MISSING = "Falta {file}: no sonará."
FILE_READY = "{file}"

FILES_GROUP = "Archivos de sonido"
TEST_LABEL = "Probar un sonido"
TEST_OPTION = "{label} ({file})"
TEST_BUTTON = "Probar"
TEST_EMPTY = "Aún no hay ningún sonido en la carpeta."
OPEN_FOLDER = "Abrir carpeta de sonidos"
MISSING_SUMMARY_NONE = "Están los siete sonidos."
MISSING_SUMMARY_ONE = "Falta 1 sonido: cópielo en la carpeta de sonidos."
MISSING_SUMMARY_MANY = "Faltan {count} sonidos: cópielos en la carpeta de sonidos."
NO_AUDIO = "Este ordenador no ofrece a Anki la función de sonido que usa el complemento: no sonará nada."

OPTIONS_SAVED = "Sonidos de consola: opciones guardadas."

# Avisos generales
ERROR_GENERIC = "Sonidos de consola tuvo un problema. Anki sigue funcionando; el detalle quedó en su registro."


def missing_summary(count: int) -> str:
    if count == 0:
        return MISSING_SUMMARY_NONE
    if count == 1:
        return MISSING_SUMMARY_ONE
    return MISSING_SUMMARY_MANY.format(count=count)
