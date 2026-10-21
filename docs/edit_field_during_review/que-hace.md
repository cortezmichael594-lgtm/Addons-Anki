# Qué hace «Edit field during review»

Versión 1.0.0 · 2026-10-21

Le deja corregir el texto de una nota directamente sobre la tarjeta, mientras repasa o en la vista
previa de Explorar, sin abrir la ventana de edición. Se mantiene pulsada la tecla Ctrl y se hace clic
sobre el texto de un campo: aparece un recuadro azul, se escribe, e Intro guarda (Escape descarta).
Solo cambia el campo que usted edita, y cada cambio se puede deshacer desde Editar > Deshacer. Lo
único que guarda por su cuenta es una opción.

## 1. Dónde aparece

- En la pantalla de repaso, en las dos caras de la tarjeta (pregunta y respuesta), también en los
  mazos filtrados.
- En la vista previa de Explorar (el botón «Vista previa»), en las dos caras.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No aparece en la lista de mazos, en la pantalla de un mazo, en la ventana «Tarjetas…» de las
  plantillas, en las ventanas de añadir o editar notas ni en las estadísticas.
- No añade menús, botones ni atajos de teclado de Anki, y no marca de ninguna forma qué campos se
  pueden editar: la tarjeta se ve exactamente igual hasta que usted empieza a editar.

## 2. Cómo se edita un campo

1. Mantenga pulsada Ctrl (⌘ en Mac) y haga clic sobre el texto del campo. Si desactiva la opción del
   apartado 5, basta un clic normal.
2. El campo queda rodeado por un recuadro azul de 2 píxeles, con las esquinas algo redondeadas y un
   pequeño margen interior (el texto puede moverse unos píxeles mientras edita). El cursor se coloca
   donde hizo clic o, si no es posible, al final del campo.
3. Lo que verá dentro del recuadro:
   - En un campo normal, el mismo texto que se ve en la tarjeta, con su formato (negrita, cursiva,
     imágenes…). Nunca ve el código interno de la nota.
   - En un campo de huecos (tarjetas de rellenar huecos), el texto tal como está guardado, con las
     marcas de hueco a la vista, por ejemplo «La {{c1::capital}} de Francia», para que pueda cambiar
     tanto el texto como los huecos. Al guardar, ese trozo vuelve a verse con sus huecos.
   - En un campo cuyo aspecto en la tarjeta ya no coincide con lo guardado (por ejemplo, una fórmula
     que Anki ha dibujado), el contenido tal como está guardado: en ese ejemplo, el código de la
     fórmula.
   - Las etiquetas, solo si la plantilla de la tarjeta las muestra y la nota tiene alguna: se ven
     como texto separado por espacios, y cada palabra es una etiqueta.
4. Teclas mientras edita:
   - Intro guarda y termina.
   - Mayúsculas+Intro añade un salto de línea.
   - Escape descarta lo escrito y deja el campo exactamente como estaba.
   - Las demás teclas escriben en el campo en lugar de hacer sus funciones de repaso.
5. También se guarda y se termina al hacer clic fuera del campo, al pulsar uno de los botones de
   abajo (por ejemplo «Mostrar respuesta») o al pasar a otra cara o a otra tarjeta con la edición
   abierta. Ctrl+clic en otro campo guarda el primero y empieza a editar el segundo.
6. Después de guardar:
   - En el repaso, la tarjeta no se vuelve a dibujar entera: se queda lo que usted escribió (en los
     campos de huecos se redibuja solo ese trozo). Si el mismo campo aparece dos veces en esa cara y
     el complemento reconoce las dos, cambian a la vez. Al pasar a la respuesta, ya se ve el cambio.
   - En la vista previa, Anki vuelve a dibujar la tarjeta entera, y Explorar actualiza su lista (y
     la nota de abajo, con el editor de siempre; véase el apartado 9).
   - No sale ningún aviso si todo va bien.

## 3. Qué se puede editar y qué no

- Se puede editar cualquier campo con contenido cuyo texto se vea en la tarjeta tal como está
  guardado, en cualquier tipo de nota: no depende de los nombres de los campos, porque el complemento
  reconoce cada campo comparando lo que se ve con lo guardado.
- Si el complemento no logra localizar un campo en la tarjeta, ese campo no se puede editar: Ctrl+clic
  sobre él no hace nada. Pasa con:
  - los campos vacíos (no hay nada sobre lo que pulsar, así que no se pueden rellenar desde aquí);
  - los campos que la plantilla transforma antes de mostrarlos de forma que cambia lo que se ve (por
    ejemplo, con furigana) o que el código propio de la plantilla modifica después;
  - los campos con sonidos, porque en la tarjeta se ven como un botón de reproducir;
  - los campos con imágenes cuyo nombre de archivo lleva espacios u otros caracteres especiales;
  - las marcas de hueco {{c1::…}} escritas en un tipo de nota que no es de huecos.
- Pulsar sobre un enlace, un botón de reproducir sonido o la casilla para escribir la respuesta nunca
  empieza a editar.
- Las etiquetas solo se pueden editar si la plantilla las muestra.
- Hay tres casos en que el reconocimiento falla de forma visible (descritos en «Pendientes» de sus
  errores): dos campos con el mismo contenido, fórmulas y algunas plantillas de huecos.

## 4. Qué cambia de su colección y cómo deshacerlo

- Solo cambia el campo que edita (o las etiquetas) de esa nota. Como los campos son de la nota, el
  cambio se ve en todas las tarjetas de esa nota.
- Se guarda sin congelar Anki.
- Antes de guardar quita los espacios del principio y del final. Si al terminar no ha cambiado nada,
  no guarda nada ni deja ningún paso de deshacer.
- Lo que se guarda es el contenido tal como queda en el recuadro, con su formato. Los saltos de línea
  y algunos espacios pueden quedar escritos internamente de otra forma que antes, sin que se note al
  verlos.
- No limpia lo que se pega: si pega texto copiado de una página web, puede entrar con su tipo de
  letra, tamaño o color, que quedan guardados en el campo.
- En las etiquetas, cada palabra separada por espacios es una etiqueta; si borra todas, la nota se
  queda sin etiquetas.
- Cada cambio guardado es un paso de Editar > Deshacer (Ctrl+Z). En el repaso, al deshacer, la
  tarjeta se vuelve a dibujar con el texto anterior.
- No hace copia de seguridad antes de guardar.
- Los cambios viajan con la sincronización como cualquier otra edición.

## 5. Ventana de opciones

- Título: «Edit field during review» (el nombre del complemento, en inglés).
- Casilla «Exigir Ctrl + clic para empezar a editar (⌘ en Mac)»: marcada por defecto. Desmarcada,
  basta un clic normal sobre un campo para empezar a editar; entonces es más fácil entrar a editar
  sin querer al seleccionar texto, y por eso viene marcada.
- Botones Aceptar y Cancelar, en el idioma de Anki. Aceptar guarda sin mostrar ningún aviso;
  Cancelar cierra sin guardar.
- El cambio se aplica desde la siguiente cara o tarjeta que se muestre, no en la que ya está en
  pantalla.
- La ventana no recuerda su tamaño ni su posición.

## 6. Mensajes

Todos son avisos breves que desaparecen solos a los 3 segundos:

- «No se pudo guardar el cambio:» seguido del motivo técnico (normalmente en inglés). El cambio no
  se guarda.
- «El campo «Nombre» ya no existe. El cambio no se ha guardado.», con el nombre del campo, si se
  borró o se renombró mientras la tarjeta estaba en pantalla.
- «La nota ya no existe. El cambio no se ha guardado.», si la nota se borró mientras la tarjeta
  estaba en pantalla.
- «El editor envió una orden que no se entiende. El cambio no se ha guardado.»
- «El cambio se ha guardado, pero no se pudo redibujar la tarjeta.»

Si la ventana de opciones no se puede abrir, sale una ventana de aviso titulada «Edit field during
review» con el motivo técnico.

## 7. Qué guarda y dónde

- Su única opción, en la configuración de complementos de Anki de este ordenador: vale para todos
  los perfiles y no viaja con la sincronización.
- Si la opción falta (por ejemplo, porque la configuración viene de una versión anterior), usa el
  valor por defecto: casilla marcada.
- No guarda historial propio de cambios ni crea archivos. El detalle técnico de los fallos queda en
  el registro del complemento, un archivo de texto en la carpeta de registros de Anki.

## 8. Idiomas

Sus avisos y la casilla de opciones están en 49 idiomas, entre ellos español, catalán, gallego y
euskera; si el idioma de Anki no está, salen en inglés. El portugués es el de Brasil y el chino, el
simplificado, para todas sus variantes. Los botones Aceptar y Cancelar los pone Anki en su idioma. El
título de la ventana de opciones sale siempre en inglés.

## 9. Convivencia con otras ventanas de Anki

- No usa la ventana de edición de Anki, así que funciona igual con el editor de siempre y con el
  editor nuevo, que Anki tiene aún en pruebas.
- Si tiene abierta a la vez la ventana «Editar» con la misma nota, o Explorar con esa nota
  seleccionada, el editor de siempre se actualiza solo con el cambio. El editor nuevo de Anki no se
  actualiza solo: ciérrelo y vuelva a abrirlo para ver el cambio.
- Las plantillas que usan la marca «edit:» de otros complementos parecidos (por ejemplo, {{edit:Frente}})
  muestran el campo con normalidad, y se edita igual que los demás.

## 10. Si algo falla

- Nunca abre la ventana de error de Anki por un fallo suyo durante el repaso: muestra uno de los
  avisos del apartado 6 y deja el detalle en su registro. Anki sigue funcionando.
- Si algo falla al preparar una tarjeta, la tarjeta se muestra con normalidad y ese campo, o la
  tarjeta entera, simplemente no se puede editar.

## 11. Qué no hace

- No se conecta a internet.
- No añade menús ni botones, y no cambia plantillas, tipos de nota ni otras notas.
- No rellena campos vacíos ni crea campos nuevos.
- No funciona en la ventana «Tarjetas…», en la lista de mazos ni en las estadísticas.
- No limpia el formato de lo que se pega.
- No hace copia de seguridad: cada cambio es de una sola nota y se puede deshacer.
- No avisa de qué campos se pueden editar.
