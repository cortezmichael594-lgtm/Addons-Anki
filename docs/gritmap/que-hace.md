# Qué hace «GritMap»

Versión 4.6.0 · 2026-10-21

Mapa de calor de su estudio, como el de las contribuciones de GitHub, en tarjetas. Arriba, centrada y
con cuadritos de 24 px de serie (con el dibujo de la versión 4.1.0), la tarjeta del mapa, con el año entero (un cuadrito por día: gris sin estudio y cuatro tonos
del tema; los días que vienen, en cuatro grises según las tarjetas que vencen). Debajo, cinco tarjetas
pequeñas del mismo ancho entre todas, que responden de un vistazo: «Hoy», «Racha», «Promedio
diario», «Retención» y «Próxima fecha». Tiene una meta diaria opcional, comodines que perdonan días
sueltos y una pausa de la racha.
Solo lee su colección: nunca cambia tarjetas, notas ni repasos. Lo único que guarda son sus opciones.

## 1. Dónde aparece

- En la lista de mazos (la pantalla principal), debajo de la lista y de la línea en la que Anki dice
  cuánto ha estudiado hoy. Ahí cuenta toda la colección, menos los mazos que usted excluya. Anki no
  ofrece a los complementos un sitio encima de la lista; por eso va debajo (decisión del cliente).
- En la pantalla de un mazo (la que tiene el botón «Comenzar a estudiar»), debajo de las cifras de
  tarjetas. Ahí cuenta solo ese mazo y sus submazos, y no hay meta (véase el apartado 3).
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones (la misma que el botón de opciones del mapa), delante de la ventana Complementos.
- No aparece en el repaso, en Explorar, en las estadísticas ni en el editor. No añade menús.
- De serie, el mapa tiene cuadritos de 24 px, centrado; si no cabe en la ventana, se desplaza de
  lado. Con otro tamaño, el mapa entero crece o encoge en proporción (los huecos incluidos, así que
  se ve igual, solo más grande o más pequeño). Con «Ajustado al ancho», ocupa todo el ancho de la
  pantalla y sus cuadritos crecen o encogen con la ventana (nunca por debajo de 10 px). Las cinco tarjetas pequeñas van debajo y suman exactamente su ancho, con los bordes
  alineados con los del mapa. Cada tarjeta tiene el fondo un punto más claro
  que el de Anki, un borde suave, esquinas redondeadas y su título arriba a la izquierda; de día
  llevan una sombra muy leve y de noche ninguna.

## 2. Mientras se calcula

La primera vez que se abre una pantalla se ven ya las tarjetas con huecos grises donde irán los
datos, y la rejilla del año con su alto final, para que nada salte cuando llegan. Después, cada vez
que Anki vuelve a dibujar esa pantalla (al volver del repaso, sincronizar, deshacer, plegar un mazo o
cada 10 minutos), se ve al instante lo último que se mostró y se sustituye, sin hueco, si los datos al
día son distintos. El cálculo se hace sin congelar Anki.

## 3. Las tarjetas de debajo del mapa

Cinco tarjetas del mismo ancho (cuatro si se desactiva «Mostrar racha y meta»), que suman el ancho
del mapa. Cada una tiene un título, un dato grande y una línea gris de hasta dos renglones (si no
cabe, se corta con «…» y se lee entera al pasar el ratón). No tienen enlaces: al pulsarlas no pasa
nada. Se reordenan según el ancho del mapa: por debajo de 760 px, dos por fila, con la quinta a lo
ancho de las dos para que la fila quede cuadrada, y, por debajo de 420 px, una.

### Hoy

- Sin meta: lo hecho hoy en la unidad de la medida («35 repasos») y, debajo, lo hecho en los 7 últimos
  días completos (terminan ayer): «448 repasos en 7 días».
- Con la meta «Un número»: un anillo pequeño que se llena con lo hecho, «80 de 100» y, debajo,
  «faltan 20 repasos». Al cumplirla, «✓ Meta cumplida»; si la supera, «120 de 100», con el anillo
  cerrado. La primera vez que se dibuja después de cumplirla (al volver a la lista de mazos tras
  repasar), el ✓ aparece con un leve aumento de 150 ms; nada si Anki o el sistema piden reducir las
  animaciones, y no se repite al volver a la pantalla.
- Con la meta «Terminar lo de hoy»: lo mismo, en tarjetas: las respondidas hoy frente a esas más las
  que aún vencen hoy (con los límites diarios de Anki y sin los mazos excluidos).
- La meta se elige en Opciones, «Metas y fechas» > «Meta diaria».
- En la pantalla de un mazo, el título es «Hoy en este mazo», con lo hecho hoy en ese mazo y sus 7
  días, sin meta: la meta es de toda la colección.
- Con «Mostrar racha y meta» desactivado, lo hecho hoy y sus 7 días, sin meta.

### Racha

Días seguidos estudiando hasta hoy, en la medida elegida («18 días»). La racha no se rompe por no
haber estudiado todavía hoy. La línea gris dice:

- «✓ hoy» si hoy ya cuenta, u «hoy pendiente» si todavía no;
- «· 1 comodín» o «· 2 comodines» si tiene comodines guardados (subrayado de puntos: al pasar el
  ratón o llegar con el tabulador, «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin
  estudiar gasta uno.»);
- «· a 3 días del récord» si la racha más larga está a 7 días o menos, o «· récord: 40 días» si
  está más lejos (si la racha actual es la más larga, no se añade nada);
- «· Un año seguido» el día en que la racha llega a 365 días (y a 730, 1.095…).

Casos especiales: si nunca ha estudiado, «0 días» y «hoy pendiente»; si la racha está a cero,
«0 días» y «Última sesión hace 3 días»; al volver tras romperla, «Día 1» y «récord: 45 días».

### Promedio diario

Lo hecho por día estudiado, en la unidad de la medida («72 repasos», «60 tarjetas», «8 nuevas»), en el
periodo de las cifras, contando solo días completos (el periodo termina ayer). Debajo, el periodo:
«últimos 30 días», «último año» o «todo el historial». Sin días completos estudiados escribe «N/A» en
gris, subrayado de puntos: al pasar el ratón (o llegar con el tabulador), «Sin días completos
estudiados en los últimos 30 días» (o «… en todo el historial»). Con «Nuevas», un promedio que se
queda en 0 también es «N/A», con «Menos de una nueva por día estudiado…».

### Retención

El porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención real de Anki
(tarjetas con al menos un día de intervalo), en el periodo de las cifras (Opciones). Debajo, el periodo:
«últimos 30 días», «último año» o «todo el historial». Con menos de 20 respuestas que contar escribe
«N/A» (el texto de Anki), en gris. En la pantalla de un mazo con FSRS activado añade la retención
deseada de su configuración: «· objetivo 90 %».

### Próxima fecha

La próxima fecha clave de hoy en adelante: «faltan 23 días», «falta 1 día» o «es hoy», sin estrella.
Debajo, solo su nombre (varias el mismo día, separadas por « · »): «Examen de Anatomía». Sin fechas
por venir: «N/A» en gris y, debajo, «sin fechas clave», en minúscula. Las fechas se añaden en
Opciones > «Gestionar fechas». La tarjeta nunca desaparece.

## 4. La tarjeta del mapa

- Sin título ni cifras encima: solo los botones, centrados sobre el mapa: «‹ 2026 ›» (año anterior y
  siguiente, con su nombre al pasar el ratón) y el botón de opciones. No hay botón «Hoy». Las flechas
  se apagan en el primer año con repasos y en el último con vencimientos o fechas clave.
- El año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki (siempre con el calendario gregoriano). El dibujo es
  siempre el mismo, como en la 4.1.0: el hueco mide 3/14 del cuadrito y las esquinas, el redondeo
  elegido en píxeles (3 px de serie). Cada cuadrito mide el tamaño elegido (24 px de serie) y todo lo
  demás crece con él; con «Ajustado al ancho», el año llena el ancho de la tarjeta y el redondeo es el
  de un cuadrito de 14 px.
  Si el año no cabe, se desplaza de lado: al abrir un año se ve la semana de hoy; en un año pasado, diciembre, y en uno
  futuro, enero.
- Días pasados y hoy: cinco niveles. Sin estudio, el gris vacío; con estudio, cuatro tonos del tema,
  repartidos según su promedio de siempre en los días que estudió (con un mínimo, para que al empezar
  no salga todo oscuro): hasta la mitad del promedio, hasta el promedio, hasta el doble y más del
  doble.
- Días futuros con tarjetas que vencen: en cuatro grises, más oscuros (de día) o más claros (de noche)
  cuantas más tarjetas vencen, con los mismos cortes en proporción a su promedio de repasos. Lo
  atrasado no se dibuja.
- Hoy lleva un borde del color del texto.
- Las fechas clave llevan una estrella en su cuadrito, en el color del texto y con un filo del color
  de la tarjeta, que se ve sobre cualquier tono y es igual en todos los temas; al pasar el ratón, su
  nombre y su cuenta atrás.
- Un día perdonado por un comodín o por la pausa queda vacío (no estudió), con un borde fino
  discontinuo.
- Al pasar el ratón por un día, el cuadrito se resalta; si se puede pulsar, el puntero cambia a una
  mano y el globo lo dice.
- Qué mide el color se elige en las opciones: repasos (cada respuesta cuenta una; no cuentan los
  cambios manuales de fecha ni las reprogramaciones), tarjetas (tarjetas distintas respondidas ese
  día) o nuevas (tarjetas que empezó a estudiar ese día, también en los años anteriores al
  planificador actual de Anki). Con «Nuevas», un día estudiado sin ninguna nueva queda en gris.
- Debajo, a la derecha, la leyenda: «Menos», los cinco cuadritos del mapa y «Más». Al pasar el ratón
  por cada uno, las cifras que cubre, calculadas con su promedio actual: «Ningún repaso», «de 1 a 20
  repasos», «de 21 a 40 repasos», «de 41 a 80 repasos» y «81 repasos o más» (con «Nuevas», «Ninguna
  nueva»…). Detrás, «Pendientes» (un gris) si en el año que se ve hay días pendientes, «Fecha clave»
  (la estrella) si ese año tiene alguna, y «Perdonado» (el borde discontinuo) si hay días
  perdonados.
- Debajo, a la izquierda, como mucho una línea de sorpresa al día, solo cuando ocurre y con datos
  reales, por este orden: «Nueva racha más larga» (el día en que la racha supera la mejor anterior),
  «Su mejor día del año» (hoy supera a todos los demás días del año, con al menos 7 días estudiados
  antes), «Mes completo» (el último día del mes, si estudió todos sus días) y «1.000 repasos este año»
  (el día en que el total del año cruza 100, 500 o un múltiplo de 1.000). Solo si hoy ya cuenta.
- En árabe, hebreo, persa y uigur, la navegación del año, el mapa y su pie van de izquierda a derecha,
  como el calendario; el resto sigue la dirección del idioma.
- Cambiar de año o de tema, tamaño, forma, periodo de las cifras, meta, comodines o pausa no vuelve a leer la
  colección: es inmediato. Cambiar la medida o los mazos excluidos sí la vuelve a leer, sin quitar el
  mapa mientras tanto.

### Cuando no hay nada que dibujar

- En una colección sin repasos, sin vencimientos y sin fechas clave: la cuadrícula del año actual en
  gris con hoy marcado y, debajo, «Cada día que estudie se pintará aquí.», sin leyenda y con las
  flechas de año apagadas; y debajo, las tarjetas («0 repasos» con «0 repasos en 7 días», «0 días»
  con «hoy pendiente», promedio y retención «N/A», y «N/A» con «sin fechas clave»).
- En la pantalla de un mazo excluido: una tarjeta con «Este mazo está excluido del mapa.»
  y el botón de opciones.
- Si algo falla: una tarjeta con «No se pudo cargar el mapa de calor.» y el botón de opciones.

## 5. Al pasar el ratón por un día (o llegar a él con el teclado)

Sale un globo con la fecha larga en el idioma de Anki (sin «el»), en gris, y, en la línea de abajo, lo
hecho ese día. Después, en gris y según el caso: si el día está perdonado, «Perdonado con un comodín»
o «Racha en pausa»; y en los días que se pueden pulsar, «Pulse para ver estas tarjetas» o «Pulse para
ver las que vencen ese día». El globo no dice nada de la meta. La tecla Esc lo cierra. En español:

- «lunes, 22 de junio de 2026» / «**12** **repasos**» (o «1 repaso»).
- Con la medida «Tarjetas»: «… / **9** **tarjetas**».
- Con la medida «Nuevas»: «… / **3** **nuevas**», «**1** **nueva**» o «**Ninguna** **nueva**».
- Sin estudio: «… / **Ningún** **repaso**».
- Días futuros: «… / **30** tarjetas **pendientes**», «**1** tarjeta **pendiente**» o «**Ninguna**
  tarjeta **pendiente**».
- En una fecha clave, encima de todo, en negrita: el nombre (varios, separados por « · ») y, si no ha
  pasado, la cuenta atrás: «Examen de Anatomía (faltan 23 días)».
- Las cifras de 1.000 o más llevan punto de millar. Un lector de pantalla lee el mismo texto.

## 6. Al pulsar un día

- Un día pasado con repasos abre Explorar con la búsqueda de las tarjetas respondidas ese día
  (prop:rated), limitada al mazo de la pantalla y sin los mazos excluidos.
- Un día futuro con vencimientos abre Explorar con las tarjetas que vencen ese día (prop:due).
- Los días sin nada no responden al clic. Con el teclado, Intro o la barra espaciadora hacen lo mismo.

## 7. Comodines y pausa

- Comodines (activados por defecto; se desactivan en Opciones): cada 7 días seguidos estudiados se
  gana uno, con un máximo de 2 guardados. Un día sin estudiar gasta uno automáticamente al empezar el
  día siguiente: la racha no se rompe, pero tampoco suma ese día. Sin comodines, el día sin estudiar
  rompe la racha. Se ganan estudiando; no se compran ni se piden.
- Pausa de la racha: en Opciones, de un día a otro, de 1 a 30 días. Un día de pausa sin estudiar ni
  suma ni rompe la racha y no gasta comodines; un día de pausa en que estudió cuenta como siempre. Se
  ven como los perdonados.
- La meta nunca afecta a la racha: basta un repaso para que el día cuente.
- El «hoy» de la racha y del mapa es el de Anki: el día empieza a la hora que marca Anki en
  Preferencias (por defecto, las 4 de la madrugada), y lo estudiado antes cuenta para el día anterior.

## 8. Ventana de opciones

Título «GritMap». Se abre después de leer los mazos y las opciones sin congelar Anki (un segundo clic
mientras tanto no abre otra), delante de la ventana desde la que se pidió. Tres recuadros con título
(«Apariencia», «Qué se cuenta» y «Metas y fechas»), con controles estándar de Anki, y los botones «Restaurar apariencia» (a la izquierda; al pasar el ratón, «No cambia los mazos
excluidos ni las fechas clave»), Aceptar y Cancelar. Intro pulsa el botón que tiene el foco. Recuerda
su ancho y su posición; el alto es siempre el que piden sus opciones, sin huecos. Al aceptar, el mapa se redibuja en su sitio, sin recargar la pantalla.

En este orden (Apariencia: las tres primeras; Qué se cuenta: de «El color mide» a «Excluir mazos»;
Metas y fechas: el resto):

| Opción | Valores | Por defecto |
|---|---|---|
| Tema de color | Azul océano, Naranja atardecer, Púrpura real y Verde clásico, cada uno con un cuadrito de su tono en el modo activo (cambia si Anki pasa de día a noche) | Verde clásico |
| Tamaño del mapa | Campo numérico con flechas: «Ajustado al ancho» (el primer valor) o de 8 px a 60 px, el lado de cada cuadrito; el mapa entero crece en proporción | 24 px |
| Redondeo de esquinas | Campo numérico con flechas, de 0 px a 15 px (a partir de la mitad del cuadrito, es un círculo) | 3 px |
| El color mide | Repasos, Tarjetas, Nuevas; debajo, «Cada respuesta cuenta una», «Cada tarjeta cuenta una vez por día» o «Solo las tarjetas que empezó ese día» | Repasos |
| Periodo de las cifras | 30 o 365 días, o Todo el historial (vale para el promedio diario y la retención) | 30 días |
| Excluir mazos | Botón «Seleccionar mazos» (o «1 mazo excluido», «2 mazos excluidos», con hasta 15 nombres al pasar el ratón y «…» si hay más) | Ninguno |
| Meta diaria | «Sin meta», «Un número» (con el número, de 1 a 9.999, en la unidad de la medida) o «Terminar lo de hoy» | Sin meta (50 si elige «Un número») |
| Comodines | Casilla «Perdonar días sueltos con comodines» (al pasar el ratón, la regla) | Marcada |
| Pausa | Casilla «Pausar la racha» con las fechas de inicio y fin (el fin, como mucho 29 días después del inicio; al pasar el ratón, «La pausa dura 30 días como máximo.») | Desmarcada |
| Fechas clave | Botón «Gestionar fechas» (o «1 fecha marcada», «3 fechas marcadas», con la lista al pasar el ratón) | Ninguna |
| Mostrar racha y meta | Casilla | Marcada |

- Mientras cambia el tema, el tamaño o el redondeo, el mapa de detrás cambia al momento (un
  instante después de soltar la flecha), sin guardar nada; si cancela, vuelve a como estaba. La medida
  y los mazos excluidos se ven al aceptar, porque piden leer la colección.
- «Restaurar apariencia» repone el tema, el tamaño, el redondeo y la medida; no toca los
  mazos excluidos, las fechas clave, la meta, los comodines, la pausa ni el periodo.
- Si tenía Rojo fuego, Rosa suave o Turquesa laguna, retirados en esta versión, pasa sin preguntar a
  Naranja atardecer, Púrpura real o Azul océano, y la ventana lo dice una vez, arriba: «Su tema «Rojo
  fuego» se ha retirado; ahora usa «Naranja atardecer».».
- Al pasar a la 4.6.0, el mapa toma los valores de serie (24 px y 3 px de redondeo): el tamaño y el
  redondeo guardados por la 4.2 a la 4.5 se dejan de leer. Si venía de la 4.0 o la 4.1 con
  «Redondeado», el redondeo pasa a 8 px; las opciones «Tamaño» y «Forma» de esas versiones se
  dejan de guardar.
- Excluir mazos: árbol de mazos con casillas, como en la pantalla principal (sin mazos filtrados ni
  el mazo predeterminado vacío), con un buscador encima («Buscar», el texto de Anki). Marcar un mazo
  marca y bloquea (en gris) sus submazos; al desmarcarlo, cada submazo vuelve a su propia casilla. Lo
  excluido no cuenta en ningún mapa. Solo se cuentan y se nombran mazos que existen.
- Fechas clave: lista en dos columnas, fecha corta (con el año en cuatro cifras) y nombre; el botón
  «Eliminar» (o la tecla Supr con el foco en la lista; tras borrar queda seleccionada la siguiente);
  un campo con el ejemplo «p. ej., examen de Matemáticas» (60 caracteres como máximo), un selector de
  fecha con calendario (de 2000 a 2100; hoy por defecto) y el botón «Añadir». Intro en el campo añade.
  Avisos: «Falta el nombre de la fecha.», «Esa fecha con ese nombre ya está en la lista.» y «Caben
  hasta 50 fechas.».

## 9. Qué guarda y dónde

- La apariencia y las metas (tema, medida, tamaño, forma, periodo de las cifras, meta, comodines y
  mostrar racha y meta), en la configuración de complementos de este ordenador: vale para todos los
  perfiles y no se sincroniza. Los ajustes de versiones anteriores que ya no existen (píxeles,
  comparativa semanal y estadísticas plegadas) se dejan de guardar al aceptar las opciones.
- Los mazos excluidos, las fechas clave y la pausa, dentro de cada colección: cada perfil tiene los
  suyos y viajan con la sincronización. Se leen de la colección cada vez. No se pueden deshacer desde
  Editar, porque son ajustes, no estudio.
- Si encuentra mazos o fechas guardados como en versiones antiguas, los copia una vez a cada perfil
  que aún no los tenga.
- Un valor que falte o no sirva (por ejemplo, escrito a mano) se sustituye por el predeterminado.

## 10. Idiomas

Sus textos están en 51 idiomas, también los nuevos de la 4.0.0; si el de Anki no está, sale en
inglés. Cada cifra con unidad usa la forma de plural de su idioma (por ejemplo, en ruso 1 день,
2 дня, 5 дней; «1 comodín», «2 comodines»). Las cifras, los porcentajes, las fechas y los nombres de
los meses los escribe el navegador de Anki en su idioma; en español, con punto de millar desde 1.000.
«N/A», «Añadir», «Eliminar» y «Buscar» usan los textos de Anki.

## 11. Colores, letra y espacio

- Cada color tiene una sola función: los cuatro tonos del tema significan «estudió» (mapa y anillo
  de la meta); los cuatro grises, «vence»; el gris vacío, «no estudió»; el azul de Anki, el foco del
  teclado. Las señales son formas, no colores: la estrella y el borde discontinuo.
- Todo lo que no es la escala del tema sale de los colores de Anki, que la paleta Nocturne redefine,
  con su pareja de día y de noche: tarjeta (fondo de capa elevada y borde suave), textos (texto y texto
  suave), botones, foco (azul de foco) y globo. El gris de los días sin estudio es el borde suave
  de día y el fondo hundido de noche, para que se distinga sobre la tarjeta en los dos modos. Los
  cuatro tonos de cada tema y los cuatro grises de los pendientes son colores propios (véase «Así a
  propósito» en errores).
- Dos tamaños de letra: 20 px para el dato de cada tarjeta y 12 px para todo lo demás; la jerarquía se
  marca con el grosor y el gris. La letra es la de Anki.
- Espacios de 4, 8, 16 y 32 px: 16 px dentro de las tarjetas y entre ellas.

## 12. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento (un archivo
de texto en la carpeta de registros del perfil de Anki) y, en el sitio del mapa, sale «No se pudo
cargar el mapa de calor.», con el botón de opciones. Anki sigue funcionando.

## 13. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No aparece en el repaso, en Explorar ni en las estadísticas.
- No avisa, no mete prisa ni habla de perder la racha; no hay premios al azar, clasificaciones,
  insignias ni puntos.
- No anima nada salvo el leve hundimiento de los botones al pulsarlos y la aparición del ✓ al cumplir
  la meta.

## 14. Lo que se probó y se descartó

Lo que tuvo alguna versión y ya no está, y el motivo. Sirve para no volver a ello sin querer.

### En el mapa

| Descartado | Versión en la que se quitó | Por qué |
|---|---|---|
| Ocupar literalmente todo el ancho de la pantalla como única forma | 4.2.0 | Resultaba demasiado grande. Queda como «Ajustado al ancho», el primer valor de «Tamaño del mapa». |
| «Ajustado al ancho» como valor de serie | 4.6.0 | El cliente prefirió 24 px de serie. |
| Hueco fijo de 3 px entre cuadritos con cualquier tamaño | 4.5.0 | Al cambiar el tamaño, las líneas entre filas y columnas perdían la proporción y el mapa dejaba de parecerse. Ahora el hueco crece con el cuadrito. |
| Título «Actividad» y cifra del año («22.129 repasos en 2026») encima del mapa | 4.3.0 | El cliente los quería fuera: no aportaban y ocupaban sitio. |
| Botón «Hoy» | 4.4.0 | El mapa ya se abre en la semana de hoy. |
| «Meta cumplida» escrito en el mapa | 4.1.0 | Repetía lo que ya dice la tarjeta «Hoy». |
| Puntos para los días con tarjetas pendientes | 4.1.0 | El cliente prefirió el marcado de antes: cuatro grises según las tarjetas que vencen. |
| Esquina doblada para marcar las fechas clave | 4.2.0 | Se veía poco. Se cambió por una estrella dentro del cuadrito. |
| Salto o enlace desde «Próxima fecha» hasta su día en el mapa | 4.2.0 | El cliente no quiere enlaces en las tarjetas. |

### En las tarjetas de debajo

| Descartado | Versión en la que se quitó | Por qué |
|---|---|---|
| Tarjeta de estadísticas, plegable | 4.1.0 | Sobraba. La sustituyó «Promedio diario». |
| Tarjetas encima o al lado del mapa | 4.1.0 | El cliente las quería debajo, sumando el ancho del mapa. |
| Botones de periodo (30 días, 365 días…) en la página | 4.1.0 | El periodo se elige solo en Opciones. Las tarjetas dicen cuál se usa. |
| Estrella junto a «Próxima fecha» | 4.1.0 | No hacía falta: la estrella marca el día en el mapa. |
| La fecha al lado del nombre en «Próxima fecha» | 4.3.0 | Ya dice cuántos días faltan. Queda solo el nombre. |
| «Sin fechas clave» como dato grande | 4.4.0 | Ahora pone «N/A», igual que las demás tarjetas sin dato, y debajo «sin fechas clave». |
| «Récord» con mayúscula en medio de la línea de la racha | 4.1.0 | Va en medio de una frase: «récord». |
| Enlaces dentro de las tarjetas («Fijar meta», «Añadir» fechas, ir a los mazos excluidos) y la ventanita «Fijar meta» | 4.2.0 | El cliente no quiere enlaces. Todo se cambia en Opciones. |

### En la ventana de opciones

| Descartado | Versión en la que se quitó | Por qué |
|---|---|---|
| «Tamaño» (Ajustado / Grande) y «Forma» (Cuadrado / Redondeado) | 4.2.0 | El cliente quería, como en las primeras versiones, el tamaño y el redondeo en píxeles. |
| Mes de muestra (vista previa) dentro de Opciones | 4.2.0 | Se sustituyó por el propio mapa, que cambia en vivo detrás de la ventana. |
| Barras deslizantes para el tamaño y el redondeo | 4.3.0 | Se veían raras. Volvieron los campos numéricos con flechas. |
| Opciones en una sola lista, sin recuadros | 4.4.0 | El cliente prefirió los tres recuadros con título. |
| Hueco entre «Apariencia» y «Qué se cuenta» | 4.3.0 | Venía de una altura guardada por otra versión. Ahora el alto se ajusta siempre al contenido. |
| «Tamaño de celda» | 4.5.0 | Pasó a «Tamaño del mapa»: agranda o encoge el mapa entero, no solo los cuadritos. |
| Redondeo en la escala de un cuadrito de 14 (de 0 a 7) | 4.6.0 | El cliente lo quería en píxeles, con «px» al final. |

### Antes de estas versiones

| Descartado | Por qué |
|---|---|
| Medida «minutos» | Hay días con cientos de repasos guardados sin tiempo, así que la cifra no era coherente (decisión del cliente, 2026-10-08). |
| Temas Rojo fuego, Rosa suave y Turquesa laguna | Se retiraron en la 4.0.0 y se pasa sin preguntar al más parecido (Naranja atardecer, Púrpura real y Azul océano). |
| Mapa encima de la lista de mazos | Anki no ofrece a los complementos ese sitio. Va debajo (decisión del cliente). |
