# Qué hace «Hider»

Versión 4.0.3 · 2026-10-21

Deja la pantalla de repaso limpia para concentrarse en la tarjeta: mientras repasa, pliega la barra
de menú, la barra superior y la barra inferior de la ventana, quita la barra de desplazamiento de la
tarjeta, esconde el puntero del ratón cuando lleva un rato quieto y puede dejar solo los botones
«Otra vez» y «Bien». Además, al abrir un mazo con tarjetas pendientes, puede saltar directamente a
la primera tarjeta. Todo vuelve a su sitio al salir del repaso. No cambia nada de su colección: lo
único que guarda son sus opciones.

## 1. Dónde aparece

- En la pantalla de repaso, que es donde actúa todo lo que oculta.
- Al abrir un mazo, si está activada la opción de empezar el repaso automáticamente (apartado 6).
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones (apartado 7), no el editor de texto que Anki muestra con otros complementos.
- No añade menús, botones ni atajos propios. No cambia nada en la lista de mazos, en la pantalla de
  un mazo (salvo el instante del salto automático), en Explorar, en el editor ni en las
  estadísticas. La única excepción es el puntero: mientras está en el repaso, se esconde en
  cualquier ventana de Anki (apartado 5).

## 2. Qué oculta durante el repaso

Cada pieza se puede activar o desactivar en las opciones; por defecto se ocultan todas.

- La barra de menú (Archivo, Editar, Herramientas…). Sus atajos de teclado siguen funcionando aunque
  no se vea: por ejemplo, Ctrl+Z para deshacer, Ctrl+P para las preferencias o Ctrl+Shift+A para los
  complementos.
- La barra superior (Mazos, Añadir, Explorar, Estadísticas y el botón de sincronizar).
- La barra inferior, la que tiene «Mostrar respuesta», los botones de respuesta, «Editar», «Más» y
  el recuento de tarjetas que quedan. Cómo se repasa sin ella, en el apartado 3.
- La barra de desplazamiento de la tarjeta (la vertical y la horizontal). Es solo de aspecto: la
  rueda del ratón y las teclas siguen desplazando la tarjeta.

Cómo se comporta:

- Las barras se pliegan antes de que Anki dibuje el repaso, así que no llegan a verse al entrar. La
  tarjeta aprovecha el sitio que dejan.
- Siguen plegadas aunque cambie el tema (de día a noche), las preferencias o la tarjeta.
- En pantalla completa, Anki enseña la barra de menú al llevar el ratón fuera de la tarjeta; Hider
  la vuelve a plegar en el acto, así que durante el repaso no aparece.
- Al salir del repaso, las barras vuelven todas a la vez cuando la pantalla siguiente (la lista de
  mazos o la de un mazo) ya está lista para dibujarse, para que no haya saltos. Si esa pantalla
  tardara, vuelven igualmente a las cuatro décimas de segundo. Si vuelve a entrar en el repaso antes
  de que hayan vuelto, no se mueven.
- La barra inferior no la devuelve Hider: la abre Anki, de una vez y con los botones de la pantalla
  nueva, al dibujarla.
- Si cambia una opción en mitad del repaso (la ventana de opciones se puede abrir con Ctrl+Shift+A),
  el cambio se nota en el acto: la barra que marque se pliega y la que desmarque vuelve.

## 3. Repasar con la barra inferior oculta

Con la barra inferior plegada (lo normal con los valores por defecto) no se ven ni «Mostrar
respuesta» ni los botones de respuesta: se repasa con el teclado, con los atajos de siempre de Anki.

- Espacio o Intro muestran la respuesta y, después, responden con el botón por defecto («Bien»), si
  Anki está configurado así.
- 1 responde «Otra vez» y 3 responde «Bien». 2 («Difícil») y 4 («Fácil») funcionan solo si no están
  ocultos esos botones (apartado 4).
- E edita la nota y M abre el menú «Más».
- D vuelve a la lista de mazos y S, a la pantalla del mazo.

## 4. Los botones «Difícil» y «Fácil»

- Con esta opción activada (lo está por defecto), entre los botones de respuesta solo quedan «Otra
  vez» y «Bien». Los nombres son los que da Anki en su idioma.
- Se quitan de la lista con la que Anki construye los botones, no se tapan: así nunca se oculta
  «Bien» por error. Si otro complemento añade botones, se queda el primero y el que Anki considera
  su botón por defecto.
- Sus atajos de teclado (2 y 4) también quedan bloqueados: al pulsarlos no se responde la tarjeta y
  sale durante 2 segundos el aviso «Ese botón está oculto. Solo puedes responder «Otra vez» o
  «Bien».».
- Si la barra inferior está oculta, los botones no se ven de todos modos, pero el bloqueo de 2 y 4
  sigue valiendo.

## 5. El puntero del ratón

- Mientras repasa, si el ratón lleva quieto el tiempo elegido (por defecto, 3 segundos), el puntero
  desaparece. Vuelve en cuanto mueve el ratón. Pulsar teclas, girar la rueda o hacer clic sin mover
  el ratón no lo devuelven.
- Vale para todas las ventanas de Anki mientras la ventana principal está en el repaso: si abre, por
  ejemplo, la ventana de editar (E) o Explorar (B) y escribe sin mover el ratón, el puntero también
  se esconde allí.
- Al salir del repaso el puntero vuelve siempre, aunque no mueva el ratón.
- Si Anki pone su puntero de espera durante una operación larga, Hider no se lo quita.

## 6. Empezar el repaso automáticamente

- Con esta opción activada (lo está por defecto), al abrir la pantalla de un mazo (por ejemplo, al
  pulsarlo en la lista de mazos) Hider salta directamente a la primera tarjeta, como si hubiera
  pulsado «Comenzar a estudiar», y pone en marcha el contador de la sesión de estudio igual que ese
  botón.
- Solo salta si hay alguna tarjeta que Anki enseñaría ya en ese mazo o en sus submazos. Si no la
  hay, se queda en la pantalla del mazo, como siempre.
- Por el camino no se ve la pantalla del mazo: durante un instante sale vacía, sin nombre, recuentos
  ni botón, y con las barras ya plegadas. Hider espera a que Anki deje de redibujarla (algo más de
  una décima de segundo sin cambios) y entonces salta.
- Si en ese instante deja de haber tarjetas o usted cambia de pantalla, no salta: la pantalla del
  mazo se dibuja entera y las barras vuelven.
- Si es usted quien sale del repaso a la pantalla del mazo (con la tecla S, eligiendo otro mazo con
  «/», o porque terminó las tarjetas y aparece la pantalla de felicitación), Hider no le vuelve a
  meter en el repaso. Vuelve a saltar cuando pase otra vez por la lista de mazos y abra un mazo.
- Con el planificador antiguo de Anki no salta nunca (Anki tampoco deja repasar con él).
- Si Anki redibujara tarde la pantalla del mazo encima del repaso ya empezado, Hider vuelve a abrir
  el repaso para que no quede tapado; la tarjeta de ese momento se vuelve a mostrar desde la
  pregunta.

## 7. Ventana de opciones

Título «Configurar 'Hider'», el mismo que Anki pone a la configuración de cualquier complemento. No
tiene botón de ayuda. Es una ventana que hay que cerrar para seguir usando Anki. No recuerda su
tamaño ni su posición.

Primer grupo, «Durante el repaso, ocultar:»:

| Opción | Globo al pasar el ratón | Por defecto |
|---|---|---|
| «La barra de menú (Archivo, Editar, Herramientas...)» | «Vuelve a aparecer en cuanto sales del repaso.» | Marcada |
| «La barra superior (Mazos, Añadir, Explorar, Estadísticas)» | «Vuelve a aparecer en cuanto sales del repaso.» | Marcada |
| «La barra inferior de la ventana» | «Vuelve a aparecer en cuanto sales del repaso.» | Marcada |
| «La barra de desplazamiento de la tarjeta» | «Solo visual: puedes seguir bajando con la rueda del ratón. El cambio se nota en la tarjeta siguiente.» | Marcada |
| «Los botones «Difícil» y «Fácil»» | «Deja solo «Otra vez» y «Bien». Sus atajos de teclado también quedan bloqueados, para que no respondas sin querer con un botón que no ves.» | Marcada |
| «El puntero del ratón cuando lleva quieto:» y, al lado, un número de segundos (de 1 a 60, escrito como «3 s»), que se apaga si la casilla está desmarcada | «Reaparece en cuanto mueves el ratón.» | Marcada, 3 s |

Segundo grupo, «Comportamiento»:

| Opción | Globo al pasar el ratón | Por defecto |
|---|---|---|
| «Empezar el repaso automáticamente al abrir un mazo» | «Solo si hay tarjetas pendientes. Si eres tú quien sale del repaso, Hider no te vuelve a meter dentro.» | Marcada |

Botones Aceptar, Cancelar y el estándar para restaurar los valores predeterminados, con los textos de
Qt en el idioma de Anki.

- Restaurar valores predeterminados marca todas las casillas y pone 3 segundos, y muestra el aviso
  breve de Anki «Se restauró la configuración predeterminada». No guarda nada hasta que pulse
  Aceptar.
- Aceptar guarda, aplica el cambio en el acto (también en mitad del repaso) y muestra durante 2
  segundos «Configuración de Hider guardada.».
- Cancelar cierra sin guardar nada.
- Si no se pudiera guardar, sale una ventana de aviso titulada «Hider» con el texto «No se ha podido
  guardar la configuración de Hider.» y la configuración anterior sigue en vigor.

El globo de la barra de desplazamiento dice que el cambio se nota en la tarjeta siguiente; en
realidad, si cambia la opción en mitad del repaso se nota en el acto, y si la cambia fuera del
repaso, la próxima vez que entre en él.

## 8. Idiomas

Sus textos están en 42 idiomas: español, inglés, francés, alemán, italiano, portugués de Brasil y
de Portugal, neerlandés, catalán, gallego, rumano, ruso, ucraniano, polaco, checo, eslovaco,
esloveno, croata, serbio, búlgaro, sueco, danés, noruego, finés, estonio, lituano, húngaro, griego,
turco, árabe, hebreo, persa, hindi, tailandés, japonés, coreano, chino simplificado y tradicional,
vietnamita, indonesio, malayo y filipino. Si el idioma de Anki no está entre ellos, salen en inglés.
Sigue el idioma de Anki en cada momento, sin reiniciar. Los nombres de los botones de respuesta, el
título de la ventana y el aviso de valores restaurados son los de Anki; los botones Aceptar,
Cancelar y Restaurar los traduce Qt. Sus frases tratan de tú.

## 9. Qué guarda y dónde

- Sus opciones, en la configuración de complementos de Anki de este ordenador: valen para todos los
  perfiles y no viajan con la sincronización.
- Si falta una opción o tiene un valor que no sirve (por ejemplo, escrito a mano o de una versión
  anterior), usa el valor por defecto. Los segundos del puntero tienen que ser un número entero del
  1 al 60; si no, usa 3.
- No escribe nada en su colección: solo consulta si hay tarjetas para repasar al abrir un mazo.
- Cuando algo falla, anota el detalle técnico en el registro del complemento, un archivo de texto
  en la carpeta de registros de Anki (Anki conserva los de los últimos 10 días).

## 10. Si algo falla

- Nunca abre la ventana de error de Anki. En su lugar muestra durante 4 segundos el aviso «Hider ha
  encontrado un problema y ha desactivado esa parte por seguridad. Revisa la configuración del
  complemento.», como mucho una vez por minuto por cada sitio que falle, para no llenar la pantalla.
- Ese aviso no es exacto: en realidad no desactiva nada. La parte que falló sigue funcionando y, si
  vuelve a fallar, el aviso puede repetirse pasado un minuto. Está anotado como fallo pendiente.
- Anki sigue funcionando. Si al salir del repaso fallara la vuelta de una barra, las otras vuelven
  igualmente.
- Al cerrar el perfil o cambiar de perfil en mitad del repaso, las barras y el puntero vuelven en el
  acto.

## 11. Qué no hace

- No se conecta a internet.
- No cambia tarjetas, notas, mazos ni repasos: las respuestas las guarda Anki como siempre, y se
  pueden deshacer igual que sin el complemento.
- No oculta nada fuera del repaso, salvo el instante del salto automático.
- No quita las barras de otras ventanas (Explorar, el editor, las estadísticas).
- No cambia colores ni el aspecto de las tarjetas, aparte de quitar la barra de desplazamiento.
- No añade menús, botones ni atajos de teclado.
