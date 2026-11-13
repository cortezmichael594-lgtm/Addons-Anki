"""Todos los textos que ve la persona, en español y en un solo sitio."""

from __future__ import annotations

# Menú Herramientas y ventana
MENU_OPTIONS = "Sonidos de consola…"
OPTIONS_TITLE = "Sonidos de consola"

VOLUME_LABEL = "&Volumen:"
VOLUME_ACCESSIBLE = "Volumen de los sonidos"
VOLUME_TIP = "Mueva la barra para cambiar el volumen: oirá el tic de navegación con el volumen nuevo al soltarla o con cada paso del teclado."

NAVIGATION_LABEL = "&Navegación en los menús:"
NAVIGATION_CHOICES = {
    "hover": "Al pasar el ratón o las flechas por las opciones",
    "click": "Solo al hacer clic",
    "off": "Nunca",
}

SOUNDS_GROUP = "Sonidos"
SOUND_LABELS = {
    "coldboot": "Al abrir Anki",
    "gameboot": "Globo de notificación",
    "option": "Navegación por los menús",
    "cancel": "Cancelar, cerrar o salir del estudio",
    "system_ok": "Sincronización correcta o «Sí» en una pregunta",
    "system_ng": "Al comenzar a estudiar",
    "error": "Error o aviso de Anki",
}
TEST_BUTTON = "Probar"
TEST_ACCESSIBLE = "Probar el sonido «{label}»"
FILE_MISSING = "Falta {file}"
FILE_READY = "{file}"

OPEN_FOLDER = "Abrir carpeta de &sonidos"
OPEN_FOLDER_TIP = "Copie ahí sus siete archivos .wav con su nombre exacto. Se conservan al actualizar el complemento."
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
