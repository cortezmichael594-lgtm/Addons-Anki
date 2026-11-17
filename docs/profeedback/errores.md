# Errores de «ProFeedback»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las tres primeras se hicieron antes de que el complemento llegara a este taller (versión
2.0.0); la versión exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 2.0.0 · Qué pasa: choca con una regla del taller. Para elegir la insignia, al
  mostrar cada tarjeta el complemento lee su historial de respuestas mientras Anki espera, en lugar
  de hacerlo en segundo plano. Es una lectura pequeña (las respuestas de una sola tarjeta, una vez
  por tarjeta), del mismo tipo que la que hace Anki en ese momento para dibujarla; no se ha medido
  dentro de Anki si se nota al pasar de tarjeta. Propuesta: que usted pruebe a repasar con las
  insignias activadas y desactivadas; si no nota diferencia, pasarlo a «Así a propósito» con su
  permiso, porque leerlo en segundo plano obligaría a poner la insignia un instante después de la
  tarjeta, y eso sería un parpadeo.

## Corregidos

Cada corrección: número, fecha, versión, qué pasaba, por qué pasaba y la regla que evita que vuelva.

- FIX-001 · 2026-10-13 · versión 2.0.0 o anterior · Qué pasaba: al guardar las opciones, un sonido
  en «al azar» se convertía en el primer sonido de la lista y ya no volvía a ser al azar. Por qué:
  el desplegable no tenía ninguna entrada para «al azar» y, al no encontrarla, mostraba el primer
  archivo, que era el que se guardaba. Regla: todo desplegable de sonido lleva como primera entrada
  «Aleatorio», y un sonido guardado que ya no existe se muestra como esa entrada. Desde la 2.5.0,
  con el visto bueno de la persona (informe 2.4.0, aplicado entero), la lista empieza por «Sin
  sonido», «Aleatorio» va después de los sonidos y un sonido guardado que ya no existe se muestra
  como el primero de la lista; lo que la regla protege sigue igual: «Aleatorio» siempre se puede
  elegir y se guarda tal cual.
- FIX-002 · 2026-10-13 · versión 2.0.0 o anterior · Qué pasaba: tras repasar un rato y salir a la
  lista de mazos sin terminar, al abrir más tarde un mazo ya terminado saltaban el sonido y el
  confeti. Por qué: la señal de «acabo de repasar» no se apagaba al salir del repaso por otro
  camino. Regla: solo la vuelta del repaso a la pantalla del mazo puede celebrar; salir por
  cualquier otra pantalla descarta la sesión.
- FIX-003 · 2026-10-13 · versión 2.0.0 o anterior · Qué pasaba: el «día perfecto» empezaba a
  medianoche en lugar de a la hora de cambio de día de Anki, mezclaba los perfiles, se perdía si
  Anki se cerraba de golpe y no contaba lo repasado en otros dispositivos. Por qué: el complemento
  llevaba su propia cuenta del día en sus opciones, comunes a todos los perfiles, en lugar de
  preguntar al historial de Anki. Regla: lo que ya está en el historial de la colección se lee de
  ahí, que respeta el cambio de día de Anki, es de cada perfil y viaja con la sincronización.
- FIX-004 · 2026-11-09 · versión 2.1.0 · Qué pasaba: la nota de la ventana de opciones decía que los
  sonidos propios se copiaban en «user_files/sonidos», pero el complemento solo los busca en una
  subcarpeta por tipo de sonido, que además no venían creadas; un .mp3 copiado como decía la nota no
  aparecía en ningún desplegable. Por qué: la nota no nombraba las subcarpetas. Regla: las
  subcarpetas («correcto», «finalizado/mazo», «finalizado/todo», «perfecto-mazo» y «perfecto-todo»)
  se crean vacías al abrir los ajustes, y la nota dice que cada sonido va en la suya. Desde la
  2.5.0 la nota se sustituye por «Abrir la carpeta de estos sonidos…» en cada lista (informe 2.4.0).
- FIX-005 · 2026-11-13 · versión 2.2.0 · Qué pasaba: al abrir la configuración se veía un destello:
  la ventana salía primero vacía, con su fondo, y después aparecía el panel y la ventana cambiaba de
  alto. Por qué: la ventana se enseñaba en seguida y solo la página esperaba, oculta, a estar
  dibujada. Regla: la ventana entera es invisible hasta que el panel avisa de que está listo y ya
  tiene su alto; entonces aparece de una vez.
- FIX-006 · 2026-11-13 · versión 2.3.0 · Qué pasaba: con Atelier (Nocturne) instalado, los botones
  de respuesta y «Mostrar respuesta» salían con esquinas pequeñas, borde y una raya abajo, y al
  pasar el ratón por encima se volvían oscuros. Por qué: Atelier pinta esos mismos botones con
  reglas más fuertes que las del complemento, y ganaban. Regla: con «Botones de respuesta 3D de
  colores» marcado, la forma y el color de los botones son siempre los del complemento, y al pasar
  el ratón solo se aclaran.
- FIX-007 · 2026-11-17 · versión 2.5.0 (el fallo venía de la 2.0.0) · Qué pasaba: si «Insignias sobre
  la tarjeta» estaba desmarcada al entrar a repasar y se marcaba en ese momento, las tarjetas
  siguientes mostraban la insignia sin su aspecto (icono grande y texto sueltos) hasta salir del
  repaso y volver. Por qué: el estilo de la insignia solo se cargaba en la página del repaso si la
  opción estaba marcada al cargarla. Regla: el estilo de la insignia se carga siempre en el repaso
  (es pequeño y no se ve si no hay insignia); la opción solo decide si se pone la insignia. Estaba en
  «Pendientes» desde el 2026-10-21, con esta misma propuesta.

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- 2.6.0 · Informe «Rediseño de color y forma: ProFeedback 2.5.0», aplicado entero a petición de la
  persona el 2026-11-17, con la opción recomendada en sus tres decisiones:
  - Decisión 1 (A): «Mostrar respuesta» en el azul de acción de Atelier; el oro queda solo para
    celebrar haber terminado.
  - Decisión 2: paleta propia de los cuatro botones (coral, ámbar, jade, cielo), calculada por
    contraste y con versión de noche. Sustituye a los colores del original que la persona fijó el
    2026-11-13 («lo quiero igual al original»), que eran los de Duolingo.
  - Decisión 3: esquinas de 12 px y canto de 3 (48 px de alto).
  - Además, sin decisión: insignias con colores e iconos nuevos, confeti diseñado entero, título en el
    oro de CoreProgress con un brillo de 1,2 s, ratón encima que aleja la cara de su letra, raya de
    1 px, tiempos previstos en gris de 12 px, sin el alias «Feather Bold.ttf», tres destellos fijos con
    «reducir movimiento», colores del sistema en el contraste alto y «Ver» junto a «Confeti al
    terminar».
- 2.6.0 · Decisiones del taller al aplicarlo: todos los colores salen de un solo sitio (look.py) y
  llegan a la página como variables incrustadas antes del primer pintado, y al confeti en JSON, para
  que las pruebas comprueben cada contraste; la letra de «Mostrar respuesta» y el dibujo de los iconos
  de día son el blanco de HIGHLIGHT_FG de Nocturne (el que Anki pone sobre el azul de acción), no otro;
  «Ver» enseña el confeti de mazo, que es el más frecuente; los movimientos del confeti (2,4 y 3,8 s) y
  del brillo (1,2 s) superan los 150 ms de la guía: excepción aprobada con el informe, como en la
  2.5.0. Con la tritanopía (la forma más rara de daltonismo), «Bien» y «Fácil» se acercan (de 14,5 a
  7,1 de diferencia): lo acepta el informe, porque llevan palabra.

- 2.5.0 · Informe «ProFeedback 2.4.0: auditoría y rediseño de la interfaz», aplicado entero a
  petición de la persona el 2026-11-16, con la opción recomendada en sus cuatro decisiones:
  - «Difícil» es un acierto (manual de Anki): suena como «Bien». Solo «Otra vez» suena distinto, más
    bajo y sin tono de castigo. Sustituye a la decisión del autor original («Difícil» como fallo).
  - Opción B: la celebración dorada premia terminar el día, no la nota; la de mazo nunca es dorada.
    Ya no hay sonidos «perfecto» aparte: son variantes más de los dos finales. La celebración del
    día sale una vez al día; si vuelven tarjetas, se celebra como un mazo. Una respuesta deshecha
    deja de contar (resuelve el pendiente del 2026-10-21).
  - «Bien» mide 190 px, como «Mostrar respuesta», para que el puntero quede dentro de él. Es la
    propuesta de la que el propio informe estaba menos seguro.
  - «SE RESISTE» y «OTRA OPORTUNIDAD» sustituyen a «EJERCICIO DIFÍCIL» y «ERROR ANTERIOR».
  - Confeti de 4 s como máximo (2,5 s el de mazo) y un solo brillo del título; sustituye a la
    excepción del autor original (7 s y dos brillos).
  - Sonidos de respuesta fijos por defecto y variados los de final; los 18 sonidos son nuevos, creados
    con la receta del informe (los anteriores, algunos con nombres de marcas, se retiran).
  - Sin la espera de 0,1 s al pulsar con el ratón: la respuesta sale al soltar. Sustituye a la
    decisión del autor original.
- 2.5.0 · Decisiones de diseño del taller al aplicar el informe: «Restaurar» va en cada recuadro y no
  una sola vez abajo, porque el modelo de opciones del taller restaura por grupo; el aviso de
  «Probar» va encima de su fila, como todos los avisos del modelo, y no debajo; las casillas conservan
  el texto en seminegrita del modelo (el informe pedía letra normal; las etiquetas nuevas de la
  izquierda sí van en letra normal); los recuadros conservan el relleno del modelo (16 × 20 px).
- 2.5.0 · El texto de ejemplo y los avisos usan los tokens de la paleta. Las insignias, los botones y
  el título dorado llevan colores propios del complemento, fijados por los informes (desde la 2.6.0,
  los de look.py, calculados por contraste).

- El confeti y el brillo dorado necesitan un mínimo: 5 respuestas en la sesión para el mazo y 20
  tarjetas distintas hoy para el día. Sin él solo suena el sonido de fin. Decisión del
  autor original, para que el confeti no salga por repasar dos tarjetas.
- Si al terminar un mazo ya no queda nada en ningún otro, la celebración es la de todos los mazos,
  con su mínimo de 20 tarjetas del día, aunque la sesión del mazo hubiera llegado a 5 respuestas.
  Por eso, en un día corto, terminar el último mazo puede sonar sin confeti. Decisión del autor
  original.
- Los sonidos usan un reproductor propio y no el de Anki, para que el audio de la tarjeta siguiente
  no corte el sonido de acierto. Decisión del autor original.
- El estilo y el código de los botones, las insignias y el confeti van dentro de la propia página
  del repaso, no como archivos aparte: así están listos desde el primer momento y ninguna tarjeta
  puede pedir archivos del complemento. Decisión del autor original.
- En los idiomas que no son los nueve completos, los textos de la ventana de opciones y de los avisos
  nuevos de la 2.5.0 salen en inglés; si a un idioma le falta un texto, sale en inglés. Decisión del
  autor original, que el informe 2.4.0 mantiene (las insignias sí están en los 54).
- 2.2.0 · Los dos sonidos de fallo los creó el taller para el complemento. Desde la 2.5.0 los 18
  sonidos de serie salen de la receta del informe 2.4.0 (herramientas/generar_sonidos_profeedback.py):
  sumas de tonos, sin grabaciones ni derechos de terceros.
- 2.4.0 (sustituido en la 2.6.0 por la paleta propia del informe del 2026-11-17) · Botones,
  insignias, «Editar» y «Más» y la raya gris eran iguales que en el ProFeedback original, con sus
  colores fijos, que no cambiaban con Atelier ni con el modo noche. Lo pidió la
  persona el 2026-11-13 («lo quiero igual al original»), con el original delante. Es una excepción a
  la regla de colores de la paleta del taller: cada color lleva su marca. Desde la 2.5.0 los textos
  que no llegaban a 4,5 a 1 (insignias de día, «Mostrar respuesta», «Editar» y «Más») usan un tono
  más oscuro del mismo color o los grises de la paleta; las caras y los iconos no cambian.
