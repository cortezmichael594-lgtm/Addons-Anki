# Qué hace «GritMap»

Versión 4.10.0 · 2026-10-26

Mapa de calor de su estudio, como el de las contribuciones de GitHub, en tarjetas. Cuenta tarjetas: cada
tarjeta respondida cuenta una vez por día, aunque la conteste varias veces. Arriba, centrada y
con cuadritos de 24 px de serie (con el dibujo de la versión 4.1.0), la tarjeta del mapa, con el año entero (un cuadrito por día: gris sin estudio y cuatro tonos
del tema; los días que vienen, en tres grises suaves según las tarjetas que vencen). Debajo, hasta
cinco tarjetas pequeñas del mismo ancho entre todas, que responden de un vistazo: «Hoy», «Racha»,
«Promedio diario», «Retención» y, solo si tiene alguna fecha clave por venir, «Próxima fecha». Tiene una meta diaria opcional, comodines que perdonan días
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
  pantalla y sus cuadritos crecen o encogen con la ventana (nunca por debajo de 10 px). Las tarjetas
  pequeñas (de tres a cinco) van debajo y suman el ancho visible del mapa, con los bordes alineados
  con los de su tarjeta. Cada tarjeta tiene el fondo un punto más claro
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

Hasta cinco tarjetas del mismo ancho, que suman el ancho del mapa: «Hoy», «Racha» (no sale si se
desactiva «Mostrar racha y meta»), «Promedio diario», «Retención» y «Próxima fecha» (solo si hay
alguna fecha clave de hoy en adelante). Así quedan cinco, cuatro o tres. Cada una tiene un título, un dato grande y una línea gris de hasta dos renglones (si no
cabe, se corta con «…» y se lee entera al pasar el ratón). No tienen enlaces: al pulsarlas no pasa
nada. Se reordenan según el ancho del mapa: por debajo de 940 px, dos por fila (con cinco o con tres,
la última a lo ancho de las dos para que la fila quede cuadrada) y, por debajo de 420 px, una.

### Hoy

- Sin meta: las tarjetas respondidas hoy («35 tarjetas») y, debajo, las de los 7 últimos días
  completos (terminan ayer): «448 tarjetas en 7 días».
- Con la meta «Un número»: un anillo pequeño que se llena con lo hecho, «80 de 100» y, debajo,
  «faltan 20 tarjetas». Al cumplirla, «✓ Meta cumplida»; si la supera, «120 de 100», con el anillo
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

Días seguidos estudiando hasta hoy («18 días»). Cuenta cualquier respuesta. La racha no se rompe por no haber
estudiado todavía hoy. La línea gris dice, por este orden (si no cabe, se corta por el final, así que
lo último en perderse es si hoy ya cuenta):

- «✓ hoy» si hoy ya cuenta, u «hoy pendiente» si todavía no;
- «· en pausa hasta el 5 nov.» mientras dure una pausa de la racha (la fecha, en el idioma de Anki);
- «· 1 comodín» o «· 2 comodines» si tiene comodines guardados (subrayado de puntos: al pasar el
  ratón o llegar con el tabulador, «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin
  estudiar gasta uno.»);
- «· a 3 días del récord» si la racha más larga está a 7 días o menos y es de 7 días o más, o
  «· récord: 40 días» en los demás casos (si la racha actual es la más larga, no se añade nada).

Casos especiales: si nunca ha estudiado, «0 días» y «hoy pendiente»; si la racha está a cero,
«0 días» y «Última sesión hace 3 días»; al volver tras romperla, «Día 1» y «récord: 45 días».

### Promedio diario

Las tarjetas al día, de media («41 tarjetas»), en el periodo de las cifras: lo hecho en el periodo
dividido entre sus días, también los que no estudió. Quien estudia 4 días de cada 7, con 72 tarjetas
esos días, ve 41. Así la cifra sube al estudiar más
días, no solo más cada día. Reglas: solo días completos (el periodo termina ayer); se cuenta desde el
primer día con estudio dentro del periodo (quien empezó hace 10 días no se divide entre 30); los días
de pausa no cuentan; los cubiertos por un comodín sí, porque no se estudió. Debajo, solo el periodo:
«últimos 30 días», «último año» o «todo el historial». Sin ningún día completo estudiado en el periodo
escribe «N/A» en gris, subrayado de puntos: al pasar el ratón (o llegar con el tabulador), «Sin días
completos estudiados en los últimos 30 días» (o «… en todo el historial»). Los cortes de color del mapa y la meta que se propone en Opciones siguen calculándose por día estudiado.

### Retención

El porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención real de Anki
(tarjetas con al menos un día de intervalo), en el periodo de las cifras (Opciones). Debajo, el periodo:
«últimos 30 días», «último año» o «todo el historial». Usa el mismo periodo que el promedio: días
completos que terminan ayer. Con menos de 20 respuestas que contar escribe «N/A» (el texto de Anki),
en gris y subrayado de puntos: al pasar el ratón, «Menos de 20 respuestas en los últimos 30 días» (o
«… en todo el historial»). Con FSRS activado, el porcentaje va subrayado de puntos y, al pasar el
ratón o llegar con el tabulador, dice la retención deseada: «Objetivo 90 %». Sale en la pantalla de un
mazo (la de su configuración) y también en la lista de mazos si todos los mazos que cuentan usan la
misma; si usan retenciones distintas, en la lista de mazos no hay globo. La línea gris solo dice el
periodo.

### Próxima fecha

Solo aparece si hay alguna fecha clave de hoy en adelante; si no, no hay tarjeta y las demás se
reparten el ancho. Dice la próxima: «faltan 23 días», «falta 1 día» o «es hoy» (siempre en días,
aunque falten meses), sin ninguna marca. Debajo, solo su nombre (varias el mismo día, separadas por
« · »): «Examen de Anatomía», sin el día de la semana. Al día siguiente de la última fecha, la tarjeta
desaparece. La cuenta atrás es neutra: no cambia de color ni de aspecto al acercarse la fecha. Las
fechas se añaden en Opciones > «Gestionar fechas».

## 4. La tarjeta del mapa

- Sin título ni cifras encima: «‹ 2026 ›» (año anterior y siguiente, botones de 28 × 28 px a 5 px de
  la cifra, con su nombre al pasar el ratón), centrado sobre el mapa, y el botón de opciones aparte, en la esquina de
  arriba (a la derecha; a la izquierda en los idiomas que se escriben de derecha a izquierda). No hay
  botón «Hoy». Las flechas se ven apagadas en el primer año con repasos y en el último con
  vencimientos o fechas clave; al pulsarlas no pasa nada, pero siguen diciendo su nombre al pasar el
  ratón y el lector de pantalla las anuncia como no disponibles. Al cambiar de año, el lector de
  pantalla dice la cifra del año («2025»).
- El año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki (siempre con el calendario gregoriano) y, a la izquierda,
  las iniciales de lunes, miércoles y viernes («L», «X», «V» en español), en gris. El dibujo es
  siempre el mismo, como en la 4.1.0: el hueco mide 3/14 del cuadrito y las esquinas, el redondeo
  elegido en píxeles (3 px de serie). Cada cuadrito mide el tamaño elegido (24 px de serie) y todo lo
  demás crece con él; con «Ajustado al ancho», el año llena el ancho de la tarjeta y el redondeo es el
  de un cuadrito de 14 px.
  Si el año no cabe, se desplaza de lado: al abrir un año se ve la semana de hoy; en un año pasado,
  diciembre, y en uno futuro, enero. Mientras quede mapa por ver a un lado, ese borde se desvanece
  suavemente, para que se note que sigue; al llegar al final, el degradado se va. Las tarjetas de
  debajo miden el ancho visible, nunca el del año entero. Las iniciales de los días se desplazan con
  el mapa.
- Días pasados y hoy: cinco niveles. Sin estudio, el gris vacío; con estudio, cuatro tonos del tema,
  repartidos según su promedio de siempre en los días que estudió (con un mínimo, para que al empezar
  no salga todo oscuro): hasta la mitad del promedio, hasta el promedio, hasta el doble y más del
  doble.
- Días futuros con tarjetas que vencen: en tres grises suaves, algo más marcados cuantas más tarjetas
  vencen: poca carga (hasta la mitad de su promedio de tarjetas), normal (hasta vez y media) y mucha.
  Los tres son más suaves que el primer tono de cualquier tema, para que lo que viene no pese a la
  vista más que lo hecho. Lo atrasado no se dibuja.
- Hoy lleva un borde del color del texto.
- Las fechas clave llevan un rombo de hito (◆) en su cuadrito, la marca con que los cronogramas
  señalan una fecha. La de hoy y las que vienen, rombo lleno en el color del texto con un filo del
  color de la tarjeta, que se ve sobre cualquier tono y es igual en todos los temas; las ya pasadas,
  rombo hueco en gris, para que la próxima destaque. Se lee a cualquier tamaño, también con cuadritos
  de 10 px. Al pasar el ratón, su nombre y su cuenta atrás.
- Un día perdonado por un comodín o por la pausa queda vacío (no estudió), con un borde fino
  discontinuo.
- Al pasar el ratón por un día, el cuadrito se resalta; si se puede pulsar, el puntero cambia a una
  mano y el globo lo dice.
- El color mide tarjetas: las tarjetas distintas respondidas ese día (no cuentan los cambios manuales
  de fecha ni las reprogramaciones). Desde la 4.10.0 no se puede elegir otra medida.
- Debajo, a la derecha, la leyenda: «Menos», los cinco cuadritos del mapa y «Más». Al pasar el ratón
  por cada uno, las cifras que cubre, calculadas con su promedio actual: «Ningún repaso», «de 1 a 20
  tarjetas», «de 21 a 40 tarjetas», «de 41 a 80 tarjetas» y «81 tarjetas o más». Detrás, «Pendientes» (un gris) si en el año que se ve hay días pendientes, «Fecha clave»
  (el rombo) si ese año tiene alguna, y «Perdonado» (el borde discontinuo) si hay días
  perdonados.
- Debajo, a la izquierda, como mucho una línea de sorpresa al día, solo cuando ocurre y con datos
  reales, por este orden: «Un año seguido» (el día en que la racha llega a 365 días, y a 730, 1.095…;
  es la más rara y la primera), «Nueva racha más larga» (el día en que la racha supera la mejor
  anterior),
  «Su mejor semana del año» (los 7 últimos días, hoy incluido, suman más que cualquier otra semana
  anterior del año, con al menos cuatro semanas con que comparar), «Mes completo» (el último día del
  mes, si respondió alguna tarjeta todos sus días; los perdonados no cuentan como estudiados) y «1.000 tarjetas este año»
  (el día en que el total del año cruza 100, 500 o un múltiplo de 1.000). Solo si hoy ya cuenta.
- En árabe, hebreo, persa y uigur, la navegación del año, el mapa y su pie van de izquierda a derecha,
  como el calendario; el resto sigue la dirección del idioma.
- Cambiar de año o de tema, tamaño, redondeo, periodo de las cifras, meta, comodines o pausa no vuelve a leer la
  colección: es inmediato. Cambiar los mazos excluidos sí la vuelve a leer, sin quitar el mapa mientras
  tanto.
- Ningún texto del mapa ni de sus tarjetas se puede seleccionar con el ratón.

### Cuando no hay nada que dibujar

- En una colección sin repasos, sin vencimientos y sin fechas clave: la cuadrícula del año actual en
  gris con hoy marcado y, debajo, «Cada día que estudie se pintará aquí.», sin leyenda y con las
  flechas de año apagadas; y debajo, las tarjetas («0 tarjetas» con «0 tarjetas en 7 días», «0 días»
  con «hoy pendiente», y promedio y retención «N/A»; sin tarjeta «Próxima fecha»).
- En la pantalla de un mazo excluido: una tarjeta con «Este mazo está excluido del mapa.»
  y el botón de opciones.
- Si algo falla: una tarjeta con «No se pudo cargar el mapa de calor.», debajo «Vuelva a abrir Anki;
  si se repite, el detalle está en el registro del complemento.», y el botón de opciones.

## 5. Al pasar el ratón por un día (o llegar a él con el teclado)

Sale un globo con la fecha larga en el idioma de Anki (sin «el»), en gris, y, en la línea de abajo, lo
hecho ese día. Después, en gris y según el caso: si el día está perdonado, «Perdonado con un comodín»
o «Racha en pausa»; y en los días que se pueden pulsar, «Pulse para ver estas tarjetas» o «Pulse para
ver las que vencen ese día». El globo no dice nada de la meta. La tecla Esc lo cierra. Se puede llevar
el ratón encima del globo sin que se cierre; al salir, se cierra tras un instante. Su letra es de
13 px. En español:

- «lunes, 22 de junio de 2026» / «**9** **tarjetas**» (o «1 tarjeta»).
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
- La meta nunca afecta a la racha: basta una respuesta para que el día cuente.
- El «hoy» de la racha y del mapa es el de Anki: el día empieza a la hora que marca Anki en
  Preferencias (por defecto, las 4 de la madrugada), y lo estudiado antes cuenta para el día anterior.

## 8. Ventana de opciones

Título «GritMap». Es un panel hecho a medida, del mismo material que las tarjetas del mapa (el fondo
de Anki, tarjetas de capa elevada con borde suave y esquinas redondeadas, la letra de Anki), de día y
de noche. Un solo azul, el de Anki, marca lo que se pulsa, lo elegido y el foco del teclado; los
colores de los temas solo aparecen en sus muestras. No hay animaciones. La letra es de 12 px (los
títulos, de 14 y 15 px) y ningún texto se puede seleccionar con el ratón, salvo lo que se escribe en
los campos.

- Se abre al instante, delante de la ventana desde la que se pidió, con las opciones guardadas; la
  lista de mazos se lee después sin congelar Anki (mientras tanto, la fila «Excluir mazos» muestra un
  hueco gris). Un segundo clic no abre otra: trae la que ya está abierta. El contenido no se ve hasta
  que está dibujado entero (si por algo tardara, a los 3 segundos se ve igualmente).
- Mide 560 px de ancho y el alto de la página principal, como mucho 720 px (o el de la pantalla
  menos 80 px, si es menor). El alto se fija al abrir y no cambia al entrar en las subpáginas; lo que no
  cabe se desplaza dentro del cuerpo, con la cabecera («Opciones») y el pie (Cancelar y Aceptar)
  siempre fijos. Recuerda su posición.
- Arriba, si tenía el tema retirado Rojo fuego, una franja gris con un icono de información lo dice
  una vez: «Su tema «Rojo fuego» se ha retirado; ahora usa «Naranja atardecer».». Pasa sin preguntar
  a Naranja atardecer. (Rosa suave y Turquesa laguna volvieron en la 4.10.0: quien los tenía guardados
  los recupera.)
- Nada se guarda hasta pulsar Aceptar. Al aceptar, el mapa se redibuja en su sitio, sin recargar la
  pantalla. Aceptar y Cancelar van en el orden de cada sistema (en Windows, Aceptar primero).

### Tarjeta «Apariencia»

En su título, a la derecha, «Restaurar apariencia»: vuelve al tema, tamaño y redondeo de serie (Verde
clásico, 24 px, 3 px), solo de esta tarjeta, y junto a él aparece «Deshacer» hasta el siguiente cambio;
como no se guarda nada, Cancelar también lo deshace. Debajo del título: «Se ve ya en el mapa; se guarda
al aceptar.»: mientras cambia el tema, el tamaño o el redondeo, el mapa de detrás cambia al momento, y
si cancela vuelve a como estaba.

| Opción | Cómo se elige | Por defecto |
|---|---|---|
| Tema de color | Seis fichas en dos columnas (una si algún nombre no cabe), por orden alfabético del nombre en el idioma de Anki (en español: Azul océano, Naranja atardecer, Púrpura real, Rosa suave, Turquesa laguna y Verde clásico), cada una con un cuadrito de su tono en el modo activo (cambia si Anki pasa de día a noche con la ventana abierta). La elegida lleva borde azul, fondo suave y ✓. Con el tabulador se entra en la elegida y las flechas cambian de tema | Verde clásico |
| Tamaño del mapa | Campo con «−», el número con «px» y «+», de 10 a 60 (el lado de cada cuadrito; el mapa entero crece en proporción). Debajo, la casilla «Ajustado al ancho»: marcada, apaga el campo y dice «El mapa ocupa todo el ancho; los cuadritos miden al menos 10 px.» | 24 px, sin la casilla |
| Redondeo de esquinas | Campo con «−» y «+», de 0 px hasta la mitad del cuadrito; debajo lo dice: «Hasta la mitad del cuadrito (12 px).» (7 px con «Ajustado al ancho») | 3 px |

Los campos con «−» y «+»: se puede escribir el número; las flechas arriba y abajo suben y bajan 1,
RePág y AvPág 5, Inicio y Fin van al mínimo y al máximo; mantener pulsado «−» o «+» repite. En el
límite, el botón de ese lado se apaga. Un número fuera de rango se corrige al límite al salir del campo.

### Tarjeta «Qué se cuenta»

Debajo del título: «Los mazos excluidos se aplican al aceptar.», porque piden leer la colección.

| Opción | Cómo se elige | Por defecto |
|---|---|---|
| Periodo de las cifras | Tres botones en un carril: «30 días», «365 días» y «Todo el historial»; debajo, «Vale para el promedio diario y la retención.» | 30 días |
| Excluir mazos | Una fila que abre su subpágina, con su resumen escrito: «Ninguno» o «2 mazos excluidos: Inglés, Japonés» (hasta tres nombres y «y 2 más») | Ninguno |

Si en algún idioma un valor no cabe en su botón, el carril pasa entero a una lista vertical; nunca se
corta un texto dentro de un botón.

### Tarjeta «Metas y fechas»

Primero, la casilla «Mostrar racha y meta» (marcada de serie). Lo que depende de ella va debajo,
agrupado por una línea a la izquierda; desmarcada, se ve apagado y una línea explica: «La meta, los
comodines y la pausa no cuentan mientras esté desmarcada; se conservan.»

| Opción | Cómo se elige | Por defecto |
|---|---|---|
| Meta diaria | Tres botones: «Sin meta», «Un número» y «Terminar lo de hoy». Con «Un número», debajo, el campo con «−» y «+» (de 1 a 9.999) seguido de «tarjetas al día» y la propuesta: «Propuesta: el 80 % de su promedio diario (41).». Con «Terminar lo de hoy»: «Las tarjetas que vencen hoy, con los límites diarios de Anki.» | Sin meta |
| Comodines | Casilla «Perdonar días sueltos con comodines» y, debajo, la regla y cuántos tiene ahora: «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin estudiar gasta uno. Ahora tiene 1 comodín.» (cuántos tiene solo se dice si la ventana se abre desde la lista de mazos) | Marcada |
| Pausa | Casilla «Pausar la racha». Marcada, debajo: «Desde [26 oct 2026] hasta [1 nov 2026] · 7 días»; cada fecha es un botón que abre el calendario. El inicio, hoy como pronto (una pausa guardada que ya empezó conserva su inicio); el fin, como mucho 29 días después del inicio; el calendario no deja elegir otros días. Regla escrita: «Los días de pausa sin estudio no rompen la racha ni gastan comodines. Dura 30 días como máximo.» | Desmarcada (de 7 días si se marca) |
| Fechas clave | Una fila que abre su subpágina, con su resumen: «Ninguna», «3 fechas marcadas · próxima: Examen de Anatomía, faltan 23 días» o «2 fechas marcadas, todas pasadas». No depende de «Mostrar racha y meta» | Ninguna |

La meta propuesta: al elegir «Un número» se propone el 80 % de su promedio diario de los últimos 30
días (el mismo promedio, por día natural, que la tarjeta «Promedio diario»), redondeado a 5. Quien
estudia 4 días de cada 7 con 72 tarjetas esos días tiene un promedio de 41 y se le proponen 35. Sin
historial (o abierta desde la pantalla de un mazo), 30 tarjetas, sin línea de propuesta.

### Subpágina «Excluir mazos»

Sustituye al cuerpo de la ventana; arriba, «‹ Opciones» vuelve a la página principal (también Esc), y
el pie sigue con Cancelar y Aceptar, porque todo se guarda o se descarta junto. Al volver, el foco
vuelve a la fila «Excluir mazos».

- Un buscador («Buscar», el texto de Anki) deja a la vista los mazos cuyo nombre lo contiene, con sus
  padres; sin resultados, «Ningún mazo coincide.».
- Los mazos, como en la pantalla principal (sin mazos filtrados ni el predeterminado vacío), con
  casilla y, los que tienen submazos, un botón para plegarlos y desplegarlos (desplegados al abrir).
  Marcar un mazo marca y apaga sus submazos; al desmarcarlo, cada submazo vuelve a su propia casilla.
  Debajo: «Al excluir un mazo se excluyen también sus submazos.» y el recuento («2 mazos excluidos:
  Inglés, Japonés»). Lo excluido no cuenta en ningún mapa. Solo se cuentan y se nombran mazos que
  existen; un mazo filtrado o el predeterminado vacío que estuviera excluido se conservan.
- Mientras se lee la lista de mazos, filas grises en su lugar.

### Subpágina «Fechas clave»

Con la misma cabecera y el mismo pie que la de mazos.

- Arriba, la tarjeta «Nueva fecha»: «Nombre» (con el ejemplo «p. ej., examen de Matemáticas», 60
  caracteres como máximo), «Fecha» (un botón con la fecha, hoy de serie, que abre el calendario; de
  2000 a 2100) y «Añadir». Intro en el nombre añade. Los avisos salen encima de los campos, en rojo con
  un icono, y se borran al escribir: «Falta el nombre de la fecha.», «Esa fecha con ese nombre ya está
  en la lista.» y «Caben hasta 50 fechas.».
- Debajo, la lista ordenada por fecha. Cada fila: el rombo del mapa (lleno en las que vienen, hueco y
  gris en las pasadas), la fecha corta con el año, el nombre (gris en las pasadas), la cuenta atrás en
  gris («faltan 23 días»; en las pasadas, «(pasada)») y dos botones: editar (lápiz) y eliminar
  (papelera).
- Editar: el nombre y la fecha se cambian en la propia fila; Intro o «Guardar» guardan y Esc lo deja
  como estaba. Un nombre vacío o repetido vuelve al de antes. El doble clic en el nombre también edita.
- Eliminar (también Supr con el foco en la fila): la fila desaparece y en su lugar queda «Se eliminó
  «Parcial».» con «Deshacer», hasta el siguiente cambio. No se pregunta antes.
- Debajo de la lista: «3 de 50 fechas».

### Calendario

Una capa flotante bajo el botón de fecha, con el aspecto del mapa: mes y año («octubre de 2026») con
botones para el mes anterior y el siguiente; las iniciales de los días desde el lunes; los días en
cuadritos de 32 px. Hoy lleva el borde del color del texto, como en el mapa; el día elegido, relleno
azul; los días con fecha clave, un rombo pequeño bajo el número; los días fuera de rango se ven
apagados y no responden. Teclas: flechas (día a día y semana a semana), Inicio y Fin (lunes y domingo
de la semana), RePág y AvPág (mes anterior y siguiente; con Mayús, año), Intro elige y cierra, Esc
cierra sin cambiar. Un clic fuera también lo cierra.

### Cerrar

Esc cierra siempre lo de más arriba: primero el calendario, después la edición de una fecha, después
la subpágina (volviendo a la principal) y, en la principal, la ventana, como Cancelar (también la cruz
de la ventana). Cancelar no guarda nada y el mapa vuelve a como estaba. Si se añadieron, cambiaron o
eliminaron fechas clave, antes pregunta: «¿Descartar los cambios?», «Se perderán las fechas clave que
ha añadido, cambiado o eliminado.», con «Descartar» y «Seguir editando» (el foco, en «Seguir
editando»). Es la única pregunta: todo lo demás se vuelve a elegir en un clic. Intro pulsa el botón que
tiene el foco.

### Accesibilidad

Los controles son botones, casillas y botones de opción de verdad, dibujados a medida: el tabulador
los recorre, el lector de pantalla los anuncia por su nombre («Eliminar Examen de Anatomía»), y al
restaurar la apariencia o eliminar una fecha lo dice en voz alta. El foco del teclado se ve con un
contorno azul de 2 px. Todos los botones miden al menos 28 px. Con el alto contraste de Windows, todo
control tiene borde, lo elegido se marca con borde y ✓, y el foco usa el color del sistema.

## 9. Qué guarda y dónde

- La apariencia y las metas (tema, tamaño, redondeo, periodo de las cifras, meta, comodines y
  mostrar racha y meta), en la configuración de complementos de este ordenador: vale para todos los
  perfiles y no se sincroniza. Los ajustes de versiones anteriores que ya no existen (píxeles,
  comparativa semanal y estadísticas plegadas) se dejan de guardar al aceptar las opciones. Una medida
  guardada por una versión anterior («Repasos» o «Nuevas») se lee como «Tarjetas».
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
  de la meta); los tres grises suaves, «vence»; el gris vacío, «no estudió»; el azul de Anki, el foco
  del teclado. Las señales son formas, no colores: el rombo (lleno o hueco) y el borde discontinuo.
- Todo lo que no es la escala del tema sale de los colores de Anki, que la paleta Nocturne redefine,
  con su pareja de día y de noche: tarjeta (fondo de capa elevada y borde suave), textos (texto y texto
  suave), botones, foco (azul de foco) y globo. El gris de los días sin estudio es el borde suave
  de día y el fondo hundido de noche, para que se distinga sobre la tarjeta en los dos modos. Los
  cuatro tonos de cada tema y los tres grises de los pendientes son colores propios (véase «Así a
  propósito» en errores).
- Tamaños de letra: 20 px para el dato de cada tarjeta, 13 px para las líneas grises de las tarjetas
  y el globo, y 12 px para los meses, las iniciales de los días, la leyenda y el resto. La
  jerarquía se marca con el grosor y el gris. La letra es la de Anki.
- Espacios de 4, 8, 16 y 32 px: 16 px dentro de las tarjetas y entre ellas.

## 12. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento (un archivo
de texto en la carpeta de registros del perfil de Anki) y, en el sitio del mapa, sale «No se pudo
cargar el mapa de calor.» con, debajo, qué hacer («Vuelva a abrir Anki; si se repite, el detalle está
en el registro del complemento.») y el botón de opciones. Anki sigue funcionando.

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
| Siete temas de diez tonos | 4.0.0 | Diez tonos no se distinguían entre sí; quedan cuatro temas de cuatro tonos (seis temas desde la 4.10.0). |
| Temas Rojo fuego, Rosa suave y Turquesa laguna | 4.0.0 (Rosa y Turquesa vuelven en 4.10.0) | El rojo significa error; los otros dos repetían Púrpura y Azul. En la 4.10.0 el cliente recuperó Rosa suave y Turquesa laguna, con cuatro tonos como los demás; Rojo fuego sigue fuera. |
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
| Cuatro grises para los días pendientes | 4.8.0 | El más oscuro pesaba a la vista más que lo estudiado. Ahora son tres, más suaves que el primer tono de cualquier tema (decisión del cliente). |
| Estrella como marca de las fechas clave | 4.8.0 | La estrella se lee como «favorito», «nota» o «premio», y la gris de las pasadas, como «no conseguido». Ahora es un rombo de hito: lleno en las que vienen, hueco en las pasadas. |
| Fila aparte para la marca con cuadritos de menos de 14 px | 4.8.0 | El rombo se lee hasta con 10 px: una sola regla para todos los tamaños. |
| Iniciales de los días fijas al desplazarse de lado | Probado en 4.8.0, descartado | Dejaban asomar trozos de cuadritos y de meses en el borde; se desplazan con el mapa, como en GitHub. |
| Fechas clave con borde naranja (o azul) | 4.0.0 | Pasaron a una ★ sobre su semana. |
| ★ sobre la semana de la fecha clave | 4.1.0 | El cliente pidió otra manera de encontrarlas; pasó a una esquina doblada. |
| Esquina doblada en el cuadrito de la fecha clave | 4.2.0 | Se veía poco. Se cambió por una estrella dentro del cuadrito. |
| Salto o enlace desde «Próxima fecha» hasta su día en el mapa | 4.2.0 | El cliente no quiere enlaces. |
| Línea de sorpresa «Su mejor día del año» | 4.7.0 | Premiaba un día enorme, que empuja a estudiar a atracones. Ahora es «Su mejor semana del año». |
| Iniciales de los días a la derecha en árabe y hebreo | Propuesto en 4.7.0, no aplicado | La rejilla va siempre de izquierda a derecha (corrección FIX-023), así que las iniciales van a la izquierda. |
| Texto «No hay repasos antes de…» en las flechas apagadas | Propuesto en 4.7.0, no aplicado | Pide textos nuevos en 51 idiomas; a la espera de que el cliente lo pida. (El anuncio del año, que solo dice la cifra, se añadió en la 4.8.0.) |
| Encoger el cuadrito cuando el año no cabe | Propuesto de nuevo en 4.8.0, no aplicado | Se mantienen los 24 px; en su lugar, el borde por donde sigue el mapa se desvanece. |

### En las tarjetas de debajo

| Descartado o cambiado | Versión | Por qué |
|---|---|---|
| Llama de la racha y globos de motivación | 3.5.0 | Los descartó el cliente: presionan en lugar de informar. |
| Globo explicativo de la retención | 2026-10-09 | Lo retiró el cliente. Desde la 4.7.0 solo hay globo para explicar el «N/A». |
| Objetivo de retención solo en la pantalla de un mazo | 4.8.0 | Un porcentaje sin referencia no dice si es bueno; ahora sale también en la lista de mazos cuando todos usan el mismo. |
| Periodos de 7 y 90 días | 3.x | Se quedaron 30 días, 1 año y todo el historial (cliente, 2026-10-13). |
| Botones de periodo en la página (junto al año, luego encima de las cifras, luego en la tarjeta de estadísticas) | 4.1.0 | El periodo se elige solo en Opciones. Las tarjetas dicen cuál se usa. |
| Raya entre los dos grupos de cifras | 3.6.0 | Los separaba el espacio; después los grupos se convirtieron en tarjetas. |
| Cuadritos de color delante de las cifras | 4.0.0 | Usaban un color sin explicar. |
| Tarjeta de estadísticas plegable (constancia de la semana, dos barras, anillos de días estudiados y meta cumplida) | 4.1.0 | Sobraba. La sustituyó «Promedio diario»; el récord pasó a la línea de «Racha». |
| Tarjetas encima o al lado del mapa | 4.1.0 | El cliente las quería debajo, sumando el ancho del mapa. |
| Estrella junto a «Próxima fecha» | 4.1.0 | No hacía falta: la estrella marca el día en el mapa. |
| Enlaces dentro de las tarjetas («Fijar meta», «Añadir» fechas, ir a los mazos excluidos) y la ventanita «Fijar meta» | 4.2.0 | El cliente no quiere enlaces. Todo se cambia en Opciones. |
| La fecha al lado del nombre en «Próxima fecha» | 4.3.0 | Ya dice cuántos días faltan. |
| «Sin fechas clave» como dato grande | 4.4.0 | Pasó a «N/A» con «sin fechas clave» debajo. |
| Tarjeta «Próxima fecha» siempre a la vista («N/A · sin fechas clave») | 4.8.0 | Para quien no usa fechas era una caja vacía para siempre, que no informaba de nada. Ahora solo aparece si hay alguna fecha de hoy en adelante. |
| «Un año seguido» al final de la línea de «Racha» | 4.8.0 | Era lo primero que se cortaba, y es lo más raro y memorable. Ahora es la primera línea de sorpresa del mapa. |
| «Promedio diario» por día estudiado | 4.8.0 | Sin decirlo, exageraba lo que estudia quien no estudia todos los días. Ahora es por día natural del periodo, y el título dice la verdad. |
| «Récord» con mayúscula en medio de la línea | 4.1.0 | Va en medio de una frase: «récord». |
| Racha contada en la medida del color | 4.7.0 | Con «Nuevas», un día de solo repasos rompía la racha o gastaba un comodín. Ahora cuenta cualquier respuesta (cliente, 2026-10-22). |
| «· objetivo 90 %» en la línea gris de «Retención» | 4.10.0 | El cliente lo quiso como globo sobre el porcentaje; la línea dice solo el periodo. |
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
| Iniciales de los días a 11 px | 4.8.0 | Era el único tamaño usado una sola vez; ahora 12 px, como los meses. |
| «Periodo de las cifras» como lista desplegable | 4.7.1 | El cliente lo quiso en tres botones, como «El color mide». |
| «Restaurar apariencia» reponía también la medida | 4.7.0 | La medida está en otro recuadro; ahora repone solo «Apariencia». |
| Reglas de comodines y pausa solo al pasar el ratón | 4.7.0 | Casi nadie descubre un globo; ahora van escritas debajo. |
| «Mostrar racha y meta» al final del recuadro | 4.7.0 | Ahora va primero y apaga lo que depende de ella. |
| Meta propuesta fija de 50 | 4.7.0 | Ahora se propone según su historial y en la unidad de la medida. |
| Pausa que empieza en un día pasado | 4.7.0 | Servía para tapar después un fallo; los fallos sueltos ya los cubren los comodines (decisión del cliente). |
| Temas con el de serie primero y los demás por tono | 4.10.0 | Desde la 4.7.0 iban así; el cliente los quiso por orden alfabético. |
| Tira de cuatro tonos como muestra de cada tema | Propuesto en 4.7.0, no aplicado | Se mantiene un solo cuadrito, como pidió el cliente con una captura en la 4.3.0. |
| Letras subrayadas para manejar Opciones con Alt | Propuesto en 4.7.0, no aplicado | Piden cambiar los textos en 51 idiomas; el tabulador y las flechas ya recorren la ventana. |
| Ventana con los controles estándar de Anki (recuadros grises de Qt) | 4.9.0 | Parecía otro producto junto al mapa. Ahora es un panel a medida, del mismo material que las tarjetas (petición del cliente). |
| «Seleccionar mazos» y «Gestionar fechas» como ventanas encima de Opciones | 4.9.0 | Ventana sobre ventana: se perdía el contexto y no se sabía a cuál afectaba Esc. Ahora son subpáginas dentro de la misma ventana. |
| Resumen de mazos excluidos y fechas clave solo en un globo | 4.9.0 | Ahora va escrito en su fila. |
| «Restaurar apariencia» en el pie, con un globo que explicaba su alcance | 4.9.0 | Ahora está en el título de la tarjeta que restaura, con «Deshacer». |
| Corregir una fecha clave solo con un doble clic sin señal, y eliminar sin poder deshacer | 4.9.0 | Ahora hay botones de editar (nombre y fecha) y eliminar, y «Deshacer» al eliminar; el doble clic queda como atajo. |
| Selector de fecha del sistema | 4.9.0 | Distinto en cada ordenador y sin relación con el mapa; ahora es un calendario propio con hoy y las fechas clave marcados. |
| Esperar a leer los mazos para abrir la ventana | 4.9.0 | Ahora se abre al instante; solo el resumen de mazos espera. |
| Meta propuesta por día estudiado | 4.9.0 | No coincidía con el «Promedio diario» de la tarjeta; ahora usa el mismo promedio y lo dice. |
| «El color mide» (Repasos, Tarjetas, Nuevas) | 4.10.0 | El cliente quiso una sola medida y que se llamara «tarjetas». Se cuentan tarjetas distintas, no respuestas, para que la palabra diga la verdad (regla de FIX-006; decisión del cliente). Una medida guardada antes pasa a «Tarjetas». |
| Letra de 13 px y espacios de 24 px en el panel | 4.10.0 | El cliente lo veía grande y muy alto; ahora 12 px y espacios algo más ceñidos, con el mismo aspecto. |
| Ventana que cambiaba de alto en cada subpágina | 4.10.0 | En Windows descolocaba la página (FIX-028); ahora el alto se fija al abrir, como mucho 720 px. |
| Textos del panel seleccionables con el ratón | 4.10.0 | El cliente no los quería; solo se selecciona lo que se escribe en los campos. |
| Semana según el idioma (empezar en domingo o sábado donde se acostumbra) | Propuesto en 4.9.0, descartado | El navegador de Anki puede no tener ese dato, y cambiaría las iniciales, Inicio y Fin y el calendario; el mapa y el calendario siguen empezando en lunes (decisión del cliente). |

### Otros

| Descartado | Por qué |
|---|---|
| Medidas «Repasos» y «Nuevas» | Se quitaron en la 4.10.0: solo queda «Tarjetas» (decisión del cliente). |
| Medida «minutos» | Hay días con cientos de repasos guardados sin tiempo, así que la cifra no era coherente (decisión del cliente, 2026-10-08). |
| Mapa encima de la lista de mazos | Anki no ofrece a los complementos ese sitio. Va debajo (decisión del cliente). |
| Avisos, cuentas atrás de pérdida, premios al azar, puntos, insignias y clasificaciones | Presionan o crean dependencia en lugar de informar; descartados desde la 3.6.0 y confirmados en el informe de la 4.7.0. |
