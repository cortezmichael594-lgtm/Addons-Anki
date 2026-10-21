# Qué hace «Nocturne»

Versión 3.4.0 · 2026-10-21

Temas de color para Anki, en modo día y en modo noche. Trae tres paletas (Nocturne, Papel y Bosque), y
Nocturne está elegida de serie. Cada paleta es un estilo completo: colores, letra de los títulos,
esquinas, botones, separación de las filas de la lista de mazos, resaltados y banderas. La paleta se
elige en la configuración del complemento y se aplica al momento, sin reiniciar. En Windows 11, también
la barra de título de las ventanas toma los colores de la paleta. No toca su colección, sus tarjetas
ni sus plantillas.

La paleta Nocturne conserva el aspecto de la original que usted subió al taller (la del 28 de julio de
2026). Las decisiones se apoyan en los resúmenes de docs/referencias: sobre todo «Refactoring UI»,
«Practical UI», Norman, Tufte y el vídeo de tipografía de Tim Gabe, y en menor medida Webflow, Orbix y
Weinschenk. La versión 2.0.0, hecha en otra copia del taller, se descartó el 2026-10-21 y no está aquí.
Las paletas Grafito y Alto contraste existieron en la 3.1.0 y se retiraron en la 3.2.0 a petición del
cliente.

## 1. Dónde aparece

- Herramientas > «Complementos», con Nocturne seleccionado, botón «Configuración» (o doble clic en
  Nocturne): abre la ventana para elegir paleta, encima de la de complementos (no el editor de texto
  que Anki muestra con otros complementos). No hay entrada en el menú Herramientas: así lo pidió el
  cliente (2026-10-21).
- La paleta elegida se nota en todas las ventanas de Anki (la principal, Explorar, Añadir, Editar,
  Preferencias, menús, listas, tablas, casillas, botones, barras de desplazamiento y diálogos) y en sus
  páginas (barra superior, lista de mazos, pantalla de un mazo, repaso alrededor de la tarjeta y sus
  botones de respuesta, editor, estadísticas, opciones de mazo y felicitación).
- No cambia el aspecto de las tarjetas, que decide su plantilla, ni toca páginas de internet que otro
  complemento abra dentro de Anki.

## 2. La ventana de configuración

- Hecha como las de Anki (Preferencias > Interfaz de usuario), sin colores ni dibujos propios: hereda
  el tema, el teclado y el idioma. Título: «Configurar 'Nocturne'», el mismo que Anki pone a la
  configuración de cualquier complemento. Sin el botón «?» en la barra de título.
- Se abre encima de la ventana de complementos y, mientras está abierta, esa ventana no responde
  (como con cualquier diálogo de Anki). Aparece centrada sobre ella y con el tamaño justo para su
  contenido.
- Un recuadro «Apariencia» con la lista desplegable «Paleta» (Nocturne, Papel, Bosque) y, debajo, una
  línea con la descripción de la paleta elegida en la lista (textos en el apartado 3), que cambia al
  cambiar la elección. Al abrirla, está elegida la paleta activa. La ventana no cambia de tamaño al
  cambiar de paleta en la lista.
- Botones, con los nombres que pone Anki en su idioma: «Restaurar los valores predeterminados» (elige
  Nocturne en la lista; no se aplica hasta «Aceptar»), «Aceptar» (también con Ctrl+Intro, como en la
  configuración de Anki) y «Cancelar».
- Con «Aceptar», si ha elegido otra paleta, se aplica al momento a todas las ventanas y páginas
  abiertas y aparece el aviso «Paleta «Papel» aplicada.» (con el nombre que corresponda). Ese aviso es
  el de Anki: de día sale en su amarillo de siempre. Si deja la misma, no hace nada. «Cancelar», Esc o
  la X la cierran sin cambiar nada.
- Elegir en la lista no cambia nada todavía: la paleta se aplica solo con «Aceptar».
- Solo se elige la paleta: no hay ajustes sueltos. Así lo decidió el cliente (2026-10-21).

## 3. Las tres paletas

Todas siguen el modo día o noche que usted elija en Anki y cambian con él. Ningún color es blanco ni
negro puro.

Cada descripción ocupa una sola línea y las tres siguen la misma estructura: colores y acento, y
después su forma. Valen para el día y para la noche.

- Nocturne (de serie). Descripción en la ventana: «Grises azulados y acento azul. Letra del sistema y
  esquinas suaves.». Fondo #F7F8FA de día y #12161F de noche; texto #1B2430 y #D6DAE1;
  azul de acción #3B6FE0 y #4066E6. Títulos en seminegrita con las letras un poco más juntas, esquinas
  de 6px en las ventanas, 12px en los recuadros de las páginas y 7px en los botones de las ventanas.
  Un degradado azul muy tenue en la esquina superior derecha del fondo de las páginas. «Aprendiendo»
  va en naranja.
- Papel. «Papel y tinta con acento azul petróleo. Títulos con remates, como un libro.». De día: fondo #FAF7F1,
  texto #2A2520, acento #1F6A80. De noche («Tinta», elegida por el cliente el 2026-10-21): fondo azul
  petróleo muy oscuro #10171A, de la misma familia que el acento, y texto crema #E3DAC9; acento
  #1F6E85. Títulos de las páginas en Georgia (o Cambria), en negrita; descripciones con más espacio
  entre líneas; esquinas algo más redondeadas; filas de la lista de mazos un poco más holgadas;
  degradado azul petróleo muy tenue.
- Bosque. «Verdes grisáceos y acento verde azulado. Esquinas redondeadas y filas amplias.». Fondo #F3F7F4 y #111814; texto #17251C y #D5E0D8; acento #0F766E y #0E7068. Las esquinas
  más redondeadas de las tres, las filas más holgadas y un degradado verde azulado muy tenue.

Colores con significado (cifras de la lista de mazos, banderas, avisos): Nocturne y Papel de día usan
los suyos de siempre. En Bosque (día y noche) y en Papel de noche giran un poco su tono hacia el
carácter de la paleta: el azul hacia azul petróleo, el rojo hacia rojo ladrillo y el verde hacia verde
musgo, sin dejar de ser azul, rojo y verde. En Papel y en Bosque, «Aprendiendo» va en el rojo de Anki.

## 4. Lo que tienen todas

- Tres niveles de texto bien diferenciados: principal, secundario (más suave) y lo menos importante
  (más suave aún), todos legibles sobre cualquier fondo.
- De noche, lo que está «más arriba» es más claro: los campos hundidos son lo más oscuro, después el
  fondo, los recuadros, los botones, los menús desplegables y, por último, un botón con el ratón
  encima. Así los menús se distinguen de lo que tapan.
- De noche, los colores con significado son algo menos saturados, para que no «vibren» sobre el fondo
  oscuro.
- Barra de título de las ventanas (solo Windows 11): cada paleta tiene la suya, del matiz de su
  fondo y con algo más de color, más oscura que la ventana de noche y más clara de día, para que se
  distinga de la ventana y se reconozca la paleta:
  - Nocturne: azul profundo #070C16 de noche (fondo #12161F) y blanco azulado #FAFBFE de día (fondo
    #F7F8FA).
  - Papel: azul petróleo profundo #070F12 de noche (fondo #10171A) y marfil #FFFCF7 de día (fondo
    #FAF7F1).
  - Bosque: verde profundo #08100C de noche (fondo #111814) y blanco menta #F8FEFA de día (fondo
    #F3F7F4).
  De día la diferencia con la ventana es pequeña: el fondo ya es casi blanco y la barra no llega al
  blanco puro. Título en el color del texto y borde suave, en vez de blanca de día y negra de noche. Cambia con el modo
  día o noche y con la paleta. El título de las ventanas que no están en primer plano va en el texto
  secundario, para distinguir cuál es la activa. Los botones de minimizar, maximizar y cerrar siguen
  el modo día o noche de Anki, aunque Windows esté en el otro. Cada ventana se tiñe antes de aparecer,
  así que no se ve primero blanca. En Windows 10, macOS y Linux la barra queda como siempre.
- Ayudas emergentes (el recuadro que aparece al dejar el ratón sobre un botón): con el mismo fondo, el
  mismo borde suave y algo de margen que los menús, en vez de confundirse con la ventana.
- Lista de mazos: las cabeceras de las columnas (Mazo, Nuevas, Aprendiendo...) van en el texto
  secundario y algo menos gruesas. Pantalla de un mazo: las etiquetas «Nuevas:», «Aprendiendo:» y «A
  repasar:» van en el texto secundario. Así destacan las cifras, que es lo que se viene a mirar. Solo en
  esas dos tablas.
- Al pasar el ratón por las páginas de Anki, los cambios de color tardan 100 milisegundos en vez de
  180, y se perciben instantáneos. El fundido de las tarjetas no cambia. Si tiene marcada «Reducir
  movimiento» en las preferencias de Anki, los cambios son inmediatos (desde la 3.4.0).
- Títulos de las páginas que ocupan varias líneas (por ejemplo, el nombre largo de un mazo): las
  líneas quedan de longitud parecida, sin una palabra sola debajo. En la descripción de un mazo, la
  última línea no queda con una sola palabra (desde la 3.4.0).
- Casillas, botones de opción y barras propias de las páginas de Anki que no tienen un color dado
  toman el color de acción de la paleta, para que haya un solo color de acción (desde la 3.4.0).
- Al moverse con el teclado por la barra superior (Mazos, Añadir, Explorar...) y por los enlaces de
  las páginas (el nombre de cada mazo, el engranaje de opciones), la opción con el foco lleva el
  contorno del color de acción de la paleta. Anki lo oculta en la barra superior; el contorno no ocupa
  sitio y nada se mueve. El subrayado de los enlaces va algo separado de las letras (desde la 3.4.0).
- Barra superior (Mazos, Añadir, Explorar, Estadísticas, Sincronizar): al pasar el ratón, la opción
  toma un fondo suave con las esquinas de la paleta, en lugar del subrayado de Anki. No cambia de
  tamaño ni de sitio.
- Botones de respuesta del repaso: una raya fina de color al pie de «Otra vez» (rojo), «Difícil»
  (naranja), «Bien» (verde) y «Fácil» (azul), también con el ratón encima. El texto no cambia; el color
  solo ayuda a reconocerlos de un vistazo.
- Botón principal de las ventanas (el que se pulsa con Intro, por ejemplo «Aceptar» o «Añadir»)
  relleno del color de acción, con texto blanco. Al pasar el ratón o llegar con el teclado se oscurece
  y lleva un anillo; al pulsarlo, se oscurece más. Si está desactivado, se ve como un botón normal
  apagado. Al moverse con Tab entre botones, el relleno sigue al botón que respondería a Intro.
- Esquinas de los botones y recuadros según la paleta.
- Casillas y botones de opción con un borde visible sin marcar; con el ratón encima o con el foco, el
  borde toma el color de acción.
- En la lista de mazos, la fila del mazo actual y la que tiene el ratón encima se resaltan con un tinte
  del color de acción. Solo las filas de mazos: la tabla de la pantalla de estudio (Nuevas,
  Aprendiendo, A repasar) no se resalta. En Explorar, las filas seleccionadas llevan un tinte más
  visible que en Anki. El texto que se selecciona en las páginas toma ese mismo tinte.
- Banderas: conservan el color de su nombre (la roja es roja) y, además, la roja y la verde se
  distinguen por su claridad, para quien confunde el rojo y el verde. En Nocturne, la bandera rosa es
  rosa de verdad: antes de la 3.1.0 se confundía con la roja.
- En la lista de mazos, la pantalla de un mazo y las tablas de las páginas, todas las cifras tienen el
  mismo ancho y se alinean en columna.
- La descripción de un mazo tiene líneas de unos 70 caracteres como mucho.
- Al moverse con el teclado por los botones de la lista de mazos, de la pantalla de un mazo y del
  repaso, el botón con el foco lleva un contorno del color de acción. Anki lo oculta de serie. Al
  abrir la pantalla de un mazo, Anki pone el foco en «Comenzar a estudiar», así que ese contorno se ve
  desde el principio: indica que Intro empieza el estudio.
- Letra del texto de las páginas: la de interfaz del sistema (en Windows, Segoe UI Variable o Segoe
  UI), con la que Anki elige para su idioma como reserva (por ejemplo, para japonés o chino).
- No cambia el tamaño de la letra (manda el que tenga elegido en Anki) ni la letra de las ventanas,
  que Anki elige según el idioma.

## 5. Sin parpadeos

- Aplica la paleta antes de que se dibuje cada página, también en estadísticas y felicitación, para
  que no haya un fogonazo claro al abrirlas de noche.
- Al cambiar de paleta, ventanas y páginas cambian una sola vez, sin recargarse; lo que estuviera
  escribiendo en el editor se conserva.
- Al cambiar de perfil vuelve a afirmar los colores sin redibujar las ventanas.

## 6. Qué guarda

- Solo el nombre de la paleta elegida, en la configuración del complemento (la que Anki guarda en su
  carpeta de complementos). Es la misma para todos los perfiles. No viaja con la sincronización.
- Si esa configuración falta, es antigua o tiene un valor que no existe (por ejemplo, «grafito» o
  «alto_contraste» de la 3.1.0), usa Nocturne sin avisar.

## 7. Si algo falla

- Ningún fallo abre la ventana de error ni interrumpe un repaso: Anki conserva su aspecto habitual en
  la parte afectada y el detalle queda en el registro propio del complemento.
- Si Windows no acepta el color de la barra de título, la barra queda como siempre. Si al teñirla
  ocurre un error, el complemento deja de teñir barras hasta el próximo arranque de Anki, sin avisar.

## 8. Qué no hace

- No permite ajustar por separado colores, letra o esquinas: cada paleta va completa.
- No se conecta a internet ni descarga letras: usa las que ya trae el sistema (si falta Georgia, Papel
  usa Cambria u otra letra con remates).
- No cambia su colección, sus tarjetas ni el aspecto que tenga elegido con otro estilo de controles en
  Preferencias: con un estilo que no sea el de Anki, botones y casillas quedan como los dibuje el
  sistema.

## 9. Legibilidad medida (2026-10-21)

Contraste del texto frente al fondo; el mínimo recomendado para leer con comodidad es 4,5 (y 3 para
bordes de casillas e iconos). Lo comprueban las pruebas del taller en cada entrega, en las tres
paletas, de día y de noche.

- Todo color que Anki usa como texto llega al menos a 4,5 sobre cualquier fondo, también sobre el
  resaltado de la fila.
- El texto blanco de los botones de acción llega a 4,5 en todos sus estados.
- De noche, el texto desactivado (botones apagados y la cifra de tarjetas enterradas, como «+3», de la
  pantalla de un mazo) es algo más claro desde la 3.3.0, en las tres paletas: llega al mínimo de APCA
  para texto (30) sobre el fondo, los recuadros y los botones, y sigue más apagado que el texto menos
  importante, para que lo desactivado se vea desactivado.
- Las casillas sin marcar llegan a 3 frente al fondo; las banderas, a 3 como icono; las rayas de los
  botones de respuesta, a 3 sobre el botón.
- En Explorar, el texto de las filas con bandera o estado, y el de las filas seleccionadas, llega a 4,5.
- La bandera roja y la verde se diferencian en claridad al menos 1,4 veces.
- De noche, el texto principal queda como mucho en 13,5 frente al fondo, para no deslumbrar (en
  Nocturne y en Papel, 13; la versión original de Nocturne llegaba a 15,4).
- Además se mide con APCA, un método más reciente que tiene en cuenta que el texto claro sobre fondo
  oscuro se percibe distinto: el texto principal llega al menos a 75, el secundario a 60 y el menos
  importante a 45 (mínimos que propone «Practical UI»).
