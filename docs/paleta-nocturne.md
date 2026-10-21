# Paleta Nocturne — referencia de color para complementos de Anki

> Documento de contexto. Nocturne es el complemento de color **principal**: define
> los colores por defecto de la interfaz de Anki en **modo día** y **modo noche**.
> Cualquier complemento futuro debería tomar estos valores como referencia para que
> su apariencia **combine** con Anki en ambos modos, en lugar de introducir colores
> sueltos. Todos los valores están en formato hexadecimal; los de 8 dígitos incluyen
> transparencia (`#RRGGBBAA`).

## Identidad

Azul sereno de acción sobre una base de grises ligeramente azulados. El modo día es
luminoso y limpio; el modo noche es profundo pero no negro puro, para reducir el
deslumbramiento. Valores de Nocturne 3.3.0 (2026-10-21), comprobados en cada entrega por las
pruebas del taller:

* Todo color que se use como texto llega a 4,5:1 sobre cualquier fondo (WCAG 2) y,
  medido con APCA, a 75 el texto principal (`FG`), 60 el secundario (`FG_SUBTLE`) y
  45 el menos importante (`FG_FAINT`). El texto desactivado (`FG_DISABLED`) llega
  a 30 de APCA, el mínimo absoluto, y queda por debajo de `FG_FAINT` a propósito.
* De noche, el texto principal queda en unos 13:1 frente al fondo, para no
  deslumbrar, y lo que está «más arriba» es más claro: `CANVAS_INSET` < `CANVAS` <
  `CANVAS_ELEVATED` < `BUTTON_BG` < `CANVAS_OVERLAY` < `BUTTON_HOVER`.
* Bordes de casillas (`NOCTURNE_CONTROL_BORDER`) e iconos de bandera, 3:1 o más.
  La bandera roja y la verde se distinguen además por su claridad.
* Nocturne es una de las tres paletas del complemento (con Papel y Bosque); este
  documento describe solo Nocturne, la de serie. Las otras están en
  `complementos/nocturne/themes.py`.

## Cómo usar esta paleta en un complemento futuro

Hay dos vías, según dónde pinte el complemento:

**1. Interfaz nativa (ventanas y widgets Qt).** Cuando Nocturne está activo, ya ha
reescrito los tokens de Anki, así que basta con leer el color del tema activo:

```python
from aqt import colors
from aqt.theme import theme_manager

# Devuelve el valor correcto según el modo (día/noche) en curso:
color = theme_manager.var(colors.CANVAS)          # fondo base
texto = theme_manager.var(colors.FG)              # texto principal
acento = theme_manager.var(colors.BUTTON_PRIMARY_BG)  # azul de acción
```

**2. Contenido web (repaso, editor, vistas propias en webview).** Usa las variables
CSS que Nocturne inyecta, siempre con un valor de reserva por si el complemento se
usa sin Nocturne:

```css
.mi-addon-boton {
  background: var(--button-primary-bg, #3B6FE0);
  color: var(--highlight-fg, #FFFFFF);
  border: 1px solid var(--border, #DADEE7);
  border-radius: 6px;
}
/* Para adaptarse al modo noche sin JS, apóyate en la clase de Anki: */
body.night_mode .mi-addon-boton {
  background: var(--button-primary-bg, #4066E6);
}
```

No fijes colores a mano si existe un token equivalente: úsalo, y así el complemento
seguirá encajando aunque la paleta se ajuste en el futuro.

## Tabla de colores (modo día y modo noche)

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
|`STATE_LEARN`|`--state-learn`|`#B8460A`|`#F1A95B`|
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
|`FLAG_1`|`--flag-1`|`#D92121`|`#D13939`|
|`FLAG_2`|`--flag-2`|`#E8590C`|`#C07F3A`|
|`FLAG_3`|`--flag-3`|`#2F9E44`|`#4C9E5A`|
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

## Bloque para pegar como contexto

Mismo contenido en JSON, cómodo para incluir como referencia rápida:

```json
{
  "ACCENT_CARD": {
    "css": "--accent-card",
    "light": "#186CB9",
    "dark": "#7EBFF4"
  },
  "ACCENT_DANGER": {
    "css": "--accent-danger",
    "light": "#CA2D2D",
    "dark": "#F37777"
  },
  "ACCENT_NOTE": {
    "css": "--accent-note",
    "light": "#257A35",
    "dark": "#57D06B"
  },
  "BORDER": {
    "css": "--border",
    "light": "#DADEE7",
    "dark": "#2C3444"
  },
  "BORDER_FOCUS": {
    "css": "--border-focus",
    "light": "#3B6FE0",
    "dark": "#6390FF"
  },
  "BORDER_STRONG": {
    "css": "--border-strong",
    "light": "#C0C6D3",
    "dark": "#3D475C"
  },
  "BORDER_SUBTLE": {
    "css": "--border-subtle",
    "light": "#E8EAF0",
    "dark": "#1F2635"
  },
  "BUTTON_BG": {
    "css": "--button-bg",
    "light": "#FBFCFE",
    "dark": "#242C3A"
  },
  "BUTTON_DISABLED": {
    "css": "--button-disabled",
    "light": "#FBFCFE80",
    "dark": "#242C3A80"
  },
  "BUTTON_HOVER": {
    "css": "--button-gradient-start, --button-gradient-end",
    "light": "#EDF0F5",
    "dark": "#2E3747"
  },
  "BUTTON_HOVER_BORDER": {
    "css": "--button-hover-border",
    "light": "#C0C6D3",
    "dark": "#3D475C"
  },
  "BUTTON_PRIMARY_BG": {
    "css": "--button-primary-bg",
    "light": "#3B6FE0",
    "dark": "#4066E6"
  },
  "BUTTON_PRIMARY_DISABLED": {
    "css": "--button-primary-disabled",
    "light": "#3B6FE059",
    "dark": "#4066E659"
  },
  "BUTTON_PRIMARY_GRADIENT_END": {
    "css": "--button-primary-gradient-end",
    "light": "#2F5BC7",
    "dark": "#3452C8"
  },
  "BUTTON_PRIMARY_GRADIENT_START": {
    "css": "--button-primary-gradient-start",
    "light": "#3B6FE0",
    "dark": "#4066E6"
  },
  "CANVAS": {
    "css": "--canvas, --bs-body-bg",
    "light": "#F7F8FA",
    "dark": "#12161F"
  },
  "CANVAS_CODE": {
    "css": "--canvas-code",
    "light": "#F2F4F7",
    "dark": "#141924"
  },
  "CANVAS_ELEVATED": {
    "css": "--canvas-elevated",
    "light": "#FBFCFE",
    "dark": "#212836"
  },
  "CANVAS_GLASS": {
    "css": "--canvas-glass",
    "light": "#FBFCFECC",
    "dark": "#212836CC"
  },
  "CANVAS_INSET": {
    "css": "--canvas-inset",
    "light": "#EEF0F4",
    "dark": "#0F131B"
  },
  "CANVAS_OVERLAY": {
    "css": "--canvas-overlay",
    "light": "#FBFCFE",
    "dark": "#293040"
  },
  "FG": {
    "css": "--fg, --bs-body-color",
    "light": "#1B2430",
    "dark": "#D6DAE1"
  },
  "FG_DISABLED": {
    "css": "--fg-disabled",
    "light": "#A9AFBC",
    "dark": "#7C869A"
  },
  "FG_FAINT": {
    "css": "--fg-faint",
    "light": "#646C7D",
    "dark": "#9AA3B4"
  },
  "FG_LINK": {
    "css": "--fg-link",
    "light": "#2F63D8",
    "dark": "#A3C1F7"
  },
  "FG_SUBTLE": {
    "css": "--fg-subtle",
    "light": "#4E576A",
    "dark": "#B7BECC"
  },
  "FLAG_1": {
    "css": "--flag-1",
    "light": "#D92121",
    "dark": "#D13939"
  },
  "FLAG_2": {
    "css": "--flag-2",
    "light": "#E8590C",
    "dark": "#C07F3A"
  },
  "FLAG_3": {
    "css": "--flag-3",
    "light": "#2F9E44",
    "dark": "#4C9E5A"
  },
  "FLAG_4": {
    "css": "--flag-4",
    "light": "#1971C2",
    "dark": "#5993C2"
  },
  "FLAG_5": {
    "css": "--flag-5",
    "light": "#C62FAD",
    "dark": "#B378C1"
  },
  "FLAG_6": {
    "css": "--flag-6",
    "light": "#099268",
    "dark": "#439C81"
  },
  "FLAG_7": {
    "css": "--flag-7",
    "light": "#7048E8",
    "dark": "#9680D6"
  },
  "HIGHLIGHT_BG": {
    "css": "--highlight-bg",
    "light": "#3B6FE0",
    "dark": "#4066E6"
  },
  "HIGHLIGHT_FG": {
    "css": "--highlight-fg",
    "light": "#FFFFFF",
    "dark": "#FFFFFF"
  },
  "NOCTURNE_ROW_HIGHLIGHT": {
    "css": "--nocturne-row-highlight",
    "light": "#EAEEF8",
    "dark": "#19233F"
  },
  "SCROLLBAR_BG": {
    "css": "--scrollbar-bg",
    "light": "#D5D9E2",
    "dark": "#272F3F"
  },
  "SCROLLBAR_BG_ACTIVE": {
    "css": "--scrollbar-bg-active",
    "light": "#AAB1C0",
    "dark": "#3D475C"
  },
  "SCROLLBAR_BG_HOVER": {
    "css": "--scrollbar-bg-hover",
    "light": "#C0C6D3",
    "dark": "#353E50"
  },
  "SELECTED_BG": {
    "css": "--selected-bg",
    "light": "#3B6FE038",
    "dark": "#6390FF40"
  },
  "SELECTED_FG": {
    "css": "--selected-fg",
    "light": "#1B2430",
    "dark": "#D6DAE1"
  },
  "SHADOW": {
    "css": "--shadow",
    "light": "#1B243026",
    "dark": "#05080F66"
  },
  "SHADOW_FOCUS": {
    "css": "--shadow-focus",
    "light": "#3B6FE040",
    "dark": "#6390FF4D"
  },
  "SHADOW_INSET": {
    "css": "--shadow-inset",
    "light": "#1B24301A",
    "dark": "#05080F4D"
  },
  "SHADOW_SUBTLE": {
    "css": "--shadow-subtle",
    "light": "#1B243012",
    "dark": "#05080F33"
  },
  "STATE_BURIED": {
    "css": "--state-buried",
    "light": "#9A7B3F",
    "dark": "#A98754"
  },
  "STATE_LEARN": {
    "css": "--state-learn",
    "light": "#B8460A",
    "dark": "#F1A95B"
  },
  "STATE_MARKED": {
    "css": "--state-marked",
    "light": "#7048E8",
    "dark": "#9680D6"
  },
  "STATE_NEW": {
    "css": "--state-new",
    "light": "#186CB9",
    "dark": "#7EBFF4"
  },
  "STATE_REVIEW": {
    "css": "--state-review",
    "light": "#257A35",
    "dark": "#57D06B"
  },
  "STATE_SUSPENDED": {
    "css": "--state-suspended",
    "light": "#868E96",
    "dark": "#848E9C"
  }
}
```

## Reglas de coherencia

* **Haz** que cada elemento nuevo derive su color de un token de esta tabla.
* **Haz** que el color de acción (botones/enlaces destacados) use el azul
`BUTTON_PRIMARY_BG` / `HIGHLIGHT_BG`; es el azul de acción del sistema.
* **Haz** que el texto sobre un fondo de acción use `HIGHLIGHT_FG` (blanco).
* **Haz** que cualquier color que definas a mano tenga su pareja día **y** noche.
* **Evita** el negro puro (`#000`) y el blanco puro como fondos: usa `CANVAS` y
`CANVAS_ELEVATED`.
* **Evita** introducir un segundo azul de acción distinto; reutiliza el existente.
* **Evita** rojos o verdes fuera de los ya definidos (`ACCENT_DANGER`,
`ACCENT_NOTE`, `FLAG_*`), para no romper el código de color de Anki.
