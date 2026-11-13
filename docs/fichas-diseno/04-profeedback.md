# Ficha de diseño: ProFeedback

Versión 2.3.0 (13 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Hace más agradable el repaso: un sonido al responder «Bien» o «Fácil» y otro con «Otra vez» o
«Difícil», una insignia encima de la
tarjeta (tarjeta nueva, ejercicio difícil o error anterior), botones de respuesta de colores con
relieve y, al terminar un mazo o todo lo del día, un sonido de fin y confeti, dorado si no hubo
fallos.

## 2. Para quién y para qué

Para dar respuesta inmediata y gratificante a cada acierto y un cierre de sesión celebrado, al estilo
de las aplicaciones de idiomas con gamificación. Solo lee la colección; guarda sus opciones.

## 3. Dónde se ve y se oye

- Repaso: insignia encima de la tarjeta, botones de la barra inferior y sonido al acertar.
- Pantalla del mazo, al volver del repaso con el mazo terminado («¡Felicitaciones! Has finalizado este
  mazo por ahora.»): sonido de fin y confeti.
- Herramientas > Complementos > ProFeedback > Configuración: ventana de opciones.
- No añade menús ni atajos; no aparece en la lista de mazos, Explorar, editor, vistas previas ni
  estadísticas.

## 4. Sonidos al acertar y al fallar

- «Bien» o «Fácil» (ratón o teclado): suena un sonido corto de acierto.
- «Otra vez» o «Difícil» (2.2.0): suena un sonido corto de fallo, si su casilla está marcada (de
  serie, sí). Dos sonidos de serie creados para el complemento (grave, suave); «Aleatorio» por defecto.
- Tres sonidos de serie (good, magic, soft). De serie, «Aleatorio»: uno distinto del anterior cada vez.
- Reproductor propio, para que el audio de la tarjeta siguiente no lo corte.

## 5. Insignias de la tarjeta

Una píldora centrada encima del contenido de la tarjeta, con icono y texto en mayúsculas. Una sola, por
prioridad:

| Insignia | Cuándo | Color (token) | Día | Noche |
|---|---|---|---|---|
| «TARJETA NUEVA» | La tarjeta es nueva (también si se reinició) | FLAG_7 (morado, 2.3.0; antes STATE_NEW) | #7048E8 | #9680D6 |
| «EJERCICIO DIFÍCIL» | Sus tres últimas respuestas fueron «Otra vez» | FLAG_2 (naranja) | #E8590C | #C07F3A |
| «ERROR ANTERIOR» | Alguna de sus dos últimas respuestas fue «Otra vez» (también hoy) | ACCENT_DANGER | #CA2D2D | #F37777 |

Aspecto de la píldora:

- Fondo: el color de la insignia al 12 % sobre transparente. Borde de 1 px: el color al 40 %. Esquinas
  totalmente redondas.
- Texto e icono: de día, el color mezclado al 82 % con el color del texto (FG), para oscurecerlo y que
  se lea; de noche, el color tal cual.
- Letra: la del sistema (o una propia, apartado 9), 0,78 rem, negrita, interlineado 1, mayúsculas.
  Icono de 26 px dibujado en el mismo color que el texto; alto de la píldora 1,7 em.
- Ocupa su sitio encima de la tarjeta (la empuja un poco abajo). Aparece con un fundido de 140 ms
  (opacidad y un desplazamiento de 2 px hacia abajo). No se puede pulsar ni seleccionar.
- La misma insignia en pregunta y respuesta. Solo cuentan respuestas dadas con un botón.

## 6. Botones del repaso

Con «Botones de respuesta 3D de colores» (marcada de serie):

| Botón | Color base (token) | Día | Noche |
|---|---|---|---|
| «OTRA VEZ» | ACCENT_DANGER | #CA2D2D | #F37777 |
| «DIFÍCIL» | FLAG_2 | #E8590C | #C07F3A |
| «BIEN» | ACCENT_NOTE | #257A35 | #57D06B |
| «FÁCIL» | ACCENT_CARD | #186CB9 | #7EBFF4 |
| «MOSTRAR RESPUESTA» | BUTTON_PRIMARY_BG, canto BUTTON_PRIMARY_GRADIENT_END | #3B6FE0 / #2F5BC7 | #4066E6 / #3452C8 |
| «Editar» y «Más» | BUTTON_BG, borde interior de 1,5 px BORDER, canto BORDER_STRONG, letra FG_SUBTLE | #FBFCFE | #242C3A |

- Relleno de los cuatro de respuesta: de día, el color mezclado al 82 % con el texto (FG), más oscuro,
  con letra blanca (HIGHLIGHT_FG); de noche, el color vivo al 100 % con letra oscura (CANVAS, #12161F).
- Brillo fino arriba (1 px por dentro, HIGHLIGHT_FG al 22 %) y canto inferior de 4 px (2.3.0; antes 3) que da relieve: el color mezclado al 52 % con un tono de sombra (FG de día,
  CANVAS_INSET de noche).
- Medidas: 128 × 44 px los de respuesta, 160 px «Mostrar respuesta»; esquina de 14 px; letra de 13,5 px,
  negrita, interlineado 1,15, mayúsculas. Todos del mismo tamaño en todos los idiomas: si una palabra no
  cabe, se reduce la letra, nunca el botón. Fila centrada.
- Ventanas de menos de 760 px: 104 px (130 «Mostrar respuesta»), letra 12 px, márgenes 10/4/14 px.
  Menos de 560 px: 82 × 40 px (104 «Mostrar respuesta»), letra 11 px, esquina 12 px.
- «Editar» y «Más»: discretos, con letra gris; al pasar el ratón, como los demás.
- Tiempos previstos («10 min», «4 d») y recuento de tarjetas encima de los botones, en gris (FG_SUBTLE),
  11,5 px, peso 500, sin mayúsculas.
- Al pasar el ratón, se aclaran un poco (brillo 1,06) y se elevan 1 px; nunca se oscurecen (2.3.0). Al
  pulsar con el ratón, se hunden 3 px sobre su canto (el canto baja a 1 px, 70 ms) y la respuesta llega a Anki 0,1 s después, para que se vea el gesto. Con el
  teclado, al instante. Un segundo clic en el mismo botón antes de 0,4 s se ignora.
- Movimiento: solo desplazamiento, 100 ms.
- Su forma y sus colores mandan aunque Atelier esté instalado (FIX-006, 2.3.0): sin el borde, las
  esquinas pequeñas, la raya de color ni el oscurecido con el ratón que Atelier pone a los botones
  de estudio. Con la casilla desmarcada, los botones son los de Anki o Atelier.

## 7. Celebración al terminar

Solo al volver del repaso a la pantalla del mazo habiendo respondido algo en esa sesión. Si sale por
otro camino (lista de mazos, «Terminar» en el aviso de tiempo), no se celebra.

| Celebración | Cuándo | Mínimo para el confeti | Es «perfecta» si… | Confeti |
|---|---|---|---|---|
| Mazo | No queda nada en ese mazo, pero sí en otros | 5 respuestas en la sesión | Todas «Bien» o «Fácil» | Dos cañones desde las esquinas de abajo |
| Todos los mazos (prioritaria) | No queda nada en ningún mazo | 20 tarjetas distintas hoy | Ninguna tarjeta de hoy con «Otra vez» o «Difícil» | Lluvia desde arriba durante 7 s |

- Lo que queda se cuenta como Anki, con sus límites diarios. Puede celebrarse otra vez el mismo día si
  vuelven tarjetas de aprendizaje.
- El sonido de fin suena siempre que hay celebración (si está activado). Sin el mínimo, solo sonido.
- Confeti normal: colores de la paleta: ACCENT_DANGER, FLAG_2, ACCENT_NOTE, ACCENT_CARD, STATE_MARKED
  (#7048E8 / #9680D6) y FLAG_5 (#C62FAD / #B378C1).
- Perfecta: sonido «perfecto» de su tipo; confeti dorado (mezclas de STATE_BURIED #9A7B3F / #A98754,
  FLAG_2 y blanco) y el título de la pantalla del mazo brilla en dorado: un degradado de STATE_BURIED a
  FLAG_2 que lo recorre dos veces, 3,6 s cada una, con una sombra suave.
- El confeti pasa por encima de todo sin tapar: se puede seguir pulsando. Desaparece solo.
- La decisión se toma sin congelar Anki.

## 8. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «ProFeedback». Cuatro recuadros, sin «Restaurar»:
  1. Volumen: deslizador de 0 a 100 (carril hundido de 6 px, tramo lleno del color de acción hasta el
     valor, tirador redondo de 18 px con el borde de los controles) y la cifra «100 %» al lado, en
     seminegrita.
  2. «Sonidos al responder»: casilla de acierto y, colgando de ella, la lista desplegable «Sonido»
     («Aleatorio» primero) con el botón secundario «Probar» al lado; debajo, igual, la casilla
     «Reproducir sonido al fallar (Otra vez/Difícil)» con su lista y su «Probar» (2.2.0).
  3. «Sonidos al finalizar»: casilla y cuatro listas con su «Probar» (mazo, todos, mazo perfecto,
     todos perfecto).
  4. «Aspecto»: tres casillas (confeti, botones 3D, insignias) y la nota gris sobre sonidos propios,
     que nombra las seis subcarpetas.
- Lo que cuelga de una casilla desmarcada se ve atenuado al 45 %; una lista sin sonidos de su tipo,
  también. «Probar» suena con el volumen del deslizador sin guardar; Cancelar devuelve el volumen.
- La ventana es invisible hasta que el panel está dibujado y con su alto; aparece de una vez, sin
  destello (2.2.0).

## 9. Sonidos y letra propios

- Solo .mp3. Los propios, en «user_files/sonidos/» del complemento, en subcarpetas «correcto»,
  «fallo», «finalizado/mazo», «finalizado/todo», «perfecto-mazo» y «perfecto-todo» (se crean vacías al abrir las opciones). Uno con
  el mismo nombre que uno de serie lo sustituye.
- Letra: un archivo «ProFeedback.ttf» o «Feather Bold.ttf» (1,5 MB como mucho) en «user_files» hace que
  botones e insignias la usen. Ahora no hay ninguno: letra del sistema.

## 10. Accesibilidad

- Foco de teclado: contorno de 2 px BORDER_FOCUS (#3B6FE0 / #6390FF) separado 3 px del botón.
- Atajos de teclado de Anki (1–4, Espacio) intactos y al instante.
- Contraste de los botones: de día se oscurece el color (82 % con el texto) para que el blanco se lea;
  de noche, letra oscura sobre el color vivo.
- Los iconos de las insignias están ocultos al lector de pantalla (el texto basta).
- Color nunca solo: cada botón y cada insignia llevan su texto.
- Movimiento reducido del sistema: sin fundido de insignias, sin hundimiento retardado (respuesta al
  instante), sin confeti; en una celebración perfecta, el título queda dorado sin moverse.
- Excepción aprobada: confeti (hasta 7 s) y brillo (2 × 3,6 s) duran más que la norma del taller porque
  son la función del complemento.
- Puntos débiles: los sonidos no tienen alternativa visual (salvo el confeti); la celebración no se
  anuncia al lector de pantalla.

## 11. Textos visibles (español)

Insignias: «TARJETA NUEVA», «EJERCICIO DIFÍCIL», «ERROR ANTERIOR». Opciones: los de la tabla del
apartado 8, «Probar», «Aleatorio», «Volumen», las dos notas de sonidos. Fallo: «ProFeedback tuvo un
problema. Anki sigue funcionando; el detalle quedó en su registro.» (5 s, una vez por función y
sesión). 54 idiomas; nueve completos (español, inglés, portugués de Brasil y de Portugal, catalán,
gallego, francés, italiano, alemán); en el resto, cinco textos en inglés. Los textos de los botones del
repaso son los de Anki.

## 12. Qué guarda

Opciones en la configuración de complementos del ordenador (todos los perfiles, no se sincroniza);
tamaño y posición de la ventana, en el perfil. Nada en la colección.

## 13. Fallos conocidos pendientes

- Deshacer una respuesta sin salir del repaso no se descuenta en la celebración del mazo.
- Activar las insignias a mitad de repaso las muestra sin su aspecto hasta volver a entrar.
- Elegir la insignia lee el historial de la tarjeta mientras Anki espera (pequeño; no medido).

## 14. Decisiones tomadas a propósito

«Difícil» no es acierto. Mínimos de confeti (5 y 20). La celebración de todos los mazos tiene
prioridad. Reproductor propio. Retardo de 0,1 s al pulsar con ratón. Duraciones largas de confeti y
brillo. Estilo dentro de la página del repaso (listo desde el primer momento). Cinco textos en inglés
en muchos idiomas.

## 15. Qué no hace

No se conecta a internet, no cambia la colección, no celebra si
se sale por otra pantalla, no pone insignias en vistas previas ni editor, no añade menús ni atajos.
