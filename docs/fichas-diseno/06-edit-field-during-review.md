# Ficha de diseño: Edit field during review

Versión 1.1.0 (9 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Permite corregir el texto de una nota directamente sobre la tarjeta, durante el repaso o en la vista
previa de Explorar: Ctrl+clic sobre un campo, aparece un recuadro azul, se escribe e Intro guarda
(Escape descarta).

## 2. Para quién y para qué

Para arreglar una errata o completar una respuesta en el momento en que se ve, sin abrir la ventana de
edición ni perder el hilo del repaso. Cada cambio se puede deshacer con Editar > Deshacer.

## 3. Dónde funciona

- Repaso (pregunta y respuesta), también en mazos filtrados.
- Vista previa de Explorar (ambas caras).
- Herramientas > Complementos > Edit field during review > Configuración: ventana de opciones.
- No funciona en la lista de mazos, la pantalla de un mazo, la ventana «Tarjetas…», Añadir, Editar ni
  estadísticas.
- No añade menús, botones ni atajos, y no marca qué campos se pueden editar: la tarjeta se ve igual
  hasta que se empieza a editar.

## 4. Cómo se edita

1. Ctrl (⌘ en Mac) + clic sobre el texto del campo (o clic simple si se desactiva la opción).
2. El campo queda rodeado por un recuadro: contorno de 2 px, esquinas de 3 px y margen interior de 2 px
   arriba y abajo y 4 px a los lados (el texto puede moverse unos píxeles). Si el campo ocupa varias
   líneas, el recuadro es uno solo, no uno por línea. El cursor se coloca donde se hizo clic o al final.
3. Contenido dentro del recuadro:
   - Campo normal: el mismo texto con su formato (negrita, cursiva, imágenes). Nunca el código interno.
   - Campo de huecos: el texto guardado con las marcas visibles («La {{c1::capital}} de Francia»). Al
     guardar, vuelve a verse con sus huecos.
   - Campo cuyo aspecto ya no coincide con lo guardado (una fórmula dibujada): el contenido guardado.
   - Etiquetas, si la plantilla las muestra: texto separado por espacios.
4. Teclas: Intro guarda y termina; Mayús+Intro, salto de línea; Escape descarta; las demás escriben
   (no hacen sus funciones de repaso).
5. También guarda al hacer clic fuera, al pulsar un botón de abajo o al cambiar de cara o de tarjeta.
   Ctrl+clic en otro campo guarda el primero y abre el segundo.
6. Después de guardar: en el repaso, la tarjeta no se redibuja entera (se queda lo escrito; en huecos se
   redibuja solo ese trozo). Si el mismo campo sale dos veces en esa cara, cambian a la vez. En la vista
   previa, Anki redibuja la tarjeta y Explorar se actualiza. Sin aviso si todo va bien.

## 5. Colores

| Uso | Día | Noche |
|---|---|---|
| Contorno del recuadro de edición | BORDER_FOCUS, #3B6FE0 con Nocturne | BORDER_FOCUS, #6390FF con Nocturne |

Desde la 1.1.0 el contorno usa el color de foco de la paleta, así que con Atelier sigue al color de
acción de cada paleta (hasta la 1.0.0 eran dos azules fijos, #1971C2 y #4A9EFF). Se marca como
importante para que ninguna plantilla de tarjeta lo oculte. El resto lo dibuja la plantilla de la
tarjeta.

## 6. Qué se puede editar y qué no

- Se puede: cualquier campo con contenido cuyo texto se vea en la tarjeta tal como está guardado, en
  cualquier tipo de nota (se reconoce comparando lo que se ve con lo guardado).
- No se puede (Ctrl+clic no hace nada): campos vacíos; campos transformados por la plantilla (furigana,
  código propio); campos con sonidos; imágenes con espacios o caracteres especiales en el nombre;
  marcas de hueco en notas que no son de huecos.
- Pulsar un enlace, un botón de sonido o la casilla de escribir la respuesta nunca abre la edición.

## 7. Qué cambia en la colección

- Solo el campo editado (o las etiquetas) de esa nota; se ve en todas sus tarjetas.
- Se guarda sin congelar Anki. Quita espacios al principio y al final. Si nada cambió, no guarda ni deja
  paso de deshacer.
- No limpia lo pegado (puede entrar con letra, tamaño o color de una web).
- Cada cambio, un paso de Editar > Deshacer (Ctrl+Z); en el repaso, al deshacer, la tarjeta se
  redibuja. No hace copia de seguridad. Viaja con la sincronización.

## 8. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «Edit field during review» (en inglés en todos los idiomas). Un recuadro con «Restaurar los
  valores predeterminados» (y «Deshacer») y la casilla «Exigir Ctrl + clic para empezar a editar (⌘
  en Mac)», marcada de serie. Es el panel más pequeño: alto justo para su contenido.

## 9. Mensajes (avisos breves de Anki, 3 s)

- «No se pudo guardar el cambio:» + motivo técnico (normalmente en inglés).
- «El campo «Nombre» ya no existe. El cambio no se ha guardado.»
- «La nota ya no existe. El cambio no se ha guardado.»
- «El editor envió una orden que no se entiende. El cambio no se ha guardado.»
- «El cambio se ha guardado, pero no se pudo redibujar la tarjeta.»
- Si la ventana de opciones no se abre: ventana de aviso «Edit field during review» con el motivo.

## 10. Accesibilidad

- Edición con teclado una vez abierta (Intro, Mayús+Intro, Escape); para abrirla hace falta el ratón
  (Ctrl+clic): no hay forma de entrar a editar solo con el teclado.
- Recuadro de 2 px bien visible, pero sin indicación previa de qué es editable (descubrimiento bajo).
- Ctrl exigido de serie para no entrar a editar al seleccionar texto.
- Los avisos de error desaparecen a los 3 s y algunos llevan texto técnico en inglés.
- Contraste del recuadro no medido contra los fondos de las plantillas.

## 11. Idiomas

49 idiomas (con catalán, gallego y euskera); si falta, inglés. Portugués de Brasil y chino simplificado
para todas sus variantes. Aceptar y Cancelar, de Anki. Título siempre en inglés.

## 12. Convivencia

No usa la ventana de edición de Anki: funciona con el editor de siempre y con el nuevo. Si Editar o
Explorar tienen la misma nota abierta, el editor de siempre se actualiza solo; el nuevo, no (hay que
reabrirlo). Las plantillas con la marca «edit:» de otros complementos ({{edit:Frente}}) se ven normal y
se editan igual.

## 13. Qué guarda

Su única opción, en la configuración de complementos del ordenador (todos los perfiles, no se
sincroniza). Sin historial propio ni archivos.

## 14. Fallos conocidos pendientes

- Dos campos con el mismo contenido en bloques distintos: edita siempre el primero.
- Tras editar un campo con fórmula, se ve el código hasta cambiar de cara.
- En plantillas de huecos con otro campo en el mismo bloque, ese otro campo no se puede editar y
  desaparece mientras se edita el de huecos.

## 15. Decisiones tomadas a propósito

Ctrl+clic exigido. Se guarda al salir del campo (solo Escape descarta). No se redibuja la tarjeta entera.
Sin cambio, sin guardado. Título en inglés.

## 16. Qué no hace

No se conecta a internet, no añade menús ni botones, no cambia plantillas ni otras notas, no rellena
campos vacíos, no limpia lo pegado, no hace copia de seguridad, no avisa de qué campos son editables.
