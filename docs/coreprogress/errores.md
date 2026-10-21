# Errores de «CoreProgress»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las dos primeras se hicieron antes de que el complemento llegara a este taller; la versión
exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 1.0.0 · Qué pasa: deshacer algo que no es una respuesta le quita una respuesta
  a la racha. Por ejemplo: lleva 4 «Bien» seguidas, en la quinta tarjeta la entierra y pulsa Editar >
  Deshacer; la racha baja a 3 aunque no ha deshecho ninguna respuesta. Si esas 4 acababan de batir el
  récord (era 3 y se guardó 4), el récord guardado vuelve a 3 y, si sale del repaso sin volver a
  llegar a 4, se pierde. Pasa igual al deshacer suspender, olvidar o cambiar la fecha de una tarjeta
  durante el repaso. Por qué: al deshacer, el complemento descuenta una respuesta siempre que lo
  deshecho toque la cola de estudio, y esas acciones también la tocan. Propuesta: descontar solo
  cuando lo deshecho sea una respuesta (Anki dice el nombre de la acción deshecha).
- 2026-10-21 · versión 1.0.0 · Qué pasa: con un récord de 1 (por ejemplo, en el primer repaso, una
  «Bien» y después «Otra vez»), la ventana de opciones dice «Tu récord actual: 1 seguidas!». Pasa
  también en otros idiomas que distinguen singular y plural, como el catalán («1 seguides!»). Por
  qué: la frase tiene el plural fijo. Propuesta: que la frase tenga su forma en singular y en plural y
  se elija por la cifra.
- 2026-10-21 · versión 1.0.0 · Qué pasa: con el «Espacio superior» en 0, que es el valor por defecto,
  la barra no aparta la tarjeta: se dibuja encima. Con la plantilla estándar de Anki la tarjeta
  empieza a 20 píxeles del borde de arriba y la barra ocupa de 10 a 26 (los hitos, de 7 a 29), así que
  roza la parte alta de la primera línea; y el aviso de racha, que va debajo de la barra (de unos 33 a
  49 píxeles), queda encima de esa primera línea mientras se ve. Al bajar por una tarjeta larga, la
  barra sigue fija y tapa lo que pasa por debajo. Por qué: la barra flota sobre la página y el hueco
  para ella depende solo de esa opción. Propuesta: que la tarjeta deje sitio a la barra y a su aviso
  por sí sola, y que «Espacio superior» sea un extra. Hay que confirmarlo a la vista dentro de Anki.
- 2026-10-21 · versión 1.0.0 · Qué pasa: al pulsar «Restablecer», la pregunta «¿Poner tu récord a
  cero?» trae «Sí» marcado de antemano, así que un Intro de más borra el récord; no se puede deshacer,
  y pulsar Cancelar después en la ventana de opciones no lo devuelve. Por qué: la regla del taller
  pide que lo que borra sin vuelta atrás traiga «No» marcado de antemano; aquí no se hizo así, y el
  borrado se aplica antes de Guardar. Propuesta: «No» marcado de antemano y borrar el récord solo al
  pulsar Guardar.
- 2026-10-21 · versión 1.0.0 · Qué pasa: todos los colores de la barra son propios, fuera de la paleta
  Nocturne: las siete escalas de los temas y la dorada (160 colores), y el blanco puro del número de
  los hitos alcanzados y de las chispas, más las sombras y los grises del canal provisional. El
  comprobador del taller los rechaza (162 avisos de color fijo), así que no se podrá entregar una
  versión nueva hasta decidirlo. Por qué: el complemento llegó hecho antes de las reglas del taller.
  Propuesta: como en GritMap, que usted apruebe las escalas propias de los temas, que son la razón de
  ser de la opción «Tema de color», y que se marquen como aprobadas; el blanco puro y los grises pasan
  a tonos de la paleta.
- 2026-10-21 · versión 1.0.0 · Qué pasa: la barra se mueve más de lo que permite la guía del taller.
  Un destello cruza el relleno cada 9 segundos mientras repasa, sin parar; el relleno se desliza en
  cuatro décimas de segundo; los colores se funden en casi medio segundo; los hitos dan un salto y
  los avisos avivan el relleno durante seis décimas de segundo, con chispas. La guía pide no
  animar salvo que usted lo pida, y entonces solo con fundidos o desplazamientos de 150 milésimas como
  máximo. Además, el destello y el salto de los hitos no se apagan con la casilla de efectos, y el
  salto tampoco con la opción del sistema de reducir las animaciones. Por qué: el complemento llegó
  hecho antes de la guía. Propuesta: que usted diga qué movimientos quiere conservar; esos pasan a
  «Así a propósito» y los demás se quitan o se acortan, y que la casilla de efectos los apague todos.
- 2026-10-21 · versión 1.0.0 · Qué pasa: el complemento lee y escribe la colección en el hilo
  principal, que es la parte de Anki que dibuja la pantalla y atiende sus clics: pide la cuenta de
  tarjetas pendientes en cada respuesta, lee los mazos al entrar a repasar y guarda el récord al
  batirlo. En la práctica no se nota, porque es la misma cuenta que Anki hace para dibujar los
  contadores de abajo, pero va contra la regla del taller de tocar la colección siempre fuera de ese
  hilo, que evita tirones con colecciones grandes. Por qué: el complemento llegó hecho antes de las
  reglas del taller. Propuesta: guardar el récord fuera del hilo principal y, si usted lo aprueba,
  dejar la cuenta como está y anotarla en «Así a propósito».

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-07-23 · versión anterior a su llegada al taller · Qué pasaba: al empezar el repaso,
  o al responder la primera tarjeta, la barra daba un tirón o se quedaba atascada un momento. Por qué:
  al crecer el relleno, toda la página del repaso se recolocaba en cada fotograma, compitiendo con las
  fórmulas de la tarjeta y con la medida del fondo; además, al empezar se volvía a cargar todo el
  código de la barra aunque ya estaba en la página, y seis relojes de reintento medían el fondo una y
  otra vez. Regla: lo que cambia de tamaño en la barra queda aislado del resto de la página; no se
  vuelve a cargar lo que ya está en la página; y el fondo se vuelve a medir cuando Anki cambia la
  tarjeta, con solo unos pocos relojes como red de seguridad.
- FIX-002 · 2026-07-27 · versión anterior a su llegada al taller · Qué pasaba: con dos perfiles en el
  mismo Anki, el récord de uno aparecía en el otro; y al cambiar de perfil desde el repaso podía
  perderse el récord del repaso en marcha o intentar guardarse con la colección ya cerrada. Por qué:
  el récord se guardaba en la configuración del complemento, que es una sola para todo el ordenador, y
  solo al salir del repaso. Regla: lo que pertenece a un perfil se guarda en su colección, comprobando
  antes que esté abierta, y se guarda también al cerrar el perfil, antes de que Anki cierre la
  colección.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- «Difícil» rompe la racha: solo «Bien» y «Fácil» cuentan como acierto. Decisión del autor original;
  no consta el motivo. Si prefiere que «Difícil» no la rompa, es un cambio pequeño.
- Cada vez que entra a repasar, la barra empieza vacía y toma lo que queda como nuevo total, aunque
  vuelva al mismo mazo. Decisión del autor original.
- El récord se celebra una sola vez por repaso, en el momento exacto de batirlo; si coincide con un
  número de racha, gana el aviso de récord. Decisión del autor original.
- El récord se celebra desde 3 seguidas; antes era desde 5. Lo bajó el usuario del complemento, según
  consta en el código (sin fecha).
- El aviso de récord es «¡Récord! N», el texto original, sin añadidos. En las opciones, la línea del
  récord termina en «!» sin el signo de apertura («7 seguidas!») y, sin récord, muestra un guion corto
  («-»). Lo pidió el usuario, según consta en el código (sin fecha).
- El récord se guarda en el momento de batirlo, para no perderlo si Anki se cierra de golpe, y baja
  si se deshacen esas respuestas. Decisión del autor original.
- El récord no entra en Editar > Deshacer: es un ajuste y no estudio, y así no tapa el «deshacer
  respuesta». Decisión del autor original.
- Rehacer no devuelve la respuesta a la racha, porque Anki no avisa a los complementos cuando se
  rehace; la racha queda a la baja. Decisión del autor original.
- Los mazos excluidos solo afectan al récord (por eso la opción se llama «Excluir mazos (récord)»):
  en ellos siguen la barra, los avisos de racha y la barra dorada. Decisión del autor original.
- La ventana de excluir mazos no lleva ningún texto de ayuda, en ningún idioma. Lo retiró el usuario,
  según consta en el código.
- El título de la ventana de opciones es solo el nombre, «CoreProgress», sin traducir. Lo pidió el
  usuario, según consta en el código.
- Los botones estándar de las ventanas (Guardar, Cancelar, Aceptar, restaurar) llevan el texto de Qt
  en el idioma de Anki, no traducciones propias. Decisión del autor original.
- El canal de la barra toma su color del fondo real de la tarjeta y no del tema de Anki, para no
  chocar con plantillas que tienen fondo propio. Decisión del autor original.
- El halo dorado y los tonos del relleno se suavizaron a petición del usuario: el halo debe adornar,
  no llamar la atención, y el final del degradado no debe quedar casi negro. Según consta en el
  código (sin fecha).
