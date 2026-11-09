# Ficha de diseño: CoreProgress

Versión 1.0.0 (21 de octubre de 2026). Léase junto con `00-contexto-comun.md`. Es un complemento que
la persona trajo hecho fuera del taller: algunos colores y textos no siguen la paleta Nocturne ni el
trato de usted (se indica en cada caso).

## 1. Qué es, en una frase

Una barra de progreso fija arriba de la pantalla de repaso que se llena a medida que se despachan las
tarjetas pendientes de hoy en el mazo, con marcas numeradas por el camino; además cuenta los aciertos
seguidos, los celebra con un aviso breve, vuelve dorada la barra desde 5 seguidos y guarda el récord
personal.

## 2. Para quién y para qué

Para ver cuánto falta en una sesión de repaso y motivarse con pequeños logros (hitos, rachas, récord).
Solo lee la cuenta de tarjetas que muestra Anki; guarda sus opciones y el récord.

## 3. Dónde se ve

- En la pantalla de repaso, también en mazos filtrados y estudio personalizado.
- Herramientas > Complementos > CoreProgress > Configuración: su ventana de opciones.
- No aparece en la lista de mazos, la pantalla de un mazo, Explorar (ni su vista previa), plantillas,
  editor ni estadísticas. No añade menús ni atajos.
- En todo el repaso baja la estrella de nota marcada y la bandera de Anki para que queden justo debajo
  de la barra.

## 4. La barra

Qué mide:

- Al entrar a repasar toma como 100 % la suma de las tres cifras de Anki en ese momento (nuevas, en
  aprendizaje, para repasar). Avanza según cuántas de esas tarjetas han salido de la cola de hoy.
- Una tarjeta cuenta solo cuando sale de verdad de la cola (se gradúa o un repaso pasa a otro día). Una
  fallada vuelve a aprendizaje y no hace avanzar la barra mientras Anki la siga contando.
- Enterrar, suspender o apartar una tarjeta de hoy también hace avanzar la barra.
- Se pone al día una décima de segundo después de cada respuesta o cambio.
- Cada vez que entra a repasar empieza vacía, con lo que quede como nuevo 100 %.
- Si la cuenta de Anki sube (vencen tarjetas en aprendizaje, se deshace una respuesta), retrocede; nunca
  baja de vacía.
- Al terminar, Anki sale del repaso y la barra se va con él: casi nunca se ve llena.

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
  38 %, y un destello blanco que lo cruza de izquierda a derecha cada 9 s sin parar.
- Día o noche se decide por lo oscuro que sea el fondo real de la tarjeta, no solo por el modo de Anki.
  Se repinta al cambiar de modo o de tamaño de ventana.
- Con «Espacio superior» en 0 (de serie), la barra se dibuja encima de la parte alta de la tarjeta, sin
  apartarla (fallo pendiente, apartado 13).

Colores del relleno (no son de la paleta Nocturne; los trae el complemento):

| Tema | Degradado de día | Degradado de noche | Color del aviso (día / noche) | Muestra en Opciones |
|---|---|---|---|---|
| Verde clásico (de serie) | #64D97A, #3DD65A, #25CB44, #1DAF38 | #2DB947, #33D151, #4BD865, #68DC7E | #167628 / #88E098 | #3DD65A |
| Azul océano | #5F87DD, #376BDD, #1E56D2, #1649B6 | #2757BF, #2C62D8, #4575DE, #638AE1 | #12337A / #84A2E4 | #376BDD |
| Turquesa laguna | #5DE0D0, #34DFCC, #1BD5BF, #14B8A5 | #24C1AF, #29DBC6, #42E0CE, #60E3D4 | #107C70 / #82E5DA | #34DFCC |
| Rojo fuego | #DE5E62, #DE363B, #D31D23, #B6161B | #C0262B, #D92B30, #DF4449, #E26266 | #7B1115 / #E48386 | #DE363B |
| Rosa suave | #DD608F, #DB3876, #D11F62, #B41853 | #BE2860, #D72D6D, #DD467F, #E06493 | #791339 / #E385A8 | #DB3876 |
| Púrpura real | #7E60DC, #7450B8, #4B20D0, #3E18B4 | #4D28BD, #572ED6, #6B46DC, #8264E0 | #2C1379 / #9C85E3 | #7450B8 |
| Naranja atardecer | #E0935D, #DF7B34, #D5681B, #B85814 | #C16524, #DB7329, #E18442, #E39660 | #7C3D10 / #E5AB82 | #DF7B34 |
| Dorado (5 o más seguidas) | #E3BD59, #E4B230, #DAA416, #BC8D10 | #C59820, #DFAC25, #E4B73E, #E7C15D | #BC8D10 / #E7C15D | — |

Dorado: además, un halo suave (0 0 6px dorado al 18 % y 0 0 2px al 14 %), rebajado dos veces a
petición del usuario («debe adornar, no llamar la atención»). El aviso dorado lleva un resplandor de 8
px de su color al 45 %.

Nota: los temas comparten nombre con los de GritMap, pero sus tonos son otros, y CoreProgress conserva
Rojo fuego, que GritMap retiró.

## 5. Hitos (marcas numeradas)

- Con «Mostrar hitos en la barra» y un total de 10 tarjetas o más: cuatro marcas en el 20, 40, 60 y
  80 %, cada una con su número de tarjetas (con 50: 10, 20, 30 y 40). Con menos de 10, ninguna.
- Números redondeados; si dos coinciden, sale uno.
- Cada marca está donde llega el relleno al despachar ese número.
- Forma: círculo (pastilla si el número es largo), con letra en negrita de 9 a 13 px (el 62 % de la
  altura de la barra), un poco más alto que la barra.
- Sin alcanzar: color del canal, número en gris (de día, tinta oscura al 62 %; de noche, gris claro al
  78 %). Al alcanzarla: toma el color del relleno, número en blanco con sombra, da un pequeño salto
  (crece durante 0,4 s) y suelta tres chispas blancas.
- Los hitos se animan aunque la casilla de efectos esté desmarcada.

## 6. Racha y récord

- Racha: respuestas seguidas con «Bien» o «Fácil» en este repaso. «Otra vez» y «Difícil» la ponen a
  cero. Empieza de cero en cada repaso. No se ve como cifra fija.
- Avisos (con efectos marcados): al llegar a 2, 5, 10, 15, 25, 35, 45… (cada 10 desde 25), debajo de la
  barra y centrado bajo el relleno (se mueve con él), en mayúsculas: «2 SEGUIDAS». Letra de 13 px,
  negrita, interletraje 0,04 em, con sombra 0 1px 3px negro al 25 %. Desde 5, el relleno se aviva un
  instante y suelta cuatro chispas en su borde.
- El aviso aparece al responder, se ve durante la pregunta siguiente y se apaga con fundido al mostrar
  la respuesta, nunca antes de 2 s a la vista.
- Barra dorada: con 5 o más seguidas, relleno y aviso dorados; al romperse, vuelve al tema.
- Récord: racha más larga, propia de cada perfil. Se celebra una vez por repaso, al batirlo (como
  mínimo a las 3): «¡RÉCORD! 11», con avivado y chispas si es de 5 o más. Gana al aviso de racha si
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
- Destello cada 9 s, continuo.
- Saltos de hitos (0,4 s), chispas, avivado, fundido de avisos.
- Con «reducir animaciones» del sistema: el destello queda quieto y tenue (opacidad 0,12), sin chispas
  ni fundidos de color; el salto de los hitos sí se mantiene.
- Esto supera la norma del taller (150 ms, sin animación continua): es una excepción heredada del
  complemento original.

## 9. Ventana de opciones

Ventana nativa de Anki (toma los colores de Atelier), título «CoreProgress» (sin traducir, a petición
del usuario). Modal. No recuerda tamaño ni posición. Ancho mínimo de unos 400 px.

- Arriba, el récord con la cifra en negrita: «Tu récord actual: -» o «Tu récord actual: 7 seguidas!»
  (sin signo de apertura, a petición del usuario). A la derecha, «Restablecer», que pregunta en una
  ventana «Anki»: «¿Poner tu récord a cero?», con «Sí» marcado de antemano.

| Opción | Control | Valores | De serie |
|---|---|---|---|
| Tema de color | Lista desplegable, cada tema con un cuadrito de muestra (siempre en su tono de día) | Verde clásico, Azul océano, Turquesa laguna, Rojo fuego, Rosa suave, Púrpura real, Naranja atardecer | Verde clásico |
| Altura de la barra (px) | Campo numérico | 12 a 22; también escala hitos y números | 16 |
| Espacio superior (px) | Campo numérico, flechas de 4 en 4 | 0 a 300 px libres encima de la tarjeta | 0 |
| Excluir mazos (récord) | Botón «Seleccionar mazos» | — | Ninguno |
| Efectos de racha y récord (aura/oro/texto) | Casilla | Avisos, dorado, avivado, chispas de avisos | Marcada |
| Mostrar hitos en la barra | Casilla | — | Marcada |

- Botones estándar Guardar, Cancelar y Restaurar valores predeterminados (textos de Qt). Restaurar
  repone tema, altura, espacio y casillas sin guardar; no toca récord ni mazos excluidos.
- Guardar: si está repasando, la barra se redibuja al momento.
- «Seleccionar mazos» abre «Excluir mazos (récord)»: lista de todos los mazos con nombre completo
  (submazos con «::»), incluidos filtrados y el predeterminado, cada uno con casilla; Aceptar y Cancelar.
  Sin buscador ni textos de ayuda (retirados a petición del usuario). Lista de al menos 180 px de alto.

## 10. Accesibilidad

- La barra no recibe foco ni clics (los atraviesan): no interfiere con el teclado del repaso.
- Movimiento reducido respetado en parte (apartado 8).
- Lo que no tiene: la barra, los hitos y los avisos no se anuncian al lector de pantalla; los avisos se
  apoyan en el color (dorado) y en el texto en mayúsculas; la ventana de opciones es nativa y accesible
  como cualquier ventana de Anki; los colores del relleno no se han medido contra la norma de
  contraste. Son puntos de mejora posibles.

## 11. Textos visibles (español)

«2 SEGUIDAS», «¡RÉCORD! 11», «Tu récord actual: -», «Tu récord actual: 7 seguidas!», «Restablecer»,
«¿Poner tu récord a cero?», «Seleccionar mazos», «Excluir mazos (récord)», las etiquetas de la tabla
del apartado 9, y el aviso de fallo de Anki «El problema podría ser causado por un add-on.». Trata de
tú (no de usted, como el resto del taller). 60 idiomas; si falta, inglés; el idioma se fija al
arrancar Anki.

## 12. Qué guarda

- Opciones: configuración de complementos del ordenador (todos los perfiles, no se sincroniza).
- Récord: en la colección de cada perfil (se sincroniza); no entra en Editar > Deshacer.
- Un valor que falte o no sirva usa el de serie; los números fuera de margen se llevan al límite.

## 13. Fallos conocidos pendientes (decisión de la persona)

- Deshacer algo que no es una respuesta (enterrar, suspender) quita una respuesta a la racha y puede
  bajar el récord.
- «1 seguidas!» en singular (plural fijo).
- Con «Espacio superior» en 0, la barra y el aviso tapan la parte alta de la tarjeta.
- «Restablecer» trae «Sí» marcado de antemano y borra el récord sin vuelta atrás, aunque después se
  pulse Cancelar.

## 14. Decisiones tomadas a propósito

- «Difícil» rompe la racha. El récord se celebra desde 3 (antes 5). La barra empieza vacía en cada
  repaso. El récord se celebra una vez por repaso y gana al aviso de racha. Se guarda al batirlo y baja
  si se deshace. Rehacer no lo devuelve. Los mazos excluidos solo afectan al récord. El canal toma el
  color del fondo real de la tarjeta. Halo dorado y tonos suavizados a petición del usuario.

## 15. Qué no hace

No se conecta a internet, no cambia el estudio, no muestra la racha como cifra fija ni el récord durante
el repaso, no aparece fuera del repaso. La casilla de efectos no apaga el destello ni los hitos.
