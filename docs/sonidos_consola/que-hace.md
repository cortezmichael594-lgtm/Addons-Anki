# Qué hace «Sonidos de consola»

Versión 1.0.0 · 2026-11-13

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

Título: «Sonidos de consola». No tiene botón de ayuda. De arriba abajo:

1. «Volumen:»: una barra horizontal de 0 a 100, con marcas cada 10 y la cifra al lado («70 %»). Por
   defecto, 70 %. El volumen sigue el oído: la mitad de la barra suena como la mitad de fuerte, no casi
   igual que el máximo. Al soltar la barra suena el tic de navegación con el volumen nuevo; con el
   teclado, suena en cada paso. El volumen vale para los siete sonidos y se suma al del sistema: con el
   de Windows en silencio no se oye nada.
2. «Navegación en los menús:»: una lista desplegable con tres opciones:
   - «Al pasar el ratón o las flechas por las opciones» (por defecto): el tic suena al resaltarse cada
     opción, como el cursor de la PS3.
   - «Solo al hacer clic»: el tic suena al elegir una opción de un menú o al hacer clic en un título de
     la barra de menús.
   - «Nunca»: la navegación no suena. Los demás sonidos siguen.
3. Recuadro «Sonidos», con una fila por sonido:
   - Una casilla con el momento en que suena: «Al abrir Anki», «Globo de notificación», «Navegación por
     los menús», «Cancelar, cerrar o salir del estudio», «Sincronización correcta o «Sí» en una
     pregunta», «Al comenzar a estudiar» y «Error o aviso de Anki». Todas marcadas por defecto.
     Desmarcada, ese sonido no suena nunca.
   - El nombre del archivo que usa. Si no está en la carpeta, en su lugar dice «Falta
     snd_cancel.wav» (con el nombre que corresponda), con el texto atenuado.
   - Un botón «Probar», que lo hace sonar al momento con el volumen que marque la barra, aunque la
     casilla esté desmarcada. Atenuado e inactivo si falta el archivo.
4. Una frase con lo que falta: «Están los siete sonidos.», «Falta 1 sonido: cópielo en la carpeta de
   sonidos.» o «Faltan 3 sonidos: cópielos en la carpeta de sonidos.».
5. Botón «Abrir carpeta de sonidos»: abre en el Explorador de Windows la carpeta donde se copian los
   siete archivos. Si no existía, la crea. Al pasar el ratón explica: «Copie ahí sus siete archivos
   .wav con su nombre exacto. Se conservan al actualizar el complemento.».
6. Botones «Aceptar» y «Cancelar». Aceptar guarda y muestra el globo «Sonidos de consola: opciones
   guardadas.». Cancelar, Esc o la X cierran sin guardar. Los cambios de la barra y de las casillas
   solo valen desde que se pulsa Aceptar; mientras tanto, solo los usan los botones «Probar».

Además:
- La ventana recuerda su tamaño y su posición.
- Si ya está abierta y vuelve a pedirla, se trae al frente en lugar de abrir otra.
- Bloquea solo la ventana desde la que se abrió (la principal o la de Complementos), no todo Anki.
- Al cerrarla, el complemento vuelve a mirar la carpeta: los archivos copiados con la ventana abierta
  empiezan a sonar sin reiniciar Anki. Un archivo sustituido por otro con el mismo nombre también se
  recarga.

## 5. Colores y aspecto

- El complemento no define ningún color, tipo de letra ni dibujo propio. La ventana usa solo los
  controles estándar de Anki (barra, lista desplegable, casillas, botones, recuadro con título) y toma
  sus colores del tema activo de Anki: claro, oscuro o, si está instalado, Nocturne.
- El único cambio de aspecto es el atenuado (gris del tema) del nombre de un archivo que falta y de su
  botón «Probar». No depende solo del color: el texto dice «Falta» y el botón queda inactivo.
- El globo de notificación es el de Anki, sin cambios.
- No hay animaciones.

## 6. Accesibilidad

- Todo se maneja con el teclado: el tabulador recorre la ventana en orden (volumen, navegación, cada
  casilla y su botón «Probar», «Abrir carpeta de sonidos», Aceptar, Cancelar). Intro acepta y Esc
  cancela. Los botones «Probar» y «Abrir carpeta de sonidos» no se activan con Intro por accidente.
- Atajos con Alt: Alt+V lleva a la barra de volumen, Alt+N a la lista de navegación y Alt+S pulsa
  «Abrir carpeta de sonidos».
- La barra de volumen se mueve con las flechas (de 5 en 5), con RePág y AvPág (de 10 en 10) y con
  Inicio y Fin (0 y 100). Cada paso suena con el volumen nuevo, así que se ajusta de oído.
- Cada control tiene su etiqueta asociada y un nombre para lectores de pantalla (Narrador de Windows):
  la barra se lee «Volumen de los sonidos» y cada botón, por ejemplo, «Probar el sonido «Al abrir
  Anki»».
- La cifra del volumen se ve escrita junto a la barra, no solo por la posición.
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
