# [PRACTICAL-UI] Resumen — Practical UI (Adham Dannaway, 2024)

Convenciones: (cap. N) es el capítulo de origen; las «Notas de Claude» son del resumidor, no del autor; [Específico de …] no se aplica tal cual en España.

## [PRACTICAL-UI] Ficha
- Título: Practical UI. Quick and practical UI design guidelines to design intuitive, accessible, and beautiful interfaces. No se conoce con seguridad una edición española.
- Autor: Adham Dannaway, diseñador de producto en Sídney (Australia) desde 2005, especializado en interfaces y sistemas de diseño para empresas emergentes, agencias, grandes empresas y administración, en productos con millones de usuarios. Vende el propio libro (practical-ui.com); no recomienda productos suyos.
- Año: 2024, 2.ª edición.
- Idioma del original: inglés.
- Tipo: práctico.
- A quién sirve: a quien diseña, programa o revisa interfaces web y móviles y quiere criterios objetivos, sobre todo si empieza.
- Tesis: casi todas las decisiones de diseño de interfaces se pueden tomar con un sistema de pautas lógicas, no con talento artístico; el objetivo es reducir el riesgo de que alguien no pueda usar la interfaz, con pantallas simples, familiares y accesibles.
- Temas: diseño y experiencia de usuario, accesibilidad, sesgos cognitivos, comunicación, toma de decisiones, productividad.
- Ideas esenciales:
  - P1 Minimizar el riesgo de usabilidad con interfaces simples y familiares.
  - P2 Cada detalle necesita una razón lógica, no solo estética.
  - P3 Reducir el coste de interacción y la carga cognitiva.
  - M1 Crear un sistema de diseño: estilos predefinidos, componentes y pautas de uso.
  - P4 Buena accesibilidad es gran usabilidad; mínimo WCAG 2.1 nivel AA.
  - P10 Un solo color de marca, reservado para lo interactivo.
  - P12 Espaciar según la relación entre elementos, en múltiplos de 8 puntos.
  - P14 Una sola tipografía de palo seco, solo en regular y negrita.
  - P17 Un único botón primario, alineado a la izquierda, y sin botones desactivados.
  - P18 Formularios en una columna con la etiqueta encima.
- Mapa:
  - Introducción: interfaz (UI) frente a experiencia de usuario (UX) y tutorial de una app de fitness.
  - Cap. 1 Fundamentos: riesgo, coste de interacción, carga cognitiva, sistema de diseño, accesibilidad, patrones y estados.
  - Cap. 2 Menos es más: quitar lo innecesario, revelación progresiva y reducir elecciones.
  - Cap. 3 Color: contraste, color de marca, paletas sólidas, oscuras y transparentes, y nombres de colores.
  - Cap. 4 Maquetación y espaciado: agrupación, jerarquía visual, espaciado, cuadrícula y alineación.
  - Cap. 5 Tipografía: palo seco, pesos, escala, tamaño, interlineado y longitud de línea.
  - Cap. 6 Redacción: concisión, lenguaje llano, enlaces y mensajes de error.
  - Cap. 7 Botones: pesos, desactivados, alineación, tamaño y acciones destructivas.
  - Cap. 8 Formularios: una columna, etiquetas, alternativas a desplegables, pasos y validación.

## [PRACTICAL-UI] Principios y recomendaciones

### P1 · Minimizar los riesgos de usabilidad (minimise usability risks) — [PRACTICAL-UI], cap. 1
Afirma: Dannaway decide según el riesgo de que alguien tenga dificultades: texto fino y gris claro que no se lee, iconos sin etiqueta que no se entienden, títulos en color que parecen enlaces.
Por qué, según el autor: las pruebas detectan los riesgos grandes, no los pequeños, y rara vez se sabe quién usará el producto; hay que pensar en mala vista, poca soltura digital, poca destreza y capacidad cognitiva reducida.
Base: buenas prácticas convencionales y experiencia.
Matices: simplificar lo ambiguo antes de pagar pruebas, que siguen siendo recomendables.

### P2 · Una razón lógica para cada detalle (have a logical reason for every design detail) — [PRACTICAL-UI], cap. 1
Afirma: para Dannaway diseñar no es «dejarlo bonito»: cada detalle mejora la usabilidad por una razón (E1).
Por qué, según el autor: la lógica acelera y permite defender decisiones; «me gusta» no es una crítica.
Base: experiencia. Matices: lo decorativo vale si no estorba (P7).

### P3 · Minimizar el coste de interacción y la carga cognitiva (minimise interaction cost and cognitive load) — [PRACTICAL-UI], cap. 1 y 4
Afirma: Dannaway reduce el esfuerzo (C1) acercando y agrandando las acciones, quitando distracciones (banners animados, ventanas emergentes) y opciones, agrupando y siendo consistente.
Por qué, según el autor: más esfuerzo, más tareas fallidas; por eso triunfan las apps centradas en una tarea.
Base: leyes de Fitts y Hick citadas por su nombre (C3; ver N7); objetivo táctil de 48 × 48 pt (ver N2).
Matices: los pequeños ahorros se suman en acciones repetidas.

### P4 · Buena accesibilidad es gran usabilidad (good accessibility means great usability) — [PRACTICAL-UI], cap. 1
Afirma: Dannaway pide que la interfaz sirva también a personas con ceguera, baja visión, daltonismo o discapacidad motora o mental, cumplir como mínimo las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.1 nivel AA e incluirlas en las pruebas (ver N3).
Por qué, según el autor: todos sufrimos discapacidades temporales (una lesión) o situacionales (sol en la pantalla); además gana clientes y en algunos países es obligatorio.
Matices: el libro no trata el código, del que depende mucho la accesibilidad (C14).

### P5 · Patrones comunes y consistencia (use common design patterns; be consistent) — [PRACTICAL-UI], cap. 1 y 4
Afirma: Dannaway usa soluciones conocidas (C3), hace que lo parecido funcione igual y lo distinto se vea distinto (E5) y sigue las guías de iOS y Android.
Por qué, según el autor: aprovechar lo que la gente ya sabe ahorra aprendizaje, errores y pruebas.
Matices: innovar solo donde está el valor diferencial.

### P6 · Regla 80/20 y costes (use the 80/20 Rule; keep costs in mind) — [PRACTICAL-UI], cap. 1
Afirma: según Dannaway, en torno al 80 % de los efectos sale del 20 % de las causas (principio de Pareto): la mayoría usa pocas funciones, así que se optimizan las tareas comunes y no los casos raros.
Por qué, según el autor: el tiempo cuesta dinero; aconseja reutilizar plantillas e iconos y hablar pronto con los desarrolladores.
Base: el principio de Pareto como aproximación.

### P7 · Quitar información y estilos innecesarios (remove unnecessary information and styles) — [PRACTICAL-UI], cap. 2
Afirma: Dannaway elimina repeticiones, frases introductorias y adornos (líneas, colores, fondos, animaciones) porque cada elemento compite con los demás.
Por qué, según el autor: distraen; un color decorativo parece significar algo y un icono decorativo, un botón.
Matices: las modas envejecen mal; el glasmorfismo (glassmorphism) y el neumorfismo (neumorphism) dificultan contraste y jerarquía.

### P8 · Minimalismo no es simplicidad (don't confuse minimalism with simplicity) — [PRACTICAL-UI], cap. 2
Afirma: Dannaway advierte que «la gente no usa lo que no ve»: si hay sitio, las acciones importantes van visibles, etiquetadas y con contraste.
Por qué, según el autor: los menús ocultos y los iconos sin etiqueta se pasan por alto.
Matices: lo oculto debe ser descubrible. Diseñar primero para el móvil obliga a priorizar, como una casa pequeña obliga a no acumular trastos.

### P9 · No depender solo del color (don't rely on colour alone to convey meaning) — [PRACTICAL-UI], cap. 3
Afirma: Dannaway acompaña el color con icono, borde y fondo en los errores, y con subrayado en los enlaces.
Por qué, según el autor: el daltonismo, más frecuente en hombres, suele confundir rojo y verde.

### P10 · Un solo color de marca, para lo interactivo (use 1 brand colour; apply it to interactive elements) — [PRACTICAL-UI], cap. 3
Afirma: Dannaway usa un color de marca con blanco y negro, solo en enlaces y botones y nunca en títulos, con al menos 4,5:1 de contraste.
Por qué, según el autor: enseña qué es interactivo.
Matices: con varias marcas, la de más contraste; evitar en acciones una marca roja, verde o ámbar (C6); la psicología del color no es universal. Con marca muy clara: retocarla o usar el color de texto con borde de 3:1.

### P11 · Primero en blanco y negro, sin negro puro (use black and white; avoid pure black) — [PRACTICAL-UI], cap. 3 y 5
Afirma: Dannaway diseña en grises y añade color solo donde significa algo; fondo blanco transmite sencillez y negro, lujo o drama.
Por qué, según el autor: sin color se trabaja mejor espaciado, tamaño y contraste. El negro puro sobre blanco cansaría la vista; propone gris oscuro (ver N6).
Matices: el gris claro tampoco: el texto necesita 4,5:1.

### P12 · Espaciar según la relación (space elements based on how closely related they are) — [PRACTICAL-UI], cap. 4
Afirma: para Dannaway la distancia expresa la relación: poca dentro de un grupo y más hacia fuera (M7); ante la duda, más espacio en blanco.
Por qué, según el autor: el espaciado agrupa (C9); lo apretado oculta grupos y jerarquía.
Matices: no hay regla exacta; elegir la opción siguiente y comprobar con M15.

### P13 · Alinear a la izquierda (align text; avoid multiple alignments) — [PRACTICAL-UI], cap. 4 y 5
Afirma: Dannaway alinea a la izquierda, sin que los iconos rompan el borde, y no mezcla alineaciones en un componente.
Por qué, según el autor: el borde recto ancla la vuelta al inicio de línea; la lectura sigue un patrón en F (ver N5).
Matices: centrado solo en textos cortos; nunca justificado, que perjudica con dislexia.

### P14 · Una tipografía de palo seco, regular y negrita (use a single sans serif typeface; regular and bold only) — [PRACTICAL-UI], cap. 5
Afirma: Dannaway usa una sola tipografía sin remates (sans serif), negrita para títulos y regular para el resto.
Por qué, según el autor: es la más legible, neutra y simple; más tipos o pesos añaden ruido.
Matices: con experiencia, una segunda tipografía solo en títulos (C12); pesos extremos solo en grande. Elección en M17.

### P15 · Texto cómodo de leer (make long body text bigger) — [PRACTICAL-UI], cap. 5
Afirma: Dannaway fija para el texto largo 18 px o más, interlineado de 1,5 a 2 y de 40 a 80 caracteres por línea.
Por qué, según el autor: se lee a un brazo de distancia; el interlineado evita releer; las líneas largas pierden el inicio y las cortas cansan.
Matices: a mayor tamaño de letra, menor interlineado y menor espaciado entre letras.

### P16 · Redactar conciso, llano y con lo importante primero (be concise; plain language; front-load text) — [PRACTICAL-UI], cap. 6
Afirma: Dannaway pide frases de menos de 20 palabras, sin jerga, argot ni siglas sin explicar, mayúscula solo inicial, cifras en vez de letras y la clave al principio de títulos, listas y enlaces.
Por qué, según el autor: se escanea y mucha gente lee con dificultad; los lectores de pantalla listan títulos y enlaces fuera de contexto.
Matices: varias pautas son propias del inglés («Específico de otro país», N8).

### P17 · Botones: un primario, a la izquierda, sin desactivados (use a single primary button; left align buttons; try to avoid disabled buttons) — [PRACTICAL-UI], cap. 7
Afirma: Dannaway reserva el primario para la acción principal, ordena los botones de izquierda a derecha por importancia (en móvil, apilados y a ancho completo), los rotula con verbo y sustantivo («Guardar publicación») y evita los desactivados.
Por qué, según el autor: varios primarios compiten; a la derecha se pierden con lupa o en pantallas grandes; los desactivados no explican qué falta ni reciben foco de teclado (M12).
Matices: en diálogos pequeños la derecha también vale; en formularios por pasos, «Atrás» terciario arriba a la izquierda; en buscadores, botón pegado al campo.

### P18 · Formularios en una columna, con campos mínimos y marcados (stack forms in a single column; mark both required and optional fields) — [PRACTICAL-UI], cap. 8
Afirma: Dannaway apila los campos con la etiqueta encima y cerca, pide solo lo esencial, marca obligatorios (asterisco o «obligatorio») y opcionales («opcional») y ajusta el ancho al dato.
Por qué, según el autor: una columna mantiene el recorrido descendente y evita saltarse campos; cada campo extra aumenta abandono y errores; las instrucciones generales se saltan.
Base: experiencia; no cita estudios (ver N6).
Matices: asterisco no rojo y explicado arriba; no hace falta marcar en inicios de sesión; mejor que un opcional, una casilla que revele el campo.

### P19 · Evitar desplegables (try to use radio buttons instead of dropdowns) — [PRACTICAL-UI], cap. 8
Afirma: Dannaway usa botones de opción con 10 opciones o menos, autocompletado en listas largas, selector numérico (stepper) para cantidades pequeñas, casilla para sí/no que se aplica al enviar e interruptor (toggle) para efectos inmediatos.
Por qué, según el autor: el desplegable exige varias interacciones precisas, parece relleno y oculta opciones (E12).
Matices: aceptable si el espacio manda; las listas que hay que explorar se parten en dos campos (sector y ocupación).

## [PRACTICAL-UI] Conceptos y mecanismos

### C1 · Coste de interacción y carga cognitiva (interaction cost; cognitive load) — [PRACTICAL-UI], cap. 1
Qué es: el coste de interacción suma el esfuerzo físico y mental de una tarea (mirar, desplazarse, leer, hacer clic, esperar, teclear, recordar); la carga cognitiva es la potencia mental que exige la interfaz.
Cómo funciona, según el autor: el coste se mide contando clics y desplazamientos (E2). Relación: P3.

### C2 · Sistema de diseño (design system) — [PRACTICAL-UI], cap. 1
Qué es: estilos predefinidos con nombre (tokens), componentes reutilizables y pautas de uso.
Cómo funciona, según el autor: los componentes van de pequeños (botón, avatar) a grandes y a plantillas, en una biblioteca (UI kit). Procedimiento en M1.

### C3 · Leyes citadas (Fitts, Hick, Jakob, posición serial, gradiente de meta) — [PRACTICAL-UI], cap. 1, 4 y 8
Qué es: Fitts: cuanto más cerca y grande el objetivo, antes se pulsa. Hick: decidir tarda más con más opciones y más complejas. Jakob: la gente espera que una interfaz funcione como las que conoce (sus modelos mentales). Posición serial: se recuerdan mejor el primero y el último. Gradiente de meta: la motivación sube cerca del final.
Cómo funciona, según el autor: justifican acercar acciones, reducir opciones (M8), usar patrones, poner el precio al final (M6) y mostrar el progreso (M13). Base: sin estudios citados (ver N7).

### C4 · Estados de interacción (interaction states) — [PRACTICAL-UI], cap. 1 y 3
Qué es: por defecto, cursor encima (hover), pulsado (press), foco de teclado (focus) y desactivado (disabled).
Cómo funciona, según el autor: cada estado debe verse distinto (M5).

### C5 · Contraste: WCAG 2 frente a APCA (contrast ratio; Accessible Perceptual Contrast Algorithm) — [PRACTICAL-UI], cap. 3
Qué es: diferencia de brillo percibido. WCAG 2 la mide de 1:1 a 21:1; APCA, con valores de 15 a 90 que dependen del tamaño y grosor del texto y de cuál es el texto y cuál el fondo.
Cómo funciona, según el autor: WCAG 2 yerra con algunos colores (blanco sobre naranja suspende con 3,04:1 y negro pasa con 4,5:1, aunque se lea peor; APCA da 62 y 43) y con fondos oscuros. Dannaway sitúa APCA en el borrador de WCAG 3 (ver N1): úsese en proyectos personales; en los comerciales con obligación legal, WCAG 2, intentando pasar ambos.

### C6 · Colores de sistema (system colours) — [PRACTICAL-UI], cap. 3
Qué es: rojo para error, ámbar para advertencia y verde para éxito, como un semáforo.
Cómo funciona, según el autor: siempre con icono (P9); 4,5:1 en texto y 3:1 en iconos y elementos.

### C7 · Sistema HSB (hue, saturation, brightness) — [PRACTICAL-UI], cap. 3
Qué es: tono (0 a 360 grados), saturación (0 a 100) y brillo (0, negro, a 100); el valor alfa (0 a 1) da la opacidad.
Cómo funciona, según el autor: las variaciones salen de cambiar saturación y brillo del tono de marca, 230 en el libro (M2).

### C8 · Colores primitivos y semánticos (primitive and semantic colours) — [PRACTICAL-UI], cap. 3
Qué es: los primitivos se nombran por aspecto, color.número de 0 a 1000 según contraste (grey.light.1000), y no se usan directamente; los semánticos o tokens de color se nombran por uso con hasta cuatro palabras, elemento.tono.énfasis.estado (text.error, stroke.strong, fill.success.weak).
Cómo funciona, según el autor: un semántico apunta a un primitivo distinto en claro y en oscuro, lo que facilita cambiar de modo. Elementos posibles: text, stroke, icon, fill, background; tonos: neutral, brand, error, warning, success.

### C9 · Métodos de agrupación (common region, proximity, similarity, continuity) — [PRACTICAL-UI], cap. 4
Qué es: región común (mismo contenedor; la señal más fuerte), proximidad, similitud (tamaño, forma, color) y continuidad (elementos en línea).
Cómo funciona, según el autor: se combinan; si actúan varios, sobra el contenedor (E6); para destacar un miembro del grupo se le hace algo distinto (E4).

### C10 · Jerarquía visual (visual hierarchy) — [PRACTICAL-UI], cap. 3 y 4
Qué es: el orden de importancia que comunica la pantalla.
Cómo funciona, según el autor: se gradúa con tamaño, color (saturación, tono, contraste), estilo, espaciado, posición y profundidad (sombras o tonos más claros parecen más cerca). Procedimiento en M6.

### C11 · Modelo de caja, puntos y cuadrícula (box model; points; 12 column grid) — [PRACTICAL-UI], cap. 4
Qué es: cada elemento es una caja con margen, borde y relleno interior (padding). Se diseña en puntos: 1 pt es 1 px a @1x, 4 px a @2x y 9 px a @3x. La cuadrícula de 12 columnas tiene columnas flexibles, medianiles (gutters) fijos y vacíos y márgenes.
Cómo funciona, según el autor: los contenedores principales se alinean a columnas (12 en escritorio, 4 en móvil); lo interior usa el espaciado predefinido.

### C12 · Tipografías y escala tipográfica (typeface classifications; type scale) — [PRACTICAL-UI], cap. 5
Qué es: cinco clases: con remates (serif), palo seco (sans serif), manuscrita (script), de exhibición (display) y monoespaciada (monospaced, para código y cifras). La escala es la serie de tamaños obtenida multiplicando por un factor fijo.
Cómo funciona, según el autor: palo seco transmite neutralidad; con remates, tradición; redondeada, juego; manuscrita, artesanía o elegancia; fina, lujo. Escalas pequeñas para aplicaciones complejas; grandes para webs comerciales; en móvil, una menor (M9).

### C13 · Revelación progresiva y pirámide invertida (progressive disclosure; inverted pyramid) — [PRACTICAL-UI], cap. 2 y 6
Qué es: mostrar solo lo necesario y el resto bajo demanda; y, en textos, lo más importante primero, luego el apoyo y al final el contexto.
Cómo funciona, según el autor: añade interacciones pero quita carga (E3); quien solo lee el título ya puede actuar (E10).

### C14 · Tecnologías de apoyo (assistive technology) — [PRACTICAL-UI], cap. 1
Qué es: lectores de pantalla (voz o braille) y lupas de pantalla, más usadas que los lectores.
Cómo funciona, según el autor: con lupa se ve solo una porción, y se pierde lo que queda a la derecha o en otra columna; con lector se salta por listas de títulos, enlaces y botones, que deben entenderse solos.

## [PRACTICAL-UI] Métodos y protocolos

### M1 · Crear un sistema de diseño (create a design system) — [PRACTICAL-UI], cap. 1
Objetivo: decidir rápido y con consistencia.
Pasos: 1) predefinir estilos: paleta (M2), escala tipográfica (M9), espaciado XS 8, S 16, M 24, L 32, XL 48 y XXL 80 pt, dos sombras (elevada, pequeña y nítida, para tarjetas; superpuesta, grande y suave, para menús y diálogos) y radios de 8, 16 y 32 pt para elementos pequeños, medianos y grandes; 2) construir componentes y plantillas; 3) escribir pautas de uso, incluida la redacción, que muchos sistemas olvidan.

### M2 · Paleta sólida de cinco variaciones (5 colour variations is often all you need) — [PRACTICAL-UI], cap. 3
Objetivo: paleta monocromática accesible con una función por color.
Pasos: 1) marca, para lo interactivo: HSB 230, 65, 85; 2) texto fuerte (text strong), para títulos, cuerpo y etiquetas: bajar mucho el brillo y saturar, 230, 57, 24; 3) texto débil (text weak), para lo secundario: 230, 27, 48; 4) trazo fuerte (stroke strong), para bordes de campos e iconos: 230, 23, 65; 5) trazo débil (stroke weak), para separadores decorativos: 230, 5, 94; 6) relleno (fill), fondo secundario de etiquetas: 230, 2, 98; 7) fondo 0, 0, 100; 8) comprobar contra el relleno: 4,5:1 marca y textos, 3:1 trazo fuerte; 9) probarlo todo en una pantalla de ejemplo.
Matices: para grises neutros, saturación 0. Los sólidos fallan sobre fondos distintos (M4).

### M3 · Paleta oscura (create a dark colour palette) — [PRACTICAL-UI], cap. 3
Objetivo: modo oscuro legible (ver N4).
Pasos: 1) desde el blanco (texto fuerte 230, 0, 100), subir saturación y bajar brillo: texto débil 230, 5, 85; trazo fuerte 230, 10, 65; trazo débil 230, 15, 25; relleno 230, 20, 15; fondo 230, 30, 10; marca 230, 40, 99; 2) nunca negro puro; 3) contraste muy por encima del mínimo, comprobado con APCA; 4) si la marca no contrasta, aclararla y desaturarla, o usar blanco en lo interactivo; 5) profundidad con tres fondos, porque las sombras no se ven: base 230, 30, 10; elevado 230, 25, 15; superpuesto 230, 20, 20.

### M4 · Paleta transparente (create a transparent colour palette) — [PRACTICAL-UI], cap. 3
Objetivo: que el primer plano conserve su prominencia sobre fondos distintos (E7).
Pasos: 1) fondos oscuros 0, 0, 10; 0, 0, 15; 0, 0, 20, y blancos en claro; 2) oscuro: blanco al 100, 78, 60, 12 y 6 % (texto fuerte, texto débil, trazo fuerte, trazo débil, relleno), comprobado contra el fondo más claro; 3) claro: negro al 90, 60, 45, 10 y 4 %, contra blanco; 4) marca 230, 65, 85 en claro y 230, 36, 100 en oscuro; sistema, claro / oscuro: rojo 0, 71, 78 / 0, 39, 100; ámbar 42, 82, 56 / 42, 50, 88; verde 162, 95, 48 / 162, 40, 78; cada uno al 100 % (texto, 4,5:1), 80 % (trazo fuerte, 3:1), 20 % (trazo débil) y 5 % (relleno); 5) comprobar el texto dentro de insignias y subir el brillo del relleno si queda apagado; 6) probar en una pantalla «fregadero» (kitchen sink) con todos los colores.
Variante monocromática: en oscuro, teñir los fondos (230, 30, 10; 230, 25, 15; 230, 20, 20); en claro, tono 230 y saturación 100 con brillo 15 al 90 %, 20 al 65 %, 30 al 45 %, 40 al 10 % y 50 al 4 % (ver N8).

### M5 · Marcar los estados de interacción — [PRACTICAL-UI], cap. 3
Objetivo: distinguir los estados (C4) sin colores nuevos.
Pasos (combinables): 1) opacidad: 80 % con el cursor encima, 20 % desactivado, contorno para el foco; 2) relleno: sobre blanco, «relleno» al pasar y «trazo débil» al pulsar; en botones de marca, «texto débil» al pasar y «texto fuerte» al pulsar; 3) sombra mayor al pasar; 4) quitar el subrayado al pasar en enlaces, añadirlo en menús; 5) con paleta transparente, capa de «relleno» al pasar y de «trazo débil» al pulsar.

### M6 · Corregir la jerarquía visual — [PRACTICAL-UI], cap. 4
Objetivo: pasar de una tabla plana a una pantalla escaneable (E8).
Pasos: 1) agrupar en secciones y ordenarlas por importancia, lo importante arriba; 2) nombre grande, negrita y texto fuerte; secundarios pequeños y en texto débil; estrellas como iconos; 3) acción y precio elevados con sombra y fijos abajo, al alcance del pulgar, con el precio al final (posición serial, C3); 4) detalles con icono de contorno en trazo fuerte y etiqueta en texto débil; 5) quitar etiquetas obvias («descripción»); 6) comprobar con M15.

### M7 · Espaciar de dentro afuera — [PRACTICAL-UI], cap. 4
Objetivo: espaciado que refleje relaciones.
Pasos: 1) opciones «de talla de camiseta» en múltiplos de 8 pt (cuadrícula de 8 puntos; 4 pt en interfaces muy detalladas), que crecen a saltos mayores; 2) ver la pantalla como rectángulos anidados; 3) XS en lo más interior, M en el relleno de tarjetas, L entre tarjetas y enlaces de navegación, XXL entre secciones; 4) fijar reglas: 24 pt de relleno en tarjetas, 32 pt entre columnas, 80 pt entre secciones.
Base: muchas pantallas son divisibles por 8.

### M8 · Reducir elecciones (reduce choice to speed up decision making) — [PRACTICAL-UI], cap. 2
Objetivo: decisiones más rápidas.
Pasos: 1) eliminar lo que no se gana su sitio (E3); 2) agrupar por categorías; 3) dividir en pasos o niveles; 4) recomendar lo popular (búsquedas sugeridas).

### M9 · Crear una escala tipográfica (use a type scale) — [PRACTICAL-UI], cap. 5
Objetivo: pocos tamaños que combinen.
Pasos: 1) base de 16 px; 2) multiplicar por el factor (1,2): 16 × 1,2 = 19,2, redondeado a 20, y así sucesivamente; 3) redondear; 4) interlineados múltiplos de 4; 5) ajustar con experiencia y no crear estilos que no se usen. Resultado en «Cifras».

### M10 · Texto legible sobre fotos (ensure text on photos is legible) — [PRACTICAL-UI], cap. 5
Objetivo: 4,5:1 en texto de 18 px o menos y 3:1 en grande.
Pasos (opciones): 1) degradado gris oscuro del 90 % de opacidad abajo al 0 % a media altura, más sombra de texto; 2) capa uniforme al 50 %; 3) capa desenfocada; 4) fondo sólido tras el texto, como en subtítulos.

### M11 · Fricción en acciones destructivas (add friction to destructive actions) — [PRACTICAL-UI], cap. 7
Objetivo: evitar borrados accidentales.
Pasos: 1) inicial: acción poco prominente (terciaria), alejada o revelada progresivamente, sin rojo; 2) ligera: pedir confirmación; 3) moderada: confirmación en rojo avisando de que no se recuperará; 4) fuerte: rojo y casilla obligatoria («confirmo que quiero eliminar mi cuenta»); 5) si se puede, permitir deshacer.

### M12 · Alternativas a los botones desactivados — [PRACTICAL-UI], cap. 7
Objetivo: que nadie se atasque (P17).
Pasos (opciones): 1) botón activo y validar al enviar (E11); 2) quitar acciones no disponibles y explicar por qué; 3) candado en botones normales, útil en funciones de pago, explicando cómo acceder; 4) si no hay remedio, mensaje junto al botón, descripción emergente (tooltip) y foco de teclado.

### M13 · Formularios de varios pasos (break up long forms into multiple steps) — [PRACTICAL-UI], cap. 8
Objetivo: menos errores y más formularios terminados.
Pasos: 1) avisar de la duración y de lo que hará falta; 2) 30 preguntas en 6 pasos de 5, no en 30; 3) de lo fácil a lo difícil; 4) mostrar el progreso («Paso 2 de 3»), que motiva (C3); 5) permitir revisar antes de enviar; 6) confirmar el éxito y decir qué pasará. Si no se puede dividir, agrupar bajo títulos.

### M14 · Elegir cómo validar (choose your form validation approach) — [PRACTICAL-UI], cap. 8
Objetivo: avisar de errores y ayudar a corregirlos; se pueden combinar.
Pasos: 1) al enviar, lo más sencillo: error encima del campo (debajo lo tapan el autocompletado y el teclado), borde rojo, fondo e icono, y con varios errores, lista arriba con enlaces, aunque llegan todos de golpe; 2) al salir del campo (validación en línea, «on blur»): inmediato y con contexto, pero distrae, va mal en grupos de casillas y es complejo; el error se quita al corregirlo; 3) al teclear, con retraso: ayuda a crear contraseñas (al menos 8 caracteres) o elegir usuario, pero los avisos prematuros frustran.

### M15 · Prueba de entrecerrar los ojos (The Squint Test) — [PRACTICAL-UI], cap. 4
Objetivo: comprobar jerarquía y espacio.
Pasos: 1) entrecerrar los ojos, alejarse, reducir el zoom o desenfocar; 2) debe verse lo más importante y para qué es la pantalla; 3) si no, más espacio o contraste.

### M16 · Regla de los tercios (Rule of Thirds) — [PRACTICAL-UI], cap. 4
Objetivo: fotos con equilibrio y movimiento.
Pasos: 1) cuadrícula de 3 × 3; 2) sujeto en uno de los cuatro cruces; 3) horizonte sobre una línea.

### M17 · Elegir tipografía (choose a sans serif typeface) — [PRACTICAL-UI], cap. 5
Objetivo: una tipografía legible y fiable.
Pasos: 1) popular y probada; 2) con muchos pesos; 3) altura de x (x-height) alta y espaciado amplio; 4) que admita los idiomas necesarios y funciones OpenType; 5) en caso de duda, la del sistema.

## [PRACTICAL-UI] Ejemplos y casos
E1 · Fila de tres bloques con icono en la que cada detalle tiene su razón (alineación, enlaces descriptivos, espaciado interno menor que externo); ilustra P2 (cap. 1).
E2 · Taza en una tienda: con desplegable y botón lejano, comprar 2 cuesta 3 clics y 1 desplazamiento; con selector numérico y botón al lado, 2 clics (cap. 1).
E3 · Suscripción reducida a solo el email, y casilla «Recibir avisos por SMS» que revela el campo del móvil (cap. 2 y 8).
E4 · Tres planes de precio en los que el central destaca por tamaño, borde, sombra, botón relleno e insignia «más popular» (cap. 4).
E5 · Insignias «Verificado» que parecían el botón primario, cambiadas a verde, más redondeadas y con fondo claro (cap. 4).
E6 · Tabla de canciones de un reproductor que prescinde del contenedor porque ya la agrupan proximidad, similitud y continuidad (cap. 4).
E7 · Etiquetas grises sólidas que pierden prominencia sobre fondo gris y en modo oscuro, resuelto con transparencias (cap. 3).
E8 · App de reserva de una casa de playa que pasa de tabla plana a cuatro secciones jerarquizadas (M6) (cap. 4).
E9 · Menú lateral de un blog con el botón de cierre movido al punto de apertura y categorías más grandes; ilustra la Ley de Fitts (cap. 4).
E10 · Pantalla de sincronizar contactos construida como pirámide invertida (cap. 6).
E11 · Pago con un campo olvidado: con el botón desactivado nadie sabe qué falla; activo, el error aparece al enviar (cap. 7).
E12 · Elegir 2 adultos, 1 niño y 1 bebé: 6 clics y 3 desplazamientos con desplegables; 4 clics con selectores numéricos (cap. 8).
E13 · «¡Uy, algo salió mal!» con «Ok», reescrito como «Pago fallido. Actualiza tus datos de pago» con botón «Actualizar datos de pago» (cap. 6).
E14 · Tutorial de la app de fitness: botón de 48 pt abajo y a ancho completo, iconos de contorno, acciones visibles, marca solo en lo interactivo, gris oscuro, Inter en vez de League Spartan (altura de x baja), interlineado 1,5, jerga («pranayama») cambiada por palabras llanas y botón «Inhale good vibes» rebautizado «Start workout» (introducción a cap. 7).

## [PRACTICAL-UI] Errores frecuentes y advertencias
- Campos no convencionales o con la etiqueta dentro, que parecen rellenos (cap. 1 y 8).
- Ocultar acciones en menús habiendo sitio (cap. 2).
- Color de marca en elementos no interactivos, o dos colores para lo interactivo (cap. 3).
- Contenedores para todo y el mismo espaciado en todas partes (cap. 4).
- Ocultar datos que desbordan en vez de hacer el componente flexible; si hay que recortar, mejor por el medio (cap. 4).
- Cuerpo de 14 px, interlineado de 1, líneas de toda la anchura y texto blanco directo sobre foto (cap. 5).
- Mayúsculas en cada palabra (title case) y texto en MAYÚSCULAS, salvo etiquetas cortas, pequeñas, en negrita y espaciadas (cap. 6).
- «Mi email» en etiquetas, porque habla la interfaz; basta «Email» (cap. 6).
- Vocabulario inconsistente («cesta» y «bolsa», «registrarse» y «darse de alta») (cap. 6).
- Enlaces «más información» o «haz clic aquí» (cap. 6).
- Errores que culpan, piden perdón o usan jerga (cap. 6).
- Nueve errores de botones, sin figuras en el texto: rellenos o bordes por debajo de 3:1, secundario gris claro que parece desactivado, primario y secundario distinguibles solo por color, texto por debajo de 4,5:1, formas distintas sin motivo y pesos visuales parecidos (cap. 7).
- «Atrás» junto al primario en formularios por pasos, que hace perder datos (cap. 7).
- Pistas ocultas o debajo del campo: van visibles y encima (cap. 8).
- Marcador de posición (placeholder) como etiqueta: desaparece, parece relleno y no contrasta; solo vale en buscadores con 4,5:1 y etiqueta accesible (cap. 8).
- Bordes de campo por debajo de 3:1 (cap. 8).
- Casillas en negativo: si al cambiar la casilla por «sí» la frase confunde, hay que reescribirla (cap. 8).

## [PRACTICAL-UI] Ejercicios y acciones
- Tutorial acumulativo: al final de los capítulos 1 a 7 se mejora la pantalla de un entrenamiento de yoga en una app ficticia (E14); el capítulo 8 no tiene tutorial (introducción a cap. 7).
- Probar la paleta en una pantalla con todas las variaciones, también en modo oscuro (cap. 3).
- Pasar la prueba de entrecerrar los ojos a los propios diseños (cap. 4).
- Validar las pautas con pruebas de usabilidad propias que incluyan a personas con discapacidad (introducción y cap. 1).

## [PRACTICAL-UI] Cifras y reglas concretas
- Mínimo de accesibilidad: WCAG 2.1 nivel AA (cap. 1; ver N3).
- Objetivo táctil de al menos 48 × 48 pt; botones separados al menos 8 pt, Dannaway suele usar 16 (cap. 1, 4 y 7; ver N2).
- Contraste WCAG 2: 4,5:1 para texto de 18 px o menos; 3:1 para texto grande (más de 18 px en negrita o más de 24 px regular) y controles como campos, casillas, botones e interruptores; lo decorativo, sin mínimo (cap. 3, 7 y 8).
- APCA: 90 preferido para cuerpo (14 px o más); 75 mínimo para cuerpo (18 px o más); 60 para otro texto (24 px regular o 16 px negrita); 45 para texto grande (36 px regular o 24 px negrita) y controles; 30 mínimo absoluto (marcador de posición, botón desactivado); 15 para elementos no textuales (cap. 3; ver N1).
- Espaciado: XS 8, S 16, M 24, L 32, XL 48 y XXL 80 pt; radios de 8, 16 y 32 pt (cap. 1 y 4).
- Cuadrícula: 12 columnas en escritorio y 4 en móvil; medianiles de 32 y 16 pt; márgenes de 80 y 16 pt (cap. 4).
- Factores de escala: 1,067; 1,125; 1,200; 1,250; 1,333; 1,414; 1,500; 1,618 (cap. 5).
- Escala de Dannaway, tamaño e interlineado en px: 40/48, 32/40, 24/32, 20/28, 16/24 y 14/20 (cap. 1 y 5).
- Texto largo: 18 px o más, interlineado de 1,5 a 2 (títulos menos: 24 px a 1,3), de 40 a 80 caracteres por línea (cap. 5).
- Etiquetas en mayúsculas: 14 px, negrita, 2 px de espaciado entre letras (cap. 6).
- Frases de menos de 20 palabras; lenguaje para un alumno de sexto curso (cap. 6).
- Hasta 10 opciones, botones de opción; 10 sugerencias como máximo en un autocompletado (cap. 8).
- Etiqueta a 4 pt de su campo y 32 pt entre campos (cap. 8).
- 30 preguntas en 6 pasos de 5 (cap. 8).

## [PRACTICAL-UI] Preguntas que este libro responde
- ¿Cómo empiezo a diseñar sin talento artístico? Según Dannaway en [PRACTICAL-UI], con pautas lógicas: diseñar en grises, predefinir estilos y justificar cada detalle. P2, P11 y M1 (cap. 1 y 3).
- ¿Qué contraste necesita el texto? Según Dannaway en [PRACTICAL-UI], 4,5:1 hasta 18 px y 3:1 en texto grande y controles, comprobando también con APCA. C5 (cap. 3; ver N1).
- ¿Cuántos colores necesita una paleta? Según Dannaway en [PRACTICAL-UI], uno de marca con cinco variaciones más el fondo. M2 (cap. 3).
- ¿Cómo hago un modo oscuro? Según Dannaway en [PRACTICAL-UI], partiendo del blanco, sin negro puro y con tres fondos para la profundidad. M3 y M4 (cap. 3; ver N4).
- ¿Qué tamaño deben tener los botones? Según Dannaway en [PRACTICAL-UI], 48 × 48 pt como mínimo, separados 8 pt. P3 (cap. 1 y 7; ver N2).
- ¿Cuánto espacio dejo entre elementos? Según Dannaway en [PRACTICAL-UI], el que marque su relación, en múltiplos de 8 pt y creciendo hacia fuera. P12 y M7 (cap. 4).
- ¿Qué tipografía y tamaño uso? Según Dannaway en [PRACTICAL-UI], una palo seco en regular y negrita, con cuerpo de 18 px e interlineado de 1,5. P14, P15 y M17 (cap. 5).
- ¿Es verdad que el negro puro cansa la vista? Según Dannaway en [PRACTICAL-UI], sí, pero no cita estudios. P11 (cap. 3; ver N6).
- ¿Dónde pongo los botones? Según Dannaway en [PRACTICAL-UI], a la izquierda y por importancia, con un solo primario. P17 (cap. 7).
- ¿Desactivo el botón de enviar hasta completar el formulario? Según Dannaway en [PRACTICAL-UI], no: activo y validar al enviar. M12 y M14 (cap. 7 y 8).
- ¿Cómo evito borrados por error? Según Dannaway en [PRACTICAL-UI], con fricción proporcional y opción de deshacer. M11 (cap. 7).
- ¿Cómo hago un formulario fácil? Según Dannaway en [PRACTICAL-UI], una columna, etiquetas encima, pocos campos bien marcados y sin desplegables innecesarios. P18 y P19 (cap. 8).
- ¿Cuándo muestro los errores de un formulario? Según Dannaway en [PRACTICAL-UI], al enviar si hay pocos recursos, o al salir del campo o al teclear si hace falta ayuda inmediata. M14 (cap. 8).
- ¿Cómo escribo los textos de una app? Según Dannaway en [PRACTICAL-UI], conciso, llano, lo importante primero y botones con verbo y sustantivo. P16 y E13 (cap. 6 y 7).

## [PRACTICAL-UI] Glosario
- Interfaz de usuario (user interface, UI): lo que se ve y se usa en un producto digital.
- WCAG (Web Content Accessibility Guidelines): pautas internacionales de accesibilidad web.
- APCA (Accessible Perceptual Contrast Algorithm): método de medir contraste según la percepción.
- Coste de interacción (interaction cost): esfuerzo físico y mental de una tarea.
- Carga cognitiva (cognitive load): esfuerzo mental que exige una interfaz.
- Sistema de diseño (design system): estilos, componentes y pautas de uso.
- Lector de pantalla (screen reader): programa que lee la interfaz en voz o braille.
- Lupa de pantalla (screen magnifier): programa que amplía parte de la pantalla.
- Revelación progresiva (progressive disclosure): mostrar la información cuando hace falta.
- Color semántico (semantic colour): nombre de color según su uso.
- Jerarquía visual (visual hierarchy): orden de importancia visible.
- Modelo de caja (box model): margen, borde y relleno de cada elemento.
- Punto (point, pt): unidad independiente de la resolución.
- Medianil (gutter): espacio vacío entre columnas.
- Altura de x (x-height): altura de las minúsculas.
- Interlineado (line height): distancia entre líneas, relativa al tamaño de letra.
- Mayúscula solo inicial (sentence case): solo la primera palabra y los nombres propios.
- Selector numérico (stepper): campo con botones + y −.

## [PRACTICAL-UI] Específico de otro país
- [Específico del inglés] P16, cap. 6: las listas de palabras sobrantes («actually», «basically», los artículos «a», «an», «the»), las contracciones («you're»), la crítica a las mayúsculas en cada palabra y el «sexto curso» (6th grade) del sistema escolar de EE. UU.
- [Específico del inglés] P16, cap. 6: separar los miles con coma (1,000) y escribir «1 billion» (ver N8).
- [Específico de Australia] P18, cap. 8: el código postal de 4 cifras como ejemplo de ancho de campo.
- No hay consejos legales ni fiscales; el libro solo dice que la accesibilidad es obligatoria «en algunos países» (ver N3).

## [PRACTICAL-UI] Notas de Claude

### N1 · APCA no forma parte de WCAG 3 — [PRACTICAL-UI], sobre C5, cap. 3
Qué dice el libro: Dannaway presenta APCA como parte del borrador de WCAG 3.
Qué se sabe hoy: el W3C lo retiró del borrador en julio de 2023; en abril de 2026 el algoritmo de contraste de WCAG 3 sigue «por determinar» y la norma está a años de cerrarse. Los valores de APCA son una propuesta, no un requisito.
Fuente: Adrian Roselli, «WCAG3 Contrast as of April 2026», adrianroselli.com, abril de 2026.

### N2 · El tamaño de objetivo de WCAG — [PRACTICAL-UI], sobre P3, cap. 1 y 7
Qué dice el libro: 48 × 48 pt sería algo más que los 44 × 44 pt que recomienda WCAG.
Qué se sabe hoy: 44 × 44 px es el criterio 2.5.5, de nivel AAA; para el nivel AA, WCAG 2.2 (octubre de 2023) exige 24 × 24 px CSS (criterio 2.5.8). Los 44 pt son de Apple y los 48 dp, de Material Design de Google. Los 48 pt cumplen de sobra.
Fuente: Eric Bailey, Smashing Magazine, 19 de julio de 2024.

### N3 · WCAG vigente y ley española — [PRACTICAL-UI], sobre P4, cap. 1
Qué dice el libro: WCAG 2.1 AA y obligación legal «en algunos países».
Qué se sabe hoy: la versión vigente es WCAG 2.2. En España, el Real Decreto 1112/2018 obliga al sector público (WCAG 2.1 AA mediante la norma EN 301 549) y la Ley 11/2023, que transpone el Acta Europea de Accesibilidad, rige desde el 28 de junio de 2025 para servicios de consumo como el comercio electrónico o la banca. Excepciones sin comprobar en el BOE.
Fuente: AllAccessible, 9 de octubre de 2023; Wawsome, «Spain digital accessibility laws guide», 8 de diciembre de 2025.

### N4 · Modo oscuro y vista — [PRACTICAL-UI], sobre M3, cap. 3
Qué dice el libro: la evidencia sería contradictoria.
Qué se sabe hoy: con visión normal rinde mejor el modo claro, sobre todo con letra pequeña (Piepenbrock y colaboradores, 2013); con cataratas se lee mejor en oscuro (Legge y colaboradores, 1985). Se aconseja ofrecer el modo oscuro como opción, no por defecto.
Fuente: Raluca Budiu, Nielsen Norman Group, 2 de febrero de 2020.

### N5 · El patrón de lectura en F — [PRACTICAL-UI], sobre P13 y P17, cap. 5 y 7
Qué dice el libro: se leería siempre en F.
Qué se sabe hoy: el patrón viene de estudios de seguimiento ocular de Nielsen Norman Group, que luego aclaró que no es universal y que surge sobre todo con textos mal estructurados. Que el borde izquierdo recibe mucha atención sigue siendo válido.
Fuente: conocimiento general de Claude, sin comprobar en detalle.

### N6 · Pautas sin estudios — [PRACTICAL-UI], sobre P11 y P18, cap. 3, 5 y 8
Qué dice el libro: el negro puro cansa, una columna y etiquetas encima aceleran los formularios y marcar opcionales sería requisito de accesibilidad. No cita ningún estudio ni trae bibliografía.
Qué se sabe hoy: Claude no conoce pruebas sólidas de la fatiga por negro puro ni ha comprobado los estudios sobre formularios; WCAG pide indicar los obligatorios, no marcar los opcionales.
Fuente: conocimiento general de Claude, sin comprobar.

### N7 · Alcance de Fitts y Hick — [PRACTICAL-UI], sobre C3 y P3, cap. 1 y 2
Qué dice el libro: ambas leyes justifican acercar objetivos y reducir opciones.
Qué se sabe hoy: Fitts está bien respaldada para apuntar; Hick describe reacciones ante opciones simples y no se aplica tal cual a elegir productos o leer menús. Reducir opciones suele ayudar, sin fórmula exacta.
Fuente: conocimiento general de Claude, sin comprobar.

### N8 · Convenciones del inglés e incoherencias menores — [PRACTICAL-UI], sobre P16 y M4, cap. 3 y 6
Qué dice el libro: escribir 1,000 y «1 billion»; la opacidad del texto débil claro aparece al 60 % y al 65 %, y la del relleno al 4 % y al 5 %.
Qué se sabe hoy: «billion» son mil millones, y en España los miles se separan con punto o con espacio, no con coma. Las diferencias de opacidad son menores; el autor invita a ajustarlas.
Fuente: conocimiento general de Claude, sin comprobar.
