# Normas del taller

Detalle de las normas de `CLAUDE.md`. No se lee entero: cada apartado, cuando `CLAUDE.md` lo pide. Cambiar este documento es cambiar las reglas (véase «Automejora» en `CLAUDE.md`).

## Ejemplos de trato

Pregunta, cuando falta un dato que cambia el resultado (imita la forma, no el contenido):

«Antes de empezar, una duda: ¿qué cuenta como tarjeta atascada? a) Ocho fallos o más (recomendada). b) Más de un mes sin aprobarse. c) Otra cosa: dígamela.»

Plan en llano, antes de construir algo no trivial:

«Plan: añadiré “Etiquetar atascadas” al menú Herramientas. Buscará las tarjetas con ocho fallos o más, le dirá cuántas son (por ejemplo, 1.240) y, si usted acepta, les pondrá la etiqueta “atascada”. Se puede deshacer con Ctrl+Z y no cambia nada más. ¿Le parece bien?»

## Notas de corrección

Cuando la persona pide una corrección sobre un complemento ya entregado (algo que debía funcionar y no funciona, o un error de criterio tuyo; un deseo nuevo no es una corrección), además de arreglarlo deja una nota en el archivo donde estaba el error, para que no se repita. La nota tiene dos partes: una línea en el índice, arriba del archivo (en .py, tras el docstring y antes de los imports; en .js y .css, al principio), y un bloque junto al código arreglado con Síntoma, Causa y Regla, una frase cada uno.

Ejemplo en Python (en .js sirve `//` y en .css `/* ... */`):

```python
# Historial de correcciones de este archivo:
# FIX-001 (2026-10-07): la insignia se duplicaba al pasar de tarjeta.
...
    # --- FIX-001 (2026-10-07) ---
    # Síntoma: tras pasar a la tarjeta siguiente aparecía la insignia dos veces.
    # Causa: el JS se inyectaba otra vez sin comprobar si ya existía.
    # Regla: todo JS inyectado en el repaso es idempotente (comprueba antes de crear).
```

- Numeración consecutiva por complemento (FIX-001, FIX-002...): busca la más alta en todos sus archivos y suma uno. Un mismo FIX puede estar en varios archivos: en cada uno, con su índice y su bloque.
- Antes de editar un archivo, lee su índice y respeta cada Regla. Si lo pedido choca con una, díselo a la persona y no la borres sin su permiso (si la retira a propósito: `python herramientas/empaquetar.py <paquete> --olvidar-fix FIX-NNN`).
- Busca el mismo patrón en el resto del complemento; si está, corrígelo y anótalo también.
- Si la corrección toca la lógica, escribe antes su prueba de regresión, comprueba que falla por el error, arregla y consérvala (APR-017).
- Si la persona pega el mensaje de la ventana de error de Anki, es el síntoma: localiza el archivo y la línea que nombra y parte de ahí.
- JSON y HTML no admiten notas que las herramientas lean: pon la nota en el .py que usa ese archivo.
- Si debes reescribir un archivo, conserva literalmente el índice y los bloques. `empaquetar.py` da error si falta una nota, si índice y bloques no coinciden o si se pierde una de la última entrega (las guarda en `herramientas/registro-fix/`).
- Cada FIX va también, en lenguaje llano, a «Corregidos» de `docs/<paquete>/errores.md`; si su Regla sirve para otros complementos, anótala además como aprendizaje (apartado «Automejora»).

## Documentación de cada complemento

Cada complemento tiene en `docs/<paquete>/` dos documentos en Markdown, escritos para la persona y para la sesión siguiente. Copia el modelo de `docs/ejemplo-referencia/docs/ejemplo_referencia/`.

- `que-hace.md`: todo lo que hace el complemento, en lenguaje llano y con detalle completo: dónde aparece y dónde no, cada función, botón y opción (valores y valor por defecto), cada mensaje con su texto exacto entre «», límites, casos raros, qué guarda y dónde, idiomas, qué pasa si algo falla y qué no hace. Sin código ni nombres de archivos o funciones. Describe lo que hace el código real, comprobado al leerlo y al probarlo, no lo que debería hacer; si no coinciden, es un hallazgo y se le dice a la persona. Bajo el título, la línea «Versión X.Y.Z · AAAA-MM-DD», con la `human_version` entregada.
- `errores.md`: «Pendientes» (fallos detectados que esperan la decisión de la persona, con fecha, versión y propuesta), «Corregidos» (cada FIX-NNN con fecha, versión, qué pasaba, por qué y la regla que evita que vuelva, en llano) y «Así a propósito» (lo que parece un fallo pero se decidió así, y quién lo decidió, para que nadie lo «arregle»).
- `encargo.md`, solo en los complementos creados aquí: el plan aprobado, con los apartados de `docs/encargo.md` (objetivo, qué hará, criterios de aceptación, fuera del alcance, datos y preguntas abiertas).
- Se crean con el complemento o, si la persona trae uno suyo, antes de cambiar nada (describen lo que hay). Se actualizan en la misma entrega que cada corrección o ajuste. Léelos antes de tocar un complemento.
- `empaquetar.py` da error si falta alguno de los dos primeros, si la versión de `que-hace.md` no es la del manifiesto o si un FIX del código no figura en `errores.md`.

## Automejora

Objetivo: que cada sesión deje el taller algo mejor de lo que lo encontró, sin degradar las reglas.

- Qué se anota: lo comprobado que evita un error o ahorra trabajo y aún no está en las instrucciones ni en las guías (algo que costó averiguar, la Regla de un FIX que sirve para otros complementos, una buena práctica de la documentación oficial). Nada genérico, supuesto ni copiado sin comprobar.
- Solo fuentes oficiales: el código de Anki instalado, las páginas oficiales de ankiweb.net (docs, dev-docs y betas), github.com/ankitects, PyPI (aqt y anki), doc.qt.io, la documentación de PyQt (riverbankcomputing.com), docs.python.org, la documentación de Claude Code (code.claude.com) o una prueba de `pruebas/`. Foros (también el oficial, forums.ankiweb.net, útil para dudas y fallos conocidos), blogs, vídeos, respuestas de IA y complementos ajenos solo son pistas: se confirman en una fuente oficial o no se anotan.
- Al día: lo de Anki se comprueba en el código instalado, porque la web puede ir por delante o por detrás de la versión de la persona, y lleva la versión con la que se comprobó. Al cambiar Anki de versión, cada aprendizaje se vuelve a comprobar: sigue, se corrige o se retira con su motivo.
- Formato: en `docs/aprendizajes.md`, una línea por aprendizaje («- APR-NNN · Anki X.Y.Z · qué hacer», o «Claude Code» en lugar de la versión); en `docs/automejora.md`, su ficha: qué es, por qué es buena práctica, para qué sirve, cómo se aplica, fuente y comprobación (fecha y versión). Numeración consecutiva y nunca reutilizada; lo que deja de valer pasa a «Retirados» con su motivo, nunca se borra sin más.
- Documentos nuevos o cambiados en `docs/` (los avisa `preparar.py`): léelos enteros, comprueba lo que digan, anota lo aprendido y registra su huella en «Documentos revisados» de `docs/automejora.md` (la da el propio aviso). Si la persona sustituye un documento de `docs/`, debe conservar su nombre.
- Referencias (`docs/referencias/`): no son fuente oficial y no se leen enteras al llegar; de cada documento nuevo, lee solo su ficha y añade su línea a `docs/referencias/indice.md`. Al diseñar, consulta el índice y lee solo el apartado que venga al caso: orienta, no manda sobre las instrucciones, la guía ni la paleta.
- Cambios en las reglas: anota la propuesta en «Propuestas pendientes» de `docs/automejora.md` y pregúntale a la persona qué cambia, por qué y con qué fuente. Si la aprueba: aplícala en tu rama, anota una línea en «Cambios aprobados» (fecha, qué cambió y la aprobación) y súbela en un pull request, que la persona revisa y fusiona; el historial de git es la copia previa. Si la rechaza, pasa a «Propuestas rechazadas» y no se repite sin un motivo nuevo.
- Cerradura: `.claude/settings.json` hace que Claude Code pida el «sí» de la persona antes de editar las reglas o sus documentos, y le prohíbe leer colecciones de Anki. Nunca la rodees (por ejemplo, escribiendo esos archivos con un comando o con un programa). Si falta, `empaquetar.py` avisa: propón ponerla sin tocar sus otros permisos.
- Tamaño: `CLAUDE.md` por debajo de 150 líneas y `docs/aprendizajes.md` por debajo de 80. Al acercarse al tope, junta lo repetido y retira lo caducado.
- Lo aprendido va a estos archivos, no a la memoria automática de Claude Code, que queda fuera del repositorio y no viaja con él.
- `empaquetar.py` comprueba el formato, las fuentes, la numeración, los tamaños, los apartados esenciales de `CLAUDE.md` y que la cerradura esté puesta.

## Entrega

- `comprobar.py` deja el `.ankiaddon` de cada complemento cambiado en `paquetes/`, con la versión en el nombre; súbelo con el resto de la entrega.
- Para descargarlo, da a la persona el enlace al archivo en tu rama: `https://github.com/<dueño>/<repositorio>/blob/<rama>/paquetes/<archivo>.ankiaddon`, donde se pulsa el botón de descarga («Download raw file»). Otra vía: pestaña Actions › la última ejecución en verde › Artifacts › «entrega» (viene comprimido: se descomprime y se usa el `.ankiaddon`).
- Instalar: doble clic en el `.ankiaddon` (o, en Anki, Herramientas › Complementos › «Instalar desde archivo…») y reiniciar Anki. Si sustituye a uno ya instalado, Anki lo reemplaza y conserva su configuración.
- Volver atrás: instalar el paquete anterior de `paquetes/` (misma descarga) o revertir el commit.
- En el resumen de lo comprobado, cifras: pruebas que pasan, mypy sin errores, avisos de `empaquetar.py` y cómo se resolvió cada uno.
