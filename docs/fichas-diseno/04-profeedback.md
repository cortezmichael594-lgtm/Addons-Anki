# Ficha de diseño: ProFeedback

Versión 2.5.0 (16 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

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

| Insignia | Cuándo | Icono (siempre) | Texto de noche | Texto de día |
|---|---|---|---|---|
| «TARJETA NUEVA» | La tarjeta es nueva | Destello, #CE82FF | #CE82FF | #8F3BD9 |
| «SE RESISTE» | Sus tres últimas respuestas fueron «Otra vez» | Pesa, #FF4B4B | #FF4B4B | #C92C2C |
| «OTRA OPORTUNIDAD» | Alguna de sus dos últimas respuestas fue «Otra vez» | Flechas en bucle, #FFAB33 | #FFAB33 | #9E5A00 |

- Icono de 24 px, 8 px de hueco, letra de 14 px en negrita con 0,4 px entre letras, mayúsculas.
- Franja fija de 40 px encima de la tarjeta (24 del icono y 16 de aire), haya insignia o no: la tarjeta
  no cambia de sitio entre una y otra.
- Fundido de 120 ms (solo opacidad). No se puede pulsar ni seleccionar. La misma en pregunta y
  respuesta. Solo cuentan respuestas dadas con un botón.
- Contraste del texto: 5,1 a 9,6 a 1 en los dos modos. Los tonos de día son el mismo color con menos
  luz; el icono conserva el original.

## 6. Botones del repaso

Con «Botones de colores con relieve» (marcada de serie). Colores de las caras fijos, iguales de día y
de noche (decisión de la persona: se quedan como en el original):

| Botón | Cara | Canto (4 px) | Letra | Ancho mínimo |
|---|---|---|---|---|
| «Otra vez» | #FF4B4B | #E62222 | #131F24 | 130 px |
| «Difícil» | #FFAB33 | #E6951F | #131F24 | 130 px |
| «Bien» | #93D333 | #79B933 | #131F24 | 190 px |
| «Fácil» | #49C0F8 | #1899D6 | #131F24 | 130 px |
| «Mostrar respuesta» | #FFD700 | #E7A601 | #5C3700 | 190 px |
| «Editar» y «Más» | Sin relleno; contorno de 2 px y canto de 4 px NOCTURNE_CONTROL_BORDER | — | FG_SUBTLE | 130 px |

- Todos: 50 px de alto (cara de 46 y canto de 4), esquinas de 16 px, 24 px de relleno lateral. Letra
  propia («Feather») o la del sistema, 15 px, negrita, espaciado 0,8 px, sin mayúsculas. «Editar» y
  «Más», separados 40 px a los lados.
- «Bien» mide lo mismo que «Mostrar respuesta»: tras pulsar este, el puntero queda dentro de «Bien», y
  no en el hueco de 16 px entre «Difícil» y «Bien».
- Raya de 2 px encima de la barra: BORDER.
- Tiempos previstos y recuento de tarjetas: FG.
- Ratón encima: los de color, brillo 1,08 (se aclaran, nunca se oscurecen); «Editar» y «Más», relleno
  BUTTON_HOVER.
- Pulsado: la cara baja 4 px y tapa el canto en 80 ms, sin cambiar de color; vuelve en 70 ms, sin
  rebote. La respuesta sale al soltar dentro del botón (soltar fuera no responde). Un segundo clic antes
  de 0,4 s se ignora. Teclado: al instante. Con «reducir movimiento», sin animación.
- Foco de teclado: aro de 2 px BORDER_FOCUS separado 2 px (contrasta con la barra, 6,0 a 1 de noche).
- Mandan sobre Atelier (FIX-006). Con la casilla desmarcada, los botones son los de Anki o Atelier.
- Por debajo de 640 px, sin ancho mínimo (salvo «Bien» y «Mostrar respuesta») y 12 px de relleno; si
  una palabra no cabe, se reduce la letra. La barra completa necesita unos 1.064 px.

## 7. Celebración al terminar

Solo al volver del repaso a la pantalla del mazo habiendo respondido algo en esa sesión. Si sale por
otro camino (lista de mazos, «Terminar» en el aviso de tiempo), no se celebra. Una respuesta deshecha
deja de contar.

| Celebración | Cuándo | Mínimo para el confeti | Confeti |
|---|---|---|---|
| Mazo | No queda nada en ese mazo, pero sí en otros | 5 respuestas en la sesión | Dos cañones desde las esquinas de abajo, 2,5 s como máximo, colores de la paleta |
| Día (prioritaria, una vez al día) | No queda nada en ningún mazo | 20 tarjetas distintas hoy | Lluvia dorada desde arriba, 4 s como máximo, y un brillo del título de 3,6 s |

- Ninguna depende de las notas: no hay «perfecta» (opción B del informe 2.4.0).
- Si el día ya se celebró y vuelven tarjetas, se celebra como un mazo.
- Sonido de fin siempre que hay celebración, salvo «Sin sonido». Sin el mínimo, solo sonido.
- Confeti normal: ACCENT_DANGER, FLAG_2, ACCENT_NOTE, ACCENT_CARD, STATE_MARKED y FLAG_5. Dorado: mezclas
  de STATE_BURIED, FLAG_2 y blanco.
- Título dorado: degradado #FFD700 → #FFF1A8 de noche (12,9 a 1 o más) y #8A5200 → #A35F00 de día (4,7
  a 1 o más), una pasada.
- El confeti no tapa ni bloquea nada y se desvanece en sus últimos 0,4 s. Con «reducir movimiento», sin
  confeti y con el título dorado quieto.

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
☑ Confeti al terminar
                                              [Aceptar] [Cancelar]
```

- Filas con la etiqueta a la izquierda (200 px, letra normal), 8 px entre filas y 16 entre los dos
  grupos de sonidos. «Probar» de 76 × 32 px.
- Cada lista: «Sin sonido», los de serie («1 · Madera»…), los propios, «Aleatorio», una raya y «Abrir la
  carpeta de estos sonidos…». No hay casillas de sonido ni nota al pie.
- «Probar»: apagado (FG_DISABLED) con «Sin sonido»; si no consigue sonar, aviso en ACCENT_DANGER con
  icono encima de la fila. Nombre propio para el lector de pantalla en cada uno.
- Enlaces en FG_LINK, subrayados.
- 16 controles de ajuste: deslizador, cuatro listas con su «Probar» y tres casillas.

## 9. Sonidos y letra propios

- Solo .mp3, en «user_files/sonidos/» del complemento: «correcto», «fallo», «finalizado/mazo» y
  «perfecto-mazo» (fin de mazo), «finalizado/todo» y «perfecto-todo» (fin del día). Se crean vacías al
  abrir las opciones; «Abrir la carpeta…» abre la de cada lista. Uno con el mismo nombre que uno de
  serie lo sustituye.
- Letra: «ProFeedback.ttf» o «Feather Bold.ttf» (1,5 MB como mucho) en «user_files». Ahora no hay
  ninguno: letra del sistema.

## 10. Accesibilidad

- Contraste: todo texto a 4,5 a 1 o más y todo contorno a 3 a 1 o más, de día y de noche (letra de
  «Mostrar respuesta» 7,5; «Editar» y «Más» 9,7 de noche; insignias de día 5,1 a 5,2).
- Foco de teclado visible en la barra (aro separado) y en las opciones.
- Atajos de teclado de Anki (1–4, Espacio) intactos y al instante.
- Iconos de insignia ocultos al lector de pantalla (el texto basta).
- Color nunca solo: cada botón y cada insignia llevan su texto. Con deuteranopia, «Difícil» y «Bien»
  se ven casi iguales; los distinguen la palabra y el sitio.
- Movimiento: nada se mueve durante el repaso más de 150 ms salvo el botón pulsado; al terminar, nada
  dura más de 4 s.
- Pendiente de comprobar: si el lector de pantalla lee la insignia al aparecer la tarjeta.

## 11. Textos visibles (español)

Insignias: «TARJETA NUEVA», «SE RESISTE», «OTRA OPORTUNIDAD» (54 idiomas). Opciones: los del apartado
8, «Sin sonido», «Aleatorio», «Abrir la carpeta de estos sonidos…», «No se pudo reproducir. Compruebe
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

- Activar las insignias a mitad de repaso las muestra sin su aspecto hasta volver a entrar.
- Elegir la insignia lee el historial de la tarjeta mientras Anki espera (pequeño; no medido).

## 14. Decisiones tomadas a propósito

- Informe 2.4.0 (aplicado entero, 2026-11-16): «Difícil» es acierto; el oro premia terminar el día
  (opción B); «Bien» de 190 px; «SE RESISTE» y «OTRA OPORTUNIDAD»; confeti de 4 s y un brillo;
  sonidos fijos en las respuestas y variados al final; respuesta al soltar, sin espera.
- Se quedan: los colores de caras e insignias, el relieve, los mínimos de confeti (5 y 20), la
  prioridad de la celebración del día, el reproductor propio, el estilo dentro de la página del
  repaso, el filtro del doble clic y el .mp3 con sus seis carpetas.
- No se añaden (informe 2.4.0, 7.4): rachas, puntos o niveles; sonido en «Mostrar respuesta»; mensajes
  de ánimo tras cada respuesta; más colores.
- Restaurar por recuadro (modelo de opciones), no uno solo abajo.

## 15. Qué no hace

No se conecta a internet, no cambia la colección, no premia la nota que uno se pone, no celebra si se
sale por otra pantalla, no pone insignias en vistas previas ni editor, no añade menús ni atajos.
