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

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- La retención usa la misma ventana que el promedio, y solo días completos. Lo decidió el cliente el
  2026-10-08.
- Las tarjetas borradas cuentan en el mapa general (no en el de un mazo, porque ya no tienen mazo).
  Lo decidió el cliente el 2026-10-08.
- La medida «minutos» se retiró: hay días con cientos de repasos guardados sin tiempo y la cifra no
  era coherente. Lo decidió el cliente el 2026-10-08.
- Con la medida «Nuevas», un día estudiado sin nuevas sale en gris, y un promedio que se queda en 0
  se escribe «N/A». Lo decidió el cliente el 2026-10-08 y el 2026-10-09.
- La retención no tiene globo explicativo. Lo retiró el cliente el 2026-10-09.
- Las ventanas de excluir mazos y de fechas clave no llevan textos de ayuda. Lo decidió el cliente.
- Las siete escalas de los temas y la escala gris de los días futuros son colores propios, fuera de
  la paleta Nocturne, que no tiene escalas de diez tonos. Lo aprobó el cliente el 2026-10-08.
- Los mazos excluidos y las fechas clave se guardan sin paso de deshacer, porque son ajustes y no
  estudio, como hace Anki con sus búsquedas guardadas. Criterio del complemento original.
- Las cifras del mapa se leen directamente de la base de datos, solo para leer, porque Anki no ofrece
  ninguna función que dé la actividad por día. Criterio del complemento original; se revisa en la
  auditoría de 2026-10-12.
