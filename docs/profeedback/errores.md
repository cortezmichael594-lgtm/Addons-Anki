# Errores de «ProFeedback»

Registro en lenguaje llano de los fallos de este complemento. Lo mantiene Claude Code: cada corrección
del código (FIX-NNN) tiene aquí su línea con el mismo número, y el comprobador vigila que no falte
ninguna. Las tres primeras se hicieron antes de que el complemento llegara a este taller (versión
2.0.0); la versión exacta de cada una no consta, solo su fecha.

## Pendientes

Fallos detectados que esperan su decisión. Cada uno: fecha, versión, qué pasa y propuesta.

- 2026-10-21 · versión 2.0.0 · Qué pasa: la nota de la ventana de opciones dice «Para añadir sonidos
  propios, copie archivos .mp3 en la carpeta «user_files/sonidos» del complemento.», pero el
  complemento solo busca dentro de cinco subcarpetas de esa carpeta, una por tipo («correcto»,
  «finalizado/mazo», «finalizado/todo», «perfecto-mazo» y «perfecto-todo»), que además no vienen
  creadas. Un .mp3 copiado tal como dice la nota no aparece en ningún desplegable y no suena nunca.
  Propuesta: que la nota diga qué subcarpeta corresponde a cada sonido y que el complemento cree
  esas carpetas vacías la primera vez.
- 2026-10-21 · versión 2.0.0 · Qué pasa: si deshace una respuesta (Editar > Deshacer) sin salir del
  repaso, el complemento la sigue contando para la celebración del mazo. Una «Otra vez» deshecha y
  respondida después con «Bien» impide la celebración perfecta aunque todas las respuestas que
  quedan sean «Bien» o «Fácil»; y las respuestas deshechas suman para el mínimo de 5, así que con 4
  tarjetas y una respuesta deshecha sale confeti. La celebración de todos los mazos no tiene este
  fallo, porque lee el historial de Anki. Propuesta: que la sesión del mazo también se cuente con
  el historial de Anki (las respuestas desde que entró a repasar), que ya descuenta lo deshecho.
- 2026-10-21 · versión 2.0.0 · Qué pasa: si «Insignias en la tarjeta» estaba desmarcada al entrar a
  repasar y la marca en ese momento (Herramientas > Complementos > Configuración), las tarjetas
  siguientes muestran la insignia sin su aspecto: el icono grande y el texto sueltos encima de la
  tarjeta, sin la píldora de color, hasta que sale del repaso y vuelve a entrar. Propuesta: cargar
  siempre el estilo de la insignia en el repaso (es pequeño y no se ve si no hay insignia), de modo
  que activarla a mitad de repaso salga ya con su aspecto.
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
  «Aleatorio», y un sonido guardado que ya no existe se muestra como esa entrada.
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

## Así a propósito

Lo que parece un fallo pero se decidió así, y quién lo decidió. No se «arregla» sin preguntar.

- «Difícil» no cuenta como acierto: no suena el sonido de acierto y quita la celebración perfecta
  (del mazo y del día). Decisión del autor original.
- El confeti y el brillo dorado necesitan un mínimo: 5 respuestas en la sesión para el mazo y 20
  tarjetas distintas hoy para todos los mazos. Sin él solo suena el sonido de fin. Decisión del
  autor original, para que el confeti no salga por repasar dos tarjetas.
- Si al terminar un mazo ya no queda nada en ningún otro, la celebración es la de todos los mazos,
  con su mínimo de 20 tarjetas del día, aunque la sesión del mazo hubiera llegado a 5 respuestas.
  Por eso, en un día corto, terminar el último mazo puede sonar sin confeti. Decisión del autor
  original.
- Los sonidos usan un reproductor propio y no el de Anki, para que el audio de la tarjeta siguiente
  no corte el sonido de acierto. Decisión del autor original.
- Al pulsar un botón de respuesta con el ratón, la respuesta llega a Anki una décima de segundo
  después, para que se vea el botón hundirse; con el teclado es inmediata. Decisión del autor
  original.
- El confeti (hasta 7 segundos) y el brillo del título (dos pasadas de unos 3,6 segundos) duran más
  que las animaciones breves que pide la guía del taller, porque son la función misma del
  complemento. Respetan la opción del sistema de reducir las animaciones. Decisión del autor
  original.
- El estilo y el código de los botones, las insignias y el confeti van dentro de la propia página
  del repaso, no como archivos aparte: así están listos desde el primer momento y ninguna tarjeta
  puede pedir archivos del complemento. Decisión del autor original.
- Muchos idiomas tienen cinco textos de la ventana de opciones en inglés («Volume», «Sound»,
  «Random», la nota de sonidos propios y el aviso de fallo); si a un idioma le falta un texto, sale
  en inglés. Decisión del autor original.
