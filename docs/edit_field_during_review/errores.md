# Errores de «Edit field during review»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las tres primeras se hicieron antes de que el complemento llegara a este taller; la versión
exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

(Ninguno.)

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-24 · versión anterior a la 1.0.0 (no consta) · Qué pasaba: al editar un campo
  largo, de varias líneas, que se muestra dentro de un texto (por ejemplo, en cursiva), el recuadro
  azul salía troceado, un recuadro por línea, en vez de uno solo. Por qué: el navegador dibuja el
  contorno de un texto en línea por trozos, uno por cada línea que ocupa. Regla: el campo en edición
  se convierte en una caja solo si se muestra en línea, comprobándolo en ese momento; los campos que
  ya son un bloque no se tocan, para que no se muevan de sitio.
- FIX-002 · 2026-07-24 · versión anterior a la 1.0.0 (no consta) · Qué pasaba: la tecla Escape
  guardaba el cambio en lugar de descartarlo y, al cancelar, seguía viéndose en pantalla el texto
  tecleado aunque no se hubiera guardado. Por qué: Escape e Intro compartían la misma salida, que
  siempre guardaba, y al cancelar solo se restauraba la vista en algunos casos. Regla: Intro confirma
  y Escape descarta, como en cualquier programa; cancelar nunca escribe en la colección y deja la
  pantalla exactamente como estaba antes de empezar a editar.
- FIX-003 · 2026-07-24 · versión anterior a la 1.0.0 (no consta) · Qué pasaba: al contestar la
  tarjeta justo después de editar, el complemento seguía trabajando sobre la tarjeta nueva. Por qué:
  el guardado termina un poco después de la pulsación y, para entonces, en pantalla ya podía haber
  otra tarjeta. Regla: al terminar un trabajo en segundo plano, se comprueba que lo que hay en
  pantalla sigue siendo la nota editada antes de tocar nada.
- FIX-004 · 2026-11-09 · versión 1.1.0 · Qué pasaba: una tarjeta preparada a propósito (por ejemplo,
  de un mazo compartido descargado) podía hacer que la pantalla de repaso cargara, a través de este
  complemento, archivos de estilo o de código de otros complementos instalados. Por qué: la regla con
  que el complemento comparte sus archivos con el repaso dejaba pasar cualquier ruta. Regla: solo se
  comparten sus dos archivos, con una regla cerrada, como en GritMap.
- FIX-005 · 2026-11-09 · versión 1.1.0 · Qué pasaba: el recuadro azul de edición tenía dos azules
  propios, fuera de la paleta, así que con Atelier en Bosque, Lavanda, Atardecer o Papel seguía azul
  aunque el color de acción fuera otro. Por qué: los colores estaban escritos a mano. Regla: el
  recuadro usa el color de foco de la paleta, de día y de noche.
- FIX-006 · 2026-11-17 · versión 1.1.0 · Qué pasaba: si dos campos de una nota tenían exactamente el
  mismo contenido y la plantilla ponía cada uno en su bloque (por ejemplo, «Palabra» y «Lectura» con
  «すし»), al editar el segundo en pantalla el cambio se guardaba en el primero. Por qué: cada campo se
  reconoce en la tarjeta por su texto, y dos textos iguales no se distinguen. Regla: si dos campos
  tienen el mismo contenido, ninguno se ofrece para editar sobre la tarjeta; antes no editar que
  guardar en el campo equivocado.
- FIX-007 · 2026-11-17 · versión 1.1.0 · Qué pasaba: al guardar un campo con una fórmula (MathJax), en
  su sitio quedaba su código («\(x^2\)») hasta pasar a la otra cara. Por qué: el trozo se redibujaba
  con el texto de Anki sin pedir que se dibujaran sus fórmulas. Regla: todo trozo redibujado que pueda
  llevar fórmulas pide a MathJax que las dibuje, solo en ese trozo.
- FIX-008 · 2026-11-17 · versión 1.1.0 · Qué pasaba: en tarjetas de huecos cuya plantilla pone el
  texto con huecos y otro campo (por ejemplo, «Reverso extra») en un mismo bloque, el complemento
  tomaba el bloque entero por el campo de huecos: el otro no se podía editar y desaparecía mientras se
  editaba el de huecos. Por qué: se marcaba el primer bloque con todo el texto de los huecos, aunque
  tuviera también el de otro campo. Regla: un bloque solo se toma por un campo si no contiene el
  texto de otro; si lo contiene, se envuelve solo el tramo con los huecos.
- Sin nota en el código · 2026-11-17 · El pendiente «el recuadro azul usa dos azules fijos propios»
  ya estaba resuelto por FIX-005 (2026-11-09); se quita de «Pendientes».

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- Para empezar a editar hay que mantener Ctrl (⌘ en Mac) al hacer clic; se puede quitar en las
  opciones. Así no se entra a editar sin querer al seleccionar texto. Decisión del autor original.
- Una edición abierta se guarda al hacer clic fuera, al pulsar los botones de abajo o al pasar de
  cara o de tarjeta, para no perder lo escrito; solo Escape descarta. Decisión del autor original.
- En el repaso, al guardar, la tarjeta no se vuelve a dibujar entera: se deja lo que usted escribió
  (y en los campos de huecos se redibuja solo ese trozo), para que la pantalla no salte. Decisión del
  autor original.
- Si al terminar no ha cambiado nada, no se guarda ni se crea un paso de deshacer. Decisión del
  autor original.
- La ventana de opciones se titula «Edit field during review», en inglés, en todos los idiomas,
  porque el nombre del complemento no se traduce. Decisión del autor original.
