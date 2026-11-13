# Qué hace «ProFeedback»

Versión 2.4.0 · 2026-11-13

Hace más agradable el repaso: suena un sonido cuando responde «Bien» o «Fácil» y otro cuando
responde «Otra vez» o «Difícil», pone una
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

## 2. Sonidos al acertar y al fallar

- Al responder «Bien» o «Fácil», con el ratón o con el teclado, suena un sonido corto de acierto.
- Desde la 2.2.0, al responder «Otra vez» o «Difícil» suena un sonido corto de fallo, si su casilla
  está marcada (lo está por defecto). Trae dos sonidos de fallo propios del complemento, breves y
  suaves (suave.mp3, dos notas que bajan, y grave.mp3, una nota grave), creados para él; por defecto
  está en «Aleatorio». Se puede fijar uno o desmarcar la casilla para no oír nada al fallar.
- Los sonidos de acierto: el complemento trae tres.
  Por defecto está en «Aleatorio»: cada vez suena uno de
  ellos, procurando no repetir el anterior (igual con los de fallo). En las opciones se puede fijar uno concreto.
- Usa un reproductor propio, aparte del de Anki, para que el audio de la tarjeta siguiente no lo
  corte a medias.

## 3. Insignias de la tarjeta

Desde la 2.4.0, iguales que en el ProFeedback original (petición del 2026-11-13): encima del
contenido de la tarjeta, centrados, un icono redondo de 32 px y un texto en mayúsculas y negrita,
los dos del color de su aviso, sin recuadro ni píldora. Solo una a la vez, por este orden de
prioridad:

- «TARJETA NUEVA», en morado (#CE82FF): la tarjeta es nueva (también si se reinició y vuelve a ser
  nueva).
- «EJERCICIO DIFÍCIL», en rojo (#FF4B4B): sus tres últimas respuestas fueron «Otra vez».
- «ERROR ANTERIOR», en naranja (#FFAB33): alguna de sus dos últimas respuestas fue «Otra vez»
  (incluidas las de hoy, por ejemplo una tarjeta que vuelve en el paso de aprendizaje).
- Si no se cumple nada de esto, no hay insignia.

Solo cuentan las respuestas dadas con un botón; los cambios de fecha hechos a mano no. La misma
insignia sale en la pregunta y en la respuesta. Ocupa su sitio encima de la tarjeta (la empuja un
poco hacia abajo, con medio renglón de aire debajo) y aparece con un fundido de 0,16 segundos; sin
fundido si el sistema pide reducir las animaciones. No se puede pulsar ni seleccionar. Los colores
son los fijos del original, los mismos de día y de noche: no cambian con Atelier.

## 4. Botones del repaso

Con la opción «Botones de respuesta 3D de colores» (marcada por defecto), los botones de la barra
inferior del repaso tienen, desde la 2.4.0, el aspecto del ProFeedback original (petición del
2026-11-13), con sus colores fijos, los mismos de día y de noche:

- «Otra vez» rojo (#FF4B4B), «Difícil» naranja (#FFAB33), «Bien» verde (#93D333) y «Fácil» azul
  claro (#49C0F8), con la letra casi negra (#131F24) en negrita de 15 px, sin mayúsculas. Cada uno
  con un canto de 2 px debajo, de su color más oscuro, que le da relieve.
- «Mostrar respuesta», dorado (#FFD700) con la letra ámbar (#AE6802) y un canto de 4 px más oscuro.
- «Editar» y «Más», sin relleno: contorno gris de 2 px con un canto de 4 px abajo y letra gris
  (de día #C9D1D9 y #57606A; de noche #37464F y #52656D), separados de los demás.
- Medidas: 48 px de alto, 130 px de ancho como mínimo (crecen con el texto), 24 px de relleno a los
  lados y esquinas de 18 px.
- Encima de la barra, una raya gris continua de 2 px (#D7DDE2 de día, #37464F de noche).
- Los tiempos previstos («10 min», «4 d») y el recuento de tarjetas, en el color de texto de Anki (el
  original usaba negro y blanco puros: retoque casi imperceptible).
- Al pasar el ratón se aclaran (brillo 1,08); nunca se oscurecen. Mandan su forma y sus colores
  aunque Atelier (Nocturne) esté instalado (FIX-006). Si desmarca «Botones de respuesta 3D de
  colores», los botones vuelven al aspecto de Anki o de Atelier.
- Al pulsarlos se hunden sobre su canto con un pequeño rebote. Con el ratón, la respuesta llega a
  Anki una décima de segundo después, para que se vea el gesto; con «reducir movimiento» activado
  en el sistema, al instante y sin rebote. Los atajos de teclado responden siempre al instante. En
  «Mostrar respuesta» y en los de respuesta, un segundo clic en el mismo botón antes de 0,4
  segundos se ignora.
- Retoques casi imperceptibles sobre el original: con el teclado, el botón elegido lleva un aro de
  foco azul; en ventanas de menos de 640 px los botones se compactan un poco para no salirse; y si
  una palabra no cabe, se reduce la letra.

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

Título «ProFeedback». Desde la 2.1.0 sigue el modelo de ventana de opciones del taller, el panel de GritMap (regla
PROP-012, petición del 2026-11-09): un panel de 560 px de ancho y el alto justo para su contenido,
hecho de recuadros sobre el fondo de Anki, con los colores de la paleta (también con Atelier) y
Aceptar y Cancelar abajo (en Windows, Aceptar primero). Desde la 2.2.0, la ventana entera es
invisible hasta que el panel está dibujado y con su alto definitivo, y entonces aparece de una vez:
sin destello, sin fondo vacío previo y sin cambiar de tamaño ante sus ojos (FIX-005). Recuerda
su tamaño y su posición, y si ya está abierto se trae al frente. Esc cancela y Ctrl+Intro acepta.
Nada se guarda hasta pulsar Aceptar. Aceptar, Cancelar, Restaurar, Sí y No llevan el texto de Qt en
el idioma de Anki. Con el teclado: el tabulador recorre los controles, cada uno con su contorno de
foco azul; el lector de pantalla anuncia el nombre de cada control.

Cuatro recuadros, de arriba abajo (sin «Restaurar», como antes):

| Recuadro | Opción | Control | Por defecto |
|---|---|---|---|
| — | Volumen | Deslizador de 0 a 100 con la cifra al lado («100 %»), con el carril relleno del color de acción hasta el valor. Vale para todos los sonidos. La mitad suena a la mitad, no casi igual de fuerte | 100 % |
| Sonidos al responder | «Reproducir sonido al acertar (Bien/Fácil)» | Casilla | Marcada |
| | Sonido (colgando de la casilla) | Lista desplegable con «Aleatorio» o uno de los sonidos de acierto (de serie: good.mp3, magic.mp3 y soft.mp3), y el botón «Probar» al lado | Aleatorio |
| | «Reproducir sonido al fallar (Otra vez/Difícil)» (2.2.0) | Casilla, debajo de la de acierto | Marcada |
| | Sonido (colgando de la casilla) | Lista con «Aleatorio» o uno de los sonidos de fallo (de serie: grave.mp3 y suave.mp3) y «Probar» | Aleatorio |
| Sonidos al finalizar | «Reproducir sonido al terminar de repasar» | Casilla | Marcada |
| | «Al terminar un mazo» | Lista + «Probar» (duolingo.mp3, khan.mp3 y winners.mp3) | Aleatorio |
| | «Al terminar todos los mazos» | Lista + «Probar» (duolingo.mp3 y mario bros.mp3) | Aleatorio |
| | «Al terminar un mazo (perfecto)» | Lista + «Probar» (winning1.mp3 y winning2.mp3) | Aleatorio |
| | «Al terminar todos los mazos (perfecto)» | Lista + «Probar» (mario-bros.mp3 y sound-celebration.mp3) | Aleatorio |
| Aspecto | «Confeti» | Casilla | Marcada |
| | «Botones de respuesta 3D de colores» | Casilla | Marcada |
| | «Insignias en la tarjeta (Nueva/Difícil/Error anterior)» | Casilla | Marcada |

- Al pie del recuadro de aspecto, la nota gris «Para añadir sonidos propios, copie archivos .mp3 en
  la subcarpeta de «user_files/sonidos» del complemento que corresponda: «correcto», «fallo»,
  «finalizado/mazo», «finalizado/todo», «perfecto-mazo» o «perfecto-todo».» (desde la 2.1.0, en los
  nueve idiomas completos; en los demás, en inglés). Al abrir la ventana se crean esas subcarpetas
  vacías si faltan (FIX-004).
- Lo que cuelga de una casilla se ve atenuado y no responde si la casilla está desmarcada. Una lista y
  su «Probar» se ven apagados también si no hay ningún sonido de ese tipo.
- Si no hay ningún sonido de acierto, en su recuadro aparece «No se encontraron archivos .mp3 en
  «sonidos/correcto».»; si no hay ninguno de fallo, «No se encontraron archivos .mp3 en
  «sonidos/fallo».»; si no hay ninguno de fin, «No se encontraron archivos .mp3 en
  «sonidos/finalizado».».
- «Probar» toca el sonido elegido (o uno al azar con «Aleatorio») con el volumen que marca el
  deslizador, sin guardar nada. Al cerrar la ventana, el volumen vuelve al guardado si no acepta.
- «Confeti» es independiente de los sonidos: puede tener confeti sin sonido de fin, y al revés. Si
  desmarca las dos cosas, al terminar no se hace nada.
- Aceptar guarda y deja los sonidos preparados al momento. El aspecto de los botones cambia la
  próxima vez que entre a repasar. Las insignias se quitan o se ponen desde la tarjeta siguiente;
  si las activa en mitad de un repaso, salen sin su aspecto hasta que vuelva a entrar (es un fallo
  pendiente). Cancelar cierra sin guardar.
- Si un sonido guardado ya no existe, la lista muestra «Aleatorio» y suena uno al azar.

## 7. Sonidos y letra propios

- Solo se usan archivos .mp3. Los que trae el complemento están en su carpeta, separados por tipo.
- Los propios van en la carpeta «user_files» del complemento (Herramientas > Complementos,
  seleccionarlo y pulsar «Ver archivos»), que Anki conserva al instalar versiones nuevas. Dentro,
  en «sonidos» y en una subcarpeta con el mismo nombre que la del complemento para cada tipo:
  «correcto» (acierto), «fallo» (fallo, desde la 2.2.0), «finalizado/mazo», «finalizado/todo», «perfecto-mazo» y «perfecto-todo».
  Desde la 2.1.0 se crean vacías al abrir la ventana de opciones. Un archivo propio con el mismo nombre que uno de serie lo
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
