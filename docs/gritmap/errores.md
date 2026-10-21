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
  Regla: sin días que promediar se escribe «N/A», y el globo explica por qué.

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

Las dos siguientes salieron de la revisión de la versión 3.6.0 (2026-10-21).

- FIX-024 · 2026-10-21 · versión 3.6.0 · Qué pasaba: al recorrer el mapa con el tabulador, los
  botones de encima y los de periodo no mostraban ningún contorno, así que no se sabía dónde estaba
  el foco. Por qué: Anki quita a propósito el contorno de todos los botones de sus páginas, y el del
  mapa no tenía fuerza suficiente para imponerse. Regla: el contorno de foco de cada botón del mapa
  se impone al de Anki y solo aparece con el teclado, nunca al hacer clic.
- FIX-025 · 2026-10-21 · versión 3.6.0 · Qué pasaba: abierta desde Herramientas > Complementos >
  «Configuración», la ventana de opciones podía quedarse detrás de la ventana Complementos en
  Windows. Por qué: se abría siempre sobre la ventana principal de Anki. Regla: una ventana que se
  abre desde otra se abre sobre la ventana activa (y, si esta se cerró entretanto, sobre la
  principal).

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

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
  imagen que aportó («30 días», «1 año», «Todo»). Lo pidió el cliente el 2026-10-13. Desde la 3.6.0
  (cliente, 2026-10-21) el selector está encima de las tres cifras que cambia (promedio, días
  estudiados y retención) y no junto al año; las rachas forman aparte el grupo «Rachas».
- Versión 3.5.0 (plan aprobado por el cliente el 2026-10-13, con criterios de diseño citados en la
  entrega): cifras en dos grupos (constancia y rendimiento) con la racha actual primero, número
  grande y unidad pequeña, misma letra que Anki, globos con la fecha en gris y cierre con Esc, y
  botones de periodo de al menos 24 píxeles de alto. El cliente descartó la llama de la racha y sus
  globos de motivación.
- El globo del año lleva el signo de exclamación de cada idioma; en español, los dos («¡…!»). Lo
  pidió el cliente el 2026-10-13.
- La retención no tiene globo explicativo. Lo retiró el cliente el 2026-10-09.
- Las ventanas de excluir mazos y de fechas clave no llevan textos de ayuda. Lo decidió el cliente.
- Las siete escalas de los temas y la escala gris de los días futuros son colores propios, fuera de
  la paleta Nocturne, que no tiene escalas de diez tonos. Lo aprobó el cliente el 2026-10-08; el
  2026-10-13 aprobó rehacerlas a partir de los tonos de Nocturne, con escalones iguales.
- Los mazos excluidos y las fechas clave se guardan sin paso de deshacer, porque son ajustes y no
  estudio, como hace Anki con sus búsquedas guardadas. Criterio del complemento original.
- Las cifras del mapa se leen directamente de la base de datos, solo para leer, porque Anki no ofrece
  ninguna función que dé la actividad por día. Criterio del complemento original, confirmado en la
  revisión del 2026-10-12: Anki 26.09.3 sigue sin esa función.
- Versión 3.3.0 (pedido del cliente el 2026-10-13, tras ver la 3.2.0): sin recuadro alrededor del
  mapa, sin leyenda y sin las iniciales de los días; los cuatro botones encima y el año debajo, como
  en la 3.1.1; la muestra del tema en Opciones vuelve a ser un solo cuadrito. La leyenda volvió en
  la 3.6.0, ahora con la cifra de cada tono: el cliente la pidió de nuevo el 2026-10-21, avisado de
  que la había quitado en la 3.3.0. Siguen sin recuadro y sin iniciales de los días.
- Versión 3.6.0 (propuesta de mejoras del cliente del 14-10-2026, aprobada el 2026-10-21):
  leyenda, cifras agrupadas por periodo, comparativa con su total, notas de la racha, próxima fecha
  clave a la vista, línea «Pulse para ver…» en el globo, mapa vacío que orienta, vista previa y
  frase de la medida en Opciones y «Restaurar apariencia». La comparativa dice «en 7 días» y «los
  7 anteriores», no «esta semana», porque mide los 7 días completos que terminan ayer (FIX-001); lo
  eligió el cliente el 2026-10-21.
- Las notas de la racha solo informan: «hoy pendiente» u «hoy hecho», la distancia al récord solo
  si está a 7 días o menos, y «nuevo récord» solo el día en que se bate. No hay avisos, cuentas
  atrás ni mensajes de pérdida: la propuesta del cliente los descarta por ser patrones que presionan
  (versión 3.6.0).
- Los días sin estudio usan el gris de borde suave de Nocturne y no el fondo hundido que proponía
  el documento de mejoras: de noche ese fondo es más oscuro que la página y la rejilla vacía casi
  desaparecería. Criterio técnico de la versión 3.6.0.
- Los dos grupos de cifras ya no llevan una raya entre ellos: los separa el espacio, ahora que cada
  uno tiene su cabecera (versión 3.6.0).
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
