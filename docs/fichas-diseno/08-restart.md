# Ficha de diseño: Restart

Versión 2.1.0 (9 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Reinicia Anki con un atajo (Ctrl+R de serie; ⌘R en Mac) mediante un cierre normal (guarda,
sincroniza si toca, hace la copia de seguridad) y vuelve a abrir Anki con el mismo perfil.

## 2. Para quién y para qué

Para aplicar cambios de complementos o recuperar Anki sin cerrar y abrir a mano. No cambia la colección.

## 3. Aspecto propio

No pinta nada: sin colores, iconos ni letra propios. Su interfaz son avisos breves de Anki, ventanas de
aviso nativas y una ventana de opciones con el modelo del panel de GritMap (colores de la paleta).

## 4. Dónde actúa

- El atajo, en la ventana principal (lista de mazos, pantalla de un mazo y repaso).
- No responde si hay otra ventana delante (Explorar, Añadir, Preferencias, opciones, preguntas de Anki)
  ni en la ventana de elegir perfil.
- Herramientas > Complementos > Restart > Configuración: ventana de opciones.
- No añade menús, botones ni nada visible.

## 5. El reinicio, paso a paso

1. Si Anki está en una tarea con barra de progreso: no reinicia y avisa «Anki está ocupado ahora mismo.
   Espera a que termine e inténtalo de nuevo.».
2. Si no identifica con seguridad el programa de Anki: no cierra nada; ventana «Restart»: «No se
   encontró el programa de Anki, así que no se puede reiniciar. Anki sigue abierto y no se ha perdido
   nada.».
3. Si todo va bien: aviso breve «Reiniciando Anki…» y cierre normal (cierra ventanas; si hay algo
   escrito en Añadir, Anki pregunta; sincroniza si está activado; copia de seguridad si toca).
4. Con la colección cerrada, abre Anki de nuevo con el mismo perfil y carpeta de datos, sin pasar por
   la elección de perfil. Vuelve a la lista de mazos; las ventanas no se reabren.

Si el cierre se detiene (por ejemplo, la persona sigue editando en Añadir), Anki queda abierto y el
reinicio se anula en unos segundos (como mucho 5).

## 6. Límites

- Repaso en curso: lo respondido queda guardado; la tarjeta sin responder volverá. Tras reiniciar, lista
  de mazos.
- Pulsaciones repetidas o tecla mantenida: un solo reinicio.
- Cierre de más de 5 minutos: Anki se cierra sin reabrirse.
- Anki se reabre en modo normal aunque se hubiera abierto en modo seguro.
- Si otro complemento usa la misma combinación, ninguno responde (se comprueba al abrir y al guardar).

## 7. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «Restart». Un recuadro con «Restaurar los valores predeterminados» (y «Deshacer»), la
  casilla «Activar atajo para reiniciar Anki» y, colgando de ella, el campo grabador «Atajo» (Ctrl+R),
  igual que el de Always on Top, atenuado si la casilla está desmarcada. Vacío al aceptar, conserva
  el atajo guardado.
- Si la combinación no sirve, el aviso sale en rojo encima del campo y la ventana no se cierra.

## 8. Accesibilidad

- Funciona solo con el teclado; la ventana de opciones sigue el modelo del panel de GritMap, accesible con Tab.
- No pide confirmación antes de reiniciar: un Ctrl+R accidental reinicia (sin pérdida de datos, porque
  es un cierre normal). Ctrl+R es un atajo frecuente en otros programas (recargar).
- Los avisos breves desaparecen solos y pueden no anunciarse al lector de pantalla.
- Trato de tú en español.

## 9. Idiomas

55 idiomas de Anki y seis más; si falta, inglés. Usa el idioma de Anki en cada momento. La combinación
se escribe con los nombres o símbolos de cada sistema. Botones estándar en el idioma de Anki si Qt lo
trae; si no, en inglés.

## 10. Qué guarda

Sus dos opciones, en la configuración de complementos del ordenador (todos los perfiles, no se
sincroniza). Un registro técnico de cada reinicio. Nada en la colección.

## 11. Si algo falla

Nunca la ventana de error de Anki: ventana «Restart» con «Ocurrió un error inesperado:» y el detalle
técnico. Si el cierre no empieza, se anula. Si no logra reabrir, Anki queda cerrado sin pérdida y hay
que abrirlo a mano.

## 12. Fallo conocido pendiente

Si se cancela el cierre y en los pocos segundos siguientes se cierra Anki a mano, Anki se vuelve a abrir
solo; y un segundo atajo en ese margen no hace nada.

## 13. Decisiones tomadas a propósito

Espera a que el Anki anterior cierre la colección (nunca dos Anki con la colección abierta). Cierre de
más de 5 minutos: no se reabre. Sin programa identificado, no reinicia. Ctrl+W nunca se admite. Sin
teclas sueltas. Campo vacío conserva el atajo. Ventana propia sin colores propios. No reinicia durante
una tarea con progreso.

## 14. Qué no hace

No se conecta a internet, no cambia la colección, no pide confirmación, no tiene atajo para solo cerrar
(para eso, Ctrl+Q de Anki), no añade menús ni botones, no reabre ventanas ni la pantalla anterior.
