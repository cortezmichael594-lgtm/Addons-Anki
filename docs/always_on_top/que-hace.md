# Qué hace «Always on Top»

Versión 1.3 · 2026-11-09

Mantiene la ventana Añadir de Anki por encima de todas las demás ventanas del ordenador, también de
las de otros programas, para que pueda copiar de un documento o de una página web sin que Añadir
quede tapada. Se enciende y se apaga con un atajo de teclado, Ctrl+Mayús+O por defecto, que se puede
cambiar en su ventana de opciones. No toca su colección: no lee ni cambia tarjetas, notas ni
repasos. Lo único que guarda es el atajo.

## 1. Dónde aparece

- No añade menús, botones ni iconos. Se usa solo con su atajo de teclado.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones (apartado 4), no el editor de texto que Anki muestra con otros complementos.
- El efecto solo se aplica a la ventana Añadir, tanto a la normal como a la otra versión que Anki
  abre si se pulsa Añadir con Mayús. No afecta a la ventana principal, al repaso, a Explorar, a
  Editar ni a las estadísticas.

## 2. Encender y apagar «siempre visible»

- Cada pulsación del atajo cambia el estado: la primera lo enciende, la siguiente lo apaga, y así
  sucesivamente.
- Cada vez muestra un aviso breve, durante un segundo y medio, abajo a la izquierda de la ventana de
  Anki que esté delante: «Siempre visible: activado» o «Siempre visible: desactivado».
- El atajo responde en cualquier ventana de Anki que esté delante (la principal, el repaso, Explorar
  o la propia Añadir), no solo en Añadir. Si lo que está delante es otro programa, no responde: hay
  que volver antes a una ventana de Anki.
- Si Añadir está abierta, el cambio se ve al momento. Si no lo está, el aviso sale igual y el estado
  se queda puesto para la próxima vez: con «activado», Añadir aparecerá ya por encima de todo.
- Con el efecto encendido, Añadir sigue por encima aunque usted pase a otro programa. Si la cierra y
  la vuelve a abrir, sigue encendido.
- El estado dura mientras Anki esté abierto, también si cambia de perfil. Al cerrar Anki se olvida:
  cada vez que abre Anki empieza apagado.
- En Windows, con Añadir ya a la vista, el cambio se hace sin que la ventana parpadee, se mueva ni
  pierda el foco.
- Al abrir Añadir con el efecto ya encendido, se aplica antes de que la ventana aparezca, así que
  tampoco parpadea.

## 3. El atajo de teclado

- Por defecto, Ctrl+Mayús+O. Anki 26.09.3 no usa esa combinación.
- Solo admite una combinación que lleve Ctrl o Alt y que Anki no use ya. Para saber cuáles usa Anki,
  el complemento tiene una lista fija, sacada del código de Anki 25.09 (menús, repaso, Explorar,
  plantillas, editor y las de cortar, copiar, pegar y guardar) y completada en la 1.3 con los seis
  atajos del editor de Anki 26.09.3 que faltaban (listas, sangría, superíndice y subíndice), y además mira los atajos que tienen
  en ese momento los menús de la ventana principal, incluidos los que añadan otros complementos.
- Es una sola combinación: no admite secuencias de dos pulsaciones seguidas.
- Al abrir Anki, si el atajo guardado no sirve (está vacío, no se entiende, no lleva Ctrl ni Alt o
  está en la lista fija de Anki), usa Ctrl+Mayús+O sin avisar. Esto vale también para un atajo
  guardado por una versión anterior del complemento.

## 4. Ventana de opciones

Título «Always on Top».
Desde la 1.3 sigue el modelo de ventana de opciones del taller, el panel de GritMap (regla
PROP-012, petición del 2026-11-09): un panel de 560 px de ancho y el alto justo para su contenido,
hecho de recuadros sobre el fondo de Anki, con los colores de la paleta (también con Atelier) y
Aceptar y Cancelar abajo (en Windows, Aceptar primero). No se enseña hasta estar dibujado, recuerda
su tamaño y su posición, y si ya está abierto se trae al frente. Esc cancela y Ctrl+Intro acepta.
Nada se guarda hasta pulsar Aceptar. Aceptar, Cancelar y Restaurar llevan el texto de Qt en el
idioma de Anki. Con el teclado: el tabulador recorre los controles, cada uno con su contorno de foco
azul; el lector de pantalla anuncia el nombre de cada control.

Un solo recuadro, con «Restaurar los valores predeterminados» arriba a la derecha (tras usarlo,
«Deshacer» al lado), y dentro el campo «Atajo» (sin los dos puntos de antes) con el atajo actual y el
foco puesto al abrir. Vacío, muestra en gris «Presione el atajo de teclado».

- El campo del atajo graba la combinación que se pulse con el foco en él (no hace falta escribir
  nada). El tabulador y Mayús+Tab siguen moviendo el foco y Esc sigue cerrando la ventana, así que esas
  tres no se pueden grabar; Retroceso o Supr solos vacían el campo, igual que la pequeña cruz de al
  lado (que se llama «Eliminar» para el lector de pantalla). La combinación se ve escrita con los
  nombres de teclas del sistema y del idioma de Anki.
  Hasta la 1.2, Intro y Esc se grababan como atajo y había que usar los botones; ya no.
- «Restaurar» pone Ctrl+Mayús+O en el campo, sin guardar nada hasta Aceptar.
- «Aceptar»:
  - Con el campo vacío, guarda Ctrl+Mayús+O. No hay manera de dejar el complemento sin atajo.
  - Si la combinación no sirve (no lleva Ctrl ni Alt, o Anki ya la usa), el aviso «No se puede usar
    «Control+Q». Elige una combinación que incluya Ctrl o Alt y que Anki no use ya.» sale en rojo
    encima del campo, que se marca con borde rojo, y la ventana sigue abierta con el foco en él
    (hasta la 1.2 salía una ventana de aviso aparte).
  - Si sirve y es distinta de la guardada, la guarda y funciona al momento, sin reiniciar Anki; la
    anterior deja de funcionar. No muestra ningún aviso de confirmación.
- «Cancelar», Esc o la cruz de la ventana la cierran sin guardar nada.

## 5. Mensajes

Todos los textos que puede ver, en español:

- «Siempre visible: activado» y «Siempre visible: desactivado»: aviso breve al pulsar el atajo.
- «Atajo» y «Presione el atajo de teclado»: en la ventana de opciones.
- «No se puede usar «…». Elige una combinación que incluya Ctrl o Alt y que Anki no use ya.»: aviso
  en rojo encima del campo al aceptar una combinación que no sirve.
- «Restaurar los valores predeterminados» y «Deshacer»: enlaces del recuadro de la ventana de
  opciones (desde la 1.3 ya no sale el aviso breve «Se restauró la configuración predeterminada»).
- «Always on Top: Se produjo un problema»: si algo falla (apartado 9).
- El complemento trae también el texto «Atajo de teclado actualizado», pero en la práctica no se
  muestra nunca: solo saldría al guardar desde el editor de texto de la configuración de Anki, que
  este complemento sustituye por su propia ventana de opciones.

## 6. Idiomas

- Sus textos están en 60 idiomas, entre ellos todos los que ofrece Anki; si el de Anki no está, salen
  en inglés. Distingue el portugués de Brasil del de Portugal y el chino simplificado del
  tradicional.
- Mira el idioma de Anki cada vez que muestra un texto.
- Los botones de la ventana de opciones, «Deshacer», «Eliminar» y los nombres de las teclas usan los
  textos de Qt y de Anki en el idioma de Anki.
- En español, el aviso de combinación no válida trata de tú («Elige»), mientras que el resto trata de
  usted («Presione»).

## 7. Límites y casos raros

- Si tiene abiertas a la vez las dos versiones de la ventana Añadir, el atajo solo cambia la última
  que se abrió. También está en «Pendientes».
- Si otro complemento usa la misma combinación en una ventana distinta de la principal, el
  complemento no lo detecta, y los dos atajos se pelean por la misma tecla con un resultado
  imprevisible.
- En Mac y Linux, o si la vía propia de Windows fallara, cambiar el estado con Añadir a la vista hace
  que la ventana desaparezca un instante y vuelva a aparecer en el mismo sitio y con el mismo tamaño;
  si era la ventana activa, recupera el foco.
- Con Añadir minimizada, el cambio se aplica igual y se nota al restaurarla desde la barra de
  tareas.

## 8. Qué guarda y dónde

- Solo el atajo, en la configuración de complementos de Anki de este ordenador: vale para todos los
  perfiles y no viaja con la sincronización.
- Al guardar el atajo conserva cualquier otro dato que hubiera en esa configuración, por si una
  versión futura añade opciones.
- El estado encendido o apagado no se guarda en ningún sitio.
- No guarda nada en su colección.

## 9. Si algo falla

- Nunca abre la ventana de error de Anki. En su lugar muestra durante un segundo y medio el aviso
  «Always on Top: Se produjo un problema», una sola vez por cada función y sesión, para no llenar la
  pantalla si el fallo se repite. Anki sigue funcionando.
- El detalle técnico queda en el registro del complemento: un archivo de texto en la carpeta de
  registros de Anki, que conserva los de los últimos 10 días.
- Si la vía propia de Windows falla, usa la general (con el parpadeo del apartado 7).
- Si la ventana Añadir se cierra justo mientras se aplica el cambio, lo deja estar, sin aviso.

## 10. Qué no hace

- No se conecta a internet ni abre otros programas.
- No lee ni cambia su colección.
- No mantiene por encima ninguna otra ventana de Anki: ni la principal, ni Explorar, ni Editar.
- No recuerda, al volver a abrir Anki, si estaba encendido.
- No muestra en ningún sitio si está encendido, salvo el aviso breve al pulsar el atajo.
