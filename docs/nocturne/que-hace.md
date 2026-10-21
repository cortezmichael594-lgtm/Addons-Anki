# Qué hace «Nocturne»

Versión 3.0.0 · 2026-10-21

Tema de colores para Anki, en modo día y en modo noche: grises azulados con un único azul de acción
sereno. Se instala y se aplica solo; no tiene menú, ni ventana de opciones, ni ningún texto propio, así
que se ve igual con Anki en cualquier idioma. No toca su colección, sus tarjetas ni sus plantillas.

La versión 3.0.0 conserva el aspecto de la original que usted subió al taller (la del 28 de julio de
2026) y lo ordena como un sistema: una sola familia de grises azulados, tres niveles de texto, fondos
que de noche se aclaran cuanto más arriba están, foco del teclado visible y una tipografía más
cuidada. Se apoya en «Refactoring UI», «Practical UI» y el vídeo de tipografía de Tim Gabe. La versión
2.0.0, hecha en otra copia del taller, se descartó el 2026-10-21 y no está aquí.

## 1. Dónde se nota

- En todas las ventanas de Anki: la principal, Explorar, Añadir, Editar, Preferencias, menús, listas,
  tablas, casillas, barras de desplazamiento y diálogos.
- En las páginas de Anki: lista de mazos, pantalla de un mazo, repaso (alrededor de la tarjeta, no en
  ella), editor, estadísticas, opciones de mazo y la pantalla de felicitación.
- No cambia el aspecto de las tarjetas: su plantilla manda. Tampoco toca páginas de internet que otro
  complemento abra dentro de Anki.

## 2. Colores

- Todos los grises (fondos, bordes y textos) son de la misma familia azulada; ninguno es blanco ni
  negro puro.
- Fondo de día casi blanco, con un toque azulado (#F7F8FA); de noche, azul muy oscuro (#12161F).
- De noche, lo que está «más arriba» es más claro: los campos hundidos son lo más oscuro, después el
  fondo, los recuadros, los botones, los menús desplegables y, por último, un botón con el ratón
  encima. Así los menús se distinguen de lo que tapan.
- Tres niveles de texto bien diferenciados: principal, secundario (más suave) y lo menos importante
  (más suave aún), todos legibles sobre cualquier fondo.
- Texto principal de día gris pizarra muy oscuro (#1B2430); de noche, gris claro azulado (#D6DAE1),
  algo menos brillante que en la versión original para no deslumbrar en sesiones largas.
- Un único azul de acción para botones principales, selección y foco (#3B6FE0 de día, #4066E6 de noche).
- Bordes muy suaves en campos, listas, tablas y separadores, que dan un aspecto limpio y ligero.
- Las casillas y los botones de opción tienen un borde gris visible, para distinguirlas sin marcar; con
  el ratón encima o al llegar con el teclado, el borde se vuelve azul.
- Colores de las cifras de la lista de mazos: Nuevas en azul, Aprendiendo en naranja (Anki usa rojo) y
  Para repasar en verde. De día son algo más oscuros que en la versión original, para leerse bien.
- Las banderas siguen la familia de colores de Anki, en tonos propios. De noche son algo menos vivas
  que en la versión original: Anki pinta con ellas, oscurecidas, las filas de Explorar, y así el texto
  de esas filas se lee bien.
- El botón azul principal mantiene su azul al pasar el ratón por encima, en lugar de aclararse, para
  que su texto blanco se siga leyendo bien.
- Sigue al modo día o noche que usted elija en Anki y cambia con él.

## 3. Acabado

- Letra de interfaz del sistema (en Windows, Segoe UI Variable o Segoe UI) en las páginas de Anki, con
  la letra que Anki elige para su idioma como reserva (por ejemplo, para japonés o chino).
- En la lista de mazos, la pantalla de un mazo y las tablas de las páginas, todas las cifras tienen el
  mismo ancho, de modo que se alinean en columna (1204 y 41 ocupan lo que les corresponde).
- Los títulos de las páginas (por ejemplo, los de cada gráfico de las estadísticas) van en seminegrita
  y con las letras un poco más juntas.
- La descripción de un mazo tiene más espacio entre líneas y líneas de unos 70 caracteres como mucho.
- Al moverse con el teclado (tecla Tab) por los botones de la lista de mazos, de la pantalla de un mazo
  y del repaso, el botón que tiene el foco lleva un contorno azul. Anki lo oculta de serie.
- No cambia el tamaño de la letra: manda el que usted tenga elegido en Anki.
- Un degradado azul muy tenue, fijo en la esquina superior derecha del fondo de las páginas (algo más
  visible de noche).

## 4. Sin parpadeos

- Aplica los colores antes de que se dibuje cada página, también en estadísticas y felicitación, para
  que no haya un fogonazo claro al abrirlas de noche.
- Al cambiar de perfil vuelve a afirmar los colores sin redibujar las ventanas.

## 5. Si algo falla

- Ningún fallo abre la ventana de error ni interrumpe un repaso: Anki conserva su aspecto habitual en
  la parte afectada y el detalle queda en el registro propio del complemento.

## 6. Qué no hace

- No tiene opciones: no se pueden cambiar los colores desde Anki.
- No guarda nada, no se conecta a internet y no cambia su colección.

## 7. Legibilidad medida (2026-10-21)

Contraste del texto frente al fondo; el mínimo recomendado para leer con comodidad es 4,5 (y 3 para
bordes de casillas e iconos). Lo comprueban las pruebas del taller en cada entrega.

- Todo color que Anki usa como texto llega al menos a 4,5 sobre cualquier fondo, de día y de noche.
- El texto blanco del botón azul llega a 4,5 en todos sus estados.
- Las casillas sin marcar llegan a 3 frente al fondo; las banderas, a 3 como icono.
- En Explorar, el texto de las filas con bandera o estado llega a 4,5, de día y de noche.
- De noche, el texto principal queda en 13 frente al fondo (la versión original llegaba a 15,4), y
  al menos en 8,5 sobre cualquier superficie, incluidos los botones.
- Además se mide con APCA, un método más reciente que tiene en cuenta que el texto claro sobre fondo
  oscuro se percibe distinto: el texto principal llega al menos a 75, el secundario a 60 y el menos
  importante a 45 (mínimos que propone «Practical UI»).
