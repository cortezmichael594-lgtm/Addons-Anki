# Qué hace «ProFeedback»

Versión 2.0.0 · 2026-10-21

Hace más agradable el repaso: suena un sonido cuando responde «Bien» o «Fácil», pone una
insignia encima de la tarjeta (tarjeta nueva, ejercicio difícil o error anterior), da a los botones
de la barra inferior del repaso un aspecto de colores con relieve y, al terminar un mazo o todo lo
del día, toca un sonido de fin y suelta confeti, dorado si no hubo ningún fallo. Solo lee su
colección: nunca cambia tarjetas, notas ni repasos. Lo único que guarda son sus opciones.

## 1. Dónde aparece

- En la pantalla de repaso: la insignia encima de la tarjeta, los botones de la barra inferior con
  su nuevo aspecto y el sonido al acertar.
- En la pantalla del mazo, al volver del repaso con el mazo terminado (la pantalla en la que Anki
  dice «¡Felicitaciones! Has finalizado este mazo por ahora.»): el sonido de fin y el confeti.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No añade menús ni atajos de teclado. No aparece en la lista de mazos, en Explorar, en el editor,
  en las vistas previas de tarjetas ni en las estadísticas.

## 2. Sonido al acertar

- Al responder «Bien» o «Fácil», con el ratón o con el teclado, suena un sonido corto. Con «Otra
  vez» y «Difícil» no suena nada.
- El complemento trae tres sonidos para esto. Por defecto está en «Aleatorio»: cada vez suena uno de
  ellos, procurando no repetir el anterior. En las opciones se puede fijar uno concreto.
- Usa un reproductor propio, aparte del de Anki, para que el audio de la tarjeta siguiente no lo
  corte a medias.

## 3. Insignias de la tarjeta

Encima del contenido de la tarjeta, centrada, aparece una píldora con un icono y un texto en
mayúsculas, del color de su aviso. Solo una a la vez, por este orden de prioridad:

- «TARJETA NUEVA», en azul: la tarjeta es nueva (también si se reinició y vuelve a ser nueva).
- «EJERCICIO DIFÍCIL», en naranja: sus tres últimas respuestas fueron «Otra vez».
- «ERROR ANTERIOR», en rojo: alguna de sus dos últimas respuestas fue «Otra vez» (incluidas las de
  hoy, por ejemplo una tarjeta que vuelve en el paso de aprendizaje).
- Si no se cumple nada de esto, no hay insignia.

Solo cuentan las respuestas dadas con un botón; los cambios de fecha hechos a mano no. La misma
insignia sale en la pregunta y en la respuesta. Ocupa su sitio encima de la tarjeta (la empuja un
poco hacia abajo) y aparece con un fundido muy breve, de algo más de una décima de segundo; sin
fundido si el sistema pide reducir las animaciones. No se puede pulsar ni seleccionar. Los colores
salen del tema de Anki (o de Nocturne), con su versión para el modo noche.

## 4. Botones del repaso

Con la opción «Botones de respuesta 3D de colores» (marcada por defecto), los botones de la barra
inferior del repaso cambian de aspecto:

- «Otra vez» en rojo, «Difícil» en naranja, «Bien» en verde y «Fácil» en azul, con letra en
  mayúsculas y negrita y un canto inferior que les da relieve. De día el color es algo más oscuro y
  la letra blanca; de noche, el color vivo con la letra oscura.
- «Mostrar respuesta», en el azul de acción de Anki, algo más ancho.
- «Editar» y «Más», discretos: fondo de botón normal, contorno fino y letra gris, que se oscurece
  al pasar el ratón.
- Todos tienen el mismo tamaño en todos los idiomas. Si una palabra no cabe, se reduce la letra,
  nunca el botón. En ventanas estrechas los botones se hacen más pequeños, pero todos iguales.
- Los tiempos previstos («10 min», «4 d») y el recuento de tarjetas siguen encima de los botones,
  como en Anki, en gris y sin mayúsculas.
- Al pasar el ratón se aclaran un poco. Al pulsarlos con el ratón se hunden sobre su canto y la
  respuesta llega a Anki una décima de segundo después, para que se vea el gesto; con «reducir
  movimiento» activado en el sistema, al instante. Los atajos de teclado responden siempre al
  instante. En «Mostrar respuesta» y en los de respuesta, un segundo clic en el mismo botón antes
  de 0,4 segundos se ignora.
- Con el teclado, el botón elegido lleva un recuadro de foco.

## 5. Al terminar de repasar: sonido y confeti

La celebración solo ocurre al volver del repaso a la pantalla del mazo habiendo respondido alguna
tarjeta en esa sesión. Si sale del repaso por otro camino (a la lista de mazos, o con «Terminar»
en el aviso de tiempo de estudio), esa sesión se descarta y no se celebra nada. Una sesión empieza
cada vez que entra a repasar.

Qué se celebra al volver:

- Si no queda nada por repasar hoy en ninguno de sus mazos: celebración de «todos los mazos».
  Tiene prioridad: al terminar el último mazo del día sale esta y no la del mazo.
- Si no queda nada en el mazo que repasaba, pero sí en otros: celebración de «mazo».
- Si aún queda algo en el mazo, nada.

Lo que queda se cuenta como lo cuenta Anki, con sus límites diarios: las tarjetas nuevas por
encima del límite no cuentan, ni las de aprendizaje que todavía no tocan. Por eso, si vuelven
tarjetas de aprendizaje y las termina, puede celebrarse otra vez el mismo día. Si deshace una
respuesta sin salir del repaso, la sesión la sigue contando (es un fallo pendiente).

El sonido de fin suena siempre que hay celebración (si su opción está marcada). El confeti necesita
un mínimo de repaso:

| Celebración | Mínimo para el confeti | Es «perfecta» si… | Confeti |
|---|---|---|---|
| Mazo | 5 respuestas en la sesión | además, todas las respuestas de la sesión fueron «Bien» o «Fácil» | Dos cañones desde las esquinas de abajo |
| Todos los mazos | 20 tarjetas distintas respondidas hoy en toda la colección | además, ninguna tarjeta de hoy tuvo un «Otra vez» o un «Difícil» | Lluvia desde arriba durante 7 segundos |

- «Hoy» empieza a la hora de cambio de día de Anki, y lo de hoy se lee del historial de Anki: cuenta
  cada perfil por separado, incluye lo repasado en otros dispositivos ya sincronizado y no se pierde
  si Anki se cierra de golpe.
- Una celebración perfecta toca el sonido «perfecto» de su tipo; si no hay ninguno, el normal. El
  confeti perfecto es dorado (tonos dorados y anaranjados) y el título de la pantalla del mazo
  brilla en dorado: un reflejo que lo recorre dos veces, de unos 3,6 segundos cada una.
- El confeti normal usa los colores del tema: rojo, naranja, verde, azul y los de las marcas.
- Sin el mínimo, solo suena el sonido de fin: ni confeti ni brillo, aunque no hubiera fallos.
- El confeti pasa por encima de todo sin tapar nada: se puede seguir pulsando. Desaparece solo.
- Con «reducir movimiento» activado en el sistema no hay confeti; en una celebración perfecta el
  título queda dorado, sin moverse.
- La decisión se toma sin congelar Anki.

## 6. Ventana de opciones

Título «ProFeedback», sin botón de ayuda. Recuerda su tamaño y su posición. De arriba abajo:

| Opción | Valores | Por defecto |
|---|---|---|
| Volumen | Deslizador de 0 a 100, con la cifra al lado («100 %»). Vale para todos los sonidos. La mitad suena a la mitad, no casi igual de fuerte | 100 % |
| Sonidos al responder: «Reproducir sonido al acertar (Bien/Fácil)» | Casilla | Marcada |
| Sonido | «Aleatorio» o uno de los sonidos de acierto (de serie: good.mp3, magic.mp3 y soft.mp3), con el botón «Probar» | Aleatorio |
| Sonidos al finalizar: «Reproducir sonido al terminar de repasar» | Casilla | Marcada |
| «Al terminar un mazo» | «Aleatorio» o un sonido (de serie: duolingo.mp3, khan.mp3 y winners.mp3), con «Probar» | Aleatorio |
| «Al terminar todos los mazos» | «Aleatorio» o un sonido (de serie: duolingo.mp3 y mario bros.mp3), con «Probar» | Aleatorio |
| «Al terminar un mazo (perfecto)» | «Aleatorio» o un sonido (de serie: winning1.mp3 y winning2.mp3), con «Probar» | Aleatorio |
| «Al terminar todos los mazos (perfecto)» | «Aleatorio» o un sonido (de serie: mario-bros.mp3 y sound-celebration.mp3), con «Probar» | Aleatorio |
| Aspecto: «Confeti» | Casilla | Marcada |
| Aspecto: «Botones de respuesta 3D de colores» | Casilla | Marcada |
| Aspecto: «Insignias en la tarjeta (Nueva/Difícil/Error anterior)» | Casilla | Marcada |

- Al pie, la nota «Para añadir sonidos propios, copie archivos .mp3 en la carpeta «user_files/sonidos»
  del complemento.» (véase el apartado 7) y los botones Aceptar y Cancelar.
- Un desplegable y su «Probar» se ven apagados si su casilla está desmarcada o si no hay ningún
  sonido de ese tipo.
- Si no hay ningún sonido de acierto, en su grupo aparece «No se encontraron archivos .mp3 en
  «sonidos/correcto».»; si no hay ninguno de fin, «No se encontraron archivos .mp3 en
  «sonidos/finalizado».».
- «Probar» toca el sonido elegido (o uno al azar con «Aleatorio») con el volumen que marca el
  deslizador, sin guardar nada. Al cerrar la ventana, el volumen vuelve al guardado si no acepta.
- «Confeti» es independiente de los sonidos: puede tener confeti sin sonido de fin, y al revés. Si
  desmarca las dos cosas, al terminar no se hace nada.
- Aceptar guarda y deja los sonidos preparados al momento. El aspecto de los botones cambia la
  próxima vez que entre a repasar. Las insignias se quitan o se ponen desde la tarjeta siguiente;
  si las activa en mitad de un repaso, salen sin su aspecto hasta que vuelva a entrar (es un fallo
  pendiente). Cancelar cierra sin guardar.
- Si un sonido guardado ya no existe, el desplegable muestra «Aleatorio» y suena uno al azar.

## 7. Sonidos y letra propios

- Solo se usan archivos .mp3. Los que trae el complemento están en su carpeta, separados por tipo.
- Los propios van en la carpeta «user_files» del complemento (Herramientas > Complementos,
  seleccionarlo y pulsar «Ver archivos»), que Anki conserva al instalar versiones nuevas. Dentro,
  en «sonidos» y en una subcarpeta con el mismo nombre que la del complemento para cada tipo:
  «correcto» (acierto), «finalizado/mazo», «finalizado/todo», «perfecto-mazo» y «perfecto-todo».
  Esas carpetas no vienen creadas. Un archivo propio con el mismo nombre que uno de serie lo
  sustituye.
- La lista de sonidos se vuelve a leer al abrir la ventana de opciones y al abrir un perfil.
- Letra: si deja en «user_files» (o en la carpeta del complemento) un archivo «ProFeedback.ttf» o
  «Feather Bold.ttf» de 1,5 MB como máximo, los botones y las insignias usan esa letra. Si no hay
  ninguno, como ahora, usan la letra del sistema.

## 8. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de Anki de ese ordenador: valen para todos los
  perfiles y no viajan con la sincronización.
- El tamaño y la posición de la ventana de opciones, en el perfil de Anki.
- Nada en la colección. Solo lee el historial de respuestas y lo que queda por repasar.
- Si falta una opción o tiene un valor que no sirve (por ejemplo, escrito a mano), usa el valor por
  defecto; el volumen se limita a 0–100. Al guardar, borra tres datos que guardaba una versión
  anterior para llevar la cuenta del día y que ya no se usan.

## 9. Idiomas

Las insignias y la ventana de opciones están en 54 idiomas, según el idioma de Anki; si el de Anki
no está, en inglés. Español, inglés, portugués (de Brasil y de Portugal), catalán, gallego,
francés, italiano y alemán están completos. En los otros 45, cinco textos salen en inglés: «Volumen»,
«Sonido», «Aleatorio», la nota de sonidos propios y el aviso de fallo. Los botones Aceptar y
Cancelar salen en el idioma de Anki, y los de la barra de repaso conservan los textos de Anki.

## 10. Si algo falla

- Nunca abre la ventana de error de Anki. En su lugar muestra durante 5 segundos el aviso
  «ProFeedback tuvo un problema. Anki sigue funcionando; el detalle quedó en su registro.», una sola
  vez por cada función y sesión de Anki, para no llenar la pantalla si el fallo se repite.
- Los tropiezos con los sonidos, con los archivos o con la decisión de qué celebrar no avisan: no se
  oye o no se celebra, y el detalle queda en el registro del complemento.
- Si el equipo no tiene el módulo de sonido de Qt (pasa en algunas instalaciones de Linux), usa el
  reproductor de Anki: entonces el volumen no se aplica y el audio de una tarjeta puede cortar el
  sonido.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su colección: ni tarjetas, ni notas, ni repasos, ni fechas.
- No suena con «Otra vez» ni con «Difícil».
- No celebra si sale del repaso por otra pantalla que no sea la del mazo.
- No pone insignias en las vistas previas ni en el editor de tarjetas.
- No deja que las tarjetas lean archivos suyos: su estilo y su código van dentro de la propia página.
- No añade menús ni atajos.
