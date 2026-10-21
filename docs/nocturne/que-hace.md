# Qué hace «Nocturne»

Versión 2026.07.28 · 2026-10-21

Tema de colores para Anki, en modo día y en modo noche: grises azulados con un único azul de acción
sereno. Se instala y se aplica solo; no tiene menú, ni ventana de opciones, ni ningún texto propio, así
que se ve igual con Anki en cualquier idioma. No toca su colección, sus tarjetas ni sus plantillas.

Este documento describe la versión original que usted subió al taller (la del 28 de julio de 2026).
La versión 2.0.0, hecha en otra copia del taller, se descartó el 2026-10-21 y no está aquí.

## 1. Dónde se nota

- En todas las ventanas de Anki: la principal, Explorar, Añadir, Editar, Preferencias, menús, listas,
  tablas, casillas, barras de desplazamiento y diálogos.
- En las páginas de Anki: lista de mazos, pantalla de un mazo, repaso (alrededor de la tarjeta, no en
  ella), editor, estadísticas, opciones de mazo y la pantalla de felicitación.
- No cambia el aspecto de las tarjetas: su plantilla manda. Tampoco toca páginas de internet que otro
  complemento abra dentro de Anki.

## 2. Colores

- Fondo de día casi blanco, con un toque azulado (#F7F8FA); de noche, azul muy oscuro (#12161F).
- Texto principal de día gris pizarra muy oscuro (#1B2430); de noche, blanco roto azulado (#E9EDF4).
- Un único azul de acción para botones principales, selección y foco (#3B6FE0 de día, #4066E6 de noche).
- Bordes muy suaves, casi invisibles, que dan un aspecto limpio y ligero.
- Colores de las cifras de la lista de mazos: Nuevas en azul, Aprendiendo en naranja (Anki usa rojo) y
  Para repasar en verde. Las banderas siguen la familia de colores de Anki, en tonos propios.
- Sigue al modo día o noche que usted elija en Anki y cambia con él.

## 3. Acabado

- Letra de interfaz del sistema (en Windows, Segoe UI Variable o Segoe UI) en las páginas de Anki, con
  la letra que Anki elige para su idioma como reserva (por ejemplo, para japonés o chino).
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
bordes de casillas e iconos).

- De día: el texto principal y el secundario pasan con holgura. Por debajo: las cifras «Aprendiendo»
  (3,4) y «Para repasar» (3,2) de la lista de mazos, el rojo de aviso (4,3) y las cifras «Nuevas» en
  campos hundidos (4,4). Los bordes de las casillas sin marcar quedan en 1,3.
- De noche: todo el texto pasa; el principal llega a 15,4, un brillo alto para sesiones largas. Por
  debajo: en Explorar, las filas con bandera naranja, verde, azul, rosa o turquesa (de 2,9 a 3,7) y
  los bordes de las casillas (1,5).
