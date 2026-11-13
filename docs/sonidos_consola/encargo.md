# Encargo: Sonidos de consola

Fecha: 2026-11-13 · Estado: aprobado

## Objetivo
Que Anki suene como el menú de una consola (estilo PS3) al usarlo, con los ocho sonidos que tiene la
persona y una barra de volumen.

## Qué hará
1. coldboot_stereo al abrir Anki; gameboot_stereo con cada globo de notificación; snd_option al navegar
   por los menús (pasar el ratón o las flechas, o solo al hacer clic; para silenciarla, su casilla); snd_cancel al
   cancelar, cerrar un menú sin elegir, pulsar la X, Esc o «Cancelar» y al salir del estudio a mitad;
   snd_system_ok solo al aceptar algo («Aceptar» o «Sí»; cambio pedido el 2026-11-13, sin sincronización); snd_system_ng al
   comenzar a estudiar; snd_trophy al terminar un mazo (1.2.0); snd_error con los avisos y errores de Anki.
2. Sin solaparse: un altavoz por sonido que se reinicia, navegación con un mínimo de 60 ms entre tics
   y prioridad de cancelar, error, ok y ng sobre la navegación y el globo.
3. Ventana en Herramientas > Complementos > Configuración (sin entrada en Herramientas desde la 1.2.0): barra de volumen, una casilla y un botón «Probar»
   por sonido, modo de navegación y «Abrir carpeta de sonidos».

## Criterios de aceptación
- [ ] `comprobar.py` acaba en «Comprobación correcta».
- [ ] Cada sonido suena en su momento y no se pisan (pendiente de probar por la persona en Windows).
- [ ] El volumen y las casillas se guardan y se respetan.
- [ ] Sin sonido al responder tarjetas.

## Fuera del alcance
- Sonidos distintos de los ocho de la persona, incluidos en el paquete.
- Sonar al pasar el ratón por la lista de mazos o por las páginas de Anki.

## Datos y seguridad
No lee ni cambia la colección. Solo guarda sus opciones en la configuración del complemento.

## Preguntas abiertas
- Ninguna.
