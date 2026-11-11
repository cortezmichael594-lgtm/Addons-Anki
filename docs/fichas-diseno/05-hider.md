# Ficha de diseño: Hider

Versión 4.1.0 (9 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Deja la pantalla de repaso limpia para concentrarse en la tarjeta: pliega la barra de menú, la barra
superior y la barra inferior, quita la barra de desplazamiento, esconde el puntero cuando está quieto,
puede dejar solo «Otra vez» y «Bien», y puede entrar directamente al repaso al abrir un mazo.

## 2. Para quién y para qué

Para un repaso a pantalla limpia, con el teclado, sin elementos que distraigan ni decisiones de más
(dos botones en lugar de cuatro). Todo vuelve al salir del repaso. No cambia la colección.

## 3. Aspecto propio

No pinta nada propio: no tiene colores, iconos ni letra propios. Su efecto es quitar cosas. Su única
interfaz es una ventana de opciones con el modelo del panel de GritMap (colores de la paleta) y avisos breves de Anki
(recuadro amarillo con letra negra, propio de Anki).

## 4. Dónde actúa

- Pantalla de repaso: todo lo que oculta.
- Al abrir un mazo, si está activado el salto automático.
- Herramientas > Complementos > Hider > Configuración: ventana de opciones.
- No añade menús, botones ni atajos. Excepción: mientras se está en el repaso, el puntero se esconde en
  cualquier ventana de Anki.

## 5. Qué oculta durante el repaso (cada pieza, activable; de serie, todas)

- Barra de menú (Archivo, Editar, Herramientas…). Sus atajos siguen funcionando (Ctrl+Z, Ctrl+P,
  Ctrl+Mayús+A…).
- Barra superior (Mazos, Añadir, Explorar, Estadísticas, Sincronizar).
- Barra inferior («Mostrar respuesta», botones de respuesta, «Editar», «Más», recuento).
- Barra de desplazamiento de la tarjeta (vertical y horizontal); la rueda y las teclas siguen
  desplazando.

Comportamiento visual:

- Las barras se pliegan antes de que Anki dibuje el repaso: no llegan a verse al entrar. La tarjeta
  aprovecha el sitio.
- Siguen plegadas aunque cambie el tema, las preferencias o la tarjeta.
- En pantalla completa, Anki enseñaría la barra de menú al llevar el ratón arriba; Hider la vuelve a
  plegar en el acto.
- Al salir, las barras vuelven todas a la vez cuando la pantalla siguiente está lista (como mucho a las
  0,4 s), sin saltos. La barra inferior la redibuja Anki.
- Un cambio de opción a mitad de repaso se nota en el acto.

## 6. Repasar con la barra inferior oculta (con el teclado)

Espacio o Intro: mostrar respuesta y luego «Bien» (si Anki está configurado así). 1: «Otra vez». 3:
«Bien». 2 y 4: solo si «Difícil» y «Fácil» no están ocultos. E: editar. M: menú «Más». D: lista de
mazos. S: pantalla del mazo.

## 7. «Difícil» y «Fácil» ocultos

- Solo quedan «Otra vez» y «Bien», con los nombres de Anki. Se quitan de la lista de botones, no se
  tapan (nunca se oculta «Bien» por error).
- Las teclas 2 y 4 quedan bloqueadas: no responden y sale 2 s el aviso «Ese botón está oculto. Solo
  puedes responder «Otra vez» o «Bien».».

## 8. Puntero del ratón

- Quieto el tiempo elegido (3 s de serie): desaparece. Vuelve al mover el ratón (no con teclas, rueda o
  clic sin mover).
- Vale en todas las ventanas de Anki mientras la principal está en el repaso.
- Al salir del repaso, vuelve siempre. No quita el puntero de espera de Anki.

## 9. Empezar el repaso automáticamente

- Al abrir la pantalla de un mazo con tarjetas que Anki enseñaría ya, salta a la primera tarjeta como
  «Comenzar a estudiar» (también pone en marcha el contador de sesión).
- Sin tarjetas, se queda en la pantalla del mazo.
- Por el camino, la pantalla del mazo sale vacía un instante (sin nombre, recuentos ni botón, con las
  barras ya plegadas); Hider espera algo más de una décima de segundo sin cambios y salta.
- Si es la persona quien sale del repaso a la pantalla del mazo, no la vuelve a meter.
- Con el planificador antiguo de Anki, nunca salta.

## 10. Ventana de opciones

Sigue el modelo de `09-patron-configuracion.md` (panel de GritMap, 560 px, recuadros, Aceptar y Cancelar abajo, nada se guarda hasta Aceptar). El detalle completo de cada opción, con sus textos, está en el documento «qué hace» del complemento; aquí, lo que importa para el diseño.

- Título «Configurar 'Hider'» (el de Anki para cualquier complemento).
- Recuadro «Durante el repaso, ocultar», con la nota gris «Vuelve a aparecer en cuanto sales del
  repaso.» bajo el título y «Restaurar los valores predeterminados» (y «Deshacer») a la derecha: seis
  casillas. Las explicaciones, que antes eran globos al pasar el ratón, son ahora notas grises a la
  vista bajo su casilla. Los segundos del puntero (1 a 60, con «−» y «+» y «s» al lado) cuelgan de su
  casilla y se atenúan si está desmarcada.
- Recuadro «Comportamiento», con su «Restaurar»: la casilla del salto automático y su nota.
- Al aceptar, aviso breve de Anki «Configuración de Hider guardada.»; si no se puede guardar, el aviso
  sale en rojo encima de la primera casilla y la ventana sigue abierta.

## 11. Accesibilidad

- Pensado para el teclado: con la barra inferior oculta, todo el repaso se hace con los atajos de Anki.
- El bloqueo de 2 y 4 evita respuestas sin querer con un botón invisible, y lo explica con un aviso.
- Las notas grises bajo cada casilla explican cada opción, a la vista.
- Riesgos para quien no conoce los atajos: sin barra inferior no hay forma visible de responder; el
  puntero oculto puede desorientar. Ningún aviso al entrar explica cómo repasar sin barra.
- Los avisos breves de Anki desaparecen solos (2–4 s) y no se anuncian necesariamente al lector de
  pantalla.

## 12. Textos e idiomas

42 idiomas; si falta, inglés. Sigue el idioma de Anki en cada momento. Trata de tú. Nombres de botones
de respuesta, título de la ventana y aviso de restaurar, de Anki; Aceptar, Cancelar y Restaurar, de Qt.

## 13. Qué guarda

Opciones en la configuración de complementos del ordenador (todos los perfiles, no se sincroniza).
Valores no válidos vuelven al de serie (segundos: entero de 1 a 60, si no, 3). Nada en la colección.

## 14. Si algo falla

Nunca la ventana de error de Anki. Aviso 4 s: «Hider ha encontrado un problema y ha desactivado esa parte
por seguridad. Revisa la configuración del complemento.», como mucho una vez por minuto y sitio. Al
cerrar o cambiar de perfil a mitad de repaso, barras y puntero vuelven.

## 15. Fallos conocidos pendientes

- El aviso de fallo no es exacto: no desactiva nada. Propuesta: «Hider ha tenido un problema. Anki sigue
  funcionando; el detalle queda en el registro del complemento.».
- El salto automático consulta la colección dos veces sin dejar libre a Anki; en colecciones muy grandes
  podría notarse un parón breve (no medido).

## 16. Decisiones tomadas a propósito

2 y 4 bloqueados con aviso. En pantalla completa no aparece la barra de menú. No vuelve a meter en el
repaso a quien sale. La pantalla del mazo vacía un instante en el salto. Las barras vuelven cuando la
pantalla siguiente está lista. Si Anki redibuja tarde el mazo encima del repaso, se reabre el repaso
desde la pregunta. Barra de desplazamiento oculta solo de aspecto. Avisos de fallo como mucho uno por
minuto. Opciones comunes a todos los perfiles.

## 17. Qué no hace

No se conecta a internet, no cambia tarjetas ni repasos, no oculta nada fuera del repaso (salvo el
instante del salto), no quita barras de otras ventanas, no cambia colores, no añade menús ni atajos.
