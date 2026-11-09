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
- FIX-003 · 2026-11-09 · versión 1.1.0 · Qué pasaba: al pulsar «Restablecer», la pregunta «¿Poner tu
  récord a cero?» traía «Sí» marcado de antemano, así que un Intro de más borraba el récord, y el
  borrado se aplicaba en el acto aunque después pulsara Cancelar. Por qué: se usaba la pregunta de
  Anki sin «No» por defecto y se borraba antes de guardar. Regla: lo que borra sin vuelta atrás
  pregunta con el foco en «No» y solo se aplica al pulsar Aceptar; Cancelar lo deja como estaba.
- FIX-004 · 2026-11-09 · versión 1.2.0 · Qué pasaba: con el «Espacio superior» en 0, el valor de
  serie, la barra se dibujaba encima de la parte alta de la tarjeta, donde suele estar la pregunta.
  Por qué: el hueco para la barra dependía solo de esa opción. Regla: la tarjeta deja siempre sitio a
  la barra y a su aviso por sí sola (10 px de margen, el alto de la barra, 24 px para el aviso si las
  celebraciones están activadas y 8 px de aire: 58 px con la barra de serie; el informe proponía 34,
  pero así el aviso de racha también tapaba la primera línea); la opción pasa a ser «Espacio extra», que se suma. Quien había subido el espacio a mano
  conserva el mismo hueco.
- Sin nota en el código · 2026-11-09 · versión 1.2.0 · Qué pasaba: con un récord de 1, la ventana de
  opciones decía «Tu récord actual: 1 seguidas!». Se resolvió al cambiar el texto: ahora cada idioma
  tiene sus formas de plural («Récord: 1 acierto seguido»).

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- Desde la 1.2.0, «Difícil» mantiene la racha: es un acierto, como dice el manual de Anki. Solo «Otra
  vez» la rompe. Lo aprobó el cliente el 2026-11-09 (informe de CoreProgress, apartado 2.1), sabiendo
  que el autor original lo había decidido al revés. Antes: «Difícil» rompía la racha. Decisión del autor original;
  no consta el motivo. Si prefiere que «Difícil» no la rompa, es un cambio pequeño.
- Desde la 1.2.0 el 100 % es todo lo de hoy en ese mazo, y al volver la barra sigue donde la dejó
  (informe del 2026-11-09, apartado 3.1). Antes: cada vez que entraba a repasar, la barra empezaba vacía y tomaba lo que queda como nuevo total, aunque
  vuelva al mismo mazo. Decisión del autor original.
- El récord se celebra una sola vez por repaso, en el momento exacto de batirlo; si coincide con un
  número de racha, gana el aviso de récord. Decisión del autor original.
- El récord se celebra desde 3 seguidas; antes era desde 5. Lo bajó el usuario del complemento, según
  consta en el código (sin fecha).
- Desde la 1.2.0 los textos son «Nuevo récord: 11», «5 aciertos seguidos» y «Récord: 7 aciertos
  seguidos» o «Sin récord todavía», sin tuteo; lo aprobó el cliente el 2026-11-09 sabiendo que había
  pedido los anteriores. Antes: el aviso de récord era «¡Récord! N», el texto original, sin añadidos. En las opciones, la línea del
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
- Desde la 1.2.0 la lista se llama «Mazos que no cuentan para el récord» y lleva la línea «Útil para
  mazos muy fáciles.»; lo aprobó el cliente el 2026-11-09 sabiendo que antes la retiró. Antes: la ventana de excluir mazos no llevaba ningún texto de ayuda, en ningún idioma. Lo retiró el usuario,
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
- Los temas de la barra tienen escalas de color propias, fuera de la paleta Nocturne, igual que los de
  GritMap: son la razón de ser de la opción «Tema de color». Lo aprobó el cliente con el informe del
  2026-11-09, que conserva los temas; en el código van marcadas como aprobadas. Rojo fuego se retira
  desde la 1.2.0 (en Anki el rojo es error) y quien lo tenía pasa a Naranja atardecer, con aviso.
- Movimiento desde la 1.2.0 (informe del 2026-11-09): se quitó el destello que cruzaba la barra cada
  9 segundos. Se conservan, porque informan del avance o de un logro: el relleno que avanza en 0,4 s,
  el fundido de color al pasar a dorado, el salto y las chispas de los hitos y el avivado de los
  avisos. Salvo el avance y el cambio de color, todo se apaga con «Celebrar rachas y récords». Son más
  largos que los 150 ms de la guía: excepción aprobada por el cliente con el informe.
- Los avisos de racha salen a las 5, 10, 20, 30… seguidas y duran 1,5 segundos (informe del
  2026-11-09, apartados 2.2 y 4.3). El primer récord sigue avisándose desde 3.
- La barra no retrocede cuando la cuenta de Anki sube (vencen tarjetas en aprendizaje): se queda quieta
  hasta que el avance la alcance. Solo retrocede al deshacer (informe del 2026-11-09, apartado 3.2).
- En la pantalla de «Enhorabuena», la barra llena va sin animación, con una sola línea de datos: la
  celebración ya la pone ProFeedback (informe del 2026-11-09, apartado 8.1).
