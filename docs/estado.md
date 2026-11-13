# Estado del trabajo

Se actualiza al terminar cada sesión de un trabajo largo y se lee al retomarlo. Va aquí, y no en CLAUDE.md, porque cambia a menudo.

## Hecho

- 2026-11-03: el taller se adaptó a la plantilla en la rama `refactor-plantilla`, con el plan aprobado (solo en la nube; automejora aligerada; cerradura intacta). CLAUDE.md queda en 117 líneas y el detalle de las normas pasa a `docs/normas-del-taller.md`; el encargo del taller está en `docs/encargo.md`. Comprobación general con `herramientas/comprobar.py` (también al final de cada turno y en GitHub Actions), preparación de la nube con `herramientas/preparar.py` y el script de `docs/preparar-entorno.md`, y permisos con cerradura y colecciones protegidas en `.claude/settings.json`. `herramientas/copias` y las huellas de CLAUDE.md se retiran: el historial de git guarda cada versión. El código de los complementos no cambia: GritMap (37 pruebas) y Nocturne (81) pasan la comprobación.

- 2026-11-04: GritMap pasa de la 3.5.0 a la 4.11.2 que traía la persona (hecha fuera del taller) y
  a la 4.12.0 con las mejoras del informe 4.11, aprobado entero. Se rehízo `que-hace.md` a partir del
  código, se anotaron FIX-024 a FIX-031 en `errores.md` y se pusieron al día las pruebas de la 3.5.0
  (45 pruebas). Su `meta.json` personal no se sube: el repositorio es público.

- 2026-11-04: Atelier pasa a la 3.8.0 y GritMap a la 4.13.0 con la auditoría «Atelier 3.7.2»
  del 2026-11-04, aprobada entera (también el borde visible de los campos, que en octubre se había
  descartado, y las dos propuestas que eran de GritMap). La versión que la persona tenía instalada
  era idéntica a la del repositorio. FIX-012 (fila seleccionada de Explorar por debajo de 4,5 en
  cuatro paletas) y FIX-013 (botón del cuerpo relleno en Preferencias). Lo no aplicado, con su
  motivo, está en «Así a propósito» de docs/nocturne/errores.md; el blanco puro del editor queda en
  «Pendientes».

- 2026-11-09: GritMap 4.14.0 quita los globos de las tarjetas (informe breve del cliente del
  mismo día, aprobado entero): récord delante de los comodines, motivo de «N/A» en la línea gris, sin
  objetivo de FSRS, «falta 1 tarjeta» con la frase en plural en cada idioma y el globo del sistema
  solo con la línea cortada. 54 pruebas.

- 2026-11-09: GritMap 4.15.0 con el informe «textos, hábito y abandono» (aprobado entero), las
  líneas grises y el pie del mapa en minúscula y la accesibilidad de las líneas (sin corte, «·»
  oído como pausa, «✓ hoy» oído como «hoy hecho»). 62 pruebas. Va en el mismo pull request que la
  4.14.0.

- 2026-11-09: GritMap 4.15.1: «Propuesta: 5 (el 80 % de su promedio diario).», sin la cifra final,
  en 51 idiomas (petición del cliente).

- 2026-11-13: Sonidos de consola 1.0.0, nuevo (plan aprobado en docs/sonidos_consola/encargo.md):
  los siete sonidos de la persona, que ella copia en user_files (no van en el repositorio). Excepción
  aprobada: PyQt6.QtMultimedia en empaquetar.py (ALLOWED_DIRECT_QT). 36 pruebas. Falta que la persona
  lo pruebe en Windows con audio.

## En curso

- El pull request de la adaptación espera la revisión de la persona. No se fusiona sin ella.

## Siguiente paso

Seis complementos no pasan `python herramientas/empaquetar.py <paquete> --solo-comprobar` (Anki 26.09.3, 2026-11-03); su código no se ha tocado. Uno por sesión, cada uno con su corrección, sus notas y su entrega, empezando por los de menos errores:

| Complemento | Errores | Qué falla |
| --- | --- | --- |
| ProFeedback | 1 | `audio.py:43` importa Qt directamente, no desde `aqt.qt`. |
| Always on Top | 2 | Falla al importarse fuera de Anki (`__init__.py:22`, sin `if mw is None: return`); FIX-001 está en el índice de `shortcuts.py`, pero sin su bloque. |
| Hider | 2 | mypy: `logic.py:725` (`moveToState` recibe un texto cualquiera) y `logic.py:741` (`get_queued_cards` con el planificador ficticio); falla al importarse fuera de Anki porque importa `aqt.deckbrowser` al cargar, que llama a `tr` (APR-064). |
| Restart | 3 | Falla al importarse fuera de Anki (`__init__.py:15`); FIX-003 está en el índice de `logic.py` y de `ui.py`, pero sin su bloque. Aviso: la nota FIX-002 de `logic.py:200` no tiene Síntoma, Causa ni Regla. |
| Edit field during review | 4 | Dos colores fijos en `web/editor.css` (líneas 8 y 32); FIX-001 de `web/editor.css` no está en su índice; falla al importarse fuera de Anki porque `__init__.py` importa `anki.hooks` antes que `aqt` (APR-069). Aviso: `dialogs.py:36` usa `_()` (APR-039). |
| CoreProgress | 162 | 160 colores fijos en `palettes.py` y 2 en `view.py`: decidir si son paletas de datos legítimas (marca «colores-ok: motivo») o se pasan a la paleta Nocturne. |

Los seis tienen además el aviso de que no hay pruebas de su lógica en `pruebas/<paquete>/`.

## Dudas para la persona

- El repositorio es público: cualquiera puede ver el código y descargar los paquetes. Cambiarlo es decisión suya, en GitHub: Settings › General › Danger Zone › Change visibility.
- ProFeedback trae sonidos con nombres de marcas (Mario Bros, Duolingo, Khan). Si son copias de los originales, publicarlos en un repositorio público puede vulnerar derechos de autor; no se ha comprobado su origen.
