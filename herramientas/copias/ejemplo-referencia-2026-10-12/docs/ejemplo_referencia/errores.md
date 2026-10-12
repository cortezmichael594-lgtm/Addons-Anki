# Errores de «Ejemplo de referencia»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

(Ninguno.)

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-10-09 · versión 1.0.1 · Qué pasaba: con una sola nota, la pregunta y el aviso final
  decían «1 notas» («Se etiquetarán 1 notas con «ejemplo». ¿Continuar?» y «Se etiquetaron 1 notas…»).
  Por qué: las frases tenían el plural fijo, sin mirar la cifra. Regla: toda frase con una cifra tiene
  su forma en singular y en plural, y se elige por la cifra. Prueba de regresión: «TagMessagesTest»,
  que falló antes del arreglo y pasa después.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- 1.0.0 · Etiquetar notas no hace copia de seguridad antes de cambiar nada. Lo decide el criterio del
  taller: la copia previa se reserva para borrar o cambiar lo que ya existe, y añadir una etiqueta no
  es ninguna de las dos cosas. Sí hay confirmación con la cifra exacta y se puede deshacer.
