# Errores de «Sonidos de consola»

Registro en lenguaje llano de los fallos de este complemento. Cada corrección del código (FIX-NNN)
tiene aquí su línea con el mismo número.

## Pendientes

(Ninguno.)

## Corregidos

- FIX-001 · 2026-11-13 · versión 1.0.1 · Qué pasaba: la 1.0.0 abría sus opciones en una ventana de
  controles estándar, distinta del panel que usan sus demás complementos. Por qué: se construyó con la
  guía anterior y la regla del panel modelo llegó a la rama principal a la vez. Regla: las opciones de
  todo complemento son una página del panel modelo, nunca una ventana de controles estándar.

## Así a propósito

- 1.0.0 · Los sonidos no van dentro del complemento: los copia la persona en su carpeta de sonidos.
  Decidido por la persona el 2026-11-13, porque parecen de una consola comercial y el repositorio es
  público.
- 1.0.0 · Responder tarjetas no suena (ni «Bien» ni «Fácil», ni los demás). Lo decidió la persona el
  2026-11-13.
- 1.0.0 · snd_system_ng suena al comenzar a estudiar y no en las preguntas de confirmación. Lo decidió
  la persona el 2026-11-13.
- 1.0.0 · El sonido usa directamente la parte de sonido de Qt que trae Anki (PyQt6.QtMultimedia), una
  excepción a la regla de usar Qt solo a través de Anki, aprobada por la persona el 2026-11-13: el
  reproductor de las tarjetas cortaría su audio y tiene retraso.
- 1.0.0 · Para saber cuándo se abre un menú, se cierra una ventana o aparece un globo, el complemento
  observa los eventos de la interfaz (Anki no tiene ganchos para eso). Solo mira seis tipos de evento
  y deja pasar el resto de inmediato; nunca bloquea ni cambia nada. Si una versión futura de Anki
  cambia cómo crea sus globos de notificación (hoy, una etiqueta «CustomLabel» de aqt.utils), el
  sonido del globo dejaría de sonar sin más; hay que revisarlo al cambiar Anki de versión.
- 1.0.0 · Cerrar una ventana cuenta como «cancelar» solo si la persona tocó esa ventana (tecla o clic)
  en las 0,6 segundos anteriores, o pulsó su X: así no suenan las ventanas de progreso que Anki cierra
  solo.
- 1.0.1 · El botón suelto «Abrir carpeta de sonidos» es el botón secundario del catálogo del panel
  modelo, añadido a la copia de este complemento como pieza «button»; el modelo no lo tenía como
  opción suelta. Los «Probar» de cada sonido se reúnen en una lista con su botón, como en ProFeedback.
- 1.1.0 · snd_system_ok suena solo al aceptar algo y ya no con la sincronización. Lo pidió la persona
  el 2026-11-13. Aceptar un error o un aviso no lo hace sonar, para no oír dos sonidos seguidos.
