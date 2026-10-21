# Qué hace «GritMap»

Versión 3.6.0 · 2026-10-21

Mapa de calor de su estudio, como el de las contribuciones de GitHub: un cuadrito por día del año,
más oscuro (de día) o más luminoso (de noche) cuanto más estudió ese día, y en gris los días que
vienen, según las tarjetas que vencen. Debajo del mapa, una leyenda que dice qué cifra representa
cada tono, y después cinco cifras en dos grupos: las rachas (actual y más larga) y, bajo el selector
de periodo, el promedio diario, los días estudiados y la retención. Solo lee su colección: nunca
cambia tarjetas, notas ni repasos. Lo único que guarda son sus opciones.

## 1. Dónde aparece

- En la lista de mazos (la pantalla principal), debajo de la lista, junto a la línea en la que Anki
  dice cuánto ha estudiado hoy. Ahí cuenta toda la colección, menos los mazos que usted excluya.
- En la pantalla de un mazo (la que tiene el botón «Comenzar a estudiar»), debajo de las cifras de
  tarjetas. Ahí cuenta solo ese mazo y sus submazos.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones (la misma que el botón de opciones del mapa), delante de la ventana Complementos.
- No aparece en el repaso, en Explorar, en las estadísticas ni en el editor. No añade menús.

## 2. El mapa

- Encima del mapa, cuatro botones pequeños centrados (véase el apartado 5). Debajo de los botones,
  si hay alguna fecha clave por venir, una línea con la próxima (véase «La próxima fecha clave»).
- Debajo del mapa, a la izquierda, el año que se ve; al pasar el ratón por él (o llegar con el
  tabulador) dice lo hecho ese año en la unidad de la medida, con el signo de exclamación de cada
  idioma: «¡12.480 repasos!», «¡9.300 tarjetas!» o «¡850 nuevas!» (los días futuros no cuentan). A
  la derecha, la leyenda (véase más abajo). Si no caben en una línea, la leyenda pasa a la de abajo.
  El mapa y esa fila tienen el mismo ancho, así que la leyenda queda alineada con el borde derecho
  del mapa.
- Un año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki y siempre con el calendario gregoriano.
- Días pasados y hoy: el color sale del tema elegido, en diez tonos. Sin estudio, el cuadrito queda
  en el gris de fondo. Los tonos se reparten según su promedio de siempre en los días que estudió
  (con un mínimo, para que al empezar no salga todo oscuro): desde un octavo del promedio hasta
  cuatro veces el promedio.
- Días futuros: en diez grises suaves, según cuántas tarjetas vencen ese día. Lo atrasado no se
  dibuja.
- El cuadrito de hoy lleva un borde del color del texto. Las fechas clave llevan un borde naranja
  (el de la bandera naranja de Anki); en los temas Rojo fuego, Naranja atardecer y Rosa suave, azul
  (el de la bandera azul), porque el naranja no se distingue sobre ellos.
- Al pasar el ratón por un día, el cuadrito se resalta con un borde; si se puede pulsar, el puntero
  cambia a una mano y el globo lo dice en su última línea (véase el apartado 3).
- Qué mide el color se elige en las opciones: repasos (cada respuesta cuenta una; no cuentan los
  cambios manuales de fecha ni las reprogramaciones), tarjetas (tarjetas distintas respondidas ese
  día) o nuevas (tarjetas que empezó a estudiar ese día, también en los años anteriores al
  planificador actual de Anki). Con «Nuevas», un día estudiado sin ninguna nueva queda en gris.
- Si el mapa no cabe a lo ancho, se puede desplazar de lado. Al abrir un año se ve la semana de hoy;
  en un año pasado, diciembre, y en uno futuro, enero. Al redibujar el mismo año se conserva el
  desplazamiento. «Hoy» vuelve siempre a la semana de hoy.
- La primera vez que se abre una pantalla muestra «…» en el hueco que ocupará el mapa, para que la
  pantalla no dé un salto. Después, cada vez que Anki vuelve a dibujar esa pantalla (al volver del
  repaso, sincronizar, deshacer, plegar un mazo o cada 10 minutos), se ve al instante el último mapa
  y se sustituye, sin hueco, si los datos al día son distintos.
- Cambiar de año o de tema, tamaño, redondeo, periodo o comparativa no vuelve a calcular el mapa: es
  inmediato. Cambiar la medida o los mazos excluidos sí lo recalcula, sin quitar el mapa mientras
  tanto. El cálculo se hace sin congelar Anki.
- En árabe, hebreo, persa y uigur, los botones, el mapa y la fila del año con la leyenda van de
  izquierda a derecha, como el calendario, y las cifras de debajo, de derecha a izquierda.

### La leyenda

- «Menos», seis cuadritos y «Más», seguidos de la medida activa: «· repasos», «· tarjetas» o
  «· nuevas». Los cuadritos llevan el redondeo de esquinas elegido (hasta 4 px, para que se vean
  como cuadritos).
- El primero es el gris de los días sin estudio; al pasar el ratón dice «Ningún repaso» (con
  «Nuevas», «Ninguna nueva»). Los otros cinco llevan los tonos 2, 4, 6, 8 y 10 del tema: los diez
  tonos del mapa se agrupan de dos en dos y cada cuadrito muestra el más intenso de su pareja. Al
  pasar el ratón, cada uno dice las cifras que cubre, calculadas con su promedio actual: «de 1 a 10
  repasos», «de 11 a 30 repasos», …, y el último «81 repasos o más». Si un grupo cubre una sola
  cifra, la escribe sola («3 nuevas»). Un lector de pantalla lee esos mismos textos.
- Después, unas muestras con su nombre, solo si eso sale en el año que se ve: «Pendientes» (un gris
  de días futuros), «Hoy» (un cuadrito con el borde de hoy) y «Fecha clave» (un cuadrito con el borde
  de las fechas clave).

### La próxima fecha clave

- Si hay una fecha clave hoy o más adelante, bajo los cuatro botones aparece una línea discreta, en
  gris, con una estrella naranja (o azul en los temas cálidos): «★ Examen de Anatomía · faltan 23
  días», «· falta 1 día» o «· es hoy». Si ese día hay varias, sus nombres van separados por « · ».
  Si no hay ninguna por venir, la línea no existe.
- Es un botón: al pulsarlo (o con Intro o la barra espaciadora), el mapa pasa al año de esa fecha,
  la centra si el mapa no cabe a lo ancho y le da el foco, de modo que se abre su globo con el
  nombre y la cuenta atrás.

### Cuando no hay nada que dibujar

- En una colección sin repasos, sin vencimientos y sin fechas clave, se ve igualmente la cuadrícula
  del año actual en gris, con hoy marcado, el año debajo (sin globo) y la frase «Cada día que
  estudie se pintará aquí.». No hay leyenda ni cifras. Los botones de año están apagados; «Hoy» y
  «Opciones» funcionan.
- En la pantalla de un mazo excluido dice «Este mazo está excluido del mapa.» y, a continuación, el
  enlace «Cambiar mazos excluidos», que abre la ventana de opciones y, sobre ella, la lista de mazos
  excluidos. Queda también el botón de opciones.

## 3. Al pasar el ratón por un día (o llegar a él con el teclado)

Sale un globo con la fecha larga en el idioma de Anki (sin «el»), en gris y algo más pequeña, y, en
la línea de abajo, lo hecho ese día. Si el día se puede pulsar, una última línea en gris lo dice. Es
igual en todos los idiomas. La tecla Esc lo cierra. En español:

- «lunes, 22 de junio de 2026» / «**12** **repasos**» (o «1 repaso») / «Pulse para ver estas
  tarjetas».
- Con la medida «Tarjetas»: «… / **9** **tarjetas**».
- Con la medida «Nuevas»: «… / **3** **nuevas**», «**1** **nueva**» o «**Ninguna** **nueva**».
- Sin estudio: «… / **Ningún** **repaso**», sin línea de pulsar.
- Días futuros: «… / **30** tarjetas **pendientes**», «**1** tarjeta **pendiente**» o «**Ninguna**
  tarjeta **pendiente**»; los que tienen tarjetas llevan «Pulse para ver las que vencen ese día».
- En una fecha clave, encima de todo, con una estrella: el nombre (varios, separados por « · ») y,
  si no ha pasado, la cuenta atrás: «★ Examen de Anatomía (faltan 23 días)», «(falta 1 día)» o
  «(es hoy)».
- Las cifras de 1.000 o más llevan punto de millar.
- Un lector de pantalla lee el mismo texto, línea de pulsar incluida.

## 4. Al pulsar un día

- Un día pasado con repasos abre Explorar con la búsqueda de las tarjetas respondidas ese día
  (prop:rated), limitada al mazo de la pantalla y sin los mazos excluidos. Se puede leer y retocar
  en la barra de búsqueda.
- Un día futuro con vencimientos abre Explorar con las tarjetas que vencen ese día (prop:due).
- Los días sin nada no responden al clic.
- Con el teclado, Intro o la barra espaciadora hacen lo mismo que el clic.

## 5. Los botones de encima del mapa

Cuatro botones pequeños con icono, centrados y separados por un hueco de 8 px, con su nombre al
pasar el ratón: «Año anterior», «Hoy» (vuelve al año actual y a la semana de hoy), «Año siguiente» y
«Opciones». Al pasar el ratón toman un fondo y un borde algo más marcados. Retroceder y avanzar se
apagan en el primer año con repasos y en el último con vencimientos o fechas clave. Al pulsarlos se
hunden un instante (nada si Anki o el sistema piden reducir las animaciones).

Con el teclado: el tabulador llega a los botones, a la línea de la próxima fecha clave y al mapa (a
un solo día: hoy, o el 1 de enero en otro año); el botón o el día que tiene el foco lleva un contorno
azul, que solo se ve con el teclado, nunca al hacer clic. Dentro del mapa, las flechas arriba y
abajo cambian de día y las flechas a los lados, de semana; cada día dice en voz alta su globo a un
lector de pantalla. Al cambiar de año con el teclado el foco se queda en el botón pulsado (o en
«Hoy», si ese botón se apaga).

## 6. Las cifras de debajo

Cinco cifras, centradas, en dos grupos separados por espacio. Cada grupo lleva una cabecera a la
misma altura:

- A la izquierda, «Rachas» (rótulo pequeño en gris), con «Racha actual» y «Racha más larga». No
  dependen del periodo.
- A la derecha, los tres botones del periodo, «30 días», «1 año» y «Todo», sin marco alrededor,
  justo encima de las tres cifras que cambian: «Promedio diario», «Días estudiados» y «Retención».
  El periodo elegido lleva el fondo azul suave de selección de Anki en forma de pastilla y letra en
  negrita; los demás son texto gris que toma un fondo suave al pasar el ratón. Al pulsar otro, las
  cifras cambian al momento y la elección se guarda (es la misma opción «Periodo de las cifras» de
  la ventana de opciones). Al pasar el ratón por ellos dice «Periodo de las cifras».

Si la ventana es estrecha, los grupos pasan a dos líneas. Cada cifra va arriba: el número grande y
en negrita, en el color del texto, con la unidad («días», «repasos», «%») más pequeña y en gris, y un
cuadrito delante del tono del tema que le corresponde según lo buena que es; su nombre va debajo, en
gris, y en dos de ellas, una nota más abajo (véase la racha). Sin dato, la cifra va en gris y sin
cuadrito. Los números tienen todos el mismo ancho, para que no bailen al cambiar.

Todas siguen la medida elegida: con «Repasos» y «Tarjetas», un día estudiado es un día con repasos;
con «Nuevas», solo un día en que empezó alguna tarjeta nueva. Así cambian el promedio, los días
estudiados, las dos rachas, sus notas y la última sesión. La retención no depende de la medida.

- «Racha actual»: días seguidos hasta hoy (no se rompe por no haber estudiado todavía hoy). Debajo
  de su nombre, una nota en gris: «hoy pendiente» mientras hoy no cuenta todavía y «hoy hecho» en
  cuanto cuenta. Si la racha es cero, en su lugar dice «hace 3 días» con el nombre «Última sesión»,
  sin nota.
- «Racha más larga»: el mayor número de días seguidos estudiando. Con una racha actual en marcha,
  lleva una nota cuando el récord está cerca: «a 3 días de igualarla» si le faltan de 1 a 7 días
  para igualarla. El día en que la racha actual supera la mejor racha anterior (que fuera de 1 día o
  más) y hoy ya cuenta, la nota dice «nuevo récord»; al día siguiente desaparece. Lejos del récord
  no hay nota.
- «Promedio diario»: lo hecho por día estudiado, en la unidad de la medida («85 repasos»,
  «60 tarjetas», «8 nuevas»), dentro del periodo de las cifras, contando solo días completos (el
  periodo termina ayer). Si no hay ningún día completo estudiado escribe «N/A» y, al pasar el ratón
  (o al llegar con el tabulador), «Sin días completos estudiados en los últimos 30 días» (o «… en
  todo el historial»). Con «Nuevas», un promedio que se queda en 0 también es «N/A», con el globo
  «Menos de una nueva por día estudiado en los últimos 30 días».
- «Días estudiados»: porcentaje de días con estudio en ese periodo, escrito a la manera del idioma
  («77 %»). Hoy cuenta solo si ya estudió, y el periodo no empieza antes de su primer repaso.
- «Retención»: porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención
  real de Anki (tarjetas con al menos un día de intervalo), en el mismo periodo. Con menos de 20
  respuestas que contar escribe «N/A», con el texto de Anki.

### La comparativa semanal

En la lista de mazos, si la opción está activada y estudió en la semana anterior, se añade, junto a
la línea de Anki sobre lo estudiado hoy, una frase en gris con lo hecho en los 7 últimos días
completos (terminan ayer) y su diferencia con los 7 anteriores: «· 102 repasos en 7 días · ▲ 15 más
que los 7 anteriores». Solo la diferencia cambia de color: en verde si sube; si baja, «▼ 15 menos que
los 7 anteriores», en gris; si es igual, «● igual que los 7 anteriores», en gris. Al pasar el ratón
dice «Últimos 7 días frente a los 7 anteriores».

## 7. Ventana de opciones

Título «GritMap». Se abre después de leer los mazos y las opciones sin congelar Anki (un segundo clic
mientras tanto no abre otra), delante de la ventana desde la que se pidió (la principal o la de
Complementos; si esta se cerró entretanto, delante de la principal). Botones «Restaurar apariencia»
(a la izquierda), Aceptar y Cancelar; los dos últimos con los textos de Qt en el idioma de Anki y, en
los idiomas para los que Qt no trae traducción, con los textos del complemento. Intro pulsa el botón
que tiene el foco. Recuerda su tamaño y su posición. Al aceptar, el mapa se redibuja en su sitio, sin
recargar la pantalla.

| Opción | Valores | Por defecto |
|---|---|---|
| Tema de color | Azul océano, Naranja atardecer, Púrpura real, Rojo fuego, Rosa suave, Turquesa laguna, Verde clásico (con un cuadrito de muestra del tono del modo activo, que cambia si Anki pasa de día a noche) | Verde clásico |
| El color mide | Repasos, Tarjetas, Nuevas; debajo, una frase que dice qué cuenta: «Cada respuesta cuenta una», «Cada tarjeta cuenta una vez por día» o «Solo las tarjetas que empezó ese día» | Repasos |
| Tamaño de celda | 8 a 60 px | 25 px |
| Redondeo de esquinas | 0 a 15 px | 1 px |
| Vista previa | Una tira con el gris de los días sin estudio y los diez tonos del tema, al tamaño y con el redondeo elegidos; cambia al momento al mover el tema, el tamaño o el redondeo, y también al pasar Anki de día a noche. Si los cuadritos son grandes, se ven los que caben | — |
| Periodo de las cifras | 30 o 365 días, o Todo el historial (vale para el promedio, los días estudiados y la retención; también se cambia con los botones sobre esas cifras). Si tenía 7 o 90 días, pasa a 30 | 30 días |
| Excluir mazos | Botón «Seleccionar mazos» (o «1 mazo excluido», «2 mazos excluidos», con hasta 15 nombres al pasar el ratón y «…» si hay más) | Ninguno |
| Fechas clave | Botón «Gestionar fechas» (o «1 fecha marcada», «3 fechas marcadas», con la lista al pasar el ratón) | Ninguna |
| Mostrar comparativa semanal | Casilla, en la columna de los campos | Marcada |

«Restaurar apariencia» solo repone la apariencia; al pasar el ratón dice «No cambia los mazos
excluidos ni las fechas clave». La vista previa ocupa siempre el alto del cuadrito más grande (60
px), para que la ventana no cambie de tamaño al mover el control.

- Excluir mazos: árbol de mazos con casillas, como en la pantalla principal (sin mazos filtrados ni
  el mazo predeterminado vacío), con un buscador encima («Buscar», el texto de Anki) que deja a la
  vista los mazos cuyo nombre contiene lo escrito, con sus mazos padre. Marcar un mazo marca y
  bloquea (en gris) sus submazos, porque quedan excluidos con él; al desmarcarlo, cada submazo
  vuelve a su propia casilla. Lo excluido no cuenta en ningún mapa: tampoco dentro del mapa de un
  mazo que lo contenga. Solo se cuentan y se nombran mazos que existen; los que ya no existen se
  dejan de guardar al aceptar. Un mazo filtrado excluido a mano en la configuración se conserva.
- Fechas clave: lista en dos columnas, fecha corta (con el año en cuatro cifras) y nombre; encima de
  los campos, el botón «Eliminar» a la derecha (o la tecla Supr con el foco en la lista; tras
  borrar queda seleccionada la siguiente). Debajo, un campo con el ejemplo «p. ej., examen de
  Matemáticas» (60 caracteres como máximo, con el cursor ya puesto al abrir), un selector de fecha
  con calendario (de 2000 a 2100; hoy por defecto) y el botón «Añadir». Intro en el campo añade.
  Avisos: «Falta el nombre de la fecha.», «Esa fecha con ese nombre ya está en la lista.» y «Caben
  hasta 50 fechas.».

## 8. Qué guarda y dónde

- La apariencia (tema, medida, tamaño, redondeo, periodo de las cifras y comparativa), en la
  configuración de complementos de este ordenador: vale para todos los perfiles y no se sincroniza.
- Los mazos excluidos y las fechas clave, dentro de cada colección: cada perfil tiene los suyos y
  viajan con la sincronización. Se leen de la colección cada vez, así que lo que llega al sincronizar
  se ve en el siguiente dibujado y en Opciones. No se pueden deshacer desde Editar, porque son
  ajustes, no estudio.
- Si las encuentra guardadas como en versiones antiguas, las copia una vez a cada perfil que aún no
  las tenga. Cuando esas copias antiguas quedan vacías, se borran al guardar las opciones.
- Un valor que falte o no sirva (por ejemplo, escrito a mano) se sustituye por el predeterminado.

## 9. Idiomas

Sus textos están en 51 idiomas, también los nuevos de la 3.6.0; si el de Anki no está, sale en
inglés. Cada cifra con unidad usa la forma de plural de su idioma (por ejemplo, en ruso 1 день,
2 дня, 5 дней). Las cifras, los porcentajes, las fechas y los nombres de los meses los escribe el
navegador de Anki en su idioma; en español, con punto de millar desde 1.000. «N/A», «Añadir»,
«Eliminar» y «Buscar» usan los textos de Anki.

## 10. Colores

Todo lo que no es la escala del tema sale de los colores de Anki, que la paleta Nocturne redefine,
con su pareja de día y de noche: textos y grises (texto y texto suave), botones (fondo, fondo al
pasar el ratón, borde y borde al pasar el ratón), periodo elegido (fondo de selección), contorno de
foco (azul de foco), globo (fondo de capa superior y borde), enlace «Cambiar mazos excluidos» (color
de enlace), subida de la comparativa (verde del sistema) y fechas clave (banderas naranja y azul).
Los días sin estudio usan el gris de borde suave, que se distingue del fondo de día y de noche. Las
siete escalas de los temas y los grises de los días futuros son colores propios (véase «Así a
propósito» en errores).

## 11. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento (un archivo
de texto en la carpeta de registros del perfil de Anki) y, en el sitio del mapa, sale «No se pudo
cargar el mapa de calor.», con el botón de opciones. Anki sigue funcionando.

## 12. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No aparece en el repaso, en Explorar ni en las estadísticas.
- No anima nada salvo el leve hundimiento de los botones al pulsarlos.
- No avisa ni mete prisa para no perder la racha: las notas de la racha solo informan.
