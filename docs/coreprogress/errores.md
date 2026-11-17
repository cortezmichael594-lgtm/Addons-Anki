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

- 1.6.0 · Petición de la persona el 2026-11-17, con capturas: el ancho de la barra se elige
  («Tarjeta», de serie, o «Ventana», como hasta la 1.4.0), y al bajar por una tarjeta larga el
  contenido ya no se ve a través de la barra: detrás de ella va una franja opaca del color del fondo.
  La barra sigue fija arriba (no se va al bajar). Con la fila nueva, la ventana de opciones crece unos
  60 px: en una pantalla de 1.366 × 768 puede necesitar desplazarse un poco.

- 1.5.0 · Informe «Rediseño de color y forma: CoreProgress 1.4.0», aplicado entero a petición del
  cliente el 2026-11-17, con la opción recomendada en sus tres decisiones:
  - Decisión 1: barra de 720 px como mucho, centrada sobre la tarjeta (antes, de lado a lado).
  - Decisión 2: hitos como cortes finos; número solo en el próximo hito y en el total. Sustituye a los
    discos numerados de la 1.3.0.
  - Decisión 3: estrella en la punta de la racha dorada, sin halo (el halo lo había dejado el cliente).
  - Además, sin decisión: paleta nueva de los seis temas y del oro, calculada por contraste (sustituye
    a las escalas hechas a mano, que estaban aprobadas); sin el contorno de 1 px de la 1.3.0 salvo en
    el oro de día; canal gris plano, sin sombra; aviso en una píldora tintada; movimiento de 0,3 s con
    frenada, sin avivar el relleno; grosor en tres tamaños; muestras de tema como minibarras; colores
    del sistema para cada pieza en el contraste alto de Windows.
- 1.5.0 · El canal usa el gris que midió el informe (#D5D9E2 de día y #272F3F de noche), que el informe
  llama SCROLLBAR_BG porque lo tomó de la tabla del texto común de las fichas. Esa tabla estaba
  atrasada: Atelier 3.9.0 (2026-11-11) oscureció SCROLLBAR_BG a #828893 y #6C7587 para que el tirador
  de las barras de desplazamiento llegue a 3 a 1. Con ese gris el canal quedaría a 3,5 a 1 del fondo y
  toda la paleta medida dejaría de valer, así que se queda el valor del informe, marcado en el código,
  y la tabla del texto común se ha puesto al día.
- 1.5.0 · El grosor elegido va como los controles segmentados del panel modelo de GritMap (fondo de la
  capa elevada, borde azul y seminegrita) y no relleno de azul con texto blanco, como proponía el
  informe (2.6): la ventana de opciones sigue el panel modelo, que es regla del taller, y así se ve
  igual que en GritMap. El contraste del elegido no depende del relleno.
- 1.5.0 · La muestra de tema es una minibarra de 30 × 10 px (informe, 2.6) y no el cuadrito de 16 × 16
  del panel modelo: enseña el degradado que se va a ver. Lo aprobó el cliente con el informe.
- 1.5.0 · Movimiento (informe, 3.1 y 8.7): el relleno avanza en 0,3 s, el color cambia en 0,4 s, el hito
  alcanzado dura 0,6 s y las chispas 0,5 s. Son más largos que los 150 ms de la guía: excepción
  aprobada por el cliente con el informe, como las de la 1.2.0. Con «reducir el movimiento», nada se
  anima.
- 1.5.0 · Decisiones de diseño del taller al aplicar el informe: el número del hito alcanzado va en
  CANVAS_ELEVATED (#FBFCFE) y no en blanco puro, que el taller no usa; la actualización tras cada
  respuesta pasa de 120 a 50 ms, para que la barra responda antes; al entrar a repasar o al cambiar las
  opciones la barra se dibuja en su sitio, sin deslizarse; lo que se inyecta en el repaso pasa a llevar
  el prefijo del paquete («coreprogress»), como pide la regla del taller (antes, «_cprog»), y la
  variable de plantilla antigua --cprog-track se sigue entendiendo.
- 1.3.0 · Informe «Auditoría y rediseño de la interfaz: CoreProgress 1.2.0», aplicado entero a petición
  del cliente el 2026-11-16, con la opción recomendada en sus cuatro decisiones:
  - Decisión 1 (B): se celebra la mejor racha de los últimos 30 días («MEJOR RACHA EN 30 DÍAS: 42»),
    además del récord histórico, que queda como dato y se sigue celebrando si se bate. Se guarda la
    mejor racha de cada día de los últimos 30 en la colección. «Poner a cero» solo pone a cero el
    récord histórico.
  - Decisión 2 (B): hitos en números redondos (paso de 5, 10, 20, 25, 50… con cinco marcas como mucho
    y ninguna más allá del 92 %) y una marca final con el total. Sustituye a los hitos al 20, 40, 60 y
    80 %, que el informe 1.1 había dado por buenos.
  - Decisión 3 (A): relleno plano, sin brillo de cristal ni sombra de color, con un contorno de 1 px en
    la tinta del tema; el halo dorado queda como única luz. (Desde la 1.5.0, sin contorno salvo en el
    oro de día y sin halo.)
  - Decisión 4 (A): sin la cabecera «CoreProgress» dentro de la ventana de opciones.
  - Una sola celebración por respuesta (récord, 30 días, racha; el hito solo cambia de color si
    coincide); aviso centrado en la ventana; con «reducir el movimiento», nada se anima.
- 1.3.0 · Decisiones de diseño del taller al aplicar el informe: los enlaces («Restaurar…», «Poner a
  cero», «Deshacer») van subrayados además de en FG_LINK, como manda la regla de enlaces del taller
  (el informe los pedía sin subrayar en reposo); el borde de la ficha elegida es BORDER_FOCUS, como
  pide el informe, y con el foco del teclado pasa a 4 px; los colores de la vista previa (canal y
  número del hito sin alcanzar) son los de Nocturne con su marca, porque en la ventana de opciones no
  hay una tarjeta que medir. (Desde la 1.5.0 llegan de palettes.py, los mismos que en el repaso.)
- 1.3.0 · No aplicado y por qué: Intro sin Ctrl no acepta la ventana (el informe lo deja «por
  comprobar» y sigue pendiente también en Atelier); la lista de mazos, si los nombres no caben, no
  lleva globo con la lista entera; las chispas siguen siendo blancas también de día (el informe pide
  comprobarlo antes con una captura). (Desde la 1.5.0, las chispas van en la tinta del tema.)

- Desde la 1.2.0, «Difícil» mantiene la racha: es un acierto, como dice el manual de Anki. Solo «Otra
  vez» la rompe. Lo aprobó el cliente el 2026-11-09 (informe de CoreProgress, apartado 2.1), sabiendo
  que el autor original lo había decidido al revés. Antes: «Difícil» rompía la racha. Decisión del autor original;
  no consta el motivo. Si prefiere que «Difícil» no la rompa, es un cambio pequeño.
- Desde la 1.2.0 el 100 % es todo lo de hoy en ese mazo, y al volver la barra sigue donde la dejó
  (informe del 2026-11-09, apartado 3.1). Antes: cada vez que entraba a repasar, la barra empezaba vacía y tomaba lo que queda como nuevo total, aunque
  vuelva al mismo mazo. Decisión del autor original.
- El récord se celebra una sola vez por repaso, en el momento exacto de batirlo; si coincide con un
  número de racha, gana el aviso de récord. Decisión del autor original; desde la 1.3.0, lo mismo con la
  mejor racha de 30 días, que va detrás del récord y delante de la racha.
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
  usuario, según consta en el código. Desde la 1.3.0 va solo en la barra de la ventana (decisión 4 del
  informe del 2026-11-16).
- Los botones estándar de las ventanas (Guardar, Cancelar, Aceptar, restaurar) llevan el texto de Qt
  en el idioma de Anki, no traducciones propias. Decisión del autor original.
- El canal de la barra se ajusta al fondo real de la tarjeta y no al tema de Anki, para no chocar con
  plantillas que tienen fondo propio. Decisión del autor original; desde la 1.5.0, sobre el fondo de
  Atelier es el gris de la paleta y sobre otro, un gris con el mismo contraste.
- Los temas de la barra tienen colores propios, fuera de la paleta Nocturne, igual que los de GritMap:
  son la razón de ser de la opción «Tema de color». Desde la 1.5.0 son los del informe del 2026-11-17,
  calculados para que pesen igual; en el código van marcados como aprobados. Rojo fuego se retira
  desde la 1.2.0 (en Anki el rojo es error) y quien lo tenía pasa a Naranja atardecer, con aviso.
- Movimiento desde la 1.2.0 (informe del 2026-11-09; desde la 1.5.0, véase arriba): se quitó el
  destello que cruzaba la barra cada 9 segundos. Se conservan, porque informan del avance o de un logro: el relleno que avanza en 0,4 s,
  el fundido de color al pasar a dorado, el salto y las chispas de los hitos y el avivado de los
  avisos. Salvo el avance y el cambio de color, todo se apaga con «Celebrar rachas y récords». Son más
  largos que los 150 ms de la guía: excepción aprobada por el cliente con el informe.
- Los avisos de racha salen a las 5, 10, 20, 30… seguidas y duran 1,5 segundos (informe del
  2026-11-09, apartados 2.2 y 4.3). El primer récord sigue avisándose desde 3.
- La barra no retrocede cuando la cuenta de Anki sube (vencen tarjetas en aprendizaje): se queda quieta
  hasta que el avance la alcance. Solo retrocede al deshacer (informe del 2026-11-09, apartado 3.2).
- Desde la 1.4.0 no hay nada en la pantalla de «Enhorabuena»: la barra llena y la línea de resumen
  que puso la 1.2.0 (informe del 2026-11-09, apartado 8.1) se quitaron del todo a petición de la
  persona el 2026-11-17. La celebración al terminar es de ProFeedback.
