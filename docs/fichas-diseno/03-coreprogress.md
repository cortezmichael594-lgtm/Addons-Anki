# Ficha de diseño: CoreProgress

Versión 1.2.0 (9 de noviembre de 2026). Léase junto con `00-contexto-comun.md`. Es un complemento que
la persona trajo hecho fuera del taller; la 1.2.0 aplica entero el primer informe de diseño de
CoreProgress (interfaz, aprendizaje y hábito, 9 de noviembre de 2026). Los colores de los temas son
propios, fuera de la paleta Nocturne, y están aprobados.

## 1. Qué es, en una frase

Una barra de progreso fija arriba de la pantalla de repaso que se llena a medida que se despacha todo
lo de hoy en el mazo (lo hecho más lo que queda), con marcas numeradas por el camino; además cuenta los aciertos
seguidos, los celebra con un aviso breve, vuelve dorada la barra desde 5 seguidos y guarda el récord
personal. Al terminar un mazo, deja la barra llena y una línea de resumen en la pantalla de
«¡Enhorabuena!».

## 2. Para quién y para qué

Para ver cuánto falta en una sesión de repaso y motivarse con pequeños logros (hitos, rachas, récord).
Solo lee la cuenta de tarjetas que muestra Anki y lo respondido hoy; guarda sus opciones y el récord.

## 3. Dónde se ve

- En la pantalla de repaso, también en mazos filtrados y estudio personalizado.
- En la pantalla de «¡Enhorabuena!» de Anki, al terminar un mazo: la barra llena y quieta y la línea
  «48 tarjetas · mejor racha: 17» (o «nuevo récord: 17») debajo, en 13 px gris (FG_SUBTLE), centrada,
  en su sitio arriba de la página (no flota ni tapa nada). Sin animación: la celebración es de
  ProFeedback.
- Herramientas > Complementos > CoreProgress > Configuración: su ventana de opciones.
- No aparece en la lista de mazos, la pantalla de un mazo, Explorar (ni su vista previa), plantillas,
  editor ni estadísticas. No añade menús ni atajos.
- En todo el repaso baja la estrella de nota marcada y la bandera de Anki para que queden justo debajo
  de la barra.

## 4. La barra

Qué mide:

- El 100 % es todo lo de hoy en el mazo: lo que ya salió hoy de la cola (respondido hoy y fuera de
  aprendizaje, leído en segundo plano) más las tres cifras de Anki (nuevas, en aprendizaje, para
  repasar). Al volver a un mazo a medias, la barra empieza donde lo dejó, con los hitos alcanzados
  marcados y sin animación.
- Una tarjeta cuenta solo cuando sale de verdad de la cola (se gradúa o un repaso pasa a otro día). Una
  fallada vuelve a aprendizaje y no hace avanzar la barra mientras Anki la siga contando.
- Enterrar, suspender o apartar una tarjeta de hoy también hace avanzar la barra.
- Se pone al día una décima de segundo después de cada respuesta o cambio.
- Si la cuenta de Anki sube (vencen tarjetas en aprendizaje), la barra se queda quieta hasta que el
  avance la alcance; solo retrocede al deshacer.
- Al terminar, Anki sale del repaso; la barra llena se ve en la pantalla de «¡Enhorabuena!».

Posición y forma:

- Fija arriba, de lado a lado, con 18 px de margen a cada lado y 10 px arriba, por encima de la
  tarjeta; no se mueve al desplazarse. Los clics la atraviesan.
- Altura de 12 a 22 px (16 de serie); esquinas redondeadas.
- Canal (parte vacía): un tono 7,5 % más claro (de noche) o más oscuro (de día) que el fondo real de la
  tarjeta, medido en pantalla, con sombra interior (de día: inset 0 2px 5px negro al 13 % y 0 1px 2px al
  9 %; de noche: inset 0 2px 6px negro al 55 % y 0 1px 2px al 40 %). Así encaja con plantillas de
  fondo propio. Quien edite plantillas puede fijar el color del canal. Hasta tener la medida (algo más
  de medio segundo como mucho), la barra no se enseña; luego aparece con un fundido breve.
- Relleno: degradado horizontal de cuatro tonos del tema (0 %, 30 %, 70 %, 100 %), brillo de cristal en
  la mitad de arriba (blanco al 30 % que se desvanece al 55 %), sombra 0 2px 8px de un tono profundo al
  38 %. Sin destello desde la 1.2.0 (antes cruzaba la barra cada 9 s).
- Día o noche se decide por lo oscuro que sea el fondo real de la tarjeta, no solo por el modo de Anki.
  Se repinta al cambiar de modo o de tamaño de ventana.
- La tarjeta deja siempre sitio a la barra y a su aviso: 10 px de margen, el alto de la barra, 24 px
  para el aviso (si las celebraciones están activadas) y 8 px de aire; 58 px con la barra de serie.
  «Espacio extra» (0 a 300 px) se suma.
- Para el lector de pantalla, es una barra de progreso con el valor en palabras («30 de 50 tarjetas»),
  sin anuncios automáticos.

Colores del relleno (no son de la paleta Nocturne; los trae el complemento):

| Tema | Degradado de día | Degradado de noche | Color del aviso (día / noche) | Muestra en Opciones (día) |
|---|---|---|---|---|
| Verde clásico (de serie) | #64D97A, #3DD65A, #25CB44, #1DAF38 | #2DB947, #33D151, #4BD865, #68DC7E | #167628 / #88E098 | #3DD65A |
| Azul océano | #5F87DD, #376BDD, #1E56D2, #1649B6 | #2757BF, #2C62D8, #4575DE, #638AE1 | #12337A / #84A2E4 | #376BDD |
| Turquesa laguna | #5DE0D0, #34DFCC, #1BD5BF, #14B8A5 | #24C1AF, #29DBC6, #42E0CE, #60E3D4 | #107C70 / #82E5DA | #34DFCC |
| Rosa suave | #DD608F, #DB3876, #D11F62, #B41853 | #BE2860, #D72D6D, #DD467F, #E06493 | #791339 / #E385A8 | #DB3876 |
| Púrpura real | #7E60DC, #7450B8, #4B20D0, #3E18B4 | #4D28BD, #572ED6, #6B46DC, #8264E0 | #2C1379 / #9C85E3 | #7450B8 |
| Naranja atardecer | #E0935D, #DF7B34, #D5681B, #B85814 | #C16524, #DB7329, #E18442, #E39660 | #7C3D10 / #E5AB82 | #DF7B34 |
| Dorado (5 o más seguidas) | #E3BD59, #E4B230, #DAA416, #BC8D10 | #C59820, #DFAC25, #E4B73E, #E7C15D | #BC8D10 / #E7C15D | — |

Dorado: además, un halo suave (0 0 6px dorado al 18 % y 0 0 2px al 14 %), rebajado dos veces a
petición del usuario («debe adornar, no llamar la atención»). El aviso dorado lleva un resplandor de 8
px de su color al 45 %.

Nota: los temas comparten nombre con los de GritMap, pero sus tonos son otros. Rojo fuego se retiró en
la 1.2.0, como en GritMap (en Anki el rojo es error); quien lo tenía pasa a Naranja atardecer con aviso.
La muestra de Opciones sale en el tono del modo activo (de noche, el sexto tono de la rampa nocturna).

## 5. Hitos (marcas numeradas)

- Con «Mostrar hitos en la barra» y un total de 10 tarjetas o más: cuatro marcas en el 20, 40, 60 y
  80 %, cada una con su número de tarjetas (con 50: 10, 20, 30 y 40). Con menos de 10, ninguna.
- Números redondeados; si dos coinciden, sale uno.
- Cada marca está donde llega el relleno al despachar ese número.
- Forma: círculo (pastilla si el número es largo), con letra en negrita de 11 a 13 px, un poco más alto
  que la barra. Con la barra por debajo de 14 px, sin número: solo la marca.
- Sin alcanzar: color del canal, número en gris (de día, tinta oscura al 62 %; de noche, gris claro al
  78 %). Al alcanzarla: toma el color del relleno y su número va en blanco (con sombra) o en oscuro
  #1B2430, el que tenga más contraste con el tono del degradado justo detrás. Con «Celebrar rachas y
  récords», además da un pequeño salto (crece durante 0,4 s) y suelta tres chispas blancas.

## 6. Racha y récord

- Racha: respuestas seguidas con «Difícil», «Bien» o «Fácil» en este repaso (aciertos, como los
  entiende Anki). Solo «Otra vez» la pone a cero. Empieza de cero en cada repaso. No se ve como cifra fija.
- Avisos (con «Celebrar rachas y récords»): al llegar a 5, 10, 20, 30… (cada 10 desde 10), debajo de
  la barra y centrado bajo el relleno (se mueve con él), en mayúsculas: «5 ACIERTOS SEGUIDOS». Letra de 13 px,
  negrita, interletraje 0,04 em, con sombra 0 1px 3px negro al 25 %. Desde 5, el relleno se aviva un
  instante y suelta cuatro chispas en su borde.
- El aviso dura 1,5 s y se apaga solo con su fundido; uno nuevo sustituye al anterior.
- Barra dorada: con 5 o más seguidas, relleno y aviso dorados; al romperse, vuelve al tema.
- Récord: racha más larga, propia de cada perfil. Se celebra una vez por repaso, al batirlo (como
  mínimo a las 3): «NUEVO RÉCORD: 11», con avivado y chispas si es de 5 o más. Gana al aviso de racha si
  coinciden.
- Se guarda al batirlo (con efectos) y, en todo caso, al salir del repaso o cerrar el perfil.
- Mazos excluidos: sin celebración ni récord; barra, avisos de racha y dorado siguen. Excluir un mazo
  excluye sus submazos. Cuenta el mazo que se abrió para estudiar.

## 7. Al deshacer

- Deshacer una respuesta: la barra retrocede, la racha pierde esa respuesta, el aviso visible se apaga y
  el récord, si subió en este repaso, baja con ella (nunca por debajo del inicial).
- Deshacer algo que no toca la cola no cambia la racha. Deshacer enterrar o suspender sí le quita una
  (fallo pendiente). Rehacer no devuelve la respuesta.

## 8. Movimiento

- Relleno: avanza deslizándose en 0,4 s; cambios de color en casi 0,5 s; canal, fundidos de 0,3 s.
- Sin animación continua (el destello se retiró en la 1.2.0).
- Saltos de hitos (0,4 s), chispas, avivado, fundido de avisos: todo se apaga con «Celebrar rachas y
  récords», salvo el avance del relleno y el cambio de color, que informan.
- Con «reducir animaciones» del sistema: sin chispas ni fundidos de color; el salto de los hitos sí se
  mantiene.
- Duraciones por encima de la norma del taller (150 ms): excepción aprobada con el informe.

## 9. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «CoreProgress». Tres recuadros:
  1. Línea de dato con acción: «Récord: **7 aciertos seguidos**» (o «Sin récord todavía»; con la
     racha en curso si la supera) y el enlace «Poner a cero» a la derecha (apagado sin récord).
     Pregunta en un diálogo dentro del panel «¿Poner el récord a cero?» con «Poner a cero» y
     «Cancelar» y el foco en «Cancelar»; el borrado solo se aplica al pulsar Aceptar.
  2. Aspecto de la barra, con «Restaurar los valores predeterminados» (y «Deshacer»): seis fichas de
     tema por orden alfabético, en dos columnas, con muestra de 16 px en el tono del modo activo y ✓;
     «Altura de la barra» y «Espacio extra» con «−» y «+» y «px» al lado; dos casillas («Celebrar
     rachas y récords» y «Mostrar hitos en la barra»). Si tenía Rojo fuego, arriba la franja de aviso
     «Su tema «Rojo fuego» se ha retirado; ahora usa «Naranja atardecer».».
  3. Fila de resumen «Mazos que no cuentan para el récord» con los nombres marcados (o «-») y la nota
     gris «Útil para mazos muy fáciles.» debajo; abre una subpágina con buscador y la lista de mazos
     con casillas.
- Los textos de Aceptar, Cancelar y Restaurar son los de Qt en el idioma de Anki.

## 10. Accesibilidad

- La barra no recibe foco ni clics (los atraviesan): no interfiere con el teclado del repaso.
- Movimiento reducido respetado en parte (apartado 8).
- La barra se anuncia como barra de progreso («30 de 50 tarjetas»), sin anuncios automáticos que
  interrumpan la lectura de la tarjeta; los avisos de racha no se anuncian.
- Números de los hitos alcanzados en blanco u oscuro según el contraste con el tono de detrás (el
  blanco solo llegaba a 1,6–4,7 a 1 sobre verde, turquesa, naranja y dorado); de 11 px como mínimo.
- La ventana de opciones sigue el modelo del panel de GritMap, con su teclado y su lector de pantalla.
- Por comprobar: el contraste del relleno frente al canal (3 a 1) y que el paso a dorado se note con
  Naranja atardecer.

## 11. Textos visibles (español)

«5 ACIERTOS SEGUIDOS», «NUEVO RÉCORD: 11», «Récord: 7 aciertos seguidos», «Sin récord todavía»,
«Poner a cero», «¿Poner el récord a cero?», «Celebrar rachas y récords», «Espacio extra», «Mazos que no
cuentan para el récord», «Útil para mazos muy fáciles.», «48 tarjetas · mejor racha: 17», «30 de 50
tarjetas» (lector de pantalla), el aviso del tema retirado y el aviso de fallo de Anki «El problema
podría ser causado por un add-on.». Impersonales desde la 1.2.0 (sin tú ni usted), salvo el aviso del
tema retirado (usted, como GritMap). Formas de plural de cada idioma. 60 idiomas; si falta, inglés.

## 12. Qué guarda

- Opciones: configuración de complementos del ordenador (todos los perfiles, no se sincroniza).
- Récord: en la colección de cada perfil (se sincroniza); no entra en Editar > Deshacer.
- Un valor que falte o no sirva usa el de serie; los números fuera de margen se llevan al límite.

## 13. Fallos conocidos pendientes (decisión de la persona)

- Deshacer algo que no es una respuesta (enterrar, suspender) quita una respuesta a la racha y puede
  bajar el récord.
- La barra lee en el hilo principal la cuenta de pendientes de Anki en cada respuesta (la misma que usa
  Anki para dibujar sus cifras); propuesta pendiente de pasarla a «Así a propósito».

## 14. Decisiones tomadas a propósito

- Desde la 1.2.0 (aprobado con el informe): «Difícil» mantiene la racha; la barra sigue donde se dejó
  y no retrocede salvo al deshacer; sin destello; avisos a las 5, 10, 20, 30… de 1,5 s; textos
  impersonales; ayuda en la lista de mazos; Rojo fuego retirado; barra llena al terminar, sin
  animación; sin mensajes de ánimo al fallar.
- El récord se celebra desde 3 (antes 5). El récord se celebra una vez por repaso y gana al aviso de racha. Se guarda al batirlo y baja
  si se deshace. Rehacer no lo devuelve. Los mazos excluidos solo afectan al récord. El canal toma el
  color del fondo real de la tarjeta. Halo dorado y tonos suavizados a petición del usuario.

## 15. Qué no hace

No se conecta a internet, no cambia el estudio, no muestra la racha como cifra fija ni el récord durante
el repaso, no da mensajes de ánimo al fallar, no aparece fuera del repaso salvo la barra llena de
«¡Enhorabuena!». Ideas descartadas en el informe: racha de días (la lleva GritMap), contador fijo,
puntos e insignias, tiempo estimado (mejor en la pantalla del mazo o en GritMap).
