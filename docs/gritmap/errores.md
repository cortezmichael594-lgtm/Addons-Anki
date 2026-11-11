# Errores de «GritMap»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las diez primeras se hicieron antes de que el complemento llegara a este taller (versión
3.1.1); la versión exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

(Ninguno.)

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-27, restablecida el 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: la
  comparativa semanal salía muy negativa los lunes y subía a lo largo de la semana sin que cambiara el
  ritmo de estudio. Por qué: comparaba lo que iba de semana con la semana anterior entera. Regla: se
  comparan siempre dos periodos iguales y completos: los 7 días que terminan ayer contra los 7
  anteriores; hoy no entra.
- FIX-002 · 2026-07-27 · versión 3.1.1 o anterior · Qué pasaba: la retención salía 0 %, como si se
  hubiera fallado todo, en cuentas recién empezadas o con solo tarjetas nuevas. Por qué: «no hay nada
  que medir» se escribía como cero. Regla: «no hay datos» y «cero» son cosas distintas; sin datos se
  escribe «N/A», con el texto de Anki.
- FIX-003 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: una tarjeta prestada a un mazo
  filtrado no contaba en el cuadrito gris de su día de vencimiento. Por qué: dentro de un mazo
  filtrado la fecha real se guarda en otro sitio. Regla: el vencimiento se lee de la fecha original
  cuando la tarjeta está en un mazo filtrado, igual que la búsqueda de Anki.
- FIX-004 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: el historial de las tarjetas borradas
  contaba en el mapa general mientras no hubiera mazos excluidos y desaparecía en cuanto se excluía
  alguno. Por qué: con exclusiones se exigía que la tarjeta siguiera existiendo. Regla: excluir quita
  lo excluido, nunca exige que la tarjeta exista; las borradas cuentan siempre en el mapa general.
- FIX-005 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: con «Infinity» o «NaN» escrito a mano
  en la configuración, el mapa desaparecía sin aviso. Por qué: esos valores pasaban por números y
  fallaban al convertirlos. Regla: todo número que entra se comprueba antes de usarlo; si no es un
  número de verdad, se usa el valor por defecto.
- FIX-006 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: el globo decía «37 tarjetas
  repasadas» y el promedio «85 tarjetas», pero Explorar mostraba menos tarjetas. Por qué: las cifras
  contaban respuestas y los textos hablaban de tarjetas. Regla: cada cifra se escribe en la unidad de
  lo que cuenta: «repasos» para respuestas, «tarjetas» para tarjetas distintas.
- FIX-007 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: en modo noche, la muestra de color de
  cada tema en las opciones enseñaba el tono de día. Por qué: se tomaba siempre de la escala de día.
  Regla: toda muestra de color se toma de la escala del modo activo.
- FIX-008 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: lo que el mapa pone en la página de
  Anki (identificadores, clases, colores, órdenes) empezaba por «shm» y podía chocar con otro
  complemento. Por qué: venía de un nombre antiguo. Regla: todo lo inyectado empieza por «gritmap».
- FIX-009 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: si la página cargaba dos veces el
  código del mapa, cada clic se enviaba dos veces. Por qué: no se comprobaba si ya estaba cargado.
  Regla: el código inyectado comprueba si ya existe antes de crearse y marca en la página que sus
  detectores están puestos.
- FIX-010 · 2026-10-08 · versión 3.1.1 o anterior · Qué pasaba: el promedio diario decía «0 repasos»
  cuando la ventana no tenía ningún día completo estudiado. Por qué: «sin días» se trataba como cero.
  Regla: sin días que promediar se escribe «N/A», y el globo explica por qué (desde la 4.14.0, a
  petición del cliente, lo explica la línea gris de la tarjeta, no un globo; desde la 4.15.0, también
  a petición suya, sin dato la tarjeta no se muestra: nunca sale un cero falso).

Las trece siguientes salieron de la revisión completa del 2026-10-12 y se corrigieron en la versión
3.2.0.

- FIX-011 · 2026-10-13 · versión 3.2.0 · Qué pasaba: con la medida «Nuevas», todos los días anteriores
  al planificador actual de Anki (v3) salían en gris y el promedio decía «N/A». Por qué: los
  planificadores antiguos anotaban la primera respuesta de otra manera. Regla: una tarjeta empieza
  ese día si es su primera respuesta, se anotara como se anotara, igual que la búsqueda de Anki de
  tarjetas introducidas.
- FIX-012 · 2026-10-13 · versión 3.2.0 · Qué pasaba: con la hora de cambio de día de Anki a las 12 o
  más tarde, cada cuadrito llevaba la fecha del día siguiente, el borde de hoy caía en mañana y la
  cuenta atrás de las fechas clave se quedaba corta en un día. Por qué: el cálculo del «hoy» de Anki
  solo acertaba con horas de cambio anteriores a mediodía. Regla: el día se calcula con el
  calendario, a partir del corte de Anki, y vale para las 24 horas de cambio y los cambios de hora.
- FIX-013 · 2026-10-13 · versión 3.2.0 · Qué pasaba: en la pantalla de un mazo que reúne casi todas
  las tarjetas, el mapa tardaba segundos y, mientras, Anki no respondía al pulsar «Estudiar ahora».
  Por qué: la consulta buscaba tarjeta por tarjeta en lugar de leer el historial de corrido. Regla:
  el peor caso es siempre una lectura seguida, y la lectura va por años para dejar pasar a Anki
  entre medias.
- FIX-014 · 2026-10-13 · versión 3.2.0 · Qué pasaba: tras sincronizar, el mapa no mostraba una fecha
  clave añadida en otro ordenador y, al pulsar Aceptar en Opciones, esa fecha se borraba aquí y
  después también en el otro ordenador. Por qué: los mazos excluidos y las fechas clave se
  guardaban en memoria y nada los refrescaba al sincronizar. Regla: lo que vive en la colección se
  lee de ella cada vez; en memoria solo queda la apariencia, que no cambia al sincronizar.
- FIX-015 · 2026-10-13 · versión 3.2.0 · Qué pasaba: una tarjeta con código preparado a propósito
  podía leer archivos de otros complementos a través de GritMap. Por qué: la regla que dice qué
  archivos sirve GritMap a la página era demasiado abierta. Regla: solo se sirven los dos archivos
  propios del mapa, con un patrón cerrado.
- FIX-016 · 2026-10-13 · versión 3.2.0 · Qué pasaba: al excluir un mazo, sus submazos seguían sin
  marcar en la lista aunque el mapa ya no los contaba, y el botón contaba mazos que ya no existían.
  Por qué: cada mazo tenía su casilla suelta y la cifra contaba lo guardado, no lo que existe.
  Regla: la ventana enseña exactamente lo que excluye el mapa: un mazo marcado marca y bloquea a
  sus submazos, y solo se cuentan y se nombran mazos que existen.
- FIX-017 · 2026-10-13 · versión 3.2.0 · Qué pasaba: con el teclado, Intro sobre «Seleccionar mazos»
  o sobre «Restaurar» cerraba Opciones y guardaba, y en Fechas clave, Intro sobre Aceptar intentaba
  añadir una fecha. Por qué: a esos botones se les había quitado la respuesta a Intro. Regla: Intro
  pulsa el botón que tiene el foco; solo se elige cuál es el botón por defecto.
- FIX-018 · 2026-10-13 · versión 3.2.0 · Qué pasaba: con Opciones abierta, al pasar Anki de modo día a
  noche, las muestras de color de los temas se quedaban con los tonos del modo anterior. Por qué: se
  pintaban una sola vez. Regla: todo color que depende del modo se vuelve a pintar al cambiar de
  modo.
- FIX-019 · 2026-10-13 · versión 3.2.0 · Qué pasaba: en español salía «1240 repasos» pero «12.240
  repasos». Por qué: la costumbre del navegador no separa los millares con cuatro cifras. Regla: en
  español, toda cifra lleva punto de millar desde 1.000.
- FIX-020 · 2026-10-13 · versión 3.2.0 · Qué pasaba: al cambiar de año con el teclado, el foco
  saltaba al principio de la página y el mapa volvía a enero. Por qué: el mapa se sustituye entero y
  se perdían el botón con el foco y el desplazamiento. Regla: antes de sustituir el mapa se anotan
  el foco y el desplazamiento, y se devuelven después.
- FIX-021 · 2026-10-13 · versión 3.2.0 · Qué pasaba: en persa y en tailandés los meses y el año del
  globo salían de su propio calendario, distinto del de la rejilla. Por qué: el navegador usa el
  calendario de cada idioma. Regla: toda fecha del mapa se escribe en el calendario gregoriano, el
  de la rejilla y el de Anki.
- FIX-022 · 2026-10-13 · versión 3.2.0 · Qué pasaba: en ruso, polaco, checo, árabe y otros nueve
  idiomas, días, repasos, tarjetas y cuentas atrás salían con la forma de plural equivocada (por
  ejemplo, «22 дней» en lugar de «22 дня»). Por qué: fuera de «Nuevas» solo había dos formas. Regla:
  toda cifra con unidad elige su forma con las reglas de plural de su idioma.
- FIX-023 · 2026-10-13 · versión 3.2.0 · Qué pasaba: en árabe, hebreo, persa y uigur, las flechas de
  año salían invertidas y la cifra se pegaba a su rótulo. Por qué: Anki pone esas páginas de derecha
  a izquierda y el mapa no lo tenía en cuenta. Regla: la cabecera, la rejilla y la leyenda van
  siempre de izquierda a derecha, como el calendario, y los huecos entre textos siguen la dirección
  del idioma.

Las ocho siguientes se hicieron en la serie 4 fuera de este taller; constan la fecha y la nota del
código, no la versión exacta. Se anotaron aquí al traer la 4.11.2 (2026-11-04).

- FIX-024 · 2026-10-21 · serie 4 · Qué pasaba: al recorrer el mapa con el tabulador, los botones de
  encima no mostraban ningún contorno y no se sabía dónde estaba el foco. Por qué: Anki quita el
  contorno de todos los botones de sus páginas con una regla que gana a las normales. Regla: el foco
  de todo botón del complemento lleva una regla más fuerte que la de Anki y solo aparece al usar el
  teclado, nunca al hacer clic.
- FIX-025 · 2026-10-21 · serie 4 · Qué pasaba: abiertas desde Herramientas > Complementos >
  «Configuración», las opciones podían quedar detrás de la ventana Complementos en Windows. Por qué:
  la ventana se colgaba siempre de la principal de Anki. Regla: una ventana que se abre desde otra se
  cuelga de la que está activa, comprobando antes que siga abierta.
- FIX-026 · 2026-10-22 · serie 4 · Qué pasaba: con la meta «Terminar lo de hoy» ya cumplida, la
  tarjeta «Hoy» volvía al rato a «faltan 3». Por qué: las tarjetas en aprendizaje vuelven a vencer
  horas después y la meta se recalculaba con ellas. Regla: una meta cumplida queda cumplida el resto
  del día; solo vuelve atrás si se deshace la respuesta que la cumplió.
- FIX-027 · 2026-10-26 · serie 4 · Qué pasaba: en la fila de arriba y en la primera y la última
  columna, el borde de hoy y el discontinuo de los días perdonados se veían cortados. Por qué: esos
  bordes sobresalen del cuadrito y el dibujo recortaba lo que quedaba fuera. Regla: lo que se dibuja
  alrededor de un cuadrito cabe siempre; el dibujo no recorta y la rejilla deja margen por los cuatro
  lados (desde la 4.12.0, 4 px, para que quepa también el contorno de foco del día de hoy).
- FIX-028 · 2026-10-26 · serie 4 · Qué pasaba: al entrar en «Fechas clave», la cabecera de Opciones
  desaparecía por arriba y Aceptar y Cancelar quedaban a media ventana. Por qué: la ventana cambiaba
  de alto en cada subpágina y la página entera podía desplazarse al llevar el foco a un campo. Regla:
  el alto de la ventana se fija al abrirla y solo se desplaza el cuerpo del panel, nunca la página.
- FIX-029 · 2026-10-26 · serie 4 · Qué pasaba: al subir deprisa con el ratón por el mapa, el globo
  se quedaba abierto y tapaba los días de arriba. Por qué: el globo recogía el ratón. Regla: el globo
  de los días nunca recoge el ratón; el ratón llega siempre al día que tiene debajo.
- FIX-030 · 2026-10-26 · serie 4 · Qué pasaba: al marcar «Pausar la racha» (o cualquier casilla de
  abajo), la cabecera de Opciones desaparecía por arriba. Por qué: la casilla invisible de verdad se
  colocaba respecto a la ventana y no a su fila, y al recibir el foco el navegador desplazaba la
  página entera. Regla: todo control invisible va colocado dentro de su fila, y si la página se
  desplazara, vuelve a su sitio.
- FIX-031 · 2026-10-27 · serie 4 · Qué pasaba: el ✓ de «✓ hoy» en «Racha» era gris y fino, y el de
  «✓ Meta cumplida» en «Hoy», del color del texto y en seminegrita. Por qué: cada uno se dibujaba de
  una manera. Regla: todo ✓ de las tarjetas se dibuja con la misma pieza y el mismo aspecto.
- FIX-032 · 2026-11-11 · versión 4.16.0 · Qué pasaba: de noche, en Opciones, «Restaurar apariencia» se
  leía con 3,0 a 1 de contraste, «‹ Opciones» con 3,7 y el texto de ejemplo de los campos con 3,2 (la
  norma pide 4,5). Por qué: los textos que se pulsan usaban el azul de los botones, que es un color de
  relleno, y el texto de ejemplo, el gris de serie del navegador, fuera de la paleta. Regla: el azul de
  acción es para rellenos y bordes; el texto que se pulsa usa el color de enlace de la paleta, el de
  ejemplo su gris tenue y lo apagado su gris de apagado (informe 4.15.1).
- FIX-033 · 2026-11-11 · versión 4.16.0 · Qué pasaba: en «Fechas clave», quien escribía el nombre de una
  fecha y pulsaba Aceptar sin «Añadir» la perdía sin aviso; Cancelar tampoco preguntaba. Por qué: Aceptar
  solo guardaba la lista ya añadida y lo escrito no contaba como cambio. Regla: lo escrito en un
  formulario interior y sin añadir cuenta: Aceptar lo añade (o avisa y no cierra) y Cancelar pregunta
  antes de perderlo.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

Serie 4 (lo más reciente primero):

- Versión 4.16.0 (informe 4.15.1, aprobado entero el 2026-11-10): el ✓ de la meta cumplida sigue
  apareciendo con un leve aumento de 150 ms: es una transformación, que la norma del taller admite
  («solo opacity o transform y 150 ms como máximo»), así que no se cambia por un fundido. La leyenda no
  añade paradas al tabulador: cada cuadrito ya es una imagen con su nombre («de 3 a 6 tarjetas») que el
  lector de pantalla lee en la propia leyenda. Los títulos de las tarjetas ya eran encabezados (comprobado
  de nuevo en el código). Las tarjetas siguen repartiéndose el ancho del mapa y el panel no lleva índice
  ni pestañas (apartado 9 y 7.4 del informe). El color de enlace, el gris tenue y el gris de apagado se
  toman de Anki: con Atelier dan las cifras del informe; sin Atelier, de noche, el gris tenue de Anki es
  más oscuro (#545454) y el texto de ejemplo contrastaría menos.

- Versión 4.15.0 (informe «textos, hábito y abandono» del cliente, 2026-11-09): «Promedio diario» y
  «Retención» no se muestran sin dato, en lugar de «N/A» con su motivo, para no recibir con un panel
  de ceros el primer día ni al volver tras mucho tiempo. Con la racha a cero, la línea es «hoy
  pendiente · [plan]» y no «Última sesión: hace N días». «Perdonado» pasa a «cubierto». Las líneas
  grises de las tarjetas y el pie del mapa empiezan siempre en minúscula, salvo la mayúscula que
  exige la ortografía (sustantivos alemanes), y no se cortan con «…» (accesibilidad). Lo pidió el
  cliente el 2026-11-09.

- Las tarjetas no tienen globos (historial de la meta, récord, comodines, objetivo de retención y
  motivo de «N/A»): se descubrían poco, tapaban la cifra y repetían lo que está en Opciones o en
  Anki. Lo decidió el cliente el 2026-11-09 (versión 4.14.0). El historial de la meta sigue en
  Opciones; el récord se dice como distancia («a 3 días del récord») y solo cuando está cerca; el
  motivo de «N/A» va en la línea gris. Con la racha a cero o lejos del récord, no se ve cuál es el
  récord: ahí no motiva. Si un día se echa de menos el objetivo de retención, la vuelta prevista es
  «últimos 30 días · objetivo 90 %» en la línea gris, sin globo. El único globo de las tarjetas es
  el del sistema cuando una línea gris está cortada con «…».

- «0 de 2» en «Hoy» con una sola tarjeta por estudiar en la lista de mazos no es un fallo: con la
  meta «Un número», el 2 es la meta elegida, no lo que vence. Comprobado el 2026-11-04 (informe 4.11,
  apartado 4.3).
- El texto sobre el azul de acción sigue en blanco también de noche (4,9:1; de día, 4,6:1): la
  paleta Nocturne lo fija así. El informe 4.8 proponía texto oscuro; se revisó el 2026-11-04 y no se
  cambia porque ya cumple y la paleta manda. El borde de los controles de Opciones da 3,2:1 o más en
  los dos modos.
- Los títulos de las tarjetas ya eran encabezados para el lector de pantalla; el informe 4.11 lo
  daba por pendiente. Comprobado en el código el 2026-11-04.
- El globo de los días del mapa no se puede recorrer con el ratón (FIX-029), aunque WCAG 2.2 lo pide
  (criterio 1.4.13). El cliente aceptó la desviación en el informe 4.10. Los de los cuadritos de la
  leyenda sí se pueden recorrer.
- «Sin dato» no tiene cuadrito en la leyenda: es fondo, no información (informe 4.11, aprobado el
  2026-11-04).

Las entradas de la serie 3 que siguen describen decisiones que la serie 4 cambió en parte (vuelven la
leyenda y las iniciales de los días, desaparecen los botones de periodo y el borde naranja de las
fechas clave, hay cuatro tonos por tema en lugar de diez). Se conservan como historia; manda
la descripción «Qué hace».

- La retención usa la misma ventana que el promedio, y solo días completos. Lo decidió el cliente el
  2026-10-08.
- Las tarjetas borradas cuentan en el mapa general (no en el de un mazo, porque ya no tienen mazo).
  Lo decidió el cliente el 2026-10-08.
- La medida «minutos» se retiró: hay días con cientos de repasos guardados sin tiempo y la cifra no
  era coherente. Lo decidió el cliente el 2026-10-08.
- Con la medida «Nuevas», un día estudiado sin nuevas sale en gris, y un promedio que se queda en 0
  se escribe «N/A». Lo decidió el cliente el 2026-10-08 y el 2026-10-09. Desde la versión 3.4.0
  (cliente, 2026-10-13), todas las cifras siguen la medida: con «Nuevas», un día cuenta como
  estudiado solo si empezó alguna nueva (promedio, días estudiados, rachas y última sesión).
- Los periodos de 7 y 90 días se retiraron al poner los botones rápidos de periodo junto al año,
  como control segmentado sin marco: el elegido con fondo suave de pastilla y negrita, como en la
  imagen que aportó («30 días», «1 año», «Todo»). Lo pidió el cliente el 2026-10-13.
- Versión 3.5.0 (plan aprobado por el cliente el 2026-10-13, con criterios de diseño citados en la
  entrega): cifras en dos grupos (constancia y rendimiento) con la racha actual primero, número
  grande y unidad pequeña, misma letra que Anki, globos con la fecha en gris y cierre con Esc, y
  botones de periodo de al menos 24 píxeles de alto. El cliente descartó la llama de la racha y sus
  globos de motivación.
- El globo del año lleva el signo de exclamación de cada idioma; en español, los dos («¡…!»). Lo
  pidió el cliente el 2026-10-13.
- La retención no tiene globo explicativo. Lo retiró el cliente el 2026-10-09.
- Las ventanas de excluir mazos y de fechas clave no llevan textos de ayuda. Lo decidió el cliente.
- Las siete escalas de los temas son colores propios, fuera de la paleta Nocturne, que no tiene
  escalas de diez tonos. Lo aprobó el cliente el 2026-10-08; el 2026-10-13 aprobó rehacerlas a partir
  de los tonos de Nocturne, con escalones iguales. Los tres grises de los días futuros también eran
  propios hasta la 4.12.0; desde la 4.13.0 salen de la paleta de Anki o de Atelier (aprobado el
  2026-11-04, informe de Atelier 3.7, apartado 1.6).
- 4.13.0 · Con Atelier en Atardecer de noche y el tema Rosa suave, el gris de los días con más carga
  es tan marcado como el primer tono rosa (1,66 frente a 1,59 a 1 sobre la tarjeta). No se cambian
  las proporciones, que con Nocturne dan los grises aprobados: se distinguen por el color. Decisión
  del taller.
- Los mazos excluidos y las fechas clave se guardan sin paso de deshacer, porque son ajustes y no
  estudio, como hace Anki con sus búsquedas guardadas. Criterio del complemento original.
- Las cifras del mapa se leen directamente de la base de datos, solo para leer, porque Anki no ofrece
  ninguna función que dé la actividad por día. Criterio del complemento original, confirmado en la
  revisión del 2026-10-12: Anki 26.09.3 sigue sin esa función.
- Versión 3.3.0 (pedido del cliente el 2026-10-13, tras ver la 3.2.0): sin recuadro alrededor del
  mapa, sin leyenda y sin las iniciales de los días; los cuatro botones encima y el año debajo, como
  en la 3.1.1; la muestra del tema en Opciones vuelve a ser un solo cuadrito.
- El globo de cada día lleva la fecha arriba (sin «el») y lo hecho debajo, en todos los idiomas. Lo
  pidió el cliente el 2026-10-13.
- Las fechas clave llevan el borde naranja de siempre, y azul en los temas Rojo fuego, Naranja
  atardecer y Rosa suave, donde el naranja no se distingue. Lo eligió el cliente el 2026-10-13.
- Las cifras de debajo del mapa se escriben en el color del texto, con un cuadrito del tono delante,
  y no en el tono del tema. Lo eligió el cliente el 2026-10-13: los tonos claros no se leían.
- Los botones del mapa ya no funden el color al pasar el ratón; solo se hunden un instante al
  pulsarlos. La guía del taller pide no animar el color (versión 3.2.0, plan aprobado el
  2026-10-13).
- Al cambiar de año o una opción de aspecto, el mapa no se vuelve a calcular: usa los datos que ya tiene
  hasta que Anki redibuja la pantalla (al volver del repaso, sincronizar o deshacer, y cada 10
  minutos). Así cambiar de año es inmediato (versión 3.2.0).
