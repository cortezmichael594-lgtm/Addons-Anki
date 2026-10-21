# Qué hace «GritMap»

Versión 4.0.0 · 2026-10-21

Mapa de calor de su estudio, como el de las contribuciones de GitHub, ordenado en tres bandas de
tarjetas. Arriba, cuatro tarjetas pequeñas que responden de un vistazo: «Hoy», «Racha», «Retención» y
«Próxima fecha». Debajo, la tarjeta «Actividad», con el año entero (un cuadrito por día en cinco
niveles: gris sin estudio y cuatro tonos del tema). Al final, la tarjeta «Estadísticas», que se puede
plegar. Tiene una meta diaria opcional, comodines que perdonan días sueltos y una pausa de la racha.
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
- Las tarjetas ocupan como mucho 960 px de ancho, centradas. Cada una tiene el fondo un punto más
  claro que el de Anki, un borde suave, esquinas redondeadas y su título arriba a la izquierda; de
  día llevan una sombra muy leve y de noche ninguna.

## 2. Mientras se calcula

La primera vez que se abre una pantalla se ven ya las tarjetas con huecos grises donde irán los
datos, y la rejilla del año con su alto final, para que nada salte cuando llegan. Después, cada vez
que Anki vuelve a dibujar esa pantalla (al volver del repaso, sincronizar, deshacer, plegar un mazo o
cada 10 minutos), se ve al instante lo último que se mostró y se sustituye, sin hueco, si los datos al
día son distintos. El cálculo se hace sin congelar Anki.

## 3. La fila de resumen

Cuatro tarjetas del mismo ancho (tres si se desactiva «Mostrar racha y meta»). Cada una tiene un
título, un dato grande y una línea gris. Al pulsarlas no pasa nada, salvo en los enlaces azules. Si la
ventana es estrecha, pasan a dos por fila y, más estrecha aún, a una.

### Hoy

- Sin meta: lo hecho hoy en la unidad de la medida («35 repasos») y el enlace «Fijar meta».
- Con la meta «Un número»: un anillo pequeño que se llena con lo hecho, «80 de 100» y, debajo,
  «faltan 20 repasos». Al cumplirla, «✓ Meta cumplida»; si la supera, «120 de 100», con el anillo
  cerrado. La primera vez que se dibuja después de cumplirla (al volver a la lista de mazos tras
  repasar), el ✓ aparece con un leve aumento de 150 ms; nada si Anki o el sistema piden reducir las
  animaciones, y no se repite al volver a la pantalla.
- Con la meta «Terminar lo de hoy»: lo mismo, en tarjetas: las respondidas hoy frente a esas más las
  que aún vencen hoy (con los límites diarios de Anki y sin los mazos excluidos).
- «Fijar meta» abre una ventana pequeña, «Meta diaria», con «Cada día, al menos:» y un número ya
  propuesto: el 80 % de su promedio diario de los últimos 30 días, redondeado a 5 (50 si aún no hay
  promedio). Al aceptar, la meta pasa a «Un número».
- En la pantalla de un mazo, el título es «Hoy en este mazo», con lo hecho hoy en ese mazo, sin meta
  ni enlace: la meta es de toda la colección.
- Con «Mostrar racha y meta» desactivado, solo lo hecho hoy, sin meta ni enlace.

### Racha

Días seguidos estudiando hasta hoy, en la medida elegida («18 días»). La racha no se rompe por no
haber estudiado todavía hoy. La línea gris dice:

- «✓ hoy» si hoy ya cuenta, u «hoy pendiente» si todavía no;
- «· 1 comodín» o «· 2 comodines» si tiene comodines guardados (subrayado de puntos: al pasar el
  ratón o llegar con el tabulador, «Cada 7 días seguidos gana un comodín (2 como máximo). Un día sin
  estudiar gasta uno.»);
- «· a 3 días del récord» si la racha más larga está a 7 días o menos;
- «· Un año seguido» el día en que la racha llega a 365 días (y a 730, 1.095…).

Casos especiales: si nunca ha estudiado, «0 días» y «hoy pendiente»; si la racha está a cero,
«0 días» y «Última sesión hace 3 días»; al volver tras romperla, «Día 1» y «Récord: 45 días».

### Retención

El porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención real de Anki
(tarjetas con al menos un día de intervalo), en el periodo elegido en Estadísticas. Debajo, el periodo:
«últimos 30 días», «último año» o «todo el historial». Con menos de 20 respuestas que contar escribe
«N/A» (el texto de Anki), en gris. En la pantalla de un mazo con FSRS activado añade la retención
deseada de su configuración: «· objetivo 90 %».

### Próxima fecha

La próxima fecha clave de hoy en adelante: «★ faltan 23 días», «★ falta 1 día» o «★ es hoy», con su
nombre debajo (varias el mismo día, separadas por « · »). Sin fechas por venir: «Sin fechas clave» y
el enlace «Añadir», que abre las opciones y, sobre ellas, la lista de fechas clave. La tarjeta nunca
desaparece.

## 4. La tarjeta «Actividad»

- Título «Actividad» y, a su lado, en gris, lo hecho en el año que se ve: «12.480 repasos en 2026»
  (los días futuros no cuentan). En una colección sin repasos no lleva esa cifra.
- A la derecha: «‹ 2026 ›» (año anterior y siguiente, con su nombre al pasar el ratón), el botón
  «Hoy» y el botón de opciones. Las flechas se apagan en el primer año con repasos y en el último con
  vencimientos o fechas clave. «Hoy» solo se ve cuando sirve: en otro año o, con cuadritos grandes,
  cuando la semana de hoy queda fuera de la vista; su hueco está siempre reservado. «Hoy» vuelve al
  año actual y a la semana de hoy.
- El año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki (siempre con el calendario gregoriano). Con el tamaño
  «Ajustado al ancho», el año cabe en la tarjeta con cuadritos de 10 a 22 px; si la ventana es más
  estrecha que los cuadritos de 10 px, se desplaza de lado. Con «Grande», cuadritos de 25 px y
  desplazamiento de lado. Al abrir un año se ve la semana de hoy; en un año pasado, diciembre, y en
  uno futuro, enero.
- Días pasados y hoy: cinco niveles. Sin estudio, el gris vacío; con estudio, cuatro tonos del tema,
  repartidos según su promedio de siempre en los días que estudió (con un mínimo, para que al empezar
  no salga todo oscuro): hasta la mitad del promedio, hasta el promedio, hasta el doble y más del
  doble.
- Días futuros con tarjetas que vencen: el cuadrito vacío con un punto gris (una forma, no un tono,
  para que no se confunda con «estudió poco»). Lo atrasado no se dibuja.
- Hoy lleva un borde del color del texto.
- Las fechas clave llevan una ★ pequeña y gris sobre la columna de su semana, en una fila bajo los
  meses (solo si ese año tiene alguna); al pasar el ratón, su nombre y su cuenta atrás.
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
  nueva»…). Detrás, «Pendientes» (el cuadrito con punto) si en el año que se ve hay días pendientes, y
  «Perdonado» (el borde discontinuo) si hay días perdonados.
- Debajo, a la izquierda, como mucho una línea de sorpresa al día, solo cuando ocurre y con datos
  reales, por este orden: «Nueva racha más larga» (el día en que la racha supera la mejor anterior),
  «Su mejor día del año» (hoy supera a todos los demás días del año, con al menos 7 días estudiados
  antes), «Mes completo» (el último día del mes, si estudió todos sus días) y «1.000 repasos este año»
  (el día en que el total del año cruza 100, 500 o un múltiplo de 1.000). Solo si hoy ya cuenta.
- En árabe, hebreo, persa y uigur, la navegación del año, el mapa y su pie van de izquierda a derecha,
  como el calendario; el resto sigue la dirección del idioma.
- Cambiar de año o de tema, tamaño, forma, periodo, meta, comodines o pausa no vuelve a leer la
  colección: es inmediato. Cambiar la medida o los mazos excluidos sí la vuelve a leer, sin quitar el
  mapa mientras tanto.

### Cuando no hay nada que dibujar

- En una colección sin repasos, sin vencimientos y sin fechas clave: la fila de resumen («0 repasos»
  con «Fijar meta», «0 días» con «hoy pendiente», retención «N/A» y «Sin fechas clave» con «Añadir»),
  la cuadrícula del año actual en gris con hoy marcado y, debajo, «Cada día que estudie se pintará
  aquí.». Sin leyenda y sin tarjeta de estadísticas; las flechas de año, apagadas.
- En la pantalla de un mazo excluido: una tarjeta «Actividad» con «Este mazo está excluido del mapa.»,
  el enlace «Cambiar mazos excluidos» (abre las opciones y, sobre ellas, la lista de mazos excluidos) y
  el botón de opciones.
- Si algo falla: una tarjeta con «No se pudo cargar el mapa de calor.» y el botón de opciones.

## 5. Al pasar el ratón por un día (o llegar a él con el teclado)

Sale un globo con la fecha larga en el idioma de Anki (sin «el»), en gris, y, en la línea de abajo, lo
hecho ese día. Después, en gris y según el caso: si el día está perdonado, «Perdonado con un comodín»
o «Racha en pausa»; con la meta «Un número», en la lista de mazos y en los días pasados con estudio,
«Meta cumplida» o «Meta: 60 de 100»; y en los días que se pueden pulsar, «Pulse para ver estas tarjetas» o «Pulse para ver las
que vencen ese día». La tecla Esc lo cierra. En español:

- «lunes, 22 de junio de 2026» / «**12** **repasos**» (o «1 repaso»).
- Con la medida «Tarjetas»: «… / **9** **tarjetas**».
- Con la medida «Nuevas»: «… / **3** **nuevas**», «**1** **nueva**» o «**Ninguna** **nueva**».
- Sin estudio: «… / **Ningún** **repaso**».
- Días futuros: «… / **30** tarjetas **pendientes**», «**1** tarjeta **pendiente**» o «**Ninguna**
  tarjeta **pendiente**».
- En una fecha clave, encima de todo, con una estrella: el nombre (varios, separados por « · ») y,
  si no ha pasado, la cuenta atrás: «★ Examen de Anatomía (faltan 23 días)».
- Las cifras de 1.000 o más llevan punto de millar. Un lector de pantalla lee el mismo texto.

## 6. Al pulsar un día

- Un día pasado con repasos abre Explorar con la búsqueda de las tarjetas respondidas ese día
  (prop:rated), limitada al mazo de la pantalla y sin los mazos excluidos.
- Un día futuro con vencimientos abre Explorar con las tarjetas que vencen ese día (prop:due).
- Los días sin nada no responden al clic. Con el teclado, Intro o la barra espaciadora hacen lo mismo.

## 7. La tarjeta «Estadísticas»

- Cabecera: el título a la izquierda y, a la derecha, «30 días · 1 año · Todo» (el periodo elegido con
  el fondo azul suave de selección de Anki y letra en negrita; los demás, texto gris que toma un fondo
  suave al pasar el ratón) y el botón para plegarla («Plegar» / «Desplegar» al pasar el ratón).
  Plegada, solo queda la cabecera. Se pliega al instante y GritMap recuerda cómo la dejó; la primera
  vez aparece abierta. El periodo se guarda al pulsarlo y cambia los anillos, el promedio y la
  retención de la fila de resumen.
- Mitad izquierda, «Constancia · últimos 7 días»: siete bloques, uno por día (de hace 7 días a ayer),
  en el tono 4 del tema si estudió y vacíos si no, con «6 de 7» al lado. Debajo, dos barras en el
  color del tema, «Últimos 7 días» y «7 anteriores», con su cifra al final («448 repasos»): los 7 días
  completos que terminan ayer frente a los 7 anteriores. La diferencia se ve en la longitud y en la
  cifra, sin verde ni rojo.
- Mitad derecha, anillos de 56 px con la cifra dentro («26» y «de 30»): «Días estudiados» (días con
  estudio en el periodo; hoy cuenta solo si ya estudió, y el periodo no empieza antes de su primer
  repaso) y, con la meta «Un número», «Meta cumplida» (días del periodo en que la alcanzó).
- Al pie, en gris: «Promedio diario 72 repasos · Racha más larga 40 días». El promedio es lo hecho
  por día estudiado en el periodo, contando solo días completos (termina ayer). Sin días completos
  estudiados escribe «N/A», con el globo «Sin días completos estudiados en los últimos 30 días» (o «…
  en todo el historial»); con «Nuevas», un promedio que se queda en 0 también es «N/A», con «Menos de
  una nueva por día estudiado…». La racha más larga queda aquí aunque la actual se rompa.
- En una ventana estrecha, las dos mitades se apilan.

Todas las cifras siguen la medida elegida: con «Repasos» y «Tarjetas», un día estudiado es un día con
repasos; con «Nuevas», solo un día en que empezó alguna tarjeta nueva. La retención no depende de la
medida.

## 8. Comodines y pausa

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

## 9. Ventana de opciones

Título «GritMap». Se abre después de leer los mazos y las opciones sin congelar Anki (un segundo clic
mientras tanto no abre otra), delante de la ventana desde la que se pidió. Tres grupos con título y
los botones «Restaurar apariencia» (a la izquierda; al pasar el ratón, «No cambia los mazos
excluidos ni las fechas clave»), Aceptar y Cancelar. Intro pulsa el botón que tiene el foco. Recuerda
su tamaño y su posición. Al aceptar, el mapa se redibuja en su sitio, sin recargar la pantalla.

| Grupo | Opción | Valores | Por defecto |
|---|---|---|---|
| Apariencia | Tema de color | Azul océano, Naranja atardecer, Púrpura real y Verde clásico, cada uno con su tira de cuatro tonos del modo activo (cambia si Anki pasa de día a noche) | Verde clásico |
| | Tamaño | «Ajustado al ancho» o «Grande» | Ajustado al ancho |
| | Forma | «Cuadrado» o «Redondeado» | Cuadrado |
| | Vista previa | Un mes de mapa en miniatura con los tonos del tema, hoy, una ★ y días pendientes; cambia al momento con el tema, el tamaño y la forma | — |
| Qué se cuenta | El color mide | Repasos, Tarjetas, Nuevas; debajo, «Cada respuesta cuenta una», «Cada tarjeta cuenta una vez por día» o «Solo las tarjetas que empezó ese día» | Repasos |
| | Excluir mazos | Botón «Seleccionar mazos» (o «1 mazo excluido», «2 mazos excluidos», con hasta 15 nombres al pasar el ratón y «…» si hay más) | Ninguno |
| Metas y fechas | Meta diaria | «Sin meta», «Un número» (con el número, de 1 a 9.999, en la unidad de la medida) o «Terminar lo de hoy» | Sin meta (50 si elige «Un número») |
| | Comodines | Casilla «Perdonar días sueltos con comodines» (al pasar el ratón, la regla) | Marcada |
| | Pausa | Casilla «Pausar la racha» con las fechas de inicio y fin (el fin, como mucho 29 días después del inicio; al pasar el ratón, «La pausa dura 30 días como máximo.») | Desmarcada |
| | Fechas clave | Botón «Gestionar fechas» (o «1 fecha marcada», «3 fechas marcadas», con la lista al pasar el ratón) | Ninguna |
| | Mostrar racha y meta | Casilla | Marcada |

- «Restaurar apariencia» repone el tema, el tamaño, la forma y la medida; no toca los mazos excluidos,
  las fechas clave, la meta, los comodines ni la pausa.
- Si tenía Rojo fuego, Rosa suave o Turquesa laguna, retirados en esta versión, pasa sin preguntar a
  Naranja atardecer, Púrpura real o Azul océano, y la ventana lo dice una vez, arriba: «Su tema «Rojo
  fuego» se ha retirado; ahora usa «Naranja atardecer».».
- Si tenía los cuadritos a 30 px o más pasa a «Grande», y si tenía el redondeo a 4 px o más, a
  «Redondeado»; si no, a los valores por defecto.
- El periodo de las cifras ya no está aquí: se elige en la tarjeta de estadísticas.
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

## 10. Qué guarda y dónde

- La apariencia y las metas (tema, medida, tamaño, forma, periodo de las cifras, estadísticas
  plegadas, meta, comodines y mostrar racha y meta), en la configuración de complementos de este
  ordenador: vale para todos los perfiles y no se sincroniza. Los ajustes de la versión 3.x que ya no
  existen (píxeles y comparativa semanal) se dejan de guardar al aceptar las opciones.
- Los mazos excluidos, las fechas clave y la pausa, dentro de cada colección: cada perfil tiene los
  suyos y viajan con la sincronización. Se leen de la colección cada vez. No se pueden deshacer desde
  Editar, porque son ajustes, no estudio.
- Si encuentra mazos o fechas guardados como en versiones antiguas, los copia una vez a cada perfil
  que aún no los tenga.
- Un valor que falte o no sirva (por ejemplo, escrito a mano) se sustituye por el predeterminado.

## 11. Idiomas

Sus textos están en 51 idiomas, también los nuevos de la 4.0.0; si el de Anki no está, sale en
inglés. Cada cifra con unidad usa la forma de plural de su idioma (por ejemplo, en ruso 1 день,
2 дня, 5 дней; «1 comodín», «2 comodines»). Las cifras, los porcentajes, las fechas y los nombres de
los meses los escribe el navegador de Anki en su idioma; en español, con punto de millar desde 1.000.
«N/A», «Añadir», «Eliminar» y «Buscar» usan los textos de Anki.

## 12. Colores, letra y espacio

- Cada color tiene una sola función: los cuatro tonos del tema significan «estudió» (mapa, anillos,
  bloques y barras); el gris vacío, «no estudió»; el azul de Anki, «se puede pulsar o está elegido»
  (foco del teclado, periodo elegido y enlaces). Las señales son formas, no colores: la estrella, el
  punto y el borde discontinuo.
- Todo lo que no es la escala del tema sale de los colores de Anki, que la paleta Nocturne redefine,
  con su pareja de día y de noche: tarjeta (fondo de capa elevada y borde suave), textos (texto y texto
  suave), punto de pendientes (texto desactivado), botones, periodo elegido (fondo de selección), foco
  (azul de foco), enlaces (color de enlace) y globo. El gris de los días sin estudio es el borde suave
  de día y el fondo hundido de noche, para que se distinga sobre la tarjeta en los dos modos. Los
  cuatro tonos de cada tema son colores propios (véase «Así a propósito» en errores).
- Dos tamaños de letra: 20 px para el dato de cada tarjeta y 12 px para todo lo demás; la jerarquía se
  marca con el grosor y el gris. La letra es la de Anki.
- Espacios de 4, 8, 16 y 32 px: 16 px dentro de las tarjetas y entre ellas.

## 13. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento (un archivo
de texto en la carpeta de registros del perfil de Anki) y, en el sitio del mapa, sale «No se pudo
cargar el mapa de calor.», con el botón de opciones. Anki sigue funcionando.

## 14. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No aparece en el repaso, en Explorar ni en las estadísticas.
- No avisa, no mete prisa ni habla de perder la racha; no hay premios al azar, clasificaciones,
  insignias ni puntos.
- No anima nada salvo el leve hundimiento de los botones al pulsarlos y la aparición del ✓ al cumplir
  la meta.
