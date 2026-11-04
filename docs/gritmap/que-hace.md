# Qué hace «GritMap»

Versión 4.13.0 · 2026-11-04

Un mapa de calor de su estudio, parecido al de las contribuciones de GitHub: un cuadrito por cada
día del año, más intenso cuanto más estudió, y en gris los días que vienen, según las tarjetas que
vencen. Debajo hay cuatro o cinco tarjetas pequeñas: «Hoy», «Racha», «Promedio diario»,
«Retención» y, si tiene fechas clave por venir, «Próxima fecha». Solo lee su colección: nunca
cambia tarjetas, notas ni repasos. Guarda sus opciones y, cada día con meta, si la cumplió.

Esta descripción se rehízo a partir del código de la 4.11.2 al traerla al taller, con los cambios de
la 4.12.0 (informe 4.11, aprobado el 2026-11-04) y de la 4.13.0 (dos propuestas del informe de
Atelier 3.7, aprobado el mismo día, para que los dos complementos combinen: la esquina de las
tarjetas y los grises de los días que vienen).

## 1. Dónde aparece

- En la lista de mazos (la pantalla principal), debajo de la lista, junto a la línea en la que Anki
  dice cuánto ha estudiado hoy. Ahí cuenta toda la colección, menos los mazos que usted excluya.
- En la pantalla de un mazo (la que tiene el botón «Comenzar a estudiar»), debajo de las cifras de
  tarjetas. Ahí cuenta solo ese mazo y sus submazos. Si el mazo está excluido, en su lugar sale
  «Este mazo está excluido del mapa.» con el botón de opciones.
- En Herramientas > Complementos, al seleccionar GritMap y pulsar «Configuración», se abre su
  ventana de opciones, la misma que abre el botón de opciones del mapa.
- No aparece en el repaso, en Explorar, en las estadísticas ni en el editor. No añade menús.

## 2. El mapa

- Una tarjeta con el año entero, de enero a diciembre, en columnas de semanas que empiezan en lunes.
  Encima van los meses y, a la izquierda, las iniciales del lunes, el miércoles y el viernes, en el
  idioma de Anki y siempre con el calendario gregoriano.
- Encima del mapa, centrado, «‹ 2026 ›»: las flechas pasan al año anterior o al siguiente. Se apagan
  cuando no hay otro año con datos (siguen diciendo su nombre al pasar el ratón y el lector de
  pantalla las anuncia como no disponibles). En la esquina, el botón de opciones (icono de
  deslizadores, «Opciones»). Los tres botones reaccionan también un poco más allá de su borde (4.12.0).
- Qué color tiene cada cuadrito:
  - Días pasados y hoy con estudio: uno de los cuatro tonos del tema, según las tarjetas distintas
    respondidas ese día. Los cortes salen de su propio promedio: hasta la mitad, hasta el promedio,
    hasta el doble y más del doble.
  - Días sin estudio desde su primer repaso: el gris vacío, que en la leyenda está bajo «Menos».
  - Días anteriores a su primer repaso y días futuros sin tarjetas pendientes: «sin dato», un tono
    aún más apagado, a medio camino entre el gris vacío y el fondo de la tarjeta (4.12.0). Si nunca
    ha estudiado, todos los días anteriores a hoy son «sin dato».
  - Días futuros con tarjetas que vencen: tres grises, según la carga (hasta la mitad de lo normal,
    hasta vez y media y más). Desde la 4.13.0 no son grises fijos: salen de mezclar el color del
    texto con el de la tarjeta (de día, un 16, 21 y 26 % de texto; de noche, un 10, 15 y 19 %), así
    que toman el matiz de la paleta de Anki o de Atelier (cálidos con Atardecer, verdosos con Bosque,
    lilas con Lavanda). Con Nocturne son prácticamente los de antes. Son más suaves que el primer
    tono del tema en todas las combinaciones con las paletas de Atelier salvo una: con Atardecer de
    noche y el tema Rosa suave, el gris de más carga es tan marcado como el primer rosa (1,66 frente a
    1,59 a 1 sobre la tarjeta); se distinguen por el color.
- Hoy lleva un borde del color del texto.
- Días perdonados (por un comodín o por la pausa de la racha): vacíos y con un borde fino
  discontinuo.
- Fechas clave: un rombo dentro del cuadrito; lleno en el color del texto si es hoy o está por venir,
  hueco y gris si ya pasó.
- El cuadrito mide 24 px y su redondeo 3 px, salvo que elija otra cosa en Opciones. Con «Ajustado al
  ancho», el mapa ocupa todo el ancho y los cuadritos miden al menos 10 px.
- Si el año no cabe a lo ancho, el mapa se desplaza de lado: el borde por donde sigue se desvanece y,
  al abrirlo, se ve la semana de hoy (en un año pasado, su final; en uno futuro, su principio).
- Al pie del mapa:
  - A la izquierda, como mucho una línea de sorpresa, solo si hoy ya ha estudiado y es verdad, por
    este orden: «Un año seguido», «Nueva racha más larga», «Su mejor semana del año», el 31 de
    diciembre «2026: 250 días con estudio», «Mes completo» (el último día de un mes estudiado
    entero) o una cifra redonda del año («500 tarjetas este año»: 100, 500 y cada 1.000).
  - A la derecha, la leyenda: «Menos», el gris vacío y los cuatro tonos, «Más». Cada cuadrito de la
    leyenda dice en su globo las cifras que cubre («de 3 a 6 tarjetas», «13 tarjetas o más»).
    Detrás, si salen en el año que se ve: «Pendientes», «Fecha clave» y «Perdonado». «Sin dato» no
    tiene cuadrito: es fondo, no información.
- Con la colección vacía se ve el mapa igual, con hoy marcado, y al pie «Cada día que estudie se
  pintará aquí.».

## 3. Al pasar el ratón por un día (o llegar a él con el teclado)

Un globo encima del día: la fecha completa en gris («lunes, 22 de junio de 2026») y, debajo, lo
hecho: «9 tarjetas», «0 tarjetas» (también antes de su primer repaso), «12 tarjetas pendientes» o
«Ninguna tarjeta pendiente». Si es una fecha clave, su nombre va arriba en negrita con la cuenta
atrás («Parcial (faltan 23 días)»); si está perdonado, debajo «Perdonado con un comodín» o «Racha
en pausa». El globo de los días no se puede recorrer con el ratón, para que nunca tape los días de
arriba; Esc lo cierra.

## 4. Al pulsar un día (o Intro o Espacio con el foco en él)

- Un día pasado con repasos abre Explorar con las tarjetas respondidas ese día.
- Un día futuro con tarjetas pendientes abre Explorar con las que vencen ese día; hoy incluye lo
  atrasado.
- Los días sin nada no responden ni muestran la mano.

Con el teclado, el tabulador entra en el mapa por hoy (o por el 1 de enero en otro año). Las flechas
mueven por días y semanas; Inicio y Fin van al lunes y al domingo; RePág y AvPág, al mismo día del
mes anterior o siguiente (con Mayús, del año). Si el día cae en otro año, el mapa cambia de año y el
foco espera allí. El día con el foco lleva un contorno azul; en el día de hoy va por fuera, separado
2 px, para que se vea también su borde (4.12.0). El foco nunca queda bajo el borde que se desvanece.

## 5. Las tarjetas de debajo

El mapa y las tarjetas llevan la esquina de los recuadros de Anki: 12 px, o la de la paleta de
Atelier si está instalado (12 px en Nocturne, Papel y Lavanda; 16 px en Bosque y Atardecer), la misma
que la lista de mazos que tienen encima. Hasta la 4.12.0 eran 10 px.

Cuatro o cinco tarjetas del mismo ancho, que suman el ancho del mapa: de dos en dos en ventanas
estrechas y de una en una en muy estrechas. Cada una tiene su título en gris suave, el dato grande
(la cifra a 20 px y la unidad pequeña, en gris) y una línea gris que, si no cabe en dos renglones, se
corta con «…» y se lee entera al pasar el ratón. Lo que lleva subrayado de puntos tiene un globo,
también con el tabulador, y ese globo sí se puede recorrer con el ratón. Las tarjetas no se pulsan.

- «Hoy»: las tarjetas de hoy.
  - Sin meta (o con «Mostrar racha y meta» desmarcada): la cifra y, debajo, «85 tarjetas en 7 días»
    (los 7 últimos días completos).
  - Con meta: un anillo que se llena en el tono más intenso del tema (lo que falta, en el gris de
    pendientes, desde la 4.12.0) y «0 de 2», con «de 2» pequeño y en gris (4.12.0). Debajo, «faltan
    2 tarjetas». Al cumplirla, «✓ Meta cumplida · 3 días esta semana» («✓ Al día» con «Terminar lo
    de hoy»). La primera vez que se dibuja cumplida, el ✓ aparece con un leve aumento de 150 ms (un
    fundido si Anki pide reducir las animaciones). Desde que hay dos días con datos, el globo de esa
    línea dice «Cumplida 6 de los últimos 8 días.» (14 días como mucho; no cuentan la pausa ni los
    días sin datos).
  - Con «Terminar lo de hoy», la meta son las tarjetas respondidas hoy más las que aún vencen, con
    los límites diarios de Anki y sin los mazos excluidos; una vez cumplida, queda cumplida el resto
    del día. Si hoy no vence nada ni ha estudiado, «Hoy» se ve como sin meta.
  - En la pantalla de un mazo, «Hoy en este mazo», sin meta (la meta es de toda la colección).
- «Racha» (solo con «Mostrar racha y meta»): los días seguidos con algún repaso. Debajo, por orden:
  «✓ hoy» o «hoy pendiente» (con su plan detrás si lo escribió: «hoy pendiente · al levantarme de la
  cama»), «en pausa hasta el 5 nov.», los comodines que le quedan («1 comodín», con su regla en el
  globo) y, a menos de 7 días de su récord, «a 3 días del récord». Si la racha actual no es la más
  larga, el globo de la cifra dice «Récord: 12 días». Tras romperla, el primer día dice «Día 1». Sin
  racha, «0 días» y «Última sesión: hace 4 días».
- «Promedio diario»: tarjetas por día en el periodo de las cifras, contado desde el primer día con
  estudio de ese periodo; sin los días de pausa. Debajo, «últimos 30 días», «último año» o «todo el
  historial». Sin ningún día completo estudiado, «N/A» en gris, con el motivo en el globo («Sin días
  completos estudiados en los últimos 30 días»).
- «Retención»: el porcentaje de repasos acertados en el mismo periodo, con el mismo texto debajo. Con
  menos de 20 respuestas que medir, «N/A» con su motivo. Con FSRS y la misma retención deseada en
  todo lo que cuenta, el globo del porcentaje dice «Objetivo: 90 %».
- «Próxima fecha» (solo si hay alguna fecha clave de hoy en adelante): «faltan 23 días» o «es hoy» y,
  debajo, su nombre (varios, separados por «·»).

## 6. Mientras carga, al cambiar algo y si algo falla

- La primera vez se ven las tarjetas con huecos grises y la rejilla con su alto final: nada salta al
  llegar los datos. Al volver a una pantalla se ve al instante el último mapa y se sustituye si
  cambió.
- Al cambiar de año o de aspecto no se vuelve a leer la colección. Al cambiar los mazos excluidos sí:
  el mapa anterior sigue a la vista y, si tarda más de un segundo, al pie sale «Actualizando…» en
  gris, que el lector de pantalla anuncia (4.12.0).
- Al cambiar el día de Anki (a las 4 de la mañana, de serie) el mapa se recalcula.
- Si algo falla, nunca abre la ventana de error de Anki: en el sitio del mapa sale «No se pudo cargar
  el mapa de calor.» y, debajo, «Vuelva a abrir Anki; si se repite, el detalle está en el registro
  del complemento.», con el botón de opciones. Anki sigue funcionando.

## 7. Ventana de opciones

Un panel propio de 560 px de ancho, hecho del mismo material que las tarjetas del mapa, con el título
«Opciones», tres grupos y Aceptar y Cancelar abajo, en el orden de cada sistema. Nada se guarda hasta
Aceptar. Si tenía el tema Rojo fuego, que se retiró, arriba sale «Su tema «Rojo fuego» se ha
retirado; ahora usa «Naranja atardecer».».

### Apariencia

«Se ve ya en el mapa; se guarda al aceptar.»: el mapa de detrás cambia en vivo y Cancelar lo
deshace. Arriba a la derecha, «Restaurar apariencia» (con «Deshacer» al lado tras usarlo).

| Opción | Valores | De serie |
|---|---|---|
| Tema de color | Azul océano, Naranja atardecer, Púrpura real, Rosa suave, Turquesa laguna, Verde clásico, con su muestra en el tono del modo activo | Verde clásico |
| Tamaño del mapa | De 10 a 60 px, con «−» y «+» (mantener pulsado repite), o la casilla «Ajustado al ancho» («El mapa ocupa todo el ancho; los cuadritos miden al menos 10 px.») | 24 px |
| Redondeo de esquinas | De 0 px a la mitad del cuadrito, como mucho 15 («Hasta la mitad del cuadrito (12 px).») | 3 px |

### Qué se cuenta

«Los mazos excluidos se aplican al aceptar.»

- Periodo de las cifras: «30 días», «365 días» o «Todo el historial» («Vale para el promedio diario
  y la retención.»). De serie, 30 días.
- Excluir mazos: fila con el resumen («Ninguno», «2 mazos excluidos») que abre su subpágina dentro de
  la misma ventana: un buscador («Ningún mazo coincide.» si no hay ninguno) y el árbol de mazos con
  casillas; «Al excluir un mazo se excluyen también sus submazos.». Lo excluido no cuenta en ningún
  mapa ni en la meta.

### Metas y fechas

- «Mostrar racha y meta» (marcada de serie). Desmarcada: «La meta, los comodines y la pausa no
  cuentan mientras esté desmarcada; se conservan.».
- Meta diaria: «Sin meta» (de serie), «Un número» o «Terminar lo de hoy».
  - «Un número»: de 1 a 9.999 tarjetas al día; al elegirla se propone el 80 % de su promedio diario
    («Propuesta: 5 (el 80 % de su promedio diario, 7).»; sin historial, 30). Debajo: «Si es menor que
    lo que vence, el resto queda para mañana.».
  - «Terminar lo de hoy»: «Las tarjetas que vencen hoy, con los límites diarios de Anki.».
  - Con al menos 7 días con datos de esa meta, «Cumplida 12 de los últimos 14 días.»; con «Terminar
    lo de hoy» cumplida la mitad de los días o menos, además «Si le cuesta terminar, baje las tarjetas
    nuevas al día en las opciones del mazo.».
- «Perdonar días sueltos con comodines» (marcada de serie): «Cada 7 días seguidos gana un comodín (2
  como máximo). Un día sin estudiar gasta uno.», y «Ahora tiene 1 comodín.» si se sabe.
- «Pausar la racha»: «Desde» y «hasta», con calendario, como mucho 30 días. «Los días de pausa sin
  estudio no rompen la racha ni gastan comodines. Dura 30 días como máximo.».
- «Suelo estudiar»: un campo libre («p. ej., después de desayunar», 60 caracteres como máximo) que se
  dice en «Racha» mientras hoy esté pendiente.
- Fechas clave: fila con el resumen que abre su subpágina. Arriba, «Nueva fecha», con «Nombre» («p.
  ej., examen de Matemáticas», 60 caracteres como máximo), «Fecha» (calendario de 2000 a 2100) y
  «Añadir»; debajo, la lista ordenada por fecha, con «Editar» y «Eliminar» en cada fila y «pasada» en
  las que ya pasaron. Avisos encima de los campos: «Falta el nombre de la fecha.», «Esa fecha con ese
  nombre ya está en la lista.» y «Caben hasta 50 fechas.». Al eliminar, «Se eliminó «Parcial».» con
  «Deshacer» en el sitio de la fila. Si hay cambios sin guardar en las fechas y pulsa Cancelar,
  pregunta «¿Descartar los cambios?» («Se perderán las fechas clave que ha añadido, cambiado o
  eliminado.»), con el foco en «Seguir editando».

## 8. Qué guarda y dónde

- La apariencia, el periodo de las cifras, la meta, los comodines, «Mostrar racha y meta» y «Suelo
  estudiar», en la configuración de complementos de este ordenador: valen para todos los perfiles y
  no se sincronizan.
- Los mazos excluidos, las fechas clave, la pausa de la racha y los días con meta de las últimas 3
  semanas (si se cumplió o no), dentro de cada colección: cada perfil tiene los suyos y viajan con la
  sincronización. No se deshacen desde Editar, porque son ajustes, no estudio.
- Un valor que falte o no sirva (por ejemplo, escrito a mano) se sustituye por el de serie.

## 9. Idiomas

Sus textos están en 51 idiomas; si el de Anki no está, sale en inglés. Cada cifra con unidad usa la
forma de plural de su idioma. Las cifras, los porcentajes, las fechas y los meses los escribe Anki en
su idioma; en español, con punto de millar desde 1.000. «N/A», «Añadir», «Eliminar», «Buscar»,
«Deshacer» y «Descartar» usan los textos de Anki. En los idiomas que se escriben de
derecha a izquierda, el eje del tiempo (flechas, rejilla y leyenda) sigue yendo de izquierda a
derecha.

## 10. Qué no hace

- No se conecta a internet.
- No cambia nada de su estudio: solo lee.
- No avisa, no envía notificaciones y no da premios: lo que cambia se ve donde ocurre.
- No anima nada salvo el leve hundimiento de los botones al pulsarlos y la aparición del ✓ al cumplir
  la meta.
- No tiene botón «Hoy» ni botones de periodo junto al año (el periodo está en Opciones).
