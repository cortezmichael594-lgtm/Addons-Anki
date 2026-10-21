# Errores de «Edit field during review»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las tres primeras se hicieron antes de que el complemento llegara a este taller; la versión
exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 1.0.0 · Qué pasa: si dos campos de una nota tienen exactamente el mismo
  contenido y la plantilla pone cada uno en su propio bloque (por ejemplo, «Palabra» y «Lectura» con
  «すし», como ocurre en japonés con las palabras escritas solo en kana), el complemento toma los dos
  por el primero. Al editar el segundo en pantalla, el cambio se guarda en el primer campo y el
  segundo se queda como estaba, aunque en pantalla se vean cambiados los dos. Se puede deshacer con
  Editar > Deshacer. Propuesta: reconocer cada campo por su sitio en la plantilla y no solo por su
  texto; mientras tanto, si dos campos coinciden, no dejar editar ninguno de los dos antes que
  guardar en el equivocado.
- 2026-10-21 · versión 1.0.0 · Qué pasa: una tarjeta preparada a propósito (por ejemplo, de un mazo
  compartido descargado) podría hacer que la pantalla de repaso cargue, a través de este complemento,
  archivos de estilo o de código de otros complementos que usted tenga instalados. La regla con que
  el complemento comparte sus dos archivos con la pantalla de repaso es demasiado abierta: es el
  mismo fallo que ya se corrigió en el complemento de ejemplo y en GritMap. Propuesta: una regla
  cerrada que solo deje pasar sus dos archivos.
- 2026-10-21 · versión 1.0.0 · Qué pasa: si edita un campo que contiene una fórmula (MathJax) y
  guarda, en su sitio queda el código de la fórmula (por ejemplo, «\(x^2\)») en lugar de la fórmula
  dibujada, hasta que pasa a la otra cara o a otra tarjeta. Lo guardado es correcto; solo falla lo
  que se ve. Por qué: el complemento redibuja ese trozo con el texto que le da Anki, pero no pide que
  se vuelvan a dibujar sus fórmulas. Propuesta: tras redibujar el trozo, pedir que se dibujen de
  nuevo las fórmulas que contiene.
- 2026-10-21 · versión 1.0.0 · Qué pasa: en las tarjetas de huecos cuya plantilla pone el texto con
  huecos y otro campo (por ejemplo, «Reverso extra») dentro de un mismo bloque, sin un bloque propio
  para cada uno, el complemento toma el bloque entero por el campo de huecos: el otro campo no se
  puede editar y, mientras edita el de huecos, desaparece de la vista hasta que guarda o cancela. No
  se pierde nada. La plantilla de huecos que trae Anki no tiene este problema. Propuesta: limitar el
  campo de huecos a su propio texto también en ese caso.
- 2026-10-21 · versión 1.0.0 · Qué pasa: el recuadro azul de edición usa dos azules fijos propios:
  de día, el de la bandera azul de Anki, y de noche, uno que no está en la paleta Nocturne. No es el
  azul de foco de Anki, así que no casa con el resto de la interfaz. Además, el comprobador del
  taller no deja empaquetar una versión nueva con colores fijos. Propuesta: usar el azul de foco de
  la paleta, con su pareja de modo noche.

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
