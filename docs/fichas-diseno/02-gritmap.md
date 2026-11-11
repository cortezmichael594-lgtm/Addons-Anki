# Ficha de diseño: GritMap

Versión 4.16.0 (11 de noviembre de 2026). Léase junto con `00-contexto-comun.md`.

## 1. Qué es, en una frase

Un mapa de calor del estudio: un cuadrito por cada día del año, más intenso cuanto más se estudió, y
en gris los días que vienen según las tarjetas que vencen; debajo, de una a cinco tarjetas pequeñas
con cifras («Hoy», «Racha», «Promedio diario», «Retención» y «Próxima fecha»). Se parece al mapa de
contribuciones de GitHub.

## 2. Para quién y para qué

Para ver de un vistazo la constancia (qué días se estudió y cuánto), mantener el hábito con una racha
y una meta diaria, y anticipar la carga de los próximos días y las fechas clave (exámenes). Solo lee la
colección: nunca cambia tarjetas, notas ni repasos. Guarda sus opciones y, cada día con meta, si se
cumplió.

Principios que guían su diseño (decididos con la persona): cada color tiene una sola función (el
tema es «estudio», el gris vacío «no estudio», el azul de Anki «se puede pulsar o está elegido»); lo
que viene pesa a la vista menos que lo hecho; nada de premios, avisos ni notificaciones: lo que cambia
se ve donde ocurre; nada de paneles de ceros el primer día.

## 3. Dónde se ve

- Lista de mazos (pantalla principal): debajo de la lista, junto a la línea «Estudiadas N tarjetas
  en…». Cuenta toda la colección menos los mazos excluidos.
- Pantalla de un mazo: debajo de las cifras de tarjetas. Cuenta solo ese mazo y sus submazos. Si el
  mazo está excluido, en su lugar: «Este mazo está excluido del mapa.» con el botón de opciones.
- Herramientas > Complementos > GritMap > Configuración: abre la ventana de opciones (la misma que el
  botón del mapa).
- No aparece en el repaso, Explorar, estadísticas ni editor. No añade menús.

## 4. Composición general

De arriba abajo, dentro del ancho de la lista de mazos:

1. Tarjeta del mapa (un recuadro):
   - Arriba, centrado: «‹ 2026 ›» (flechas de año; sin más años, en FG_DISABLED). En la esquina,
     botón de opciones de 28 px (icono de deslizadores de 16 px, nombre «Opciones»).
   - Encima de la rejilla, los meses; a la izquierda, las iniciales del lunes, miércoles y viernes.
   - La rejilla: columnas de semanas que empiezan en lunes, de enero a diciembre, siempre calendario
     gregoriano.
   - Pie: a la izquierda, como mucho una línea de sorpresa; a la derecha, la leyenda.
2. Debajo, una fila de tarjetas de cifras del mismo ancho, que suman exactamente el ancho del mapa
   (simetría): de dos en dos en ventanas estrechas y de una en una en muy estrechas.

Medidas y ritmo:

- Espacios de 4, 8, 16 y 32 px.
- Dos tamaños de letra: 20 px para el dato de cada tarjeta y 12 px para casi todo lo demás (13 px en la
  línea gris de las tarjetas y en el globo). La jerarquía va con el grosor (400 y 600) y el gris.
- Misma letra que Anki.
- Esquina del mapa y de las tarjetas: la de los recuadros de Anki, 12 px, o la de la paleta de Atelier
  (12 px en Nocturne, Papel y Lavanda; 16 px en Bosque y Atardecer), igual que la lista de mazos que
  tienen encima.
- Mapa y tarjetas: fondo CANVAS_ELEVATED, borde fino BORDER_SUBTLE y sombra suave de día (0 1px 3px
  SHADOW_SUBTLE); de noche, sin sombra.
- Cuadrito: 24 px y redondeo de 3 px de serie (ajustables). Con «Ajustado al ancho», el mapa ocupa
  todo el ancho y los cuadritos miden al menos 10 px.
- Si el año no cabe a lo ancho, el mapa se desplaza de lado: el borde por donde sigue se desvanece y,
  al abrirlo, se ve la semana de hoy (en un año pasado, su final; en uno futuro, su principio).

## 5. El mapa: qué significa cada cuadrito

| Estado del día | Aspecto |
|---|---|
| Pasado u hoy con estudio | Uno de los cuatro tonos del tema, según tarjetas distintas respondidas. Cortes a partir del promedio propio: hasta la mitad, hasta el promedio, hasta el doble, más del doble |
| Sin estudio, desde el primer repaso | Gris vacío (BORDER_SUBTLE de día, CANVAS_INSET de noche); en la leyenda, bajo «menos» |
| Anterior al primer repaso, o futuro sin pendientes | «Sin dato»: mezcla al 50 % del gris vacío y el fondo de la tarjeta, aún más apagado. No tiene cuadrito en la leyenda: es fondo, no información |
| Futuro con tarjetas que vencen | Tres grises según la carga (hasta la mitad de lo normal, hasta vez y media, más). Salen de mezclar el color del texto con el de la tarjeta: de día 16, 21 y 26 % de texto; de noche 10, 15 y 19 %. Así toman el matiz de la paleta de Atelier (cálidos en Atardecer, verdosos en Bosque, lilas en Lavanda). Con Nocturne: de día #D8DEE8, #CDD3DD, #C2C8D2; de noche #343A44, #3C424C, #434953 |
| Hoy | Borde del color del texto |
| Cubierto (comodín o pausa de la racha) | Vacío, con borde fino discontinuo |
| Fecha clave | Rombo dentro del cuadrito: lleno en el color del texto si es hoy o futura; hueco y gris si ya pasó |

Los grises de pendientes son más suaves que el primer tono de cualquier tema en todas las
combinaciones salvo una: Atardecer de noche con el tema Rosa suave (1,66 frente a 1,59 a 1 sobre la
tarjeta); ahí se distinguen por el color y por el sitio (pendientes solo en el futuro, estudio solo en
el pasado, con hoy entre medias).

### Temas de color del estudio

Seis temas; cuatro tonos cada uno, con la misma luminosidad percibida en todos (OKLCH 0,80, 0,67,
0,54 y 0,41 de día; 0,42, 0,56, 0,70 y 0,84 de noche). De día, más estudio es más oscuro; de noche,
más claro: siempre más estudio es más contraste con el fondo. Cada tono se distingue del vecino
(salto de 1,5 a 1,9 veces en luminosidad).

| Tema | Día (tono 1 → 4) | Noche (tono 1 → 4) |
|---|---|---|
| Verde clásico (de serie) | #95CF96, #5DAA61, #2D8336, #0E5A1A | #335735, #4C844F, #6CB26F, #9DDE9E |
| Azul océano | #8CC3FC, #519AE2, #1B71BC, #004C86 | #2E5072, #4378AD, #61A3E6, #A2CFFF |
| Púrpura real | #C7AFF5, #A281D9, #7C58B3, #553781 | #53446E, #7E66A6, #AA8DDE, #D3BDFE |
| Naranja atardecer | #F0AD7F, #D17D3E, #A75605, #723902 | #6A4225, #A16336, #D78951, #FFB98A |
| Rosa suave | #F2A3C1, #D27199, #AA4673, #79284E | #6B3C4F, #A25A77, #D87DA2, #FEB0CE |
| Turquesa laguna | #67D2CC, #0DABA5, #077F7A, #025653 | #085955, #048681, #08B6AF, #67E2DA |

Rojo fuego existió y se retiró (en la interfaz el rojo significa error); quien lo tenía pasa a Naranja
atardecer y lo ve avisado en Opciones.

### Resto de colores del mapa (de la paleta Nocturne)

| Uso | Token | Día | Noche |
|---|---|---|---|
| Fondo de mapa y tarjetas | CANVAS_ELEVATED | #FBFCFE | #212836 |
| Borde de mapa y tarjetas | BORDER_SUBTLE | #E8EAF0 | #1F2635 |
| Sombra de mapa y tarjetas | SHADOW_SUBTLE | #1B243012 | ninguna |
| Texto principal, borde de hoy, rombos | FG | #1B2430 | #D6DAE1 |
| Texto secundario (títulos, unidades, línea gris) | FG_SUBTLE | #4E576A | #B7BECC |
| Gris vacío | BORDER_SUBTLE / CANVAS_INSET | #E8EAF0 | #0F131B |
| Botones del mapa | BUTTON_BG, borde BORDER | #FBFCFE / #DADEE7 | #242C3A / #2C3444 |
| Botones con el ratón | BUTTON_HOVER, borde BUTTON_HOVER_BORDER | #EDF0F5 / #C0C6D3 | #2E3747 / #3D475C |
| Contorno de foco | BORDER_FOCUS | #3B6FE0 | #6390FF |
| Flechas de año apagadas | FG_DISABLED | #A9AFBC | #7C869A |
| Globo | CANVAS_OVERLAY, texto FG, borde BORDER, sombra 0 6px 18px SHADOW | #FBFCFE | #293040 |

## 6. Pie del mapa

Todo en minúscula al empezar, salvo donde la ortografía pide mayúscula (sustantivos en alemán).

- Izquierda, como mucho una línea de sorpresa, solo si hoy ya ha estudiado y es verdad, por orden:
  «un año seguido», «nueva racha más larga», «mejor semana del año», el 31 de diciembre «2026: 250 días
  con estudio», «mes completo» (último día de un mes estudiado entero) o una cifra redonda del año
  («500 tarjetas este año»: 100, 500 y cada 1.000).
- Derecha, la leyenda: «menos», gris vacío, los cuatro tonos, «más». Cada cuadrito tiene un globo con
  las cifras que cubre («de 3 a 6 tarjetas», «13 tarjetas o más»). Detrás, si salen en el año visible:
  «pendientes», «fecha clave» y «cubierto».
- Colección vacía: el mapa igual, con hoy marcado, y al pie «cada día de estudio se pintará aquí.».

## 7. Globo de un día (ratón o teclado)

Encima del día: la fecha completa en gris («lunes, 22 de junio de 2026») y debajo lo hecho: «9
tarjetas», «0 tarjetas», «12 tarjetas pendientes» o «Ninguna tarjeta pendiente». Antes del primer
repaso, solo la fecha. En una fecha clave, su nombre arriba en negrita con la cuenta atrás («Parcial
(faltan 23 días)»); en un día cubierto, debajo «Cubierto con un comodín» o «Racha en pausa». El globo no
se puede recorrer con el ratón (para no tapar los días de arriba); Esc lo cierra. Letra de 13 px.

## 8. Pulsar un día (clic, Intro o Espacio)

- Día pasado con repasos: abre Explorar con las tarjetas respondidas ese día.
- Día futuro con pendientes: abre Explorar con las que vencen; hoy incluye lo atrasado.
- Días sin nada: no responden ni muestran la mano.

## 9. Tarjetas de cifras

Cada tarjeta: título en gris suave (12 px, seminegrita), dato grande (cifra a 20 px seminegrita y
unidad pequeña en gris) y una línea gris. Sin globos, sin subrayados, no se pulsan y el tabulador no se
para en ellas. Una tarjeta sin dato no se muestra: el primer día solo se ven «Hoy» y «Racha», y las que
quedan se reparten el ancho.

Línea gris: siempre en minúscula al empezar (salvo ortografía); lo que escribe la persona (su plan,
nombres de fechas clave) sale tal cual. Siempre entera, en los renglones que necesite, sin «…».
Interlineado 1,5; 13 px; gris suave (7,9 a 1 de noche). Las tarjetas de una fila igualan su alto.
Separador «·».

- «Hoy»:
  - Sin meta (o con «Mostrar racha y meta» desmarcada): la cifra y «85 tarjetas en 7 días» (7 últimos
    días completos); si esos días están vacíos, solo la cifra.
  - Con meta: un anillo que se llena con el tono más intenso del tema (lo que falta, en el gris de
    pendientes) y «0 de 2», con «de 2» pequeño y gris. Debajo, «faltan 2 tarjetas» («falta 1
    tarjeta»). Cumplida: «✓ meta cumplida · 3 días esta semana» («✓ al día» con «Terminar lo de hoy»).
    La primera vez que se dibuja cumplida, el ✓ aparece con un leve aumento de 150 ms (fundido si se
    pide reducir el movimiento).
  - Con «Terminar lo de hoy», la meta son las respondidas hoy más las que aún vencen, con los límites
    diarios de Anki y sin mazos excluidos; una vez cumplida, queda cumplida el resto del día. Si hoy no
    vence nada ni ha estudiado, se ve como sin meta.
  - En la pantalla de un mazo: «Hoy en este mazo», sin meta.
- «Racha» (solo con «Mostrar racha y meta»): días seguidos con algún repaso. Debajo, por orden: «✓ hoy»
  o «hoy pendiente» (con el plan detrás: «hoy pendiente · al levantarme de la cama»), «en pausa hasta el
  5 nov.», «a 3 días del récord» y los comodines («1 comodín»). El récord solo sale si el récord es
  mayor que la racha, de 7 días o más, y faltan 7 o menos. Si la línea no cabe, lo primero que se
  pierde son los comodines. Con la racha a cero: «0 días» y «hoy pendiente · [plan]». Al volver, el
  primer día dice «Día 1».
- «Promedio diario»: tarjetas por día en el periodo, desde el primer día con estudio de ese periodo, sin
  días de pausa. Debajo: «últimos 30 días», «último año» o «todo el historial». No se muestra sin ningún
  día completo estudiado.
- «Retención»: porcentaje de repasos acertados en el mismo periodo, mismo texto debajo. No se muestra con
  menos de 20 respuestas. No muestra el objetivo de FSRS.
- «Próxima fecha» (solo con fechas clave de hoy en adelante): «faltan 23 días» o «es hoy» y, debajo, su
  nombre (varios, separados por «·»).

## 10. Carga, cambios y fallos

- Primera carga: tarjetas con huecos grises y la rejilla ya con su alto final: nada salta al llegar
  los datos. Al volver a una pantalla, se ve al instante el último mapa y se sustituye si cambió.
- Cambiar de año o de aspecto no relee la colección. Cambiar los mazos excluidos sí: el mapa anterior
  sigue a la vista y, si tarda más de 1 s, al pie sale «Actualizando…» en gris (el lector de pantalla
  lo anuncia).
- Al cambiar el día de Anki (4 de la mañana de serie) el mapa se recalcula.
- Si algo falla: en el sitio del mapa, «No se pudo cargar el mapa de calor.» y debajo «Vuelva a abrir
  Anki; si se repite, el detalle está en el registro del complemento.», con el botón de opciones. Nunca
  la ventana de error de Anki.

## 11. Ventana de opciones

Panel propio de 560 px de ancho, del mismo material que las tarjetas del mapa (el panel de Atelier
copia sus medidas). Título «Opciones», tres grupos en recuadros, por orden de uso desde la 4.16.0
(«Metas y fechas», «Qué se cuenta», «Apariencia»), y Aceptar y Cancelar abajo, en el orden de cada
sistema. Al abrir, el foco está en «Mostrar racha y meta»; si se abrió con el ratón, el contorno de foco
no se ve hasta la primera tecla. Si no cabe, los últimos 24 px del cuerpo se funden con el fondo
mientras quede contenido debajo. El sitio de la barra de desplazamiento está siempre reservado. Nada se guarda hasta Aceptar. Si tenía Rojo fuego, arriba: «Su tema «Rojo
fuego» se ha retirado; ahora usa «Naranja atardecer».».

Colores del panel (Nocturne): fondo CANVAS, recuadros CANVAS_ELEVATED con borde BORDER_SUBTLE,
campos hundidos CANVAS_INSET, líneas BORDER, bordes de controles #878C97 de día y #727B8C de noche,
acción BUTTON_PRIMARY_BG con texto blanco (solo rellenos y bordes), texto que se pulsa FG_LINK
(«Restaurar apariencia» y «Deshacer» subrayados; «‹ Opciones» con su flecha), texto de ejemplo
FG_FAINT, lo apagado FG_DISABLED (casilla marcada apagada BUTTON_PRIMARY_DISABLED), foco BORDER_FOCUS, opción elegida con el resaltado de fila
(#EAEEF8 / #19233F), hover BUTTON_HOVER, peligro ACCENT_DANGER. Filas de al menos 48–52 px; botones de
32 px; letra de 14 px en las filas, 12 px en ayudas, 16 px en títulos de subpágina, 11 px en detalles
del calendario.

### Apariencia

«Se ve ya en el mapa; se guarda al aceptar.»: el mapa de detrás cambia en vivo y Cancelar lo deshace.
Arriba a la derecha, «Restaurar apariencia» (con «Deshacer» al lado tras usarlo), subrayados.

| Opción | Control | Valores | De serie |
|---|---|---|---|
| Tema de color | Fichas de selección (grupo de opciones), cada una con su muestra en el tono del modo activo | Azul océano, Naranja atardecer, Púrpura real, Rosa suave, Turquesa laguna, Verde clásico | Verde clásico |
| Tamaño del mapa | Número con «−» y «+» (mantener pulsado repite) y casilla «Ajustado al ancho» («El mapa ocupa todo el ancho; los cuadritos miden al menos 10 px.») | 10 a 60 px | 24 px |
| Redondeo de esquinas | Número con «−» y «+» | 0 px a la mitad del cuadrito, como mucho 15 («Hasta la mitad del cuadrito (12 px).») | 3 px |

### Qué se cuenta

«Los mazos excluidos se aplican al aceptar.»

- Periodo de las cifras: control segmentado «30 días», «365 días», «Todo el historial» («Vale para el
  promedio diario y la retención.»). De serie, 30 días.
- Excluir mazos: fila con resumen («Ninguno», «2 mazos excluidos») que abre una subpágina en la misma
  ventana: buscador («Ningún mazo coincide.») y árbol de mazos plegable con casillas; «Al excluir un
  mazo se excluyen también sus submazos.».

### Metas y fechas

- «Mostrar racha y meta» (marcada). Desmarcada: «La meta, los comodines y la pausa no cuentan mientras
  esté desmarcada; se conservan.».
- Meta diaria: «Sin meta» (de serie), «Un número» o «Terminar lo de hoy».
  - «Un número»: 1 a 9.999; al elegirla propone el 80 % exacto del promedio que dice la tarjeta, sin
    redondear («Propuesta: 16 (el 80 % de su promedio diario).» con un promedio de 20; sin historial,
    30). Debajo: «Si es menor que lo que vence, el resto queda para
    mañana.».
  - «Terminar lo de hoy»: «Las tarjetas que vencen hoy, con los límites diarios de Anki.».
  - Con 7 días o más de datos: «Cumplida 12 de los últimos 14 días.»; con «Terminar lo de hoy» cumplida
    la mitad o menos: «Si le cuesta terminar, baje las tarjetas nuevas al día en las opciones del
    mazo.».
- «Cubrir días sueltos con comodines» (marcada): «Cada 7 días seguidos gana un comodín (2 como máximo).
  Un día sin estudiar gasta uno.» y «Ahora tiene 1 comodín.».
- «Pausar la racha»: «Desde» y «hasta» con calendario propio, como mucho 30 días. «Los días de pausa sin
  estudio no rompen la racha ni gastan comodines. Dura 30 días como máximo.».
- «Suelo estudiar»: campo libre («p. ej., después de desayunar», 60 caracteres) que se dice en «Racha»
  mientras hoy esté pendiente.
- Fechas clave: fila con resumen que abre subpágina. Arriba, «Nueva fecha» con «Nombre» («p. ej.,
  examen de Matemáticas», 60 caracteres), «Fecha» (calendario de 2000 a 2100) y «Añadir». Debajo, la
  lista por fecha, con «Editar» y «Eliminar» en cada fila y «pasada» en las pasadas. Avisos encima de
  los campos: «Falta el nombre de la fecha.», «Esa fecha con ese nombre ya está en la lista.», «Caben
  hasta 50 fechas.». Al eliminar: «Se eliminó «Parcial».» con «Deshacer» en el sitio de la fila. Al
  cancelar con cambios: «¿Descartar los cambios?» («Se perderán las fechas clave que ha añadido,
  cambiado o eliminado.»), con el foco en «Seguir editando». Sin fechas, en lugar de «0 de 50 fechas»:
  «Cada fecha clave se marca con un rombo en el mapa. Mientras esté por venir, la tarjeta «Próxima
  fecha» cuenta los días que faltan.»; con fechas, «2 de 50 fechas» a 12 px, alineado con el texto de
  las tarjetas. Un nombre escrito sin «Añadir» cuenta: Aceptar lo añade (si no se puede, no cierra y
  avisa), Cancelar pregunta y «‹ Opciones» lo conserva.

## 12. Movimiento

Solo dos: el leve hundimiento de los botones al pulsarlos (100 ms) y la aparición del ✓ al cumplir la
meta (150 ms, escala y transparencia; fundido simple si Anki o el sistema piden reducir el
movimiento). Nada más se anima.

## 13. Accesibilidad

- Teclado en el mapa: el tabulador entra por hoy (o por el 1 de enero en otro año). Flechas: días y
  semanas. Inicio y Fin: lunes y domingo. RePág y AvPág: mismo día del mes anterior o siguiente (con
  Mayús, del año). Si el día cae en otro año, el mapa cambia de año y el foco espera allí. Intro o
  Espacio abren el día. Esc cierra el globo. Un solo día es alcanzable con el tabulador (navegación
  itinerante), el resto con flechas.
- Foco visible: contorno azul (BORDER_FOCUS); en el día de hoy va por fuera, separado 2 px, para que se
  vea también su borde. En los botones, 2 px separados 2 px (Anki los quita de serie; GritMap lo
  fuerza). El foco nunca queda bajo el borde que se desvanece.
- Zona de pulsación: los tres botones del mapa reaccionan también un poco más allá de su borde.
- Botones apagados (flechas de año sin más años): se anuncian como no disponibles, pero siguen diciendo
  su nombre al pasar el ratón.
- Lector de pantalla: el mapa es un grupo con el año como nombre; cada día lleva como nombre el texto de
  su globo; iconos, rombos e iniciales de los días están ocultos al lector; cada cuadrito de la leyenda es
  una imagen cuyo nombre son las cifras que cubre; «Actualizando…» se anuncia; los títulos de las tarjetas son encabezados; «·» se oye como
  pausa y «✓ hoy» como «hoy hecho»; el mapa se marca como ocupado mientras carga.
- Opciones: grupos de botones de opción con nombre, campos numéricos con valor, mínimo, máximo y
  unidad anunciados, árbol de mazos con estado plegado o desplegado, campos inválidos marcados,
  calendario como diálogo con el mes anunciado.
- Texto que no se corta («…») en ninguna línea gris: no pierde texto al agrandar letra o espaciado.
- Color nunca solo: hoy por borde, cubierto por borde discontinuo, fecha clave por rombo, pendientes por
  su posición en el futuro.
- Contraste: línea gris 7,9 a 1 de noche; borde de los controles de Opciones 3,2 a 1 o más; texto blanco
  sobre el azul de acción 4,6 a 1 de día y 4,9 de noche; enlaces (FG_LINK) 8,1 a 1 de noche y 5,3 de
  día sobre los recuadros; texto de ejemplo (FG_FAINT) 5,8 de noche y 5,1 de día; flechas apagadas
  (FG_DISABLED) 4,0 de noche.
- Idiomas de derecha a izquierda: el eje del tiempo (flechas, rejilla, leyenda) sigue de izquierda a
  derecha.
- Desviación aceptada por la persona: el globo de los días no se puede recorrer con el ratón (WCAG 2.2,
  criterio 1.4.13, lo pediría).

## 14. Qué guarda

- En la configuración de complementos del ordenador (todos los perfiles, no se sincroniza): apariencia,
  periodo, meta, comodines, «Mostrar racha y meta», «Suelo estudiar».
- Dentro de cada colección (viaja con la sincronización): mazos excluidos, fechas clave, pausa de la
  racha y los días con meta de las 3 últimas semanas. No se deshacen desde Editar.
- Un valor que falte o no sirva se sustituye por el de serie.

## 15. Idiomas

51 idiomas (si falta el de Anki, inglés), con la forma de plural de cada idioma. Cifras, porcentajes,
fechas y meses los escribe Anki; en español, punto de millar desde 1.000. «Añadir», «Eliminar»,
«Buscar», «Deshacer» y «Descartar» usan los textos de Anki. Trata de usted.

## 16. Decisiones tomadas a propósito (no «corregir» sin preguntar)

- Las tarjetas no tienen globos: se descubrían poco, tapaban la cifra y repetían lo de Opciones. Si un
  día se echa de menos el objetivo de retención, la vuelta prevista es «últimos 30 días · objetivo
  90 %» en la línea gris.
- «Promedio diario» y «Retención» desaparecen sin dato (no «N/A»): no recibir con ceros.
- Con la racha a cero no se dice «Última sesión: hace N días»: el mapa ya lo enseña.
- «Perdonado» pasó a «cubierto».
- «0 de 2» con una sola tarjeta pendiente es correcto: 2 es la meta elegida.
- Texto blanco sobre el azul también de noche (lo fija la paleta).
- El ✓ de la meta aparece con un leve aumento: es una transformación de 150 ms, que la norma admite.
- La leyenda no añade paradas al tabulador: el lector de pantalla ya lee las cifras de cada cuadrito.
- Las tarjetas se reparten el ancho del mapa (decisión de la 4.1.0); si un día molesta, la salida
  prevista es un tope de 400 px por tarjeta, alineadas a la izquierda.
- Opciones sin índice ni pestañas, sin botón «Usar 16» junto a la propuesta y sin ayuda bajo «Suelo
  estudiar» (informe 4.15.1, apartado 7.4): el orden por uso y el fundido bastan.
- Sin llama de racha, sin premios, sin notificaciones, sin botón «Hoy» ni botones de periodo junto al
  año (el periodo está en Opciones).
- La retención usa la misma ventana que el promedio y solo días completos. Las tarjetas borradas
  cuentan en el mapa general. La medida «minutos» se retiró.

## 17. Qué no hace

No se conecta a internet, no cambia nada del estudio, no avisa ni da premios, no anima nada salvo lo
del apartado 12.
