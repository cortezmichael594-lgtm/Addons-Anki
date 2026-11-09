# Ficha de diseño: Always on Top

Versión 1.3 (9 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Mantiene la ventana Añadir de Anki por encima de todas las ventanas del ordenador, también de otros
programas, y se enciende y apaga con un atajo (Ctrl+Mayús+O de serie).

## 2. Para quién y para qué

Para crear tarjetas copiando de un documento o una página web sin que Añadir quede tapada. No toca la
colección; solo guarda el atajo.

## 3. Aspecto propio

No pinta nada: sin colores, iconos ni letra propios. Su interfaz son un aviso breve de Anki y una
ventana de opciones con el modelo del panel de GritMap (colores de la paleta).

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

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «Always on Top». Un recuadro con «Restaurar los valores predeterminados» (y «Deshacer») y
  el campo grabador «Atajo» con el foco al abrir: muestra la combinación con los nombres de teclas
  del idioma («Control+Mayúsculas+O»), en seminegrita; vacío, «Presione el atajo de teclado» en gris.
  A su lado, una cruz para vaciarlo. Graba la combinación que se pulse; Tab, Mayús+Tab y Esc siguen
  haciendo lo suyo; Retroceso o Supr solos lo vacían.
- Si la combinación no sirve, el aviso sale en rojo encima del campo (con icono) y el campo lleva
  borde rojo; la ventana no se cierra.

## 8. Accesibilidad

- Todo con el teclado: el atajo y la ventana (campo con el foco al abrir; botones con Tab).
- Punto débil: el estado no se ve en ningún sitio salvo el aviso de 1,5 s; no hay indicador permanente
  (por ejemplo, en el título de Añadir).
- Dentro del campo del atajo, Tab y Esc hacen lo de siempre (desde la 1.3); Intro sí se graba como parte de una combinación.
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

- Con las dos ventanas Añadir abiertas, solo cambia la última.

## 13. Decisiones tomadas a propósito

Atajo inválido al abrir: vuelve al de serie sin avisar. La ventana no se cierra con una combinación
inválida. No se puede dejar sin atajo. El atajo responde en cualquier ventana de Anki. Vía propia de
Windows sin parpadeo. Un fallo avisa una vez por sesión. Botones con textos de Qt.

## 14. Qué no hace

No se conecta a internet, no lee ni cambia la colección, no mantiene encima otras ventanas de Anki, no
recuerda el estado al reabrir Anki, no muestra el estado de forma permanente.
