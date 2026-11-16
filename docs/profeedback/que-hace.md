# Qué hace «ProFeedback»

Versión 2.5.0 · 2026-11-16

Hace más agradable el repaso: suena un sonido corto al acertar y otro, más discreto, al pulsar «Otra
vez»; pone una insignia encima de la tarjeta (tarjeta nueva, «se resiste» u «otra oportunidad»); da a
los botones de la barra inferior del repaso un aspecto de colores con relieve; y, al terminar un mazo o
todo lo del día, toca un sonido de fin y suelta confeti, dorado al terminar el día. Solo lee su
colección: nunca cambia tarjetas, notas ni repasos. Lo único que guarda son sus opciones.

La 2.5.0 aplica el informe «ProFeedback 2.4.0: auditoría y rediseño de la interfaz» (aprobado entero el
2026-11-16), con la opción recomendada en sus cuatro decisiones: el oro premia terminar el día y no la
nota que uno se pone, «Bien» más ancho, «SE RESISTE» y «OTRA OPORTUNIDAD», y confeti más corto.

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

- Colores: el icono conserva siempre el color del original (#CE82FF, #FF4B4B, #FFAB33). El texto, de
  noche, también; de día, el mismo tono más oscuro (#8F3BD9, #C92C2C, #9E5A00), para leerse sobre el
  fondo claro (5 a 1 o más).
- Encima de la tarjeta hay siempre una franja de 40 px (24 del icono y 16 de aire), haya insignia o no:
  la tarjeta empieza siempre en el mismo sitio y no salta de una a otra.
- Aparece con un fundido de 0,12 segundos; sin fundido si el sistema pide reducir las animaciones. No se
  puede pulsar ni seleccionar. Solo cuentan las respuestas dadas con un botón. La misma insignia sale en
  la pregunta y en la respuesta.
- Los dos textos nuevos están traducidos en los 54 idiomas.

## 4. Botones del repaso

Con la opción «Botones de colores con relieve» (marcada por defecto), los botones de la barra inferior
del repaso tienen el aspecto del ProFeedback original, con sus colores fijos, los mismos de día y de
noche:

- «Otra vez» rojo (#FF4B4B), «Difícil» naranja (#FFAB33), «Bien» verde (#93D333) y «Fácil» azul claro
  (#49C0F8), con la letra casi negra (#131F24) en negrita de 15 px.
- «Mostrar respuesta», dorado (#FFD700) con la letra ámbar oscura (#5C3700; desde la 2.5.0, antes
  #AE6802, que no se leía bien).
- Todos miden 50 px de alto: una cara de 46 y un canto de 4 px de su color más oscuro, con esquinas de
  16 px. 130 px de ancho como mínimo; «Bien» y «Mostrar respuesta», 190 px: así, tras pulsar «Mostrar
  respuesta», el puntero queda dentro de «Bien» y no en el hueco entre «Difícil» y «Bien».
- «Editar» y «Más», sin relleno: contorno de 2 px con canto de 4 px del gris de los controles de la paleta
  y letra en el gris secundario (de noche, 9,7 a 1; antes 3,0). Con el ratón encima, se rellenan del
  color de pasar el ratón de la paleta.
- Encima de la barra, una raya de 2 px del color de las rayas de la paleta.
- Los tiempos previstos y el recuento de tarjetas, en el color de texto de Anki.
- Al pasar el ratón por un botón de color, se aclara (brillo 1,08); nunca se oscurece. Mandan su forma y
  sus colores aunque Atelier (Nocturne) esté instalado (FIX-006).
- Al pulsarlo, la cara baja 4 px sobre su canto en 80 ms, sin cambiar de color, y vuelve en 70 ms al
  soltar, sin rebote. La respuesta sale en el instante en que se suelta el botón (antes había una espera
  de una décima de segundo); si se suelta fuera, no responde. Los atajos de teclado responden al
  instante. Un segundo clic en el mismo botón antes de 0,4 segundos se ignora. Con «reducir movimiento»,
  sin animación.
- Con el teclado, el botón elegido lleva un aro de foco azul de 2 px, separado 2 px del botón.
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
| Mazo | 5 respuestas en la sesión | Dos cañones desde las esquinas de abajo, 2,5 s como máximo; colores de la paleta |
| Día | 20 tarjetas distintas respondidas hoy en toda la colección | Lluvia dorada desde arriba, 4 s como máximo, y el título de la pantalla brilla en dorado una vez (3,6 s) |

- Desde la 2.5.0 ninguna celebración depende de las notas: el oro premia terminar el día. Antes, la
  dorada exigía no haber pulsado nunca «Otra vez» ni «Difícil», lo que empujaba a calificarse al alza.
- El título dorado es #FFD700 de noche y #8A5200 de día (se lee en los dos modos).
- El sonido de fin suena siempre que hay celebración, salvo con «Sin sonido». Sin el mínimo, solo
  suena: ni confeti ni brillo.
- «Hoy» empieza a la hora de cambio de día de Anki, y lo de hoy se lee del historial de Anki: cuenta cada
  perfil por separado e incluye lo repasado en otros dispositivos ya sincronizado.
- El confeti pasa por encima de todo sin tapar nada y se desvanece en sus últimos 0,4 s.
- Con «reducir movimiento» activado en el sistema no hay confeti; al terminar el día, el título queda
  dorado sin moverse.
- La decisión se toma sin congelar Anki.

## 6. Ventana de opciones

Título «ProFeedback» en la barra de la ventana (no se repite dentro). Sigue el modelo de ventana de
opciones del taller (el panel de GritMap): 560 px de ancho y el alto justo para su contenido (unos 545
px, sin barra de desplazamiento), recuadros sobre el fondo de Anki con los colores de la paleta, y
Aceptar y Cancelar abajo (en Windows, Aceptar primero). La ventana entera es invisible hasta que el
panel está dibujado y con su alto, y entonces aparece de una vez (FIX-005). Recuerda su tamaño y su
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
| | Confeti al terminar | Casilla | Marcada |

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
- Letra: si deja en «user_files» (o en la carpeta del complemento) un archivo «ProFeedback.ttf» o
  «Feather Bold.ttf» de 1,5 MB como máximo, los botones y las insignias usan esa letra. Si no hay
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
