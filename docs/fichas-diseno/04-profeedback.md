# Ficha de diseño: ProFeedback

Versión 2.4.0 (13 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

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

Desde la 2.4.0, como en el ProFeedback original (petición del cliente, con el original delante): un icono
redondo y un texto en mayúsculas, centrados encima del contenido de la tarjeta, sin píldora. Una sola,
por prioridad. Colores fijos del original, iguales de día y de noche (no siguen la paleta ni Atelier):

| Insignia | Cuándo | Color |
|---|---|---|
| «TARJETA NUEVA» | La tarjeta es nueva (también si se reinició) | Morado #CE82FF |
| «EJERCICIO DIFÍCIL» | Sus tres últimas respuestas fueron «Otra vez» | Rojo #FF4B4B |
| «ERROR ANTERIOR» | Alguna de sus dos últimas respuestas fue «Otra vez» (también hoy) | Naranja #FFAB33 |

- Texto e icono del mismo color. Letra propia si la hay («Feather», apartado 9) o la del sistema, 1 rem,
  negrita, interlineado 1 rem, espaciado 0,04 em, mayúsculas. Icono de 32 px, 0,35 em de separación.
- Ocupa todo el ancho, encima de la tarjeta (la empuja un poco abajo), con 0,5 em de aire debajo.
  Aparece con un fundido de 160 ms (solo opacidad). No se puede pulsar ni seleccionar.
- La misma insignia en pregunta y respuesta. Solo cuentan respuestas dadas con un botón.
- Contraste: de día, el morado y el naranja quedan por debajo de 3 a 1 sobre el fondo claro (como en
  el original; decisión del cliente).

## 6. Botones del repaso

Con «Botones de respuesta 3D de colores» (marcada de serie). Desde la 2.4.0, como en el ProFeedback
original (petición del cliente), con colores fijos iguales de día y de noche:

| Botón | Relleno | Canto (debajo) | Letra |
|---|---|---|---|
| «Otra vez» | #FF4B4B | 2 px #E62222 | #131F24 |
| «Difícil» | #FFAB33 | 2 px #E6951F | #131F24 |
| «Bien» | #93D333 | 2 px #79B933 | #131F24 |
| «Fácil» | #49C0F8 | 2 px #1899D6 | #131F24 |
| «Mostrar respuesta» | #FFD700 | 4 px #E7A601 | #AE6802 |
| «Editar» y «Más» | Sin relleno; contorno de 2 px y canto de 4 px #C9D1D9 (noche #37464F) | — | #57606A (noche #52656D) |

- Medidas: 48 px de alto, 130 px de ancho mínimo (crecen con el texto), 24 px de relleno lateral,
  esquinas de 18 px. Letra propia («Feather») o la del sistema, 15 px, negrita, espaciado 0,8 px, sin
  mayúsculas. «Editar» y «Más», separados 40 px a los lados.
- Raya gris continua de 2 px encima de la barra: #D7DDE2 de día, #37464F de noche.
- Tiempos previstos y recuento de tarjetas en el color de texto de Anki (FG; el original, negro y
  blanco puros).
- Con el ratón encima: brillo 1,08 (se aclaran); nunca se oscurecen.
- Al pulsar: se hunden (1 a 2 px) sobre su canto, que baja a 1 px, en 90 ms; al soltar vuelven con
  un pequeño rebote (220 ms). Con el ratón, la respuesta llega a Anki 0,1 s después; con el teclado,
  al instante. Un segundo clic en el mismo botón antes de 0,4 s se ignora. Con «reducir movimiento»,
  solo el cambio de brillo.
- Mandan sobre Atelier (FIX-006): sin el borde, las esquinas, la raya ni el oscurecido que Atelier
  pone a los botones de estudio. Con la casilla desmarcada, los botones son los de Anki o Atelier.
- Retoques casi imperceptibles sobre el original: aro de foco azul con el teclado; por debajo de
  640 px, sin ancho mínimo y con 12 px de relleno; si una palabra no cabe, se reduce la letra.

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
- Contraste de los botones (2.4.0, colores del original): letra casi negra sobre los cuatro de
  respuesta, que se lee bien; la letra ámbar de «Mostrar respuesta» sobre el dorado queda por debajo
  de 4,5 a 1, como en el original (decisión del cliente).
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
