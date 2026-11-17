# Ficha de diseño: ProFeedback

Versión 2.6.0 (17 de noviembre de 2026). Léase junto con `00-contexto-comun.md`. La 2.6.0 aplica entero el
informe «Rediseño de color y forma: ProFeedback 2.5.0», con la opción recomendada en sus tres decisiones.

## 1. Qué es, en una frase

Hace más agradable el repaso: un sonido corto al acertar y otro, más discreto, al pulsar «Otra vez»,
una insignia encima de la tarjeta (tarjeta nueva, «se resiste» u «otra oportunidad»), botones de
respuesta de colores con relieve y, al terminar un mazo o todo lo del día, un sonido de fin y confeti,
dorado al terminar el día.

## 2. Para quién y para qué

Para dar respuesta inmediata y agradable a cada respuesta y un cierre de sesión celebrado, sin
convertir el repaso en un videojuego. Criterio de la persona: «lo mejor para el aprendizaje». Por eso,
desde la 2.5.0, nada premia la nota que uno se pone (en Anki la pone el propio estudiante): el sonido de
cada tarjeta informa de qué se registró y el premio va al final y premia terminar. Solo lee la
colección; guarda sus opciones.

## 3. Dónde se ve y se oye

- Repaso: insignia encima de la tarjeta, botones de la barra inferior y sonido al responder.
- Pantalla del mazo, al volver del repaso con el mazo terminado («¡Felicitaciones! Has finalizado este
  mazo por ahora.»): sonido de fin y confeti.
- Herramientas > Complementos > ProFeedback > Configuración: ventana de opciones.
- No añade menús ni atajos; no aparece en la lista de mazos, Explorar, editor, vistas previas ni
  estadísticas.

## 4. Sonidos al responder

- «Difícil», «Bien» y «Fácil» son aciertos (manual de Anki): sonido de acierto, dos notas que suben,
  0,4 s.
- «Otra vez»: una nota grave y corta, de la misma familia, 3 dB más baja. Dice «anotado», no «mal».
- Nada suena con «Mostrar respuesta», «Editar» ni «Más».
- Por defecto, el mismo sonido siempre («1 · Madera»): lo que se repite cientos de veces debe ser
  previsible y volverse fondo. «Aleatorio» queda para los finales.
- 18 sonidos de serie, nuevos en la 2.5.0, creados por síntesis aditiva (sin grabaciones): tres voces
  («Madera», tipo marimba; «Campanilla», tipo kalimba; «Suave», piano con sordina), Do mayor
  pentatónica, picos entre −16 y −8 dBFS (8 dB de margen entre el más bajo y el más alto), todos por
  debajo de 3 s. La receta exacta está en el informe 2.4.0, apartado 8.9.
- Reproductor propio, para que el audio de la tarjeta siguiente no lo corte. Los de respuesta acaban
  en unos 0,25 s audibles para no pisar el audio de la tarjeta siguiente.

## 5. Insignias de la tarjeta

Un icono redondo y un texto en mayúsculas, centrados encima del contenido de la tarjeta, sin píldora.
Una sola, por prioridad:

| Insignia | Cuándo | Dibujo del icono | Texto día / noche | Icono día / noche | Dibujo día / noche |
|---|---|---|---|---|---|
| «TARJETA NUEVA» | La tarjeta es nueva | Destello de cuatro puntas de 11 px (el de CoreProgress) | #73428F / #CDA1E9 | #A572C4 / #CDA1E9 | #FFFFFF / #532F67 |
| «SE RESISTE» | Sus tres últimas respuestas fueron «Otra vez» | Pesa, trazo de 2 px | #9B322F / #F9988E | #D3655E / #F9988E | #FFFFFF / #6D2824 |
| «OTRA OPORTUNIDAD» | Alguna de sus dos últimas respuestas fue «Otra vez» | Flecha en bucle, trazo de 2 px | #7A4D07 / #E0A761 | #BA7816 / #E0A761 | #FFFFFF / #593704 |

- Icono: círculo de 24 px de su color con el dibujo encima (SVG con currentColor); 8 px de hueco; letra
  de 14 px en negrita, mayúsculas, 0,06 em entre letras (2.6.0; antes 0,4 px).
- Franja fija de 40 px encima de la tarjeta (24 del icono y 16 de aire), haya insignia o no: la tarjeta
  no cambia de sitio entre una y otra.
- Fundido de 120 ms (solo opacidad). No se puede pulsar ni seleccionar. La misma en pregunta y
  respuesta. Solo cuentan respuestas dadas con un botón.
- Contraste (2.6.0): las tres pesan igual. Texto 6,80 a 6,84 de día y 8,51 a 8,54 de noche; icono de
  día 3,40 a 3,42 contra el fondo; dibujo blanco sobre el icono, 3,6. De día, lejos de las banderas 1 y
  7 de Anki (7,7 y 14,4 de diferencia; antes, 3,8 y 6,0).
- Contraste alto de Windows: círculo vacío con trazo CanvasText de 1,5; dibujo y texto CanvasText.

## 6. Botones del repaso

Con «Botones de colores con relieve» (marcada de serie). Desde la 2.6.0, paleta propia calculada por
contraste en OKLCH (tonos muy cerca de las franjas de respuesta de Atelier), con versión de noche (15 %
menos de croma) y la letra en un tono muy oscuro de su color:

| Botón | Cara día / noche | Letra | Canto (3 px) día / noche | Ratón encima día / noche | Ancho mínimo |
|---|---|---|---|---|---|
| «Otra vez» (coral) | #F47B72 / #E8847B | #2F0405 | #DB655D / #C05F58 | #FD867C / #F38D84 | 130 px |
| «Difícil» (ámbar) | #FDB354 / #F8B564 | #311C01 | #C78112 / #D08F3C | #FEC178 | 130 px |
| «Bien» (jade) | #53E2A6 / #70DDAB | #01291A | #15A472 / #46B686 | #5FECAF / #7AE7B5 | 190 px |
| «Fácil» (cielo) | #73C9FB / #7FC8F3 | #012537 | #4098C9 / #5AA1CB | #88D1FD / #89D1FD | 130 px |
| «Mostrar respuesta» (azul de acción, BUTTON_PRIMARY_BG) | #3B6FE0 / #4066E6 | #FFFFFF | #284EAA / #2B45AA (NOCTURNE_PRIMARY_PRESSED) | #3366D6 / #385CDC (oscurece) | 190 px |
| «Editar» y «Más» | Sin relleno; contorno de 2 px y canto de 3 px NOCTURNE_CONTROL_BORDER | FG_SUBTLE | — | BUTTON_HOVER | 130 px |

- Todos: 48 px de alto (cara de 45 y canto de 3), esquinas de 12 px (las de la tarjeta y Atelier),
  24 px de relleno lateral. Letra del sistema (o «ProFeedback.ttf»), 15 px, negrita, espaciado 0,8 px,
  sin mayúsculas. «Editar» y «Más», separados 40 px a los lados.
- Contraste de la letra: 6,95 a 9,60 de día y 7,03 a 9,46 de noche; «Mostrar respuesta», 4,63 y 4,93
  (5,23 con el ratón encima). Canto contra la barra de día: 3,00 a 3,28. Con protanopía y deuteranopía,
  ningún par de botones baja de 10,8 de diferencia («Difícil»·«Bien», de 2,3 a 17,0).
- «Bien» mide lo mismo que «Mostrar respuesta»: tras pulsar este, el puntero queda dentro de «Bien».
- Raya de 1 px encima de la barra: BORDER.
- Tiempos previstos: FG_SUBTLE, 12 px, cifras tabulares.
- Ratón encima: la cara se aleja de su letra (+0,03 de luminosidad; −0,03 en «Mostrar respuesta»), sin
  filtro de brillo; «Editar» y «Más», relleno BUTTON_HOVER.
- Pulsado: la cara baja 3 px y tapa el canto en 80 ms, sin cambiar de color; vuelve en 70 ms, sin
  rebote. La respuesta sale al soltar dentro del botón. Un segundo clic antes de 0,4 s se ignora.
  Teclado: al instante. Con «reducir movimiento», sin animación.
- Foco de teclado: aro de 2 px BORDER_FOCUS separado 2 px.
- Contraste alto de Windows: ButtonFace y ButtonText, borde de 1 px, sin canto; foco en Highlight.
- Mandan sobre Atelier (FIX-006). Con la casilla desmarcada, los botones son los de Anki o Atelier.
- Por debajo de 640 px, sin ancho mínimo (salvo «Bien» y «Mostrar respuesta») y 12 px de relleno; si
  una palabra no cabe, se reduce la letra. La barra completa necesita unos 1.064 px.

## 7. Celebración al terminar

Solo al volver del repaso a la pantalla del mazo habiendo respondido algo en esa sesión. Si sale por
otro camino (lista de mazos, «Terminar» en el aviso de tiempo), no se celebra. Una respuesta deshecha
deja de contar.

| Celebración | Cuándo | Mínimo para el confeti | Confeti |
|---|---|---|---|
| Mazo | No queda nada en ese mazo, pero sí en otros | 5 respuestas en la sesión | 72 piezas desde dos cañones, 2,4 s, con los colores de los botones |
| Día (prioritaria, una vez al día) | No queda nada en ningún mazo | 20 tarjetas distintas hoy | 120 piezas en lluvia dorada, 3,8 s, y un brillo del título de 1,2 s |

- Ninguna depende de las notas: no hay «perfecta» (opción B del informe 2.4.0).
- Si el día ya se celebró y vuelven tarjetas, se celebra como un mazo.
- Sonido de fin siempre que hay celebración, salvo «Sin sonido». Sin el mínimo, solo sonido.
- Confeti (2.6.0), en un lienzo a pantalla completa que no recibe clics:
  - Formas: tiras de 6 × 14 px con esquinas de 2, círculos de 8 y destellos de cuatro puntas de 12 (los
    de CoreProgress); en la lluvia, también estrellas de cinco puntas de 13. Tamaño ±15 %. Mazo: tiras
    50 %, círculos 25 %, destellos 25 %. Día: 40, 20, 25 y 15 % (estrellas).
  - Mazo: dos cañones a 24 px de las esquinas de abajo, ángulo de 40° a 75°, dos ráfagas en 0,12 s;
    recorrido de 0,40 a 0,85 del alto con frenada exponencial de 0,16 s; caída de 0,14 a 0,24 del alto
    por segundo; vaivén de 6 a 20 px.
  - Día: entra por arriba repartida en 0,9 s; empujón de 0,05 a 0,45 del alto; caída de 0,15 a 0,33 del
    alto por segundo; vaivén de 12 a 38 px.
  - Volteo de papel de 0,6 a 1,4 vueltas por segundo y giro de 60 a 240° por segundo.
  - Desvanecido: de 2,0 a 2,4 s (mazo) y de 3,4 a 3,8 s (día). Empieza con el sonido de fin.
  - Colores del mazo: de día, las cuatro caras y sus cantos; de noche, las caras y su tono de ratón
    encima. Día: de día #E9AC1A y #CB9515 (el doble de veces), #AF8110 y #845E09; de noche #F0BB43,
    #F9CD54 y #FEE06D (el doble) y #FFF0C4.
- Título del fin del día: el oro de CoreProgress, #845E09 de día y #FEE06D de noche. A los 0,3 s lo cruza
  una banda más clara (#926A0C de día, que mantiene 4,6 a 1; #FFF6D6 de noche) en 1,2 s con la curva
  de CoreProgress; después se queda dorado y quieto.
- Con «reducir movimiento»: sin confeti ni brillo; tres destellos fijos de 10 a 12 px encima del título
  (jade, ámbar y cielo en el mazo; dorados en el día, con el título dorado quieto). En el contraste
  alto de Windows, sin confeti ni destellos y el título en CanvasText.

## 8. Ventana de opciones

Sigue `09-patron-configuracion.md`, sin el título repetido dentro (ya está en la barra de la ventana).
Dos recuadros, sin desplazamiento (unos 545 px de alto); cada uno con «Restaurar valores
predeterminados» y «Deshacer» arriba a la derecha:

```
Sonido                                  Restaurar valores predeterminados
Volumen                ━━━━━━━━━━━━━━━━━━━━━━━━○  100 %
Al acertar             [ 1 · Madera              ▾] [Probar]
Al pulsar «Otra vez»   [ 1 · Madera              ▾] [Probar]

Al terminar un mazo    [ Aleatorio               ▾] [Probar]
Al terminar el día     [ Aleatorio               ▾] [Probar]

Aspecto                                 Restaurar valores predeterminados
☑ Botones de colores con relieve
☑ Insignias sobre la tarjeta
☑ Confeti al terminar                                              [Ver]
                                              [Aceptar] [Cancelar]
```

- Filas con la etiqueta a la izquierda (200 px, letra normal), 8 px entre filas y 16 entre los dos
  grupos de sonidos. «Probar» de 76 × 32 px.
- Cada lista: «Sin sonido», los de serie («1 · Madera»…), los propios, «Aleatorio», una raya y «Abrir la
  carpeta de estos sonidos…». No hay casillas de sonido ni nota al pie.
- «Probar»: apagado (FG_DISABLED) con «Sin sonido»; si no consigue sonar, aviso en ACCENT_DANGER con
  icono encima de la fila. Nombre propio para el lector de pantalla en cada uno.
- Enlaces en FG_LINK, subrayados.
- «Ver» (2.6.0), a la derecha de «Confeti al terminar»: suelta el confeti de mazo dentro de la propia
  ventana, sin guardar nada.
- 17 controles de ajuste: deslizador, cuatro listas con su «Probar», tres casillas y «Ver».

## 9. Sonidos y letra propios

- Solo .mp3, en «user_files/sonidos/» del complemento: «correcto», «fallo», «finalizado/mazo» y
  «perfecto-mazo» (fin de mazo), «finalizado/todo» y «perfecto-todo» (fin del día). Se crean vacías al
  abrir las opciones; «Abrir la carpeta…» abre la de cada lista. Uno con el mismo nombre que uno de
  serie lo sustituye.
- Letra: «ProFeedback.ttf» (1,5 MB como mucho) en «user_files». Desde la 2.6.0 sin el alias «Feather
  Bold.ttf» (la letra de Duolingo). Ahora no hay ninguna: letra del sistema.

## 10. Accesibilidad

- Contraste (2.6.0): todo texto a 4,5 a 1 o más y todo contorno a 3 a 1 o más, de día y de noche; los
  iconos de insignia de día también (3,4).
- Foco de teclado visible en la barra (aro separado) y en las opciones.
- Atajos de teclado de Anki (1–4, Espacio) intactos y al instante.
- Iconos de insignia ocultos al lector de pantalla (el texto basta).
- Color nunca solo: cada botón y cada insignia llevan su texto. Con protanopía y deuteranopía, los
  cuatro botones se distinguen (10,8 o más). Con tritanopía, «Bien» y «Fácil» quedan a 7,1 de día y 6,2
  de noche: se notan juntos y llevan palabra.
- Movimiento: nada se mueve durante el repaso más de 150 ms salvo el botón pulsado; al terminar, nada
  dura más de 3,8 s; ninguna pieza parpadea más de 3 veces por segundo.
- Pendiente de comprobar: si el lector de pantalla lee la insignia al aparecer la tarjeta.

## 11. Textos visibles (español)

Insignias: «TARJETA NUEVA», «SE RESISTE», «OTRA OPORTUNIDAD» (54 idiomas). Opciones: los del apartado
8, «Ver», «Sin sonido», «Aleatorio», «Abrir la carpeta de estos sonidos…», «No se pudo reproducir. Compruebe
la salida de audio del equipo.». Fallo: «ProFeedback no pudo mostrar la insignia / pintar los botones /
reproducir el sonido / celebrar el final. Anki sigue funcionando. El detalle está en el registro del
complemento.» (5 s, una vez por función y sesión). Ventana y avisos completos en nueve idiomas
(español, inglés, portugués de Brasil y de Portugal, catalán, gallego, francés, italiano, alemán); en
el resto, en inglés. Los textos de los botones del repaso son los de Anki. Trato de usted, sin
exclamaciones.

## 12. Qué guarda

Opciones en la configuración de complementos del ordenador (todos los perfiles, no se sincroniza);
tamaño y posición de la ventana, en el perfil. Nada en la colección.

## 13. Fallos conocidos pendientes

- Elegir la insignia lee el historial de la tarjeta mientras Anki espera (pequeño; no medido).

## 14. Decisiones tomadas a propósito

- Informe 2.4.0 (aplicado entero, 2026-11-16): «Difícil» es acierto; el oro premia terminar el día
  (opción B); «Bien» de 190 px; «SE RESISTE» y «OTRA OPORTUNIDAD»; confeti de 4 s y un brillo;
  sonidos fijos en las respuestas y variados al final; respuesta al soltar, sin espera.
- Informe del 2026-11-17 (aplicado entero, 2.6.0): «Mostrar respuesta» en el azul de acción (decisión
  1, A); paleta propia de botones en lugar de la de Duolingo (decisión 2); esquinas de 12 y canto de 3
  (decisión 3); además, insignias, confeti, título, ratón encima, raya, tiempos, sin «Feather Bold.ttf»,
  destellos fijos, contraste alto y «Ver». El oro solo celebra haber terminado.
- Se quedan: las cuatro familias de color, el relieve, los mínimos de confeti (5 y 20), la
  prioridad de la celebración del día, el reproductor propio, el estilo dentro de la página del
  repaso, el filtro del doble clic y el .mp3 con sus seis carpetas.
- No se añaden (informe 2.4.0, 7.4, y del 2026-11-17, 7.3): rachas, puntos o niveles; sonido en
  «Mostrar respuesta»; mensajes de ánimo tras cada respuesta; más colores; más celebraciones o premios
  sorpresa; movimiento durante el repaso; degradados en los botones; oro en cualquier otra pieza; un
  personaje o mensajes en el confeti.
- Restaurar por recuadro (modelo de opciones), no uno solo abajo.

## 15. Qué no hace

No se conecta a internet, no cambia la colección, no premia la nota que uno se pone, no celebra si se
sale por otra pantalla, no pone insignias en vistas previas ni editor, no añade menús ni atajos.
