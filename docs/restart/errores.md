# Errores de «Restart»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las tres primeras ya estaban en el código de la versión 2.0.0, la que llegó a este taller;
la versión exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 2.0.0 · Qué pasa: si pulsa el atajo de reinicio, Anki pregunta algo antes de
  cerrar (por ejemplo, si descarta lo escrito en la ventana Añadir) y usted elige no cerrar, la orden
  de reinicio sigue guardada unos segundos más, hasta cinco desde la última comprobación. Si en ese
  margen cierra Anki a mano (Ctrl+Q o el aspa de la ventana), Anki se vuelve a abrir solo en lugar
  de quedarse cerrado; y si en ese margen vuelve a pulsar el atajo, no hace nada. No se pierde nada:
  es una apertura que usted no pidió. Propuesta: anular el reinicio en cuanto el cierre se detiene,
  en lugar de esperar a la comprobación cada cinco segundos.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-28 · versión 2.0.0 o anterior · Qué pasaba: un atajo puesto en Ctrl+W no hacía
  nada en Mac ni en Linux, y se podía guardar un atajo que Anki ya usaba, con lo que no respondía ni
  el de Anki ni el del complemento. Por qué: en Mac y Linux Anki se queda la combinación de cerrar
  ventana antes de que llegue a ningún atajo, y las combinaciones ocupadas se comprobaban con una
  lista escrita a mano, incompleta y anticuada. Regla: nunca se acepta una combinación que el
  sistema reserve para cerrar ventana, y se le pregunta a la ventana principal qué combinaciones
  tiene ocupadas en ese momento (sin contar las del propio complemento).
- FIX-002 · 2026-07-28 · versión 2.0.0 o anterior · Qué pasaba: Anki se volvía a abrir sola al
  cerrarla mucho después, sin haber pedido ningún reinicio. Por qué: si el cierre del reinicio se
  quedaba a medias (por ejemplo, al responder que no a descartar lo escrito), la orden de reinicio
  seguía guardada y la cumplía el siguiente cierre. Regla: la orden caduca a los cinco minutos y se
  retira en cuanto se nota que el cierre no siguió adelante.
- FIX-003 · 2026-07-28 · versión 2.0.0 o anterior · Qué pasaba: el complemento ofrecía un segundo
  atajo para cerrar Anki, que repetía lo que ya hace Ctrl+Q, y sus dos ajustes seguían guardados
  después de retirarlo. Por qué: se añadió sin comprobar que Anki ya lo hacía de serie. Regla: antes
  de añadir una acción, se comprueba si Anki ya la hace; no se vuelve a añadir un atajo para cerrar
  Anki, y al guardar las opciones solo se escriben los ajustes que el complemento usa hoy.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- El nuevo Anki no se abre hasta que el anterior ha guardado y cerrado la colección y ha terminado la
  copia de seguridad, para que nunca haya dos Anki con la colección abierta a la vez. Por eso el
  reinicio tarda lo mismo que un cierre normal más una apertura. Decisión del autor original.
- Si el cierre tarda más de cinco minutos, Anki se cierra sin volver a abrirse: pasado ese plazo,
  un cierre ya no se toma como parte del reinicio (es la regla de FIX-002). Decisión del autor
  original.
- Si no identifica con seguridad el programa de Anki, no reinicia y avisa: cerrar Anki sin poder
  volver a abrirlo sería peor que no reiniciar. Decisión del autor original.
- Ctrl+W no se admite como atajo en ningún sistema, tampoco en Windows, donde sí funcionaría: se
  rechaza toda combinación que el sistema reserve para cerrar ventana (regla de FIX-001). Decisión
  del autor original.
- No se admiten teclas sueltas ni combinaciones con solo Mayúsculas: Anki reparte las teclas
  sueltas por toda su interfaz. Decisión del autor original.
- Si vacía el campo del atajo y pulsa Aceptar, se conserva el atajo guardado; para quitar el atajo
  se desmarca la casilla. Decisión del autor original.
- Las opciones se cambian en una ventana propia con casilla y campo, en lugar del editor de texto de
  Anki, y sin colores propios, para que siga el tema de Anki. Decisión del autor original.
- Si Anki está ocupado con una tarea con barra de progreso, el atajo no reinicia y lo dice, para no
  interrumpir esa tarea. Decisión del autor original.
