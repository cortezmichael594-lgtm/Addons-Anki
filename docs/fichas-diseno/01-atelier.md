# Ficha de diseño: Atelier

Versión 3.8.0 (4 de noviembre de 2026). Nombre interno del paquete: «nocturne» (hasta la 3.5.0 el
complemento se llamaba Nocturne; ahora Nocturne es solo el nombre de su paleta de serie). Léase
junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Un tema de color completo para todo Anki: cinco paletas (Atardecer, Bosque, Lavanda, Nocturne y
Papel), cada una con versión de día y de noche, que cambian colores, letra de los títulos, esquinas,
botones, separación de filas, resaltados y banderas de todas las ventanas y páginas de Anki. Es el
complemento de color principal: los demás toman de él sus colores.

## 2. Para quién y para qué

Para estudiar muchas horas con una interfaz cómoda, legible y coherente, de día y de noche, sin
deslumbrar. No toca la colección, las tarjetas ni sus plantillas: el aspecto de cada tarjeta lo
decide su plantilla.

## 3. Dónde se ve

- En todas las ventanas de Anki: principal, Explorar, Añadir, Editar, Preferencias, menús, listas,
  tablas, casillas, botones, barras de desplazamiento y diálogos.
- En todas las páginas: barra superior, lista de mazos, pantalla de un mazo, repaso (alrededor de la
  tarjeta y sus botones), editor, estadísticas, opciones de mazo y felicitación.
- En Windows 11, en la barra de título de cada ventana.
- No cambia el aspecto de las tarjetas ni las páginas de internet que otro complemento abra dentro
  de Anki.
- No tiene entrada en los menús: su ventana se abre desde Herramientas > Complementos > Atelier >
  Configuración (o doble clic en Atelier). Lo pidió la persona.

## 4. Primer contacto

- La primera vez que Anki arranca con el complemento, 1,5 s después de abrirse la ventana principal,
  sale durante 6 s el aviso breve de Anki (recuadro amarillo con letra negra, propio de Anki): «Atelier
  está activo, con la paleta Nocturne. Para elegir otra: Herramientas > Complementos > Atelier >
  Configuración.». Una sola vez en la vida del complemento.
- Quien ya lo tenía cuando se llamaba Nocturne ve en su lugar, una vez: «Nocturne ahora se llama
  Atelier. Su paleta sigue igual.».

## 5. El panel de configuración

Es una página dentro de una ventana, con el mismo material y las mismas medidas que el panel de
opciones de GritMap, para que los dos se reconozcan como familia.

Ventana:

- Título «Atelier», sin el botón «?». Se abre centrada sobre la ventana de complementos, que queda
  bloqueada mientras tanto.
- 560 px de ancho; el alto justo para el contenido (unos 650 px con la interfaz al 100 %), como
  mucho 720 px o el alto de pantalla menos 80 px. Si no cabe, el cuerpo se desplaza y la cabecera y
  el pie quedan fijos.
- No se enseña hasta estar dibujada (sin parpadeo). Mientras se prepara, el puntero es el de espera
  (la primera vez en una sesión puede tardar hasta 3 s).
- El texto del panel no se puede seleccionar con el ratón.

Contenido, de arriba abajo:

1. Cabecera «Paleta», 14 px, seminegrita. Debajo, en texto secundario: «Elija una paleta: se ve ya
   en Anki y se guarda al aceptar.».
2. Rótulos «Día» y «Noche» encima de las columnas de miniaturas, una sola vez. El del modo actual de
   Anki va en color de texto y seminegrita; el otro, en texto secundario. Cambian si Anki cambia de
   modo con el panel abierto.
3. Las cinco paletas, una debajo de otra, por orden alfabético. Cada fila es un recuadro de 76 px de
   alto con:
   - Dos miniaturas de 80 × 48 px (día y noche, cada una siempre en sus colores, esté Anki como esté).
     Son la lista de mazos reducida a lo que cambia: fondo, borde, barra superior, un recuadro con dos
     filas (texto principal y secundario), tres puntos azul, rojo y verde (Nuevas, Aprendiendo, A
     repasar) y un botón del color de acción, con la esquina de esa paleta.
   - El nombre (en Papel, con su letra de títulos, Georgia o Cambria), con «predeterminada» detrás en
     Nocturne, y debajo una descripción de una línea (apartado 6).
   - A la derecha, una marca ✓ en la elegida.
   - La elegida lleva borde de 2 px por dentro (nada se mueve) en el tono de trazo de acción, fondo con
     el tinte de acción y la ✓. Con el ratón encima, el borde se oscurece. Toda la fila se pulsa.
4. Debajo de la lista: «Cada paleta tiene versión de día y de noche. Anki está ahora en modo noche;
   se cambia en Preferencias de Anki, en «Tema».» (o «modo día»).
5. Pie con «Aceptar» y «Cancelar». En Windows, «Aceptar» primero; en macOS y Linux, a la derecha.
   «Aceptar» es el único botón relleno.

Comportamiento:

- Vista previa en vivo: un clic en una paleta la aplica al momento a todo Anki, también al panel.
- «Aceptar» (o Ctrl+Intro) guarda, sin más avisos. «Cancelar», Esc o la X vuelven a la paleta que
  había al abrir.
- No hay «Restaurar los valores predeterminados»: Nocturne ya dice «predeterminada» y un clic la elige.
- Solo se elige la paleta: no hay ajustes sueltos de color, letra o esquinas (decisión de la persona).

Avisos dentro del panel (arriba, en una franja de fondo hundido con un icono de aviso, sin rojo):

- Si en la sesión algo no se pudo pintar: «Alguna parte de Anki no se pudo pintar y conserva su
  aspecto normal.», con el botón «Abrir el registro».
- Si el sistema pide más contraste, en lugar de la línea de introducción: «Su sistema pide más
  contraste: Atelier deja sus colores. La paleta que elija se aplicará cuando vuelva al contraste
  normal y reinicie Anki.». Se puede elegir y guardar, sin vista previa.

Salida de emergencia: si el panel falla o no carga en 3 s, se abre una ventana sencilla nativa con una
fila «Paleta» y una lista desplegable de las cinco (con su muestra de color), la descripción de la
elegida debajo, la misma vista previa y los botones «Restaurar los valores predeterminados»,
«Cancelar» y «Aceptar».

## 6. Las cinco paletas

Todas siguen el modo día o noche de Anki. Ningún color es blanco ni negro puro. Descripción que se ve
en el panel entre comillas.

| Paleta | Descripción visible | Carácter | Fondo día / noche | Texto día / noche | Acción día / noche |
|---|---|---|---|---|---|
| Atardecer | «Melocotón y marrón cálido, con botones cobre. Esquinas redondeadas.» | Cálida, para estudiar con luz baja | #FCF8F5 / #1F1712 | #261C15 / #E1DAD6 | #845727 / #8F5D27 |
| Bosque | «Verdes grisáceos y botones verde azulado. Esquinas redondeadas y filas amplias.» | Natural, holgada | #F3F7F4 / #111814 | #17251C / #D5E0D8 | #0F766E / #0E7068 |
| Lavanda | «Grises lila y botones violeta. Letra y esquinas como Nocturne.» | Fría y tranquila | #F8F7FA / #17121F | #231B30 / #DAD6E1 | #7B47D4 / #804CDA |
| Nocturne (de serie) | «Grises azulados y botones azules. Letra del sistema y esquinas suaves.» | Sobria, luminosa de día y profunda de noche | #F7F8FA / #12161F | #1B2430 / #D6DAE1 | #3B6FE0 / #4066E6 |
| Papel | «Papel y tinta, con botones azul petróleo. Títulos con remates, como un libro.» | Editorial; de noche, «Tinta»: azul petróleo con texto crema | #FAF7F1 / #10171A | #2A2520 / #E3DAC9 | #1F6A80 / #1F6E85 |

Forma de cada paleta:

| Paleta | Letra de títulos | Peso | Interletraje | Interlineado de descripciones | Esquina de botones y campos (ventanas) | Esquina de recuadros (páginas) | Esquina de botones redondeados (páginas) | Relleno vertical de filas de la lista de mazos | Degradado del fondo (día / noche) |
|---|---|---|---|---|---|---|---|---|---|
| Nocturne | Letra del sistema | 600 | −0,01 em | 1,5 | 6 px | 12 px | 16 px | 4 px | rgba(59,111,224,0,04) / rgba(99,144,255,0,07) |
| Papel | Georgia, Cambria, Noto Serif | 700 | 0 | 1,6 | 6 px | 12 px | 16 px | 5 px | rgba(31,106,128,0,035) / rgba(95,179,204,0,06) |
| Bosque | Letra del sistema | 600 | −0,01 em | 1,6 | 8 px | 16 px | 20 px | 6 px | rgba(15,118,110,0,04) / rgba(63,179,165,0,07) |
| Lavanda | Letra del sistema | 600 | −0,01 em | 1,55 | 6 px | 12 px | 16 px | 5 px | rgba(123,71,212,0,04) / rgba(159,111,243,0,07) |
| Atardecer | Letra del sistema | 600 | −0,01 em | 1,6 | 8 px | 16 px | 20 px | 5 px | rgba(132,87,39,0,045) / rgba(236,179,118,0,06) |

- El degradado es un velo muy tenue en la esquina superior derecha del fondo de las páginas.
- Dos familias de esquinas, separadas un 33 %: suaves (6 y 12 px: Nocturne, Papel y Lavanda) y
  redondeadas (8 y 16 px: Bosque y Atardecer). Regla: los recuadros llevan el doble que botones y
  campos. Casillas: 4 px siempre (para no parecer botones de opción, que son redondos). Los botones de
  las ventanas no pasan de 9 px: con más, el sistema los dibuja cuadrados.
- Contorno de foco: 2 px en todas.
- Colores con significado: Nocturne y Papel de día usan los de siempre; Bosque y Papel de noche giran
  el azul hacia azul petróleo, el rojo hacia rojo ladrillo y el verde hacia verde musgo; Lavanda y
  Atardecer usan los de Nocturne (en Lavanda de noche, bandera roja y verde ajustadas para
  daltonismo). «Aprendiendo» va en el rojo de la paleta en las cinco.
- El cobre de Atardecer se parece en matiz al naranja de «Difícil», pero es mucho más oscuro y está a
  31° del rojo de «Aprendiendo».

Las tablas completas de color de cada paleta están en el apartado 14.

## 7. Barra de título (solo Windows 11)

Cada paleta tiñe la barra de título de las ventanas, del matiz de su fondo y con algo más de color:
más oscura que la ventana de noche y algo más clara de día. Título en el color del texto; en las
ventanas que no están delante, en el texto secundario. Los botones de minimizar, maximizar y cerrar
siguen el modo de Anki. Cada ventana se tiñe antes de aparecer (no se ve primero blanca). La
diferencia con la ventana es pequeña (1,03 a 1,08 a 1): la separa el borde suave; el matiz la
identifica. En Windows 10, macOS y Linux la barra queda como siempre.

| Paleta | Barra de día | Barra de noche |
|---|---|---|
| Nocturne | #FAFBFE | #070C16 |
| Papel | #FFFCF7 | #070F12 |
| Bosque | #F8FEFA | #08100C |
| Lavanda | #FBFAFE | #0C0716 |
| Atardecer | #FFFBF9 | #160D07 |

## 8. Retoques que aplica en todo Anki (todas las paletas)

Texto y jerarquía:

- Tres niveles de texto: principal, secundario y menos importante, todos legibles sobre cualquier
  fondo; el desactivado, más apagado a propósito.
- Lista de mazos: cabeceras de columna (Mazo, Nuevas, Aprendiendo…) en texto secundario y algo menos
  gruesas; rótulos alineados con sus cifras y separados 24 px; «Mazo» empieza donde los nombres. La
  línea «Estudiadas N tarjetas en…» en texto secundario.
- Pantalla de un mazo: las etiquetas «Nuevas:», «Aprendiendo:» y «A repasar:» en texto secundario,
  para que destaquen las cifras.
- Cifras de igual ancho, alineadas en columna, en lista de mazos, pantalla de un mazo y tablas.
- Descripción de un mazo: líneas de unos 70 caracteres como mucho; la última nunca con una sola
  palabra. Títulos de varias líneas equilibrados.
- Letra de las páginas: la de interfaz del sistema (Segoe UI Variable o Segoe UI en Windows), con la
  que Anki elige para el idioma como reserva (japonés, chino…). No cambia el tamaño de letra (manda el
  de Anki) ni la letra de las ventanas.

Materiales:

- La tabla de la lista de mazos tiene el fondo de los recuadros (CANVAS_ELEVATED), el mismo que las
  tarjetas de GritMap: un solo material para todo lo que va sobre el fondo.
- Ayudas emergentes con el mismo fondo, borde suave y margen que los menús.
- De noche, lo que está más arriba es más claro (campos hundidos < fondo < recuadros < botones < menús
  < botón con el ratón encima).
- De noche, los colores con significado son algo menos saturados.

Controles:

- Dos tonos de acción: relleno (botones principales, con texto blanco) y trazo (foco, anillo del botón
  principal, raya de la pestaña activa, bordes de casillas con el ratón o el foco). De día casi
  coinciden; de noche el de trazo es más claro (3 a 1 o más sobre cualquier fondo; 4,3 sobre el de la
  ventana). Los enlaces tienen color propio, legible a 5 a 1 o más.
- Botón principal de las ventanas (el que responde a Intro en la fila de abajo): relleno del color de
  acción con texto blanco; con el ratón o el foco, más oscuro y con anillo; al pulsarlo, más oscuro
  aún; desactivado, como un botón normal apagado. El relleno sigue al botón que respondería a Intro al
  moverse con Tab por esa fila. Un botón del cuerpo de la ventana nunca se rellena.
- Pestañas (por ejemplo, Preferencias): la activa lleva el tinte de acción, el texto normal y una raya
  de 2 px abajo en el tono de trazo. Mismo tamaño que las demás; la letra no cambia de grosor.
- Campos de texto, numéricos y listas desplegables: borde fino visible (el de las casillas); con el
  foco, del color de acción.
- Casillas y botones de opción: borde visible sin marcar; con el ratón o el foco, borde del color de
  acción; marcada, rellena del color de acción con la marca en blanco.
- Flechas de desplegables, campos numéricos y orden de columnas, en texto secundario.
- Menús y desplegables: la opción con el ratón o el teclado encima lleva el tinte de acción y el texto
  normal (no el relleno azul con texto blanco de Anki).
- Interruptor «Tarjetas/Notas» de Explorar: «Tarjetas» en el color de acción; «Notas» sigue en verde.
- Editor: nombres de los campos en texto secundario; lo escrito, en color de texto.

Lista de mazos y navegación:

- Fila del mazo actual y fila con el ratón encima: tinte del color de acción, con la esquina de los
  botones. Solo filas de mazos.
- Explorar: filas seleccionadas con fondo opaco del tono de acción, texto a 5 a 1 o más; una fila con
  bandera seleccionada se ve del color de la selección.
- Barra superior: al pasar el ratón, fondo suave con las esquinas de la paleta (no subrayado); en
  seminegrita. No cambia de tamaño ni de sitio.
- Botones de la barra inferior de la lista de mazos y de la pantalla de un mazo: esquina de botones
  (6 u 8 px), en vez de medias píldoras.
- La fila vacía bajo la cabecera de la lista de mazos (donde se suelta un mazo para sacarlo al nivel
  superior) mide 10 px.

Repaso:

- «Editar» y «Más», sin fondo ni borde (borde transparente, no cambian de tamaño); fondo suave al
  pasar el ratón. Así los botones de respuesta son lo único con forma de botón.
- Botones de respuesta: una raya fina de color al pie de «Otra vez» (rojo), «Difícil» (naranja),
  «Bien» (verde) y «Fácil» (azul); el texto no cambia.
- Intervalos encima de los botones («10 min», «4 d») en texto secundario y con cifras de igual ancho.
- «Comenzar a estudiar» relleno del color de acción con texto blanco (lo hace Anki con el azul de la
  paleta).

Banderas:

- Conservan el color de su nombre; la roja y la verde se distinguen además por claridad (al menos 1,4
  veces, también simulando deuteranopía y protanopía). En Nocturne, la rosa es rosa de verdad (tono
  310°).

## 9. Movimiento

- Cambios de color al pasar el ratón por las páginas: 100 ms (Anki trae 180).
- El fundido de las tarjetas de Anki no cambia.
- Con «Reducir movimiento» en las preferencias de Anki o en el sistema («Efectos de animación»
  desactivados en Windows), los cambios son inmediatos.
- En el panel, al recorrer las paletas con las flechas, se aplica cuando la elección lleva 200 ms
  quieta, para no repintar Anki a cada paso.
- Sin parpadeos: la paleta se aplica antes de dibujar cada página (sin fogonazo claro de noche). Al
  cambiar de paleta, ventanas y páginas cambian una sola vez sin recargarse y se conserva lo que se
  esté escribiendo en el editor.

## 10. Accesibilidad

- Contraste medido en cada entrega, en las cinco paletas, de día y de noche:
  - todo texto, 4,5 a 1 o más sobre cualquier fondo, también sobre el resaltado de fila;
  - texto blanco sobre los botones de acción, 4,5 a 1 en todos sus estados;
  - casillas sin marcar, bordes de campos, banderas y rayas de los botones de respuesta, 3 a 1;
  - trazos de acción (foco, anillo, enlaces), 3 a 1 sobre cualquier fondo;
  - filas de Explorar con bandera o estado, 4,5; seleccionadas, 5;
  - de noche, el texto principal como mucho a 13,5 a 1 (en Nocturne y Papel, 13) para no deslumbrar;
  - APCA: texto principal 75, secundario 60, menos importante 45; desactivado 30.
- Daltonismo: bandera roja y verde distinguibles por claridad (simulación de Machado, 2009).
- Foco visible: contorno de 2 px del color de acción en la barra superior, en los enlaces (nombre de
  cada mazo, engranaje) y en los botones de la lista de mazos, de la pantalla de un mazo y del repaso,
  que Anki oculta de serie. No ocupa sitio. «Comenzar a estudiar» lo muestra desde el principio
  (indica que Intro empieza el estudio). El subrayado de los enlaces va algo separado de las letras.
- Teclado en el panel: el tabulador entra en la paleta elegida; las flechas (las cuatro) pasan a la
  siguiente y la eligen, en bucle; la barra espaciadora elige la que tiene el foco; Ctrl+Intro acepta;
  Esc cancela.
- Lector de pantalla: la lista es un grupo de botones de opción llamado «Paleta»; cada opción se lee
  por su nombre, con la descripción como información adicional; las miniaturas no se leen.
- Alto contraste del sistema (temas de contraste de Windows 11, «Aumentar contraste» de macOS, alto
  contraste de GNOME): Atelier no pinta nada (ni ventanas, ni páginas, ni barra de título) y deja el
  contraste máximo del sistema. Se comprueba al abrir Anki. Con los temas de contraste de Windows, el
  panel usa los colores del sistema salvo las miniaturas.
- Movimiento reducido respetado (apartado 9).
- El tamaño de letra lo decide la persona en Anki; Atelier no lo cambia.

## 11. Qué guarda

- El nombre de la paleta y que ya salieron los dos avisos de bienvenida, en la configuración de
  complementos de este ordenador (vale para todos los perfiles; no se sincroniza).
- Unos archivos de dibujo muy pequeños con las flechas y la marca de las casillas en los colores de la
  paleta, en la carpeta de datos del complemento.
- Una configuración ausente, antigua o con una paleta que ya no existe vuelve a Nocturne sin avisar.

## 12. Si algo falla

Nunca abre la ventana de error de Anki ni interrumpe un repaso: la parte afectada conserva el aspecto
normal de Anki y el detalle va al registro. El panel lo dice con su franja de aviso. Si Windows no
acepta el color de la barra de título, queda como siempre.

## 13. Decisiones tomadas a propósito (no «corregir» sin preguntar)

- «Aprendiendo» en rojo, no naranja (el naranja es de «Difícil»).
- Bordes de listas, tablas y separadores muy suaves (parte del aspecto original; reforzarlos se
  descartó por perder atractivo). Los campos, en cambio, sí llevan borde visible.
- De noche, banderas algo menos vivas, para que el texto de Explorar se lea bien.
- Borde azul (no gris oscuro) en casillas con el ratón o el foco.
- El fondo, el azul de acción y el tono de los colores con significado de Nocturne no cambian respecto
  a la versión original: es la identidad que la persona quiere conservar.
- No se cambia el tamaño de la letra.
- Solo se elige la paleta; no hay ajustes sueltos.
- Grafito y Alto contraste fueron paletas y se retiraron por decisión de la persona.
- Papel de noche usa azul petróleo con texto crema (no marrón); lo eligió la persona entre tres
  muestras.
- La ventana de paletas solo se abre desde Complementos > Configuración.
- El aviso «Paleta aplicada» se quitó: la vista previa ya lo enseña. El de bienvenida usa el aviso
  amarillo de Anki, una vez.
- De día, la barra de título solo es un poco más clara que la ventana: el fondo ya es casi blanco.
- Pendiente de comprobar: de noche se midió el texto de los campos del editor en blanco puro (14,8 a
  1), por encima del techo; probablemente viene del estilo de la plantilla de la nota, no de Atelier.

## 14. Tablas completas de color de cada paleta

Mismos nombres de color que la paleta Nocturne de `00-contexto-comun.md`.

### Atardecer

|Color|Día|Noche|
|-|-|-|
|ACCENT_CARD|#186CB9|#7EBFF4|
|ACCENT_DANGER|#CA2D2D|#F37777|
|ACCENT_NOTE|#257A35|#57D06B|
|BORDER|#EFDED2|#44362C|
|BORDER_FOCUS|#7C5225|#ECB376|
|BORDER_STRONG|#E0C5B3|#5C493D|
|BORDER_SUBTLE|#F5EAE3|#35281F|
|BUTTON_BG|#FFFCFA|#3A2D24|
|BUTTON_DISABLED|#FEFCFB80|#3A2D2480|
|BUTTON_HOVER|#F9F0E9|#47382E|
|BUTTON_HOVER_BORDER|#E0C5B3|#5C493D|
|BUTTON_PRIMARY_BG|#845727|#8F5D27|
|BUTTON_PRIMARY_DISABLED|#84572759|#8F5D2759|
|BUTTON_PRIMARY_GRADIENT_END|#624424|#654727|
|BUTTON_PRIMARY_GRADIENT_START|#845727|#8F5D27|
|CANVAS|#FCF8F5|#1F1712|
|CANVAS_CODE|#FAF3EF|#241A14|
|CANVAS_ELEVATED|#FFFCFA|#362921|
|CANVAS_GLASS|#FFFCFACC|#362921CC|
|CANVAS_INSET|#F8F0EA|#1B140F|
|CANVAS_OVERLAY|#FFFCFA|#403229|
|FG|#261C15|#E1DAD6|
|FG_DISABLED|#BCB1A9|#9A887C|
|FG_FAINT|#76685E|#B4A49A|
|FG_LINK|#6A4822|#ECCEAE|
|FG_SUBTLE|#6A594E|#CCBFB7|
|FLAG_1|#BE1D1D|#C12D2D|
|FLAG_2|#E8590C|#C07F3A|
|FLAG_3|#2F9E44|#4DA05B|
|FLAG_4|#1971C2|#5993C2|
|FLAG_5|#C62FAD|#B378C1|
|FLAG_6|#099268|#439C81|
|FLAG_7|#7048E8|#9680D6|
|HIGHLIGHT_BG|#845727|#8F5D27|
|HIGHLIGHT_FG|#FFFFFF|#FFFFFF|
|NOCTURNE_CONTROL_BORDER|#968B85|#8C7C72|
|NOCTURNE_PRIMARY_PRESSED|#48321A|#49331C|
|NOCTURNE_PRIMARY_RING|#21160B|#F4D5B4|
|NOCTURNE_ROW_HIGHLIGHT|#F6F1EC|#3A2C1E|
|NOCTURNE_TITLEBAR|#FFFBF9|#160D07|
|NOCTURNE_TABLE_SELECTED|#E1BF9C|#6F5438|
|SCROLLBAR_BG|#E2DAD5|#3F3127|
|SCROLLBAR_BG_ACTIVE|#C0B3AA|#5C493D|
|SCROLLBAR_BG_HOVER|#D3C8C0|#504035|
|SELECTED_BG|#CB905038|#ECB37640|
|SELECTED_FG|#261C15|#E1DAD6|
|SHADOW|#30231B26|#0F090566|
|SHADOW_FOCUS|#7C522540|#ECB3764D|
|SHADOW_INSET|#30231B1A|#0F09054D|
|SHADOW_SUBTLE|#30231B12|#0F090533|
|STATE_BURIED|#9A7B3F|#A98754|
|STATE_LEARN|#CA2D2D|#F37777|
|STATE_MARKED|#7048E8|#9680D6|
|STATE_NEW|#186CB9|#7EBFF4|
|STATE_REVIEW|#257A35|#57D06B|
|STATE_SUSPENDED|#968C86|#9C8E84|

### Bosque

|Color|Día|Noche|
|-|-|-|
|ACCENT_CARD|#246F9B|#89C5E8|
|ACCENT_DANGER|#BA3F2C|#D78174|
|ACCENT_NOTE|#1C7929|#41C853|
|BORDER|#CED9D1|#2A362D|
|BORDER_FOCUS|#0F766E|#3FB3A5|
|BORDER_STRONG|#B1C0B5|#3B4A3F|
|BORDER_SUBTLE|#DEE6E0|#1E2821|
|BUTTON_BG|#F9FCFA|#1F2922|
|BUTTON_DISABLED|#F9FCFA80|#1F292280|
|BUTTON_HOVER|#E6EDE7|#2D3931|
|BUTTON_HOVER_BORDER|#B1C0B5|#3B4A3F|
|BUTTON_PRIMARY_BG|#0F766E|#0E7068|
|BUTTON_PRIMARY_DISABLED|#0F766E59|#0E706859|
|BUTTON_PRIMARY_GRADIENT_END|#0D635C|#0C5F58|
|BUTTON_PRIMARY_GRADIENT_START|#0F766E|#0E7068|
|CANVAS|#F3F7F4|#111814|
|CANVAS_CODE|#EEF3EF|#141C17|
|CANVAS_ELEVATED|#F9FCFA|#1B241E|
|CANVAS_GLASS|#F9FCFACC|#1B241ECC|
|CANVAS_INSET|#E9EFEA|#0D130F|
|CANVAS_OVERLAY|#F9FCFA|#26312A|
|FG|#17251C|#D5E0D8|
|FG_DISABLED|#A2AFA6|#778A7C|
|FG_FAINT|#5E6E63|#98A99E|
|FG_LINK|#0D6B64|#7FD0C3|
|FG_SUBTLE|#45554A|#B0BEB4|
|FLAG_1|#B23C2A|#B74635|
|FLAG_2|#C17C2D|#C48339|
|FLAG_3|#26A136|#31A741|
|FLAG_4|#3094CE|#4699C9|
|FLAG_5|#D756D7|#D366D3|
|FLAG_6|#259C8C|#2FA192|
|FLAG_7|#9F6FDD|#A67EDA|
|HIGHLIGHT_BG|#0F766E|#0E7068|
|HIGHLIGHT_FG|#FFFFFF|#FFFFFF|
|SCROLLBAR_BG|#CCD7CF|#28332B|
|SCROLLBAR_BG_ACTIVE|#98A99D|#3B4A3F|
|SCROLLBAR_BG_HOVER|#B1C0B5|#35423A|
|SELECTED_BG|#0F766E33|#3FB3A540|
|SELECTED_FG|#17251C|#D5E0D8|
|SHADOW|#17251C26|#05080666|
|SHADOW_FOCUS|#0F766E40|#3FB3A54D|
|SHADOW_INSET|#17251C1A|#0508064D|
|SHADOW_SUBTLE|#17251C12|#05080633|
|STATE_BURIED|#BC802C|#855E27|
|STATE_LEARN|#BA3F2C|#D78174|
|STATE_MARKED|#7583DF|#5D6DD0|
|STATE_NEW|#246F9B|#89C5E8|
|STATE_REVIEW|#1C7929|#32AD42|
|STATE_SUSPENDED|#A98828|#AC8D32|
|NOCTURNE_CONTROL_BORDER|#7E8C82|#6F8075|
|NOCTURNE_ROW_HIGHLIGHT|#E3EEEB|#112521|
|NOCTURNE_PRIMARY_PRESSED|#0A524C|#0A4F4A|
|NOCTURNE_PRIMARY_RING|#063A36|#7FD6C9|
|NOCTURNE_TITLEBAR|#F8FEFA|#08100C|
|NOCTURNE_TABLE_SELECTED|#81B6B0|#27635B|

### Lavanda

|Color|Día|Noche|
|-|-|-|
|ACCENT_CARD|#186CB9|#7EBFF4|
|ACCENT_DANGER|#CA2D2D|#F37777|
|ACCENT_NOTE|#257A35|#57D06B|
|BORDER|#DFDAE7|#352C44|
|BORDER_FOCUS|#7B47D4|#9F6FF3|
|BORDER_STRONG|#C7C0D3|#483D5C|
|BORDER_SUBTLE|#EBE8F0|#271F35|
|BUTTON_BG|#FCFBFE|#2C243A|
|BUTTON_DISABLED|#FCFBFE80|#2C243A80|
|BUTTON_HOVER|#F0EDF5|#372E47|
|BUTTON_HOVER_BORDER|#C7C0D3|#483D5C|
|BUTTON_PRIMARY_BG|#7B47D4|#804CDA|
|BUTTON_PRIMARY_DISABLED|#7B47D459|#804CDA59|
|BUTTON_PRIMARY_GRADIENT_END|#6A3ABC|#6D3FBD|
|BUTTON_PRIMARY_GRADIENT_START|#7B47D4|#804CDA|
|CANVAS|#F8F7FA|#17121F|
|CANVAS_CODE|#F4F2F7|#1A1424|
|CANVAS_ELEVATED|#FCFBFE|#292136|
|CANVAS_GLASS|#FCFBFECC|#292136CC|
|CANVAS_INSET|#F0EEF4|#130F1B|
|CANVAS_OVERLAY|#FCFBFE|#312940|
|FG|#231B30|#DAD6E1|
|FG_DISABLED|#B0A9BC|#8A7F9D|
|FG_FAINT|#6D647D|#A49AB4|
|FG_LINK|#703CCB|#C9B2F2|
|FG_SUBTLE|#584E6A|#BFB7CC|
|FLAG_1|#BE1D1D|#B43C3C|
|FLAG_2|#E8590C|#C07F3A|
|FLAG_3|#2F9E44|#4C9E5A|
|FLAG_4|#1971C2|#5993C2|
|FLAG_5|#C62FAD|#B378C1|
|FLAG_6|#099268|#439C81|
|FLAG_7|#7048E8|#9680D6|
|HIGHLIGHT_BG|#7B47D4|#804CDA|
|HIGHLIGHT_FG|#FFFFFF|#FFFFFF|
|NOCTURNE_CONTROL_BORDER|#8D8797|#7C728C|
|NOCTURNE_PRIMARY_PRESSED|#5A32A0|#5C35A0|
|NOCTURNE_PRIMARY_RING|#472482|#CAAFF9|
|NOCTURNE_ROW_HIGHLIGHT|#EFEBF7|#281C3C|
|NOCTURNE_TITLEBAR|#FBFAFE|#0C0716|
|NOCTURNE_TABLE_SELECTED|#B598E5|#654799|
|SCROLLBAR_BG|#DAD5E2|#30273F|
|SCROLLBAR_BG_ACTIVE|#B2AAC0|#483D5C|
|SCROLLBAR_BG_HOVER|#C7C0D3|#3F3550|
|SELECTED_BG|#7B47D438|#9F6FF340|
|SELECTED_FG|#231B30|#DAD6E1|
|SHADOW|#231B3026|#09050F66|
|SHADOW_FOCUS|#7B47D440|#9F6FF34D|
|SHADOW_INSET|#231B301A|#09050F4D|
|SHADOW_SUBTLE|#231B3012|#09050F33|
|STATE_BURIED|#9A7B3F|#A98754|
|STATE_LEARN|#CA2D2D|#F37777|
|STATE_MARKED|#7048E8|#9680D6|
|STATE_NEW|#186CB9|#7EBFF4|
|STATE_REVIEW|#257A35|#57D06B|
|STATE_SUSPENDED|#8C8696|#8D849C|

### Nocturne

|Color|Día|Noche|
|-|-|-|
|ACCENT_CARD|#186CB9|#7EBFF4|
|ACCENT_DANGER|#CA2D2D|#F37777|
|ACCENT_NOTE|#257A35|#57D06B|
|BORDER|#DADEE7|#2C3444|
|BORDER_FOCUS|#3B6FE0|#6390FF|
|BORDER_STRONG|#C0C6D3|#3D475C|
|BORDER_SUBTLE|#E8EAF0|#1F2635|
|BUTTON_BG|#FBFCFE|#242C3A|
|BUTTON_DISABLED|#FBFCFE80|#242C3A80|
|BUTTON_HOVER|#EDF0F5|#2E3747|
|BUTTON_HOVER_BORDER|#C0C6D3|#3D475C|
|BUTTON_PRIMARY_BG|#3B6FE0|#4066E6|
|BUTTON_PRIMARY_DISABLED|#3B6FE059|#4066E659|
|BUTTON_PRIMARY_GRADIENT_END|#2F5BC7|#3452C8|
|BUTTON_PRIMARY_GRADIENT_START|#3B6FE0|#4066E6|
|CANVAS|#F7F8FA|#12161F|
|CANVAS_CODE|#F2F4F7|#141924|
|CANVAS_ELEVATED|#FBFCFE|#212836|
|CANVAS_GLASS|#FBFCFECC|#212836CC|
|CANVAS_INSET|#EEF0F4|#0F131B|
|CANVAS_OVERLAY|#FBFCFE|#293040|
|FG|#1B2430|#D6DAE1|
|FG_DISABLED|#A9AFBC|#7C869A|
|FG_FAINT|#646C7D|#9AA3B4|
|FG_LINK|#2F63D8|#A3C1F7|
|FG_SUBTLE|#4E576A|#B7BECC|
|FLAG_1|#BE1D1D|#C12D2D|
|FLAG_2|#E8590C|#C07F3A|
|FLAG_3|#2F9E44|#4DA05B|
|FLAG_4|#1971C2|#5993C2|
|FLAG_5|#C62FAD|#B378C1|
|FLAG_6|#099268|#439C81|
|FLAG_7|#7048E8|#9680D6|
|HIGHLIGHT_BG|#3B6FE0|#4066E6|
|HIGHLIGHT_FG|#FFFFFF|#FFFFFF|
|SCROLLBAR_BG|#D5D9E2|#272F3F|
|SCROLLBAR_BG_ACTIVE|#AAB1C0|#3D475C|
|SCROLLBAR_BG_HOVER|#C0C6D3|#353E50|
|SELECTED_BG|#3B6FE038|#6390FF40|
|SELECTED_FG|#1B2430|#D6DAE1|
|SHADOW|#1B243026|#05080F66|
|SHADOW_FOCUS|#3B6FE040|#6390FF4D|
|SHADOW_INSET|#1B24301A|#05080F4D|
|SHADOW_SUBTLE|#1B243012|#05080F33|
|STATE_BURIED|#9A7B3F|#A98754|
|STATE_LEARN|#CA2D2D|#F37777|
|STATE_MARKED|#7048E8|#9680D6|
|STATE_NEW|#186CB9|#7EBFF4|
|STATE_REVIEW|#257A35|#57D06B|
|STATE_SUSPENDED|#868E96|#848E9C|
|NOCTURNE_CONTROL_BORDER|#878C97|#727B8C|
|NOCTURNE_ROW_HIGHLIGHT|#EAEEF8|#19233F|
|NOCTURNE_PRIMARY_PRESSED|#284EAA|#2B45AA|
|NOCTURNE_PRIMARY_RING|#1C3A8A|#A9C4FF|
|NOCTURNE_TITLEBAR|#FAFBFE|#070C16|
|NOCTURNE_TABLE_SELECTED|#92AEEB|#3D5696|

### Papel

|Color|Día|Noche|
|-|-|-|
|ACCENT_CARD|#2269C1|#89C5E8|
|ACCENT_DANGER|#CD2424|#D78174|
|ACCENT_NOTE|#15793A|#41C853|
|BORDER|#DFD6C6|#24323A|
|BORDER_FOCUS|#1F6A80|#5FB6CE|
|BORDER_STRONG|#C9BEAA|#34454F|
|BORDER_SUBTLE|#ECE5D8|#19242A|
|BUTTON_BG|#FEFCF8|#1C2930|
|BUTTON_DISABLED|#FEFCF880|#1C293080|
|BUTTON_HOVER|#F0EADF|#28363F|
|BUTTON_HOVER_BORDER|#C9BEAA|#34454F|
|BUTTON_PRIMARY_BG|#1F6A80|#1F6E85|
|BUTTON_PRIMARY_DISABLED|#1F6A8059|#1F6E8559|
|BUTTON_PRIMARY_GRADIENT_END|#1A5A6D|#1A5E72|
|BUTTON_PRIMARY_GRADIENT_START|#1F6A80|#1F6E85|
|CANVAS|#FAF7F1|#10171A|
|CANVAS_CODE|#F4F0E8|#121A1E|
|CANVAS_ELEVATED|#FEFCF8|#18232A|
|CANVAS_GLASS|#FEFCF8CC|#18232ACC|
|CANVAS_INSET|#F1ECE2|#0C1215|
|CANVAS_OVERLAY|#FEFCF8|#223139|
|FG|#2A2520|#E3DAC9|
|FG_DISABLED|#B0A796|#718893|
|FG_FAINT|#6E6557|#ABA496|
|FG_LINK|#1B6378|#8FCDE0|
|FG_SUBTLE|#544C40|#C4BBAB|
|FLAG_1|#C02121|#B34534|
|FLAG_2|#D47425|#C08138|
|FLAG_3|#1EA24E|#30A43F|
|FLAG_4|#5187E0|#4196C8|
|FLAG_5|#D05CE2|#D263D2|
|FLAG_6|#209D8E|#2E9F90|
|FLAG_7|#A868E4|#A47BD9|
|HIGHLIGHT_BG|#1F6A80|#1F6E85|
|HIGHLIGHT_FG|#FFFFFF|#FFFFFF|
|SCROLLBAR_BG|#DED5C5|#1F2C33|
|SCROLLBAR_BG_ACTIVE|#B2A68F|#34454F|
|SCROLLBAR_BG_HOVER|#C9BEAA|#2B3B44|
|SELECTED_BG|#1F6A8033|#5FB6CE40|
|SELECTED_FG|#2A2520|#E3DAC9|
|SHADOW|#2A252026|#04070866|
|SHADOW_FOCUS|#1F6A8040|#5FB6CE4D|
|SHADOW_INSET|#2A25201A|#0407084D|
|SHADOW_SUBTLE|#2A252012|#04070833|
|STATE_BURIED|#BB8221|#855E27|
|STATE_LEARN|#CD2424|#D78174|
|STATE_MARKED|#6F71E6|#5D6DD0|
|STATE_NEW|#2565CF|#89C5E8|
|STATE_REVIEW|#15793A|#32AE43|
|STATE_SUSPENDED|#A68B1D|#AA8C31|
|NOCTURNE_CONTROL_BORDER|#8E8574|#71858F|
|NOCTURNE_ROW_HIGHLIGHT|#EBEDE9|#13272D|
|NOCTURNE_PRIMARY_PRESSED|#154B5B|#164F60|
|NOCTURNE_PRIMARY_RING|#0E3440|#9FD6E4|
|NOCTURNE_TITLEBAR|#FFFCF7|#070F12|
|NOCTURNE_TABLE_SELECTED|#8CAFB5|#335F6C|

