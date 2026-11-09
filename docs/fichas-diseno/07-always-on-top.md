# Ficha de diseño: Always on Top

Versión 1.2 (21 de octubre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Mantiene la ventana Añadir de Anki por encima de todas las ventanas del ordenador, también de otros
programas, y se enciende y apaga con un atajo (Ctrl+Mayús+O de serie).

## 2. Para quién y para qué

Para crear tarjetas copiando de un documento o una página web sin que Añadir quede tapada. No toca la
colección; solo guarda el atajo.

## 3. Aspecto propio

No pinta nada: sin colores, iconos ni letra propios. Su interfaz son un aviso breve de Anki y una
ventana de opciones nativa (colores de Atelier).

## 4. Dónde actúa

- Solo sobre la ventana Añadir (la normal y la que se abre con Mayús+Añadir).
- El atajo responde en cualquier ventana de Anki que esté delante (principal, repaso, Explorar,
  Añadir), no en otros programas.
- Herramientas > Complementos > Always on Top > Configuración: ventana de opciones.
- No añade menús, botones ni iconos.

## 5. Encender y apagar

- Cada pulsación cambia el estado.
- Aviso breve de Anki durante 1,5 s, abajo a la izquierda de la ventana de Anki que esté delante:
  «Siempre visible: activado» o «Siempre visible: desactivado».
- Con Añadir abierta, el cambio es inmediato; si no, el estado queda para la próxima vez que se abra.
- Con el efecto encendido, Añadir sigue encima aunque se pase a otro programa, y al cerrarla y
  reabrirla.
- El estado dura mientras Anki esté abierto (también al cambiar de perfil); al cerrar Anki se olvida.
- Sin parpadeo en Windows (ni movimiento ni pérdida de foco). Al abrir Añadir con el efecto encendido,
  se aplica antes de que aparezca. En Mac y Linux, la ventana desaparece un instante y vuelve en el
  mismo sitio.

## 6. El atajo

- De serie Ctrl+Mayús+O (Anki 26.09.3 no lo usa).
- Debe llevar Ctrl o Alt y no estar usado por Anki (lista fija sacada de Anki 25.09, más los atajos de
  los menús de la ventana principal en ese momento, incluidos los de otros complementos).
- Una sola combinación, no secuencias.
- Si el guardado no sirve, al abrir Anki usa Ctrl+Mayús+O sin avisar.

## 7. Ventana de opciones

- Título «Always on Top», sin botón de ayuda, modal, sobre la ventana que estuviera delante. Ancho
  mínimo 420 px. No recuerda tamaño ni posición.
- Una línea: «Atajo:» y un campo grabador de atajos con el actual, escrito con los nombres de teclas del
  idioma (en español, «Control+Mayúsculas+O»). Con el cursor puesto al abrir y una pequeña cruz para
  vaciarlo; vacío muestra en gris «Presione el atajo de teclado».
- Graba la siguiente combinación que se pulse, sea cual sea: con el cursor en el campo, Intro y Esc se
  graban («Retorno», «Escape») en vez de aceptar o cerrar, y luego se rechazan.
- Botones estándar: «Restaurar los valores predeterminados» (pone Ctrl+Mayús+O, aviso de Anki «Se
  restauró la configuración predeterminada», sin guardar), «Aceptar» y «Cancelar».
- Aceptar: vacío, guarda Ctrl+Mayús+O (no se puede dejar sin atajo). Si no sirve, ventana «Always on
  Top»: «No se puede usar «Control+Q». Elige una combinación que incluya Ctrl o Alt y que Anki no use
  ya.», y la de opciones sigue abierta con el cursor en el campo. Si sirve, guarda y funciona al
  momento, sin aviso.

## 8. Accesibilidad

- Todo con el teclado: el atajo y la ventana (campo con el foco al abrir; botones con Tab).
- Punto débil: el estado no se ve en ningún sitio salvo el aviso de 1,5 s; no hay indicador permanente
  (por ejemplo, en el título de Añadir).
- Punto débil: Intro y Esc no funcionan como esperaría la persona dentro del campo del atajo.
- El aviso breve desaparece solo y puede no anunciarse al lector de pantalla.
- Trato mezclado: «Presione» (usted) y «Elige» (tú).

## 9. Textos e idiomas

Textos: «Siempre visible: activado», «Siempre visible: desactivado», «Atajo:», «Presione el atajo de
teclado», el aviso de combinación no válida, «Se restauró la configuración predeterminada», «Always on
Top: Se produjo un problema». 60 idiomas (si falta, inglés), con portugués de Brasil y de Portugal y
chino simplificado y tradicional. Botones, nombres de teclas y aviso de restaurar, de Qt y Anki.

## 10. Qué guarda

Solo el atajo, en la configuración de complementos del ordenador (todos los perfiles, no se
sincroniza). El estado encendido o apagado no se guarda. Nada en la colección.

## 11. Si algo falla

Nunca la ventana de error de Anki: aviso de 1,5 s «Always on Top: Se produjo un problema», una vez por
función y sesión.

## 12. Fallos conocidos pendientes

- Acepta seis atajos que el editor de Añadir de Anki 26.09.3 ya usa (Ctrl+. y Ctrl+, para listas,
  Ctrl+Mayús+. y Ctrl+Mayús+, para sangría, Ctrl+= y Ctrl+Mayús+= para superíndice y subíndice).
- Con las dos ventanas Añadir abiertas, solo cambia la última.

## 13. Decisiones tomadas a propósito

Atajo inválido al abrir: vuelve al de serie sin avisar. La ventana no se cierra con una combinación
inválida. No se puede dejar sin atajo. El atajo responde en cualquier ventana de Anki. Vía propia de
Windows sin parpadeo. Un fallo avisa una vez por sesión. Botones con textos de Qt.

## 14. Qué no hace

No se conecta a internet, no lee ni cambia la colección, no mantiene encima otras ventanas de Anki, no
recuerda el estado al reabrir Anki, no muestra el estado de forma permanente.
