# Qué hace «CoreProgress»

Versión 1.2.0 · 2026-11-09

Barra de progreso en la parte de arriba de la pantalla de repaso: se va llenando a medida que despacha
lo que tenía hoy en el mazo que está estudiando, con marcas numeradas por el camino. Además cuenta sus
aciertos seguidos, los celebra con un aviso breve en ciertos números, vuelve dorada la barra a partir
de cinco y guarda su récord personal. Al terminar un mazo, deja la barra llena y una línea de resumen
en la pantalla de «¡Enhorabuena!». Solo lee su estudio: nunca cambia tarjetas, notas, repasos ni
fechas. Lo único que guarda son sus opciones y su récord.

La 1.2.0 aplica entero el informe de interfaz, aprendizaje y hábito del 2026-11-09, aprobado por el
cliente también en lo que cambiaba decisiones anteriores (véase «Así a propósito» en el registro de
errores).

## 1. Dónde aparece

- En la pantalla de repaso (la que se abre al pulsar «Estudiar ahora»), también al repasar un mazo
  filtrado o un estudio personalizado.
- En la pantalla de «¡Enhorabuena!» de Anki, la que sale al terminar un mazo: la barra llena y una
  línea (apartado 6).
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No aparece en la lista de mazos, en la pantalla de un mazo con tarjetas pendientes, en Explorar
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
- Se pone al día una décima de segundo después de cada respuesta y después de cualquier cambio que
  haga Anki.
- La barra no retrocede: si la cuenta de Anki sube durante el repaso (porque vencen tarjetas en
  aprendizaje que al empezar todavía no contaban), se queda quieta hasta que el avance la alcance.
  Solo retrocede al deshacer una respuesta. Al terminar, lo que queda es cero y llega al 100 %.
- En un mazo filtrado, las tarjetas que al responderlas vuelven a su mazo de origen dejan de contarse
  como hechas en ese filtrado si sale y vuelve a entrar.

Aspecto:

- Queda fija arriba, de lado a lado (con 18 píxeles de margen a cada lado y 10 por arriba), por
  encima de la tarjeta; no se mueve al bajar por una tarjeta larga. Los clics la atraviesan.
- La tarjeta deja siempre sitio a la barra y a su aviso: 10 px de margen, el alto de la barra, 24 px
  para el aviso de racha (solo con «Celebrar rachas y récords» marcada) y 8 px de aire: 58 px con la
  barra de serie, 34 sin celebraciones. «Espacio extra» se suma a ese mínimo. Hasta la 1.1.0, con el valor de serie
  la barra tapaba la parte alta de la tarjeta (FIX-004).
- El canal (la parte vacía) es un tono algo más claro o más oscuro que el fondo real de la tarjeta,
  medido en pantalla. Hasta tener esa medida la barra no se enseña (como mucho, algo más de medio
  segundo) y después aparece con un fundido breve. Quien edite plantillas de tarjeta puede fijar desde
  la plantilla el color del canal.
- El relleno es un degradado del tema de color elegido, con un brillo de cristal en su mitad de
  arriba. Desde la 1.2.0 ya no lo cruza ningún destello.
- Los tonos de día o de noche se eligen según lo oscuro que sea el fondo real de la tarjeta. Al
  cambiar Anki de modo, o al cambiar el tamaño de la ventana, la barra se vuelve a pintar.
- El relleno avanza deslizándose en cuatro décimas de segundo. Los cambios de color (por ejemplo, al
  pasar a dorado) se funden en casi medio segundo; sin fundido si el sistema pide reducir las
  animaciones.
- Para el lector de pantalla, la barra es una barra de progreso con su valor en palabras («30 de 50
  tarjetas»). No anuncia nada por su cuenta: se consulta cuando se quiere.

## 3. Los hitos (marcas numeradas)

- Si la opción «Mostrar hitos en la barra» está marcada y el total de hoy en el mazo es de 10 tarjetas
  o más, la barra lleva cuatro marcas, en el 20, 40, 60 y 80 % del total, cada una con su número de
  tarjetas: con 50 tarjetas, 10, 20, 30 y 40. Con menos de 10 tarjetas no hay hitos.
- Los números se redondean; si dos coinciden, solo sale uno. Van en letra de 11 a 13 px; con la barra
  por debajo de 14 px de alto no se leerían, así que solo quedan las marcas, sin número.
- Cada marca está justo donde llega el relleno al despachar ese número de tarjetas.
- Mientras no se alcanza, la marca tiene el color del canal y el número en gris. Al alcanzarla toma
  el color del relleno y su número va en blanco o en oscuro, lo que se lea mejor sobre el tono que
  tiene detrás (desde la 1.2.0: el blanco no se leía bien sobre los tonos claros). Con «Celebrar
  rachas y récords» marcada, además da un pequeño salto (crece un poco durante cuatro décimas de
  segundo) y suelta tres chispas; las chispas no salen si el sistema pide reducir las animaciones.
- Con números de muchas cifras, la marca se ensancha en forma de pastilla para que quepan.

## 4. Racha y récord

- Racha: respuestas seguidas con «Difícil», «Bien» o «Fácil» en este repaso; es decir, tarjetas
  recordadas seguidas, que es lo que Anki considera acierto. Solo «Otra vez» la pone a cero (hasta la
  1.1.0 también «Difícil», y eso empujaba a pulsar «Bien» tras dudar). Empieza de cero cada vez que
  entra a repasar. No se ve como una cifra fija: solo en los avisos.
- Avisos de racha (con «Celebrar rachas y récords» marcada): al llegar a 5, 10, 20, 30… (cada diez a
  partir de 10) aparece debajo de la barra, en mayúsculas, «5 ACIERTOS SEGUIDOS», «10 ACIERTOS
  SEGUIDOS», etc. (hasta la 1.1.0 también a las 2 y a las 15, 25…). El aviso va centrado bajo el
  relleno y se mueve con él. Además, el relleno se aviva un instante y suelta cuatro chispas en su
  borde (las chispas no, si el sistema pide reducir las animaciones).
- El aviso dura 1,5 segundos y se apaga solo con un fundido, pase lo que pase con la tarjeta; uno
  nuevo sustituye al anterior.
- Barra dorada (con la casilla marcada): con 5 o más seguidas, el relleno pasa a tonos dorados con un
  halo suave, y el aviso, a dorado. Al romperse la racha vuelve al color del tema, sin aviso.
- Récord: la racha más larga lograda en sus repasos, propia de cada perfil. Se celebra una vez por
  repaso, en el momento de batirlo: cuando la racha supera en uno el récord con el que empezó, y como
  mínimo a las 3 seguidas. El aviso dice «NUEVO RÉCORD: 11». Si coincide con un número de racha, sale
  el de récord.
- Cuándo se guarda: en el momento de batirlo (si la casilla está marcada) y, en todo caso, al salir del
  repaso o al cerrar el perfil, con la racha más larga de ese repaso si supera la guardada.
- Mazos que no cuentan para el récord: en ellos no se celebra ni se guarda récord; la barra, los
  avisos de racha y la barra dorada siguen saliendo. Excluir un mazo excluye también sus submazos.
  Cuenta el mazo que abrió para estudiar.

## 5. Al deshacer

- Editar > Deshacer (Ctrl+Z) de una respuesta: la barra retrocede (es lo único que la hace
  retroceder), la racha pierde esa respuesta, el aviso que estuviera a la vista se apaga al momento y,
  si el récord guardado había subido en este repaso, baja con ella (nunca por debajo del que tenía al
  empezar).
- Deshacer algo que no toca la cola de estudio no cambia la racha. Deshacer enterrar, suspender u
  otros cambios de la cola también le quita una respuesta a la racha (véase «Pendientes» en el
  registro de errores).
- Rehacer no devuelve la respuesta a la racha.

## 6. Al terminar un mazo

En la pantalla de «¡Enhorabuena!» de Anki, la que sale al no quedar nada en el mazo, CoreProgress pone
arriba su barra llena y quieta (sin chispas ni movimiento), en el color del tema, y debajo una línea
en gris:

```
████████████████████████████████████
48 tarjetas · mejor racha: 17
```

- «48 tarjetas» es el total de hoy en ese mazo. «Mejor racha» es la más larga de ese repaso; si batió
  el récord, «nuevo récord: 17». Sin ningún acierto seguido, solo las tarjetas.
- Solo sale al terminar de verdad, al salir del repaso con el mazo vacío; no al salir a medias.
- No tapa nada: va en su sitio, encima del contenido de la página. La celebración (confeti y sonido) es
  cosa de ProFeedback; CoreProgress solo pone el dato.

## 7. Ventana de opciones

Título «CoreProgress». Sigue el modelo de ventana de opciones del taller, el panel de GritMap: un panel
de 560 px de ancho y el alto justo para su contenido, hecho de recuadros sobre el fondo de Anki, con
los colores de la paleta (también con Atelier) y Aceptar y Cancelar abajo (en Windows, Aceptar
primero). No se enseña hasta estar dibujado, recuerda su tamaño y su posición, y si ya está abierto se
trae al frente. Esc cancela y Ctrl+Intro acepta. Nada se guarda hasta pulsar Aceptar. Aceptar,
Cancelar y Restaurar llevan el texto de Qt en el idioma de Anki. Con el teclado: el tabulador recorre
los controles, cada uno con su contorno de foco azul; el lector de pantalla anuncia el nombre de cada
control.

Tres recuadros:

1. El récord: «Récord: **7 aciertos seguidos**» («1 acierto seguido» en singular, con la forma de
   plural de cada idioma) o «Sin récord todavía». Si se abre durante un repaso, incluye la racha en
   curso cuando la supera. A la derecha, el enlace «Poner a cero» (apagado si no hay récord), que
   pregunta en una ventanita dentro del panel «¿Poner el récord a cero?», con los botones «Poner a
   cero» y «Cancelar» y el foco en «Cancelar». Si se confirma, la línea pasa a «Sin récord todavía»,
   pero el récord no se borra hasta pulsar Aceptar; con Cancelar queda como estaba (FIX-003).
2. El aspecto de la barra, con «Restaurar los valores predeterminados» arriba a la derecha (tras
   usarlo, «Deshacer» al lado), que repone el tema, la altura, el espacio y las dos casillas sin
   guardar nada y sin tocar el récord ni los mazos:

| Opción | Control | Valores | Por defecto |
|---|---|---|---|
| Tema de color | Fichas en dos columnas, por orden alfabético de su nombre, cada una con su cuadrito de muestra en el tono del modo activo (día o noche) y una ✓ en la elegida | Azul océano, Naranja atardecer, Púrpura real, Rosa suave, Turquesa laguna, Verde clásico | Verde clásico |
| Altura de la barra | Campo con «−» y «+» y «px» al lado | De 12 a 22 píxeles; también cambia el tamaño de los hitos y de sus números | 16 |
| Espacio extra | Campo con «−» y «+» (de 4 en 4) y «px» al lado | De 0 a 300 píxeles que se suman al espacio mínimo que la tarjeta deja a la barra | 0 |
| Celebrar rachas y récords | Casilla | Avisos de racha y de récord, barra dorada, avivado y chispas, y el salto y las chispas de los hitos | Marcada |
| Mostrar hitos en la barra | Casilla | — | Marcada |

   Si tenía elegido Rojo fuego, que se retiró en la 1.2.0 (en Anki el rojo es «Otra vez» y error),
   arriba del recuadro sale «Su tema «Rojo fuego» se ha retirado; ahora usa «Naranja atardecer».», el
   mismo aviso que en GritMap, hasta que pulse Aceptar.
3. «Mazos que no cuentan para el récord»: una fila con los nombres de los mazos marcados (o «-»), con
   la línea gris «Útil para mazos muy fáciles.» debajo, que abre su lista dentro de la misma ventana,
   con «‹ CoreProgress» para volver: un buscador y todos sus mazos con su nombre completo (los
   submazos, con «::»), incluidos los filtrados y el predeterminado, cada uno con su casilla. Lo
   marcado se guarda al pulsar Aceptar; los mazos que ya no existen dejan de guardarse.

- Aceptar: si está repasando, la barra se vuelve a dibujar al momento con los valores nuevos. Un
  aviso que estuviera a la vista se conserva si la casilla de celebrar sigue marcada y desaparece al
  momento si la desmarca.

## 8. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de este ordenador: valen para todos los perfiles
  y no viajan con la sincronización.
- El récord, dentro de la colección de cada perfil: cada perfil tiene el suyo y viaja con la
  sincronización. No se puede deshacer desde Editar, porque es un ajuste y no estudio.
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
- La primera vez en cada sesión de Anki muestra durante 3 segundos el aviso breve de Anki «El
  problema podría ser causado por un add-on.»; los fallos siguientes de esa sesión no avisan.
- Si no puede leer lo hecho hoy en el mazo, la barra empieza como antes, con lo que queda como total.
- Un fallo dentro del dibujo de la barra no avisa: la barra puede no aparecer o quedarse quieta, pero
  el repaso sigue con normalidad.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee la cuenta de tarjetas pendientes y lo respondido hoy.
- No muestra la racha como cifra fija ni el récord durante el repaso (el récord, en las opciones y en
  la línea de «¡Enhorabuena!» si se bate).
- No da mensajes de ánimo al fallar: fallar no cuesta nada visible (la barra no retrocede y al
  romperse la racha solo se funde el dorado).
- No aparece fuera del repaso, salvo la barra llena de la pantalla de «¡Enhorabuena!».
- No añade menús ni atajos.
