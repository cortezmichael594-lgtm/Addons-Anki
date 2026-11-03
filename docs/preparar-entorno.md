# Preparar el entorno de trabajo

El taller trabaja en la nube (claude.ai/code). Cada sesión arranca en un ordenador temporal con Ubuntu 24.04 y Python 3.13 que no trae Anki: hay que instalar la misma versión que usa la persona, porque con ella se comprueban los nombres de la API y se ejecutan las pruebas, y una pieza gráfica del sistema (libegl1) sin la que Qt no arranca en Linux. Las versiones están fijadas en `requirements-anki.txt` (Anki) y `requirements-dev.txt` (ruff, mypy, pytest y PyYAML).

## 1. Script de preparación (lo pone la persona, una vez)

En claude.ai/code, en la pantalla de sesión nueva: selector de entorno (el primer control bajo el cuadro de texto) › pase el ratón por la fila del entorno y pulse el icono de ajustes de su derecha › «Setup script». Pegue este texto y guarde con «Save changes»:

```bash
#!/bin/bash
# Anki 26.09.3 y las herramientas del taller: mismas versiones que requirements-anki.txt y requirements-dev.txt.
apt-get update -q && apt-get install -y -q libegl1 || true
python -m pip install -q "aqt[qt]==26.9.3" ruff==0.17.3 mypy==2.4.1 pytest==9.2.0 pyyaml==6.0.3 || true
```

El script se ejecuta como administrador antes de la primera sesión y el resultado queda en caché (unos siete días), así que las sesiones siguientes arrancan con todo instalado. El acceso a la red de serie («Trusted») basta: incluye PyPI y los repositorios de Ubuntu. Los `|| true` evitan que un fallo de red impida abrir la sesión; en ese caso, la red de seguridad del apartado 2 lo instala.

No copie `"aqt[qt6]"`, aunque lo digan la guía oficial («Editor Setup») y la página de betas: ese extra no existe en aqt 26.9.3, pip solo avisa y deja PyQt6 sin fijar a la versión que trae Anki (APR-054).

## 2. Red de seguridad en cada sesión

`python herramientas/preparar.py` (en claude.ai/code lo lanza solo un gancho al empezar; en un hilo de proyecto, a mano) comprueba que lo instalado coincide con los requirements; si falta algo o tiene otra versión, lo instala con pip, y si falta libEGL, con apt-get. Después dice dónde está el código de Anki y lo pendiente según `empaquetar.py --revision`.

## 3. Comprobar

`python herramientas/empaquetar.py --autoprueba` debe terminar en «AUTOPRUEBA: CORRECTA». Esa prueba crea un complemento mínimo en una carpeta temporal y recorre todo el proceso (mypy, importación y empaquetado), así que confirma que el entorno y la herramienta funcionan. Si falla con «libEGL.so.1: cannot open shared object file», falta la pieza gráfica: `apt-get install -y libegl1`.

## 4. Resumen a la persona

En cuatro líneas como máximo: qué ha quedado preparado y qué falta, si falta algo.

## Anki ha cambiado de versión

La persona actualiza Anki con Herramientas › «Comprobar actualizaciones» (desde 26.05 descarga e instala la versión nueva); no con el botón del mismo nombre de la ventana Complementos, que solo actualiza complementos. Cuando diga que ha actualizado Anki a la versión X.Y.Z (Ayuda › «Acerca de Anki»):

1. Es un cambio de las reglas pedido por la persona (véase «Automejora» en `CLAUDE.md`): en tu rama, cambia `herramientas/version-anki.txt`, los datos de «Entorno» de `CLAUDE.md`, `requirements-anki.txt` y el script del apartado 1 (sin cero a la izquierda en el mes: 26.09.3 se escribe 26.9.3), y anótalo en «Cambios aprobados» de `docs/automejora.md`. Si PyPI aún no publica esa versión, díselo a la persona y espera.
2. Instala la versión nueva: `python herramientas/preparar.py`. Recuerda a la persona que actualice el script de preparación del entorno con el texto nuevo del apartado 1.
3. Lee las notas de esa versión en https://github.com/ankitects/anki/releases (desde la 23.12 están ahí y no en el manual) y apunta lo que afecte a los complementos.
4. Ejecuta `python herramientas/comprobar.py --todos --sin-paquete`, que revisa todos los complementos con `empaquetar.py`. Resume a la persona qué falla y arréglalo; cada arreglo lleva su nota FIX.
5. Ejecuta `python herramientas/empaquetar.py --revision`: señala los aprendizajes comprobados con la versión anterior. Vuelve a comprobar cada uno en el código nuevo y, según el caso, actualiza su versión, corrígelo o retíralo con su motivo.
