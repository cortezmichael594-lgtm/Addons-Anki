# Qué hace «Always on Top»

Versión 1.2 · 2026-10-21

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
  plantillas, editor y las de cortar, copiar, pegar y guardar), y además mira los atajos que tienen
  en ese momento los menús de la ventana principal, incluidos los que añadan otros complementos.
- Es una sola combinación: no admite secuencias de dos pulsaciones seguidas.
- Al abrir Anki, si el atajo guardado no sirve (está vacío, no se entiende, no lleva Ctrl ni Alt o
  está en la lista fija de Anki), usa Ctrl+Mayús+O sin avisar. Esto vale también para un atajo
  guardado por una versión anterior del complemento.

## 4. Ventana de opciones

- Título «Always on Top», sin botón de ayuda. Aparece sobre la ventana que estuviera delante
  (normalmente, la lista de complementos) y, mientras está abierta, el resto de Anki espera.
- Una sola línea: «Atajo:» y una casilla con el atajo actual, escrito con los nombres de teclas del
  idioma de Anki (en español, «Control+Mayúsculas+O»). La casilla tiene el cursor puesto al abrir y
  una pequeña cruz para vaciarla; vacía, muestra en gris «Presione el atajo de teclado».
- Para cambiar el atajo, pulse la combinación nueva con el cursor en la casilla: la casilla graba la
  siguiente combinación que pulse, sea cual sea. Por eso, con el cursor en la casilla, Intro y Esc no
  aceptan ni cierran la ventana: se graban como atajo («Retorno», «Escape») y después se rechazan al
  aceptar, por no llevar Ctrl ni Alt. Para aceptar o cancelar, use los botones.
- Tres botones estándar, con los textos de Qt en el idioma de Anki: «Restaurar los valores
  predeterminados», «Aceptar» y «Cancelar».
- «Restaurar los valores predeterminados» pone Ctrl+Mayús+O en la casilla y muestra el aviso breve de
  Anki «Se restauró la configuración predeterminada», pero no guarda nada hasta que pulse «Aceptar».
- «Aceptar»:
  - Con la casilla vacía, guarda Ctrl+Mayús+O. No hay manera de dejar el complemento sin atajo.
  - Si la combinación no sirve (no lleva Ctrl ni Alt, o Anki ya la usa), abre una ventana de aviso
    titulada «Always on Top» con el texto «No se puede usar «Control+Q». Elige una combinación que
    incluya Ctrl o Alt y que Anki no use ya.» (con la combinación escrita como en la casilla). La
    ventana de opciones sigue abierta, con el cursor en la casilla, hasta que elija otra o cancele.
  - Si sirve y es distinta de la guardada, la guarda y funciona al momento, sin reiniciar Anki; la
    anterior deja de funcionar. No muestra ningún aviso de confirmación.
- «Cancelar» o la cruz de la ventana la cierran sin guardar nada.
- No recuerda su tamaño ni su posición.

## 5. Mensajes

Todos los textos que puede ver, en español:

- «Siempre visible: activado» y «Siempre visible: desactivado»: aviso breve al pulsar el atajo.
- «Atajo:» y «Presione el atajo de teclado»: en la ventana de opciones.
- «No se puede usar «…». Elige una combinación que incluya Ctrl o Alt y que Anki no use ya.»: ventana
  de aviso al aceptar una combinación que no sirve.
- «Se restauró la configuración predeterminada»: aviso breve de Anki al restaurar.
- «Always on Top: Se produjo un problema»: si algo falla (apartado 9).
- El complemento trae también el texto «Atajo de teclado actualizado», pero en la práctica no se
  muestra nunca: solo saldría al guardar desde el editor de texto de la configuración de Anki, que
  este complemento sustituye por su propia ventana de opciones.

## 6. Idiomas

- Sus textos están en 60 idiomas, entre ellos todos los que ofrece Anki; si el de Anki no está, salen
  en inglés. Distingue el portugués de Brasil del de Portugal y el chino simplificado del
  tradicional.
- Mira el idioma de Anki cada vez que muestra un texto.
- Los botones de la ventana de opciones, los nombres de las teclas y el aviso de restaurar usan los
  textos de Qt y de Anki en el idioma de Anki.
- En español, el aviso de combinación no válida trata de tú («Elige»), mientras que el resto trata de
  usted («Presione»).

## 7. Límites y casos raros

- La lista fija de atajos de Anki viene de Anki 25.09 y le faltan seis del editor de Anki 26.09.3
  (listas, sangría, superíndice y subíndice): la ventana de opciones los acepta, y entonces dentro de
  Añadir esa combinación enciende o apaga «siempre visible» en lugar de hacer su trabajo en el
  editor. Está anotado en el registro de errores, en «Pendientes».
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
