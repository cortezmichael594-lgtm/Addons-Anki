# Qué hace «GritMap»

Versión 4.7.1 · 2026-10-22

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
  pantalla y sus cuadritos crecen o encogen con la ventana (nunca por debajo de 10 px). Las cinco
  tarjetas pequeñas van debajo y suman exactamente su ancho, con los bordes
  alineados con los del mapa. Cada tarjeta tiene el fondo un punto más claro
  que el de Anki, un borde suave, esquinas redondeadas y su título arriba a la izquierda; de día
  llevan una sombra muy leve y de noche ninguna.

## 2. Mientras se calcula

La primera vez que se abre una pantalla se ven ya las tarjetas con huecos grises donde irán los
datos, y la rejilla del año con su alto final, para que nada salte cuando llegan. Después, cada vez
que Anki vuelve a dibujar esa pantalla (al volver del repaso, sincronizar, deshacer, plegar un mazo o
cada 10 minutos), se ve al instante lo último que se mostró y se sustituye, sin hueco, si los datos al
día son distintos. Al pasar al día siguiente (a la hora que marca Anki), el mapa se vuelve a calcular
en el acto, sin esperar a que Anki redibuje la pantalla. El cálculo se hace sin congelar Anki.

## 3. Las tarjetas de debajo del mapa

Cinco tarjetas del mismo ancho (cuatro si se desactiva «Mostrar racha y meta»), que suman el ancho
del mapa. Cada una tiene un título, un dato grande y una línea gris de hasta dos renglones (si no
cabe, se corta con «…» y se lee entera al pasar el ratón). No tienen enlaces: al pulsarlas no pasa
nada. Se reordenan según el ancho del mapa: por debajo de 940 px, dos por fila, con la quinta a lo
ancho de las dos para que la fila quede cuadrada, y, por debajo de 420 px, una.

### Hoy

- Sin meta: lo hecho hoy en la unidad de la medida («35 repasos») y, debajo, lo hecho en los 7 últimos
  días completos (terminan ayer): «448 repasos en 7 días».
- Con la meta «Un número»: un anillo pequeño que se llena con lo hecho, «80 de 100» y, debajo,
  «faltan 20 repasos». Al cumplirla, «✓ Meta cumplida»; si la supera, «120 de 100», con el anillo
  cerrado. La primera vez que se dibuja después de cumplirla (al volver a la lista de mazos tras
  repasar), el ✓ aparece con un leve aumento de 150 ms; si Anki o el sistema piden reducir las
  animaciones (en Anki viene así de serie), aparece con un fundido de 150 ms, sin moverse. No se
  repite al volver a la pantalla.
- Con la meta «Terminar lo de hoy»: lo mismo, en tarjetas: las respondidas hoy frente a esas más las
  que aún vencen hoy (con los límites diarios de Anki y sin los mazos excluidos). Una vez cumplida,
  queda cumplida el resto del día aunque vuelvan a vencer tarjetas en aprendizaje; solo vuelve atrás
  (sin animación) si deshace la respuesta que la cumplió.
- La meta se elige en Opciones, «Metas y fechas» > «Meta diaria».
- En la pantalla de un mazo, el título es «Hoy en este mazo», con lo hecho hoy en ese mazo y sus 7
  días, sin meta: la meta es de toda la colección.
- Con «Mostrar racha y meta» desactivado, lo hecho hoy y sus 7 días, sin meta.

### Racha

Días seguidos estudiando hasta hoy («18 días»). Cuenta cualquier respuesta, sea cual sea lo que mide
el color: con «Nuevas», un día en que solo repasó también cuenta. La racha no se rompe por no haber
estudiado todavía hoy. La línea gris dice, por este orden (si no cabe, se corta por el final, así que
lo último en perderse es si hoy ya cuenta):

- «✓ hoy» si hoy ya cuenta, u «hoy pendiente» si todavía no;
- «· en pausa hasta el 5 nov.» mientras dure una pausa de la racha (la fecha, en el idioma de Anki);
- «· 1 comodín» o «· 2 comodines» si tiene comodines guardados (subrayado de puntos: al pasar el
  ratón o llegar con el tabulador, «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin
  estudiar gasta uno.»);
- «· a 3 días del récord» si la racha más larga está a 7 días o menos y es de 7 días o más, o
  «· récord: 40 días» en los demás casos (si la racha actual es la más larga, no se añade nada);
- «· Un año seguido» el día en que la racha llega a 365 días (y a 730, 1.095…).

Casos especiales: si nunca ha estudiado, «0 días» y «hoy pendiente»; si la racha está a cero,
«0 días» y «Última sesión hace 3 días»; al volver tras romperla, «Día 1» y «récord: 45 días».

### Promedio diario

Lo hecho por día estudiado, en la unidad de la medida («72 repasos», «60 tarjetas», «8 nuevas»), en el
periodo de las cifras, contando solo días completos (el periodo termina ayer). Debajo, solo el
periodo: «últimos 30 días», «último año» o «todo el historial». Sin días completos estudiados escribe
«N/A» en
gris, subrayado de puntos: al pasar el ratón (o llegar con el tabulador), «Sin días completos
estudiados en los últimos 30 días» (o «… en todo el historial»). Con «Nuevas», un promedio que se
queda en 0 también es «N/A», con «Menos de una nueva por día estudiado…».

### Retención

El porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención real de Anki
(tarjetas con al menos un día de intervalo), en el periodo de las cifras (Opciones). Debajo, el periodo:
«últimos 30 días», «último año» o «todo el historial». Usa el mismo periodo que el promedio: días
completos que terminan ayer. Con menos de 20 respuestas que contar escribe «N/A» (el texto de Anki),
en gris y subrayado de puntos: al pasar el ratón, «Menos de 20 respuestas en los últimos 30 días» (o
«… en todo el historial»). En la pantalla de un mazo con FSRS activado añade la retención
deseada de su configuración: «· objetivo 90 %».

### Próxima fecha

La próxima fecha clave de hoy en adelante: «faltan 23 días», «falta 1 día» o «es hoy», sin estrella.
Debajo, solo su nombre (varias el mismo día, separadas por « · »): «Examen de Anatomía», sin el día
de la semana. Sin fechas
por venir: «N/A» en gris y, debajo, «sin fechas clave», en minúscula. Las fechas se añaden en
Opciones > «Gestionar fechas». La tarjeta nunca desaparece.

## 4. La tarjeta del mapa

- Sin título ni cifras encima: «‹ 2026 ›» (año anterior y siguiente, botones de 28 × 28 px con su
  nombre al pasar el ratón), centrado sobre el mapa, y el botón de opciones aparte, en la esquina de
  arriba (a la derecha; a la izquierda en los idiomas que se escriben de derecha a izquierda). No hay
  botón «Hoy». Las flechas se ven apagadas en el primer año con repasos y en el último con
  vencimientos o fechas clave; al pulsarlas no pasa nada, pero siguen diciendo su nombre al pasar el
  ratón y el lector de pantalla las anuncia como no disponibles.
- El año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki (siempre con el calendario gregoriano) y, a la izquierda,
  las iniciales de lunes, miércoles y viernes («L», «X», «V» en español), en gris. El dibujo es
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
  nombre y su cuenta atrás. Las ya pasadas llevan la estrella en gris, para que la próxima destaque.
  Con cuadritos de menos de 14 px (con un tamaño pequeño o con «Ajustado al ancho» en una ventana
  estrecha), la estrella no cabe dentro: sube a una fila propia entre los meses y el mapa, encima de
  la columna de su semana, y el cuadrito queda normal.
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
  «Su mejor semana del año» (los 7 últimos días, hoy incluido, suman más que cualquier otra semana
  anterior del año, con al menos cuatro semanas con que comparar), «Mes completo» (el último día del
  mes, si respondió alguna tarjeta todos sus días; los perdonados no cuentan como estudiados) y «1.000 repasos este año»
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
ver las que vencen ese día». El globo no dice nada de la meta. La tecla Esc lo cierra. Se puede llevar
el ratón encima del globo sin que se cierre; al salir, se cierra tras un instante. Su letra es de
13 px. En español:

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

Con el teclado, un solo día del mapa recibe el tabulador (hoy, o el 1 de enero en otro año) y, desde
él: las flechas arriba y abajo van al día anterior o siguiente; a los lados, a la semana anterior o
siguiente; Inicio y Fin, al lunes y al domingo de esa semana; RePág y AvPág, al mismo día del mes
anterior o siguiente; Mayús+RePág y Mayús+AvPág, al mismo día del año anterior o siguiente. Si el día
cae en otro año, el mapa cambia de año y el foco llega a ese día (si no hay año al que ir, no pasa
nada).

## 7. Comodines y pausa

- Comodines (activados por defecto; se desactivan en Opciones): cada 7 días seguidos estudiados se
  gana uno, con un máximo de 2 guardados. Esos 7 días se cuentan desde el último día sin estudio,
  aunque lo cubriera un comodín o la pausa, y la cuenta vuelve a empezar al llegar a 7, se gane o no
  (si ya tiene 2): así no se ganan comodines mientras se gastan. Un día sin estudiar gasta uno automáticamente al empezar el
  día siguiente: la racha no se rompe, pero tampoco suma ese día. Sin comodines, el día sin estudiar
  rompe la racha. Se ganan estudiando; no se compran ni se piden.
- Pausa de la racha: en Opciones, de un día a otro, de 1 a 30 días, empezando hoy como pronto (una
  pausa ya guardada que empezó antes conserva su inicio). Mientras dura, la tarjeta «Racha» lo dice. Un día de pausa sin estudiar ni
  suma ni rompe la racha y no gasta comodines; un día de pausa en que estudió cuenta como siempre. Se
  ven como los perdonados.
- La meta nunca afecta a la racha: basta una respuesta, de la medida que sea, para que el día cuente.
- El «hoy» de la racha y del mapa es el de Anki: el día empieza a la hora que marca Anki en
  Preferencias (por defecto, las 4 de la madrugada), y lo estudiado antes cuenta para el día anterior.

## 8. Ventana de opciones

Título «GritMap». Se abre después de leer los mazos y las opciones sin congelar Anki (un segundo clic
mientras tanto no abre otra), delante de la ventana desde la que se pidió. Tres recuadros con título
(«Apariencia», «Qué se cuenta» y «Metas y fechas»), con controles estándar de Anki, y los botones
«Restaurar apariencia» (a la izquierda; al pasar el ratón, «No cambia los mazos excluidos ni las
fechas clave»), Aceptar y Cancelar (en el orden de cada sistema; Esc cancela). Intro pulsa el botón que tiene el foco. Recuerda
su ancho y su posición; el alto es siempre el que piden sus opciones, sin huecos. Al aceptar, el mapa se redibuja en su sitio, sin recargar la pantalla.

En este orden:

| Recuadro | Opción | Valores | Por defecto |
|---|---|---|---|
| Apariencia | Tema de color | Verde clásico, Azul océano, Púrpura real y Naranja atardecer (el de serie primero y los demás por tono), cada uno con un cuadrito de su tono en el modo activo (cambia si Anki pasa de día a noche) | Verde clásico |
| Apariencia | Tamaño del mapa | Campo numérico con flechas, de 10 px a 60 px (el lado de cada cuadrito; el mapa entero crece en proporción) y, al lado, la casilla «Ajustado al ancho», que apaga el campo y hace que el mapa ocupe todo el ancho | 24 px, sin la casilla |
| Apariencia | Redondeo de esquinas | Campo numérico con flechas, de 0 px a la mitad del tamaño elegido (7 px con «Ajustado al ancho»; más ya no cambiaría nada) | 3 px |
| Qué se cuenta | El color mide | Tres botones de opción: Repasos, Tarjetas, Nuevas; debajo, «Cada respuesta cuenta una», «Cada tarjeta cuenta una vez por día» o «Solo las tarjetas que empezó ese día» | Repasos |
| Qué se cuenta | Periodo de las cifras | Tres botones de opción, como «El color mide»: «30 días», «365 días» y «Todo el historial»; debajo, «Vale para el promedio diario y la retención.» | 30 días |
| Qué se cuenta | Excluir mazos | Botón «Seleccionar mazos» (o «1 mazo excluido», «2 mazos excluidos», con hasta 15 nombres al pasar el ratón y «…» si hay más); debajo, «La medida y los mazos excluidos se aplican al aceptar.» | Ninguno |
| Metas y fechas | Mostrar racha y meta | Casilla, la primera del recuadro. Desmarcada, la meta, los comodines y la pausa se ven apagados | Marcada |
| Metas y fechas | Meta diaria | «Sin meta», «Un número» (con el número, de 1 a 9.999, en la unidad de la medida) o «Terminar lo de hoy». Al elegir «Un número» se propone el 80 % de su promedio de los últimos 30 días en esa unidad, redondeado a 5; sin historial, 50 repasos, 30 tarjetas o 10 nuevas. Si cambia la medida sin haber tocado el número, se propone otro en la unidad nueva | Sin meta |
| Metas y fechas | Comodines | Casilla «Perdonar días sueltos con comodines»; debajo, escrita, la regla: «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin estudiar gasta uno.» | Marcada |
| Metas y fechas | Pausa | Casilla «Pausar la racha» con las fechas de inicio (hoy como pronto) y fin (como mucho 29 días después del inicio) y, al lado, cuántos días dura («15 días»); debajo, «La pausa dura 30 días como máximo.» | Desmarcada |
| Metas y fechas | Fechas clave | Botón «Gestionar fechas» (o «1 fecha marcada», «3 fechas marcadas», con la lista al pasar el ratón) | Ninguna |

- Mientras cambia el tema, el tamaño o el redondeo, el mapa de detrás cambia al momento (un
  instante después de soltar la flecha), sin guardar nada; si cancela, vuelve a como estaba. La medida
  y los mazos excluidos se ven al aceptar, porque piden leer la colección.
- «Restaurar apariencia» repone solo el recuadro «Apariencia»: tema, tamaño y redondeo. No toca la
  medida, los mazos excluidos, las fechas clave, la meta, los comodines, la pausa ni el periodo.
- Un tamaño de 8 o 9 px guardado por versiones anteriores pasa a 10 px.
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
- Fechas clave: lista en dos columnas, ordenada por fecha: fecha corta (con el año en cuatro cifras) y
  nombre; las ya pasadas, en gris y con «(pasada)» tras la fecha. Un doble clic en el nombre permite
  corregirlo en la propia lista (si queda vacío o repetido, vuelve al de antes); el botón
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
- Tamaños de letra: 20 px para el dato de cada tarjeta, 13 px para las líneas grises de las tarjetas
  y el globo, y 12 px para los meses, la leyenda y el resto; las iniciales de los días, 11 px. La
  jerarquía se marca con el grosor y el gris. La letra es la de Anki.
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
  la meta (con animaciones reducidas, un fundido).

## 14. Lo que se probó y se descartó

Todo lo que tuvo alguna versión y ya no está (o cambió de forma), lo que se propuso y no se aplicó, y
el motivo. Sirve para no volver a ello sin querer.

### En el mapa

| Descartado o cambiado | Versión | Por qué |
|---|---|---|
| Recuadro alrededor del mapa | 3.3.0 | El cliente lo quería sin él; desde la 4.0.0 el mapa va en una tarjeta. |
| Iniciales de los días a la izquierda | 3.3.0 (vuelven en 4.7.0) | Se quitaron a petición del cliente; volvieron con el informe de mejora integral (L, X, V). |
| Botones que fundían el color al pasar el ratón | 3.2.0 | La guía del taller pide no animar el color; ahora solo se hunden al pulsarlos. |
| Siete temas de diez tonos | 4.0.0 | Diez tonos no se distinguían entre sí; quedan cuatro temas de cuatro tonos. |
| Temas Rojo fuego, Rosa suave y Turquesa laguna | 4.0.0 | El rojo significa error; los otros dos repetían Púrpura y Azul. Se pasa sin preguntar al más parecido. |
| Globo del año con signo de exclamación | 4.0.0 | Se sustituyó por la cifra del año en el título, que a su vez se quitó en la 4.3.0. |
| Comparativa semanal junto a la línea de Anki | 4.0.0 | Pasó a la tarjeta de estadísticas, retirada en la 4.1.0. |
| Ocupar todo el ancho como única forma | 4.2.0 | Resultaba demasiado grande. Queda como la casilla «Ajustado al ancho». |
| «Ajustado al ancho» como valor de serie | 4.6.0 | El cliente prefirió 24 px de serie. |
| Encoger el cuadrito cuando el año no cabe («24 px o lo que quepa») | Propuesto en 4.7.0, no aplicado | El cliente prefirió 24 px siempre, con desplazamiento de lado. |
| Hueco fijo de 3 px entre cuadritos con cualquier tamaño | 4.5.0 | Al cambiar el tamaño, las líneas entre filas y columnas perdían la proporción. Ahora el hueco crece con el cuadrito. |
| Título «Actividad» y cifra del año («22.129 repasos en 2026») encima del mapa | 4.3.0 | El cliente los quería fuera: no aportaban y ocupaban sitio. |
| Botón «Hoy» (primero solo en otro año, luego siempre visible) | 4.4.0 | El mapa ya se abre en la semana de hoy. |
| Botón de opciones junto a «‹ 2026 ›» | 4.7.0 | Navegar y configurar son cosas distintas; va aparte, en la esquina (decisión del cliente). |
| «Meta cumplida» escrita en el mapa y la meta en el globo de los días | 4.1.0 | Repetía lo que ya dice la tarjeta «Hoy». |
| Punto para los días con tarjetas pendientes | 4.1.0 | El cliente prefirió el marcado de antes: cuatro grises según las tarjetas que vencen. |
| Grises de pendientes más suaves | Propuesto en 4.7.0, pendiente | Para quedar más suaves que el primer tono del tema dejarían de distinguirse entre sí. Espera la decisión del cliente (tres grises más suaves o los cuatro de ahora). |
| Fechas clave con borde naranja (o azul) | 4.0.0 | Pasaron a una ★ sobre su semana. |
| ★ sobre la semana de la fecha clave | 4.1.0 | El cliente pidió otra manera de encontrarlas; pasó a una esquina doblada. |
| Esquina doblada en el cuadrito de la fecha clave | 4.2.0 | Se veía poco. Se cambió por una estrella dentro del cuadrito. |
| Salto o enlace desde «Próxima fecha» hasta su día en el mapa | 4.2.0 | El cliente no quiere enlaces. |
| Línea de sorpresa «Su mejor día del año» | 4.7.0 | Premiaba un día enorme, que empuja a estudiar a atracones. Ahora es «Su mejor semana del año». |
| Iniciales de los días a la derecha en árabe y hebreo | Propuesto en 4.7.0, no aplicado | La rejilla va siempre de izquierda a derecha (corrección FIX-023), así que las iniciales van a la izquierda. |
| Que el lector de pantalla anuncie el año al cambiarlo y el texto «No hay repasos antes de…» en las flechas apagadas | Propuesto en 4.7.0, no aplicado | Piden textos nuevos en 51 idiomas o el lector no los anunciaría bien; a la espera de que el cliente los pida. |

### En las tarjetas de debajo

| Descartado o cambiado | Versión | Por qué |
|---|---|---|
| Llama de la racha y globos de motivación | 3.5.0 | Los descartó el cliente: presionan en lugar de informar. |
| Globo explicativo de la retención | 2026-10-09 | Lo retiró el cliente. (En la 4.7.0 se añadió solo para explicar el «N/A»; véase el aviso de la entrega.) |
| Periodos de 7 y 90 días | 3.x | Se quedaron 30 días, 1 año y todo el historial (cliente, 2026-10-13). |
| Botones de periodo en la página (junto al año, luego encima de las cifras, luego en la tarjeta de estadísticas) | 4.1.0 | El periodo se elige solo en Opciones. Las tarjetas dicen cuál se usa. |
| Raya entre los dos grupos de cifras | 3.6.0 | Los separaba el espacio; después los grupos se convirtieron en tarjetas. |
| Cuadritos de color delante de las cifras | 4.0.0 | Usaban un color sin explicar. |
| Tarjeta de estadísticas plegable (constancia de la semana, dos barras, anillos de días estudiados y meta cumplida) | 4.1.0 | Sobraba. La sustituyó «Promedio diario»; el récord pasó a la línea de «Racha». |
| Tarjetas encima o al lado del mapa | 4.1.0 | El cliente las quería debajo, sumando el ancho del mapa. |
| Estrella junto a «Próxima fecha» | 4.1.0 | No hacía falta: la estrella marca el día en el mapa. |
| Enlaces dentro de las tarjetas («Fijar meta», «Añadir» fechas, ir a los mazos excluidos) y la ventanita «Fijar meta» | 4.2.0 | El cliente no quiere enlaces. Todo se cambia en Opciones. |
| La fecha al lado del nombre en «Próxima fecha» | 4.3.0 | Ya dice cuántos días faltan. |
| «Sin fechas clave» como dato grande | 4.4.0 | Ahora pone «N/A», como las demás tarjetas sin dato, y debajo «sin fechas clave». |
| «Récord» con mayúscula en medio de la línea | 4.1.0 | Va en medio de una frase: «récord». |
| Racha contada en la medida del color | 4.7.0 | Con «Nuevas», un día de solo repasos rompía la racha o gastaba un comodín. Ahora cuenta cualquier respuesta (cliente, 2026-10-22). |
| «a 3 días del récord» con récords muy cortos | 4.7.0 | Con un récord de 3 días salía al día siguiente de empezar; ahora solo si el récord es de 7 días o más. |
| Meta «Terminar lo de hoy» que se descumplía | 4.7.0 | Las tarjetas en aprendizaje volvían a vencer; ahora, cumplida, queda cumplida ese día (FIX-026). |
| «por día estudiado» en la línea de «Promedio diario» | 4.7.1 | Probado en la 4.7.0; el cliente lo quitó: la línea dice solo el periodo. |
| Día de la semana delante del nombre en «Próxima fecha» («jueves · Examen») | 4.7.1 | Probado en la 4.7.0; el cliente lo quitó: queda solo el nombre. |

### En la ventana de opciones

| Descartado o cambiado | Versión | Por qué |
|---|---|---|
| «Tamaño» (Ajustado / Grande) y «Forma» (Cuadrado / Redondeado) | 4.2.0 | El cliente quería el tamaño y el redondeo en píxeles, como en las primeras versiones. |
| Mes de muestra (vista previa) dentro de Opciones | 4.2.0 | Se sustituyó por el propio mapa, que cambia en vivo detrás de la ventana. |
| Barras deslizantes para el tamaño y el redondeo | 4.3.0 | Se veían raras. Volvieron los campos numéricos con flechas. |
| Opciones en una sola lista, sin recuadros | 4.4.0 | El cliente prefirió los tres recuadros con título. |
| Hueco entre «Apariencia» y «Qué se cuenta» | 4.3.0 | Venía de una altura guardada por otra versión. Ahora el alto se ajusta siempre al contenido. |
| «Tamaño de celda» | 4.5.0 | Pasó a «Tamaño del mapa»: agranda o encoge el mapa entero. |
| Redondeo en la escala de un cuadrito de 14 (de 0 a 7) | 4.6.0 | El cliente lo quería en píxeles, con «px» al final. |
| «Ajustado al ancho» como primer valor del campo de tamaño | 4.7.0 | Escondido bajo el número no se descubría. Ahora es una casilla al lado. |
| Tamaños de 8 y 9 px | 4.7.0 | Por debajo de 10 px no se distinguen los cuadritos; un valor guardado así pasa a 10. |
| Redondeo por encima de la mitad del cuadrito | 4.7.0 | No cambiaba nada; el campo llega como mucho a la mitad. |
| «El color mide» como lista desplegable | 4.7.0 | Con tres valores, tres botones se leen de un vistazo. |
| «Periodo de las cifras» como lista desplegable | 4.7.1 | El cliente lo quiso en tres botones, como «El color mide». |
| «Restaurar apariencia» reponía también la medida | 4.7.0 | La medida está en otro recuadro; ahora repone solo «Apariencia». |
| Reglas de comodines y pausa solo al pasar el ratón | 4.7.0 | Casi nadie descubre un globo; ahora van escritas debajo. |
| «Mostrar racha y meta» al final del recuadro | 4.7.0 | Ahora va primero y apaga lo que depende de ella. |
| Meta propuesta fija de 50 | 4.7.0 | Ahora se propone según su historial y en la unidad de la medida. |
| Pausa que empieza en un día pasado | 4.7.0 | Servía para tapar después un fallo; los fallos sueltos ya los cubren los comodines (decisión del cliente). |
| Temas por orden alfabético | 4.7.0 | El de serie va primero y los demás por tono. |
| Tira de cuatro tonos como muestra de cada tema | Propuesto en 4.7.0, no aplicado | Se mantiene un solo cuadrito, como pidió el cliente con una captura en la 4.3.0. |
| Letras subrayadas para manejar Opciones con Alt | Propuesto en 4.7.0, no aplicado | Piden cambiar los textos en 51 idiomas; a la espera de que el cliente lo pida. |

### Otros

| Descartado | Por qué |
|---|---|
| Medida «minutos» | Hay días con cientos de repasos guardados sin tiempo, así que la cifra no era coherente (decisión del cliente, 2026-10-08). |
| Mapa encima de la lista de mazos | Anki no ofrece a los complementos ese sitio. Va debajo (decisión del cliente). |
| Avisos, cuentas atrás de pérdida, premios al azar, puntos, insignias y clasificaciones | Presionan o crean dependencia en lugar de informar; descartados desde la 3.6.0 y confirmados en el informe de la 4.7.0. |
