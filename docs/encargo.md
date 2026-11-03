# Encargo: taller de complementos de Anki a medida

Fecha: 2026-11-03 · Estado: aprobado

## Objetivo
Que la persona, sin programar, consiga los complementos de Anki que necesita pidiéndolos en lenguaje natural. Claude decide la técnica, construye, comprueba y entrega un `.ankiaddon` listo para instalar, tan fluido que parezca parte de Anki.

## Qué hará
1. Crear complementos nuevos a partir de lo que la persona describe, con un plan en llano que ella aprueba antes de construir.
2. Corregir y mejorar los complementos ya entregados, con una nota en el código por cada corrección para que no se repita.
3. Documentar cada complemento en lenguaje llano: qué hace y qué errores tuvo o tiene pendientes.
4. Entregar cada versión como `.ankiaddon` descargable desde GitHub, con los pasos para instalarlo, probarlo y volver atrás.

## Criterios de aceptación
Valen para cada entrega. Cada uno se comprueba con `python herramientas/comprobar.py` o con pasos que la persona pueda seguir en Anki.
- [ ] `comprobar.py` acaba en «Comprobación correcta» y la comprobación de GitHub sale en verde.
- [ ] Cada petición tiene su efecto descrito y probado, o declarado «pendiente de probar» con los pasos exactos.
- [ ] `docs/<paquete>/que-hace.md` y `errores.md` describen la versión entregada y ninguna nota FIX se ha perdido.
- [ ] Todo cambio en la colección se puede deshacer y lo masivo pide confirmación con la cifra exacta.
- [ ] Sin colores ni retoques de aspecto fuera de `docs/guia-interfaz.md` y la paleta Nocturne.

## Fuera del alcance
- Leer, copiar o abrir la colección real o la carpeta de perfiles de Anki.
- Bibliotecas que Anki no trae y conexiones a internet que la persona no haya pedido de forma expresa.
- Publicar en AnkiWeb y fusionar en la rama principal: lo hace la persona.

## Datos y seguridad
La colección de Anki puede acumular años de estudio: el taller nunca la lee ni la toca, y las pruebas usan una colección temporal. Lo que cambie un complemento dentro de Anki va por operaciones que se deshacen, con copia de seguridad antes de lo masivo. El repositorio no guarda claves ni contraseñas, y Claude Code tiene prohibido leer colecciones (`.claude/settings.json`).

## Decisiones técnicas
- Anki 26.09.3 (Python 3.13.15, Qt 6.11.2, Chromium 140) en Windows 11. Para comprobar, `aqt[qt]==26.9.3` de PyPI, última versión publicada el 2026-11-03.
- Solo la biblioteca estándar de Python y lo que trae Anki; estructura de `docs/ejemplo-referencia/`.
- Trabajo en la nube (claude.ai/code) con GitHub: una rama y un pull request por tarea, y comprobación automática en cada subida.

## Preguntas abiertas
- Ninguna.
