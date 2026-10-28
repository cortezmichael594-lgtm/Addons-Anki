# Qué hace «Atelier»

Versión 3.7.0 · 2026-10-28

Temas de color para Anki, en modo día y en modo noche. Trae cinco paletas (Nocturne, Papel, Bosque,
Lavanda y Atardecer), y Nocturne está elegida de serie. Hasta la 3.5.0 el complemento se llamaba
«Nocturne»; desde la 3.6.0 se llama «Atelier» (elegido por el cliente el 2026-10-28) y «Nocturne» queda
como nombre de la paleta de serie. Para Anki sigue siendo el mismo complemento: la actualización
reemplaza a la anterior y conserva la paleta elegida. Cada paleta es un estilo completo: colores, letra de los títulos,
esquinas, botones, separación de las filas de la lista de mazos, resaltados y banderas. La paleta se
elige en la configuración del complemento, se ve al momento mientras se elige y se conserva con
«Aceptar», sin reiniciar. En Windows 11, también la barra de título de las ventanas toma los colores de
la paleta. Si su sistema pide más contraste, Atelier se aparta y deja los colores del sistema. No toca
su colección, sus tarjetas ni sus plantillas.

Desde la 3.5.0 aplica el informe de mejoras del 2026-10-26, salvo lo que trata del día de gracia y de
la meta diaria, que el cliente descartó (no aplica a un tema de colores).

La paleta Nocturne conserva el aspecto de la original que usted subió al taller (la del 28 de julio de
2026). Las decisiones se apoyan en los resúmenes de docs/referencias: sobre todo «Refactoring UI»,
«Practical UI», Norman, Tufte y el vídeo de tipografía de Tim Gabe, y en menor medida Webflow, Orbix y
Weinschenk. La versión 2.0.0, hecha en otra copia del taller, se descartó el 2026-10-21 y no está aquí.
Las paletas Grafito y Alto contraste existieron en la 3.1.0 y se retiraron en la 3.2.0 a petición del
cliente.

## 1. Dónde aparece

- Herramientas > «Complementos», con Atelier seleccionado, botón «Configuración» (o doble clic en
  Atelier): abre la ventana para elegir paleta, encima de la de complementos (no el editor de texto
  que Anki muestra con otros complementos). No hay entrada en el menú Herramientas: así lo pidió el
  cliente (2026-10-21).
- La primera vez que Anki arranca con el complemento instalado, un segundo y medio después de abrirse
  la ventana principal, sale durante 6 segundos el aviso de Anki «Atelier está activo, con la paleta
  Nocturne. Para elegir otra: Herramientas > Complementos > Atelier > Configuración.». Solo una vez: no
  vuelve a salir, ni al cambiar de perfil ni al actualizar.
- A quien ya tenía el complemento cuando se llamaba Nocturne (vio su aviso de bienvenida), en su
  lugar sale una sola vez «Nocturne ahora se llama Atelier. Su paleta sigue igual.» (desde la
  3.7.0).
- La paleta elegida se nota en todas las ventanas de Anki (la principal, Explorar, Añadir, Editar,
  Preferencias, menús, listas, tablas, casillas, botones, barras de desplazamiento y diálogos) y en sus
  páginas (barra superior, lista de mazos, pantalla de un mazo, repaso alrededor de la tarjeta y sus
  botones de respuesta, editor, estadísticas, opciones de mazo y felicitación).
- No cambia el aspecto de las tarjetas, que decide su plantilla, ni toca páginas de internet que otro
  complemento abra dentro de Anki.

## 2. El panel de configuración (desde la 3.7.0)

Un panel a medida, con el mismo material y las mismas medidas que el de GritMap 4.11.2 (informe del
cliente del 2026-10-28): es una página dentro de la ventana, como las opciones de mazo de Anki.

- Título de la ventana: «Atelier», sin el botón «?». Se abre centrado encima de la ventana de
  complementos, que no responde mientras está abierto (como con cualquier diálogo de Anki). Mide
  560 px de ancho y el alto justo para su contenido (unos 650 px con la interfaz al 100 %), como
  mucho 720 px o el alto de la pantalla menos 80 px; si no cabe, el cuerpo se desplaza y la cabecera
  y el pie quedan fijos. No se enseña hasta que está dibujado, para que no parpadee.
- Cabecera «Paleta» (14 px, seminegrita). Debajo, en el texto secundario: «Elija una paleta: se ve
  ya en Anki y se guarda al aceptar.».
- Encima de la lista, una sola vez, los rótulos «Día» y «Noche»: el del modo en que está Anki, en el
  color del texto y en seminegrita; el otro, en el secundario. Cambian si Anki cambia de modo con el
  panel abierto.
- Las cinco paletas a la vista, una debajo de otra y por orden alfabético, como los temas de GritMap:
  Atardecer, Bosque, Lavanda, Nocturne y Papel. Cada una es un recuadro de 76 px de alto con:
  - dos miniaturas de 80 × 48 px, la de día y la de noche, que son la lista de mazos reducida a lo
    que cambia entre paletas: su fondo, su borde, la barra superior, un recuadro con dos filas (texto
    principal y secundario) y los tres puntos azul, rojo y verde de Nuevas, Aprendiendo y A repasar, y
    un botón del color de acción, con la esquina de esa paleta. La de día va siempre en sus colores
    de día y la de noche en los de noche, esté Anki como esté;
  - el nombre (en Papel, en su letra de títulos, Georgia o Cambria), con «predeterminada» detrás en
    Nocturne, y debajo la descripción (apartado 3);
  - a la derecha, una marca ✓ en la elegida.
- La elegida lleva borde de 2 px en el tono de trazo de acción, por dentro (nada se mueve), el fondo
  con el tinte de acción y la ✓. Con el ratón encima, el borde se oscurece. Toda la fila se pulsa.
- Un clic en una paleta la aplica al momento a todo Anki, también al propio panel. Con el teclado: el
  tabulador entra en la paleta elegida; las flechas (arriba, abajo, izquierda o derecha) pasan a la
  siguiente y la eligen, y de la última vuelven a la primera; se aplica cuando la elección lleva 200
  milisegundos quieta, para que recorrerlas no repinte Anki a cada paso; la barra espaciadora elige la
  que tiene el foco. El foco se ve con un contorno de 2 px del color de acción.
- «Aceptar» (o Ctrl+Intro) conserva y guarda la paleta, sin más avisos: el cambio ya se ha visto.
  «Cancelar», Esc o la X vuelven a la paleta que había al abrir el panel. En Windows, «Aceptar» va
  primero, como en sus ventanas; en macOS y Linux, a la derecha. «Aceptar» es el único botón relleno.
- Debajo de la lista: «Cada paleta tiene versión de día y de noche. Anki está ahora en modo noche; el
  modo se cambia en Preferencias de Anki.» (o «modo día»).
- No hay «Restaurar los valores predeterminados»: Nocturne ya dice «predeterminada» en su fila y un
  clic la elige.
- Avisos, arriba y en una franja de fondo hundido con un icono de aviso, sin rojo:
  - solo si en la sesión algo no se pudo pintar: «Alguna parte de Anki no se pudo pintar y conserva su
    aspecto normal.», con el botón «Abrir el registro», que abre la carpeta del registro;
  - si su sistema pide más contraste (apartado 5), en lugar de la línea de introducción: «Su sistema
    pide más contraste: Atelier deja sus colores. La paleta que elija se aplicará cuando vuelva al
    contraste normal y reinicie Anki.». Se puede elegir y guardar, sin vista previa. Con los temas de
    contraste de Windows, el panel se dibuja con los colores del sistema salvo las miniaturas, que
    conservan los suyos porque son lo que se elige.
- Para un lector de pantalla, la lista es un grupo de botones de opción llamado «Paleta»; cada opción
  se lee por su nombre, con la descripción como información adicional; las miniaturas no se leen.
- El texto del panel no se puede seleccionar con el ratón, como en GritMap.
- Salida de emergencia: si el panel falla al crearse o no avisa de que está dibujado en 3 segundos,
  se cierra sin cambiar nada y se abre la ventana sencilla: una fila «Paleta» con una lista desplegable
  de las cinco paletas (por orden alfabético, con su muestra de color), la descripción de la elegida
  debajo, la misma vista previa y los botones «Restaurar los valores predeterminados», «Cancelar» y
  «Aceptar». El fallo queda en el registro y en la línea de aviso de la próxima vez.
- Solo se elige la paleta: no hay ajustes sueltos. Así lo decidió el cliente (2026-10-21).

## 3. Las cinco paletas

Todas siguen el modo día o noche que usted elija en Anki y cambian con él. Ningún color es blanco ni
negro puro.

Cada descripción ocupa una sola línea y todas siguen la misma estructura: colores y botones, y
después su forma. Valen para el día y para la noche. Desde la 3.5.0 dicen «botones» en lugar de
«acento». El nombre «Tinta» de Papel de noche no aparece en la ventana: un nombre por cosa.

- Nocturne (de serie). Descripción en la ventana: «Grises azulados y botones azules. Letra del sistema
  y esquinas suaves.». Fondo #F7F8FA de día y #12161F de noche; texto #1B2430 y #D6DAE1;
  azul de acción #3B6FE0 y #4066E6. Títulos en seminegrita con las letras un poco más juntas, esquinas
  de 6px en botones y campos de las ventanas y 12px en los recuadros de las páginas. Un degradado azul
  muy tenue en la esquina superior derecha del fondo de las páginas. «Aprendiendo» va en el rojo de la
  paleta desde la 3.5.0 (antes, naranja, que también era el color de «Difícil»).
- Papel. «Papel y tinta, con botones azul petróleo. Títulos con remates, como un libro.». De día: fondo #FAF7F1,
  texto #2A2520, acento #1F6A80. De noche («Tinta», elegida por el cliente el 2026-10-21): fondo azul
  petróleo muy oscuro #10171A, de la misma familia que el acento, y texto crema #E3DAC9; acento
  #1F6E85. Títulos de las páginas en Georgia (o Cambria), en negrita; descripciones con más espacio
  entre líneas; esquinas de 6px en botones y campos y 12px en los recuadros (desde la 3.7.0; antes 7 y 14); filas de la lista de mazos un poco más holgadas;
  degradado azul petróleo muy tenue.
- Bosque. «Verdes grisáceos y botones verde azulado. Esquinas redondeadas y filas amplias.». Fondo
  #F3F7F4 y #111814; texto #17251C y #D5E0D8; acento #0F766E y #0E7068. Las esquinas más redondeadas de
  las cinco junto con Atardecer (8px en botones y campos y 16px en los recuadros), las filas más
  holgadas y un degradado verde azulado muy tenue.
- Lavanda (desde la 3.6.0). «Grises lila y botones violeta. Letra y esquinas como Nocturne.».
  Fondo #F8F7FA de día y #17121F de noche; texto #231B30 y #DAD6E1; violeta de acción #7B47D4 y
  #804CDA. Fría y tranquila, como Nocturne pero en lila. Esquinas de 6px en botones y campos y 12px en
  los recuadros (desde la 3.7.0; antes 7 y 14); degradado violeta muy tenue. Barra de título lila: #FBFAFE de día y #0C0716 de noche.
- Atardecer (desde la 3.6.0). «Melocotón y marrón cálido, con botones cobre. Esquinas redondeadas.».
  Fondo melocotón muy claro #FCF8F5 de día y marrón cálido #1F1712 de noche; texto #261C15 y #E1DAD6;
  cobre de acción #845727 y #8F5D27. Cálida, para estudiar con luz baja. Esquinas de 8px en botones y
  campos y 16px en los recuadros; degradado cobre muy tenue. Barra de título melocotón: #FFFBF9 de día y
  #160D07 de noche. El cobre tiene un matiz parecido al naranja de «Difícil», pero es mucho más oscuro
  (se distinguen por claridad, lo comprueban las pruebas) y está a 31° del rojo de «Aprendiendo».
- Lavanda y Atardecer salen de las fuentes: el morado de HueHive y el «Púrpura real» de GritMap, y el
  «Resplandor del atardecer» de Webflow. Se obtienen girando el matiz de los grises y del color de
  acción de Nocturne, que ya cumple todas las medidas de legibilidad, y pasan las mismas pruebas que
  las demás.

Colores con significado (cifras de la lista de mazos, banderas, avisos): Nocturne y Papel de día usan
los suyos de siempre. En Bosque (día y noche) y en Papel de noche giran un poco su tono hacia el
carácter de la paleta: el azul hacia azul petróleo, el rojo hacia rojo ladrillo y el verde hacia verde
musgo, sin dejar de ser azul, rojo y verde. Lavanda y Atardecer usan los de Nocturne (en Lavanda de
noche, la bandera roja y la verde algo ajustadas para que se distingan con daltonismo). En las cinco
paletas, «Aprendiendo» va en el rojo de la paleta (en Nocturne, desde la 3.5.0).

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
  La diferencia con la ventana es pequeña (de 1,03 a 1,08 a 1 de contraste): lo que más la separa es
  el borde suave, y el matiz es lo que la identifica con su paleta. De día no puede ser mucho más
  clara: el fondo ya es casi blanco y la barra no llega al blanco puro. Título en el color del texto y
  borde suave, en vez de blanca de día y negra de noche. Cambia con el modo
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
  movimiento» en las preferencias de Anki, los cambios son inmediatos (desde la 3.4.0), y también si la
  tiene en el sistema (en Windows, «Efectos de animación» desactivados; desde la 3.5.0).
- Títulos de las páginas que ocupan varias líneas (por ejemplo, el nombre largo de un mazo): las
  líneas quedan de longitud parecida, sin una palabra sola debajo. En la descripción de un mazo, la
  última línea no queda con una sola palabra (desde la 3.4.0).
- Casillas, botones de opción y barras propias de las páginas de Anki que no tienen un color dado
  toman el color de acción de la paleta, para que haya un solo color de acción (desde la 3.4.0); desde
  la 3.5.0, en su tono de trazo (el del foco), que de noche es más claro y se ve bien sobre fondo
  oscuro.
- Dos tonos de acción: el de los rellenos (botones principales, con texto blanco encima) y otro para
  los trazos (contornos de foco, anillo del botón principal, bordes de casillas con el ratón o el foco
  y enlaces). De día casi coinciden; de noche el de trazo es más claro, y se ve a 3 a 1 o más sobre
  cualquier fondo (a 4,3 o más sobre el de la ventana).
- Repaso (desde la 3.7.0): «Editar» y «Más», a los lados de la barra inferior, sin fondo ni borde
  (el borde queda transparente, así que no cambian de tamaño) y con un fondo suave al pasar el ratón,
  como la barra superior: así, los botones de respuesta son lo único con forma de botón.
- Menús y listas desplegables de las ventanas (desde la 3.7.0): la opción con el ratón o el teclado
  encima se marca con el tinte de acción y el texto normal, como la fila del mazo actual y las filas de
  Explorar, en vez del relleno azul con texto blanco de Anki: una sola forma de marcar lo
  seleccionado. Las cabeceras de las columnas de Explorar van en el texto secundario, como las de la
  lista de mazos.
- Repaso: los intervalos que salen encima de los botones de respuesta («10 min», «4 d») van en el texto
  secundario y con cifras de igual ancho (desde la 3.5.0). «Comenzar a estudiar» ya va relleno del
  color de acción con texto blanco: lo hace Anki con el azul de la paleta. Las cifras en cero de la
  lista de mazos ya van en el texto más suave: también lo hace Anki con el de la paleta.
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
- Esquinas según la paleta, con una regla para todas (desde la 3.5.0): botones y campos (de texto,
  listas desplegables, listas) llevan la misma esquina, y los recuadros de las páginas, el doble.
  Desde la 3.7.0, dos familias separadas un 33 %: suaves (6 y 12px: Nocturne, Papel y Lavanda) y
  redondeadas (8 y 16px: Bosque y Atardecer). Las casillas, 4px, para que no parezcan botones
  de opción (estos siguen redondos).
- Casillas y botones de opción con un borde visible sin marcar; con el ratón encima o con el foco, el
  borde toma el color de acción.
- En la lista de mazos, la fila del mazo actual y la que tiene el ratón encima se resaltan con un tinte
  del color de acción. Solo las filas de mazos: la tabla de la pantalla de estudio (Nuevas,
  Aprendiendo, A repasar) no se resalta. En Explorar, las filas seleccionadas llevan un tinte más
  visible que en Anki. El texto que se selecciona en las páginas toma ese mismo tinte.
- Banderas: conservan el color de su nombre (la roja es roja) y, además, la roja y la verde se
  distinguen por su claridad, para quien confunde el rojo y el verde. Desde la 3.5.0 se comprueba con
  una simulación de daltonismo (deuteranopía y protanopía) en las cinco paletas, de día y de noche: para
  conseguirlo, la bandera roja es algo más oscura (y, en Nocturne de noche, la verde algo más clara),
  con el mismo tono. En las filas de Explorar es lo único que las distingue. En Nocturne, la bandera rosa es
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

## 5. Alto contraste del sistema (desde la 3.5.0)

- Si al abrir Anki su sistema pide más contraste (temas de contraste de Windows 11, «Aumentar
  contraste» de macOS o alto contraste de GNOME), Atelier no pinta nada: ni ventanas, ni páginas, ni
  barra de título. Deciden Anki y el sistema, que ofrecen el contraste máximo que Nocturne suaviza a
  propósito.
- La ventana de configuración lo dice y deja elegir y guardar la paleta, que se aplicará cuando el
  sistema vuelva al contraste normal y se reinicie Anki.
- Se comprueba al abrir Anki: si cambia el contraste del sistema con Anki abierto, hay que reiniciarlo.
- Con versiones de Anki cuyo Qt no informa del contraste (anteriores a Qt 6.10), nada cambia.

## 6. Sin parpadeos

- Aplica la paleta antes de que se dibuje cada página, también en estadísticas y felicitación, para
  que no haya un fogonazo claro al abrirlas de noche.
- Al cambiar de paleta, ventanas y páginas cambian una sola vez, sin recargarse; lo que estuviera
  escribiendo en el editor se conserva.
- Al cambiar de perfil vuelve a afirmar los colores sin redibujar las ventanas.

## 7. Qué guarda

- El nombre de la paleta elegida y que ya salieron el aviso de bienvenida (desde la 3.5.0) y el del
  nombre nuevo (desde la 3.7.0), en la
  configuración del complemento (la que Anki guarda en su carpeta de complementos). No es un ajuste:
  no aparece en ninguna ventana. Es la misma para todos los perfiles. No viaja con la sincronización.
- Si esa configuración falta, es antigua o tiene un valor que no existe (por ejemplo, «grafito» o
  «alto_contraste» de la 3.1.0), usa Nocturne sin avisar.

## 8. Si algo falla

- Ningún fallo abre la ventana de error ni interrumpe un repaso: Anki conserva su aspecto habitual en
  la parte afectada y el detalle queda en el registro propio del complemento. Desde la 3.5.0, la
  ventana de configuración lo dice en una línea, con el botón «Abrir el registro» (apartado 2).
- Si Windows no acepta el color de la barra de título, la barra queda como siempre. Si al teñirla
  ocurre un error, el complemento deja de teñir barras hasta el próximo arranque de Anki, sin avisar.

## 9. Qué no hace

- No permite ajustar por separado colores, letra o esquinas: cada paleta va completa.
- No se conecta a internet ni descarga letras: usa las que ya trae el sistema (si falta Georgia, Papel
  usa Cambria u otra letra con remates).
- No cambia su colección, sus tarjetas ni el aspecto que tenga elegido con otro estilo de controles en
  Preferencias: con un estilo que no sea el de Anki, botones y casillas quedan como los dibuje el
  sistema.

## 10. Legibilidad medida (2026-10-26)

Contraste del texto frente al fondo; el mínimo recomendado para leer con comodidad es 4,5 (y 3 para
bordes de casillas e iconos). Lo comprueban las pruebas del taller en cada entrega, en las cinco
paletas, de día y de noche.

- Todo color que Anki usa como texto llega al menos a 4,5 sobre cualquier fondo, también sobre el
  resaltado de la fila.
- El texto blanco de los botones de acción llega a 4,5 en todos sus estados.
- De noche, el texto desactivado (botones apagados y la cifra de tarjetas enterradas, como «+3», de la
  pantalla de un mazo) es algo más claro desde la 3.3.0, en todas las paletas: llega al mínimo de APCA
  para texto (30) sobre el fondo, los recuadros y los botones, y sigue más apagado que el texto menos
  importante, para que lo desactivado se vea desactivado.
- Las casillas sin marcar llegan a 3 frente al fondo; las banderas, a 3 como icono; las rayas de los
  botones de respuesta, a 3 sobre el botón.
- En Explorar, el texto de las filas con bandera o estado, y el de las filas seleccionadas, llega a 4,5.
- La bandera roja y la verde se diferencian en claridad al menos 1,4 veces, también vistas como las ve
  quien tiene deuteranopía o protanopía (simulación de Machado, 2009; desde la 3.5.0).
- Los trazos de acción (foco, anillo, enlaces) llegan a 3 sobre cualquier fondo (desde la 3.5.0).
- De noche, el texto principal queda como mucho en 13,5 frente al fondo, para no deslumbrar (en
  Nocturne y en Papel, 13; la versión original de Nocturne llegaba a 15,4).
- Además se mide con APCA, un método más reciente que tiene en cuenta que el texto claro sobre fondo
  oscuro se percibe distinto: el texto principal llega al menos a 75, el secundario a 60 y el menos
  importante a 45 (mínimos que propone «Practical UI»).
