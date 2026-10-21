# Errores de «Always on Top»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. La FIX-001 se hizo antes de que el complemento llegara a este taller (versión 1.2); su
versión exacta no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 1.2 · Qué pasa: la ventana de opciones acepta como atajo seis combinaciones
  que el editor de la ventana Añadir de Anki 26.09.3 ya usa: Ctrl+. (lista numerada), Ctrl+, (lista
  con viñetas), Ctrl+Mayús+. y Ctrl+Mayús+, (aumentar y reducir la sangría de una lista), y Ctrl+= y
  Ctrl+Mayús+= (superíndice y subíndice). Por ejemplo, si elige Ctrl+. y pulsa «Aceptar», no sale
  ningún aviso y, desde entonces, dentro de Añadir esa combinación enciende o apaga «siempre visible»
  y ya no crea la lista numerada. Por qué: la lista de atajos ocupados se sacó de Anki 25.09 y no
  recoge esos atajos del editor; es justo lo que la regla de FIX-001 quería evitar. Propuesta: añadir
  esas seis combinaciones a la lista de atajos ocupados y revisarla entera contra Anki 26.09.3. El
  atajo por defecto, Ctrl+Mayús+O, no está afectado: Anki 26.09.3 no lo usa.
- 2026-10-21 · versión 1.2 · Qué pasa: si tiene abiertas a la vez las dos versiones de la ventana
  Añadir (la normal y la que Anki abre si se pulsa Añadir con Mayús), el atajo solo cambia la última
  que se abrió. Por ejemplo: con «siempre visible» encendido abre Añadir, después la otra con Mayús,
  y pulsa el atajo para apagarlo; el aviso dice «Siempre visible: desactivado», pero la primera sigue
  por encima de todo hasta que la cierre. Por qué: el complemento solo recuerda una ventana Añadir, y
  Anki 26.09.3 permite tener las dos abiertas. Propuesta: que recuerde todas las ventanas Añadir
  abiertas y aplique el cambio a cada una. Es un caso raro: solo ocurre si usa las dos versiones a la
  vez.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-28 · versión 1.2 o anterior · Qué pasaba: el atajo por defecto era Ctrl+Mayús+T,
  que Anki usa dentro de la ventana Añadir para saltar al campo de etiquetas, así que los dos se
  peleaban por la misma tecla. Por qué: se eligió el atajo por su nombre («Top») sin mirar qué atajos
  usa ya Anki. Regla: todo atajo por defecto, y todo atajo que se le ofrezca a usted, se compara antes
  con la lista de atajos que Anki ya usa; si coincide, no se usa. Desde entonces el atajo por defecto
  es Ctrl+Mayús+O.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- Si el atajo guardado no lleva Ctrl ni Alt, no se entiende o coincide con uno de la lista de Anki
  (por ejemplo, porque viene de una versión anterior), al abrir Anki se usa Ctrl+Mayús+O sin avisar:
  dos atajos peleándose por la misma tecla dan un resultado imprevisible. Decisión del autor
  original.
- La ventana de opciones no se cierra con una combinación que no sirve: avisa y espera a que elija
  otra o cancele. Decisión del autor original.
- Vaciar la casilla y aceptar no deja el complemento sin atajo: vuelve a Ctrl+Mayús+O. Decisión del
  autor original.
- El atajo responde en cualquier ventana de Anki, no solo en Añadir, y sigue funcionando tras cambiar
  de perfil; así se puede encender antes de abrir Añadir. Decisión del autor original.
- En Windows, con Añadir ya a la vista, el cambio se hace con una llamada propia de Windows y no con
  la vía general, porque esta oculta y vuelve a mostrar la ventana (parpadeo). En Mac y Linux se usa
  la vía general y la ventana parpadea un instante. Decisión del autor original.
- Un mismo fallo avisa una sola vez por sesión, para no llenar la pantalla de avisos. Decisión del
  autor original.
- Los botones «Aceptar», «Cancelar» y «Restaurar los valores predeterminados», y el aviso al
  restaurar, usan los textos de Qt y de Anki y no textos propios, para que coincidan con el resto del
  programa. Decisión del autor original.
