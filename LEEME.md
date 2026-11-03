# Complementos de Anki a medida: cómo usar este taller

Este repositorio es el taller donde Claude Code crea y mantiene sus complementos de Anki. Es como entregar a un carpintero el taller ya montado: las normas de la casa (`CLAUDE.md`), los instrumentos de control de calidad (`herramientas/`) y el encargo por escrito (`docs/encargo.md`). Usted pide en lenguaje normal lo que quiere; Claude lo construye, lo comprueba y le deja un archivo `.ankiaddon` listo para instalar con doble clic.

Su colección de Anki no está aquí, y Claude Code tiene prohibido leerla o tocarla.

## Qué hay dentro

| Archivo o carpeta | Para qué sirve |
| --- | --- |
| `CLAUDE.md` | Instrucciones que Claude Code lee al empezar cada sesión. No hace falta tocarlo |
| `docs/encargo.md` | Para qué sirve el taller y cuándo está bien hecha una entrega |
| `docs/estado.md` | Por dónde va un trabajo largo y qué queda pendiente |
| `docs/` | Su paleta Nocturne, las guías de Anki y de interfaz, lo que Claude aprende de una sesión a otra y, por cada complemento, qué hace y sus errores |
| `complementos/` | El código de cada complemento, una carpeta por complemento |
| `pruebas/` | Pruebas automáticas (las escribe Claude) |
| `herramientas/` | La comprobación general (`comprobar.py`) y el comprobador y empaquetador de complementos (`empaquetar.py`) |
| `paquetes/` | Los `.ankiaddon` entregados, con la versión en el nombre |
| `.claude/settings.json` | Permisos (qué puede hacer Claude sin preguntar, qué le debe preguntar y qué nunca) y comprobación automática al final de cada turno |
| `.github/workflows/comprobar.yml` | GitHub repite las comprobaciones en cada subida y guarda el `.ankiaddon` |

## El recorrido

```
claude.ai/code: elegir este repositorio y pedir lo que quiere
  -> Claude propone un plan en llano y espera su visto bueno
  -> Claude trabaja en una rama, lo comprueba y abre un pull request
  -> GitHub comprueba otra vez (marca verde) y guarda el .ankiaddon
  -> Usted lo descarga, lo instala en Anki y lo prueba
  -> Si está bien, fusiona el pull request («Merge pull request»)
```

## Primera vez: preparar el entorno de la nube (unos cinco minutos)

La nube no trae Anki. Hay que pegar una vez un script de preparación que lo instala (la misma versión que usa usted) junto con las herramientas de comprobación. El texto exacto y dónde pegarlo están en `docs/preparar-entorno.md`, apartado 1. Si se olvida, no pasa nada grave: Claude lo instala al empezar cada sesión, solo que tarda más.

## Trabajar con Claude Code

1. Entre en https://claude.ai/code o en la pestaña Code de la aplicación de Claude.
2. Debajo del cuadro de texto, elija este repositorio y el entorno con el script de preparación.
3. Pida lo que quiera. Ejemplos:
   - «Crea un complemento que me avise de las tarjetas con muchos fallos.»
   - «Corrige el complemento GritMap: el botón parpadea al abrir la ventana.»
4. Claude le propondrá un plan y esperará su visto bueno. Después trabajará en una rama, lo comprobará y le dará el enlace para descargar el `.ankiaddon` y los pasos para probarlo.
5. Si todo está bien, fusione el pull request en GitHub con «Merge pull request». Si no, dígale qué falla.

Use una sesión normal de Claude Code, no un hilo de un proyecto de Claude: en los hilos de proyecto solo se carga CLAUDE.md, y los permisos y la comprobación automática de `.claude/settings.json` no se aplican. El taller sigue funcionando, porque CLAUDE.md manda comprobar y GitHub lo repite, pero con una red de seguridad menos.

## Instalar lo que le entregue

1. Descargue el `.ankiaddon` desde el enlace que le dé Claude (botón de descarga de GitHub) o desde la pestaña Actions › la última ejecución en verde › Artifacts › «entrega» (viene comprimido: descomprímalo).
2. Haga doble clic en el `.ankiaddon` (o, en Anki, Herramientas › Complementos › «Instalar desde archivo…») y reinicie Anki. Si sustituye a uno que ya tenía, Anki lo reemplaza y conserva su configuración.
3. Para volver a la versión anterior, instale el paquete anterior de `paquetes/`.

## Para mejorar un complemento que ya tiene

En Anki, Herramientas › Complementos, seleccione el complemento y pulse «Ver archivos». En GitHub, abra la carpeta `complementos/` y use «Add file» › «Upload files» para subir esa carpeta entera. Después pídale los cambios a Claude. Si el nombre de la carpeta es un número, viene de AnkiWeb y es de otra persona: Claude se lo advertirá antes de tocarlo.

## Para gastar menos

- Una tarea por sesión. Para algo sin relación, empiece una sesión nueva o escriba `/clear`.
- Elija modelo y esfuerzo al principio y no los cambie a mitad de tarea: cada cambio de modelo obliga a releer toda la conversación sin descuento.
- Peticiones concretas: «añade un botón Exportar en la ventana de resultados» gasta menos que «mejóralo».
- Si Claude se equivoca dos veces en lo mismo, empiece de nuevo con una petición más precisa y pídale que anote la corrección en CLAUDE.md.
- En conversaciones largas, `/compact` con una indicación, por ejemplo: `/compact conserva el plan y los fallos pendientes`.

## Si algo falla

- La comprobación de GitHub sale en rojo (una cruz junto al commit): pídale a Claude «Arregla lo que falla en GitHub Actions».
- Aparece «Stop hook feedback»: es la comprobación automática avisando de un fallo; Claude lo corrige.
- Anki muestra una ventana de error al usar un complemento: copie el texto y péguelo a Claude; es la pista para arreglarlo.
- Para revisar si CLAUDE.md tiene instrucciones viejas o contradictorias: `/doctor prompt-audit`.
