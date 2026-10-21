# Qué hace «Nocturne»

Versión 3.1.0 · 2026-10-21

Temas de color para Anki, en modo día y en modo noche. Trae cinco paletas (Nocturne, Papel, Grafito,
Bosque y Alto contraste), y Nocturne está elegida de serie. Cada paleta es un estilo completo:
colores, letra de los títulos, esquinas, botones, separación de las filas de la lista de mazos,
resaltados y banderas. La paleta se elige en una ventana propia y se aplica al momento, sin
reiniciar. No toca su colección, sus tarjetas ni sus plantillas.

La paleta Nocturne conserva el aspecto de la original que usted subió al taller (la del 28 de julio de
2026). Las decisiones se apoyan en los resúmenes de docs/referencias: sobre todo «Refactoring UI»,
«Practical UI», Tufte y el vídeo de tipografía de Tim Gabe, y en menor medida Webflow, Orbix y
Weinschenk. La versión 2.0.0, hecha en otra copia del taller, se descartó el 2026-10-21 y no está aquí.

## 1. Dónde aparece

- Menú Herramientas > «Paletas de Nocturne…»: abre la ventana para elegir paleta.
- Herramientas > «Complementos», con Nocturne seleccionado, botón «Configuración»: abre la misma
  ventana, no el editor de texto que Anki muestra con otros complementos.
- La paleta elegida se nota en todas las ventanas de Anki (la principal, Explorar, Añadir, Editar,
  Preferencias, menús, listas, tablas, casillas, botones, barras de desplazamiento y diálogos) y en sus
  páginas (lista de mazos, pantalla de un mazo, repaso alrededor de la tarjeta, editor, estadísticas,
  opciones de mazo y felicitación).
- No cambia el aspecto de las tarjetas, que decide su plantilla, ni toca páginas de internet que otro
  complemento abra dentro de Anki.

## 2. La ventana «Paletas de Nocturne»

- Arriba, el texto: «Elija el aspecto de Anki. Cada paleta trae sus colores de día y de noche, su letra
  para los títulos, sus esquinas, sus botones y sus resaltados. El cambio se aplica al momento.»
- Debajo, las cinco paletas, cada una con un botón de opción y una línea que la describe (textos en el
  apartado 3). Al abrirla, está marcada la paleta activa.
- Botones «Aceptar» y «Cancelar» (los nombres que pone Anki en su idioma). Con «Aceptar», si ha
  elegido otra paleta, se aplica al momento a todas las ventanas y páginas abiertas y aparece el aviso
  «Paleta «Papel» aplicada.» (con el nombre que corresponda). Si deja la misma, no hace nada.
  «Cancelar», Esc o la X la cierran sin cambiar nada.
- Recuerda su tamaño y su posición.
- Solo se elige la paleta: no hay ajustes sueltos. Así lo decidió el cliente (2026-10-21).

## 3. Las cinco paletas

Todas siguen el modo día o noche que usted elija en Anki y cambian con él. Los grises de cada una son de
una sola familia, y ninguno es blanco ni negro puro.

- Nocturne (de serie). Descripción en la ventana: «Serena: grises azulados y un azul de acción
  tranquilo. Esquinas suaves.». Fondo #F7F8FA de día y #12161F de noche; texto #1B2430 y #D6DAE1;
  azul de acción #3B6FE0 y #4066E6. Títulos en seminegrita con las letras un poco más juntas, esquinas
  de 6px en las ventanas, 12px en los recuadros de las páginas y 7px en los botones de las ventanas.
  Un degradado azul muy tenue en la esquina superior derecha del fondo de las páginas.
- Papel. «Cálida: fondo marfil, texto color tinta, acento azul petróleo y títulos con remates, como un
  libro. Pensada para leer mucho rato.». Fondo #FAF7F1 y #1A1714 (marrón muy oscuro de noche); texto
  #2A2520 y #E6DFD3; acento #1F6A80 y #1F6B82. Títulos de las páginas en Georgia (o Cambria), en
  negrita; descripciones con más espacio entre líneas; esquinas algo más redondeadas; filas de la lista
  de mazos un poco más holgadas; degradado azul petróleo muy tenue.
- Grafito. «Sobria: grises neutros, acento índigo, esquinas casi rectas y lista de mazos compacta.».
  Grises sin tinte (#F5F5F5 y #161616); texto #1C1C1C y #DCDCDC; acento índigo #4F46E5 y #5148D9.
  Esquinas de 2 a 4px, filas de la lista de mazos más juntas, títulos algo más ceñidos y sin degradado.
- Bosque. «Natural: verdes grisáceos, acento verde azulado, esquinas redondeadas y filas más
  holgadas.». Fondo #F3F7F4 y #111814; texto #17251C y #D5E0D8; acento #0F766E y #0E7068. Las esquinas
  más redondeadas de todas, las filas más holgadas y un degradado verde azulado muy tenue.
- Alto contraste. «Máxima legibilidad: texto casi negro o casi blanco, bordes marcados y foco del
  teclado más grueso. Para vista cansada o pantallas con reflejos.». Fondo #F9FAFB y #0E0F11; texto
  #0B0C0E y #F4F5F7; acento #1A44C2 y #1F49CC. Todo el texto llega a 7:1 o más; campos, listas y
  recuadros con borde bien visible; títulos en negrita; contorno del foco de 3px; sin degradado.

En Nocturne, «Aprendiendo» va en naranja; en las demás, en el rojo de Anki.

## 4. Lo que tienen todas

- Tres niveles de texto bien diferenciados: principal, secundario (más suave) y lo menos importante
  (más suave aún), todos legibles sobre cualquier fondo.
- De noche, lo que está «más arriba» es más claro: los campos hundidos son lo más oscuro, después el
  fondo, los recuadros, los botones, los menús desplegables y, por último, un botón con el ratón
  encima. Así los menús se distinguen de lo que tapan.
- De noche, los colores con significado (cifras, banderas, enlaces) son algo menos saturados, para que
  no «vibren» sobre el fondo oscuro.
- Botón principal de las ventanas (el que se pulsa con Intro, por ejemplo «Aceptar» o «Añadir»)
  relleno del color de acción, con texto blanco. Al pasar el ratón o llegar con el teclado se oscurece
  y lleva un anillo; al pulsarlo, se oscurece más. Si está desactivado, se ve como un botón normal
  apagado. Al moverse con Tab entre botones, el relleno sigue al botón que respondería a Intro.
- Esquinas de los botones y recuadros según la paleta.
- Casillas y botones de opción con un borde visible sin marcar; con el ratón encima o con el foco, el
  borde toma el color de acción.
- En la lista de mazos, la fila del mazo actual y la que tiene el ratón encima se resaltan con un tinte
  del color de acción. En Explorar, las filas seleccionadas llevan un tinte más visible que en Anki.
  El texto que se selecciona en las páginas toma ese mismo tinte.
- Banderas: conservan el color de su nombre (la roja es roja) y, además, la roja y la verde se
  distinguen por su claridad, para quien confunde el rojo y el verde. En Nocturne, la bandera rosa es
  ahora rosa de verdad: antes se confundía con la roja.
- En la lista de mazos, la pantalla de un mazo y las tablas de las páginas, todas las cifras tienen el
  mismo ancho y se alinean en columna.
- La descripción de un mazo tiene líneas de unos 70 caracteres como mucho.
- Al moverse con el teclado por los botones de la lista de mazos, de la pantalla de un mazo y del
  repaso, el botón con el foco lleva un contorno del color de acción. Anki lo oculta de serie.
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
- Si esa configuración falta, es antigua o tiene un valor que no existe, usa Nocturne sin avisar.

## 7. Si algo falla

- Ningún fallo abre la ventana de error ni interrumpe un repaso: Anki conserva su aspecto habitual en
  la parte afectada y el detalle queda en el registro propio del complemento.

## 8. Qué no hace

- No permite ajustar por separado colores, letra o esquinas: cada paleta va completa.
- No se conecta a internet ni descarga letras: usa las que ya trae el sistema (si falta Georgia, Papel
  usa Cambria u otra letra con remates).
- No cambia su colección, sus tarjetas ni el aspecto que tenga elegido con otro estilo de controles en
  Preferencias: con un estilo que no sea el de Anki, botones y casillas quedan como los dibuje el
  sistema.

## 9. Legibilidad medida (2026-10-21)

Contraste del texto frente al fondo; el mínimo recomendado para leer con comodidad es 4,5 (y 3 para
bordes de casillas e iconos). Lo comprueban las pruebas del taller en cada entrega, en las cinco
paletas, de día y de noche.

- Todo color que Anki usa como texto llega al menos a 4,5 sobre cualquier fondo, también sobre el
  resaltado de la fila; en Alto contraste, a 7.
- El texto blanco de los botones de acción llega a 4,5 en todos sus estados (7 en Alto contraste).
- Las casillas sin marcar llegan a 3 frente al fondo; las banderas, a 3 como icono.
- En Explorar, el texto de las filas con bandera o estado, y el de las filas seleccionadas, llega a 4,5.
- La bandera roja y la verde se diferencian en claridad al menos 1,4 veces.
- De noche, el texto principal queda como mucho en 13,5 frente al fondo, para no deslumbrar (en
  Nocturne, 13; la versión original llegaba a 15,4), salvo en Alto contraste, que busca lo contrario.
- Además se mide con APCA, un método más reciente que tiene en cuenta que el texto claro sobre fondo
  oscuro se percibe distinto: el texto principal llega al menos a 75, el secundario a 60 y el menos
  importante a 45 (mínimos que propone «Practical UI»); en Alto contraste, a 90, 75 y 60.
