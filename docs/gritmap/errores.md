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
- FIX-026 · 2026-10-22 · versión 4.7.0 · Qué pasaba: con la meta «Terminar lo de hoy» ya cumplida,
  la tarjeta «Hoy» podía volver a decir «faltan 3» al rato sin haber hecho nada mal. Por qué: las
  tarjetas en aprendizaje vuelven a vencer horas después y la meta se recalculaba con ellas. Regla:
  una meta cumplida queda cumplida el resto del día; solo vuelve atrás si se deshace la respuesta que
  la cumplió.
- FIX-027 · 2026-10-26 · versión 4.9.0 · Qué pasaba: en la fila de arriba del mapa, el recuadro de
  «hoy» y el de los días perdonados se veían cortados un pelín por arriba. Por qué: esos recuadros
  sobresalen un poco del cuadrito y el mapa recortaba todo lo que salía de su dibujo. Regla: lo que se
  dibuja alrededor de un cuadrito siempre cabe entero, también en los bordes del mapa.

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
  Desde la 4.7.0 (cliente, 2026-10-22, al aprobar el informe de mejora integral), la racha, la
  última sesión y «Mes completo» cuentan cualquier respuesta, sea cual sea la medida: con «Nuevas»,
  un día de solo repasos ya no rompe la racha ni gasta un comodín. La medida sigue mandando en el
  color, el promedio, los días estudiados y la meta.
- Los periodos de 7 y 90 días se retiraron al poner los botones rápidos de periodo junto al año,
  como control segmentado sin marco: el elegido con fondo suave de pastilla y negrita, como en la
  imagen que aportó («30 días», «1 año», «Todo»). Lo pidió el cliente el 2026-10-13. Desde la 3.6.0
  (cliente, 2026-10-21) el selector está encima de las tres cifras que cambia (promedio, días
  estudiados y retención) y no junto al año; las rachas forman aparte el grupo «Rachas». En la 4.0.0
  pasó a la tarjeta «Estadísticas»; desde la 4.1.0, al retirarse esa tarjeta, se elige solo en
  Opciones (lo eligió el cliente el 2026-10-21).
- Versión 3.5.0 (plan aprobado por el cliente el 2026-10-13, con criterios de diseño citados en la
  entrega): cifras en dos grupos (constancia y rendimiento) con la racha actual primero, número
  grande y unidad pequeña, misma letra que Anki, globos con la fecha en gris y cierre con Esc, y
  botones de periodo de al menos 24 píxeles de alto. El cliente descartó la llama de la racha y sus
  globos de motivación.
- El globo del año llevaba el signo de exclamación de cada idioma (cliente, 2026-10-13). Desde la
  4.0.0 el total del año está siempre a la vista en el título de «Actividad» («12.480 repasos en
  2026») y ese globo se retiró (informe de rediseño aprobado por el cliente el 2026-10-21).
- La retención no tiene globo explicativo. Lo retiró el cliente el 2026-10-09.
- Las ventanas de excluir mazos y de fechas clave no llevan textos de ayuda. Lo decidió el cliente.
- Las escalas de los temas son colores propios, fuera de la paleta Nocturne, que no tiene escalas.
  Lo aprobó el cliente el 2026-10-08 (siete temas de diez tonos) y el 2026-10-13 (rehechas a partir de
  Nocturne). Desde la 4.0.0 (informe del cliente, 2026-10-21) son cuatro temas de cuatro tonos, con
  los valores del informe. Los días futuros llevaron un punto en la 4.0.0; desde la 4.1.0 vuelven a
  ir en gris, con cuatro tonos tomados de la escala gris aprobada el 2026-10-13 (cliente,
  2026-10-21).
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
- Los días sin estudio usan, de día, el gris de borde suave de Nocturne y, desde la 4.0.0, de noche
  el fondo hundido. En la 3.6.0 el mapa iba sobre la página y el fondo hundido se perdía de noche;
  ahora va sobre una tarjeta más clara, donde es el borde suave el que se pierde (1,02:1) y el hueco
  se lee como «no estudió». Criterio técnico, comprobado en pantalla el 2026-10-21.
- Los dos grupos de cifras ya no llevan una raya entre ellos: los separa el espacio, ahora que cada
  uno tiene su cabecera (versión 3.6.0).
- El globo de cada día lleva la fecha arriba (sin «el») y lo hecho debajo, en todos los idiomas. Lo
  pidió el cliente el 2026-10-13.
- Las fechas clave llevaron un borde naranja, o azul en tres temas (cliente, 2026-10-13), y en la
  4.0.0 una ★ sobre su semana. Desde la 4.1.0 el cliente pidió otra manera de encontrarlas y quitar
  la estrella de «Próxima fecha»: llevan una esquina doblada en su propio cuadrito, en el color del
  texto con un filo del color de la tarjeta (igual en todos los temas), y el nombre de la próxima
  fecha es un enlace que lleva a su día en el mapa. Criterio técnico para la forma, 2026-10-21.
- Las cifras se escriben en el color del texto, no en el tono del tema (cliente, 2026-10-13: los
  tonos claros no se leían). Los cuadritos de color que llevaban delante se retiraron en la 4.0.0,
  porque usaban un color sin explicar (informe del cliente, 2026-10-21).
- Los botones del mapa ya no funden el color al pasar el ratón; solo se hunden un instante al
  pulsarlos. La guía del taller pide no animar el color (versión 3.2.0, plan aprobado el
  2026-10-13).
- Al cambiar de año o una opción de aspecto, el mapa no se vuelve a calcular: usa los datos que ya tiene
  hasta que Anki redibuja la pantalla (al volver del repaso, sincronizar o deshacer, y cada 10
  minutos). Así cambiar de año es inmediato (versión 3.2.0).

Versión 4.0.0 (informe de rediseño del cliente, aprobado el 2026-10-21, las tres tandas):

- Tres bandas de tarjetas: resumen (Hoy, Racha, Retención y Próxima fecha), «Actividad» y
  «Estadísticas» plegable. La fila de resumen va debajo de la lista de mazos y no encima, como en la
  captura de referencia: Anki no ofrece a los complementos un sitio encima y la alternativa era un
  truco en su página que podría romperse. Lo eligió el cliente el 2026-10-21.
- La superficie de las tarjetas es la capa elevada de Nocturne (CANVAS_ELEVATED) y no el #FFFFFF y
  #1A2130 del informe: la paleta no admite blanco puro de fondo ni colores fuera de sus tokens.
  Criterio técnico.
- Al cumplir la meta, el ✓ aparece con un aumento de 150 ms (escala y transparencia), no el cierre
  del anillo en 300 ms del informe: la guía del taller limita las animaciones a 150 ms. Lo eligió el
  cliente el 2026-10-21. Solo la primera vez que se dibuja tras cumplirla.
- La meta nunca afecta a la racha: basta un repaso para que el día cuente.
- Con «Terminar lo de hoy», la meta se cuenta en tarjetas (respondidas hoy frente a esas más las que
  aún vencen, con los límites de Anki y sin los mazos excluidos), sea cual sea la medida del mapa.
- Comodines: uno cada 7 días seguidos, dos como máximo, se gastan solos; activados por defecto.
- En la pausa, un día sin estudiar ni suma ni rompe; un día de pausa en que sí estudió cuenta como
  siempre. El informe no decía qué pasa si se estudia en pausa; criterio técnico, para no quitarle a
  nadie un día estudiado.
- Las sorpresas son como mucho una al día, solo con datos reales y solo si hoy ya cuenta: nueva racha
  más larga, mejor día del año (con al menos 7 días estudiados antes), mes completo y cifras redondas
  del año (100, 500 y cada 1.000). No hay avisos de pérdida, urgencia, azar ni comparación social.
- La constancia de la semana y las dos barras usan los 7 días completos que terminan ayer y los 7
  anteriores, como la comparativa de siempre (Regla de FIX-001); la comparativa ya no va junto a la
  línea de Anki.
- «Hoy» solo se ve en otro año o, con cuadritos grandes, cuando la semana de hoy queda fuera de la
  vista; su hueco queda reservado.
- Se retiraron Rojo fuego (el rojo significa error), Rosa suave y Turquesa laguna; quien los tenía
  pasa al tema más cercano y Opciones lo dice una vez.

Versión 4.1.0 (correcciones del cliente del 2026-10-21 sobre la 4.0.0):

- El mapa va arriba y a todo el ancho por defecto: los cuadritos crecen con la ventana (desde 10 px;
  por debajo, desplazamiento de lado). Las tarjetas pequeñas van debajo del mapa y suman su mismo
  ancho, para que el conjunto quede simétrico. Lo pidió el cliente; eligió «llenar todo el ancho».
- La tarjeta «Estadísticas» se retiró, con su plegado, la constancia de la semana, las dos barras y
  los anillos de días estudiados y meta cumplida. En su lugar hay una tarjeta «Promedio diario». La
  racha más larga pasa a la línea de «Racha» («récord: 40 días»).
- «récord» va en minúscula, también al principio de la línea («Día 1» / «récord: 45 días»). Lo pidió
  el cliente; en alemán se conserva la mayúscula, porque allí los sustantivos la llevan.
- El globo de los días ya no dice si se cumplió la meta. Lo pidió el cliente.
- La tarjeta «Próxima fecha» ya no lleva estrella. Lo pidió el cliente.

Versión 4.2.0 (correcciones del cliente del 2026-10-21 sobre la 4.1.0):

- Sin enlaces en las tarjetas: ni el nombre de la próxima fecha, ni «Añadir», ni «Fijar meta», ni
  «Cambiar mazos excluidos». El cliente dijo «no quiero enlaces»; se aplicó a todos. La meta, las
  fechas y los mazos excluidos se cambian en Opciones.
- Las fechas clave se marcan con una estrella en su cuadrito (en lugar de la esquina doblada de la
  4.1.0). Lo pidió el cliente.
- «Todo el ancho» no era literal: el mapa vuelve a medir lo que piden sus cuadritos, centrado, como en
  las primeras versiones, y las tarjetas de debajo toman su ancho. Vuelven «Tamaño de celda» y
  «Redondeo de esquinas» en píxeles (25 y 1 de serie); se quitan «Tamaño», «Forma» y la vista previa.
  Lo pidió el cliente.
- En lugar de la vista previa, el propio mapa cambia en vivo mientras se mueven las barras, y vuelve a
  como estaba al cancelar. Criterio técnico para «más intuitivo».
- Sin meta, la línea de «Hoy» da lo hecho en los 7 últimos días completos (Regla de FIX-001).

Versión 4.3.0 (correcciones del cliente del 2026-10-21 sobre la 4.2.0):

- La ventana de opciones vuelve a ser una sola lista, como en las primeras versiones, sin grupos con
  título, con el cuadrito de muestra de cada tema y con campos numéricos con flechas para el tamaño de
  celda y el redondeo («Tamaño de celda (px)»), en lugar de barras deslizantes. Lo pidió el cliente con
  una captura. El alto de la ventana se ajusta siempre a su contenido: una altura guardada por otra
  versión dejaba un hueco entre «Apariencia» y «Qué se cuenta».
- Sobre el mapa no hay título «Actividad» ni la cifra del año («22.129 repasos en 2026»); los botones
  quedan centrados y «Hoy» siempre a la vista, como en las primeras versiones. Lo pidió el cliente.
- «Próxima fecha» dice solo el nombre, sin la fecha al lado. Lo pidió el cliente.

Versión 4.4.0 (correcciones del cliente del 2026-10-21 sobre la 4.3.0):

- De serie, el mapa vuelve a verse como en la 4.1.0: a todo el ancho, con cuadritos que crecen con
  la ventana y esquinas apenas redondeadas. El tamaño en píxeles sigue en Opciones («Tamaño de celda
  (px)», cuyo primer valor es «Ajustado al ancho»). Lo pidió el cliente con una captura. Para que todos
  vean ese aspecto, el tamaño y el redondeo guardados por la 4.2 o la 4.3 se dejan de leer.
- Vuelven los recuadros con título en Opciones («Apariencia», «Qué se cuenta», «Metas y fechas»). Lo
  pidió el cliente.
- Sin fechas clave por venir, «Próxima fecha» dice «N/A» y, debajo, «sin fechas clave» en minúscula.
  Lo pidió el cliente.
- No hay botón «Hoy»: el mapa ya se abre en la semana de hoy. Lo pidió el cliente.

Versión 4.5.0 (petición del cliente del 2026-10-21 sobre la 4.4.0):

- «Tamaño de celda (px)» pasa a ser «Tamaño»: con un tamaño, el mapa entero crece o encoge en
  proporción, con el mismo dibujo que «Ajustado al ancho» (huecos de 3/14 del cuadrito y esquinas a
  escala). Antes el hueco se quedaba en 3 px y el redondeo en píxeles, y el mapa dejaba de parecerse.
  Lo eligió el cliente entre dos opciones. El redondeo va de 0 a 7 (7 ya es un círculo); un valor
  mayor guardado antes se queda en 7.

Versión 4.6.0 (petición del cliente del 2026-10-21 sobre la 4.5.0):

- El campo se llama «Tamaño del mapa» y, de serie, mide 24 px (ya no «Ajustado al ancho», que sigue
  como primer valor). Para que todos lo vean, el tamaño y el redondeo guardados por la 4.2 a la 4.5
  se dejan de leer. Lo pidió el cliente.
- El redondeo lleva «px» y va en píxeles reales del cuadrito, de 0 a 15 (3 px de serie, la misma
  proporción que la 4.1.0 a 24 px). Lo pidió el cliente; los huecos siguen en proporción.

Versión 4.7.0 (informe de mejora integral, aprobado por el cliente el 2026-10-22):

- El mapa sigue a 24 px aunque no quepa y entonces se desplaza de lado; el informe proponía encoger
  el cuadrito hasta que cupiera. Lo decidió el cliente.
- La pausa empieza hoy como pronto; una pausa ya guardada que empezó antes conserva su inicio. Lo
  decidió el cliente.
- El botón de opciones va aparte, en la esquina de arriba de la tarjeta del mapa. Lo decidió el
  cliente.
- La muestra de cada tema en Opciones sigue siendo un solo cuadrito (el informe proponía una tira de
  cuatro tonos), porque así lo pidió el cliente con una captura en la 4.3.0.
- La rejilla del mapa va siempre de izquierda a derecha, también en árabe o hebreo (regla de
  FIX-023), así que las iniciales de los días van siempre a la izquierda.

Versión 4.7.1 (petición del cliente del 2026-10-22 sobre la 4.7.0):

- «Promedio diario» dice solo el periodo, sin «por día estudiado», aunque la cifra sigue siendo por
  día estudiado. Lo pidió el cliente.
- «Próxima fecha» dice solo el nombre, sin el día de la semana. Lo pidió el cliente.
- «Periodo de las cifras» se elige con tres botones, como «El color mide». Lo pidió el cliente.

Versión 4.8.0 (revisión de experiencia de uso aprobada por el cliente el 2026-10-26):

- Las fechas clave llevan un rombo de hito en lugar de la estrella: lleno en las que vienen, hueco y
  gris en las pasadas. Se quita la fila aparte de los cuadritos pequeños: el rombo se lee a 10 px.
- «Próxima fecha» solo aparece si hay alguna fecha de hoy en adelante: puede haber cinco, cuatro o
  tres tarjetas. Sustituye a la decisión de la 4.4.0 («N/A» con «sin fechas clave»).
- «Promedio diario» es por día natural del periodo, desde el primer día estudiado dentro de él; los
  días de pausa no cuentan y los de comodín sí. Los cortes de color del mapa y la meta propuesta siguen
  por día estudiado, porque describen un día en que se estudia.
- Los días pendientes van en tres grises más suaves que el primer tono de cualquier tema, en lugar de
  cuatro (resuelve lo pendiente de la 4.7.0).
- «Un año seguido» pasa de la línea de «Racha» a ser la primera línea de sorpresa.
- Si el año no cabe, el borde por donde sigue se desvanece. Las iniciales de los días se desplazan
  con el mapa: fijas, dejaban asomar trozos de cuadritos en el borde (criterio técnico, comprobado en
  pantalla).
- El objetivo de retención sale también en la lista de mazos si todos los mazos que cuentan usan la
  misma retención deseada.

Versión 4.9.0 (informe «últimos retoques y panel de opciones a medida», aprobado por el cliente el
2026-10-26):

- La ventana de opciones es un panel dibujado a medida, no controles estándar de Anki. Lo pidió el
  cliente, aunque la guía de interfaz prefiere lo nativo; por eso se cuidan aparte el teclado, el modo
  noche y el modo de alto contraste.
- Los colores del panel son los de la paleta Nocturne, no los que proponía el informe: ningún color
  inventado (criterio técnico).
- Al cerrar sin aceptar, solo se pregunta si hay cambios en las fechas clave; el resto se descarta sin
  preguntar, porque se ve al instante y se rehace en un momento. Lo decidió el cliente.
- La meta propuesta parte del mismo «Promedio diario» que enseña la tarjeta, para que las dos cifras
  cuadren. Sustituye a la decisión de la 4.8.0 de proponerla por día estudiado.
- «Ahora tiene N comodines» solo aparece si el mapa abierto es el de la lista de mazos: en la pantalla
  de un mazo la cifra sería la de ese mazo, no la de la racha completa (criterio técnico).
- La semana que empieza según el idioma se propuso y se descartó: el mapa sigue empezando en lunes.
  Lo decidió el cliente.
