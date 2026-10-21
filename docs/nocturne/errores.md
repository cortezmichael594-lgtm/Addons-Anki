# Errores de «Nocturne»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 2026.07.28 · De día, las cifras «Aprendiendo» y «Para repasar» de la lista de
  mazos y el rojo de aviso se leen peor de lo recomendado. Propuesta: oscurecerlos lo justo, sin
  cambiar su tono.
- 2026-10-21 · versión 2026.07.28 · Las casillas y botones de opción sin marcar casi no se distinguen
  del fondo, de día y de noche. Propuesta: reforzar solo su borde; los campos, listas y tablas
  conservan los bordes suaves.
- 2026-10-21 · versión 2026.07.28 · De noche, en Explorar, el texto de las filas con bandera naranja,
  verde, azul, rosa o turquesa se lee mal. Propuesta: oscurecer esas banderas de noche lo justo.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-24 · versión anterior a 2026.07.28 · Qué pasaba: de noche, el degradado del fondo
  se veía repetido en varias manchas en lugar de una sola en la esquina. Por qué: al simplificar el
  estilo se quitó el anclaje del degradado a la ventana. Regla: el degradado del fondo va siempre
  anclado a la ventana, y no se quita nada de lo que ya funciona sin comprobar a la vista que el
  aspecto no cambia.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- 2026.07.28 · «Aprendiendo» va en naranja y no en el rojo de Anki. Es parte del aspecto original que
  el cliente quiere conservar (2026-10-21).
- 2026.07.28 · Los bordes de campos, listas y tablas son muy suaves. Es parte del aspecto original; la
  versión 2.0.0 los reforzó y el cliente la descartó por perder atractivo (2026-10-21).
