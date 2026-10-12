# Qué hace «GritMap»

Versión 3.1.1 · 2026-10-12

Mapa de calor de su estudio, como el de las contribuciones de GitHub: un cuadrito por día del año,
más oscuro cuanto más estudió ese día, y en gris los días que vienen, según las tarjetas que vencen.
Debajo, cinco cifras: promedio diario, días estudiados, retención, racha más larga y racha actual.
Solo lee su colección: nunca cambia tarjetas, notas ni repasos. Lo único que guarda son sus
opciones.

## 1. Dónde aparece

- En la lista de mazos (la pantalla principal), debajo de la lista, junto a la línea en la que Anki
  dice cuánto ha estudiado hoy. Ahí cuenta toda la colección, menos los mazos que usted excluya.
- En la pantalla de un mazo (la que tiene el botón «Comenzar a estudiar»), debajo de las cifras de
  tarjetas. Ahí cuenta solo ese mazo y sus submazos.
- En Herramientas > Complementos, al seleccionarlo y pulsar «Configuración», se abre su ventana de
  opciones.
- No aparece en el repaso, en Explorar, en las estadísticas ni en el editor. No añade menús.

## 2. El mapa

- Un año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes, con los nombres
  de los meses encima en el idioma de Anki.
- Días pasados y hoy: el color sale del tema elegido, en diez tonos. Sin estudio, el cuadrito queda
  en el gris de fondo. Los tonos se reparten según su promedio de siempre en los días que estudió
  (con un mínimo, para que al empezar no salga todo oscuro): desde un octavo del promedio hasta
  cuatro veces el promedio.
- Días futuros: en diez grises, según cuántas tarjetas vencen ese día. Lo atrasado no se dibuja.
- El cuadrito de hoy lleva un borde del color del texto. Las fechas clave llevan un borde naranja.
- Qué mide el color se elige en las opciones: repasos (cada respuesta cuenta una; no cuentan los
  cambios manuales de fecha ni las reprogramaciones), tarjetas (tarjetas distintas respondidas ese
  día) o nuevas (tarjetas que empezó a estudiar ese día). Con «Nuevas», un día estudiado sin ninguna
  nueva queda en gris.
- Si un mapa no cabe a lo ancho, se puede desplazar de lado.
- Si no hay nada que dibujar (ni repasos, ni vencimientos, ni fechas clave), dice «No hay datos de
  actividad para mostrar.».
- Mientras calcula muestra «…» en el hueco que ocupará el mapa, para que la pantalla no dé un salto.
  El cálculo se hace sin congelar Anki.

## 3. Al pasar el ratón por un día

Sale un globo con la cifra y la fecha larga en el idioma de Anki. En español:

- «**12** **repasos** el lunes, 12 de octubre de 2026» (o «1 repaso»).
- Con la medida «Tarjetas»: «**8** **tarjetas** el …».
- Con la medida «Nuevas»: «**3** **nuevas** el …», «**1** **nueva** el …» o «**Ninguna** **nueva** el …».
- Sin estudio: «**Ningún** **repaso** el …».
- Días futuros: «**30** tarjetas **pendientes** el …», «**1** tarjeta **pendiente** el …» o
  «**Ninguna** tarjeta **pendiente** el …».
- En una fecha clave, encima, con una estrella: el nombre (varios, separados por « · ») y, si no ha
  pasado, la cuenta atrás: «★ Examen mates (faltan 23 días)», «(falta 1 día)» o «(es hoy)».

## 4. Al pulsar un día

- Un día pasado con repasos abre Explorar con la búsqueda de las tarjetas respondidas ese día
  (prop:rated), limitada al mazo de la pantalla y sin los mazos excluidos. Se puede leer y retocar
  en la barra de búsqueda.
- Un día futuro con vencimientos abre Explorar con las tarjetas que vencen ese día (prop:due).
- Los días sin nada no responden al clic.

## 5. Los botones de encima del mapa

Cuatro botones pequeños con icono, con su nombre al pasar el ratón: «Retroceder» (año anterior),
«Hoy» (vuelve al año actual), «Avanzar» (año siguiente) y «Opciones». Retroceder y Avanzar se
apagan en el primer año con repasos y en el último con vencimientos o fechas clave. Se pueden
alcanzar con el tabulador. Debajo del mapa se escribe el año que se ve.

## 6. Las cifras de debajo

Cada cifra toma un tono del tema según lo buena que es; en gris si no hay dato.

- «Promedio diario:» lo hecho por día estudiado, en la unidad de la medida («85 repasos»,
  «60 tarjetas», «8 nuevas»), dentro de la ventana del promedio, contando solo días completos (la
  ventana termina ayer). Si no hay ningún día completo estudiado escribe «N/A» y, al pasar el ratón,
  «Sin días completos estudiados en los últimos 30 días» (o «… en todo el historial»). Con «Nuevas»,
  un promedio que se queda en 0 también es «N/A», con el globo «Menos de una nueva por día
  estudiado en los últimos 30 días».
- «Días estudiados:» porcentaje de días con estudio en esa ventana. Hoy cuenta solo si ya estudió, y
  la ventana no empieza antes de su primer repaso.
- «Retención:» porcentaje de respuestas que no fueron «Otra vez», con el criterio de la retención
  real de Anki (tarjetas con al menos un día de intervalo), en la misma ventana. Con menos de 20
  respuestas que contar escribe «N/A», con el texto de Anki.
- «Racha más larga:» el mayor número de días seguidos estudiando.
- «Racha actual:» días seguidos hasta hoy (no se rompe por no haber estudiado todavía hoy). Si la
  racha es cero, en su lugar dice «Última sesión: hace 3 días».

En la lista de mazos, si la opción está activada y estudió en la semana anterior, se añade junto a
la línea de Anki sobre lo estudiado hoy la comparativa de los 7 últimos días completos con los 7
anteriores: «▲ 15 repasos» en verde si sube, «▼ 15 repasos» en gris si baja, «● 0 repasos» si es
igual.

## 7. Ventana de opciones

Título «GritMap». Botones Aceptar, Cancelar y el estándar para restaurar los valores
predeterminados, con los textos de Qt en el idioma de Anki. Recuerda su tamaño y su posición. Al
aceptar, el mapa se redibuja en su sitio, sin recargar la pantalla.

| Opción | Valores | Por defecto |
|---|---|---|
| Tema de color | Azul océano, Naranja atardecer, Púrpura real, Rojo fuego, Rosa suave, Turquesa laguna, Verde clásico (con muestra de color del modo activo) | Verde clásico |
| El color mide | Repasos, Tarjetas, Nuevas | Repasos |
| Tamaño de celda (px) | 8 a 60 | 25 |
| Redondeo de esquinas (px) | 0 a 15 | 1 |
| Ventana del promedio | 7, 30, 90 o 365 días, o Todo el historial | 30 días |
| Excluir mazos | Botón «Seleccionar mazos» (o «2 mazo(s) excluido(s)», con los nombres al pasar el ratón) | Ninguno |
| Fechas clave | Botón «Gestionar fechas» (o «3 fecha(s) marcada(s)», con la lista al pasar el ratón) | Ninguna |
| Mostrar comparativa semanal | Casilla | Marcada |

Restaurar los valores predeterminados solo repone la apariencia: no toca los mazos excluidos ni las
fechas clave.

- Excluir mazos: lista de mazos con casillas, escalonada como en la pantalla principal (sin mazos
  filtrados ni el mazo predeterminado vacío). Excluir un mazo excluye sus submazos. Lo excluido no
  cuenta en ningún mapa: tampoco dentro del mapa de un mazo que lo contenga, y el mapa de un mazo
  excluido sale vacío.
- Fechas clave: lista «fecha corta — nombre»; un campo con el ejemplo «p. ej. Examen mates» (60
  caracteres como máximo), un selector de fecha con calendario (de 2000 a 2100; hoy por defecto) y
  los botones «Añadir» y «Eliminar» (este también con la tecla Supr). Intro añade. Avisos: «Escribe
  primero un nombre para la fecha.», «Esa fecha ya está en la lista.» y «Puedes añadir hasta 50
  fechas.».

## 8. Qué guarda y dónde

- La apariencia (tema, medida, tamaño, redondeo, ventana del promedio y comparativa), en la
  configuración de complementos de este ordenador: vale para todos los perfiles y no se sincroniza.
- Los mazos excluidos y las fechas clave, dentro de cada colección: cada perfil tiene los suyos y
  viajan con la sincronización. No se pueden deshacer desde Editar, porque son ajustes, no estudio.
- Si las encuentra guardadas como en versiones antiguas, las copia una vez a la colección.
- Un valor que falte o no sirva (por ejemplo, escrito a mano) se sustituye por el predeterminado.

## 9. Idiomas

Sus textos están en 51 idiomas; si el de Anki no está, sale en inglés. Las cifras, las fechas y los
nombres de los meses los escribe el propio Anki en su idioma. «N/A» y los botones Añadir y Eliminar
usan los textos de Anki.

## 10. Si algo falla

Nunca abre la ventana de error de Anki: el detalle queda en el registro del complemento y, en el
hueco del mapa, sale «No se pudo cargar el mapa de calor.». Anki sigue funcionando.

## 11. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No aparece en el repaso, en Explorar ni en las estadísticas.
