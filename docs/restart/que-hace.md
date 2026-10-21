# Qué hace «Restart»

Versión 2.0.0 · 2026-10-21

Reinicia Anki con un atajo de teclado (combinación de teclas), por defecto Ctrl+R. El reinicio es un
cierre normal de Anki, el mismo que con Archivo > Salir: guarda la colección, sincroniza si usted
tiene activada la sincronización al cerrar y espera a que termine la copia de seguridad. Solo
cuando Anki ya está apagándose abre Anki otra vez, con el mismo perfil y la misma carpeta de datos.
No cambia nada de su colección. Lo único que guarda por su cuenta son sus dos opciones.

## 1. Dónde aparece

- En la ventana principal de Anki, el atajo de reinicio: funciona en la lista de mazos, en la
  pantalla de un mazo y durante el repaso.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones, no el editor de texto que Anki muestra con otros complementos.
- No añade menús, botones ni nada visible en las pantallas de Anki.
- El atajo no responde cuando hay otra ventana delante (Explorar, Añadir, Preferencias, su propia
  ventana de opciones o cualquier pregunta de Anki), ni en la ventana de elegir perfil.

## 2. El reinicio

Al pulsar el atajo:

1. Si Anki está en mitad de una tarea con barra de progreso, no reinicia y muestra unos segundos el
   aviso breve «Anki está ocupado ahora mismo. Espera a que termine e inténtalo de nuevo.».
2. Si no logra identificar con seguridad el programa de Anki, no cierra nada y muestra una ventana
   de aviso titulada «Restart»: «No se encontró el programa de Anki, así que no se puede reiniciar.
   Anki sigue abierto y no se ha perdido nada.».
3. Si todo está en orden, muestra un instante el aviso breve «Reiniciando Anki…» y empieza el
   cierre normal de Anki:
   - Cierra las ventanas abiertas (Explorar, Añadir, Editar…) como en cualquier cierre. Si en Añadir
     hay algo escrito, Anki pregunta, como siempre, si quiere descartarlo.
   - Si tiene activada la sincronización automática al abrir y cerrar, sincroniza al cerrar y otra
     vez al abrir. Si se están sincronizando archivos multimedia, espera a que terminen.
   - Hace la copia de seguridad automática de Anki si toca, según sus ajustes, y espera a que
     termine.
4. Cuando Anki ya ha guardado y cerrado la colección, abre Anki de nuevo con el mismo perfil y la
   misma carpeta de datos, sin pasar por la ventana de elegir perfil. Anki vuelve a la lista de
   mazos; las ventanas que tenía abiertas no se vuelven a abrir.

Si el cierre no sigue adelante (por ejemplo, porque en la pregunta de Añadir elige seguir editando),
Anki se queda abierto con normalidad y el reinicio se anula unos segundos después: como mucho cinco
desde la última comprobación. A partir de ahí puede volver a pulsar el atajo.

## 3. Límites y casos raros

- Repaso en curso: las respuestas que ya dio quedan guardadas. La tarjeta que tenía delante sin
  responder queda como estaba y Anki la volverá a enseñar cuando le toque. Tras el reinicio no se
  vuelve al repaso, sino a la lista de mazos.
- Pulsar el atajo varias veces seguidas no lanza varios reinicios: mientras hay uno en marcha, las
  pulsaciones de más no hacen nada. Dejar la tecla pulsada tampoco lo repite.
- Si el cierre tarda más de cinco minutos (por ejemplo, una sincronización muy larga), Anki se
  cierra pero no se vuelve a abrir: tendrá que abrirlo usted.
- Si usted cancela el cierre y, en los pocos segundos que tarda en anularse el reinicio, cierra Anki
  a mano, Anki se vuelve a abrir solo. Es un fallo anotado como pendiente.
- Windows, Mac y Linux: funciona igual en los tres. Para volver a abrir Anki usa el mismo programa
  con el que se abrió esta vez; si no lo identifica, lo busca junto a Anki y, por último, entre los
  programas instalados en el sistema. Solo acepta un programa cuyo nombre empiece por «anki»; en una
  instalación poco habitual en la que no lo encuentre, no cierra nada y muestra el aviso del punto 2
  del apartado 2.
- En Mac, «Ctrl» equivale a la tecla ⌘: el atajo por defecto es ⌘R.
- Anki se reabre en modo normal, con los complementos activos, aunque esta vez lo hubiera abierto
  en modo seguro (con Mayúsculas pulsada).
- Si otro complemento instalado usa la misma combinación en la ventana principal, ninguno de los dos
  responde. El complemento lo comprueba al abrir Anki y al guardar las opciones, pero no ve la
  combinación de un complemento que la ponga más tarde o solo durante el repaso: en ese caso el
  atajo no hace nada allí y el complemento solo lo anota en su registro, sin avisarle.

## 4. Ventana de opciones

- Título: «Restart». No tiene botón de ayuda. Se abre por encima de la ventana de complementos.
- Casilla «Activar atajo para reiniciar Anki»: marcada por defecto. Al desmarcarla, el campo del
  atajo queda en gris y, al aceptar, el atajo deja de funcionar al momento.
- Campo «Atajo:»: por defecto, Ctrl+R. Se rellena pulsando la combinación que quiera, que debe ser
  una sola (no una secuencia de varias). Tiene un botón pequeño para vaciarlo; si lo deja vacío y
  pulsa Aceptar, se conserva el atajo que ya estaba guardado.
- Botones Aceptar, Cancelar y el estándar para restaurar los valores predeterminados, con los textos
  de Qt en el idioma de Anki (en español, sí). Restaurar marca la casilla y pone Ctrl+R, pero no
  guarda nada hasta que pulse Aceptar. Cancelar cierra sin guardar.
- Aceptar comprueba la combinación (si la casilla está marcada). No se admite:
  - una tecla suelta o con solo Mayúsculas: debe llevar Ctrl o Alt (también vale la tecla Meta; en
    Mac, ⌘, ⌥ o Control);
  - una combinación que Anki ya usa en su ventana principal (por ejemplo Ctrl+Z, Ctrl+Q, Ctrl+P,
    Ctrl+E o Ctrl+Shift+A), contando también las de otros complementos instalados;
  - las de cerrar ventana: Ctrl+W en los tres sistemas (⌘W en Mac) y Ctrl+F4 en Windows y en algunos
    escritorios de Linux;
  - las del repaso con tecla modificadora: Ctrl+1 a Ctrl+7 (banderas), Ctrl+Alt+N, Ctrl+Alt+E,
    Ctrl+Alt+I, Ctrl+Shift+D, Ctrl+Supr y Ctrl+Retroceso (y dos variantes para teclado coreano).
  Si no se admite, muestra la ventana de aviso «Restart» con «No se puede usar «Ctrl+W». Elige una
  combinación que incluya Ctrl o Alt y que Anki no use ya.» (con la combinación que eligió) y la
  ventana de opciones sigue abierta para que elija otra.
- Si se admite, guarda, cierra la ventana y el nuevo atajo funciona al momento, sin reiniciar. No
  muestra mensaje de confirmación.

## 5. Al abrir Anki

Pone el atajo guardado en la ventana principal. Si esa combinación ya no se puede usar (por ejemplo,
porque viene de una versión anterior del complemento o porque otro complemento la ocupa ahora),
no la pone y muestra durante 6 segundos el aviso breve «No se puede usar «…». Elige una combinación
que incluya Ctrl o Alt y que Anki no use ya.». Para arreglarlo, elija otra en la ventana de opciones.

## 6. Qué guarda y dónde

- Sus dos opciones (casilla y atajo), en la configuración de complementos de Anki de ese ordenador:
  valen para todos los perfiles y no viajan con la sincronización.
- Si falta una opción o tiene un valor que no sirve (por ejemplo, retocado a mano), usa el valor
  por defecto.
- Si encuentra guardados los ajustes del antiguo atajo para cerrar Anki, de versiones anteriores,
  no los usa, y desaparecen la próxima vez que pulse Aceptar en las opciones.
- Un registro técnico, en un archivo de texto de la carpeta de registros de Anki (dentro de su
  carpeta de datos); Anki conserva los de los últimos diez días. Anota cada reinicio pedido (con el
  programa, la carpeta de datos y el nombre del perfil), los reinicios anulados o caducados, los
  atajos que no pudo poner y los fallos.
- No guarda nada en su colección.

## 7. Idiomas

Sus textos (la casilla, «Atajo:» y los avisos) están traducidos a los 55 idiomas que ofrece Anki,
y a seis más que Anki no ofrece; si faltara alguno, saldrían en inglés. Usa el idioma que tenga
Anki en ese momento. Los avisos en español tratan de tú («Espera…», «Elige…»). La combinación se
escribe con los nombres o símbolos de cada sistema. Los botones estándar salen en el idioma de Anki
cuando Qt trae esa traducción y, si no, en inglés.

## 8. Si algo falla

- Si falla algo al pulsar el atajo, al abrir Anki o al abrir las opciones, no sale la ventana de
  error de Anki: sale una ventana de aviso titulada «Restart» con «Ocurrió un error inesperado:»
  seguido del detalle técnico. Anki sigue funcionando y el detalle queda en el registro.
- Si el cierre ni siquiera llega a empezar, el reinicio se anula y Anki sigue abierto.
- Si en el último momento no logra abrir Anki de nuevo, Anki queda cerrado, sin haber perdido
  nada, y el motivo queda en el registro: ábralo usted como siempre.

## 9. Qué no hace

- No se conecta a internet.
- No cambia nada de su colección ni de sus tarjetas.
- No pide confirmación antes de reiniciar.
- No tiene atajo para cerrar Anki: para eso está Ctrl+Q de Anki.
- No añade entradas de menú ni botones; solo el atajo.
- No reabre las ventanas ni la pantalla en que estaba antes del reinicio.
