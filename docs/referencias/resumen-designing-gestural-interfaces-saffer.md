# [GESTURAL-INTERFACES] Resumen — Designing Gestural Interfaces: Touchscreens and Interactive Devices (Dan Saffer, 2008)

Convenciones: (cap. N) indica de dónde sale cada idea; las «Notas de Claude» son observaciones del resumidor, no del autor; [Específico de …] marca consejos que no se aplican tal cual en España; P, C, M, E y N son identificadores para referencias cruzadas. «Ap. A» es el apéndice A.

## [GESTURAL-INTERFACES] Ficha
- Título: Designing Gestural Interfaces: Touchscreens and Interactive Devices. No consta con seguridad edición española.
- Autor: Dan Saffer, director de diseño de experiencia en la consultora Adaptive Path; según el libro, diseña webs, aplicaciones y dispositivos desde 1995 y es autor de Designing for Interaction, que cita varias veces. Muchas figuras proceden de Adaptive Path y de fabricantes; la lista de proveedores del cap. 6 se declara no pagada.
- Año: 2008 (O'Reilly), escrito entre noviembre de 2007 y julio de 2008, justo después del primer iPhone.
- Idioma del original: inglés.
- Tipo: práctico (manual profesional de diseño, sin código).
- A quién sirve: diseñadores de interacción e industriales y desarrolladores que crean pantallas táctiles, kioscos o sistemas que responden al cuerpo; también a quien quiera entender por qué una interfaz táctil o un grifo automático resultan fáciles o frustrantes.
- Tesis: los gestos abren una nueva era del diseño de interacción; deben partir del cuerpo humano y de los sensores, emparejar cada gesto con una acción que ya tenga sentido y comunicarse bien, hasta que el producto «se disuelva en el comportamiento».
- Temas: diseño de interacción, ergonomía, tecnología, comunicación, toma de decisiones, creatividad.
- Ideas esenciales:
  1. Preguntar primero si debe ser gestual (P1).
  2. La complejidad del gesto debe igualar la de la tarea (P2).
  3. Cuanto más complicado el gesto, menos personas pueden hacerlo (P3).
  4. Toda acción necesita respuesta inmediata, idealmente en 100 ms (P4).
  5. El sensor determina qué gestos son posibles (C2, M11).
  6. Objetivos táctiles de al menos 1 cm y nada esencial bajo la mano (P7, M2).
  7. Reutilizar los patrones gestuales establecidos (M3 a M6).
  8. Documentar partes del cuerpo, duración, fases y respuesta (C10, M7).
  9. Prototipar en baja fidelidad y con un «hombre tras la cortina» (P10, M8).
  10. Comunicar presencia e instrucción con una affordance de atracción (P12, C11).
- Mapa:
  - Cap. 1, Introducing Interactive Gestures: definición, historia, sensores, cuándo usar gestos, cualidades y atributos.
  - Cap. 2, Designing for the Human Body: kinesiología, ergonomía, dedos, cobertura de pantalla, tamaño de objetivos, accesibilidad.
  - Cap. 3, Patterns for Touchscreens and Interactive Surfaces: doce patrones táctiles.
  - Cap. 4, Patterns for Free-Form Interactive Gestures: diez patrones sin contacto.
  - Cap. 5, Documenting Interactive Gestures: notaciones de danza y documentos de diseño.
  - Cap. 6, Prototyping Interactive Gestures: fidelidad, de gesto a código, sensores y pruebas.
  - Cap. 7, Communicating Interactive Gestures: zonas, affordance de atracción y métodos.
  - Cap. 8, The Future of Interactive Gestures: tendencias, estándares, patentes y ética.
  - Ap. A, A Palette of Human Gestures and Movements: catálogo de gestos con usos posibles.

## [GESTURAL-INTERFACES] Principios y recomendaciones

### P1 · Preguntarse primero si debe ser gestual — [GESTURAL-INTERFACES], cap. 1
Afirma: Saffer sostiene que la primera pregunta es si la interfaz debe ser gestual; todo diseño parte de las necesidades del usuario, limitadas por entorno, tecnología, recursos y negocio.
Por qué, según el autor: siguiendo a Bill Buxton, toda tecnología es la mejor para algo y la peor para otra cosa. En contra: mucha entrada de datos (el teclado es más rápido); dependencia visual sin respuesta táctil (mala para quien ve poco, como muchos adultos mayores); exigencia física (los gestos amplios excluyen a mayores o enfermos; los diminutos, a dedos grandes; los guantes impiden pulsar); contexto inapropiado (privacidad, vergüenza). A favor: interacción más natural, menos hardware visible (tiendas, museos, aeropuertos), flexibilidad de botones cambiantes, más matiz y más diversión.
Base: experiencia del autor y ejemplos; sin estudios.
Matices: después hay que elegir manipulación directa, indirecta o híbrida (C1); en 2008 la pantalla táctil directa era el estándar.

### P2 · La complejidad del gesto debe igualar la de la tarea — [GESTURAL-INTERFACES], cap. 1
Afirma: las tareas simples requieren gestos simples (tocar, deslizar, agitar la mano); solo las complejas admiten gestos complejos.
Por qué, según el autor: encender una luz basta con agitar la mano; atenuarla, con bajar la mano despacio; atenuar todas las luces de la casa, raro y complejo, puede pedir tres palmadas y bajar el brazo. Lo simple nunca debe exigir lo complejo.
Base: razonamiento con ejemplos.
Matices: propone que todo sea accesible con toques simples (un menú) y añadir gestos avanzados como atajos para expertos, igual que las combinaciones de teclas, explicándolos (M13).

### P3 · Cuanto más complicado el gesto, menos personas pueden hacerlo — [GESTURAL-INTERFACES], cap. 2
Afirma: todos los usuarios previstos deben poder ejecutar los comandos esenciales.
Por qué, según el autor: casi todos pueden tocar un botón, pocos agitar una mano a la pata coja; la motricidad fina decae con la edad. Un kiosco público necesita gestos más simples que una consola de jugadores expertos.
Base: ergonomía de Henry Dreyfuss (Designing for People, 1955), con sus figuras de medidas humanas Joe y Josephine.
Matices: ver accesibilidad en M2 y ética en P14.

### P4 · Respuesta inmediata (feedback) — [GESTURAL-INTERFACES], cap. 1
Afirma: toda acción debe recibir reconocimiento lo antes posible, idealmente en 100 ms o menos, que se perciben instantáneos; si va a tardar más de un segundo, hay que indicar que el sistema trabaja.
Por qué, según el autor: sin respuesta el usuario repite la acción, con riesgo de compras dobles o, con maquinaria, de lesiones; una barra de progreso no acorta la espera pero la hace parecer menor.
Base: razonamiento; no da fuente para la cifra.
Matices: depende de calibrar el sensor, y uno demasiado sensible molesta más que uno torpe (C2). En proyectores, latencia ideal menor de 20 ms (cap. 6).

### P5 · Preferir diseños sin estados ni modos — [GESTURAL-INTERFACES], cap. 1
Afirma: por ahora es mejor un diseño sin estados (stateless), con una tarea principal o un camino claro, que obligar a cambiar de modo.
Por qué, según el autor: en espacios públicos la atención es escasa y, sin pantalla, el usuario no sabe en qué modo está ni cómo volver. Un kiosco debe llevar de buscar a localizar y a comprar en un solo camino.
Base: razonamiento.
Matices: cambiará con usuarios más expertos; en el cap. 8 sugiere cambiar de modo con la voz y actuar con gestos.

### P6 · Emparejar el gesto con un comportamiento que ya existe — [GESTURAL-INTERFACES], caps. 1 y 7
Afirma: los mejores diseños asocian la acción al gesto que la gente ya haría: meter las manos bajo el grifo, cruzar un pasillo oscuro para iluminarlo, girar a la izquierda para que gire el avatar.
Por qué, según el autor: con Naoto Fukasawa, el buen diseño «se disuelve en el comportamiento»; con Adam Greenfield, cuanto más se acomoda y menos se impone, mejor (E1).
Base: casos y autoridades del diseño.
Matices: las metáforas deben respetar el significado que el gesto ya tiene: «remover una olla» confunde si no mezcla nada (cap. 7), y el dedo que reprueba no debe servir para desplazar (ap. A, M14).

### P7 · No tapar con la mano; no repetir gestos parecidos — [GESTURAL-INTERFACES], cap. 2
Afirma: nunca se debe poner información esencial (etiquetas, instrucciones, subcontroles) debajo de un elemento tocable, y conviene situar menús y controles abajo y no arriba. Tampoco deben usarse gestos parecidos para acciones distintas.
Por qué, según el autor: a diferencia del cursor, la mano y el brazo tapan lo que hay debajo (en un deslizador de color tapan etiquetas y muestra); y los dedos son imprecisos (E2).
Base: razonamiento y caso real.
Matices: las palmas apoyadas causan toques falsos; en kioscos se evita montando la pantalla en vertical. Los dedos fantasma son otra salida (M5).

### P8 · Activar al soltar — [GESTURAL-INTERFACES], cap. 3
Afirma: en pantallas táctiles, el toque debe actuar al levantar el dedo (activate-on-release).
Por qué, según el autor: permite apartarse si se cambia de opinión, sobre todo si la acción es irreversible.
Base: práctica de diseño.

### P9 · Cancelar directamente mejor que deshacer — [GESTURAL-INTERFACES], cap. 1
Afirma: un gesto ejecutado es difícil de deshacer; hay que ofrecer cancelaciones directas, como arrastrar de vuelta lo movido.
Por qué, según el autor: no hay un «deshacer» universal. Para que el usuario juegue y explore, los errores deben ser difíciles y reversibles; el juego se detiene si se siente atrapado o perdido.
Base: razonamiento.

### P10 · Elegir la fidelidad del prototipo según la respuesta buscada — [GESTURAL-INTERFACES], cap. 6
Afirma: cuanto más refinado el prototipo, más refinada la respuesta, lo que al principio es malo; hay que empezar en baja fidelidad, hacer varias variantes y planear tirarlas.
Por qué, según el autor: un prototipo pulido atrae comentarios sobre colores y tipos de letra, no sobre concepto, gestos y flujo; y el papel es mucho más barato que la electrónica.
Base: experiencia profesional.
Matices: en alta fidelidad la estética sí importa, pero el prototipo debe construirse para tirarse: reutilizar su código retrasa y empeora el producto (M9).

### P11 · Documentar lo justo — [GESTURAL-INTERFACES], cap. 5
Afirma: la documentación debe ser la necesaria para construir el producto con eficacia, y ni una página más.
Por qué, según el autor: con Dan Brown, da coherencia de visión, rendición de cuentas y trazabilidad, pero es un medio, no un fin que «fetichizar».
Base: autoridad citada.

### P12 · Comunicar presencia e instrucción — [GESTURAL-INTERFACES], cap. 7
Afirma: hay que avisar de que el sistema gestual existe (presencia) y enseñar a usarlo, incluido cómo encenderlo y apagarlo (instrucción).
Por qué, según el autor: muchas interfaces son casi invisibles y la gente teme romperlas o hacer el ridículo; Hubert Dreyfus lo atribuye a la conciencia de la vulnerabilidad del cuerpo (E4, E5).
Base: casos reales.
Matices: el medio depende de la distancia y del público (C11, M13).

### P13 · Hacen falta estándares — [GESTURAL-INTERFACES], cap. 8
Afirma: Saffer pide un repertorio común de gestos entre dispositivos, con un organismo como el W3C o, al menos, guías, impulsadas por IxDA o IDSA.
Por qué, según el autor: si no, cada empresa impondrá los suyos y habrá que adivinar si una luz se enciende agitando la mano, señalando o fingiendo pulsar un interruptor.
Base: argumento propio.
Matices: las patentes lo dificultan [Específico de EE. UU.] (ver N4).

### P14 · Respetar privacidad y dignidad — [GESTURAL-INTERFACES], caps. 1 y 8
Afirma: los gestos se ven, así que los sistemas gestuales son sociales: deben proteger la privacidad y no avergonzar.
Por qué, según el autor: los botones grandes dejan ver PIN, tarjetas o direcciones en kioscos y cajeros, lo que obliga a cuidar hardware, entorno y ubicación; los gestos difíciles o ridículos humillan a niños, mayores y personas con movilidad reducida. La interfaz debe ser «buena» para usuarios, terceros, cultura y medio ambiente.
Base: razonamiento ético; cita a Greenfield.
Matices: ver N7 sobre la detección de rasgos en el cap. 4.

## [GESTURAL-INTERFACES] Conceptos y mecanismos

### C1 · Gesto y tipos de interfaz gestual (interactive gesture) — [GESTURAL-INTERFACES], cap. 1 y ap. A
Qué es: para Saffer, cualquier movimiento físico que un sistema digital detecta y al que responde sin ratón ni lápiz: un saludo, un asentimiento, un toque, una ceja levantada.
Cómo funciona, según el autor: las interfaces táctiles (touchscreen) exigen tocar y limitan los gestos; las libres (free-form) no, a veces con mando o guante y cada vez más solo con el cuerpo. La manipulación directa (direct manipulation, Ben Shneiderman, 1983) es manejar objetos sin comandos; la táctil la lleva al extremo. La indirecta usa un gesto que no toca el objeto, como The Clapper, que enciende aparatos con una palmada. Gestos estáticos son posturas mantenidas («OK»); dinámicos, movimientos en el tiempo, mucho más difíciles de reconocer en código.
Base: Shneiderman; cita a David Liddle: el cuerpo tiene un repertorio de 15.000 años y solo usamos señalar con el ratón.

### C2 · Sensor, comparador y actuador — [GESTURAL-INTERFACES], cap. 1
Qué es: las tres partes de todo sistema gestual.
Cómo funciona, según el autor: el sensor detecta cambios; el comparador, casi siempre software, compara el estado actual con el anterior o el objetivo y decide; el actuador ejecuta, mecánicamente (motor de puerta) o en pantalla. Sensores habituales: presión, luz, proximidad, sonido, inclinación, movimiento (microondas o ultrasonidos) y orientación. El sensor determina por completo los gestos posibles («si mi portátil no detecta mi saludo, solo parezco idiota»); hay que calibrar su sensibilidad y, cuanto mayor su área, más amplio el gesto. El 3D necesita varios sensores; un acelerómetro mide el movimiento del aparato, no su posición en la sala, y por eso la Wii suma giroscopios y un sensor infrarrojo.
Base: teoría de sistemas y productos. Relación: M10, M11.

### C3 · Tecnologías táctiles (touch event) — [GESTURAL-INTERFACES], cap. 1
Qué es: un evento táctil es el momento en que el sistema registra un toque.
Cómo funciona, según el autor: resistivas, dos capas que se juntan al presionar; miden bien la presión pero apenas admiten varios dedos (multitáctil). Onda superficial: ultrasonidos que el dedo absorbe. Capacitivas: capa cargada que cede carga al dedo; algunas detectan la mano encima. Rejilla de haces infrarrojos para pantallas grandes. FTIR (reflexión interna total frustrada): luz infrarroja dentro de un metacrilato que el dedo dispersa hacia una cámara. DI (iluminación difusa) trasera, que ve el reflejo del dedo y objetos encima, o delantera, que ve su sombra.
Base: descripción técnica.

### C4 · Atributos de los gestos — [GESTURAL-INTERFACES], cap. 1
Qué es: lo que un sistema puede medir de un gesto.
Cómo funciona, según el autor: presencia, duración, posición (x, y, a veces z; relativa a la estatura o absoluta, por ejemplo gestos en alto para que no lleguen los niños), movimiento, presión (simulable con la duración o con el ensanchamiento de la yema), tamaño (dedo frente a lápiz), orientación, objetos incluidos, número de puntos de contacto, secuencia (exige memoria de estados y cuesta más al usuario) y número de participantes. Casi todas las pantallas usan solo presencia y duración.
Base: análisis del autor.

### C5 · Cualidades de una buena interfaz gestual — [GESTURAL-INTERFACES], cap. 1
Qué es: la concreción de Saffer del lema de Liz Sanders «útil, usable y deseable».
Cómo funciona, según el autor: descubrible (con affordances, propiedades que sugieren cómo usar un objeto, según James Gibson y Don Norman); digna de confianza; receptiva (P4); apropiada a cultura y contexto (el «OK» ofende en Grecia, Turquía, Oriente Medio y Rusia); significativa; inteligente (calcular y recordar por nosotros); ingeniosa (anticiparse); lúdica; placentera (perdonamos más los errores en lo bello, según Norman); y buena (P14).
Base: autoridades del diseño.

### C6 · Kinesiología básica (kinesiology) — [GESTURAL-INTERFACES], cap. 2
Qué es: estudio de la anatomía y la mecánica del movimiento, que Saffer considera tan necesario como saber de ordenadores.
Cómo funciona, según el autor: los músculos solo tiran, en pares: agonista que mueve (bíceps) y antagonista que devuelve (tríceps); el flexor cierra la articulación y el extensor la abre. Articulaciones móviles: esférica (hombro, cadera), condílea (muñeca), deslizante, en bisagra (codo, rodilla, dedos), en pivote (cuello) y en silla de montar (solo el pulgar). Movimientos en pares: flexión y extensión, rotación, abducción y aducción (alejar o acercar a la línea media), elevación y depresión, protracción y retracción; en mano y pie, supinación y pronación (palma arriba o abajo), flexión plantar y dorsiflexión, eversión e inversión, oposición (pinza del pulgar) y reposición; la circunducción las combina en círculo. Estos términos permiten documentar con precisión (M7).
Base: anatomía clásica.

### C7 · Ley de Fitts y densidad de píxeles (Fitts' Law, PPI) — [GESTURAL-INTERFACES], cap. 2
Qué es: la ley de Paul Fitts (1954) sobre el tiempo para alcanzar un objetivo, y la resolución de una pantalla.
Cómo funciona, según el autor: el tiempo sería proporcional a la distancia dividida por el tamaño (ver N1): lo grande y cercano se alcanza antes, así que los controles importantes deben estar cerca y ser grandes. El corolario del borde de pantalla, donde el cursor se detiene, no vale con dedos, que se levantan, ni en interfaces libres. PPI = píxeles de ancho / pulgadas de ancho; a más PPI, más píxeles para un mismo tamaño físico (M2).
Base: Fitts, Journal of Experimental Psychology, 1954.

### C8 · Puntas de iceberg y objetivos adaptativos (iceberg tips, adaptive targets) — [GESTURAL-INTERFACES], cap. 2
Qué es: dos formas de ampliar la zona táctil sin agrandar los iconos.
Cómo funciona, según el autor: en la punta de iceberg, la zona sensible excede el icono visible, lo que exige espacio entre objetos. El objetivo adaptativo agranda por algoritmo la zona de la tecla probable: tras «t» y «h», el teclado del iPhone favorece la «e». No hay que predecir de más y siempre debe poder corregirse (P9).
Base: ejemplo del iPhone, cuyas teclas medían 5 mm.

### C9 · Patrón y «plussing» (pattern) — [GESTURAL-INTERFACES], cap. 3
Qué es: un gesto más una respuesta del sistema que se repite en muchos productos.
Cómo funciona, según el autor: se usan para interiorizarlos, para consultarlos cuando uno se atasca y para mejorar una buena idea, lo que Walt Disney llamaba «plussing». Un patrón se establece al aparecer en varios productos durante un tiempo; los emergentes requieren explicación. Los patrones táctiles suelen adaptarse al aire. Reflejan el verano de 2008 (N3).
Relación: M3 a M6.

### C10 · Esfuerzo de Laban y preguntas de Bellotti — [GESTURAL-INTERFACES], cap. 5
Qué es: dos marcos para analizar gestos.
Cómo funciona, según el autor: Rudolf Laban describe el carácter de un movimiento (un puñetazo y una caricia son casi el mismo gesto) en cuatro continuos: espacio (directo o indirecto), peso (fuerte o ligero), tiempo (súbito o sostenido) y flujo (contenido o libre); el carácter del gesto debe casar con el de la función (un saludo lento no encaja con encender una luz de golpe). Victoria Bellotti (2002) plantea cinco preguntas: dirección (cómo se dirige el usuario al sistema), atención (cómo muestra que está listo), acción (qué se puede hacer), alineación (cómo responde) y accidente (cómo evita o corrige errores). De la danza extrae otras tres: qué partes del cuerpo intervienen, cuánto dura y qué fases tiene.
Base: teoría de la danza e investigación citada. Relación: M7.

### C11 · Tres zonas de interacción y affordance de atracción (attraction affordance) — [GESTURAL-INTERFACES], cap. 7
Qué es: un marco de Darren David y Nathan Moody (Stimulant) y un término de Saffer.
Cómo funciona, según el autor: de lejos (atracción), la persona repara en el producto por carteles, sonido, el aparato o al ver a otro usarlo; a media distancia (observación), aprende mirando y la señalización es crucial; de cerca, a un metro o menos (interacción), usa el producto y lee lo que lleva encima. La affordance de atracción es un elemento, normalmente en la pantalla en reposo, invitador y facilísimo, que solo sirve para empezar, heredero de las demostraciones de las máquinas recreativas de los ochenta: la mano animada del metro de Nueva York, el «deslizar para desbloquear» del iPhone o el agua de Microsoft Surface que invita a tocarla.
Matices: no convertir el lugar en un salón recreativo.

### C12 · Tecnologías convergentes — [GESTURAL-INTERFACES], cap. 8
Qué es: lo que Saffer prevé que se fundirá con los gestos.
Cómo funciona, según el autor: voz (señalar una silla y decir «háblame de ella»); realidad virtual; computación ubicua (ubicomp, cálculo integrado en objetos cotidianos, que podría llevar las preferencias de cada uno a cualquier habitación); NFC (comunicación de campo cercano, a menos de 10 cm, donde acercar dos aparatos es el gesto natural); interfaces hápticas (respuesta que se siente al tacto, como botones que aparecen cuando hacen falta); interfaces tangibles (datos encarnados en objetos, como el contestador de canicas de Durrell Bishop, 1992); y cobots (robots colaborativos que aumentan la fuerza y precisión humanas). Prevé además que los gestos complementen, no sustituyan, al teclado; que el ratón sea lo más vulnerable; y que su mejor uso esté en hogares, espacios públicos y aplicaciones especializadas, con la cocina como próximo laboratorio.
Base: prototipos de 2008 y opinión del autor.

## [GESTURAL-INTERFACES] Métodos y protocolos

### M1 · Elegir el gesto apropiado — [GESTURAL-INTERFACES], cap. 1
Objetivo: asignar a cada tarea su gesto.
Pasos: 1) confirmar que conviene una interfaz gestual (P1); 2) decidir directa, indirecta o híbrida; 3) cruzar sensores disponibles, pasos de la tarea y fisiología; 4) igualar la complejidad del gesto a la tarea (P2); 5) preferir gestos que la gente ya hace (P6); 6) preguntar a varios usuarios qué gesto usarían para cada función, o hacer el gesto y preguntar qué esperan, y buscar patrones.

### M2 · Dimensionar objetivos táctiles — [GESTURAL-INTERFACES], cap. 2
Objetivo: que todo lo que se toca sea pulsable.
Pasos: 1) partir de la yema media más pequeña: mínimo 1 cm de diámetro o 1 × 1 cm; 2) calcular PPI = píxeles de ancho / pulgadas de ancho; 3) convertir: píxeles = tamaño en pulgadas × píxeles de ancho / pulgadas de ancho (1 cm son unas 0,4 pulgadas); 4) prototipar con medidas reales y probar con usuarios; 5) para accesibilidad, en torno al 150 % (1,5 cm de lado) y gestos simples (tocar, agitar la mano, proximidad).
Ejemplo: en un Nokia N800 (225 PPI) 1 cm son 90 píxeles; en una pantalla de 15 pulgadas, unos 38 cm, a 85 PPI, 34 píxeles. Ver N2.

### M3 · Patrones táctiles de toque y movimiento — [GESTURAL-INTERFACES], cap. 3
Objetivo: activar, seleccionar, mover y escalar.
Pasos y reglas:
- Tocar para activar (Tap to Open/Activate): menos de un segundo, como un clic; activar al soltar (P8); mantenido, repite la acción.
- Tocar para seleccionar (Tap to Select): o un toque selecciona y un doble toque abre, o un toque abre.
- Arrastrar para mover (Drag to Move Object): el objeto sigue al dedo; puede restringirse la dirección, como el desbloqueo del iPhone.
- Tocar para parar (Tap to Stop): detiene o pausa acciones de más de varios segundos; si pausa, otro toque distinto reanuda.
- Pellizcar y separar (Pinch to Shrink, Spread to Enlarge): exige multitáctil; la posición inicial vale 100 %; escala continua, normalmente proporcional, con la relación decidida según objeto y pantalla; límites mínimo y máximo prefijados.

### M4 · Patrones táctiles de desplazamiento — [GESTURAL-INTERFACES], cap. 3
Objetivo: recorrer contenido que no cabe.
Pasos y reglas:
- Deslizar (Slide to Scroll): comprobar antes que el dedo no está sobre un objeto (sería un arrastre); no mezclarlo con dos dedos.
- Girar (Spin to Scroll): un dedo en círculo, horario adelante y antihorario atrás; para listas o más de tres pantallas, como la rueda del iPod; un círculo recorre una pantalla; si acelera, ayuda que la lista tenga orden conocido; parar en un elemento es difícil sin respuesta visual o sonora.
- Deslizar y mantener (Slide and Hold): sigue hasta levantar el dedo; puede requerir una señal («Más...»).
- Lanzar (Fling to Scroll, desplazamiento cinético o de inercia) y empujar con un toque (Flick to Nudge): la velocidad del dedo se vuelve inercia frenada por una fricción simulada; la punta indica toque ligero y la yema, empujón.
- Dos dedos (Two Fingers to Scroll): desplaza mientras un dedo mueve el cursor; propio de trackpads.
Reglas comunes: barras de posición y una respuesta al llegar al final (rebote, vibración o sonido).

### M5 · Dedos fantasma (Ghost Fingers) — [GESTURAL-INTERFACES], cap. 3
Objetivo: ver los dedos ocultos, por ejemplo detrás del aparato.
Pasos: 1) añadir un sensor que los localice (touchpad trasero o cámaras); 2) dibujarlos como sombras, contornos transparentes o fotorrealistas. Permite controles en la parte trasera, diez dedos a la vez y no tapar la pantalla (P7). Patrón emergente que hay que explicar.

### M6 · Patrones libres — [GESTURAL-INTERFACES], cap. 4
Objetivo: activar sin tocar una superficie.
Pasos y reglas:
- La proximidad activa (Proximity Activates/Deactivates): basta la presencia; luces y climatización; cámara, barrera infrarroja, presión o micrófono; el que más se dispara por error, así que hay que calibrarlo (ver N7).
- Mover el cuerpo (Move Body to Activate): exige movimiento, cuando este tiene sentido (correr, bailar) o para evitar falsos disparos.
- Señalar (Point to Select/Activate): el gesto más natural de selección; requiere detectar la orientación de la mano (cámara, mando, guante).
- Agitar la mano (Wave to Activate): rara vez accidental, adecuado en público; suele detectarse con un haz infrarrojo.
- Meter las manos (Place Hands Inside to Activate): grifos, secadores, jabón; infrarrojos.
- Girar el aparato (Rotate to Change State): cambia función o vista; giroscopio o acelerómetro con umbral definido (90°, 180°); en plano sobre una mesa puede no detectarse.
- Pisar (Step to Activate): manos ocupadas o controles bajos; sensor de presión protegido.
- Agitar el aparato (Shake to Change): acciones muy simples, divertido; acelerómetro con umbral.
- Inclinar (Tilt to Move): mucho matiz con el cuerpo quieto, difícil para niños pequeños y mayores.

### M7 · Documentar gestos — [GESTURAL-INTERFACES], cap. 5
Objetivo: que el equipo construya lo diseñado.
Pasos: 1) escribir escenarios, «bocetos con palabras», empezando por el primer uso: cuestan minutos frente a semanas de prototipo; 2) redactar casos de uso (título, actores, propósito, condición inicial, condición final, pasos, alternativas); en gestos lo esencial son las condiciones inicial y final, que indican cuándo empieza y acaba el gesto; 3) hacer el flujo de tareas, con decisiones de usuario y sistema («si gesto X, entonces Y»), que fija sensores y número de gestos; 4) dibujar wireframes a tamaño real, con controles, todos los estados de cada objeto y el gesto que los cambia, restricciones (por ejemplo, «el sensor de calor solo detecta a menos de 5 m») y ajustes de sensores; 5) explicar lo simple con anotaciones y lo intermedio con fotogramas clave (keyframes) en tres fases: iniciación, activación y actualización; 6) recoger el vocabulario común en un documento de módulos gestuales, que en sistemas simples puede bastar; 7) para gestos complejos o con contexto, hacer storyboards (bastan monigotes o fotos) y reunirlos en carriles (swim lanes), con franjas para la historia, la pantalla, el flujo del sistema y el negocio; 8) para el ritmo, animaciones con pausas y anotaciones, o vídeos rápidos con cámara de mano; ninguno basta solo; 9) enlazar animaciones y vídeos desde la documentación en papel.
Las notaciones de danza (Labanotación, Benesh, Eshkol Wachman) son demasiado lentas, pero inspiran.

### M8 · Prototipos de baja fidelidad y Mago de Oz — [GESTURAL-INTERFACES], cap. 6
Objetivo: probar concepto, flujo y gestos barato.
Pasos: 1) prototipos de papel, dibujados a escala y cambiados a mano; 2) modelos toscos de madera, cartón o arcilla para comprobar tamaño, peso, situación de controles y sensores (un aparato pesado no se agita; un botón puede estorbar al deslizar); 3) en entornos, modelos más control manual de los objetos (mandos, sedal) o un mundo virtual, barato pero con gestos de avatar pobres; 4) un «hombre tras la cortina» (técnica del Mago de Oz), visible o escondido, que dispara las respuestas cuando el usuario hace el gesto.

### M9 · Prototipos de alta fidelidad — [GESTURAL-INTERFACES], cap. 6
Objetivo: refinar detalles con algo que funcione solo.
Pasos: 1) si existe la plataforma, usar el dispositivo real (prototipo exacto), con su kit de desarrollo (SDK); 2) si no, preferir hardware comercial adaptado (off-the-shelf), comprobando antes qué lenguaje admite; para táctiles, una pantalla de tamaño parecido, una lámina táctil sobre un monitor o una grande con la zona sobrante tapada; 3) como último recurso, uno artesanal (DIY, «si necesitas soldador, es DIY») con protoboard, sensores y servomotores. La táctil suele prototiparse con dispositivo real o comercial; lo libre, casi siempre artesanal.
Matices: el artesanal pertenece a la computación física, que suma electrónica, mecánica, programación y diseño de interacción, visual, sonoro e industrial, además de la instalación.

### M10 · De gesto a código — [GESTURAL-INTERFACES], cap. 6
Objetivo: que el programa reconozca el gesto.
Pasos: 1) definir variables (altura, profundidad, velocidad, duración); 2) leer los datos del sensor; 3) calcular diferencias entre puntos; 4) compararlas con patrones; 5) ejecutar la acción si coinciden.
Reglas: el gran reto es saber cuándo empieza y acaba el gesto; las rectas son triviales y los círculos exigen comparar docenas de puntos; hay que tolerar mucha variación, descartar variables irrelevantes y hacer el patrón tan burdo como se pueda sin disparos accidentales.

### M11 · Elegir el sensor — [GESTURAL-INTERFACES], cap. 6
Objetivo: capturar el gesto con la tecnología adecuada.
Pasos según el caso: toques en superficies pequeñas, capacitiva; multitáctil grande, FTIR para solo dedos, DI delantera si se controla la luz exterior y DI trasera para objetos o mano encima; proximidad, barrera infrarroja, cámara que compara con una imagen de referencia, micrófono (poco fiable con ruido), sensor infrarrojo pasivo (PIR) de calor corporal, a unos 20 pies (unos 6 m), o presión; movimiento cercano, ultrasonidos o microondas; movimiento del aparato, acelerómetro y giroscopio; cara, cámara a la altura media de la cabeza; manos y brazos, cámaras, guantes o mando; posición exacta, una señal emitida o varias cámaras.

### M12 · Probar con usuarios — [GESTURAL-INTERFACES], cap. 6
Objetivo: detectar fallos antes de construir.
Pasos: 1) usuarios representativos, no oficinistas técnicos y sanos; 2) en sistemas libres, el entorno real; 3) plan de pruebas y guion que comprueben si los gestos son descubribles («¿qué haría para X?»), significativos («¿lo haría?»), útiles y usables; 4) normalmente menos de 10 participantes; 5) tiempo entre sesiones para recalibrar.

### M13 · Comunicar gestos — [GESTURAL-INTERFACES], cap. 7
Objetivo: enseñar presencia e instrucción (P12).
Pasos: 1) elegir el medio según público y lugar; 2) evitar enseñar varios gestos a la vez o superponerlos con pegatinas o un modo de ayuda; 3) texto para gestos simples e inequívocos, breve y, según Erika Hall, auténtico, atractivo, específico, apropiado y cortés; 4) ilustraciones, más universales, junto al lugar del gesto; 5) demostraciones animadas en bucle para imitar, como en la Wii; 6) no fiarse solo de símbolos de computación ubicua, aún desconocidos; 7) metáforas coherentes con el gesto (P6).

### M14 · Catálogo de gestos humanos — [GESTURAL-INTERFACES], ap. A
Objetivo: partir de gestos que la gente ya conoce.
Pasos: 1) elegir según la actividad: mover cursor o avatar (deslizar, ladear o girar la cabeza, inclinar el torso, señalar); seleccionar (tocar, mirar fijo, señalar, pistola con la mano); encender o apagar (tocar, pisotón, agitar la mano, palmada, chasquido); confirmar (asentir, sonreír, «OK», pulgar arriba); cancelar (negar, fruncir el ceño, pulgar abajo, mano de stop); 2) comprobar el significado cultural (N5); 3) descartar la lengua de signos (compleja, distinta en cada lengua e interferiría con quien la usa) y los gestos entre personas (abrazos, besos, apretones).
Ejemplos: brazos arriba suben un ajuste; encoger los hombros deshace; agacharse baja volumen o luz; entrecerrar los ojos agranda el texto; el dedo en los labios silencia; frotarse las manos sube la temperatura y abanicarse la baja; girar un pomo imaginario ajusta un dial.

## [GESTURAL-INTERFACES] Ejemplos y casos
- E1 · En Hong Kong la gente pasa el bolso con la tarjeta Octopus por el lector, un gesto que nadie diseñó (P6, cap. 1).
- E2 · Las máquinas de voto Diebold de California (2005) se colgaban cada pocos cientos de votos al interpretar un leve arrastre como arrastrar y soltar (P7, cap. 2).
- E3 · Philips Glowing Places: bancos que se iluminan con viveza si muchos se sientan poco rato y suavemente si pocos se quedan mucho (M6, cap. 4).
- E4 · Muchos usuarios del metro de Nueva York no tenían cuenta bancaria ni habían usado un cajero; Antenna Design añadió dos mensajes y una mano animada (P12, C11, cap. 7).
- E5 · Un diseñador en París agitando los brazos en un aseo a oscuras porque la luz se apagaba tras 20 segundos sin movimiento (P12, cap. 7).

## [GESTURAL-INTERFACES] Errores frecuentes y advertencias
- Sensores mal calibrados, demasiado sensibles o demasiado torpes (C2, cap. 1).
- Copiar convenciones de escritorio: el cursor sobra, el hover y los menús desplegables apenas funcionan, el doble clic exige un umbral (por ejemplo 200 ms) y es más seguro el toque único, la multiselección necesita un modo o dibujar un área (cap. 1; ver N3, N6).
- Olvidar a los zurdos (7 a 10 % de los adultos): permitir invertir controles (cap. 2).
- Ignorar uñas postizas y guantes, que pueden no activar las capacitivas, sobre todo en climas fríos (cap. 2).
- Acabados negros, que resaltan las huellas; mejor fondos claros o con dibujo (cap. 2).
- [Específico de EE. UU.] Saffer aconseja que los diseñadores no lean patentes, porque conocer una e infringirla agrava los daños en un pleito (cap. 8).

## [GESTURAL-INTERFACES] Ejercicios y acciones
- Observar en un parque o restaurante cómo gesticula la gente para descubrir un léxico común (cap. 2).
- Pasar cuanto antes un boceto de móvil a un bloque de madera, porque «la experiencia móvil es distinta en la mano» (Matt Jones), y simular el sistema con un Mago de Oz antes de construir sensores (M8, cap. 6).

## [GESTURAL-INTERFACES] Cifras y reglas concretas
- Doble clic: umbral de ejemplo de 200 ms (cap. 1); doble toque con pausa de menos de 75 ms (ap. A) (ver N6).
- Toque: menos de 100 ms; toque rápido o lanzamiento: roce de menos de 75 ms; empujón: menos de 2 s (ap. A).
- Objetivo táctil mínimo: 1 × 1 cm; 1,5 cm para accesibilidad (cap. 2; ver N2).
- Dedos adultos: 16 a 20 mm; punta, 8 a 10 mm; yema, 10 a 14 mm (cap. 2).
- PPI = píxeles / pulgadas de ancho; N800: 225 PPI, 1 cm = 90 px; pantalla de 15 pulgadas (unos 38 cm): 85 PPI, 1 cm = 34 px (cap. 2).
- Zona de interacción: un metro o menos (cap. 7).
- NFC: menos de 4 pulgadas (unos 10 cm) (cap. 8).
- Gestos ofensivos según el libro: «OK» en Grecia, Turquía, Rusia y Oriente Medio; pulgar arriba en Australia y Nigeria; palma de stop en Grecia; asentir y negar invertidos en partes de Oriente Medio (cap. 1 y ap. A; ver N5).

## [GESTURAL-INTERFACES] Preguntas que este libro responde
- ¿Cuándo no conviene una pantalla táctil? → Según Saffer en [GESTURAL-INTERFACES], con mucha entrada de datos, usuarios con poca vista o movilidad, o contextos poco privados (P1; cap. 1).
- ¿Qué gesto asigno a cada función? → Según Saffer en [GESTURAL-INTERFACES], uno tan complejo como la tarea, compatible con los sensores y el cuerpo, y si es posible uno que la gente ya haga (P2, P6, M1, M14; cap. 1 y ap. A).
- ¿Qué tamaño debe tener un botón táctil? → Según Saffer en [GESTURAL-INTERFACES], al menos 1 × 1 cm convertido a píxeles según la densidad (M2, C7; cap. 2; ver N2).
- ¿Cuánto puede tardar la respuesta? → Según Saffer en [GESTURAL-INTERFACES], idealmente 100 ms; si pasa de 1 s, mostrar que trabaja (P4; cap. 1).
- ¿Cómo diseño el desplazamiento y el zoom con los dedos? → Según Saffer en [GESTURAL-INTERFACES], con patrones como deslizar, lanzar con inercia o pellizcar, con barras, límites y respuesta al final (M3, M4; cap. 3).
- ¿Qué sensor uso para detectar que alguien se acerca? → Según Saffer en [GESTURAL-INTERFACES], barrera infrarroja, cámara, sensor de calor, presión o micrófono, bien calibrados (M6, M11; caps. 4 y 6).
- ¿Cómo documento un gesto? → Según Saffer en [GESTURAL-INTERFACES], indicando cuerpo, duración, fases y respuesta, con anotaciones, fotogramas clave o storyboards según su complejidad (C10, M7; cap. 5).
- ¿Cómo pruebo una interfaz de gestos sin construirla? → Según Saffer en [GESTURAL-INTERFACES], con papel o modelos toscos y alguien que simula al sistema (M8; cap. 6).
- ¿Cómo sabe la gente que algo responde a gestos? → Según Saffer en [GESTURAL-INTERFACES], comunicando presencia e instrucción con una affordance de atracción, texto, ilustración o demostración (P12, C11, M13; cap. 7).
- ¿Son universales los gestos? → Según Saffer en [GESTURAL-INTERFACES], no: varios ofenden en algunos países y todos traen un significado propio (C5, M14; ap. A; ver N5).
- ¿Se puede patentar un gesto? → Según Saffer en [GESTURAL-INTERFACES], un gesto natural probablemente no, uno ligado a una acción en un aparato quizá sí, según el derecho estadounidense de 2008 (P13; cap. 8; ver N4).
- ¿Sustituirán los gestos al teclado y al ratón? → Según Saffer en [GESTURAL-INTERFACES], no pronto: el teclado seguirá para escribir y lo vulnerable es el ratón (C12; cap. 8).

## [GESTURAL-INTERFACES] Glosario
- Gesto interactivo (interactive gesture): movimiento que un sistema detecta y al que responde sin ratón ni lápiz.
- Interfaz táctil (touchscreen) e interfaz libre (free-form): con contacto o sin él.
- Manipulación directa (direct manipulation): manejar objetos en pantalla sin comandos.
- Affordance: propiedad que sugiere cómo usar un objeto.
- Affordance de atracción (attraction affordance): elemento sencillo que invita a empezar.
- Latencia (latency): retraso entre acción y efecto.
- Kinesiología (kinesiology): estudio del movimiento humano.
- Abducción y aducción: alejar o acercar a la línea media del cuerpo.
- Ley de Fitts (Fitts' Law): lo grande y cercano se alcanza antes.
- Punta de iceberg (iceberg tip): zona táctil mayor que el icono.
- Objetivo adaptativo (adaptive target): zona táctil que crece según la tecla probable.
- Cobertura de pantalla (screen coverage): lo que tapa la mano.
- Desplazamiento cinético (kinetic scrolling): el que continúa por inercia.
- Dedos fantasma (Ghost Fingers): dibujo en pantalla de dedos ocultos.
- FTIR y DI: detección multitáctil con luz infrarroja y cámara.
- Fotograma clave (keyframe): dibujo de un momento clave del gesto.
- Carriles (swim lanes): hoja con vistas paralelas de un escenario.
- Mago de Oz (Wizard of Oz): una persona simula las respuestas del sistema.
- Computación física (physical computing): sistemas con sensores, motores y microprocesadores.
- Computación ubicua (ubicomp): cálculo integrado en objetos cotidianos.

## [GESTURAL-INTERFACES] Específico de otro país
- [Específico de EE. UU.] Requisitos de patentabilidad y consejo de no leer patentes (P13, errores; cap. 8; ver N4).
- [Específico de EE. UU.] Datos de mercado y casos de voto electrónico y del metro de Nueva York; las lecciones de diseño son generales (caps. 1, 2 y 7).

## [GESTURAL-INTERFACES] Notas de Claude

### N1 · Fórmula de la ley de Fitts — sobre C7, cap. 2
Qué dice el libro: el tiempo es proporcional a la distancia dividida por el tamaño.
Qué se sabe hoy: la forma habitual es logarítmica: tiempo = a + b × log2(distancia / tamaño + 1). La conclusión práctica se mantiene, pero el tiempo no crece en proporción directa a la distancia.
Fuente: conocimiento general de Claude, sin comprobar.

### N2 · Tamaños de objetivo actuales — sobre M2, cap. 2
Qué dice el libro: mínimo 1 × 1 cm; 1,5 cm para accesibilidad; aún no hay guías.
Qué se sabe hoy: Apple pide unos 44 × 44 puntos, Material Design de Google 48 × 48 dp (unos 9 mm) y la norma de accesibilidad web WCAG 2.2 un mínimo de 24 × 24 píxeles CSS (criterio 2.5.8, nivel AA) y 44 × 44 en el nivel AAA. El centímetro de Saffer sigue siendo prudente.
Fuente: búsqueda web del 14-10-2026 ([guía WCAG 2.5.8](https://allaccessible.org/blog/wcag-258-target-size-minimum-implementation-guide), [tamaños táctiles](https://ezud.com/touch-target-sizes-mobile-accessibility/)); solo devolvió títulos, así que las cifras son conocimiento general de Claude.

### N3 · Libro de 2008 en un campo que cambió deprisa — sobre la Ficha y caps. 1, 3 y 6
Qué dice el libro: no existe cortar y pegar táctil, apenas hay menús contextuales, conviene evitar modos, el iPhone «está por ver» y recomienda Flash, J2ME o Second Life.
Qué se sabe hoy: los móviles adoptaron cortar y pegar, la pulsación larga como menú y gestos de varios dedos; las capacitivas desplazaron a las resistivas; Flash desapareció. Los principios siguen vigentes; el estado de la técnica y las herramientas, no.
Fuente: conocimiento general de Claude, sin comprobar.

### N4 · La patente del pellizco — sobre P13, cap. 8
Qué dice el libro: no sabe si Apple logrará patentar el pellizco en móviles.
Qué se sabe hoy: Apple litigó con Samsung, pero en diciembre de 2012 la oficina de patentes de EE. UU. invalidó, en un reexamen inicialmente provisional, la llamada patente del pellizco ('915); el gesto es hoy universal. Todo el apartado se refiere al derecho estadounidense.
Fuente: búsqueda web del 14-10-2026 ([AppleInsider, 19-12-2012](https://appleinsider.com/articles/12/12/19/apple-pinch-to-zoom-patent-invalidated-by-uspto)); no se comprobó el resultado final.

### N5 · Significado cultural de algunos gestos — sobre C5 y M14, ap. A
Qué dice el libro: asentir y negar están invertidos en partes de Oriente Medio.
Qué se sabe hoy: la inversión clásica se documenta sobre todo en Bulgaria; en Grecia, Turquía y parte del mundo árabe el «no» suele hacerse alzando la cabeza, que no equivale a invertir el sí. Las demás afirmaciones son generalizaciones que conviene contrastar con el público concreto.
Fuente: conocimiento general de Claude, sin comprobar.

### N6 · Contradicciones internas — sobre las cifras, cap. 1 y ap. A
Qué dice el libro: 200 ms de umbral de doble clic en el cap. 1 y menos de 75 ms de pausa de doble toque en el ap. A; además, «ven aquí» y «fuera» tienen idéntica descripción en el ap. A.
Qué se sabe hoy: las cifras son ejemplos, no medidas, y los sistemas actuales permiten ajustar el umbral. La descripción duplicada parece un error de edición.
Fuente: comparación interna del libro; lo de los umbrales actuales es conocimiento general de Claude, sin comprobar.

### N7 · Detectar raza, edad o sexo — sobre M6 y P14, cap. 4
Qué dice el libro: propone, sin valorarlo, anuncios que cambian según la raza, la edad o el sexo detectados por cámara.
Qué se sabe hoy: en España, tratar datos biométricos para identificar o inferir el origen racial es una categoría especial en principio prohibida salvo excepciones (art. 9 del Reglamento (UE) 2016/679, RGPD), y el Reglamento (UE) 2024/1689 de Inteligencia Artificial (art. 5.1.g) prohíbe la categorización biométrica que deduzca la raza, entre otros rasgos. No es aplicable tal cual.
Fuente: conocimiento general de Claude, sin comprobar.

### N8 · Alan Kay «inventor del portátil» — sobre el cierre, cap. 8
Qué dice el libro: atribuye a Kay la invención del portátil.
Qué se sabe hoy: Kay concibió el Dynabook (1972), concepto que inspiró portátiles y tabletas, pero no inventó el portátil como producto.
Fuente: conocimiento general de Claude, sin comprobar.
