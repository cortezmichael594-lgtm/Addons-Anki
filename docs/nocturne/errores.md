# Errores de «Atelier» (antes «Nocturne»)

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-11-04 · versión 3.7.2 · Qué pasa: de noche, el informe midió el texto de los campos del editor
  en blanco puro (14,8 a 1), por encima del techo de 13,5 de las paletas, que piden #D6DAE1 en
  Nocturne. No se ha podido averiguar desde aquí de dónde sale: Atelier no pinta el interior de los
  campos, y puede venir del estilo de las tarjetas de su tipo de nota (el de serie, «Básico», pide
  texto negro). Propuesta: con Atelier desactivado en Herramientas > «Complementos», abrir Añadir de
  noche y ver si el texto sigue en blanco; si sigue, no es de Atelier y no se toca.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-24 · versión anterior a 2026.07.28 · Qué pasaba: de noche, el degradado del fondo
  se veía repetido en varias manchas en lugar de una sola en la esquina. Por qué: al simplificar el
  estilo se quitó el anclaje del degradado a la ventana. Regla: el degradado del fondo va siempre
  anclado a la ventana, y no se quita nada de lo que ya funciona sin comprobar a la vista que el
  aspecto no cambia.
- FIX-002 · 2026-10-21 · versión 2.1.0 · Qué pasaba: de día, las cifras «Aprendiendo» y «Para repasar»
  de la lista de mazos, las «Nuevas» sobre fondos hundidos y el rojo de aviso se leían peor de lo
  recomendado (entre 3,0 y 4,4). Por qué: esos colores se eligieron por cómo quedaban como iconos y no
  se midieron como texto. Regla: todo color que se use como texto llega a 4,5 sobre cualquier fondo, y
  se corrige oscureciéndolo sin cambiar su tono. Prueba: «TextContrastTest».
- FIX-003 · 2026-10-21 · versión 2.1.0 · Qué pasaba: una casilla sin marcar casi no se distinguía del
  fondo. Por qué: Anki dibuja su borde con el mismo color suave que otros detalles. Regla: las casillas
  tienen su propio borde visible y los demás bordes siguen suaves. Prueba: «CheckboxBorderTest».
- FIX-004 · 2026-10-21 · versión 2.1.0 · Qué pasaba: de noche, en Explorar, el texto de las filas con
  bandera naranja, verde, azul, rosa, turquesa o morada se leía mal. Por qué: Anki pinta esas filas con
  el color de la bandera oscurecido, y los tonos nocturnos seguían siendo demasiado claros. Regla: de
  noche, cada bandera deja su fila legible y sigue viéndose como icono; se oscurece sin cambiar el tono.
  Prueba: «ExplorerRowsTest».
- FIX-005 · 2026-10-21 · versión 2.1.0 · Qué pasaba: con el ratón encima del botón azul principal, su
  texto blanco perdía legibilidad. Por qué: el efecto de pasar el ratón aclaraba el azul. Regla: el
  azul de acción da 4,5 con texto blanco en todos sus estados. Prueba: «PrimaryButtonTest».
- FIX-006 · 2026-10-21 · versión 3.2.0 · Qué pasaba: en la pantalla de estudio de un mazo, la tabla con
  Nuevas, Aprendiendo y A repasar se teñía de color (azul en Nocturne) al pasar el ratón por encima,
  como si fuera una fila de la lista de mazos. Por qué: el resaltado de la 3.1.0 se aplicaba a
  cualquier fila de tabla con el ratón encima, y esa pantalla también usa una tabla; la separación de
  las filas tenía el mismo defecto. Regla: lo que se añade para una pantalla concreta se limita a sus
  propios elementos (aquí, las filas de mazo), nunca a etiquetas genéricas que comparten otras
  pantallas. Prueba: «test_row_highlight_only_in_deck_list», que falló antes del arreglo y pasa
  después.
- FIX-007 · 2026-10-21 · versión 3.3.0 · Qué pasaba: al pulsar «Configuración» en la ventana de
  complementos, la ventana de paletas no aparecía delante: la de complementos no dejaba elegir nada y
  solo al cerrarla con la X se veía la de paletas. Por qué: la ventana de paletas dependía de la
  ventana principal de Anki y se abría sin bloquear, así que Windows la dejaba detrás de la de
  complementos, que era la activa. Regla: toda ventana que se abre desde otra depende de la que la
  pide (la activa, no la principal) y se abre delante de ella, bloqueándola mientras esté abierta,
  como hace Anki con la suya. Prueba: «OwnerWindowTest», que falló antes del arreglo y pasa después.

- FIX-008 · 2026-10-28 · versión 3.7.1 · Qué pasaba: en la ventana sencilla de configuración, al pulsar
  «Abrir el registro» no se abría nada y cada pulsación anotaba otro fallo en el registro (por eso la
  línea de aviso no desaparecía). Por qué: el botón avisa con un dato (si está marcado) y la función no
  lo aceptaba. Regla: toda función conectada a la pulsación de un botón acepta ese dato. Prueba: la de
  la línea de fallos pulsa el botón; falló antes del arreglo y pasa después.
- FIX-009 · 2026-10-28 · versión 3.7.1 · Qué pasaba: el panel de configuración de la 3.7.0 no se
  mostraba nunca: a los 3 segundos se abría siempre la ventana sencilla de emergencia, y el registro
  decía «el panel no se dibujó en 3000 ms». Por qué: el panel está oculto hasta que avisa de que está
  listo, y esperaba a pintarse para avisar; una página oculta no se pinta, así que cada uno esperaba
  al otro. Además, oculto no sabía su ancho y habría pedido 1.878 px de alto. Regla: una página que se
  enseña cuando avisa de que está lista avisa sin esperar a pintarse, y mide su alto con el ancho de
  la ventana. Comprobado dibujándola oculta: antes no avisaba; ahora avisa con 646 px.
- FIX-010 · 2026-10-28 · versión 3.7.1 · Qué pasaba: al pasar el ratón por un botón de respuesta (por
  ejemplo «Fácil») salía una raya fina de su color arriba del botón, además de la de abajo. Por qué: el
  navegador repetía la raya como un mosaico y asomaba por el borde semitransparente que Anki pone con
  el ratón encima. Regla: toda raya o dibujo hecho como fondo lleva la orden de no repetirse. Prueba:
  «test_toolbar_and_answer_buttons».

- FIX-011 · 2026-10-28 · versión 3.7.2 · Qué pasaba: con la 3.7.1 el panel seguía sin mostrarse y
  salía la ventana sencilla («el panel no se dibujó en 3000 ms»): FIX-009 arregló una causa, pero no
  la principal. Por qué: Anki crea la función con la que la página le habla cuando la página ha
  terminado de cargar; el panel avisaba antes, la función aún no existía y el aviso se perdía. Las
  pruebas no lo veían porque la creaban desde el principio. Regla: toda página espera a que exista esa
  función antes de hablar con Anki (como GritMap), y las pruebas la crean tarde, como Anki. Además,
  si a los 3 segundos la página ha cargado pero no ha avisado (la primera vez en una sesión, el
  navegador de Anki puede tardar en arrancar), se enseña igualmente. Prueba:
  «test_page_waits_for_pycmd»; y, dibujándola como la carga Anki, antes daba «pycmd is not defined» y
  ahora avisa con 646 px.
- FIX-012 · 2026-11-04 · versión 3.8.0 · Qué pasaba: en Explorar, el texto de la fila seleccionada
  se leía peor de lo prometido: 4,46 a 1 en Nocturne de noche, y entre 3,1 y 4,1 en Papel, Bosque y
  Atardecer de noche (lo detectó el informe del 2026-11-04 en Nocturne; las demás, al medirlas). Por
  qué: Anki marca la selección con un color transparente y Explorar lo pinta tres veces encima de la
  fila, así que el color que se veía no era el que se había medido. Regla: el fondo de lo
  seleccionado en las tablas es opaco y se mide con el texto encima tal como se ve; ahora llega a 5 a
  1 o más en las cinco paletas. Prueba: «TableSelectionTest».
- FIX-013 · 2026-11-04 · versión 3.8.0 · Qué pasaba: en Preferencias, «Restablecer tamaños de las
  ventanas» salía relleno de azul y a todo el ancho, como la acción principal, y «Cerrar» en gris.
  Por qué: el relleno seguía a cualquier botón que respondiera a Intro, y Qt da ese papel al botón
  del cuerpo que tiene el foco cuando la ventana no marca uno en la fila de abajo. Regla: el relleno
  de acción es solo para el botón principal de la fila de botones del pie; un botón del cuerpo nunca
  se rellena. Prueba: «PrimaryButtonRowTest», que dibuja la ventana; falló antes del arreglo y pasa
  después.
## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- 2026.07.28 · En la paleta Nocturne, «Aprendiendo» iba en naranja, como en el aspecto original. Desde
  la 3.5.0 va en rojo, como en Papel y en Bosque: el cliente lo pidió el 2026-10-26 (informe de
  mejoras, apartado 4.2) sabiendo que se aparta del original, porque el naranja también es «Difícil».
- 2026.07.28 · Los bordes de listas, tablas y separadores son muy suaves. Es parte del aspecto
  original; la versión 2.0.0 los reforzó y el cliente la descartó por perder atractivo (2026-10-21).
  Desde la 3.8.0, los campos de texto, los campos numéricos y las listas desplegables llevan un borde
  fino visible, el mismo de las casillas: el cliente lo aprobó el 2026-11-04 (informe, apartado 2.2)
  sabiendo que en octubre lo había descartado.
- 2.1.0 · De noche, las banderas son algo menos vivas que en la versión original. Es el precio de que el
  texto de las filas de Explorar se lea bien (FIX-004); el cliente aprobó el plan el 2026-10-21.
- 2.1.0 · Con el ratón encima o con el foco, el borde de las casillas es azul y no gris oscuro, para que
  se note el cambio. Decisión del taller dentro del plan aprobado.
- 3.0.0 · El fondo, el azul de acción y el tono de los colores con significado no cambian respecto a la
  versión original; las pruebas lo vigilan. Es la identidad que el cliente quiere conservar.
- 3.0.0 · No se cambia el tamaño de la letra: manda el que el cliente tenga elegido en Anki. Decisión
  del taller. (En 3.0.0 tampoco se tocaban las esquinas ni el botón por defecto; desde 3.1.0 sí, porque
  el cliente lo pidió.)
- 3.1.0 · En Nocturne, la bandera rosa pasa de un rosa frambuesa a un rosa de verdad (tono 310°), porque
  se confundía con la roja. Es el único cambio de tono respecto al aspecto original; lo vigilan las
  pruebas.
- 3.1.0 · El relleno del botón principal de las ventanas sigue al botón que respondería a Intro: al
  moverse con Tab entre los botones de la fila de abajo, el relleno se mueve con el foco. Así funciona
  Qt y así se avisa de lo que hará Intro. Decisión del taller. Desde la 3.8.0, solo en esa fila: un
  botón del cuerpo de la ventana que responda a Intro conserva su fondo y lleva el borde azul fino
  de Anki (FIX-013).
- 3.1.0 · Solo se elige la paleta; no hay ajustes sueltos de esquinas, letra o separación. Lo decidió el
  cliente (2026-10-21).
- 3.1.0 · Los botones de las ventanas tienen como mucho 9px de radio: con más, Qt los dibuja cuadrados
  (comprobado al construir Bosque). Decisión del taller.
- 3.2.0 · Grafito y Alto contraste ya no existen: el cliente no las quiso (2026-10-21). Una configuración
  que aún las nombre vuelve a Nocturne sin avisar.
- 3.2.0 · La ventana de paletas solo se abre desde el botón «Configuración» de la ventana de
  complementos; no hay entrada en el menú Herramientas. Lo pidió el cliente (2026-10-21).
- 3.2.0 · Papel de noche usa fondos azul petróleo («Tinta») con texto crema, en vez de marrón: no es la
  misma familia que Papel de día. Lo eligió el cliente entre tres muestras (2026-10-21).
- 3.2.0 · En Bosque y en Papel de noche, azul, rojo y verde giran su tono hacia azul petróleo, rojo
  ladrillo y verde musgo. Nocturne y Papel de día no cambian. Aprobado por el cliente (2026-10-21).
- 3.2.0 · En la pantalla de un mazo, «Comenzar a estudiar» aparece con su contorno de foco desde el
  principio: Anki le da el foco al abrir la pantalla, y el contorno avisa de que Intro empieza el
  estudio. Decisión del taller.
- 3.3.0 · La ventana de configuración bloquea la de complementos mientras está abierta, como cualquier
  diálogo de Anki: así no puede quedar escondida (FIX-007). Decisión del taller.
- 3.5.0 · Vista previa: elegir una paleta la aplica a todo Anki en el acto (a los 200 milisegundos de
  dejar quieta la elección) y «Cancelar» la deshace. Antes (3.3.0) solo se aplicaba con «Aceptar».
  Pedido por el cliente el 2026-10-26 (informe, apartado 3.2).
- 3.3.0 · El aviso «Paleta «…» aplicada.» salía de día en amarillo con letra negra (el aviso breve de
  Anki, con sus colores fijos). Desde la 3.5.0 no sale: la vista previa ya enseña el cambio. El aviso
  de bienvenida sí usa ese aviso de Anki, con su amarillo, una sola vez.
- 3.3.0 · La barra de título solo cambia en Windows 11: Windows 10 no permite elegir su color, y en
  macOS y Linux la dibuja el sistema. Decisión del taller.
- 3.3.0 · De noche, el texto desactivado es algo más claro que antes en las tres paletas, también en
  Nocturne, con el mismo tono: no llegaba al mínimo de APCA para texto. Decisión del taller, explicada
  al cliente en la entrega.
- 3.4.0 · De día, la barra de título solo es un poco más clara que la ventana: el fondo de las tres
  paletas ya es casi blanco y la barra no puede llegar al blanco puro, que las reglas de la paleta
  evitan. De noche la diferencia se nota más. Pedido por el cliente (2026-10-21).
- 3.4.0 · De noche, el título de la barra queda algo por encima de 13,5 de contraste (hasta 14,2), el
  límite de comodidad del texto de lectura: es una sola línea y se lee de un vistazo. Decisión del
  taller.
- 3.5.0 · Aviso de bienvenida una sola vez, que obliga a guardar un dato más que la paleta (que ya
  salió). Pedido por el cliente el 2026-10-26 (informe, apartado 2.1). Quien ya tenía Nocturne lo verá
  una vez al instalar la 3.5.0: no hay forma fiable de distinguir una instalación de una actualización.
- 3.5.0 · Con el alto contraste del sistema, Nocturne no pinta nada. Cubre a quien lo necesita sin
  recuperar la paleta Alto contraste; quien la usaba sin tener el contraste del sistema activado sigue
  sin ella. Pedido por el cliente el 2026-10-26 (informe, apartado 6.1). Se comprueba al abrir Anki.
- 3.5.0 · No se añaden sombras de día ni se quitan de noche (informe, apartado 4.4): en las páginas de
  Anki, el color «sombra» también hace de borde inferior de los botones, y cambiarlo los alteraría.
  Decisión del taller.
- 3.5.0 · La simulación de daltonismo solo exige separar la bandera roja y la verde: las cifras de la
  lista de mazos se distinguen por su columna y las rayas de los botones de respuesta por su texto. Las
  gráficas de las estadísticas usan colores propios de Anki, que Nocturne no cambia. Decisión del
  taller.
- 3.5.0 · No se aplica lo del informe sobre el día de gracia, la meta diaria y la página de
  felicitación como cierre del día: el cliente lo descartó para Nocturne el 2026-10-26.
- 3.6.0 · El complemento se llama «Atelier» y su paleta de serie, «Nocturne». La carpeta interna y el
  paquete siguen llamándose «nocturne»: si cambiaran, Anki lo trataría como un complemento nuevo,
  instalaría dos y perdería la paleta guardada. Elegido por el cliente el 2026-10-28.
- 3.6.0 · La ventana usa una lista desplegable con muestras, como GritMap, en lugar de los botones de
  opción de la 3.5.0 (que el informe de mejoras recomendaba para comparar las descripciones). Pedido por
  el cliente el 2026-10-28: los dos complementos, con el mismo diseño. La descripción de la paleta
  elegida sigue debajo de la lista.
- 3.6.0 · El cobre de Atardecer tiene un matiz parecido al naranja de «Difícil» y de la bandera
  naranja; se distingue por claridad (mucho más oscuro) y lo vigila una prueba. Decisión del taller,
  dentro de la paleta que eligió el cliente.
- 3.7.0 · La ventana de configuración es un panel a medida (una página), no controles de Anki como
  pide la guía del taller. Pedido por el cliente el 2026-10-28 (informe, apartados 2 a 7), para que
  sea igual que el de GritMap. Si el panel falla o no se dibuja en 3 segundos, se abre la ventana
  sencilla de controles de Anki.
- 3.7.0 · El panel no tiene «Restaurar los valores predeterminados»: Nocturne dice «predeterminada»
  en su fila. La ventana sencilla de emergencia sí lo conserva. Pedido por el cliente (informe, 3.3).
- 3.7.0 · Paletas por orden alfabético (Atardecer, Bosque, Lavanda, Nocturne, Papel), como los temas de
  GritMap, en lugar de la de serie primero. Pedido por el cliente (informe, 3.4).
- 3.7.0 · Papel y Lavanda pasan de esquinas de 7 y 14 px a 6 y 12, para formar dos familias claras
  (suaves y redondeadas). El informe proponía también, para Papel, 4 y 8 px («casi rectas»); no se ha
  aplicado porque cambia a la vista una paleta que ya se usa: queda a decisión del cliente.
- 3.7.0 · Las pestañas de Anki no cambiaban (el informe proponía una raya de 2 px). Desde la 3.8.0
  sí: la activa lleva el tinte de acción, el texto normal y una raya de 2 px, pedido por el cliente
  el 2026-11-04 (informe, apartado 2.1). La letra no pasa a seminegrita, como pedía el informe: Qt
  mediría la pestaña más ancha y la barra se movería al cambiar de una a otra. Decisión del taller.
- 3.7.0 · No hay simulación de daltonismo de las series de las estadísticas: sus gráficas usan colores
  propios de Anki que Atelier no cambia, así que no hay nada que comprobar desde el complemento.
  Decisión del taller.
- 3.8.0 · En Explorar, una fila seleccionada con bandera o estado se ve del color de la selección, sin
  el tinte de su bandera debajo: el fondo de la selección es opaco para que su texto se lea (FIX-012).
  La bandera vuelve a verse al quitar la selección. Decisión del taller.
- 3.8.0 · El interruptor «Tarjetas/Notas» de Explorar se tiñe cambiando un dato interno de Anki,
  porque Anki no ofrece una forma de elegir su color (APR-015). Si una versión futura de Anki lo
  cambia, el interruptor queda como lo dibuje Anki, sin fallo. Solo cambia el lado «Tarjetas»; el de
  «Notas» sigue en verde. Decisión del taller.
- 3.8.0 · Las flechas de las listas desplegables y de los campos numéricos y la marca de las
  casillas se repintan copiando los iconos de Anki con los colores de la paleta, en la carpeta de
  datos del complemento. Anki los trae ya pintados en un blanco casi puro (de noche) o casi negro (de
  día). Los iconos de la barra lateral de Explorar y del editor no se tocan: los dibuja Anki con su
  propio color en cada sitio. Decisión del taller.
- 3.8.0 · La fila vacía bajo la cabecera de la lista de mazos, donde se suelta un mazo para sacarlo al
  nivel superior, mide 10 px en lugar de una línea entera (el informe proponía 8). Se puede seguir
  soltando ahí un mazo, con algo más de puntería; no crece al arrastrar, para que la lista no salte.
  Decisión del taller.
- 3.8.0 · El verde de «A repasar» y el tono 3 de Verde clásico de GritMap son casi el mismo verde. No
  se cambia: los colores de estado de Anki son una convención conocida (informe, apartado 1.6).
  Decisión del taller.
