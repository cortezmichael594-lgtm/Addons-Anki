# Errores de «Nocturne»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

(Ninguno.)

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-24 · versión anterior a 2026.07.28 · Qué pasaba: de noche, el degradado del fondo
  se veía repetido en varias manchas en lugar de una sola en la esquina. Por qué: al simplificar el
  estilo se quitó el anclaje del degradado a la ventana. Regla: el degradado del fondo va siempre
  anclado a la ventana, y no se quita nada de lo que ya funciona sin comprobar a la vista que el
  aspecto no cambia.
- FIX-002 · 2026-10-21 · versión 2.1.0 · Qué pasaba: de día, las cifras «Aprendiendo» y «Para repasar»
  de la lista de mazos, las «Nuevas» sobre fondos hundidos y el rojo de aviso se leían peor de lo
  recomendado (entre 3,0 y 4,4). Por qué: esos colores se eligieron por cómo quedaban como iconos y no
  se midieron como texto. Regla: todo color que se use como texto llega a 4,5 sobre cualquier fondo, y
  se corrige oscureciéndolo sin cambiar su tono. Prueba: «TextContrastTest».
- FIX-003 · 2026-10-21 · versión 2.1.0 · Qué pasaba: una casilla sin marcar casi no se distinguía del
  fondo. Por qué: Anki dibuja su borde con el mismo color suave que otros detalles. Regla: las casillas
  tienen su propio borde visible y los demás bordes siguen suaves. Prueba: «CheckboxBorderTest».
- FIX-004 · 2026-10-21 · versión 2.1.0 · Qué pasaba: de noche, en Explorar, el texto de las filas con
  bandera naranja, verde, azul, rosa, turquesa o morada se leía mal. Por qué: Anki pinta esas filas con
  el color de la bandera oscurecido, y los tonos nocturnos seguían siendo demasiado claros. Regla: de
  noche, cada bandera deja su fila legible y sigue viéndose como icono; se oscurece sin cambiar el tono.
  Prueba: «ExplorerRowsTest».
- FIX-005 · 2026-10-21 · versión 2.1.0 · Qué pasaba: con el ratón encima del botón azul principal, su
  texto blanco perdía legibilidad. Por qué: el efecto de pasar el ratón aclaraba el azul. Regla: el
  azul de acción da 4,5 con texto blanco en todos sus estados. Prueba: «PrimaryButtonTest».

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- 2026.07.28 · «Aprendiendo» va en naranja y no en el rojo de Anki. Es parte del aspecto original que
  el cliente quiere conservar (2026-10-21).
- 2026.07.28 · Los bordes de campos, listas y tablas son muy suaves. Es parte del aspecto original; la
  versión 2.0.0 los reforzó y el cliente la descartó por perder atractivo (2026-10-21).
- 2.1.0 · De noche, las banderas son algo menos vivas que en la versión original. Es el precio de que el
  texto de las filas de Explorar se lea bien (FIX-004); el cliente aprobó el plan el 2026-10-21.
- 2.1.0 · Con el ratón encima o con el foco, el borde de las casillas es azul y no gris oscuro, para que
  se note el cambio. Decisión del taller dentro del plan aprobado.
