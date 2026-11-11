# Qué hace «GritMap»

Versión 4.16.0 · 2026-11-11

Un mapa de calor de su estudio, parecido al de las contribuciones de GitHub: un cuadrito por cada
día del año, más intenso cuanto más estudió, y en gris los días que vienen, según las tarjetas que
vencen. Debajo hay cuatro o cinco tarjetas pequeñas: «Hoy», «Racha», «Promedio diario»,
«Retención» y, si tiene fechas clave por venir, «Próxima fecha». Solo lee su colección: nunca
cambia tarjetas, notas ni repasos. Guarda sus opciones y, cada día con meta, si la cumplió.

Esta descripción se rehízo a partir del código de la 4.11.2 al traerla al taller, con los cambios de
la 4.12.0 (informe 4.11, aprobado el 2026-11-04) y de la 4.13.0 (dos propuestas del informe de
Atelier 3.7, aprobado el mismo día, para que los dos complementos combinen: la esquina de las
tarjetas y los grises de los días que vienen). La 4.16.0 aplica el informe 4.15.1 (aprobado entero el
2026-11-10): orden de los grupos de Opciones, borde que se desvanece, colores de enlace, de ejemplo y de
apagado de la paleta, estado vacío de «Fechas clave» y propuesta de meta exacta.

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
  cuando no hay otro año con datos, en el gris de apagado de la paleta (4.16.0; antes, transparentes)
  (siguen diciendo su nombre al pasar el ratón y el lector de pantalla las anuncia como no
  disponibles). En la esquina, el botón de opciones (icono de deslizadores de 16 px desde la 4.16.0,
  «Opciones»). Los tres botones reaccionan también un poco más allá de su borde (4.12.0).
- Qué color tiene cada cuadrito:
  - Días pasados y hoy con estudio: uno de los cuatro tonos del tema, según las tarjetas distintas
    respondidas ese día. Los cortes salen de su propio promedio: hasta la mitad, hasta el promedio,
    hasta el doble y más del doble.
  - Días sin estudio desde su primer repaso: el gris vacío, que en la leyenda está bajo «menos».
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
    1,59 a 1 sobre la tarjeta); se distinguen por el color y por el sitio: los pendientes solo están
    en el futuro y lo estudiado solo en el pasado, con hoy entre medias.
- Hoy lleva un borde del color del texto.
- Días cubiertos (por un comodín o por la pausa de la racha): vacíos y con un borde fino
  discontinuo. Hasta la 4.14.0 se llamaban «perdonados».
- Fechas clave: un rombo dentro del cuadrito; lleno en el color del texto si es hoy o está por venir,
  hueco y gris si ya pasó.
- El cuadrito mide 24 px y su redondeo 3 px, salvo que elija otra cosa en Opciones. Con «Ajustado al
  ancho», el mapa ocupa todo el ancho y los cuadritos miden al menos 10 px.
- Si el año no cabe a lo ancho, el mapa se desplaza de lado: el borde por donde sigue se desvanece y,
  al abrirlo, se ve la semana de hoy (en un año pasado, su final; en uno futuro, su principio).
- Al pie del mapa:
  Todo el pie va en minúscula al empezar (4.15.0), salvo donde la ortografía del idioma pide
  mayúscula (los sustantivos en alemán).
  - A la izquierda, como mucho una línea de sorpresa, solo si hoy ya ha estudiado y es verdad, por
    este orden: «un año seguido», «nueva racha más larga», «mejor semana del año», el 31 de
    diciembre «2026: 250 días con estudio», «mes completo» (el último día de un mes estudiado
    entero) o una cifra redonda del año («500 tarjetas este año»: 100, 500 y cada 1.000).
  - A la derecha, la leyenda: «menos», el gris vacío y los cuatro tonos, «más». Cada cuadrito de la
    leyenda dice en su globo las cifras que cubre («de 3 a 6 tarjetas», «13 tarjetas o más»).
    Detrás, si salen en el año que se ve: «pendientes», «fecha clave» y «cubierto». «Sin dato» no
    tiene cuadrito: es fondo, no información.
- Con la colección vacía se ve el mapa igual, con hoy marcado, y al pie «cada día de estudio se
  pintará aquí.».

## 3. Al pasar el ratón por un día (o llegar a él con el teclado)

Un globo encima del día: la fecha completa en gris («lunes, 22 de junio de 2026») y, debajo, lo
hecho: «9 tarjetas», «0 tarjetas», «12 tarjetas pendientes» o «Ninguna tarjeta pendiente». En los
días anteriores a su primer repaso, solo la fecha (4.15.0): ahí no hay dato. Si es una fecha clave,
su nombre va arriba en negrita con la cuenta atrás («Parcial (faltan 23 días)»); si está cubierto,
debajo «Cubierto con un comodín» o «Racha en pausa». El globo de los días no se puede recorrer con el ratón, para que nunca tape los días de
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

De una a cinco tarjetas del mismo ancho, que suman el ancho del mapa: de dos en dos en ventanas
estrechas y de una en una en muy estrechas. Una tarjeta sin dato no se muestra (4.15.0): el primer
día solo se ven «Hoy» y «Racha», y las que quedan se reparten el ancho. Cada una tiene su título en
gris suave, el dato grande (la cifra a 20 px y la unidad pequeña, en gris) y una línea gris. Desde la
4.14.0 las tarjetas no tienen globos ni subrayados de puntos, y el tabulador no se para en ellas.
Las tarjetas no se pulsan.

La línea gris (4.15.0):

- Empieza siempre en minúscula («✓ meta cumplida», «✓ al día», «hoy pendiente»), salvo donde la
  ortografía del idioma pide mayúscula (en alemán, «Ziel erreicht»). Lo que escribe usted (su plan,
  los nombres de las fechas clave) sale tal como lo escribió.
- Se ve siempre entera, en los renglones que necesite, sin cortarse con «…»: se lee igual con el
  ratón, el teclado o una pantalla táctil, y no pierde texto si se agranda la letra o el espaciado.
  Interlineado de 1,5; 13 px en gris suave (7,9 a 1 de noche, por encima del 4,5 a 1 que pide la
  norma). Las tarjetas de una fila igualan su alto, así que una línea más larga no descoloca las
  demás.
- El lector de pantalla oye una pausa en lugar de «punto» en cada «·», y «hoy hecho» en lugar de
  «✓ hoy».

- «Hoy»: las tarjetas de hoy.
  - Sin meta (o con «Mostrar racha y meta» desmarcada): la cifra y, debajo, «85 tarjetas en 7 días»
    (los 7 últimos días completos); si en esos 7 días no hay nada, solo la cifra (4.15.0).
  - Con meta: un anillo que se llena en el tono más intenso del tema (lo que falta, en el gris de
    pendientes, desde la 4.12.0) y «0 de 2», con «de 2» pequeño y en gris (4.12.0). Debajo, «faltan
    2 tarjetas» («falta 1 tarjeta» en singular; la frase concuerda con la cifra en cada idioma). Al cumplirla, «✓ meta cumplida · 3 días esta semana» («✓ al día» con «Terminar lo
    de hoy»). La primera vez que se dibuja cumplida, el ✓ aparece con un leve aumento de 150 ms (un
    fundido si Anki pide reducir las animaciones). El historial de la meta está en Opciones.
  - Con «Terminar lo de hoy», la meta son las tarjetas respondidas hoy más las que aún vencen, con
    los límites diarios de Anki y sin los mazos excluidos; una vez cumplida, queda cumplida el resto
    del día. Si hoy no vence nada ni ha estudiado, «Hoy» se ve como sin meta.
  - En la pantalla de un mazo, «Hoy en este mazo», sin meta (la meta es de toda la colección).
- «Racha» (solo con «Mostrar racha y meta»): los días seguidos con algún repaso. Debajo, por orden:
  «✓ hoy» o «hoy pendiente» (con su plan detrás si lo escribió: «hoy pendiente · al levantarme de la
  cama»), «en pausa hasta el 5 nov.», «a 3 días del récord» («a 1 día del récord») y los comodines
  que le quedan («1 comodín»; su regla está en Opciones). El récord solo sale si la racha más larga
  es mayor que la actual, de 7 días o más, y faltan 7 días o menos; cuando se supera, la línea de
  sorpresa del mapa dice «Nueva racha más larga». Si la línea no cabe, lo primero que se pierde son
  los comodines. Con la racha a cero, «0 días» y la línea de cualquier día, «hoy pendiente · al
  levantarme de la cama» (4.15.0; antes decía «Última sesión: hace 4 días»: el mapa ya enseña cuándo
  estudió por última vez). Al volver, el primer día dice «Día 1».
- «Promedio diario»: tarjetas por día en el periodo de las cifras, contado desde el primer día con
  estudio de ese periodo; sin los días de pausa. Debajo, «últimos 30 días», «último año» o «todo el
  historial». Sin ningún día completo estudiado en el periodo, la tarjeta no se muestra (4.15.0).
- «Retención»: el porcentaje de repasos acertados en el mismo periodo, con el mismo texto debajo. Con
  menos de 20 respuestas que medir en el periodo, la tarjeta no se muestra (4.15.0). No dice el
  objetivo de FSRS (4.14.0): está en las opciones del mazo de Anki.
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
Aceptar.

Desde la 4.16.0 los grupos van por orden de uso: «Metas y fechas», «Qué se cuenta» y «Apariencia». Al
abrirse, el foco está en «Mostrar racha y meta». Si el contenido no cabe, el borde inferior del panel se
desvanece mientras quede algo debajo, y desaparece al llegar al final; al moverse con el tabulador, el
control con el foco queda siempre entero por encima. El sitio de la barra de desplazamiento está siempre
reservado, así que nada cambia de ancho al entrar o salir de una subpágina. Si la ventana se abrió con el
ratón, el contorno de foco no se ve hasta que se pulsa una tecla (en los campos de texto, siempre); si se
abrió con el teclado desde el mapa, se ve desde el principio. Los textos que se pulsan («Restaurar
apariencia», «Deshacer») van en el color de enlace de la paleta y subrayados; «‹ Opciones», en el mismo
color, con su flecha. El texto de ejemplo de los campos va en el gris tenue de la paleta, y lo apagado (lo
que depende de «Mostrar racha y meta» cuando está desmarcada, y «−» y «+» en su límite), en su gris de
apagado. Si tenía el tema Rojo fuego, que se retiró, arriba sale «Su tema «Rojo fuego» se ha
retirado; ahora usa «Naranja atardecer».».

### Apariencia

«Se ve ya en el mapa; se guarda al aceptar.»: el mapa de detrás cambia en vivo y Cancelar lo
deshace. Arriba a la derecha, «Restaurar apariencia» (con «Deshacer» al lado tras usarlo), subrayados.

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
    («Propuesta: 16 (el 80 % de su promedio diario).», sin la cifra del promedio desde la 4.15.1; sin historial, 30).
    Desde la 4.16.0 es el 80 % exacto del promedio que dice la tarjeta (20 → 16), sin redondear a 5. Debajo: «Si es menor que
    lo que vence, el resto queda para mañana.».
  - «Terminar lo de hoy»: «Las tarjetas que vencen hoy, con los límites diarios de Anki.».
  - Con al menos 7 días con datos de esa meta, «Cumplida 12 de los últimos 14 días.»; con «Terminar
    lo de hoy» cumplida la mitad de los días o menos, además «Si le cuesta terminar, baje las tarjetas
    nuevas al día en las opciones del mazo.».
- «Cubrir días sueltos con comodines» (marcada de serie): «Cada 7 días seguidos gana un comodín (2
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
  Desde la 4.16.0: sin fechas, en lugar de «0 de 50 fechas», sale «Cada fecha clave se marca con un rombo
  en el mapa. Mientras esté por venir, la tarjeta «Próxima fecha» cuenta los días que faltan.»; con la
  primera fecha vuelve el contador («1 de 50 fechas»), a 12 px y alineado con el texto de las tarjetas.
  Un nombre escrito en «Nueva fecha» sin pulsar «Añadir» cuenta: Aceptar lo añade y cierra, o, si no se
  puede (repetido o sin sitio), no cierra y muestra el aviso de siempre encima del campo; Cancelar o Esc
  preguntan «¿Descartar los cambios?»; «‹ Opciones» vuelve y lo escrito se conserva.

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
su idioma; en español, con punto de millar desde 1.000. «Añadir», «Eliminar», «Buscar»,
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
