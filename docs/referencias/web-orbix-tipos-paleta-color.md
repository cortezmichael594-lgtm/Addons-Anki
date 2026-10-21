# [W-ORBIX-PALETAS] Resumen de artículo web — Los 6 tipos de paleta de color en diseño de interfaces (Shohanur Rahman, Orbix Studio, 2026)

## [W-ORBIX-PALETAS] Ficha
- Título: 6 Color Palette Types in UI Design: Examples, Rules & How to Choose (Los 6 tipos de paleta de color en diseño de interfaces: ejemplos, reglas y cómo elegir).
- Autor: Shohanur Rahman, fundador y director general de Orbix Studio (tomado de la página; el texto pegado no lo firma). No alega otra experiencia ni consta quién lo revisó.
- Sitio y enlace: Orbix Studio, https://www.orbix.studio/blogs/color-palette-types-ui-design
- Fechas: publicación no indicada; última actualización el 23 de septiembre de 2026 (tomada de la página).
- Idioma: inglés.
- Tipo: guía práctica.
- Intereses: Orbix Studio vende servicios de diseño de interfaces y experiencia de usuario (UI/UX) para empresas de software como servicio (SaaS) y ofrece una llamada gratuita de 30 minutos; el artículo presenta su trabajo a medida como lo que distingue una paleta sólida de una plantilla.
- Fiabilidad: media. Lo central (tipos de armonía, WCAG 2.2, no depender solo del color, #121212) coincide con lo establecido, pero varios datos y ejemplos son erróneos o se contradicen (ver N1, N2, N3) y hay interés comercial. Valoración de Claude.
- Texto usado: completo (unas 2.300 palabras estimadas, texto pegado), incluidas las preguntas frecuentes, que sí traen respuesta. Autor y fecha, de la página. Se descartaron la llamada a reservar una cita y los enlaces a otros artículos del sitio.
- A quién sirve: a quien elija o revise los colores de una aplicación o web, sobre todo paneles de software, aunque no sea diseñador.
- Tesis: según Rahman, el tipo de paleta (la relación entre tonos en la rueda de color) se decide antes que los colores concretos, porque fija el contraste, el tono emocional y cuántos estados interactivos se pueden expresar; luego se reparte con la regla 60-30-10 y se comprueba accesibilidad y modo oscuro.
- Temas: diseño y experiencia de usuario, toma de decisiones.
- Ideas esenciales:
  - P1 · Elegir el tipo de paleta antes que los colores (ap. 2 y 11).
  - C2 · Los seis tipos: monocromático, análogo, complementario, complementario dividido, triádico y tetrádico (ap. 3).
  - P2 · Comprobar el contraste WCAG 2.2: 4,5:1 texto normal, 3:1 texto grande y componentes (ap. 4).
  - P3 · Colores semánticos (error, éxito, aviso) separados de los de marca (ap. 4.3).
  - M1 · Regla 60-30-10 de proporción (ap. 5).
  - M2 · Elegir el tipo con cuatro factores: tono emocional, contraste, estados interactivos y modo oscuro (ap. 6).
  - M3 · Ajustes de modo oscuro: menos saturación, gris #121212-#1E1E1E en vez de negro, semánticos propios (ap. 7).
  - P4 · No usar el color como única señal (ap. 8.1).
  - P5 · Tener una escala de neutros (ap. 8.2).
  - P6 · No trasladar la paleta de marca tal cual al producto (ap. 8.3).
- Mapa:
  - ap. 1 · Resumen rápido e introducción (Quick Summary): Spotify, Stripe y Linear como ejemplos.
  - ap. 2 · Qué es una paleta de color en interfaces (What is a color palette in UI design?).
  - ap. 3 · Los 6 tipos de paleta (The 6 types of color palettes): 3.1 monocromática; 3.2 análoga; 3.3 complementaria; 3.4 complementaria dividida; 3.5 triádica; 3.6 tetrádica o cuadrada.
  - ap. 4 · Cómo afecta cada tipo a la accesibilidad (How each palette type affects accessibility): 4.1 monocromática y análoga; 4.2 complementaria y vibración; 4.3 colores semánticos.
  - ap. 5 · La regla 60-30-10 (The 60-30-10 rule): 5.1 dominante; 5.2 secundario; 5.3 acento.
  - ap. 6 · Cómo elegir la paleta (How to choose the right color palette): emoción, estados, color de marca, modo oscuro.
  - ap. 7 · Modo oscuro (Dark mode and what actually changes).
  - ap. 8 · Errores que restan credibilidad (Color palette mistakes): 8.1 color como única señal; 8.2 sin escala de neutros; 8.3 paleta de marca directa; 8.4 daltonismo.
  - ap. 9 · Herramientas (Tools to build and test).
  - ap. 10 · Preguntas frecuentes (Frequently asked questions).
  - ap. 11 · Conclusión.

## [W-ORBIX-PALETAS] Principios y recomendaciones
### P1 · El tipo de paleta antes que los colores — [W-ORBIX-PALETAS], ap. 2 y 11
Afirma: Rahman sostiene que primero se fija la relación entre tonos (esquema, scheme) y luego los tonos (paleta, palette), porque el tipo fija contraste, emoción y estados posibles.
Base: experiencia del sitio, sin fuente concreta.

### P2 · Contraste mínimo WCAG 2.2 — [W-ORBIX-PALETAS], ap. 4 y 10
Afirma: Rahman exige comprobar cada par texto-fondo con WCAG 2.2 nivel AA: 4,5:1 texto normal; 3:1 texto grande y componentes.
Base: WCAG 2.2 del W3C (https://www.w3.org/TR/WCAG22/).
Matices: según Rahman, las complementarias traen alto contraste de serie (ver N2).

### P3 · Semánticos separados de la marca — [W-ORBIX-PALETAS], ap. 4.3
Afirma: Rahman pide que error, éxito y aviso no coincidan con los colores de marca: si la marca es roja, el error no se distingue.
Base: ninguna explícita.

### P4 · El color nunca como única señal — [W-ORBIX-PALETAS], ap. 8.1 y 8.4
Afirma: Rahman pide acompañar cada señal de color con icono, texto o borde y probar la paleta en un simulador de daltonismo antes de desarrollo, porque rojo-verde falla con deuteranopía.
Base: prevalencia del 8 % de hombres y 0,5 % de mujeres, sin fuente concreta (ver N5).

### P5 · Escala de neutros — [W-ORBIX-PALETAS], ap. 8.2
Afirma: Rahman considera imprescindible una escala de blanco a casi negro para fondos, texto y bordes; sin ella todo acaba teñido de marca.
Base: Figma usaría 10 pasos de neutros (no comprobado).

### P6 · Adaptar la paleta de marca al producto — [W-ORBIX-PALETAS], ap. 6 y 8.3
Afirma: Rahman, por las auditorías de Orbix Studio, sostiene que la paleta publicitaria copiada tal cual da botones estridentes, texto ilegible y estados que chocan; el producto necesita tintes, sombras y semánticos.
Base: experiencia del sitio.

## [W-ORBIX-PALETAS] Conceptos y mecanismos
### C1 · Partes de una paleta de interfaz — [W-ORBIX-PALETAS], ap. 2 y 10
Qué es: según Rahman, primarios (marca), secundarios, neutros (fondos, texto, bordes) y semánticos (éxito, aviso, error, información): 1-2 primarios, 1 acento, 6-10 neutros y 4 semánticos, con 2-3 tonos activos a la vez como mucho.

### C2 · Los seis tipos de paleta — [W-ORBIX-PALETAS], ap. 3
Qué es: relaciones entre tonos (hues) en la rueda de color, según Rahman:
- Monocromática (monochromatic), ap. 3.1: un tono en varias luminosidades; serena y fácil de hacer accesible; para paneles densos. Notion, Linear.
- Análoga (analogous), ap. 3.2: tres tonos vecinos; armoniosa, poco contraste, necesita neutro o acento. Slack (ver N3).
- Complementaria (complementary), ap. 3.3: dos opuestos (azul y naranja); foco fuerte, ruido si abunda; para que domine una acción. Stripe.
- Complementaria dividida (split-complementary), ap. 3.4: base más los dos vecinos de su opuesto; contraste con menos tensión; apps creativas y de público joven.
- Triádica (triadic), ap. 3.5: tres equidistantes; vibrante; un tono dominante y dos de acento. Google (ver N3).
- Tetrádica o cuadrada (tetradic, square), ap. 3.6: dos pares complementarios; máximo rango, caótica sin neutros. Google, Microsoft.

### C3 · Vibración visual (visual vibration) — [W-ORBIX-PALETAS], ap. 4.2
Qué es: según Rahman, el parpadeo de dos complementarios saturados juntos, como rojo sobre verde, «técnicamente de alto contraste» pero ilegible (ver N2). Remedio: desaturar uno un 20-30 % o usarlo solo como acento pequeño.

## [W-ORBIX-PALETAS] Métodos y protocolos
### M1 · Regla 60-30-10 (60-30-10 rule) — [W-ORBIX-PALETAS], ap. 5 y 10
Pasos: 1) 60 % dominante en fondos: blanco roto o gris muy claro; en oscuro, #121212-#1E1E1E. 2) 30 % secundario en tarjetas, barras laterales y paneles, a 10-15 puntos de luminosidad HSL del dominante. 3) 10 % acento solo en llamadas a la acción, estados activos y enlaces, para que signifique «algo que puedo hacer» (caso Stripe).
Ejemplos: monocromática 60 % claro, 30 % medio, 10 % oscuro; complementaria 60 % dominante «normalmente neutro», 30 % secundario, 10 % complementario.

### M2 · Elegir el tipo con cuatro factores — [W-ORBIX-PALETAS], ap. 6 y 10
Pasos, según Rahman: 1) Emoción: salud, finanzas y productividad, monocromática o análoga; juegos, redes y creatividad, complementaria o triádica. 2) Contar estados (por defecto, al pasar el ratón, activo, desactivado, error): la triádica confunde si sus tres tonos coinciden en un componente. 3) Partir del color de marca: naranja intenso, complementaria o dividida; verde bosque, análoga o complementaria. 4) Probar claro y oscuro durante la elección.
Matices: en paneles de datos, monocromática o análoga, con acentos complementarios solo en llamadas principales y alertas.

### M3 · Ajustes de modo oscuro — [W-ORBIX-PALETAS], ap. 7
Pasos, según Rahman: 1) Bajar la saturación HSL un 15-20 % (ver N4). 2) Fondo #121212-#1E1E1E, nunca #000000; #121212 es el de Material Design. 3) Tokens semánticos propios del modo oscuro: éxito #22C55E en claro, quizá #86EFAC en oscuro para 4,5:1 (ver N1).

## [W-ORBIX-PALETAS] Ejemplos y casos
- E1 · Spotify: carátulas sobre fondo casi negro (ap. 1).
- E2 · Stripe: blanco con acento morado; botón principal de color exclusivo (ap. 1, 5.3).
- E3 · Linear y Notion: casi monocromáticos y legibles (ap. 1, 10).
- E4 · Azul claro sobre azul medio: falla el contraste (ap. 4.1).

## [W-ORBIX-PALETAS] Errores frecuentes y advertencias
- Según Rahman: colores usados por igual o acento por todas partes (ap. 5); negro puro de fondo (ap. 7); saturados de modo claro en el oscuro (ap. 6, 7); complementarios saturados como fondo o texto (ap. 4.2).

## [W-ORBIX-PALETAS] Ejercicios y acciones
- Herramientas (ap. 9): «Colors» [dudoso: nombre cortado, quizá Coolors], genera armonías desde un tono; Adobe Color, rueda con tipos de armonía; Atmos.style, paleta, contraste y vista oscura.
- Simuladores de daltonismo gratuitos: complementos de Figma y emulación de Chrome DevTools (ap. 8.4).

## [W-ORBIX-PALETAS] Cifras y reglas concretas
- 4,5:1 y 3:1: WCAG 2.2 AA, texto normal y texto grande o componentes (ap. 4).
- 60/30/10 %: dominante, secundario, acento (ap. 5).
- 10-15 puntos HSL entre dominante y secundario (ap. 5.2).
- #121212-#1E1E1E: fondo oscuro (ap. 5.1, 7).
- 15-20 %: menos saturación en oscuro; 20-30 %: contra la vibración (ap. 7, 4.2).
- #22C55E y #86EFAC: éxito en claro y oscuro (ap. 7; ver N1).
- 8 % y 0,5 %: daltonismo en hombres y mujeres (ap. 8.1).

## [W-ORBIX-PALETAS] Preguntas que este artículo responde
- ¿Qué paleta uso en un panel de datos? Según Rahman en [W-ORBIX-PALETAS], monocromática o análoga, con acento complementario solo en lo crítico. C2, M2, ap. 10.
- ¿Cuántos colores necesita mi aplicación? Según Rahman en [W-ORBIX-PALETAS], 1-2 primarios, un acento, 6-10 neutros y 4 semánticos. C1, ap. 10.
- ¿Cómo reparto los colores? Según Rahman en [W-ORBIX-PALETAS], 60-30-10. M1, ap. 5.
- ¿Qué cambio en modo oscuro? Según Rahman en [W-ORBIX-PALETAS], menos saturación, gris #121212 y semánticos propios. M3, ap. 7.

## [W-ORBIX-PALETAS] Glosario
- HSL: tono, saturación y luminosidad (hue, saturation, lightness).
- WCAG: pautas de accesibilidad web del W3C; AA es el nivel habitual.
- Relación de contraste: cociente de luminancias texto-fondo, de 1:1 a 21:1.
- Token de diseño (design token): nombre para un valor compartido por diseño y código.
- Llamada a la acción (CTA): botón o enlace que pide actuar.
- Deuteranopía: daltonismo que confunde rojo y verde.

## [W-ORBIX-PALETAS] Específico de otro país
No aplica.

## [W-ORBIX-PALETAS] Notas de Claude
### N1 · El verde de éxito, mal planteado — [W-ORBIX-PALETAS], sobre M3, ap. 7
Qué dice el artículo: #22C55E se lee bien sobre blanco y quizá deba aclararse a #86EFAC en oscuro.
Qué no cuadra: con la fórmula WCAG, #22C55E da 2,28:1 sobre blanco (suspende) y ya 8,22:1 sobre #121212; el fallo está en modo claro.
Fuente: cálculo de Claude, 20 de octubre de 2026.

### N2 · Contraste de tono no es contraste WCAG — [W-ORBIX-PALETAS], sobre P2 y C3, ap. 4
Qué dice el artículo: las complementarias traen alto contraste y rojo sobre verde es de alto contraste.
Qué se sabe hoy: WCAG solo mide luminosidad; rojo puro sobre verde puro da unos 2,9:1 y sobre #008000, 1,3:1. Hay que medir siempre.
Fuente: cálculo de Claude, 20 de octubre de 2026.

### N3 · Ejemplos de marcas que no cuadran — [W-ORBIX-PALETAS], sobre C2, ap. 3.2, 3.5 y 3.6
Qué dice el artículo: Google es triádica (ap. 3.5) y tetrádica (ap. 3.6); Slack, análoga morada.
Qué no cuadra: lo de Google se contradice (su logotipo tiene cuatro colores), y el de Slack, desde 2019, también tiene cuatro.
Fuente: el propio artículo; Slack, conocimiento general de Claude, sin comprobar en detalle (https://techcrunch.com/2019/01/16/behold-slacks-new-logo).

### N4 · Porcentajes de modo oscuro sin respaldo — [W-ORBIX-PALETAS], sobre M3, ap. 7
Qué dice el artículo: desaturar un 15-20 %.
Qué se sabe hoy: Material Design usa #121212 y pide variantes más claras porque los saturados vibran, pero no da porcentajes.
Fuente: codelab de Google (https://codelabs.developers.google.com/codelabs/design-material-darktheme/), consultado el 20 de octubre de 2026.

### N5 · Prevalencia del daltonismo — [W-ORBIX-PALETAS], sobre P4, ap. 8.1
Qué dice el artículo: 8 % de hombres y 0,5 % de mujeres.
Qué se sabe hoy: son las cifras habituales en población de origen europeo; varían en otras.
Fuente: conocimiento general de Claude, sin comprobar.
