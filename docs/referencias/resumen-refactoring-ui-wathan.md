# [REFACTORING-UI] Resumen — Refactoring UI (Adam Wathan y Steve Schoger, año no indicado)

Convenciones: (cap. N) es el capítulo de origen; las «Notas de Claude» son del resumidor, no del autor; [Específico de …] no se aplica tal cual en España. El libro tiene nueve partes, aquí capítulos 1 a 9, divididas en apartados breves. P, C, M, E, R y N son identificadores para referencias cruzadas.

## [REFACTORING-UI] Ficha
- Título: Refactoring UI. No consta edición española.
- Autor: Adam Wathan y Steve Schoger. El archivo no trae biografía ni formación; el cierre se dirige a quien quiere que su trabajo luzca bien sin depender de un diseñador. Intereses: enlaza un recurso propio (ver N2).
- Año: año no indicado en el archivo; a finales de 2018 se anunciaba como inminente (ver N2).
- Idioma del original: inglés.
- Tipo: práctico.
- A quién sirve: a programadores, emprendedores y principiantes que hacen webs o aplicaciones y quieren que parezcan profesionales con reglas concretas, sin talento artístico.
- Tesis: una interfaz parece bien diseñada por aplicar con método pocas técnicas: jerarquía visual clara, sistemas de valores fijados de antemano (espaciado, letra, color, sombras) y decisiones deliberadas en lugar de valores por defecto.
- Temas: diseño y experiencia de usuario, toma de decisiones, productividad, creatividad.
- Ideas esenciales:
  - Empezar por una funcionalidad, en baja fidelidad y sin color (P1).
  - Elegir de sistemas definidos de antemano, por eliminación (P4, M1).
  - La jerarquía visual es lo que más hace que algo parezca diseñado (C1, P5).
  - Jerarquizar con peso y color antes que con tamaño, y restar énfasis a lo secundario (P5, P7).
  - Empezar con demasiado espacio en blanco y quitar (P12).
  - Escalas de espaciado y de letra no lineales (M2, M3).
  - Paleta amplia de grises, primarios y acentos con 5 a 10 tonos cada uno (P19, M5).
  - Luz desde arriba y sombras como sistema de elevación (P22, M8).
  - Contraste constante para el texto sobre imágenes (M9).
  - Rematar con bordes de acento, fondos, estados vacíos y menos bordes (P28-P30).
- Mapa:
  - Cap. 1, Starting from Scratch: por dónde empezar, cuánto detallar, personalidad y sistemas.
  - Cap. 2, Hierarchy is Everything: jerarquía con tamaño, peso, color, etiquetas, títulos, iconos y botones.
  - Cap. 3, Layout and Spacing: espacio en blanco, escala de espaciado, anchura, rejillas y agrupación.
  - Cap. 4, Designing Text: escala tipográfica, fuentes, longitud de línea, alineación e interlineado.
  - Cap. 5, Working with Color: HSL, paleta, tonos, saturación, brillo percibido y accesibilidad.
  - Cap. 6, Creating Depth: luz, sombras, elevación, diseño plano y superposición.
  - Cap. 7, Working with Images: fotos, texto sobre imágenes, tamaños de iconos y capturas, imágenes de usuarios.
  - Cap. 8, Finishing Touches: realzar lo existente, bordes de acento, fondos, estados vacíos y menos bordes.
  - Cap. 9, Leveling Up: seguir aprendiendo con diseños ajenos.

## [REFACTORING-UI] Principios y recomendaciones

### P1 · Funcionalidad primero, detalle después (start with a feature, not a layout; detail comes later) — [REFACTORING-UI], cap. 1
Afirma: Wathan y Schoger aconsejan empezar por una funcionalidad real, como buscar un vuelo (E1), y no por el armazón (navegación, logotipo), en baja fidelidad y en escala de grises (grayscale).
Por qué, según el autor: sin varias funcionalidades hechas falta información para decidir la navegación; sin color, espaciado, contraste y tamaño deben crear la jerarquía. Los bocetos son desechables: hay que construir lo real cuanto antes.
Base: experiencia de los autores; truco de Jason Fried, de Basecamp, de bocetar con rotulador grueso; Google funcionó casi sin armazón.

### P2 · Ciclos cortos y pesimismo (work in cycles, be a pessimist) — [REFACTORING-UI], cap. 1
Afirma: se diseña una versión simple de la siguiente funcionalidad, se construye y se itera, sin diseñarlo todo antes ni insinuar funciones aún no construibles.
Por qué, según el autor: es más fácil corregir una interfaz utilizable que imaginar casos límite, y una parte difícil prevista desde el inicio puede bloquearlo todo (E2).
Base: razonamiento y caso ilustrativo de los autores.
Matices: dejar lo «deseable» para después asegura una versión mínima publicable.

### P3 · Elegir una personalidad (choose a personality) — [REFACTORING-UI], cap. 1
Afirma: la personalidad (seria en un banco, lúdica en una empresa emergente) la deciden tipografía, color, radio de las esquinas y lenguaje.
Por qué, según el autor: letra con remates (serif), elegancia; sin remates redondeada, juego; neutra, deja hablar a lo demás. Azul, seguro; dorado, caro; rosa, desenfadado. Esquinas muy redondeadas, lúdicas; rectas, formales. Un tono cercano resulta amable; uno impersonal, oficial.
Base: opinión de los autores, que se guían más por cómo se siente cada color que por la psicología del color.
Matices: no mezclar esquinas rectas y redondeadas; inspirarse en webs del público objetivo sin copiar a la competencia.

### P4 · Limitar las opciones y sistematizarlo todo (limit your choices, systematize everything) — [REFACTORING-UI], cap. 1
Afirma: se elige de conjuntos pequeños definidos de antemano (8 a 10 tonos por color, una escala tipográfica cerrada) para todo lo enumerado en R11.
Por qué, según el autor: sin restricciones siempre hay varias opciones correctas y decidir es una tortura (E3); con sistemas se decide una vez y se gana rapidez y coherencia.
Base: razonamiento de los autores.
Matices: basta con no tomar dos veces la misma decisión menor (M1).

### P5 · No todo es igual, y el tamaño no lo es todo (not all elements are equal; size isn't everything) — [REFACTORING-UI], cap. 2
Afirma: la jerarquía visual (C1) es lo que más hace que algo «quede bien», y se construye con peso y color además de tamaño.
Por qué, según el autor: si todo compite, hay ruido; usar solo el tamaño hace lo principal enorme y lo secundario minúsculo, mientras negrita y color suave jerarquizan sin perder legibilidad.
Base: comparaciones visuales (figuras no incluidas).
Matices: dos o tres colores de texto y dos pesos (R2).

### P6 · Nada de texto gris sobre fondos de color (don't use grey text on colored backgrounds) — [REFACTORING-UI], cap. 2
Afirma: sobre fondo de color, el texto secundario lleva un color del mismo tono (hue) que el fondo, ajustando saturación y luminosidad a ojo (C2).
Por qué, según el autor: lo que jerarquiza es reducir el contraste; el blanco translúcido parece apagado o desactivado y deja ver el fondo.
Base: experiencia de los autores.

### P7 · Enfatizar quitando énfasis (emphasize by de-emphasizing) — [REFACTORING-UI], cap. 2
Afirma: si lo principal no destaca, se debilita lo que compite con él: navegación inactiva más suave, barra lateral sin color de fondo.
Por qué, según el autor: añadir más énfasis al elemento principal no siempre basta.
Base: ejemplos de los autores.

### P8 · Las etiquetas son el último recurso (labels are a last resort) — [REFACTORING-UI], cap. 2
Afirma: al mostrar datos (no en formularios) conviene evitar «etiqueta: valor», que da a todo el mismo peso.
Por qué, según el autor: a menudo basta el formato (correo, teléfono, precio) o el contexto; si no, se fusionan: «12 en existencias», «3 dormitorios».
Base: ejemplos de los autores.
Matices: en paneles de datos parecidos, la etiqueta se mantiene rebajada; si el usuario la busca, como «grosor» en una ficha técnica, se destaca ella.

### P9 · Jerarquía visual distinta de la del documento (separate visual hierarchy from document hierarchy) — [REFACTORING-UI], cap. 2
Afirma: las etiquetas HTML (h1, h2…) se eligen por significado y se estilan según la jerarquía visual; en aplicaciones, muchos títulos de sección funcionan como etiquetas y deben ser pequeños.
Por qué, según el autor: el navegador agranda los encabezados por defecto, lo que invita a títulos demasiado grandes.
Base: razonamiento de los autores.
Matices: un título puede quedar en el código por accesibilidad y ocultarse a la vista.

### P10 · Equilibrar peso y contraste (balance weight and contrast) — [REFACTORING-UI], cap. 2
Afirma: lo pesado se compensa bajando su contraste (iconos macizos de color suave junto al texto) y lo de poco contraste, con más peso (un borde tenue se ensancha en vez de oscurecerse).
Por qué, según el autor: la negrita y los iconos destacan porque cubren más superficie.
Base: razonamiento de los autores.

### P11 · Las acciones, por jerarquía antes que por significado (semantics are secondary) — [REFACTORING-UI], cap. 2
Afirma: casi toda página tiene una acción principal (fondo macizo de alto contraste), un par de secundarias (contorno o fondo suave) y pocas terciarias (aspecto de enlace).
Por qué, según el autor: así la interfaz se ve menos recargada y comunica mejor.
Base: ejemplos de los autores.
Matices: una acción destructiva que no es la principal va discreta; el botón grande y rojo se reserva para la confirmación.

### P12 · Empezar con demasiado espacio en blanco (start with too much white space) — [REFACTORING-UI], cap. 3
Afirma: el espacio en blanco se quita, no se añade: se empieza con muchísimo y se reduce.
Por qué, según el autor: añadiendo poco a poco se da lo mínimo para no verse mal; lo excesivo en un elemento aislado resulta justo en la interfaz completa.
Base: experiencia de los autores.
Matices: las interfaces densas, como paneles de datos, valen si se eligen deliberadamente.

### P13 · No llenar la pantalla ni obedecer ciegamente a la rejilla (you don't have to fill the whole screen; grids are overrated) — [REFACTORING-UI], cap. 3
Afirma: si algo necesita 600 px, se usan 600 aunque haya 1.200-1.400, y no todo debe tener ancho fluido de rejilla (grid).
Por qué, según el autor: una barra lateral al 25 % crece de más o se queda corta: mejor ancho fijo y que el contenido ocupe el resto. Lo que tiene tamaño óptimo, como una tarjeta de acceso de unos 500 px, lleva ancho máximo (max-width) y solo encoge si no cabe (E4).
Base: razonamiento y ejemplos de los autores.
Matices: algo estrecho en una interfaz ancha se divide en columnas (E5); ayuda diseñar en pequeño (M10).

### P14 · El tamaño relativo no escala (relative sizing doesn't scale) — [REFACTORING-UI], cap. 3
Afirma: no conviene fijar proporciones permanentes entre elementos ni dentro de un componente.
Por qué, según el autor: un titular de 2,5em da 45 px en escritorio pero 35 px en móvil, cuando bastan 20-24 px (R7); lo grande debe encoger más deprisa. Un botón con relleno proporcional a la letra parece el mismo con zoom; más relleno en el grande y menos en el pequeño los hace parecer de su tamaño.
Base: ejemplos de los autores.

### P15 · Evitar el espaciado ambiguo (avoid ambiguous spacing) — [REFACTORING-UI], cap. 3
Afirma: sin separador visible, debe haber más espacio alrededor de un grupo que dentro de él.
Por qué, según el autor: si una etiqueta dista lo mismo de su campo que del anterior, se rellena el equivocado; pasa también con encabezados y listas.
Base: ejemplos de los autores.

### P16 · Controlar la longitud de línea (keep your line length in check) — [REFACTORING-UI], cap. 4
Afirma: los párrafos deben tener de 45 a 75 caracteres por línea, unos 20-35em, aunque la zona de contenido sea más ancha por las imágenes.
Por qué, según el autor: el error habitual es ajustar el texto al diseño y no a la lectura.
Base: no citan fuente (ver N3).

### P17 · Línea base e interlineado proporcional (baseline, not center; line-height is proportional) — [REFACTORING-UI], cap. 4
Afirma: los tamaños mezclados en una línea se alinean por la línea base (C5), no centrados; el interlineado (line-height) crece con la longitud de línea y decrece con el tamaño de letra (R10).
Por qué, según el autor: el ojo ya percibe la línea base; el interlineado ayuda a encontrar la línea siguiente, más difícil cuanto más lejos salta el ojo y menor es la letra.
Base: razonamiento de los autores.

### P18 · Enlaces, alineación y espaciado entre letras — [REFACTORING-UI], cap. 4
Afirma: donde casi todo es enlace, basta más peso o un color más oscuro, y los secundarios pueden marcarse solo al pasar el ratón. Se centran solo titulares y bloques de dos o tres líneas; los números de tabla van a la derecha; se justifica solo con división silábica (hyphenation) (ver N5). El espaciado entre letras (letter-spacing) se respeta, salvo apretarlo en titulares con familias de espaciado amplio y abrirlo en mayúsculas.
Por qué, según el autor: los números alineados se comparan de un vistazo; las mayúsculas, de igual altura, se distinguen peor (C5); las fuentes de titulares rara vez sirven pequeñas.
Base: experiencia de los autores.

### P19 · Hacen falta más colores de los que se cree (you need more colors than you think) — [REFACTORING-UI], cap. 5
Afirma: las paletas de cinco colores no bastan; hacen falta grises (8 a 10), uno o dos primarios y acentos, con varios tonos cada uno (R14).
Por qué, según el autor: casi todo es gris, empezando por uno muy oscuro, porque el negro puro parece artificial. Los primarios dan carácter: sus tonos claros tiñen avisos y los oscuros sirven para texto. Los acentos marcan novedades y estados: rojo destructivo, amarillo advertencia, verde positivo.
Base: experiencia de los autores.
Matices: gráficos o calendarios con muchas categorías exigen más colores. Construcción en M5.

### P20 · Saturación en los extremos y grises con temperatura (don't let lightness kill your saturation; greys don't have to be grey) — [REFACTORING-UI], cap. 5
Afirma: cuanto más se aleja la luminosidad del 50 %, más saturación necesita un tono para no verse deslavado; si ya está al 100 %, se rota el tono (M6). Los grises pueden saturarse de azul (fríos) o de amarillo o naranja (cálidos), también más en sus extremos.
Por qué, según el autor: en HSL (C2) la saturación pierde efecto cerca del negro y del blanco.
Base: razonamiento de los autores.

### P21 · Accesible no es feo, y el color nunca va solo (accessible doesn't have to mean ugly; don't rely on color alone) — [REFACTORING-UI], cap. 5
Afirma: las Pautas de Accesibilidad para el Contenido Web (WCAG) piden 4,5:1 para texto normal, que el libro sitúa por debajo de unos 18 px, y 3:1 para el grande (ver N1). Se cumple invirtiendo el contraste o rotando el tono, y el color no debe comunicar solo.
Por qué, según el autor: con texto blanco el fondo debe ser tan oscuro que acapara la atención; texto oscuro sobre fondo de color claro lo evita. Rotar hacia cian, magenta o amarillo (C3) sube el contraste sin acercarse al blanco. Para el daltonismo rojo-verde, iconos en las métricas y gráficos diferenciados por claro y oscuro (ver N7).
Base: WCAG y razonamiento de los autores.

### P22 · Emular una fuente de luz (emulate a light source) — [REFACTORING-UI], cap. 6
Afirma: para que algo parezca elevado o hundido se imita luz que viene de arriba según su perfil (M7).
Por qué, según el autor: un panel de puerta en relieve tiene el borde superior claro y el inferior oscuro; uno hundido, sombra arriba y borde inferior claro. Como miramos la pantalla algo desde arriba, en lo elevado se ve el borde superior.
Base: observación de objetos reales.
Matices: no buscar el fotorrealismo, que recarga y confunde.

### P23 · Las sombras transmiten elevación (use shadows to convey elevation) — [REFACTORING-UI], cap. 6
Afirma: las sombras sitúan los elementos en un eje z virtual (C4): pequeñas para botones, medianas para menús desplegables, grandes para ventanas modales; lo más cercano atrae más atención.
Por qué, según el autor: también comunican interacción: el elemento que se arrastra gana sombra y un botón pulsado la pierde.
Base: experiencia de los autores.
Matices: se elige la altura deseada y se aplica la sombra del sistema (M8).

### P24 · Profundidad en diseño plano y por superposición (even flat designs can have depth; overlap elements) — [REFACTORING-UI], cap. 6
Afirma: lo más claro que el fondo parece elevado y lo más oscuro, hundido; las sombras sólidas cortas sin desenfoque separan sin romper la estética plana; superponer (una tarjeta que cruza dos fondos) crea capas.
Por qué, según el autor: lo claro parece más cercano y lo oscuro más lejano.
Base: experiencia de los autores.
Matices: las imágenes superpuestas llevan un «borde invisible» del color del fondo.

### P25 · Usar buenas fotografías (use good photos) — [REFACTORING-UI], cap. 7
Afirma: las malas fotos arruinan un buen diseño: o se contrata a un profesional o se usan bancos de calidad, incluso gratuitos como Unsplash.
Por qué, según el autor: una buena foto depende de luz, composición y color, no de la cámara.
Base: experiencia de los autores.
Matices: nunca diseñar con imágenes provisionales para sustituirlas por fotos del móvil.

### P26 · Todo tiene un tamaño previsto (everything has an intended size) — [REFACTORING-UI], cap. 7
Afirma: iconos, capturas y logotipos se usan al tamaño para el que se dibujaron.
Por qué, según el autor: iconos de 16-24 px ampliados tres o cuatro veces parecen toscos aunque sean vectoriales (mejor dentro de una forma con fondo); una captura muy reducida es ilegible (E6), así que se captura a tamaño de tableta, se recorta o se simplifica; un logotipo reducido a icono de pestaña (favicon) de 16 px se emborrona y hay que redibujarlo.
Base: experiencia de los autores.

### P27 · Cuidado con las imágenes de los usuarios (beware user-uploaded content) — [REFACTORING-UI], cap. 7
Afirma: se centran en contenedores fijos recortando lo que sobre (background-size: cover) y, si su fondo se confunde con el de la interfaz, se les da una sombra interior sutil o un borde interior semitransparente, no un borde normal, que choca con sus colores.
Por qué, según el autor: con su proporción original descolocan la composición.
Base: experiencia de los autores.

### P28 · Realzar lo existente con color y fondos (supercharge the defaults; accent borders; decorate your backgrounds) — [REFACTORING-UI], cap. 8
Afirma: un diseño correcto pero soso mejora con iconos en vez de viñetas, comillas grandes de color, subrayados gruesos, casillas con el color de marca, bordes de acento (en tarjetas, navegación activa, avisos o bajo titulares) y fondos de color, degradados ligeros, motivos repetidos (ver N2) o formas sueltas.
Por qué, según el autor: un rectángulo de color no exige talento gráfico.
Base: experiencia de los autores.
Matices: degradados con tonos separados como mucho unos 30°; motivos de poco contraste.

### P29 · No descuidar los estados vacíos (don't overlook empty states) — [REFACTORING-UI], cap. 8
Afirma: si una función depende de contenido del usuario, la pantalla sin datos (empty state) es prioritaria: ilustración, llamada a la acción destacada y sin filtros que aún no sirven.
Por qué, según el autor: es la primera interacción con la función, y suele olvidarse (E7).
Base: experiencia de los autores.

### P30 · Menos bordes y componentes menos convencionales (use fewer borders; think outside the box) — [REFACTORING-UI], cap. 8
Afirma: para separar, antes que un borde: una sombra, fondos ligeramente distintos o más espacio; y los componentes no tienen por qué verse como dicta la costumbre (E8).
Por qué, según el autor: demasiados bordes recargan y las ideas preconcebidas limitan.
Base: experiencia de los autores.

## [REFACTORING-UI] Conceptos y mecanismos

### C1 · Jerarquía visual (visual hierarchy) — [REFACTORING-UI], cap. 2
Qué es: la importancia aparente de cada elemento respecto a los demás.
Cómo funciona, según el autor: se destaca lo principal y se rebaja lo demás con tamaño, peso, color, contraste y espacio (P5-P11).

### C2 · Color en HSL (hue, saturation, lightness) — [REFACTORING-UI], cap. 5
Qué es: notación del color por atributos que el ojo percibe, más intuitiva que el hexadecimal (hex) o RGB.
Cómo funciona, según el autor: el tono es la posición en la rueda (0° rojo, 120° verde, 240° azul); la saturación, la viveza (0 % es gris); la luminosidad, la cercanía al negro (0 %) o al blanco (100 %), con el color puro al 50 %. En HSB, en cambio, el 100 % de brillo con saturación plena equivale al 50 % de luminosidad HSL; los navegadores usan HSL (ver N4).

### C3 · Brillo percibido (perceived brightness) — [REFACTORING-UI], cap. 5
Qué es: el brillo propio de cada tono: amarillo y azul con igual luminosidad HSL no parecen igual de claros.
Cómo funciona, según el autor: se calcula con una fórmula sobre RGB que no viene en el texto (ver N4); tiene mínimos en rojo, verde y azul y máximos en amarillo, cian y magenta, lo que permite aclarar u oscurecer rotando el tono (M6).

### C4 · Eje z y sombra en dos partes (z-axis; shadows can have two parts) — [REFACTORING-UI], cap. 6
Qué es: el eje z es la profundidad virtual de la interfaz; las buenas sombras combinan dos.
Cómo funciona, según el autor: una grande y suave, con desplazamiento y mucho desenfoque, imita la luz directa; otra ceñida y oscura imita la zona bajo el objeto sin luz ambiental, y debe ser nítida en la elevación más baja y casi invisible en la más alta.

### C5 · Línea base y altura x (baseline, x-height) — [REFACTORING-UI], cap. 4
Qué es: la línea base es donde se apoyan las letras; la altura x, la de las minúsculas sin trazos que sobresalen hacia arriba (b, f) o hacia abajo (g, p).
Cómo funciona, según el autor: esa variedad ayuda a distinguir minúsculas y falta en mayúsculas (P18); las fuentes de titulares tienen altura x baja y espaciado apretado, y las de texto pequeño, lo contrario (M4).

### C6 · Escala modular (modular scale) — [REFACTORING-UI], cap. 4
Qué es: escala tipográfica que aplica una razón repetidamente a una base, como 4:5 («tercera mayor»), 2:3 («quinta justa») o 1:1,618.
Cómo funciona, según el autor: da valores fraccionarios (base 16 y 4:5: 31,25; 39,063; 48,828 px) que cada navegador redondea distinto y saltos excesivos para interfaces (3:4 redondeada: 12, 16, 21, 28 px); sirve en textos largos redondeando, pero en interfaces es mejor una escala a mano (M3).

## [REFACTORING-UI] Métodos y protocolos

### M1 · Diseñar por eliminación (designing by process of elimination) — [REFACTORING-UI], cap. 1
Objetivo: elegir rápido dentro de un sistema.
Pasos: 1) usa una escala de valores claramente distintos (iconos de 12, 16, 24 y 32 px); 2) prueba el que creas mejor (16); 3) compáralo con sus vecinos (12 y 24); 4) si estos se ven peor, quédate el central; 5) si gana un vecino, repite tomándolo como centro.

### M2 · Escala de espaciado y tamaños (spacing and sizing system) — [REFACTORING-UI], cap. 3
Objetivo: dejar de dudar entre 120 y 125 px.
Pasos: 1) descarta escalas lineales como «múltiplos de 4 px»; 2) parte de 16 px, que se divide bien y es la letra por defecto de los navegadores; 3) construye factores y múltiplos, juntos abajo y cada vez más separados arriba; 4) que dos valores contiguos nunca difieran menos de un 25 %; 5) prueba un valor y, si no basta, el siguiente.
Base: de 12 a 16 px hay un 33 %; de 500 a 520 px, un 4 %. La escala de ejemplo no viene en el texto (ver N6).

### M3 · Escala tipográfica hecha a mano (hand-crafted type scale) — [REFACTORING-UI], cap. 4
Objetivo: evitar usar cualquier tamaño de 10 a 24 px.
Pasos: 1) saltos pequeños abajo y grandes arriba; 2) valores elegidos a mano, no por razón matemática (C6); 3) coherentes con la escala de espaciado (M2); 4) en px o rem, nunca en em.
Base: con em, lo anidado se sale de la escala: 0,875em dentro de 1,25em (20 px) da 17,5 px. La escala de ejemplo no viene en el texto (ver N6).

### M4 · Elegir tipografía (use good fonts) — [REFACTORING-UI], cap. 4
Objetivo: escoger fuentes de calidad sin experiencia.
Pasos: 1) para interfaz, una sin remates neutra (tipo Helvetica) o la pila del sistema: -apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue; 2) descarta familias de menos de cinco pesos; en Google Fonts, filtra por 10 o más estilos (ver N5); 3) evita para texto principal fuentes estrechas de altura x baja (C5); 4) ordena por popularidad, útil para una serif con personalidad; 5) mira qué usan las webs que admiras.

### M5 · Tonos definidos de antemano (define your shades up front) — [REFACTORING-UI], cap. 5
Objetivo: una escala fija por color, en vez de funciones como «lighten» o «darken», que acaban dando 35 azules casi iguales.
Pasos: 1) elige a ojo el base, que en primarios y acentos debe servir de fondo de botón; 2) elige el más oscuro (texto) y el más claro (fondos tintados), probándolos por ejemplo en un aviso; 3) numera 900 el oscuro, 500 el base y 100 el claro; 4) elige 700 y 300 como compromiso entre vecinos; 5) rellena 800, 600, 400 y 200 igual.
Frecuencia: al menos 5 tonos, mejor cerca de 10. En grises, el más oscuro es el del texto y el más claro, un blanco roto para fondos.
Matices: se retoca a ojo, sin añadir tonos a menudo.

### M6 · Aclarar u oscurecer rotando el tono (changing brightness by rotating hue) — [REFACTORING-UI], cap. 5
Objetivo: cambiar el brillo sin perder intensidad.
Pasos: 1) para aclarar, rota hacia el más cercano de 60°, 180° o 300°; 2) para oscurecer, hacia 0°, 120° o 240°; 3) combínalo con la luminosidad; 4) no pases de 20-30°.
Base: brillo percibido (C3); una paleta amarilla que vira al naranja al oscurecer no se vuelve marrón.

### M7 · Luz en elementos elevados y hundidos (simulating light) — [REFACTORING-UI], cap. 6
Objetivo: que un botón parezca elevado o un pozo (well) hundido.
Pasos para elevado: 1) borde superior algo más claro, con borde o sombra interior (inset) de leve desplazamiento, en un color elegido a mano y no con blanco translúcido; 2) debajo, sombra oscura pequeña con leve desplazamiento y un par de píxeles de desenfoque.
Pasos para hundido: 1) borde inferior más claro; 2) arriba, sombra interior oscura pequeña. Vale para campos y casillas.

### M8 · Sistema de elevación (establishing an elevation system) — [REFACTORING-UI], cap. 6
Objetivo: un juego fijo de unas cinco sombras.
Pasos: 1) define la más pequeña y la más grande; 2) rellena el medio con aumentos bastante lineales; 3) asigna según la altura deseada (P23). Los valores de ejemplo no vienen en el texto (ver N6).

### M9 · Texto legible sobre una imagen (text needs consistent contrast) — [REFACTORING-UI], cap. 7
Objetivo: igualar las zonas claras y oscuras de una foto para que el texto se lea entero.
Pasos (combinables): 1) superposición semitransparente, negra para texto claro o blanca para oscuro; 2) bajar el contraste de la imagen, compensando el brillo; 3) colorearla: bajar contraste, desaturar y añadir un relleno sólido en modo «multiplicar» (multiply); 4) sombra de texto muy desenfocada y sin desplazamiento.

### M10 · Diseñar primero en pequeño (shrink the canvas) — [REFACTORING-UI], cap. 3
Objetivo: diseñar con restricciones reales.
Pasos: 1) en una web adaptable (responsive), empieza con un lienzo de unos 400 px; 2) llévalo a pantallas mayores; 3) ajusta lo que fue un compromiso, que según los autores será poco.

### M11 · Seguir mejorando (leveling up) — [REFACTORING-UI], cap. 9
Objetivo: seguir aprendiendo.
Pasos: 1) ante un buen diseño, busca decisiones que no habrías tomado (E9); 2) reconstruye tus interfaces favoritas sin mirar las herramientas de desarrollador; 3) al comparar descubrirás trucos como reducir el interlineado de titulares o combinar sombras.

## [REFACTORING-UI] Ejemplos y casos
E1 · Buscador de vuelos: el diseño empieza por los campos de origen, destino, fechas y el botón de buscar; ilustra P1 (cap. 1).
E2 · Comentarios con adjuntos: los adjuntos cuestan mucho más de lo previsto y todo el sistema queda aparcado, aunque sin ellos ya era útil; ilustra P2 (cap. 1).
E3 · Botones con fondos casi indistinguibles: sin sistema no hay forma de decidir; ilustra P4 (cap. 1).
E4 · Tarjeta de acceso a 6 columnas en pantalla grande y 8 en mediana, que en ciertas medianas resulta más ancha que en grandes; ilustra P13 (cap. 3).
E5 · Formulario estrecho cuyo texto de apoyo pasa a una columna aparte; ilustra P13 (cap. 3).
E6 · Captura reducida un 70 %: la letra de 16 px queda en 4 px y obliga a mirar a unos 5 cm (dos pulgadas) de la pantalla; ilustra P26 (cap. 7).
E7 · Función nueva diseñada con datos de muestra perfectos que el usuario estrena vacía; ilustra P29 (cap. 8).
E8 · Menú desplegable con secciones, columnas e iconos; tabla con columnas fusionadas e imágenes; botones de opción convertidos en tarjetas seleccionables; ilustra P30 (cap. 8).
E9 · Selector de fechas con fondo invertido, botón dentro de un campo de texto y titular en dos colores; ilustra M11 (cap. 9).

## [REFACTORING-UI] Errores frecuentes y advertencias
- Empezar por la navegación, fijar detalles pronto o diseñarlo todo antes de programar (cap. 1).
- Mezclar esquinas rectas y redondeadas; copiar a la competencia directa (cap. 1).
- Elegir valores píxel a píxel sin sistema (caps. 1, 3 y 4).
- Jerarquizar solo con tamaño; texto gris o blanco translúcido sobre color; «etiqueta: valor» por defecto (cap. 2).
- Añadir espacio hasta que «no se vea mal»; mismo espacio dentro y entre grupos (cap. 3).
- Escalas en em; líneas demasiado largas; centrar párrafos largos (cap. 4).
- Paletas de cinco colores, negro puro, tonos con «lighten», comunicar solo con color (cap. 5).
- Perseguir el fotorrealismo; imágenes provisionales; ampliar iconos o reducir capturas (caps. 6 y 7).
- Dejar el estado vacío para el final; abusar de los bordes (cap. 8).

## [REFACTORING-UI] Ejercicios y acciones
- Bocetar con rotulador grueso y diseñar en grises antes del color (cap. 1).
- Revisar las webs del público objetivo para decidir la personalidad (cap. 1).
- Empezar con un lienzo de unos 400 px (M10, cap. 3).
- Inspeccionar las fuentes de las webs que se admiran (cap. 4).
- Levantar un objeto de la mesa para ver desaparecer su sombra de luz ambiental (cap. 6).
- Reconstruir interfaces admiradas sin herramientas de desarrollador (M11, cap. 9).

## [REFACTORING-UI] Cifras y reglas concretas
- R1 · 8 a 10 tonos predefinidos por color (cap. 1).
- R2 · Texto: 2 o 3 colores; pesos 400-500 normal y 600-700 énfasis; menos de 400 solo en titulares grandes (cap. 2).
- R3 · Espaciado: base 16 px, valores contiguos separados al menos un 25 % (cap. 3).
- R4 · Lienzos de 1.200-1.400 px; móvil inicial de unos 400 px (cap. 3).
- R5 · Rejilla de 12 columnas: 8,33 % cada una (cap. 3).
- R6 · Botón de ejemplo: letra de 16 px, relleno de 16 px horizontal y 12 px vertical (cap. 3).
- R7 · Titular en móvil de 20-24 px con cuerpo de 14 px; 45 px con cuerpo de 18 px en escritorio (cap. 3).
- R8 · Línea de 45 a 75 caracteres, unos 20-35em (cap. 4).
- R9 · Escalas modulares: 4:5, 2:3 y 1:1,618 (cap. 4).
- R10 · Interlineado: 1,5 en texto estrecho, hasta 2 en ancho, 1 en titulares grandes (cap. 4).
- R11 · Sistemas que fijar: tamaño y peso de letra, interlineado, color, margen, relleno, ancho, alto, sombras, radio de esquina, grosor de borde y opacidad (cap. 1).
- R12 · Google Fonts con 10 o más estilos: fuera el 85 %, quedan menos de 50 sin remates (cap. 4, ver N5).
- R13 · Tonos brillantes a 60°, 180° y 300°; oscuros a 0°, 120° y 240°; rotación máxima de 20-30° (cap. 5).
- R14 · Hasta 10 colores con 5 a 10 tonos; escala 100-900 con base en 500 (cap. 5).
- R15 · WCAG: 4,5:1 texto normal y 3:1 grande (cap. 5, ver N1).
- R16 · Unas 5 sombras de elevación (cap. 6).
- R17 · Iconos de 16-24 px, no ampliarlos 3 o 4 veces; favicon de 16 px (cap. 7).
- R18 · Degradados con tonos separados como mucho unos 30° (cap. 8).

## [REFACTORING-UI] Preguntas que este libro responde
- ¿Por dónde empiezo a diseñar una aplicación? Según Wathan y Schoger en REFACTORING-UI, por una funcionalidad concreta, en baja fidelidad y sin color, construyéndola pronto (P1, P2, cap. 1).
- ¿Cómo hago que mi web parezca seria o cercana? Según Wathan y Schoger en REFACTORING-UI, con tipografía, color, radio de esquinas y tono de los textos coherentes (P3, cap. 1).
- ¿Cómo dejo de dudar entre 12 y 13 px? Según Wathan y Schoger en REFACTORING-UI, con escalas cerradas y eligiendo por eliminación entre vecinos (P4, M1-M3, caps. 1, 3 y 4).
- Mi interfaz parece desordenada, ¿qué falla? Según Wathan y Schoger en REFACTORING-UI, la jerarquía: destacar lo principal con peso y color y debilitar lo demás (P5, P7, cap. 2).
- ¿Qué color lleva un texto secundario sobre fondo azul? Según Wathan y Schoger en REFACTORING-UI, uno del mismo tono del fondo elegido a mano, no gris (P6, cap. 2).
- ¿Cómo muestro datos sin «Nombre:», «Teléfono:»…? Según Wathan y Schoger en REFACTORING-UI, quitando etiquetas cuando el formato o el contexto bastan, o fusionándolas con el valor (P8, cap. 2).
- ¿Cómo debe ser el botón de borrar? Según Wathan y Schoger en REFACTORING-UI, discreto si no es la acción principal, y rojo y destacado en la confirmación (P11, cap. 2).
- ¿Cuánto espacio dejo entre elementos? Según Wathan y Schoger en REFACTORING-UI, empezar con demasiado y quitar, con más espacio entre grupos que dentro (P12, P15, M2, cap. 3).
- ¿Ajusto todo a una rejilla de 12 columnas? Según Wathan y Schoger en REFACTORING-UI, no: barras laterales y tarjetas van mejor con ancho fijo o máximo (P13, cap. 3).
- ¿Qué fuente y qué ancho de párrafo uso? Según Wathan y Schoger en REFACTORING-UI, una sin remates neutra o la del sistema con cinco pesos o más, y 45 a 75 caracteres por línea (M4, P16, cap. 4).
- ¿Cuántos colores necesito y cómo hago los tonos? Según Wathan y Schoger en REFACTORING-UI, grises, primarios y acentos con 5 a 10 tonos en una escala 100-900 hecha a mano (P19, M5, cap. 5).
- ¿Por qué mis tonos claros se ven apagados? Según Wathan y Schoger en REFACTORING-UI, porque la saturación pierde efecto lejos del 50 % de luminosidad: hay que subirla o rotar el tono (P20, M6, cap. 5).
- ¿Cómo cumplo el contraste accesible sin oscurecerlo todo? Según Wathan y Schoger en REFACTORING-UI, con texto oscuro sobre fondo claro o rotando el tono hacia colores brillantes (P21, cap. 5).
- ¿Cómo hago un botón en relieve y qué sombra lleva una ventana modal? Según Wathan y Schoger en REFACTORING-UI, borde superior más claro y sombra nítida debajo; y la mayor de un sistema de cinco sombras (P22, P23, M7, M8, cap. 6).
- ¿Cómo hago legible un titular sobre una foto? Según Wathan y Schoger en REFACTORING-UI, con superposición, menos contraste, coloreando la imagen o con sombra de texto difusa (M9, cap. 7).
- Mi diseño es correcto pero soso, ¿qué hago? Según Wathan y Schoger en REFACTORING-UI, bordes de acento, fondos decorados, iconos en listas, un buen estado vacío y menos bordes (P28-P30, cap. 8).

## [REFACTORING-UI] Glosario
- Armazón (shell): navegación, cabecera, logotipo y contenedor de una aplicación.
- Peso (font weight): grosor de la letra; 400 normal, 700 negrita.
- Contraste: diferencia de luminosidad entre un elemento y su fondo, que WCAG expresa como razón (4,5:1).
- Relleno (padding) y margen (margin): espacio interior de un elemento y espacio entre elementos.
- Rejilla (grid): división del ancho en columnas para colocar elementos.
- Ancho máximo (max-width): anchura a partir de la cual un elemento deja de crecer.
- Diseño adaptable (responsive): diseño que se ajusta al tamaño de pantalla.
- px, em, rem: píxel; unidad relativa a la letra del elemento padre; relativa a la letra raíz del documento.
- Con y sin remates (serif, sans serif): letras con o sin pequeños trazos terminales.
- Interlineado (line-height): altura de cada línea respecto al tamaño de letra.
- Pila de fuentes del sistema (system font stack): lista de fuentes nativas de cada sistema operativo.
- Colores de acento (accent colors): colores para destacar novedades y estados.
- WCAG: Pautas de Accesibilidad para el Contenido Web, del consorcio W3C.
- Sombra (box shadow) e interior (inset shadow): sombra proyectada por un elemento o dentro de él.
- Diseño plano (flat design): estilo sin sombras, degradados ni imitación de luz.

## [REFACTORING-UI] Específico de otro país
No aplica. Solo algunos ejemplos de P8 (cap. 2) usan formatos estadounidenses de teléfono y precio; la idea de que el formato revela el dato debe probarse con formatos españoles.

## [REFACTORING-UI] Notas de Claude

### N1 · Umbral de texto grande y obligación legal en España — [REFACTORING-UI], sobre P21, cap. 5
Qué dice el libro: el texto normal, por debajo de unos 18 px, necesita contraste 4,5:1, y el grande, 3:1.
Qué se sabe hoy: WCAG llama grande al texto de al menos 18 puntos (unos 24 px) o 14 puntos en negrita (unos 18,5 px), así que un texto normal de 18 a 23 px sigue necesitando 4,5:1. En España, la Ley 11/2023, de 8 de mayo, que transpone la Directiva (UE) 2019/882, exige accesibilidad desde el 28 de junio de 2025 a servicios como el comercio electrónico y las webs y aplicaciones de banca o transporte. Según conocimiento general de Claude, sin comprobar, su norma técnica (EN 301 549) remite a WCAG 2.1 AA, y el sector público se rige por el Real Decreto 1112/2018.
Fuente: W3C, «Understanding Success Criterion 1.4.3», w3.org, consultada el 21-10-2026; RSM, alerta sobre la Ley de Accesibilidad, rsm.global, consultada el 21-10-2026.

### N2 · Año, autores e intereses — [REFACTORING-UI], sobre la Ficha y P28, cap. 8
Qué dice el libro: no da año ni biografía; enlaza Hero Patterns para motivos de fondo.
Qué se sabe hoy: en el episodio 103 de Full Stack Radio, pódcast de Wathan, del 5 de diciembre de 2018, ambos presentaban el libro como inminente. Según conocimiento general de Claude, sin comprobar, Wathan creó Tailwind CSS, Schoger hizo Hero Patterns (gratuito) y las escalas del libro se parecen a las de Tailwind; no es un conflicto grave.
Fuente: Full Stack Radio, episodio 103, fullstackradio.com, consultada el 21-10-2026; lo demás, conocimiento general de Claude, sin comprobar.

### N3 · La regla de 45 a 75 caracteres — [REFACTORING-UI], sobre P16, cap. 4
Qué dice el libro: recomienda 45 a 75 caracteres por línea sin citar fuente.
Qué se sabe hoy: es una regla tipográfica tradicional. Los estudios en pantalla son mixtos: las líneas largas se leen algo más rápido, aunque se prefieren cortas, como recoge Weinschenk ([100-THINGS-DESIGNER], M2, cap. 18): unos 100 caracteres para velocidad y 45-72 por preferencia. Es una opción segura, no un límite demostrado.
Fuente: resumen de la biblioteca de 100 Things Every Designer Needs to Know About People; lo demás, conocimiento general de Claude, sin comprobar.

### N4 · HSL, brillo percibido y espacios de color modernos — [REFACTORING-UI], sobre C2, C3 y M6, cap. 5
Qué dice el libro: los navegadores solo entienden HSL; la fórmula del brillo percibido va en una figura no incluida.
Qué se sabe hoy: CSS Color de nivel 4, ya admitido por los navegadores principales, añade lab(), lch() y oklch(); OKLCH tiene una luminosidad cercana a la percibida, lo que reduce el problema que el libro resuelve rotando el tono. Una fórmula de brillo percibido muy difundida es la raíz cuadrada de (0,299 R² + 0,587 G² + 0,114 B²), pero no puede confirmarse que sea la del libro.
Fuente: conocimiento general de Claude, sin comprobar.

### N5 · Datos técnicos envejecidos u omitidos — [REFACTORING-UI], sobre M4, R12 y P18, cap. 4
Qué dice el libro: filtrar Google Fonts por 10 o más estilos elimina el 85 %; alinear números a la derecha; justificar con división silábica.
Qué se sabe hoy: Google Fonts ha cambiado y muchas familias son variables (pesos continuos), así que la cifra puede no coincidir; CSS ofrece hoy system-ui para la fuente del sistema. Los decimales solo cuadran con cifras de ancho fijo (font-variant-numeric: tabular-nums), y la división automática (hyphens: auto) exige declarar el idioma, por ejemplo lang="es".
Fuente: conocimiento general de Claude, sin comprobar.

### N6 · Figuras que faltan — [REFACTORING-UI], sobre M2, M3, M8 y C3, caps. 3 a 6
Qué dice el libro: muchas reglas se apoyan en figuras: la escala de espaciado (cap. 3), la tipográfica (cap. 4), la fórmula y gráfica del brillo percibido (cap. 5) y las cinco sombras (cap. 6).
Qué se sabe hoy: no vienen en el archivo, así que el resumen no da esos valores y Claude no debe reconstruirlos.
Fuente: comprobación del archivo recibido.

### N7 · Daltonismo — [REFACTORING-UI], sobre P21, cap. 5
Qué dice el libro: no comunicar solo con color por quienes no distinguen rojo y verde; no da cifras.
Qué se sabe hoy: la deficiencia rojo-verde afecta a cerca del 8 % de los hombres y del 0,5 % de las mujeres de ascendencia norte-europea, y WCAG la cubre en su criterio 1.4.1 (uso del color).
Fuente: conocimiento general de Claude, sin comprobar.
