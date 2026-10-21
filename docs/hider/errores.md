# Errores de «Hider»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las cuatro primeras se hicieron antes de que el complemento llegara a este taller (versión
4.0.3); la versión exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 4.0.3 · Qué pasa: cuando algo falla, el aviso dice «Hider ha encontrado un
  problema y ha desactivado esa parte por seguridad. Revisa la configuración del complemento.», pero
  no desactiva nada: esa parte sigue funcionando y, si vuelve a fallar, el aviso sale otra vez
  pasado un minuto. Revisar la configuración tampoco lo arregla, porque las opciones con un valor que
  no sirve ya se corrigen solas. Propuesta: cambiar el texto, en sus 42 idiomas, por uno que diga lo
  que pasa de verdad, por ejemplo «Hider ha tenido un problema. Anki sigue funcionando; el detalle
  queda en el registro del complemento.».
- 2026-10-21 · versión 4.0.3 · Qué pasa: con «Empezar el repaso automáticamente al abrir un mazo»
  activada, al pulsar un mazo Hider pregunta a la colección si hay tarjetas que repasar sin dejar
  libre a Anki mientras tanto, y lo hace dos veces (antes de dibujar la pantalla del mazo y justo
  antes de saltar al repaso). Mientras dura cada consulta, Anki no responde. Es la misma consulta
  que hace Anki al empezar el repaso, también sin dejarse libre, y en una colección normal no se
  nota; pero choca con la regla del taller de no consultar la colección sin dejar libre a Anki y,
  en una colección muy grande, podría notarse como un parón breve al pulsar el mazo. No se ha
  medido. Propuesta: que usted pruebe a abrir su mazo más grande; si no nota ningún parón, pasarlo a
  «Así a propósito». Si lo nota, hacer la consulta en segundo plano, a cambio de que la pantalla del
  mazo salga vacía un instante también cuando no haya tarjetas pendientes.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-27 · versión 4.0.3 o anterior · Qué pasaba: al abrir un mazo con el salto
  automático puesto, la pantalla del mazo (nombre, recuentos y botón) se veía cerca de un segundo
  antes de la primera tarjeta. Por qué: el salto se decidía después de que Anki dibujara esa
  pantalla, y daba tiempo a verla entera, con sus barras. Regla: lo que no deba verse se decide
  antes de que Anki dibuje la pantalla nueva; lo que ocurre después de dibujarla solo sirve para
  reaccionar a lo que ya está a la vista. Por eso la pantalla del mazo sale ahora vacía un instante.
- FIX-002 · 2026-07-27 · versión 4.0.3 o anterior · Qué pasaba: al salir del repaso, la ventana daba
  varios tirones seguidos mientras volvía cada barra. Por qué: la barra de menú volvía al instante y
  la superior solo cuando Anki terminaba de medirla. Regla: cuando vuelven varias barras a la vez,
  vuelven en el mismo momento y con la altura que ya tenían; la medición de Anki solo sirve para
  corregir después, nunca para decidir cuándo reaparece algo. La parte de esta corrección que tocaba
  la barra inferior la sustituyó FIX-003.
- FIX-003 · 2026-07-27 · versión 4.0.3 o anterior · Qué pasaba: al salir del mazo, la barra de abajo
  aparecía con los botones del repaso y se quedaba a la vista un buen rato. Por qué: se le quitaba
  el plegado al salir, y la página del repaso sigue cargada en esa barra hasta que llega la pantalla
  siguiente. Regla: a la barra inferior no se la toca al salir del repaso; es la única cuyo
  contenido cambia de pantalla a pantalla, y Anki ya la abre sola, de una vez y con el contenido
  correcto, al dibujar la pantalla nueva.
- FIX-004 · 2026-07-27 · versión 4.0.3 o anterior · Qué pasaba: al salir del mazo, las barras volvían
  encima de la tarjeta y la pantalla nueva llegaba después, con un salto visible. Por qué: se
  devolvían en cuanto se cambiaba de pantalla, cuando Anki aún tenía que preparar los datos de la
  siguiente. Regla: cambiar de pantalla no es tener la pantalla nueva lista; lo que deba coincidir
  con ella se hace cuando Anki pide su contenido, con un plazo de seguridad (cuatro décimas de
  segundo) por si ese aviso no llegara, porque quedarse sin barras sería peor que un salto.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- Las teclas 2 y 4 no responden la tarjeta cuando están ocultos «Difícil» y «Fácil», y avisan de que
  el botón está oculto: así no se responde sin querer con un botón que no se ve. Decisión del autor
  original.
- En pantalla completa, durante el repaso, la barra de menú no aparece al llevar el ratón arriba,
  aunque Anki la enseñaría. Decisión del autor original.
- Si es usted quien sale del repaso a la pantalla del mazo, Hider no le vuelve a meter en él; sí
  vuelve a saltar al abrir un mazo desde la lista de mazos. Decisión del autor original.
- Con el salto automático, la pantalla del mazo sale vacía un instante y Hider espera algo más de
  una décima de segundo a que Anki deje de redibujarla antes de saltar; si saltara antes, el segundo
  redibujado de Anki caería encima del repaso. Decisión del autor original (véase FIX-001).
- Al salir del repaso, las barras no vuelven en el acto, sino cuando la pantalla siguiente está
  lista (hasta cuatro décimas de segundo). Decisión del autor original (véase FIX-004).
- Si Anki redibuja tarde la pantalla del mazo encima del repaso, Hider vuelve a abrir el repaso y la
  tarjeta de ese momento se muestra otra vez desde la pregunta. Es la forma de que el repaso no
  quede tapado. Decisión del autor original.
- La barra de desplazamiento oculta es solo de aspecto: la rueda del ratón sigue desplazando la
  tarjeta. Decisión del autor original.
- Los avisos de fallo salen como mucho una vez por minuto por cada sitio, aunque el fallo se repita
  en cada tarjeta o en cada movimiento del ratón; el detalle se anota siempre en el registro.
  Decisión del autor original.
- Las opciones son comunes a todos los perfiles de este ordenador. Decisión del autor original.
- Con el planificador antiguo de Anki no hay salto automático, porque Anki tampoco deja repasar con
  él. Decisión del autor original.
