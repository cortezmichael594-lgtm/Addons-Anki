# Qué hace «ProFeedback»

Versión 2.6.3 · 2026-11-17

Hace más agradable el repaso: suena un sonido corto al acertar y otro, más discreto, al pulsar «Otra
vez»; pone una insignia encima de la tarjeta (tarjeta nueva, «se resiste» u «otra oportunidad»); da a
los botones de la barra inferior del repaso un aspecto de colores con relieve; y, al terminar un mazo o
todo lo del día, toca un sonido de fin y suelta confeti, dorado al terminar el día. Solo lee su
colección: nunca cambia tarjetas, notas ni repasos. Lo único que guarda son sus opciones.

La 2.5.0 aplica el informe «ProFeedback 2.4.0: auditoría y rediseño de la interfaz» (aprobado entero el
2026-11-16), con la opción recomendada en sus cuatro decisiones: el oro premia terminar el día y no la
nota que uno se pone, «Bien» más ancho, «SE RESISTE» y «OTRA OPORTUNIDAD», y confeti más corto.

La 2.6.0 aplica entero el informe «Rediseño de color y forma: ProFeedback 2.5.0» (2026-11-17), con la
opción recomendada en sus tres decisiones: «Mostrar respuesta» en el azul de acción de Atelier, paleta
propia para los cuatro botones (deja de ser la de Duolingo) y esquinas de 12 px con canto de 3. Cambian
también las insignias, el confeti (diseñado entero), el título del fin del día y el estado con el ratón
encima; y se añade «Ver» junto a «Confeti al terminar». La 2.6.1 quita el círculo de fondo de los
iconos de las insignias (a petición suya) y hace que «Ver» explique por qué no hay confeti cuando el
sistema pide reducir las animaciones (FIX-008).

## 1. Dónde aparece

- En la pantalla de repaso: la insignia encima de la tarjeta, los botones de la barra inferior con su
  nuevo aspecto y el sonido al responder.
- En la pantalla del mazo, al volver del repaso con el mazo terminado (la pantalla en la que Anki dice
  «¡Felicitaciones! Has finalizado este mazo por ahora.»): el sonido de fin y el confeti.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No añade menús ni atajos de teclado. No aparece en la lista de mazos, en Explorar, en el editor, en
  las vistas previas de tarjetas ni en las estadísticas.

## 2. Sonidos al responder

- «Difícil», «Bien» y «Fácil» son aciertos, como dice el manual de Anki: suena el sonido de acierto
  (desde la 2.5.0 también con «Difícil», que antes sonaba como fallo).
- «Otra vez» suena distinto: una nota grave y corta que dice «anotado, vuelve luego», no un castigo. Va
  unos 3 dB más baja que la de acierto.
- Los dos son de la misma familia (misma voz y tonalidad) y duran un cuarto de segundo: informan de qué
  botón se registró sin pisar el audio de la tarjeta siguiente.
- Por defecto suena siempre el mismo («1 · Madera»), para que se vuelva fondo. Se puede elegir otro, uno
  propio, «Aleatorio» o «Sin sonido».
- Usa un reproductor propio, aparte del de Anki, para que el audio de la tarjeta siguiente no lo corte a
  medias.

Los 18 sonidos de serie son nuevos en la 2.5.0 y sustituyen a todos los anteriores: tres por tipo, con
tres voces («Madera», «Campanilla» y «Suave»), creados para el complemento por síntesis (sumas de
tonos, sin grabaciones ni derechos de terceros), todos en la misma tonalidad y por debajo de 3
segundos. Por tipo:

| Tipo | Duración | Carácter |
|---|---|---|
| Acierto | 0,4 s | Dos notas que suben |
| «Otra vez» | 0,3 a 0,4 s | Una nota grave |
| Fin de mazo | 1,2 a 1,6 s | Tres a cinco notas que suben y se quedan en la última |
| Fin del día | 2,2 a 3 s | Una escala corta y un acorde que se queda sonando |

En las listas de fin de mazo y fin del día hay seis: los tres de fin y los tres que antes eran «perfecto».

## 3. Insignias de la tarjeta

Encima del contenido de la tarjeta, centrados, un icono redondo de 24 px y un texto en mayúsculas y
negrita de 14 px (0,4 px entre letras), con 8 px entre los dos y sin recuadro. Solo una a la vez, por
este orden de prioridad:

- «TARJETA NUEVA», morado: la tarjeta es nueva (también si se reinició).
- «SE RESISTE», rojo: sus tres últimas respuestas fueron «Otra vez» (antes, «EJERCICIO DIFÍCIL»).
- «OTRA OPORTUNIDAD», naranja: alguna de sus dos últimas respuestas fue «Otra vez», incluidas las de hoy
  (antes, «ERROR ANTERIOR»).
- Si no se cumple nada de esto, no hay insignia.

- Colores (2.6.0): las tres pesan igual. Texto a 6,8 a 1 de día y 8,5 de noche; de día, lejos de las
  banderas roja y morada de Anki.

  | Insignia | Texto día / noche | Icono día / noche |
  |---|---|---|
  | TARJETA NUEVA (violeta) | #73428F / #CDA1E9 | #A572C4 / #CDA1E9 |
  | SE RESISTE (rojo) | #9B322F / #F9988E | #D3655E / #F9988E |
  | OTRA OPORTUNIDAD (ámbar) | #7A4D07 / #E0A761 | #BA7816 / #E0A761 |

- Iconos: un dibujo del color de su insignia, con el fondo transparente, de día y de noche (desde la
  2.6.1; en la 2.6.0 iba sobre un círculo de color): un destello de cuatro puntas (nueva), una pesa (se
  resiste) y una flecha en bucle (otra oportunidad), con trazo de 2 px. De día, en tono medio (3,4 a 1
  contra el fondo); de noche, en tono claro. Texto con 0,06 em entre letras (antes, 0,4 px).
- Entre icono y texto, 8 px en «SE RESISTE» y 6 px en «TARJETA NUEVA» y «OTRA OPORTUNIDAD» (2.6.2,
  petición suya: sus dibujos dejan más aire alrededor).
- En el contraste alto de Windows, dibujo y texto en el color del texto.
- Encima de la tarjeta hay siempre una franja de 40 px (24 del icono y 16 de aire), haya insignia o no:
  la tarjeta empieza siempre en el mismo sitio y no salta de una a otra.
- Aparece con un fundido de 0,12 segundos; sin fundido si el sistema pide reducir las animaciones. No se
  puede pulsar ni seleccionar. Desde la 2.6.0, activarlas en mitad de un repaso las pone ya con su
  aspecto (FIX-007). Solo cuentan las respuestas dadas con un botón. La misma insignia sale en
  la pregunta y en la respuesta.
- Los dos textos nuevos están traducidos en los 54 idiomas.

## 4. Botones del repaso

Con la opción «Botones de colores con relieve» (marcada por defecto), los botones de la barra inferior
del repaso tienen colores con relieve. Desde la 2.6.0, con una paleta propia calculada por contraste
(antes, los colores de Duolingo) y una versión más suave de noche:

| Botón | Cara día / noche | Letra | Canto día / noche | Ratón encima día / noche |
|---|---|---|---|---|
| Otra vez (coral) | #F47B72 / #E8847B | #2F0405 | #DB655D / #C05F58 | #FD867C / #F38D84 |
| Difícil (ámbar) | #FDB354 / #F8B564 | #311C01 | #C78112 / #D08F3C | #FEC178 |
| Bien (jade) | #53E2A6 / #70DDAB | #01291A | #15A472 / #46B686 | #5FECAF / #7AE7B5 |
| Fácil (cielo) | #73C9FB / #7FC8F3 | #012537 | #4098C9 / #5AA1CB | #88D1FD / #89D1FD |
| Mostrar respuesta (azul de acción de Atelier) | #3B6FE0 / #4066E6 | blanca | #284EAA / #2B45AA | #3366D6 / #385CDC |

- La letra va en negrita de 15 px, en un tono muy oscuro del color de su botón (antes, un gris casi
  negro igual en los cuatro); en «Mostrar respuesta», blanca. Todas se leen igual o mejor que antes:
  «Otra vez» pasa de 5,1 a 7 a 1.
- «Difícil» y «Bien» se distinguen también con daltonismo rojo-verde (antes eran el mismo color).
- «Mostrar respuesta» ya no es dorado: el oro queda para celebrar haber terminado, como en
  CoreProgress.
- Todos miden 48 px de alto: una cara de 45 y un canto de 3 px, con esquinas de 12 px, las de la
  tarjeta y de Atelier (antes, 50 px, canto de 4 y esquinas de 16). De día el canto contrasta 3 a 1
  con la barra, para que el botón se vea como botón. 130 px de ancho como mínimo; «Bien» y «Mostrar
  respuesta», 190 px: así, tras pulsar «Mostrar respuesta», el puntero queda dentro de «Bien».
- «Editar» y «Más», sin relleno: contorno de 2 px con canto de 3 px del gris de los controles de la
  paleta y letra en el gris secundario. Con el ratón encima, se rellenan del color de pasar el ratón.
- Encima de la barra, una raya de 1 px del color de las rayas de la paleta (antes, 2).
- Los tiempos previstos («<1 min», «6 min»…), en el gris secundario de 12 px con cifras del mismo
  ancho (antes, en el color de texto de Anki).
- Al pasar el ratón por un botón de color, la cara se aleja de su letra: se aclara un poco y, en
  «Mostrar respuesta», se oscurece; el cambio se nota y nunca empeora la lectura (antes, un brillo de
  1,08 que apenas se veía). Mandan su forma y sus colores aunque Atelier (Nocturne) esté instalado
  (FIX-006).
- Al pulsarlo, la cara baja 3 px sobre su canto en 80 ms, sin cambiar de color, y vuelve en 70 ms al
  soltar, sin rebote. La respuesta sale en el instante en que se suelta el botón; si se suelta fuera,
  no responde. Los atajos de teclado responden al instante. Un segundo clic en el mismo botón antes de
  0,4 segundos se ignora. Con «reducir movimiento», sin animación.
- Con el teclado, el botón elegido lleva un aro de foco azul de 2 px, separado 2 px del botón.
- En el contraste alto de Windows, los botones toman los colores del sistema, con borde de 1 px y sin
  canto.
- En ventanas de menos de 640 px los botones se compactan un poco; si una palabra no cabe, se reduce la
  letra. Con la respuesta a la vista, la barra entera necesita unos 1.064 px de ancho.

## 5. Al terminar de repasar: sonido y confeti

La celebración solo ocurre al volver del repaso a la pantalla del mazo habiendo respondido alguna
tarjeta en esa sesión. Si sale del repaso por otro camino (a la lista de mazos, o con «Terminar» en el
aviso de tiempo de estudio), esa sesión se descarta. Una sesión empieza cada vez que entra a repasar. Si
deshace una respuesta sin salir del repaso, deja de contar (desde la 2.5.0).

Qué se celebra al volver:

- Si no queda nada por repasar hoy en ninguno de sus mazos: la celebración del día, una vez al día. Si
  después vuelven tarjetas de aprendizaje y las termina, se celebra como un mazo.
- Si no queda nada en el mazo que repasaba, pero sí en otros: la celebración de mazo.
- Si aún queda algo en el mazo, nada.

Lo que queda se cuenta como lo cuenta Anki, con sus límites diarios.

| Celebración | Mínimo para el confeti | Confeti |
|---|---|---|
| Mazo | 5 respuestas en la sesión | 72 piezas desde dos cañones en las esquinas de abajo, 2,4 s, con los cuatro colores de los botones (también el coral: cada respuesta contó) |
| Día | 20 tarjetas distintas respondidas hoy en toda la colección | 120 piezas en lluvia dorada desde arriba, 3,8 s, y el título de la pantalla pasa a dorado y lo cruza un brillo una vez (1,2 s) |

- Desde la 2.5.0 ninguna celebración depende de las notas: el oro premia terminar el día. Antes, la
  dorada exigía no haber pulsado nunca «Otra vez» ni «Difícil», lo que empujaba a calificarse al alza.
- Confeti (2.6.0, diseñado entero): tiras de 6 × 14 px con esquinas redondeadas, círculos de 8 y
  destellos de cuatro puntas de 12 (los de CoreProgress); en la lluvia, además, estrellas de cinco
  puntas de 13. Las piezas salen disparadas, frenan con el aire, caen despacio, se mecen de lado y
  giran como papel; empiezan a la vez que el sonido y la posición de cada una se sortea en cada
  celebración. Se desvanecen en los últimos 0,4 s. Como mucho 1,4 vueltas por segundo y 14 px por
  pieza: nada que parpadee. De día, la lluvia usa cuatro oros más oscuros, para que se vea caer sobre
  el fondo claro; de noche, los oros de CoreProgress y un crema.
- El título dorado es el oro de CoreProgress: #845E09 de día y #FEE06D de noche (antes, #8A5200 y
  #FFD700). El brillo es una banda más clara que lo cruza de izquierda a derecha una sola vez, desde
  los 0,3 s, y después el título se queda dorado y quieto.
- El sonido de fin suena siempre que hay celebración, salvo con «Sin sonido». Sin el mínimo, solo
  suena: ni confeti ni brillo.
- «Hoy» empieza a la hora de cambio de día de Anki, y lo de hoy se lee del historial de Anki: cuenta cada
  perfil por separado e incluye lo repasado en otros dispositivos ya sincronizado.
- El confeti pasa por encima de todo sin tapar nada y se desvanece en sus últimos 0,4 s.
- Con «reducir movimiento» activado en el sistema no hay confeti ni brillo: encima del título salen tres
  destellos fijos (jade, ámbar y cielo al terminar un mazo; dorados al terminar el día, con el título
  dorado y quieto).
- En el contraste alto de Windows no hay confeti ni destellos, y el título va en el color del texto.
- La decisión se toma sin congelar Anki.

## 6. Ventana de opciones

Título «ProFeedback» en la barra de la ventana (no se repite dentro). Sigue el modelo de ventana de
opciones del taller (el panel de GritMap): 560 px de ancho y el alto justo para su contenido (unos 545
px, sin barra de desplazamiento), recuadros sobre el fondo de Anki con los colores de la paleta, y
Aceptar y Cancelar abajo (en Windows, Aceptar primero). La ventana entera es invisible hasta que el
panel está dibujado y con su alto, y entonces aparece de una vez (FIX-005). Desde la 2.6.3 la ventana
se abre como cualquier otra, sin el pequeño destello que hacía en Windows: solo el panel espera oculto
a estar dibujado (FIX-009). Recuerda su tamaño y su
posición, y si ya está abierta se trae al frente. Esc cancela y Ctrl+Intro acepta. Nada se guarda hasta
pulsar Aceptar.

Dos recuadros, cada uno con «Restaurar valores predeterminados» arriba a la derecha (en el color de
enlace y subrayado), que devuelve ese recuadro a los valores de serie sin guardar, con «Deshacer» al
lado:

| Recuadro | Fila | Control | Por defecto |
|---|---|---|---|
| Sonido | Volumen | Deslizador de 0 a 100 con la cifra al lado («100 %»). Vale para todos los sonidos; la mitad suena a la mitad | 100 % |
| | Al acertar | Lista + «Probar» | 1 · Madera |
| | Al pulsar «Otra vez» | Lista + «Probar» | 1 · Madera |
| | Al terminar un mazo | Lista + «Probar» | Aleatorio |
| | Al terminar el día | Lista + «Probar» | Aleatorio |
| Aspecto | Botones de colores con relieve | Casilla | Marcada |
| | Insignias sobre la tarjeta | Casilla | Marcada |
| | Confeti al terminar | Casilla, con «Ver» a la derecha (2.6.0) | Marcada |

- Cada fila lleva la etiqueta a la izquierda (columna de 200 px, letra normal) y la lista a la derecha.
  Las dos de respuesta y las dos de final van separadas por un hueco.
- Cada lista, en este orden: «Sin sonido»; los de serie («1 · Madera», «2 · Campanilla», «3 · Suave»…);
  los propios, por su nombre de archivo; «Aleatorio» (si hay alguno); una raya; y «Abrir la carpeta de
  estos sonidos…», que abre en el explorador la carpeta propia de ese tipo (la crea si falta) y deja la
  lista como estaba.
- «Probar» toca el sonido elegido (o uno al azar con «Aleatorio») con el volumen del deslizador, sin
  guardar nada. Con «Sin sonido» se apaga. Si no consigue sonar, encima de la fila sale, en rojo y con
  icono, «No se pudo reproducir. Compruebe la salida de audio del equipo.», que se quita al cambiar de
  sonido o al volver a probar. El lector de pantalla oye cada «Probar» con su nombre («Probar el sonido
  de acierto», «Probar el sonido de «Otra vez»», «… de fin de mazo», «… de fin del día»).
- «Ver» (2.6.0) suelta el confeti de fin de mazo dentro de la propia ventana de opciones, con sus
  colores, sin terminar un mazo y sin guardar nada. Si el sistema pide reducir las animaciones (en
  Windows, Configuración › Accesibilidad › Efectos visuales › «Efectos de animación» desactivado), no
  hay confeti ni aquí ni al terminar, y desde la 2.6.1 «Ver» lo dice debajo de la casilla, con dónde se
  cambia (FIX-008). La opción «Reducir movimiento» de las preferencias de Anki no lo apaga: viene
  activada de serie y solo afecta a las transiciones de Anki.
- Al cerrar la ventana, el volumen vuelve al guardado si no acepta.
- Si un sonido guardado ya no existe, la lista muestra el primero de serie y suena ese.
- Aceptar guarda y deja los sonidos preparados al momento. El aspecto de los botones cambia la próxima
  vez que entre a repasar. Las insignias se quitan o se ponen desde la tarjeta siguiente; si las activa
  en mitad de un repaso, salen sin su aspecto hasta que vuelva a entrar (fallo pendiente).
- Ajustes de versiones anteriores: una casilla de sonido desmarcada pasa a «Sin sonido» en sus listas, y
  «Aleatorio» en los sonidos de respuesta (lo que venía de serie) pasa a «1 · Madera». Al guardar se
  borran los datos que ya no se usan (las casillas de sonido y los sonidos «perfecto»).

## 7. Sonidos y letra propios

- Solo se usan archivos .mp3. Los que trae el complemento están en su carpeta, separados por tipo.
- Los propios van en la carpeta «user_files/sonidos» del complemento, que Anki conserva al instalar
  versiones nuevas, en una subcarpeta por tipo: «correcto» (acierto), «fallo» («Otra vez»),
  «finalizado/mazo» y «perfecto-mazo» (fin de mazo), «finalizado/todo» y «perfecto-todo» (fin del día).
  Se crean vacías al abrir la ventana de opciones, y «Abrir la carpeta de estos sonidos…» abre la de
  cada lista. Un archivo propio con el mismo nombre que uno de serie lo sustituye.
- La lista de sonidos se vuelve a leer al abrir la ventana de opciones y al abrir un perfil.
- Letra: si deja en «user_files» (o en la carpeta del complemento) un archivo «ProFeedback.ttf» de 1,5 MB
  como máximo, los botones y las insignias usan esa letra. Desde la 2.6.0 ya no se reconoce el nombre
  «Feather Bold.ttf» (la letra de Duolingo): quien lo tuviera debe renombrarlo a «ProFeedback.ttf». Si no hay
  ninguno, como ahora, usan la letra del sistema.

## 8. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de Anki de ese ordenador: valen para todos los
  perfiles y no viajan con la sincronización.
- El tamaño y la posición de la ventana de opciones, en el perfil de Anki.
- Qué día ya se celebró en grande, solo en memoria mientras Anki está abierto.
- Nada en la colección. Solo lee el historial de respuestas y lo que queda por repasar.
- Si falta una opción o tiene un valor que no sirve, usa el valor por defecto; el volumen se limita a
  0–100.

## 9. Idiomas

Las insignias están en 54 idiomas. La ventana de opciones y los avisos, completos en español, inglés,
portugués (de Brasil y de Portugal), catalán, gallego, francés, italiano y alemán; en los otros 45, los
textos nuevos de la 2.5.0 salen en inglés. Los botones Aceptar, Cancelar y Restaurar salen en el idioma
de Anki, y los de la barra de repaso conservan los textos de Anki.

## 10. Si algo falla

- Nunca abre la ventana de error de Anki. En su lugar muestra durante 5 segundos un aviso que dice qué
  dejó de funcionar, una sola vez por cada función y sesión de Anki: «ProFeedback no pudo mostrar la
  insignia.», «… pintar los botones.», «… reproducir el sonido.» o «… celebrar el final.», seguido de
  «Anki sigue funcionando. El detalle está en el registro del complemento.» (o «ProFeedback tuvo un
  problema.» si es otra cosa).
- Los tropiezos con los sonidos, con los archivos o con la decisión de qué celebrar no avisan: no se oye
  o no se celebra, y el detalle queda en el registro del complemento.
- Si el equipo no tiene el módulo de sonido de Qt (pasa en algunas instalaciones de Linux), usa el
  reproductor de Anki: entonces el volumen no se aplica y el audio de una tarjeta puede cortar el sonido.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su colección: ni tarjetas, ni notas, ni repasos, ni fechas.
- No suena con «Mostrar respuesta», «Editar» ni «Más».
- No premia la nota que uno se pone: ningún sonido ni celebración depende de no pulsar «Otra vez».
- No celebra si sale del repaso por otra pantalla que no sea la del mazo.
- No pone insignias en las vistas previas ni en el editor de tarjetas.
- No deja que las tarjetas lean archivos suyos: su estilo y su código van dentro de la propia página.
- No añade menús ni atajos.
