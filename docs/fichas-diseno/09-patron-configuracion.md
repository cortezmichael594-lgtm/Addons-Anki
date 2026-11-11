# Modelo de ventana de configuración (el de GritMap)

Fecha: 9 de noviembre de 2026; al día con GritMap 4.16.0 el 11 de noviembre de 2026 (informe 4.15.1,
apartado 7.1). Léase junto con `00-contexto-comun.md`.

La persona quiere que la ventana de configuración de todos sus complementos siga el diseño del panel
de opciones de GritMap (4.16.0), que ya copia Atelier (3.8.0). Este documento describe ese diseño
pieza a pieza, sin código, para que se pueda reproducir igual en cualquier complemento. Al final
indica qué pieza corresponde a cada opción de los demás complementos y qué piezas faltan por
diseñar.

## 1. Idea general

- Es un panel a medida, no una ventana de controles estándar del sistema: una página dentro de una
  ventana de Anki, como las opciones de mazo de Anki.
- Está hecho del mismo material que las tarjetas del mapa de GritMap: fondo de Anki, recuadros de
  capa elevada con borde suave, la letra de Anki y una escala fija de espacios.
- Un solo azul de acción (el de Anki) para rellenos y bordes: el botón principal, lo elegido y el foco.
  El texto que se pulsa usa el color de enlace, más claro de noche, porque el azul de acción como texto
  no llega a 4,5 a 1. Ningún otro color de marca: los colores propios del complemento solo aparecen en sus muestras (por ejemplo, la muestra de
  cada tema).
- Todos los colores salen de la paleta Nocturne y cambian con Atelier y con el modo día o noche.
- Sin animaciones, salvo un hundimiento de 1 px al pulsar.
- Los controles son elementos reales (botones, casillas, botones de opción, campos, diálogos)
  dibujados a medida: conservan el teclado, el foco y lo que anuncia el lector de pantalla.

## 2. La ventana

- Título: el nombre del panel («Opciones» en GritMap; el nombre del complemento en Atelier). Sin el
  botón «?».
- Se abre sobre la ventana desde la que se pide (normalmente Herramientas > Complementos), que queda
  bloqueada mientras está abierta. Si ya está abierta, se trae al frente en vez de abrir otra.
- Ancho: 560 px. Alto: el justo para el contenido de la página principal, como mucho 720 px o el alto
  de la pantalla menos 80 px, y como poco 240 px. El alto se fija una vez al abrir y no cambia al
  entrar en subpáginas.
- Recuerda su tamaño y posición entre sesiones.
- No se enseña hasta estar dibujada entera (sin parpadeo); mientras, se ve el fondo de Anki. Si la
  página no avisa de que está lista en 3 s, se enseña igualmente.
- Ningún texto se puede seleccionar con el ratón, salvo lo que se escribe en los campos.
- Todas las cifras con dígitos de igual ancho.

## 3. Estructura

```
┌──────────────────────────────────────────────┐
│ Cabecera: título (o «‹ Volver» en subpágina)  │  48 px, fija
├──────────────────────────────────────────────┤  (raya solo si el cuerpo se ha desplazado)
│ Cuerpo (se desplaza si no cabe)               │
│  ┌────────────────────────────────────────┐  │
│  │ Recuadro: título del grupo   [enlace]  │  │
│  │ nota del grupo (gris)                  │  │
│  │ Etiqueta                               │  │
│  │ [control]                              │  │
│  │ regla o ayuda (gris)                   │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │  12 px entre recuadros
│  │ Recuadro siguiente…                    │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤  (raya solo si hay contenido por debajo)
│                       [Aceptar] [Cancelar]    │  52 px, fijo
└──────────────────────────────────────────────┘
```

- Cabecera: 48 px de alto, 24 px de margen a los lados, título de 14 px en negrita (700). Al
  desplazar el cuerpo aparece debajo una raya de 1 px.
- Cuerpo: margen de 4 px arriba (para que no se corte el foco del primer control) y 12 px a los lados
  y abajo. Al llevar el foco a un control, queda siempre a la vista con 16 px de holgura arriba y 40
  abajo (entero por encima del fundido). La página entera nunca se desplaza: solo el cuerpo. El sitio
  de la barra de desplazamiento está siempre reservado, para que el contenido no cambie de ancho entre
  páginas.
- Si el contenido no cabe, los últimos 24 px del cuerpo se funden con el fondo de la ventana mientras
  quede algo debajo, y el fundido desaparece al llegar al final. Sin animación.
- Orden de los recuadros: por uso. Arriba, lo que se vuelve a cambiar durante el uso (metas, fechas);
  la apariencia, que se elige una vez, al final. El foco inicial va al primer control del primer
  recuadro.
- Pie: 52 px de alto, 24 px de margen a los lados, botones a la derecha separados 8 px. Raya de 1 px
  arriba solo si el cuerpo tiene contenido oculto por debajo. En Windows, «Aceptar» va primero; en
  macOS y Linux, a la derecha.
- Recuadros (uno por grupo de opciones): fondo de capa elevada, borde de 1 px suave, esquinas de 10 px,
  relleno de 16 px arriba y abajo y 20 px a los lados, sombra mínima de día (0 1px 3px) y ninguna de
  noche. 12 px entre recuadros.
- Cabecera del recuadro: título de 14 px en seminegrita (600) a la izquierda y, si hace falta, un
  enlace de acción a la derecha (por ejemplo, «Restaurar apariencia»). Debajo, una nota en gris con 4
  px de separación.

## 4. Letra y espacios

| Uso | Tamaño | Interlineado | Grosor | Color |
|---|---|---|---|---|
| Título de la ventana | 14 px | 20 px | 700 | Texto |
| Título de un recuadro, de una subpágina o de un diálogo | 14 px | 20 px | 600 | Texto |
| Texto general | 12 px | 18 px | 400 | Texto |
| Etiqueta de una opción, texto de casilla, título de fila | 12 px | 18 px | 600 | Texto |
| Nota, regla, ayuda, resumen | 12 px | 18 px | 400 | Texto secundario |
| Detalles (contador de caracteres, cuenta atrás, días de la semana del calendario) | 11 px | 14 px | 400 | Texto secundario |

- La letra es la de Anki (en Windows, Segoe UI Variable).
- Escala de espacios: 4, 8, 16, 24 y 32 px. Entre opciones de un recuadro, 16 px; entre la etiqueta y
  su control, 6 px; entre un control y su regla, 8 px; textos de ayuda a 4–8 px de lo que explican.
- Dos opciones cortas pueden ir en dos columnas (cada una de 220 px como mínimo, 16 px entre ellas); en
  ventanas estrechas pasan a una.

## 5. Colores

| Uso | Token Nocturne | Día | Noche |
|---|---|---|---|
| Fondo de la ventana | CANVAS | #F7F8FA | #12161F |
| Recuadros y fondo de controles | CANVAS_ELEVATED | #FBFCFE | #212836 |
| Capas flotantes (calendario, diálogo) | CANVAS_OVERLAY | #FBFCFE | #293040 |
| Fondos hundidos (aviso, carril segmentado, huecos de carga) | CANVAS_INSET | #EEF0F4 | #0F131B |
| Texto | FG | #1B2430 | #D6DAE1 |
| Texto secundario | FG_SUBTLE | #4E576A | #B7BECC |
| Borde de recuadros | BORDER_SUBTLE | #E8EAF0 | #1F2635 |
| Rayas y separadores | BORDER | #DADEE7 | #2C3444 |
| Borde de controles (3 a 1 o más) | NOCTURNE_CONTROL_BORDER | #878C97 | #727B8C |
| Acción: botón principal, casilla marcada, borde de lo elegido | BUTTON_PRIMARY_BG | #3B6FE0 | #4066E6 |
| Texto que se pulsa (enlaces, «‹ Volver») | FG_LINK | #2F63D8 | #A3C1F7 |
| Texto de ejemplo de los campos | FG_FAINT | #646C7D | #9AA3B4 |
| Texto e iconos apagados | FG_DISABLED | #A9AFBC | #7C869A |
| Casilla marcada apagada | BUTTON_PRIMARY_DISABLED | #3B6FE059 | #4066E659 |
| Texto sobre la acción | HIGHLIGHT_FG | #FFFFFF | #FFFFFF |
| Foco | BORDER_FOCUS | #3B6FE0 | #6390FF |
| Fondo de lo elegido | NOCTURNE_ROW_HIGHLIGHT | #EAEEF8 | #19233F |
| Fondo al pasar el ratón | BUTTON_HOVER | #EDF0F5 | #2E3747 |
| Error | ACCENT_DANGER | #CA2D2D | #F37777 |
| Sombra de recuadros | SHADOW_SUBTLE | #1B243012 | ninguna |
| Sombra de capas flotantes | SHADOW | #1B243026 | ninguna |

Con Atelier, cada token toma el valor de la paleta elegida (por ejemplo, la acción es cobre en
Atardecer y violeta en Lavanda).

## 6. Catálogo de piezas

Botones:

- Principal («Aceptar»): 32 px de alto como mínimo, 16 px de relleno lateral, esquinas de 8 px, relleno
  y borde del color de acción, texto blanco en seminegrita. Con el ratón, un 6 % más luminoso. Es el
  único botón relleno de la ventana.
- Secundario («Cancelar», «Añadir»): mismas medidas, fondo de capa elevada, borde de control, texto
  normal. Con el ratón, fondo de pasar el ratón.
- Enlace o terciario («Restaurar apariencia», «Deshacer», «Editar»): 28 px de alto, 8 px de relleno,
  esquinas de 6 px, sin fondo ni borde, texto en el color de enlace, en seminegrita y subrayado (sin
  icono, el color solo no basta); con el ratón, fondo suave y sin subrayado.
- Botón de icono (flechas del calendario): 28 × 28 px, sin fondo, esquinas de 6 px.
- Volver (en subpáginas, en lugar del título): «‹ Volver», 28 px, texto en el color de enlace, en
  seminegrita, sin fondo ni subrayado (lleva su flecha).
- Al pulsar cualquier botón o fila, se hunde 1 px.

Elegir una opción entre varias:

- Fichas (para pocas opciones con muestra, como los temas de color): rejilla de dos columnas con 8 px
  entre fichas (una columna si no caben). Cada ficha: 36 px de alto, 12 px de relleno, borde de control,
  esquinas de 8 px; muestra de color de 16 × 16 px con esquinas de 4 px, nombre y una ✓ a la derecha. La
  elegida: borde de 2 px del color de acción, fondo de lo elegido y ✓ visible. Por dentro son botones
  de opción reales.
- Control segmentado (para 2–4 valores cortos, como «30 días · 365 días · Todo el historial»): carril
  hundido con 4 px de relleno, esquinas de 8 px y 4 px entre segmentos. Cada segmento: 28 px, esquinas
  de 6 px, texto secundario centrado. El elegido: fondo de capa elevada, borde de acción, texto normal
  en seminegrita. Si algún valor no cabe en su idioma, el carril pasa a lista vertical: nunca se corta
  un texto.

Números:

- Campo con «−» y «+»: 32 px de alto, borde de control, esquinas de 8 px. Botones de 32 px de ancho a
  los lados; en medio, la cifra centrada (ancho para cuatro dígitos) entre dos rayas finas; la unidad
  («px») en gris a la derecha. Mantener pulsado «−» o «+» repite (tras 0,4 s, cada 0,08 s). En el
  límite, el botón se apaga (su signo en el gris de apagado). Debajo, su regla en gris («Hasta la mitad del
  cuadrito (12 px).»).

Sí o no:

- Casilla: cuadro de 18 px con esquinas de 4 px, borde de control y fondo de capa elevada; marcada,
  rellena del color de acción con la marca blanca. Texto en seminegrita a 8 px, alineado con la primera
  línea; fila de 28 px como mínimo. Toda la fila se pulsa.
- Opciones que dependen de una casilla: agrupadas debajo con una raya vertical de 2 px a la izquierda y
  16 px de sangría. Si la casilla está desmarcada, se ven apagadas (texto e iconos en el gris de
  apagado, casillas marcadas en el azul apagado, el borde de lo elegido en el de los controles) y una
  línea dice por qué y
  que se conservan («La meta, los comodines y la pausa no cuentan mientras esté desmarcada; se
  conservan.»).

Listas y subpáginas:

- Fila de resumen (para lo que necesita más espacio, como «Excluir mazos» o «Fechas clave»): botón de
  todo el ancho, 48 px como mínimo, borde de control, esquinas de 8 px; título en seminegrita, debajo
  el resumen en gris («Ninguno», «2 mazos excluidos»; como mucho dos líneas) y un «›» a la derecha.
  Abre una subpágina dentro de la misma ventana; la cabecera muestra «‹ Volver».
- Buscador: campo de 32 px, borde de control, esquinas de 8 px. Sin resultados: «Ningún mazo
  coincide.» en gris.
- Árbol con casillas: filas de 32 px, botón de plegar de 24 px, sangría por nivel. Marcar un padre
  marca y bloquea a sus hijos (atenuados).
- Lista editable: filas de 36 px separadas por una raya suave, con «Editar» y «Eliminar» como enlaces.
  Al eliminar, la fila se sustituye en su sitio por «Se eliminó «Parcial».» con «Deshacer».
- Formulario de alta: etiquetas encima de los campos, campos de 32 px, botón «Añadir» a la derecha; el
  error va encima de los campos en rojo de error con un icono, y el campo erróneo lleva el borde rojo.
  Contador de caracteres en 11 px gris. El texto de ejemplo de los campos, en el gris tenue.
- Lista vacía: en lugar de contar cero («0 de 50 fechas»), una línea en gris que dice para qué sirve;
  con el primer elemento vuelve el contador (12 px, alineado con el texto de los recuadros).

Fechas:

- Botón de fecha (32 px, con icono de calendario en gris) que abre un calendario flotante de 272 px:
  capa flotante con esquinas de 10 px y sombra de 0 8px 24px, mes con flechas, rejilla de 7 columnas de
  32 px, días de la semana en 11 px gris. Hoy con borde del color del texto; el elegido relleno de
  acción con texto blanco; días de otro mes en gris; días no válidos al 45 %.

Piezas añadidas el 9 de noviembre de 2026 (las pidieron ProFeedback, Restart, Always on Top y
CoreProgress; mismo lenguaje que las demás):

- Deslizador (para un valor continuo, como el volumen): carril hundido de 6 px con esquinas de 3 px y
  borde fino, lleno del color de acción hasta el valor; tirador redondo de 18 px con fondo de capa
  elevada y el borde de los controles (fondo de pasar el ratón al pasarlo). A la derecha, la cifra con
  su unidad («100 %») en seminegrita. Las flechas lo mueven de uno en uno; el lector de pantalla oye
  la cifra con su unidad.
- Lista desplegable (para elegir uno entre muchos o entre una lista que crece, como los sonidos): un
  selector real de 32 px, borde de control, esquinas de 8 px, fondo de capa elevada, flecha hacia abajo
  en gris a la derecha; la primera opción es la neutra («Aleatorio»). Puede llevar al lado un botón
  secundario de acción («Probar»). Sin opciones útiles, la lista y su botón se atenúan.
- Campo grabador de atajos: campo de 32 px con la combinación en seminegrita, escrita con los nombres
  de teclas del sistema y del idioma («Control+Mayúsculas+O»); vacío, el texto de ayuda en gris. Al
  lado, un botón de icono con una cruz para vaciarlo. Graba la combinación que se pulse con el foco en
  él; el tabulador, Mayús+Tab y Esc siguen haciendo lo suyo, y Retroceso o Supr solos lo vacían. Si la
  combinación no sirve, el aviso de error va encima del campo y el campo lleva borde rojo.
- Línea de dato con acción (para un dato que se puede reiniciar, como un récord): el texto con el dato
  en negrita a la izquierda y un enlace de acción a la derecha («Restablecer»), apagado si no hay nada
  que hacer. Si la acción borra algo sin vuelta atrás, pregunta con el diálogo de abajo con el foco en
  «No», y el cambio solo se aplica al pulsar Aceptar.
- Recuadro sin título: para un grupo único o para un dato suelto; si tiene «Restaurar», el enlace va
  solo, arriba a la derecha.

Mensajes:

- Aviso dentro del panel (por ejemplo, un tema retirado): franja hundida, esquinas de 8 px, relleno de 8
  × 16 px, icono de información en gris y el texto. Nunca en rojo.
- Pregunta antes de perder algo: diálogo real centrado, 400 px como máximo, relleno de 24 px, esquinas de
  10 px, capa flotante con sombra, fondo de detrás oscurecido. Título de 14 px, texto en gris y botones
  a la derecha; el foco empieza en la opción que no pierde nada («Seguir editando»).
- Huecos de carga: barras grises redondeadas (12 px de alto) mientras llega un dato que tarda, como el
  esqueleto del mapa.

## 7. Comportamiento

- Nada se guarda hasta «Aceptar». «Cancelar», Esc o la X descartan.
- Lo que se ve en otra parte de Anki (aspecto, colores) se aplica en vivo mientras se elige (vista
  previa a los 80 ms de dejar quieto el control) y «Cancelar» lo deshace. El recuadro lo dice en su
  nota («Se ve ya en el mapa; se guarda al aceptar.»). Lo que no se puede previsualizar lo dice también
  («Los mazos excluidos se aplican al aceptar.»).
- Restaurar por grupo, no de toda la ventana: un enlace «Restaurar …» en la cabecera de su recuadro y,
  tras usarlo, «Deshacer» al lado.
- Si hay cambios que se perderían (por ejemplo, fechas añadidas) y se cancela, pregunta «¿Descartar los
  cambios?» con el foco en «Seguir editando».
- Lo escrito en un formulario interior sin pulsar «Añadir» cuenta: «Aceptar» lo añade (si no se puede,
  no cierra y avisa encima del campo), «Cancelar» lo cuenta como cambio y «‹ Volver» lo conserva.
- Al elegir una opción que necesita un valor, se propone uno razonable y se explica de dónde sale.
- La ventana se abre al instante con lo guardado; lo que tarda en leerse (la lista de mazos) llega
  después, con huecos de carga, sin bloquear Anki.
- Un valor guardado que ya no sirve se sustituye por el de serie y, si la persona lo eligió, se avisa
  en la franja de aviso.
- Si algo falla, nunca la ventana de error de Anki: el detalle va al registro.

## 8. Accesibilidad

- Foco del teclado: contorno de 2 px del color de foco, separado 2 px (dentro del campo numérico, por
  dentro). Visible en botones, campos, fichas, segmentos y casillas, solo cuando se usa el teclado:
  si la ventana se abrió con el ratón, el foco inicial no se dibuja hasta la primera tecla (en los
  campos de texto se ve siempre).
- Teclado: el tabulador recorre en orden visual; las flechas mueven dentro de fichas y segmentos (grupos
  de botones de opción); Espacio marca casillas; Intro pulsa el botón que tiene el foco (nunca acepta la
  ventana por su cuenta); Esc cancela.
- Lector de pantalla: cada grupo y cada control tiene nombre; los grupos de fichas y segmentos se
  anuncian como grupos de opciones; los campos numéricos anuncian valor, mínimo, máximo y unidad; los
  campos con error se marcan como no válidos; el árbol anuncia si está plegado; el calendario se anuncia
  como diálogo con el mes; los cambios que llegan solos («Actualizando…», «Se eliminó…») se dicen en voz
  alta; los iconos son decorativos y no se leen.
- Contraste: texto 4,5 a 1 o más; bordes de controles 3 a 1 o más; texto blanco sobre la acción, 4,6 a 1
  de día y 4,9 de noche.
- Colores forzados del sistema (alto contraste de Windows): todo control conserva un borde real, lo
  elegido se marca con el borde del sistema y la ✓, el foco con el resaltado del sistema; solo las
  muestras de color conservan su color.
- Nunca se corta un texto con «…» en un botón o un segmento: pasa a otra línea o a lista vertical.
- Idiomas de derecha a izquierda: el panel se refleja; el calendario conserva su orden.

## 9. Dónde se usa

Desde el 9 de noviembre de 2026, todos los complementos del taller abren sus opciones con este panel:
GritMap (el original), Atelier (su panel de paletas copia las mismas medidas), CoreProgress 1.1.0,
ProFeedback 2.1.0, Hider 4.1.0, Restart 2.1.0, Always on Top 1.3 y Edit field during review 1.1.0.

| Complemento | Opción | Pieza |
|---|---|---|
| CoreProgress | Récord actual y «Restablecer» | Línea de dato con acción, en un recuadro sin título |
| CoreProgress | Tema de color (7) | Fichas con muestra |
| CoreProgress | Altura de la barra, Espacio superior | Campo con «−» y «+» y «px» al lado |
| CoreProgress | Efectos de racha y récord, Mostrar hitos | Casillas |
| CoreProgress | Excluir mazos (récord) | Fila de resumen con subpágina (buscador y lista con casillas) |
| ProFeedback | Volumen 0–100 | Deslizador |
| ProFeedback | Sonidos (Aleatorio o uno) con «Probar» | Lista desplegable con botón secundario, colgando de su casilla |
| ProFeedback | Casillas de sonidos y de aspecto | Casillas, con lo dependiente agrupado y atenuado |
| Hider | Seis casillas de «Durante el repaso, ocultar» y una de comportamiento | Dos recuadros con casillas; los antiguos globos son notas grises debajo |
| Hider | Segundos del puntero (1–60) | Campo con «−» y «+», dependiente de su casilla |
| Restart | Activar atajo y Atajo | Casilla con el campo grabador colgando de ella |
| Always on Top | Atajo | Campo grabador de atajos |
| Edit field during review | Exigir Ctrl + clic | Una casilla en un recuadro |

Los paneles con una o dos opciones usan el mismo ancho de 560 px y el alto justo para su contenido
(decisión de la persona, 9 de noviembre de 2026).
