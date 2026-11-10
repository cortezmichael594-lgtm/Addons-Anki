# Contexto común para las ocho fichas

Fecha: 9 de noviembre de 2026. Este documento acompaña a las fichas de cada complemento. Sirve a una
persona o a una inteligencia artificial que vaya a rediseñar la interfaz o las funciones: explica el
entorno en el que viven los complementos y la paleta de color de referencia. Las fichas no hablan de
código, sino de lo que se ve, se oye y se puede hacer.

## Qué es Anki y dónde viven los complementos

Anki es un programa de tarjetas de memoria con repaso espaciado (cada tarjeta vuelve justo antes de
que se olvide). Sus pantallas principales:

- Lista de mazos (pantalla principal): tabla de mazos con tres columnas de cifras (Nuevas, Aprender,
  A repasar), barra superior (Mazos, Añadir, Explorar, Estadísticas, Sincronizar) y barra inferior
  con botones (Descargar mazos compartidos, Crear mazo, Importar archivo).
- Pantalla de un mazo (resumen): nombre, cifras de Nuevas, Aprendiendo y A repasar, y el botón
  «Comenzar a estudiar».
- Repaso: la tarjeta (pregunta y respuesta) en el centro; abajo, una barra con «Editar», «Mostrar
  respuesta» (o los botones de respuesta «Otra vez», «Difícil», «Bien», «Fácil», con el intervalo
  previsto encima de cada uno) y «Más».
- Explorar: buscador de tarjetas con tabla, barra lateral y editor.
- Añadir y Editar: ventanas con el editor de campos.
- Herramientas > Complementos: lista de complementos; el botón «Configuración» abre las opciones de
  cada uno.

Las páginas de Anki (lista de mazos, repaso, editor, estadísticas) son páginas web internas; las
ventanas (Explorar, Preferencias, diálogos) son ventanas nativas del sistema. Anki tiene modo día y
modo noche, que la persona elige en Preferencias > Tema.

## Entorno de la persona

Windows 11, Anki 26.09.3, letra de interfaz Segoe UI Variable. Usa los ocho complementos a la vez.

## Principios de diseño que siguen todos (normas del taller)

- Prioridades, por este orden: la colección (años de estudio) nunca se pone en riesgo y todo cambio
  se puede deshacer; Anki nunca se bloquea ni se entrecorta; la persona entiende lo que ocurre; lo
  sencillo antes que lo vistoso.
- Nativo primero: menús, botones, ventanas y avisos con el aspecto estándar de Anki. Un control
  dibujado a mano, solo si la persona lo pide.
- Paleta Nocturne (tabla de abajo) como fuente de todos los colores, con su pareja de modo noche. Un
  único azul de acción. Ni negro ni blanco puros como fondo.
- Sin parpadeos: las ventanas se construyen enteras antes de mostrarse; en las páginas, todo llega
  antes del primer pintado y nada desplaza lo que ya está.
- Sin animaciones salvo petición; si las hay, solo de opacidad o desplazamiento y de 150 ms como
  máximo (ProFeedback y CoreProgress son excepciones aprobadas).
- Un fallo nunca abre la ventana de error de Anki.
- Textos en español de España, con punto de millar («1.240 notas»).
- Contraste mínimo: 4,5 a 1 para texto (WCAG 2) y 3 a 1 para bordes de controles e iconos.

## Paleta Nocturne (Atelier 3.8.0, paleta de serie)

Valores hexadecimales; los de 8 cifras llevan transparencia (#RRGGBBAA). La columna «Variable»
es el nombre con el que las páginas de Anki la usan.

### Lienzos y fondos

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`CANVAS`|`--canvas`, `--bs-body-bg`|`#F7F8FA`|`#12161F`|
|`CANVAS_ELEVATED`|`--canvas-elevated`|`#FBFCFE`|`#212836`|
|`CANVAS_OVERLAY`|`--canvas-overlay`|`#FBFCFE`|`#293040`|
|`CANVAS_INSET`|`--canvas-inset`|`#EEF0F4`|`#0F131B`|
|`CANVAS_CODE`|`--canvas-code`|`#F2F4F7`|`#141924`|
|`CANVAS_GLASS`|`--canvas-glass`|`#FBFCFECC`|`#212836CC`|

### Texto

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`FG`|`--fg`, `--bs-body-color`|`#1B2430`|`#D6DAE1`|
|`FG_SUBTLE`|`--fg-subtle`|`#4E576A`|`#B7BECC`|
|`FG_FAINT`|`--fg-faint`|`#646C7D`|`#9AA3B4`|
|`FG_DISABLED`|`--fg-disabled`|`#A9AFBC`|`#7C869A`|
|`FG_LINK`|`--fg-link`|`#2F63D8`|`#A3C1F7`|

### Bordes

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`BORDER`|`--border`|`#DADEE7`|`#2C3444`|
|`BORDER_SUBTLE`|`--border-subtle`|`#E8EAF0`|`#1F2635`|
|`BORDER_STRONG`|`--border-strong`|`#C0C6D3`|`#3D475C`|
|`BORDER_FOCUS`|`--border-focus`|`#3B6FE0`|`#6390FF`|

### Selección y resaltado

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`HIGHLIGHT_BG`|`--highlight-bg`|`#3B6FE0`|`#4066E6`|
|`HIGHLIGHT_FG`|`--highlight-fg`|`#FFFFFF`|`#FFFFFF`|
|`SELECTED_BG`|`--selected-bg`|`#3B6FE038`|`#6390FF40`|
|`SELECTED_FG`|`--selected-fg`|`#1B2430`|`#D6DAE1`|

### Botones

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`BUTTON_BG`|`--button-bg`|`#FBFCFE`|`#242C3A`|
|`BUTTON_HOVER`|`--button-gradient-start`, `--button-gradient-end`|`#EDF0F5`|`#2E3747`|
|`BUTTON_HOVER_BORDER`|`--button-hover-border`|`#C0C6D3`|`#3D475C`|
|`BUTTON_DISABLED`|`--button-disabled`|`#FBFCFE80`|`#242C3A80`|
|`BUTTON_PRIMARY_BG`|`--button-primary-bg`|`#3B6FE0`|`#4066E6`|
|`BUTTON_PRIMARY_GRADIENT_START`|`--button-primary-gradient-start`|`#3B6FE0`|`#4066E6`|
|`BUTTON_PRIMARY_GRADIENT_END`|`--button-primary-gradient-end`|`#2F5BC7`|`#3452C8`|
|`BUTTON_PRIMARY_DISABLED`|`--button-primary-disabled`|`#3B6FE059`|`#4066E659`|

### Acentos

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`ACCENT_CARD`|`--accent-card`|`#186CB9`|`#7EBFF4`|
|`ACCENT_NOTE`|`--accent-note`|`#257A35`|`#57D06B`|
|`ACCENT_DANGER`|`--accent-danger`|`#CA2D2D`|`#F37777`|

### Estados de tarjeta

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`STATE_NEW`|`--state-new`|`#186CB9`|`#7EBFF4`|
|`STATE_LEARN`|`--state-learn`|`#CA2D2D`|`#F37777`|
|`STATE_REVIEW`|`--state-review`|`#257A35`|`#57D06B`|
|`STATE_BURIED`|`--state-buried`|`#9A7B3F`|`#A98754`|
|`STATE_SUSPENDED`|`--state-suspended`|`#868E96`|`#848E9C`|
|`STATE_MARKED`|`--state-marked`|`#7048E8`|`#9680D6`|

### Barras de desplazamiento

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`SCROLLBAR_BG`|`--scrollbar-bg`|`#D5D9E2`|`#272F3F`|
|`SCROLLBAR_BG_HOVER`|`--scrollbar-bg-hover`|`#C0C6D3`|`#353E50`|
|`SCROLLBAR_BG_ACTIVE`|`--scrollbar-bg-active`|`#AAB1C0`|`#3D475C`|

### Sombras

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`SHADOW`|`--shadow`|`#1B243026`|`#05080F66`|
|`SHADOW_SUBTLE`|`--shadow-subtle`|`#1B243012`|`#05080F33`|
|`SHADOW_INSET`|`--shadow-inset`|`#1B24301A`|`#05080F4D`|
|`SHADOW_FOCUS`|`--shadow-focus`|`#3B6FE040`|`#6390FF4D`|

### Banderas (flags)

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`FLAG_1`|`--flag-1`|`#BE1D1D`|`#C12D2D`|
|`FLAG_2`|`--flag-2`|`#E8590C`|`#C07F3A`|
|`FLAG_3`|`--flag-3`|`#2F9E44`|`#4DA05B`|
|`FLAG_4`|`--flag-4`|`#1971C2`|`#5993C2`|
|`FLAG_5`|`--flag-5`|`#C62FAD`|`#B378C1`|
|`FLAG_6`|`--flag-6`|`#099268`|`#439C81`|
|`FLAG_7`|`--flag-7`|`#7048E8`|`#9680D6`|

### Propios de Nocturne (sin variable CSS; solo los usa el complemento en las ventanas)

|Token|Variable CSS|LIGHT (día)|DARK (noche)|
|-|-|-|-|
|`NOCTURNE_CONTROL_BORDER`|—|`#878C97`|`#727B8C`|
|`NOCTURNE_PRIMARY_PRESSED`|—|`#284EAA`|`#2B45AA`|
|`NOCTURNE_PRIMARY_RING`|—|`#1C3A8A`|`#A9C4FF`|
|`NOCTURNE_ROW_HIGHLIGHT`|`--nocturne-row-highlight`|`#EAEEF8`|`#19233F`|
|`NOCTURNE_TITLEBAR`|— (barra de título, solo Windows 11)|`#FAFBFE`|`#070C16`|

## Reglas de la paleta

- Todo color nuevo sale de un token de la tabla y tiene pareja de día y de noche.
- El azul de acción (botones principales, enlaces destacados) es BUTTON_PRIMARY_BG / HIGHLIGHT_BG;
  el texto encima, HIGHLIGHT_FG (blanco).
- No hay un segundo azul de acción, ni rojos o verdes fuera de ACCENT_DANGER, ACCENT_NOTE y FLAG_*.
- De noche, lo que está «más arriba» es más claro: CANVAS_INSET < CANVAS < CANVAS_ELEVATED <
  BUTTON_BG < CANVAS_OVERLAY < BUTTON_HOVER.
- Texto: FG llega a 75 de APCA, FG_SUBTLE a 60, FG_FAINT a 45; FG_DISABLED a 30, más apagado a
  propósito.

## Las fichas

| Complemento | Versión | Qué hace, en una línea |
|---|---|---|
| Atelier (paquete «nocturne») | 3.8.0 | Temas de color completos para todo Anki: cinco paletas de día y de noche |
| GritMap | 4.15.1 | Mapa de calor del estudio del año, con racha, meta diaria y fechas clave |
| CoreProgress | 1.2.0 | Barra de progreso del repaso, con hitos, racha de aciertos y récord |
| ProFeedback | 2.1.0 | Sonidos al acertar, insignias en la tarjeta, botones de colores y confeti al terminar |
| Hider | 4.1.0 | Repaso sin distracciones: oculta barras y puntero, y entra directo al repaso |
| Edit field during review | 1.1.0 | Corregir un campo con Ctrl+clic sobre la tarjeta, durante el repaso |
| Always on Top | 1.3 | Mantener la ventana Añadir por encima de otros programas con un atajo |
| Restart | 2.1.0 | Reiniciar Anki con un atajo (Ctrl+R) |

La ventana de configuración de todos los complementos debe seguir el modelo del panel de GritMap,
descrito pieza a pieza en `09-patron-configuracion.md` (decisión de la persona, 9 de noviembre de
2026).

Los complementos que pintan colores propios son Atelier, GritMap, CoreProgress, ProFeedback y Edit
field during review. Hider, Always on Top y Restart no pintan nada propio fuera de su ventana de opciones (el panel
modelo) y de los avisos breves de Anki.
