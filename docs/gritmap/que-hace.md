# Qué hace «GritMap»

Versión 3.5.0 · 2026-10-13

Mapa de calor de su estudio, como el de las contribuciones de GitHub: un cuadrito por día del año,
más oscuro (de día) o más luminoso (de noche) cuanto más estudió ese día, y en gris los días que
vienen, según las tarjetas que vencen. Debajo, cinco cifras: promedio diario, días estudiados,
retención, racha más larga y racha actual. Solo lee su colección: nunca cambia tarjetas, notas ni
repasos. Lo único que guarda son sus opciones.

## 1. Dónde aparece

- En la lista de mazos (la pantalla principal), debajo de la lista, junto a la línea en la que Anki
  dice cuánto ha estudiado hoy. Ahí cuenta toda la colección, menos los mazos que usted excluya.
- En la pantalla de un mazo (la que tiene el botón «Comenzar a estudiar»), debajo de las cifras de
  tarjetas. Ahí cuenta solo ese mazo y sus submazos.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones (la misma que el botón de opciones del mapa).
- No aparece en el repaso, en Explorar, en las estadísticas ni en el editor. No añade menús.

## 2. El mapa

- Encima del mapa, cuatro botones pequeños centrados (véase el apartado 5). Debajo del mapa, el año
  que se ve; al pasar el ratón por él (o llegar con el tabulador) dice lo hecho ese año en la unidad
  de la medida, con el signo de exclamación de cada idioma: «¡12.480 repasos!», «¡9.300 tarjetas!»
  o «¡850 nuevas!» (los días futuros no cuentan). A su derecha, los botones de periodo (véase el
  apartado 6).
- Un año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki y siempre con el calendario gregoriano.
- Días pasados y hoy: el color sale del tema elegido, en diez tonos. Sin estudio, el cuadrito queda
  en el gris de fondo. Los tonos se reparten según su promedio de siempre en los días que estudió
  (con un mínimo, para que al empezar no salga todo oscuro): desde un octavo del promedio hasta
  cuatro veces el promedio.
- Días futuros: en diez grises suaves, según cuántas tarjetas vencen ese día. Lo atrasado no se
  dibuja.
- El cuadrito de hoy lleva un borde del color del texto. Las fechas clave llevan un borde naranja;
  en los temas Rojo fuego, Naranja atardecer y Rosa suave, azul, porque el naranja no se distingue
  sobre ellos.
- Al pasar el ratón por un día, el cuadrito se resalta con un borde; si se puede pulsar, el puntero
  cambia a una mano.
- Qué mide el color se elige en las opciones: repasos (cada respuesta cuenta una; no cuentan los
  cambios manuales de fecha ni las reprogramaciones), tarjetas (tarjetas distintas respondidas ese
  día) o nuevas (tarjetas que empezó a estudiar ese día, también en los años anteriores al
  planificador actual de Anki). Con «Nuevas», un día estudiado sin ninguna nueva queda en gris.
- Si el mapa no cabe a lo ancho, se puede desplazar de lado. Al abrir un año se ve la semana de hoy;
  en un año pasado, diciembre, y en uno futuro, enero. Al redibujar el mismo año se conserva el
  desplazamiento. «Hoy» vuelve siempre a la semana de hoy.
- Si no hay nada que dibujar (ni repasos, ni vencimientos, ni fechas clave), en su lugar dice «No
  hay datos de actividad para mostrar.». En la pantalla de un mazo excluido dice «Este mazo está
  excluido del mapa.». En los dos casos queda el botón de opciones.
- Al pulsar uno de los botones de periodo tampoco se vuelve a calcular el mapa.
- La primera vez que se abre una pantalla muestra «…» en el hueco que ocupará el mapa, para que la
  pantalla no dé un salto. Después, cada vez que Anki vuelve a dibujar esa pantalla (al volver del
  repaso, sincronizar, deshacer, plegar un mazo o cada 10 minutos), se ve al instante el último mapa
  y se sustituye, sin hueco, si los datos al día son distintos.
- Cambiar de año o de tema, tamaño, redondeo, periodo o comparativa no vuelve a calcular el mapa: es
  inmediato. Cambiar la medida o los mazos excluidos sí lo recalcula, sin quitar el mapa mientras
  tanto. El cálculo se hace sin congelar Anki.
- En árabe, hebreo, persa y uigur, los botones y el mapa van de izquierda a derecha, como el
  calendario, y las cifras de debajo, de derecha a izquierda.

## 3. Al pasar el ratón por un día (o llegar a él con el teclado)

Sale un globo con la fecha larga en el idioma de Anki (sin «el»), en gris y algo más pequeña, y, en
la línea de abajo, lo hecho ese día. Es igual en todos los idiomas. La tecla Esc lo cierra. En
español:

- «lunes, 22 de junio de 2026» / «**12** **repasos**» (o «1 repaso»).
- Con la medida «Tarjetas»: «… / **9** **tarjetas**».
- Con la medida «Nuevas»: «… / **3** **nuevas**», «**1** **nueva**» o «**Ninguna** **nueva**».
- Sin estudio: «… / **Ningún** **repaso**».
- Días futuros: «… / **30** tarjetas **pendientes**», «**1** tarjeta **pendiente**» o «**Ninguna**
  tarjeta **pendiente**».
- En una fecha clave, encima de todo, con una estrella: el nombre (varios, separados por « · ») y,
  si no ha pasado, la cuenta atrás: «★ Examen de Anatomía (faltan 23 días)», «(falta 1 día)» o
  «(es hoy)».
- Las cifras de 1.000 o más llevan punto de millar.

## 4. Al pulsar un día

- Un día pasado con repasos abre Explorar con la búsqueda de las tarjetas respondidas ese día
  (prop:rated), limitada al mazo de la pantalla y sin los mazos excluidos. Se puede leer y retocar
  en la barra de búsqueda.
- Un día futuro con vencimientos abre Explorar con las tarjetas que vencen ese día (prop:due).
- Los días sin nada no responden al clic.
- Con el teclado, Intro o la barra espaciadora hacen lo mismo que el clic.

## 5. Los botones de encima del mapa

Cuatro botones pequeños con icono, centrados, con su nombre al pasar el ratón: «Año anterior»,
«Hoy» (vuelve al año actual y a la semana de hoy), «Año siguiente» y «Opciones». Retroceder y
avanzar se apagan en el primer año con repasos y en el último con vencimientos o fechas clave. Al
pulsarlos se hunden un instante (nada si Anki o el sistema piden reducir las animaciones).

Con el teclado: el tabulador llega a los botones y al mapa (a un solo día: hoy, o el 1 de enero en
otro año); dentro del mapa, las flechas arriba y abajo cambian de día y las flechas a los lados, de
semana; cada día dice en voz alta su globo a un lector de pantalla. Al cambiar de año con el teclado
el foco se queda en el botón pulsado (o en «Hoy», si ese botón se apaga).

## 6. Las cifras de debajo

Junto al año, tres botones para elegir el periodo de las cifras: «30 días», «1 año» y «Todo», sin
marco alrededor. El elegido lleva un fondo suave en forma de pastilla y letra en negrita; los demás
son texto gris que toma ese fondo al pasar el ratón. Al pulsar otro, las cifras cambian al momento y
la elección se guarda (es la misma opción «Periodo de las cifras» de la ventana de opciones). Al
pasar el ratón por ellos dice «Periodo de las cifras».

Debajo, las cinco cifras, centradas, en dos grupos separados por una raya fina: a la izquierda la
constancia («Racha actual», «Racha más larga» y «Días estudiados»), a la derecha el rendimiento
(«Promedio diario» y «Retención»). Si la ventana es estrecha, los grupos pasan a dos líneas. Cada
cifra va arriba: el número grande y en negrita, en el color del texto, con la unidad («días»,
«repasos», «%») más pequeña y en gris, y un cuadrito delante del tono del tema que le corresponde
según lo buena que es; su nombre va debajo, en gris. Sin dato, la cifra va en gris y sin cuadrito.
Los números tienen todos el mismo ancho, para que no bailen al cambiar.

Todas siguen la medida elegida: con «Repasos» y «Tarjetas», un día estudiado es un día con repasos;
con «Nuevas», solo un día en que empezó alguna tarjeta nueva. Así cambian el promedio, los días
estudiados, las dos rachas y la última sesión. La retención no depende de la medida.

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
- «Racha más larga»: el mayor número de días seguidos estudiando.
- «Racha actual»: días seguidos hasta hoy (no se rompe por no haber estudiado todavía hoy). Si la
  racha es cero, en su lugar dice «hace 3 días» con el nombre «Última sesión».

En la lista de mazos, si la opción está activada y estudió en la semana anterior, se añade junto a
la línea de Anki sobre lo estudiado hoy la comparativa de los 7 últimos días completos con los 7
anteriores: «▲ 15 repasos» en verde si sube, «▼ 15 repasos» en gris si baja, «● 0 repasos» si es
igual. Al pasar el ratón dice «Últimos 7 días frente a los 7 anteriores».

## 7. Ventana de opciones

Título «GritMap». Se abre después de leer los mazos y las opciones sin congelar Anki (un segundo clic
mientras tanto no abre otra). Botones Aceptar, Cancelar y el estándar para restaurar los valores
predeterminados, con los textos de Qt en el idioma de Anki; en los idiomas para los que Qt no trae
traducción, con los textos del complemento. Intro pulsa el botón que tiene el foco. Recuerda su
tamaño y su posición. Al aceptar, el mapa se redibuja en su sitio, sin recargar la pantalla.

| Opción | Valores | Por defecto |
|---|---|---|
| Tema de color | Azul océano, Naranja atardecer, Púrpura real, Rojo fuego, Rosa suave, Turquesa laguna, Verde clásico (con un cuadrito de muestra del tono del modo activo, que cambia si Anki pasa de día a noche) | Verde clásico |
| El color mide | Repasos, Tarjetas, Nuevas | Repasos |
| Tamaño de celda | 8 a 60 px | 25 px |
| Redondeo de esquinas | 0 a 15 px | 1 px |
| Periodo de las cifras | 30 o 365 días, o Todo el historial (vale para el promedio, los días estudiados y la retención; también se cambia con los botones junto al año). Si tenía 7 o 90 días, pasa a 30 | 30 días |
| Excluir mazos | Botón «Seleccionar mazos» (o «1 mazo excluido», «2 mazos excluidos», con hasta 15 nombres al pasar el ratón y «…» si hay más) | Ninguno |
| Fechas clave | Botón «Gestionar fechas» (o «1 fecha marcada», «3 fechas marcadas», con la lista al pasar el ratón) | Ninguna |
| Mostrar comparativa semanal | Casilla, en la columna de los campos | Marcada |

Restaurar los valores predeterminados solo repone la apariencia: no toca los mazos excluidos ni las
fechas clave.

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

Sus textos están en 51 idiomas; si el de Anki no está, sale en inglés. Cada cifra con unidad usa la
forma de plural de su idioma (por ejemplo, en ruso 1 день, 2 дня, 5 дней). Las cifras, los
porcentajes, las fechas y los nombres de los meses los escribe el
navegador de Anki en su idioma; en español, con punto de millar desde 1.000. «N/A», «Añadir»,
«Eliminar» y «Buscar» usan los textos de Anki.

## 10. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento (un archivo
de texto en la carpeta de registros del perfil de Anki) y, en el sitio del mapa, sale «No se pudo
cargar el mapa de calor.», con el botón de opciones. Anki sigue funcionando.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No aparece en el repaso, en Explorar ni en las estadísticas.
- No anima nada salvo el leve hundimiento de los botones al pulsarlos.
