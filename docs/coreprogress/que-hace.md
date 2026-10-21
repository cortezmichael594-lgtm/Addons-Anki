# Qué hace «CoreProgress»

Versión 1.0.0 · 2026-10-21

Barra de progreso en la parte de arriba de la pantalla de repaso: se va llenando a medida que despacha
las tarjetas que tenía pendientes hoy en el mazo que está estudiando, con marcas numeradas por el
camino. Además cuenta sus aciertos seguidos: los celebra con un aviso breve en ciertos números, vuelve
dorada la barra a partir de cinco y guarda su récord personal de aciertos seguidos. Solo lee su
estudio: nunca cambia tarjetas, notas, repasos ni fechas. Lo único que guarda son sus opciones y su
récord.

## 1. Dónde aparece

- En la pantalla de repaso (la que se abre al pulsar «Estudiar ahora»), también al repasar un mazo
  filtrado o un estudio personalizado.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No aparece en la lista de mazos, en la pantalla de un mazo, en Explorar (tampoco en su vista
  previa), en la pantalla de plantillas de las tarjetas, en el editor ni en las estadísticas. No añade
  menús ni atajos de teclado.
- En la pantalla de repaso baja la estrella de nota marcada y la bandera de Anki para que queden
  justo debajo de la barra. Lo hace en toda la pantalla de repaso, también antes de que la barra
  aparezca.

## 2. La barra

Qué mide:

- Al entrar a repasar toma como total la suma de las tres cifras que Anki muestra abajo en ese
  momento (nuevas, en aprendizaje y para repasar). Ese es el 100 %. La barra se llena según cuántas
  de esas tarjetas han salido ya de la cola de hoy.
- Una tarjeta solo cuenta cuando sale de verdad de la cola: cuando se gradúa o cuando un repaso pasa a
  otro día. Una tarjeta fallada vuelve a aprendizaje y, mientras Anki la siga contando abajo, no hace
  avanzar la barra.
- Enterrar, suspender o apartar una tarjeta de hoy también hace avanzar la barra, porque sale de la
  cola.
- Se pone al día una décima de segundo después de cada respuesta y después de cualquier cambio que
  haga Anki (por ejemplo, al editar una nota desde Explorar mientras repasa).
- Cada vez que entra a repasar empieza vacía, con lo que quede en ese momento como nuevo total. Si
  sale a la lista de mazos con la mitad hecha y vuelve, la barra nueva toma esa mitad como su 100 %.
- Si la cuenta de Anki sube durante el repaso (por ejemplo, porque vencen tarjetas en aprendizaje que
  al empezar todavía no contaban, o porque deshace una respuesta), la barra retrocede. Nunca baja de
  vacía.
- Cuando no queda nada, Anki sale del repaso y la barra se va con él, así que casi nunca se ve llena
  del todo.

Aspecto:

- Queda fija arriba, de lado a lado (con 18 píxeles de margen a cada lado y 10 por arriba), por
  encima de la tarjeta; no se mueve al bajar por una tarjeta larga. Los clics la atraviesan: no impide
  pulsar lo que haya debajo.
- El canal (la parte vacía) es un tono algo más claro o más oscuro que el fondo real de la tarjeta,
  medido en pantalla; así encaja también con plantillas que tienen su propio fondo. Hasta tener esa
  medida la barra no se enseña (como mucho, algo más de medio segundo) y después aparece con un
  fundido breve. Quien edite plantillas de tarjeta puede fijar desde la plantilla el color del canal.
- El relleno es un degradado del tema de color elegido, con un brillo de cristal en su mitad de
  arriba y un destello que lo cruza de izquierda a derecha cada 9 segundos, sin parar. Si el sistema
  tiene activada la opción de reducir las animaciones, el destello queda quieto y tenue.
- Los tonos de día o de noche se eligen según lo oscuro que sea el fondo real de la tarjeta, no solo
  según el modo de Anki. Al cambiar Anki de modo, o al cambiar el tamaño de la ventana, la barra se
  vuelve a pintar.
- El relleno avanza deslizándose en cuatro décimas de segundo. Los cambios de color (por ejemplo, al
  pasar a dorado) se funden en casi medio segundo; sin fundido si el sistema pide reducir las
  animaciones.
- Con el «Espacio superior» en 0, que es el valor por defecto, la barra se dibuja encima de la parte
  alta de la tarjeta, sin apartarla (véase «Pendientes» en el registro de errores). Al subir ese
  valor, la tarjeta baja esos píxeles.

## 3. Los hitos (marcas numeradas)

- Si la opción «Mostrar hitos en la barra» está marcada y el total del repaso es de 10 tarjetas o
  más, la barra lleva cuatro marcas, en el 20, 40, 60 y 80 % del total, cada una con su número de
  tarjetas: con 50 tarjetas, 10, 20, 30 y 40. Con menos de 10 tarjetas no hay hitos.
- Los números se redondean; si dos coinciden, solo sale uno.
- Cada marca está justo donde llega el relleno al despachar ese número de tarjetas.
- Mientras no se alcanza, la marca tiene el color del canal y el número en gris. Al alcanzarla toma
  el color del relleno, con el número en blanco, da un pequeño salto (crece un poco durante cuatro
  décimas de segundo) y suelta tres chispas. Las chispas no salen si el sistema pide reducir las
  animaciones; el salto, sí.
- Esto no depende de la casilla de efectos: los hitos se animan aunque esté desmarcada.
- Con números de muchas cifras, la marca se ensancha en forma de pastilla para que quepan.

## 4. Racha y récord

- Racha: respuestas seguidas con «Bien» o «Fácil» en este repaso. «Otra vez» y también «Difícil» la
  ponen a cero. Empieza de cero cada vez que entra a repasar. No se ve como una cifra fija: solo en
  los avisos.
- Avisos de racha (con la casilla de efectos marcada): al llegar a 2, 5, 10, 15, 25, 35, 45… (cada
  diez a partir de 25) aparece debajo de la barra, en mayúsculas, «2 SEGUIDAS», «5 SEGUIDAS», etc. El
  aviso va centrado bajo el relleno y se mueve con él. Desde 5 seguidas, además, el relleno se aviva
  un instante y suelta cuatro chispas en su borde (las chispas no, si el sistema pide reducir las
  animaciones).
- El aviso aparece al responder, se ve durante la pregunta siguiente y se apaga con un fundido al
  mostrar la respuesta, pero nunca antes de llevar 2 segundos a la vista.
- Barra dorada (con la casilla de efectos marcada): con 5 o más seguidas, el relleno pasa a tonos
  dorados con un halo suave, y el aviso, a dorado. Al romperse la racha vuelve al color del tema.
- Récord: la racha más larga lograda en sus repasos, propia de cada perfil. Se celebra una vez por
  repaso, en el momento de batirlo: cuando la racha supera en uno el récord con el que empezó, y como
  mínimo a las 3 seguidas. Sin récord, o con 1 o 2, se celebra a las 3; con un récord de 10, a las 11.
  El aviso dice «¡RÉCORD! 11», con el avivado y las chispas si es de 5 o más. Si coincide con un
  número de racha, sale el de récord. Las respuestas siguientes de ese repaso vuelven a mostrar los
  avisos de racha normales.
- Cuándo se guarda: en el momento de batirlo (si la casilla de efectos está marcada) y, en todo caso,
  al salir del repaso o al cerrar el perfil, con la racha más larga de ese repaso si supera la
  guardada. Con la casilla desmarcada no se celebra, pero se guarda igual al salir.
- Mazos excluidos: en ellos no se celebra ni se guarda récord; la barra, los avisos de racha y la
  barra dorada siguen saliendo. Excluir un mazo excluye también sus submazos. Cuenta el mazo que abrió
  para estudiar: si estudia un mazo padre que contiene uno excluido, ese repaso sí cuenta para el
  récord.

## 5. Al deshacer

- Editar > Deshacer (Ctrl+Z) de una respuesta: la barra retrocede, la racha pierde esa respuesta, el
  aviso que estuviera a la vista se apaga al momento y, si el récord guardado había subido en este
  repaso, baja con ella (nunca por debajo del que tenía al empezar).
- Deshacer algo que no toca la cola de estudio (por ejemplo, un cambio de texto hecho en Explorar) no
  cambia la racha.
- Deshacer enterrar, suspender u otros cambios de la cola también le quita una respuesta a la racha
  (véase «Pendientes» en el registro de errores).
- Rehacer no devuelve la respuesta a la racha.

## 6. Ventana de opciones

Título «CoreProgress». Mientras está abierta no se puede usar el resto de Anki. No recuerda su tamaño
ni su posición.

Arriba, el récord, con la cifra en negrita: «Tu récord actual: -» si no hay ninguno, o «Tu récord actual: 7
seguidas!» (con un récord de 1, «1 seguidas!»). Durante un repaso puede no incluir todavía la racha en
curso, que se guarda al salir. A su derecha, el botón «Restablecer», que pregunta en una ventana
titulada «Anki»: «¿Poner tu récord a cero?», con «Sí» marcado de antemano. Si acepta, el récord
queda a cero en ese momento, aunque después pulse Cancelar, y no se puede deshacer. Si lo hace
mientras repasa, ese repaso solo cuenta para el récord desde la racha que lleve en ese momento.

| Opción | Valores | Por defecto |
|---|---|---|
| Tema de color | Verde clásico, Azul océano, Turquesa laguna, Rojo fuego, Rosa suave, Púrpura real, Naranja atardecer (cada uno con un cuadrito de muestra, siempre en su tono de día) | Verde clásico |
| Altura de la barra (px) | De 12 a 22 píxeles; también cambia el tamaño de los hitos y de sus números | 16 |
| Espacio superior (px) | De 0 a 300 píxeles que se dejan libres encima de la tarjeta; las flechas van de 4 en 4 | 0 |
| Excluir mazos (récord) | Botón «Seleccionar mazos» | Ninguno |
| Efectos de racha y récord (aura/oro/texto) | Casilla: avisos de racha y de récord, barra dorada, avivado y chispas de los avisos | Marcada |
| Mostrar hitos en la barra | Casilla | Marcada |

- Botones Guardar, Cancelar y el estándar para restaurar los valores predeterminados, con los textos
  de Qt en el idioma de Anki.
- Restaurar los valores predeterminados repone en la ventana el tema, la altura, el espacio y las dos
  casillas; no guarda nada hasta pulsar Guardar y no toca el récord ni los mazos excluidos.
- Guardar: si está repasando, la barra se vuelve a dibujar al momento con los valores nuevos. Un aviso
  que estuviera a la vista se conserva si la casilla de efectos sigue marcada y desaparece al momento
  si la desmarca.
- Seleccionar mazos abre la ventana «Excluir mazos (récord)»: la lista de todos sus mazos, con su
  nombre completo (los submazos, con «::»), incluidos los filtrados y el mazo predeterminado, cada uno
  con su casilla, y los botones Aceptar y Cancelar. No tiene buscador ni textos de ayuda. Lo marcado se
  guarda al pulsar Guardar en la ventana de opciones. Los mazos que ya no existen dejan de guardarse
  al aceptar esta ventana.

## 7. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de este ordenador: valen para todos los perfiles
  y no viajan con la sincronización.
- El récord, dentro de la colección de cada perfil: cada perfil tiene el suyo y viaja con la
  sincronización. No se puede deshacer desde Editar, porque es un ajuste y no estudio, y guardarlo no
  borra lo que Editar > Deshacer tenga pendiente.
- Si una versión antigua del complemento dejó el récord en la configuración de complementos, al abrir
  un perfil lo pasa a la colección de ese perfil (se queda el más alto de los dos) y lo quita de la
  configuración, así que solo lo recibe el primer perfil que se abra.
- Si falta una opción o tiene un valor que no sirve, usa el valor por defecto; un número fuera de su
  margen se lleva al límite más cercano. Entiende también la forma de guardar el tema de versiones
  antiguas.
- La racha y la barra solo existen mientras repasa: no se guardan.

## 8. Idiomas

Sus textos están en 60 idiomas; si el de Anki no está, salen en inglés. El idioma se elige una vez al
arrancar Anki: si lo cambia, el complemento lo sigue tras reiniciar Anki. En español trata de tú
(«Tu récord actual», «¿Poner tu récord a cero?»). Los botones estándar (Guardar, Cancelar, Aceptar,
Sí, No y el de restaurar) salen en el idioma de Anki.

## 9. Si algo falla

- Nunca abre la ventana de error de Anki. El detalle técnico queda en el registro del complemento (un
  archivo de texto en la carpeta de registros de Anki).
- La primera vez en cada sesión de Anki muestra durante 3 segundos el aviso breve de Anki «El
  problema podría ser causado por un add-on.»; los fallos siguientes de esa sesión no avisan.
- Un fallo dentro del dibujo de la barra no avisa: la barra puede no aparecer o quedarse quieta, pero
  el repaso sigue con normalidad.

## 10. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee la cuenta de tarjetas pendientes que muestra Anki.
- No muestra la racha como cifra fija ni el récord durante el repaso (el récord, solo en las
  opciones).
- No aparece fuera de la pantalla de repaso ni añade menús o atajos.
- La casilla de efectos no apaga el destello del relleno ni el salto y las chispas de los hitos.
