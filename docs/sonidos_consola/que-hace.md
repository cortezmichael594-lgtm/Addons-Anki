# Qué hace «Sonidos de consola»

Versión 1.0.1 · 2026-11-13

Pone sonidos de consola, al estilo de la PS3, a lo que usted hace en Anki: abrirlo, moverse por los
menús, cancelar o cerrar, recibir un globo de notificación, comenzar a estudiar, sincronizar y ver un
error. Usa solo los siete sonidos que usted copia en su carpeta de sonidos. El complemento no trae
sonidos propios. No toca su colección: no lee ni cambia tarjetas, notas ni mazos.

## 1. Dónde aparece

- En el menú Herramientas, al final: «Sonidos de consola…». Abre la ventana de opciones.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre la misma ventana,
  no el editor de texto que Anki muestra con otros complementos.
- No añade botones, barras ni dibujos a ninguna pantalla de Anki. Todo lo demás es sonido.

## 2. Cuándo suena cada sonido

| Sonido (archivo) | Cuándo suena |
|---|---|
| coldboot_stereo.wav | Al abrir Anki, en cuanto se abre su perfil. Si tiene varios perfiles, también al cambiar de perfil. |
| gameboot_stereo.wav | Cada vez que aparece un globo de notificación de Anki (el recuadro breve abajo de la ventana), por ejemplo «Sincronización completa», el aviso al añadir una tarjeta o «Sonidos de consola: opciones guardadas.». |
| snd_option.wav | Navegación por los menús: al pasar de una opción a otra en cualquier menú de Anki (barra de menús Archivo, Editar, Herramientas, Ayuda; menús de Explorar y de otras ventanas; menús del botón derecho), con el ratón o con las flechas del teclado. También al pasar el ratón por los títulos de la barra de menús. Según la opción elegida, puede sonar solo al hacer clic, o nunca (apartado 4). |
| snd_cancel.wav | Al cancelar o cerrar: cerrar un menú sin elegir nada (con Esc o haciendo clic fuera, o pulsando otra vez su título en la barra); pulsar Esc, «Cancelar», «Cerrar» o «No» en una ventana; pulsar la X (o Alt+F4) de cualquier ventana salvo la principal; y salir del estudio a mitad (volver a Mazos, pulsar otro mazo, etc.). |
| snd_system_ok.wav | Al terminar bien una sincronización pulsada a mano (botón Sincronizar) y al pulsar «Sí» o «Aceptar» en una pregunta de Anki que tenga más de un botón. |
| snd_system_ng.wav | Al comenzar a estudiar: «Comenzar a estudiar» en la pantalla de un mazo, o su atajo de teclado. Volver al estudio tras un refresco de Anki no cuenta. |
| snd_error.wav | Cuando Anki muestra una ventana de error o de aviso (las del triángulo amarillo o el círculo rojo), incluida la de una sincronización fallida. |

Lo que no suena, a propósito:
- Responder una tarjeta («Otra vez», «Difícil», «Bien», «Fácil»): en silencio, para no oír un sonido en
  cada tarjeta.
- Terminar todas las tarjetas del mazo: Anki le lleva a la pantalla de felicitación sin sonido de
  cancelar, porque no ha cancelado nada.
- Aceptar una ventana con «Aceptar» cuando es solo informativa (un único botón).
- Las ventanas que Anki abre y cierra por su cuenta, como las de progreso («Sincronizando…»,
  «Comprobando…»): solo cuenta como cancelar lo que usted cierra con el teclado o el ratón.
- Cerrar Anki con la X de la ventana principal.
- La lista de mazos, la pantalla de un mazo y la de estudio por dentro: no son menús, sino páginas, y
  pasar el ratón por ellas no suena.
- La sincronización automática al abrir o cerrar Anki no hace sonar snd_system_ok; si falla y Anki
  muestra el aviso, sí suena snd_error.

## 3. Para que los sonidos no se pisen

- Cada sonido tiene un único «altavoz» propio. Si vuelve a sonar antes de acabar, se corta y empieza de
  nuevo, como el cursor de la PS3. Nunca se amontonan copias del mismo sonido.
- Navegación: como mucho un tic cada 60 milésimas de segundo. Si pasa el ratón muy rápido por un menú,
  se oye un tic seguido, no un ruido. Pasar el ratón dentro de la misma opción no repite el tic, y las
  líneas separadoras no suenan.
- Cancelar, error, «Sí/Aceptar» y comenzar a estudiar tienen prioridad: al empezar, callan la
  navegación y el globo de notificación que estuvieran sonando, y durante un cuarto de segundo la
  navegación no suena para no taparlos.
- Si un mismo sonido con prioridad llega dos veces casi a la vez (por ejemplo, la X de una ventana
  avisa al cerrarse y al cancelarse), suena una sola vez.
- El sonido de arranque es largo (unos 10 segundos). Los demás sonidos pueden sonar a la vez que él.
- Los sonidos no usan el reproductor de audio de las tarjetas: nunca cortan ni retrasan el audio de sus
  tarjetas, ni al revés.
- Los sonidos se cargan en memoria al abrir el perfil: suenan al instante y Anki no espera al disco.

## 4. Ventana de opciones

Es el mismo panel que el resto de sus complementos (el modelo de GritMap): una página dentro de una
ventana de Anki, con recuadros y los botones Aceptar y Cancelar abajo. Título: «Sonidos de consola»,
sin botón de ayuda. Ancho de 560 px y alto justo para el contenido (como mucho 720 px o el alto de la
pantalla menos 80); si no cabe, solo se desplaza el centro y el pie queda fijo. No se enseña hasta
estar dibujada entera, así que no parpadea. De arriba abajo:

1. Recuadro sin título, con el enlace «Restaurar valores predeterminados» (el texto de Anki en su
   idioma) arriba a la derecha:
   - «Volumen»: barra deslizante de 0 a 100 con la cifra al lado en seminegrita («70 %»). Por
     defecto, 70 %. Debajo, en gris: «Vale para los siete sonidos. Pruébelo con «Probar», más abajo;
     se guarda al aceptar.». El volumen sigue el oído: la mitad de la barra suena como la mitad de
     fuerte, no casi igual que el máximo. Se suma al volumen de Windows: con Windows en silencio no se
     oye nada.
2. Recuadro «Cuándo suena cada sonido», también con «Restaurar valores predeterminados». Nota gris:
   «Debajo de cada casilla, el archivo que usa. Desmarcada, ese sonido no suena.». Siete casillas, todas
   marcadas por defecto: «Al abrir Anki», «Globo de notificación», «Navegación por los menús»,
   «Cancelar, cerrar o salir del estudio», «Sincronización correcta o «Sí» en una pregunta», «Al
   comenzar a estudiar» y «Error o aviso de Anki». Debajo de cada una, en gris, el archivo que usa
   («snd_cancel.wav») o, si no está en la carpeta, «Falta snd_cancel.wav: no sonará.».
   - De «Navegación por los menús» cuelga, con una raya vertical a la izquierda, la lista desplegable
     «Cuándo suena»: «Al pasar el ratón o las flechas por las opciones» (por defecto, como el cursor
     de la PS3), «Solo al hacer clic» (al elegir una opción de un menú o hacer clic en un título de la
     barra) o «Nunca». Si la casilla está desmarcada, la lista se ve apagada y no se puede tocar; su
     valor se conserva.
3. Recuadro «Archivos de sonido». Nota gris con lo que falta: «Están los siete sonidos.», «Falta 1
   sonido: cópielo en la carpeta de sonidos.» o «Faltan 3 sonidos: cópielos en la carpeta de
   sonidos.».
   - «Probar un sonido»: lista desplegable con los sonidos que hay en la carpeta, escritos como «Al
     abrir Anki (coldboot_stereo.wav)», y al lado el botón «Probar». Suena al momento con el volumen
     que marque la barra en ese instante (aunque aún no haya pulsado Aceptar) y aunque su casilla esté
     desmarcada. Sin ningún sonido en la carpeta, la lista y el botón se ven apagados y debajo dice
     «Aún no hay ningún sonido en la carpeta.».
   - Botón «Abrir carpeta de sonidos»: abre en el Explorador de Windows la carpeta donde se copian los
     siete archivos (si no existía, la crea).
   - Si el ordenador no ofrece a Anki la función de sonido que usa el complemento, arriba del recuadro
     aparece una franja gris con un icono de información: «Este ordenador no ofrece a Anki la función
     de sonido que usa el complemento: no sonará nada.».
4. Pie: «Aceptar» (el único botón relleno, del azul de acción) y «Cancelar». Aceptar guarda y muestra
   el globo «Sonidos de consola: opciones guardadas.». Cancelar, Esc o la X cierran sin guardar.

Además:
- «Restaurar valores predeterminados» vuelve a lo de serie solo ese recuadro y deja al lado un enlace
  «Deshacer»; nada se guarda hasta Aceptar.
- La ventana recuerda su tamaño y su posición.
- Si ya está abierta y vuelve a pedirla, se trae al frente en lugar de abrir otra.
- Bloquea solo la ventana desde la que se abrió (la principal o la de Complementos), no todo Anki.
- Al cerrarla (con Aceptar o con Cancelar), el complemento vuelve a mirar la carpeta: los archivos
  copiados con la ventana abierta empiezan a sonar sin reiniciar Anki. Un archivo sustituido por otro
  con el mismo nombre también se recarga. La lista de la ventana se pone al día la próxima vez que se
  abra.

## 5. Colores y aspecto

Todos los colores salen de la paleta de Anki (Nocturne) y cambian con el modo día o noche y, si está
instalado, con Atelier. Nada de colores inventados:

| Uso | Día | Noche |
|---|---|---|
| Fondo de la ventana | #F7F8FA | #12161F |
| Recuadros y fondo de los controles | #FBFCFE | #212836 |
| Carril de la barra de volumen, franja de aviso | #EEF0F4 | #0F131B |
| Texto | #1B2430 | #D6DAE1 |
| Texto secundario (notas, archivos, «Falta…») | #4E576A | #B7BECC |
| Borde de los recuadros | #E8EAF0 | #1F2635 |
| Borde de los controles | #878C97 | #727B8C |
| Azul de acción: «Aceptar», casillas marcadas, relleno de la barra | #3B6FE0 | #4066E6 |
| Enlaces («Restaurar valores predeterminados», «Deshacer») | #2F63D8 | #A3C1F7 |
| Texto apagado (lista de navegación con su casilla desmarcada) | #A9AFBC | #7C869A |
| Foco del teclado | #3B6FE0 | #6390FF |
| Fondo al pasar el ratón | #EDF0F5 | #2E3747 |

- Letra de Anki (en Windows, Segoe UI Variable): título de 14 px en negrita, títulos de recuadro de 14
  px en seminegrita, texto de 12 px, etiquetas y casillas en seminegrita.
- Recuadros con esquinas de 10 px y borde fino, sombra mínima de día y ninguna de noche; controles de
  32 px de alto con esquinas de 8 px; casillas de 18 px con esquinas de 4 px.
- Sin animaciones, salvo un hundimiento de 1 px al pulsar un botón.
- El globo de notificación es el de Anki, sin cambios. Fuera de su ventana, el complemento no cambia el
  aspecto de nada.

## 6. Accesibilidad

- Todo se maneja con el teclado: el tabulador recorre la ventana en orden visual (volumen, cada casilla,
  la lista «Cuándo suena», la lista de prueba, «Probar», «Abrir carpeta de sonidos», Aceptar,
  Cancelar). Espacio marca o desmarca una casilla; Intro pulsa el botón que tiene el foco y nunca
  acepta la ventana por su cuenta; Esc cancela. Al abrirse, el foco está en el volumen.
- La barra de volumen se mueve con las flechas de uno en uno, y con Inicio y Fin.
- El foco del teclado se ve como un contorno azul de 2 px, solo al usar el teclado.
- Toda la fila de una casilla se puede pulsar, no solo el cuadro.
- Lector de pantalla (Narrador de Windows): cada control tiene nombre; la barra anuncia su cifra con
  la unidad («70 %»); cada recuadro se anuncia con su título; «Restaurar» y «Deshacer» se dicen en voz
  alta.
- Contraste: texto a 4,5 a 1 o más, bordes de controles a 3 a 1 o más.
- Con el contraste alto de Windows, cada control conserva un borde real y el foco usa el resaltado del
  sistema.
- Ninguna información depende solo del color: lo que falta se dice con texto («Falta…»).
- Ninguna información depende solo del sonido: todo lo que suena (un error, un aviso, el fin de una
  sincronización) Anki lo sigue mostrando en pantalla igual que sin el complemento. Quien no oiga, o
  tenga los sonidos apagados, no pierde nada.
- Para quien prefiera menos estímulos: cada sonido se apaga por separado, la navegación tiene la opción
  «Nunca» y el volumen puede bajar a 0.

## 7. La carpeta de sonidos

- Es la carpeta «user_files» del complemento (la abre el botón «Abrir carpeta de sonidos»). Ahí se
  copian los siete archivos con su nombre exacto: coldboot_stereo.wav, gameboot_stereo.wav,
  snd_cancel.wav, snd_error.wav, snd_option.wav, snd_system_ng.wav y snd_system_ok.wav. Trae un
  LEEME.txt que lo explica.
- Anki conserva esa carpeta al actualizar el complemento: no hay que volver a copiarlos.
- Los archivos deben ser .wav sin comprimir (los habituales). Si uno no se puede reproducir, ese sonido
  no suena y queda anotado en el registro del complemento; los demás siguen sonando.
- Si falta un archivo, ese sonido no suena, sin avisos.
- Los sonidos no se incluyen en el complemento ni en el repositorio: los pone usted.

## 8. Qué guarda y dónde

- El volumen, el modo de navegación y las siete casillas, en la configuración de complementos de Anki
  de ese ordenador: valen para todos los perfiles y no viajan con la sincronización.
- Si falta una opción o tiene un valor que no sirve (por ejemplo, de una versión anterior), usa el
  valor por defecto; un volumen fuera de 0-100 se recorta.

## 9. Idiomas

Sus textos están solo en español, sea cual sea el idioma de Anki. Los botones estándar (Aceptar,
Cancelar) salen en el idioma de Anki.

## 10. Si algo falla

- Nunca abre la ventana de error de Anki. Si falla una función (por ejemplo, la ventana de opciones),
  muestra durante 5 segundos «Sonidos de consola tuvo un problema. Anki sigue funcionando; el detalle
  quedó en su registro.», una sola vez por función y sesión.
- Si falla la vigilancia de menús y ventanas, se desactiva sola hasta reiniciar Anki: dejan de sonar la
  navegación, cancelar, los globos, los avisos y el «Sí», sin aviso en pantalla; el resto sigue. El
  detalle queda en el registro.
- Si el ordenador no ofrece a Anki la función de sonido que usa el complemento, la ventana lo dice:
  «Este ordenador no ofrece a Anki la función de sonido que usa el complemento: no sonará nada.»

## 11. Qué no hace

- No incluye sonidos propios ni añade otros que los siete suyos.
- No suena al responder tarjetas ni al pasar el ratón por la lista de mazos o las páginas de Anki.
- No cambia el sonido ni el audio de sus tarjetas.
- No se conecta a internet.
- No lee ni cambia su colección.
