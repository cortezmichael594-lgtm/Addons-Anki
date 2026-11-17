# Ficha de diseño: CoreProgress

Versión 1.6.1 (17 de noviembre de 2026). Léase junto con `00-contexto-comun.md`. Es un complemento que
la persona trajo hecho fuera del taller; la 1.2.0 aplica entero el primer informe de diseño de
CoreProgress (interfaz, aprendizaje y hábito, 9 de noviembre de 2026) y la 1.5.0, el informe «Rediseño
de color y forma: CoreProgress 1.4.0» (17 de noviembre de 2026), también entero. Los colores de los
temas son propios, fuera de la paleta Nocturne, y están aprobados.

## 1. Qué es, en una frase

Una barra de progreso fija arriba de la pantalla de repaso que se llena a medida que se despacha todo
lo de hoy en el mazo (lo hecho más lo que queda), con cortes por el camino, el número del próximo hito y
el total; además cuenta los aciertos
seguidos, los celebra con un aviso breve, vuelve dorada la barra desde 5 seguidos y guarda el récord
personal.

## 2. Para quién y para qué

Para ver cuánto falta en una sesión de repaso y motivarse con pequeños logros (hitos, rachas, récord).
Solo lee la cuenta de tarjetas que muestra Anki y lo respondido hoy; guarda sus opciones y el récord.

## 3. Dónde se ve

- En la pantalla de repaso, también en mazos filtrados y estudio personalizado.
- Herramientas > Complementos > CoreProgress > Configuración: su ventana de opciones.
- No aparece en la lista de mazos, la pantalla de un mazo (tampoco la de «¡Enhorabuena!»: desde la
  1.4.0, retirada a petición de la persona), Explorar (ni su vista previa), plantillas,
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
- Se pone al día 50 ms después de cada respuesta o cambio (1.5.0; antes, 120).
- Si la cuenta de Anki sube (vencen tarjetas en aprendizaje), la barra se queda quieta hasta que el
  avance la alcance; solo retrocede al deshacer.
- Al terminar, Anki sale del repaso y la barra desaparece con él.

Posición y forma:

- Fija arriba, 10 px por debajo del borde. Ancho a elegir (1.6.0, petición de la persona): «Tarjeta»
  (de serie), 710 px como mucho (1.6.1, petición de la persona), centrada; o «Ventana», de lado a lado con 18 px a cada lado. Por
  encima de la tarjeta; no se mueve al desplazarse. Los clics la atraviesan.
- Franja opaca detrás de la barra, de lado a lado, del color del fondo de la tarjeta (10 px arriba, el
  alto de la barra y 8 abajo): al bajar por una tarjeta larga el contenido se corta limpio bajo ella
  (1.6.0, petición de la persona con capturas). Sin bajar, no tapa nada.
- Grosor: Fina 12 px, Normal 16 (de serie), Gruesa 20. Canal, relleno, discos y aviso en forma de
  píldora (radio = mitad del alto); los cortes de hito, rectos.
- Canal (parte vacía), plano y sin sombra (1.5.0): sobre el fondo de Atelier (#F7F8FA / #12161F),
  #D5D9E2 de día y #272F3F de noche (1,33 y 1,35 a 1 del fondo); sobre otro fondo, un gris con ese
  mismo contraste, calculado en pantalla. Quien edite plantillas puede fijar el color del canal. Hasta
  tener la medida (algo más de medio segundo como mucho), la barra no se enseña.
- Relleno: degradado de tres tonos del tema (0 %, 50 %, 100 %), plano, sin contorno ni brillo ni
  sombra (1.5.0). Siempre al menos tan ancho como alto, también con 0 tarjetas. Sin destello.
- Día o noche se decide por lo oscuro que sea el fondo real de la tarjeta, no solo por el modo de Anki.
  Se repinta en su sitio, sin animación, al cambiar de modo o de tamaño de ventana; al entrar a
  repasar o al cambiar las opciones se dibuja ya en su sitio, sin deslizarse desde cero.
- La tarjeta deja siempre sitio a la barra y a su aviso: 10 px de margen, el alto de la barra, 24 px
  para el aviso (si las celebraciones están activadas) y 8 px de aire; 58 px con la barra de serie.
  «Espacio extra» (0 a 300 px) se suma.
- Para el lector de pantalla, es una barra de progreso llamada «Progreso de hoy» con el valor en
  palabras («30 de 50 tarjetas»; con 5 aciertos seguidos o más, «…; 7 aciertos seguidos»), sin anuncios
  automáticos.
- Contraste alto de Windows (1.5.0): canal Canvas con borde CanvasText; relleno Highlight; cortes
  Canvas; próximo hito con fondo Canvas, aro de 2 px Highlight y número CanvasText; total con aro de
  1 px CanvasText; estrella HighlightText; aviso con fondo Canvas, borde y texto CanvasText; sin chispas.

Colores (1.5.0; no son de la paleta Nocturne, los trae el complemento). Una sola receta para todos,
calculada en OKLCH por contraste: de día, la punta del relleno a 3,1 a 1 del canal y el arranque a
2,0; de noche, a 7,0 y 4,6; croma de 0,16 como máximo de día y 0,15 de noche; ningún tono a menos de
10 (ΔE2000) del azul de acción. La tinta (texto del aviso, aro y número del próximo hito, chispas) es
oscura de día (6,5 a 1 contra el fondo) y, de noche, la propia punta. La píldora es el fondo del aviso.

| Tema | Relleno de día (arranque · centro · punta) | Tinta de día | Píldora de día | Relleno de noche (la punta es la tinta) | Píldora de noche |
|---|---|---|---|---|---|
| Verde clásico (de serie) | #53AD4B · #329D43 · #0F8B41 | #09692F | #E3F6E6 | #3EAC5F · #5EBD68 · #7BCE73 | #1C3422 |
| Turquesa laguna | #17ACA0 · #139992 · #108784 | #096462 | #DAF7F5 | #16A8A5 · #1ABCB4 · #1ED1C2 | #0B3534 |
| Azul océano | #16A4DB · #1391CC · #0F7FBE | #085E8F | #E3F2FF | #219EE9 · #26B3F9 · #53C7FD | #183042 |
| Púrpura real | #B283F0 · #9B74E1 · #8466D1 | #634C9F | #F1EEFF | #A187EE · #B897FD · #CCADFD | #2F2942 |
| Rosa suave | #EE7098 · #D95F8F · #C44E85 | #943A64 | #FFEAF1 | #E372A3 · #F883AE · #FDA0BA | #3F242F |
| Naranja atardecer | #E58018 · #D66B12 · #C7570F | #96400A | #FFECE3 | #E67A43 · #F68E4A · #FDA863 | #40261A |
| Dorado (5 o más seguidas) | #F7D856 · #F6C835 · #F4B81C | #845E09 | #FDEFCF | #F0BB43 · #F9CD54 · #FEE06D | #3C2E0F |

Dorado: claro, más que cualquier tema (se distingue también por la luminosidad con daltonismo). Sin
halo desde la 1.5.0. De día lleva un contorno de 1 px en #845E09 (sin él quedaría a 1,27 del canal; con
él, 4,14). En la punta, una estrella de cinco puntas del alto de la barra menos 5 px (8 px como mínimo):
#845E09 de día y el color del fondo de noche (3,27 y 13,87 a 1).

Piezas neutras (día / noche): fondo y color de los cortes #F7F8FA / #12161F (CANVAS); disco
#FBFCFE / #212836 (CANVAS_ELEVATED); aro del total #646C7D / #9AA3B4 (FG_FAINT); número del total
#4E576A / #B7BECC (FG_SUBTLE); número sobre la tinta #FBFCFE / #12161F.

Nota: los temas comparten nombre con los de GritMap, pero sus tonos son otros. Rojo fuego se retiró en
la 1.2.0, como en GritMap (en Anki el rojo es error); quien lo tenía pasa a Naranja atardecer con aviso.

## 5. Hitos

- Con «Mostrar hitos en la barra» y un total de 10 tarjetas o más: hitos en números redondos (1.3.0).
  Paso: el menor de 5, 10, 20, 25, 50, 100, 200, 250, 500, 1.000… que deja cinco o menos; ninguno más
  allá del 92 % del ancho. Con 27: 5, 10, 15, 20; con 50: 10, 20, 30, 40; con 130: 20, 40, 60, 80,
  100. Al final, el total («27»). Con menos de 10, ninguno. El paso se fija al entrar a repasar.
- Cada hito está donde llega el relleno al despachar ese número.
- Tres piezas (1.5.0; antes, un disco numerado por hito):
  - Hito pasado y hito lejano (detrás del próximo): corte de 2 px del color del fondo, de arriba abajo
    de la barra, sin número.
  - Próximo hito: disco del alto de la barra más 4 px, fondo CANVAS_ELEVATED, aro de 2 px y número en
    la tinta, centrado en su posición.
  - Total: disco igual, aro de 1,5 px FG_FAINT y número FG_SUBTLE, con su borde derecho en el final del
    canal. Cuando ya no queda hito intermedio, pasa a ser el próximo y toma el color.
- Números: 11 px (12 con la barra de 20), seminegrita, cifras tabulares; pastilla si tiene 3 cifras o
  más.
- Al alcanzar un hito (con «Celebrar rachas y récords» y si la respuesta no trae aviso): el disco se
  llena de tinta con el número en #FBFCFE de día o en el fondo de noche, crece a 1,15 en 0,15 s, se
  queda 0,3 s y pasa a corte en 0,15 s; tres chispas; el disco del hito siguiente aparece después, en
  0,2 s. Si no, pasa a corte sin más.
- Barra Fina (12 px): sin discos; el próximo hito es un corte de 3 px en la tinta y el final del canal
  es el total.

## 6. Racha y récord

- Racha: respuestas seguidas con «Difícil», «Bien» o «Fácil» en este repaso (aciertos, como los
  entiende Anki). Solo «Otra vez» la pone a cero. Empieza de cero en cada repaso. No se ve como cifra fija.
- Avisos (con «Celebrar rachas y récords»): al llegar a 5, 10, 20, 30… (cada 10 desde 10), en la franja
  de 24 px bajo la barra, centrado sobre la barra y quieto, en mayúsculas: «5 ACIERTOS SEGUIDOS». Desde
  la 1.5.0, en una píldora de 20 px de alto (radio 10, 12 px de margen a los lados, 4 px bajo la barra)
  con el fondo tintado del tema y el texto en su tinta (6,00 a 1 o más); letra de 12,5 px, negrita,
  interletraje 0,06 em. Desde 5, tres chispas desde la punta del relleno; el relleno ya no se aviva.
- El aviso dura 1,5 s (entrada de 150 ms y salida de 300 ms); uno nuevo sustituye al anterior.
- Mejor racha de los últimos 30 días (1.3.0): se celebra una vez por repaso al superarla (desde 3):
  «MEJOR RACHA EN 30 DÍAS: 42». Se guarda la mejor racha de cada día de los últimos 30.
- Una sola celebración por respuesta: récord, mejor de 30 días, racha y, si no hay ninguna, el salto del
  hito.
- Barra dorada: con 5 o más seguidas, relleno, aviso (píldora dorada) y próximo hito dorados, con la
  estrella en la punta; al romperse, vuelve al tema en 0,4 s y la estrella se va con el color.
- Récord: racha más larga, propia de cada perfil. Se celebra una vez por repaso, al batirlo (como
  mínimo a las 3): «NUEVO RÉCORD: 11», con chispas si es de 5 o más. Gana al aviso de racha si
  coinciden.
- Se guarda al batirlo (con efectos) y, en todo caso, al salir del repaso o cerrar el perfil.
- Mazos excluidos: sin celebración de récord ni de mejor de 30 días y sin guardarlos; barra, avisos de
  racha y dorado siguen. Excluir un mazo
  excluye sus submazos. Cuenta el mazo que se abrió para estudiar.

## 7. Al deshacer

- Deshacer una respuesta: la barra retrocede, la racha pierde esa respuesta, el aviso visible se apaga y
  el récord, si subió en este repaso, baja con ella (nunca por debajo del inicial).
- Deshacer algo que no toca la cola no cambia la racha. Deshacer enterrar o suspender sí le quita una
  (fallo pendiente). Rehacer no devuelve la respuesta.

## 8. Movimiento

- Relleno: avanza en 0,3 s con frenada al final (cubic-bezier(.2, .8, .2, 1)); cambio a oro y vuelta,
  0,4 s, solo el color; canal, fundido de 0,3 s si se corrige su color. Avisos: entrada de 150 ms,
  1,05 s quieto y salida de 300 ms.
- Hito alcanzado: 0,6 s en total (crece, se queda, pasa a corte); chispas de 0,5 s; disco siguiente,
  0,2 s.
- Chispas: tres, de cuatro puntas, de 7 a 9 px, en la tinta; suben 8 px y se apagan.
- Sin animación continua ni avivado del relleno, ni halo (1.5.0). Una sola cosa en movimiento por
  celebración, en el sitio donde ocurre.
- Hitos, chispas y fundido de avisos se apagan con «Celebrar rachas y récords», salvo el avance del
  relleno y el cambio de color, que informan.
- Con «reducir animaciones» del sistema: nada se anima; el relleno salta, el hito pasa a corte, el oro
  aparece de golpe, sin chispas y el aviso aparece y desaparece sin fundido.
- Duraciones por encima de la norma del taller (150 ms): excepción aprobada con los informes.

## 9. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «CoreProgress» solo en la barra de la ventana (1.3.0). Dos recuadros, sin desplazar (unos 646
  px de alto):
  1. Aspecto de la barra: vista previa (rectángulo de 44 px del color de fondo de las tarjetas con una
     barra al 60 % como la del repaso: cortes en 10, 20 y 30, próximo hito 40 y total 50; cambia al
     instante con el tema, el grosor y la casilla de hitos; decorativa); «Tema de color» con «Restaurar
     los valores predeterminados» (y «Deshacer») a la derecha en su misma fila; seis fichas de 32 px por
     orden alfabético, en dos columnas, con muestra en minibarra de 30 × 10 px (radio 5) con el
     degradado del modo activo, sin contorno (1.5.0); la elegida con tinte, un solo borde de 2 px
     BORDER_FOCUS y ✓ en FG_LINK (con el foco del teclado, el borde pasa a 4 px); «Grosor» (control
     segmentado del panel modelo: Fina, Normal, Gruesa; el elegido con fondo de capa elevada, borde de
     acción y seminegrita; 1.5.0) y «Ancho» (segmentado: Tarjeta, Ventana; 1.6.0) en paralelo; debajo,
     en una fila, las dos casillas a la izquierda y «Espacio extra» (con «−» y «+» y «px · 0–300») a
     la derecha (1.6.1); dos
     casillas, 12 px entre ellas: «Mostrar hitos en la barra» y «Celebrar rachas y récords». Si tenía
     Rojo fuego, arriba la franja de aviso.
  2. El récord entero: «Récord: **7 aciertos seguidos**» o «Mejor racha en 30 días: **41** · récord:
     90» (o «Sin récord todavía»; con la racha en curso si la supera) y «Poner a cero» a la derecha (no
     se enseña sin récord), con la pregunta «¿Poner el récord a cero?» y el foco en «Cancelar»; debajo,
     la fila «Mazos que no cuentan para el récord» con los nombres marcados (o «Ninguno») y la nota gris
     «Útil para mazos muy fáciles.»; abre una subpágina con buscador («Ningún mazo coincide.») y la
     lista de mazos con casillas.
- Enlaces en FG_LINK y subrayados. Signo «−» o «+» en el límite, en FG_DISABLED. Aceptar y Cancelar de
  88 px como mínimo, alineados con los recuadros. Anillo de foco solo con el teclado.
- Los textos de Aceptar, Cancelar y Restaurar son los de Qt en el idioma de Anki.

## 10. Accesibilidad

- La barra no recibe foco ni clics (los atraviesan): no interfiere con el teclado del repaso.
- Movimiento reducido respetado del todo (apartado 8).
- La barra se anuncia como «Progreso de hoy», barra de progreso («30 de 50 tarjetas»; con 5 aciertos
  seguidos o más, también la racha), sin anuncios automáticos que interrumpan la lectura de la tarjeta;
  los avisos de racha no se anuncian.
- Contrastes (1.5.0): punta del relleno a 3,08 o más del canal de día y 6,98 o más de noche, sin
  contorno; todo texto a 5,14 a 1 o más; aro del próximo hito a 4,14 o más; números de 11 px como
  mínimo.
- La ventana de opciones sigue el modelo del panel de GritMap, con su teclado y su lector de pantalla.
- Daltonismo (1.5.0): el oro, mucho más claro que los temas, se separa de Verde clásico en todos los
  tipos simulados (18,0 y 24,8 de diferencia de día con protanopía y deuteranopía), y la estrella dice
  «racha dorada» por la forma. Naranja atardecer de noche con deuteranopía queda justo (9,7): ahí
  trabaja la estrella.

## 11. Textos visibles (español)

«5 ACIERTOS SEGUIDOS», «NUEVO RÉCORD: 11», «Récord: 7 aciertos seguidos», «Sin récord todavía»,
«Poner a cero», «¿Poner el récord a cero?», «Celebrar rachas y récords», «Grosor», «Fina», «Normal»,
«Gruesa», «Espacio extra», «Mazos que no
cuentan para el récord», «Útil para mazos muy fáciles.», «30 de 50
tarjetas» (lector de pantalla), el aviso del tema retirado y el aviso de fallo de Anki «El problema
podría ser causado por un add-on.» con «CoreProgress: » delante, «MEJOR RACHA EN 30 DÍAS: 42», «Mejor
racha en 30 días: 41 · récord: 90», «Ninguno», «Ningún mazo coincide.», «Progreso de hoy» (lector de
pantalla). Impersonales desde la 1.2.0 (sin tú ni usted), salvo el aviso del
tema retirado (usted, como GritMap). Formas de plural de cada idioma. 60 idiomas; si falta, inglés.

## 12. Qué guarda

- Opciones: configuración de complementos del ordenador (todos los perfiles, no se sincroniza).
- Récord y mejor racha de cada día de los últimos 30: en la colección de cada perfil (se sincroniza); no
  entran en Editar > Deshacer.
- Un valor que falte o no sirva usa el de serie; los números fuera de margen se llevan al límite, y un
  grosor de una versión anterior, al tamaño más cercano.

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
  color del fondo real de la tarjeta (desde la 1.5.0, el gris de Atelier sobre su fondo).

- Informe del 2026-11-16 (aplicado entero, 1.3.0): mejor racha de 30 días (decisión 1), hitos redondos
  con marca final (decisión 2), relleno plano (decisión 3), sin cabecera repetida (decisión 4). Se
  quedan: los degradados y colores de aviso de los temas, el canal, la lógica de la barra y de la
  racha, los avisos y sus textos, el dorado desde 5, el diálogo de confirmación al poner a cero.
- 1.4.0 (2026-11-17, petición de la persona): se quita del todo la barra llena y la línea de resumen
  de la pantalla de «¡Enhorabuena!». No volver a proponer nada de CoreProgress en esa pantalla.
- Informe del 2026-11-17 (aplicado entero, 1.5.0), con la opción recomendada en sus tres decisiones:
  barra de 720 px centrada (1), cortes con número solo en el próximo hito y el total (2), estrella sin
  halo en la racha dorada (3). Además: paleta nueva calculada por contraste, sin contorno salvo el oro
  de día, canal gris plano, aviso en píldora, movimiento de 0,3 s con frenada, tres grosores y muestras
  en minibarra. Se quedan: la lógica, los nombres y el orden de los temas, Verde clásico de serie, los
  textos, una celebración por respuesta y su orden.
- 1.6.0 (petición de la persona): ancho elegible y franja opaca detrás de la barra. No volver a
  proponer un ancho único.
- Al aplicarlo (1.5.0): el canal es el gris medido en el informe (#D5D9E2 / #272F3F), no el
  SCROLLBAR_BG actual de Atelier, que es más oscuro desde la 3.9.0; el grosor elegido va como el
  control segmentado del panel modelo (capa elevada y borde de acción), no relleno de azul; el número
  sobre la tinta es #FBFCFE, no blanco puro.
- No se añaden (informes del 2026-11-16, 7.3, y del 2026-11-17, 7.3): porcentaje o «15/27» fijo,
  sonido propio, más niveles de color, un segundo color para hitos alcanzados, brillo o franja clara
  sobre el relleno, animación en reposo (latido o brillo que recorre la barra).

## 15. Qué no hace

No se conecta a internet, no cambia el estudio, no muestra la racha como cifra fija ni el récord durante
el repaso, no da mensajes de ánimo al fallar, no aparece fuera del repaso (la barra llena y
el resumen de «¡Enhorabuena!» se retiraron en la 1.4.0 a petición de la persona: no proponerlos de nuevo). Ideas descartadas en el informe: racha de días (la lleva GritMap), contador fijo,
puntos e insignias, tiempo estimado (mejor en la pantalla del mazo o en GritMap).
