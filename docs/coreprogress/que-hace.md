# Qué hace «CoreProgress»

Versión 1.5.0 · 2026-11-17

Barra de progreso en la parte de arriba de la pantalla de repaso: se va llenando a medida que despacha
lo que tenía hoy en el mazo que está estudiando, con marcas por el camino, el número del próximo hito y el total de hoy al final. Además cuenta sus
aciertos seguidos, los celebra con un aviso breve en ciertos números, vuelve dorada la barra a partir
de cinco, celebra la mejor racha de los últimos 30 días y guarda su récord personal. Solo lee su estudio: nunca cambia tarjetas, notas, repasos ni
fechas. Lo único que guarda son sus opciones y su récord.

La 1.2.0 aplicó entero el informe de interfaz, aprendizaje y hábito del 2026-11-09. La 1.3.0 aplica
entero el informe «Auditoría y rediseño de la interfaz: CoreProgress 1.2.0» del 2026-11-16, con la
opción recomendada en sus cuatro decisiones: mejor racha de 30 días, hitos en números redondos con el
total al final, relleno plano y sin la cabecera repetida en la ventana de opciones (véase «Así a
propósito» en el registro de errores). La 1.4.0 quita la barra llena y la línea de resumen de la
pantalla de «¡Enhorabuena!». La 1.5.0 aplica entero el informe «Rediseño de color y forma: CoreProgress
1.4.0» del 2026-11-17, con la opción recomendada en sus tres decisiones: barra de 720 px centrada,
hitos como cortes con número solo en el próximo y en el total, y estrella en la punta de la racha
dorada en lugar del halo. Cambian todos los colores de los temas (pesan igual, ninguno se parece al
azul de los botones y de noche brillan menos), el canal, el aviso (en una píldora), el movimiento y,
en la ventana de opciones, las muestras de tema, el grosor y la vista previa.

## 1. Dónde aparece

- En la pantalla de repaso (la que se abre al pulsar «Estudiar ahora»), también al repasar un mazo
  filtrado o un estudio personalizado.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No aparece en la lista de mazos, en la pantalla de un mazo (tampoco en la de «¡Enhorabuena!»), en Explorar
  (tampoco en su vista previa), en la pantalla de plantillas, en el editor ni en las estadísticas. No
  añade menús ni atajos de teclado.
- En la pantalla de repaso baja la estrella de nota marcada y la bandera de Anki para que queden
  justo debajo de la barra.

## 2. La barra

Qué mide:

- El 100 % es todo lo de hoy en ese mazo (con sus submazos): lo que ya salió hoy de la cola más lo que
  queda. Al entrar a repasar, CoreProgress lee en segundo plano qué tarjetas del mazo ya respondió hoy
  y no siguen en aprendizaje, y les suma las tres cifras que Anki muestra abajo (nuevas, en
  aprendizaje y para repasar). Si sale a la lista de mazos con la mitad hecha y vuelve, la barra
  empieza en el 50 %, con los hitos ya alcanzados marcados y sin salto ni chispas. Al cambiar el día
  de Anki (a las 4 de la mañana, de serie), vuelve a empezar de cero.
- Una tarjeta solo cuenta cuando sale de verdad de la cola: cuando se gradúa o cuando un repaso pasa a
  otro día. Una tarjeta fallada vuelve a aprendizaje y, mientras Anki la siga contando abajo, no hace
  avanzar la barra.
- Enterrar, suspender o apartar una tarjeta de hoy también hace avanzar la barra, porque sale de la
  cola.
- Se pone al día una vigésima de segundo después de cada respuesta y después de cualquier cambio que
  haga Anki (hasta la 1.4.0, una décima).
- La barra no retrocede: si la cuenta de Anki sube durante el repaso (porque vencen tarjetas en
  aprendizaje que al empezar todavía no contaban), se queda quieta hasta que el avance la alcance.
  Solo retrocede al deshacer una respuesta. Al terminar, lo que queda es cero y llega al 100 %.
- En un mazo filtrado, las tarjetas que al responderlas vuelven a su mazo de origen dejan de contarse
  como hechas en ese filtrado si sale y vuelve a entrar.

Aspecto:

- Queda fija arriba, centrada sobre la tarjeta: mide como mucho 720 px, el ancho de la tarjeta de
  Atelier, y en una ventana más estrecha ocupa el ancho menos 18 px a cada lado; 10 px por arriba
  (desde la 1.5.0; antes iba de lado a lado y la punta quedaba lejos del texto). Va por encima de la
  tarjeta y no se mueve al bajar por una tarjeta larga. Los clics la atraviesan.
- La tarjeta deja siempre sitio a la barra y a su aviso: 10 px de margen, el alto de la barra, 24 px
  para el aviso de racha (solo con «Celebrar rachas y récords» marcada) y 8 px de aire: 58 px con la
  barra de serie, 34 sin celebraciones. «Espacio extra» se suma a ese mínimo. Hasta la 1.1.0, con el
  valor de serie la barra tapaba la parte alta de la tarjeta (FIX-004).
- Grosor: Fina (12 px), Normal (16, de serie) o Gruesa (20). Canal, relleno, discos y aviso tienen
  forma de píldora (esquinas redondeadas del todo).
- El canal (la parte vacía) es gris y plano, sin sombra (1.5.0): sobre el fondo de tarjeta de Atelier,
  el gris de la paleta (#D5D9E2 de día y #272F3F de noche); sobre otro fondo, un gris con el mismo
  contraste respecto a ese fondo, medido en pantalla. Hasta tener esa medida la barra no se enseña
  (como mucho, algo más de medio segundo). Quien edite plantillas de tarjeta puede fijar desde la
  plantilla el color del canal.
- El relleno es un degradado de tres tonos del tema elegido, plano y sin contorno (1.5.0): los seis
  temas pesan igual, porque cada tono está calculado por contraste. De día, la punta queda a 3,1 a 1
  del canal; de noche, a 7,0. Siempre es al menos tan ancho como alto, también con 0 tarjetas hechas:
  un punto de partida a la vista. No lo cruza ningún destello.
- Los tonos de día o de noche se eligen según lo oscuro que sea el fondo real de la tarjeta. Al
  cambiar Anki de modo, o al cambiar el tamaño de la ventana, la barra se vuelve a pintar en su sitio,
  sin animación.
- Al entrar a repasar (también a un mazo a medias) o al cambiar las opciones, la barra se dibuja ya en
  su sitio, sin deslizarse desde cero (1.5.0).
- El relleno avanza deslizándose en 0,3 segundos y frena al final (antes, 0,4). Los cambios de color
  (al pasar a dorado y al volver) se funden en 0,4 segundos. Si el sistema pide reducir las
  animaciones, todo cambia al instante: ni deslizamiento, ni fundidos, ni hitos que crecen, ni chispas.
- Para el lector de pantalla, la barra es una barra de progreso llamada «Progreso de hoy» (1.3.0), con
  su valor en palabras («30 de 50 tarjetas»; con 5 aciertos seguidos o más, «30 de 50 tarjetas; 7
  aciertos seguidos»). No anuncia nada por su cuenta: se consulta cuando se quiere.
- En el modo de contraste alto de Windows (1.5.0), cada pieza toma un color del sistema: el canal, el
  del fondo con un borde del color del texto; el relleno, el de resaltado; los cortes, el del fondo; el
  próximo hito, aro del color de resaltado; el total, aro del color del texto; la estrella dorada, el
  del texto resaltado; y el aviso, un borde del color del texto. Las chispas no salen.

## 3. Los hitos

- Si la opción «Mostrar hitos en la barra» está marcada y el total de hoy en el mazo es de 10 tarjetas
  o más, la barra lleva hitos en números redondos (desde la 1.3.0). El paso es el menor de 5, 10, 20,
  25, 50, 100, 200, 250, 500, 1.000… que deja cinco hitos o menos, y ninguno pasa del 92 % del ancho:
  con 27 tarjetas, 5, 10, 15 y 20; con 50, 10, 20, 30 y 40; con 130, 20, 40, 60, 80 y 100. Al final
  está el total de hoy («27»). Con menos de 10 tarjetas no hay hitos. El paso se decide al entrar a
  repasar.
- Cada hito está justo donde llega el relleno al despachar ese número de tarjetas.
- Desde la 1.5.0 solo se ven dos números (antes, hasta seis):
  - El próximo hito: un disco del alto de la barra más 4 px, del color de las tarjetas elevadas, con
    un aro de 2 px y el número en la tinta del tema (la de la barra dorada, si lo es).
  - El total, al final: un disco igual con un aro gris fino y el número en gris. Cuando ya no queda
    ningún hito por delante, el total pasa a ser el próximo y toma el color.
  - Los hitos ya pasados y los que quedan detrás del próximo son cortes finos de 2 px del color del
    fondo, sin número.
- Al alcanzar un hito, con «Celebrar rachas y récords» marcada, su disco se llena de tinta con el
  número en claro, crece un poco, se queda un instante y se convierte en corte (0,6 s en total);
  suelta tres chispas pequeñas que suben y se apagan en medio segundo, y después aparece el disco del
  hito siguiente. Si esa misma respuesta trae un aviso (una celebración por respuesta), o si el sistema
  pide reducir las animaciones, el hito pasa a corte sin más.
- Números de 11 px (12 con la barra Gruesa), en seminegrita y con cifras del mismo ancho. Con números
  de muchas cifras, el disco se ensancha en forma de pastilla.
- Con la barra Fina no hay discos, que no se leerían: el próximo hito es un corte de 3 px en la tinta
  y el final del canal es el total.

## 4. Racha y récord

- Racha: respuestas seguidas con «Difícil», «Bien» o «Fácil» en este repaso; es decir, tarjetas
  recordadas seguidas, que es lo que Anki considera acierto. Solo «Otra vez» la pone a cero (hasta la
  1.1.0 también «Difícil», y eso empujaba a pulsar «Bien» tras dudar). Empieza de cero cada vez que
  entra a repasar. No se ve como una cifra fija: solo en los avisos.
- Avisos de racha (con «Celebrar rachas y récords» marcada): al llegar a 5, 10, 20, 30… (cada diez a
  partir de 10) aparece debajo de la barra, en mayúsculas, «5 ACIERTOS SEGUIDOS», «10 ACIERTOS
  SEGUIDOS», etc. Va centrado bajo la barra, 4 px por debajo, y no se mueve. Desde la 1.5.0 va en una
  píldora de 20 px de alto, con un fondo suave del color del tema y el texto en su tinta (6 a 1 de
  contraste o más), como una etiqueta de logro. Además salen tres chispas desde la punta del relleno
  (no, si el sistema pide reducir las animaciones); desde la 1.5.0 el relleno ya no se aviva.
- El aviso dura 1,5 segundos (aparece en 0,15 s y se apaga en 0,3 s, solo), pase lo que pase con la
  tarjeta; uno nuevo sustituye al anterior.
- Barra dorada (con la casilla marcada): con 5 o más seguidas, el relleno pasa a un oro claro, más
  claro que cualquier tema, y en su punta aparece una estrella de cinco puntas (1.5.0, en lugar del
  halo): dorado profundo de día y del color del fondo de noche. Así se reconoce por la forma, también
  con daltonismo y en el contraste alto de Windows. De día el relleno lleva además un contorno de 1 px
  en dorado profundo, porque un oro claro casi no se distingue del canal. El aviso y el próximo hito
  pasan a dorado (la píldora, a un dorado suave). Al romperse la racha vuelve al color del tema en
  0,4 s y la estrella se va con el color, sin aviso.
- Mejor racha de los últimos 30 días (1.3.0): se celebra una vez por repaso al superarla, como mínimo a
  las 3 seguidas, con «MEJOR RACHA EN 30 DÍAS: 42». Se guarda, junto al récord, la mejor racha de
  cada día de los últimos 30. Así hay una meta que se renueva sola: un récord histórico alto casi no
  se vuelve a batir.
- Récord: la racha más larga lograda en sus repasos, propia de cada perfil. Se celebra una vez por
  repaso, en el momento de batirlo: cuando la racha supera en uno el récord con el que empezó, y como
  mínimo a las 3 seguidas. El aviso dice «NUEVO RÉCORD: 11».
- Una sola celebración por respuesta (1.3.0), en este orden: récord, mejor racha de 30 días, número de
  racha y, solo si no hay ninguno de los anteriores, el salto del hito.
- Cuándo se guarda: en el momento de batirlo (si la casilla está marcada) y, en todo caso, al salir del
  repaso o al cerrar el perfil, con la racha más larga de ese repaso si supera la guardada.
- Mazos que no cuentan para el récord: en ellos no se celebra ni se guarda récord ni mejor racha de 30
  días; la barra, los avisos de racha y la barra dorada siguen saliendo. Excluir un mazo excluye también sus submazos.
  Cuenta el mazo que abrió para estudiar.

## 5. Al deshacer

- Editar > Deshacer (Ctrl+Z) de una respuesta: la barra retrocede (es lo único que la hace
  retroceder), la racha pierde esa respuesta, el aviso que estuviera a la vista se apaga al momento y,
  si el récord guardado (o la mejor racha de hoy) había subido en este repaso, baja con ella (nunca por
  debajo del que tenía al empezar).
- Deshacer algo que no toca la cola de estudio no cambia la racha. Deshacer enterrar, suspender u
  otros cambios de la cola también le quita una respuesta a la racha (véase «Pendientes» en el
  registro de errores).
- Rehacer no devuelve la respuesta a la racha.

## 6. Al terminar un mazo

Desde la 1.4.0, nada: al terminar un mazo, la pantalla de «¡Enhorabuena!» de Anki queda tal cual, sin
barra llena ni línea de resumen (lo pidió usted el 2026-11-17). La celebración, si la tiene activada,
es cosa de ProFeedback.

## 7. Ventana de opciones

Título «CoreProgress» en la barra de la ventana; desde la 1.3.0 no se repite dentro. Sigue el modelo de
ventana de opciones del taller, el panel de GritMap: 560 px de ancho y el alto justo para su contenido
(unos 646 px; desde la 1.3.0 cabe entera sin desplazar, también en una pantalla de 1.366 × 768),
recuadros sobre el fondo de Anki con los colores de la paleta (también con Atelier) y Aceptar y
Cancelar abajo, de 88 px de ancho como mínimo y alineados con los recuadros (en Windows, Aceptar
primero). No se enseña hasta estar dibujado, recuerda su posición, y si ya está abierto se trae al
frente. Esc cancela (en la lista de mazos, vuelve) y Ctrl+Intro acepta. Nada se guarda hasta pulsar
Aceptar. Aceptar, Cancelar y Restaurar llevan el texto de Qt en el idioma de Anki. Con el teclado: el
tabulador recorre los controles (las fichas de tema son una sola parada y se eligen con las flechas;
«−» y «+» no son paradas, el valor cambia con las flechas); el contorno de foco azul solo se ve si se
usa el teclado (si la ventana se abrió con el ratón, no hasta la primera tecla); el lector de pantalla
anuncia el nombre de cada control.

Dos recuadros (desde la 1.3.0; antes tres, con el récord primero):

1. El aspecto de la barra:
   - Arriba, una vista previa: un rectángulo del color de fondo de las tarjetas con una barra de
     muestra al 60 %, como la del repaso (1.5.0): los hitos 10, 20 y 30 son cortes, el 40 es el próximo
     (disco con número) y el total 50 queda en gris. Cambia al instante con el tema, el grosor y la
     casilla de hitos. No se pulsa ni la lee el lector de pantalla.
   - «Tema de color», con «Restaurar los valores predeterminados» en la misma fila, a la derecha (en
     el color de enlace y subrayado; tras usarlo, «Deshacer» al lado). Repone el tema, el grosor, el
     espacio y las dos casillas sin guardar nada y sin tocar el récord ni los mazos.

| Opción | Control | Valores | Por defecto |
|---|---|---|---|
| Tema de color | Fichas de 32 px en dos columnas, por orden alfabético de su nombre, cada una con su muestra: desde la 1.5.0, una minibarra de 30 × 10 px con el degradado del tema en el modo activo, sin contorno. La elegida, con el tinte de selección, un borde de 2 px y una ✓ en el color de enlace | Azul océano, Naranja atardecer, Púrpura real, Rosa suave, Turquesa laguna, Verde clásico | Verde clásico |
| Grosor (1.5.0; antes «Altura de la barra», de 12 a 22 px) | Tres botones seguidos sobre un carril (control segmentado, como los de GritMap), en paralelo con el siguiente; el elegido, con el fondo de la capa elevada, borde azul y seminegrita. Si algún nombre no cupiera en su idioma, pasan a lista vertical | Fina (12 px), Normal (16) y Gruesa (20); también cambia el tamaño de los hitos y de sus números. Un valor guardado por una versión anterior pasa al más cercano (22 → Gruesa, 14 → Normal) | Normal |
| Espacio extra | Campo con «−» y «+» (de 4 en 4) y «px · 0–300» al lado | De 0 a 300 píxeles que se suman al espacio mínimo que la tarjeta deja a la barra | 0 |
| Mostrar hitos en la barra | Casilla | — | Marcada |
| Celebrar rachas y récords | Casilla | Avisos de racha, de mejor racha de 30 días y de récord, barra dorada con su estrella, chispas, y la animación y las chispas de los hitos | Marcada |

   El signo «−» o «+» que ya no sirve (en el límite) va en el gris de apagado de la paleta.
   Si tenía elegido Rojo fuego, que se retiró en la 1.2.0, arriba del recuadro sale «Su tema «Rojo
   fuego» se ha retirado; ahora usa «Naranja atardecer».», hasta que pulse Aceptar.
2. El récord, entero:
   - «Récord: **7 aciertos seguidos**» o, si la mejor racha de los últimos 30 días es menor que el
     récord, «Mejor racha en 30 días: **41** · récord: 90» (1.3.0), o «Sin récord todavía». Si se abre
     durante un repaso, incluye la racha en curso cuando la supera. A la derecha, el enlace «Poner a
     cero», que desde la 1.3.0 no se enseña si no hay récord. Pregunta en una ventanita dentro del
     panel «¿Poner el récord a cero?», con los botones «Poner a cero» y «Cancelar» y el foco en
     «Cancelar». Si se confirma, la línea pasa a «Sin récord todavía», pero el récord no se borra hasta
     pulsar Aceptar; con Cancelar queda como estaba (FIX-003). Pone a cero el récord histórico; la
     mejor racha de los 30 días se conserva.
   - «Mazos que no cuentan para el récord»: una fila con los nombres de los mazos marcados (o
     «Ninguno», desde la 1.3.0; antes un guion), con la línea gris «Útil para mazos muy fáciles.»
     debajo, que abre su lista dentro de la misma ventana, con «‹ CoreProgress» para volver: un
     buscador («Ningún mazo coincide.» si no encuentra nada) y todos sus mazos con su nombre completo
     (los submazos, con «::»), incluidos los filtrados y el predeterminado, cada uno con su casilla. Lo
     marcado se guarda al pulsar Aceptar; los mazos que ya no existen dejan de guardarse.

- Aceptar: si está repasando, la barra se vuelve a dibujar al momento con los valores nuevos. Un
  aviso que estuviera a la vista se conserva si la casilla de celebrar sigue marcada y desaparece al
  momento si la desmarca.

## 8. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de este ordenador: valen para todos los perfiles
  y no viajan con la sincronización.
- El récord y, desde la 1.3.0, la mejor racha de cada día de los últimos 30 días, dentro de la
  colección de cada perfil: cada perfil tiene los suyos y viajan con la sincronización. No se puede deshacer desde Editar, porque es un ajuste y no estudio.
- Si una versión antigua del complemento dejó el récord en la configuración de complementos, al abrir
  un perfil lo pasa a la colección de ese perfil (se queda el más alto de los dos).
- Si falta una opción o tiene un valor que no sirve, usa el valor por defecto; un número fuera de su
  margen se lleva al límite más cercano. Entiende también la forma de guardar el tema de versiones
  antiguas. Desde la 1.2.0, el «Espacio superior» de antes se convierte en «Espacio extra» restándole
  el mínimo automático, para que quien lo había subido conserve el mismo hueco.
- La racha y la barra solo existen mientras repasa: no se guardan.

## 9. Idiomas

Sus textos están en 60 idiomas; si el de Anki no está, salen en inglés. El idioma se elige una vez al
arrancar Anki. Desde la 1.2.0 los textos son impersonales (sin tú ni usted), salvo el aviso del tema
retirado, que trata de usted como en GritMap. Las cifras con unidad («7 aciertos seguidos», «48
tarjetas») usan la forma de plural de cada idioma. Los botones estándar salen en el idioma de Anki.

## 10. Si algo falla

- Nunca abre la ventana de error de Anki. El detalle técnico queda en el registro del complemento.
- La primera vez en cada sesión de Anki muestra durante 3 segundos el aviso breve de Anki con el nombre
  delante (1.3.0): «CoreProgress: El problema podría ser causado por un add-on.»; los fallos
  siguientes de esa sesión no avisan.
- Si no puede leer lo hecho hoy en el mazo, la barra empieza como antes, con lo que queda como total.
- Un fallo dentro del dibujo de la barra no avisa: la barra puede no aparecer o quedarse quieta, pero
  el repaso sigue con normalidad.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee la cuenta de tarjetas pendientes y lo respondido hoy.
- No muestra la racha como cifra fija ni el récord durante el repaso (el récord, en las opciones y en
  el aviso de «NUEVO RÉCORD» al batirlo). No muestra un porcentaje ni «15/27»: la marca final ya da
  el total.
- No suena: el sonido es de ProFeedback.
- No da mensajes de ánimo al fallar: fallar no cuesta nada visible (la barra no retrocede y al
  romperse la racha solo se funde el dorado).
- No aparece fuera del repaso.
- No añade menús ni atajos.
