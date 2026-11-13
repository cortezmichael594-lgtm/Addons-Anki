# Estado del trabajo

Se actualiza al cerrar cada parte de un trabajo largo y se lee al retomarlo. Va aquí, y no en CLAUDE.md, porque cambia a menudo.

## Hecho

- 2026-11-03: el taller se adaptó a la plantilla en la rama `refactor-plantilla`, con el plan aprobado (solo en la nube; automejora aligerada; cerradura intacta). CLAUDE.md queda en 117 líneas y el detalle de las normas pasa a `docs/normas-del-taller.md`; el encargo del taller está en `docs/encargo.md`. Comprobación general con `herramientas/comprobar.py` (también al final de cada turno y en GitHub Actions), preparación de la nube con `herramientas/preparar.py` y el script de `docs/preparar-entorno.md`, y permisos con cerradura y colecciones protegidas en `.claude/settings.json`. `herramientas/copias` y las huellas de CLAUDE.md se retiran: el historial de git guarda cada versión. El código de los complementos no cambia: GritMap (37 pruebas) y Nocturne (81) pasan la comprobación.

- 2026-11-04: GritMap pasa de la 3.5.0 a la 4.11.2 que traía la persona (hecha fuera del taller) y
  a la 4.12.0 con las mejoras del informe 4.11, aprobado entero. Se rehízo `que-hace.md` a partir del
  código, se anotaron FIX-024 a FIX-031 en `errores.md` y se pusieron al día las pruebas de la 3.5.0
  (45 pruebas). Su `meta.json` personal no se sube: el repositorio es público.

- 2026-11-04: Atelier pasa a la 3.8.0 y GritMap a la 4.13.0 con la auditoría «Atelier 3.7.2»
  del 2026-11-04, aprobada entera (también el borde visible de los campos, que en octubre se había
  descartado, y las dos propuestas que eran de GritMap). La versión que la persona tenía instalada
  era idéntica a la del repositorio. FIX-012 (fila seleccionada de Explorar por debajo de 4,5 en
  cuatro paletas) y FIX-013 (botón del cuerpo relleno en Preferencias). Lo no aplicado, con su
  motivo, está en «Así a propósito» de docs/nocturne/errores.md; el blanco puro del editor queda en
  «Pendientes».

- 2026-11-09: GritMap 4.14.0 quita los globos de las tarjetas (informe breve del cliente del
  mismo día, aprobado entero): récord delante de los comodines, motivo de «N/A» en la línea gris, sin
  objetivo de FSRS, «falta 1 tarjeta» con la frase en plural en cada idioma y el globo del sistema
  solo con la línea cortada. 54 pruebas.

- 2026-11-09: GritMap 4.15.0 con el informe «textos, hábito y abandono» (aprobado entero), las
  líneas grises y el pie del mapa en minúscula y la accesibilidad de las líneas (sin corte, «·»
  oído como pausa, «✓ hoy» oído como «hoy hecho»). 62 pruebas. Va en el mismo pull request que la
  4.14.0.

- 2026-11-09: GritMap 4.15.1: «Propuesta: 5 (el 80 % de su promedio diario).», sin la cifra final,
  en 51 idiomas (petición del cliente).

- 2026-11-11: Atelier 3.9.0 con el informe «Atelier 3.8.0: auditoría y rediseño de la interfaz»
  (aprobado entero, con sus dos decisiones: botones de estudio sin píldora y tres tamaños de letra
  proporcionales). Ocho reglas en ventanas, páginas y panel; barras de desplazamiento a 3 a 1 en las
  cinco paletas; FIX-014 (borde de la elegida en el panel, de noche) y FIX-015 (texto del editor en
  blanco puro, que estaba en Pendientes); APR-070; docs/paleta-nocturne.md al día. Las propuestas del
  panel que el informe comparte con GritMap (borde de la elegida, miniaturas, botones de 88 px) no se
  han llevado a GritMap: el encargo era de Atelier.
- 2026-11-09: las ventanas de opciones de CoreProgress 1.1.0, ProFeedback 2.1.0, Hider 4.1.0,
  Restart 2.1.0, Always on Top 1.3 y Edit field during review 1.1.0 siguen el panel modelo de GritMap
  (PROP-012), con una pieza común copiada en cada complemento (panel.py y web/panel.css y panel.js,
  con el prefijo del paquete) y cuatro piezas nuevas en el modelo (deslizador, lista desplegable,
  grabador de atajos y línea de dato). De paso: FIX-003 de CoreProgress (Restablecer), FIX-002 de
  Always on Top (seis atajos del editor), FIX-004 y FIX-005 de Edit field (archivos compartidos y
  colores) y FIX-004 de ProFeedback (subcarpetas de sonidos); y los fallos de comprobación que traían
  de fuera del taller (importación fuera de Anki, notas FIX incompletas, colores sin marcar, tipos).
  Pruebas nuevas en pruebas/<paquete>/. Va en el pull request #16.

- 2026-11-09: CoreProgress 1.2.0 con el informe de interfaz, aprendizaje y hábito (aprobado entero,
  también en lo que cambiaba decisiones anteriores): «Difícil» mantiene la racha; el 100 % es lo de
  hoy en el mazo y la barra no retrocede salvo al deshacer; espacio automático para barra y aviso
  (FIX-004); sin destello; avisos a las 5, 10, 20, 30… de 1,5 s; casilla única de celebraciones;
  seis temas como GritMap (Rojo fuego retirado, con aviso); números de los hitos con contraste;
  barra como barra de progreso para el lector de pantalla; textos impersonales con plurales en 60
  idiomas (i18n_texts.py); barra llena y resumen en «¡Enhorabuena!». 15 pruebas.

- 2026-11-10: instrucciones del taller optimizadas con las guías de prompting y con dos sesiones
  reales que aportó la persona (PROP-013). CLAUDE.md: los detalles de diseño se deciden con las guías
  y se cuentan en la entrega; el visto bueno previo queda para cuatro casos con nombre y lo demás
  empieza sin esperar; los encargos largos se cierran y se suben por partes; la ficha de diseño se
  pone al día en la misma entrega. docs/normas-del-taller.md: ejemplos de trato entre etiquetas y
  detalle de las fichas. LEEME.md: «Cómo pedir las cosas», con dos plantillas. El código de los
  complementos no cambia. Va en el pull request #17.

- 2026-11-11: GritMap 4.16.0 con el informe «GritMap 4.15.1: auditoría y rediseño de la interfaz»
  (aprobado entero el 2026-11-10): Opciones por orden de uso, borde que se desvanece, colores de enlace,
  de ejemplo y de apagado, foco solo con el teclado, estado vacío de «Fechas clave» (51 idiomas),
  propuesta de meta sin redondear a 5, icono de opciones a 16 px. FIX-032 y FIX-033. Regla de los
  enlaces en la guía de interfaz, en la paleta, en el contexto común y en el modelo de opciones
  (`09-patron-configuracion.md`, apartado 7.1); ficha de GritMap al día. 70 pruebas. Pendiente, fuera
  del alcance que fijó la persona («solo GritMap»): los paneles copiados en CoreProgress, ProFeedback,
  Hider, Restart, Always on Top y Edit field during review aún usan el azul de acción en sus enlaces, y
  la barra de desplazamiento de Atelier contrasta 1,35 a 1.

- 2026-11-13: Atelier 3.9.1 (petición del cliente): botones de respuesta casi a su tamaño de Anki
  (30 px de alto, 84 de ancho, letra de 12) y «Comenzar a estudiar» algo menor (34 px, letra a
  14/15 del texto). La imagen congelada al empezar a estudiar coincide con un fallo conocido de Anki
  en Windows con el controlador de vídeo Direct3D (pistas del foro oficial): se le propuso cambiarlo
  a OpenGL en Preferencias y, si sigue, probar Anki sin complementos. Se quitaron las menciones a
  docs/referencias que la fusión del pull request #19 había devuelto a CLAUDE.md y docs/LEEME.txt.

- 2026-11-13: Sonidos de consola 1.0.0, nuevo (plan aprobado en docs/sonidos_consola/encargo.md):
  los siete sonidos de la persona, que ella copia en user_files (no van en el repositorio). Excepción
  aprobada: PyQt6.QtMultimedia en empaquetar.py (ALLOWED_DIRECT_QT). 1.2.0: trofeo al terminar un mazo, sin «Nunca», sin entrada en Herramientas y sin destello al abrir la configuración (FIX-002). 1.1.0: snd_system_ok solo al aceptar algo (sin sincronización). 1.0.1: opciones con el panel
  modelo (PROP-012, llegó a main a la vez; FIX-001). 39 pruebas. Falta que la persona
  lo pruebe en Windows con audio.

- 2026-11-13: ProFeedback 2.2.0 (petición del cliente): sonido al fallar («Otra vez»/«Difícil») con
  casilla, lista y «Probar» en «Sonidos al responder», dos sonidos de fallo creados en el taller
  (grave.mp3 y suave.mp3) y textos en los 54 idiomas; FIX-005, ventana de opciones sin destello (el
  mismo arreglo que FIX-002 de Sonidos de consola). 15 pruebas. Va en el pull request #21.

- 2026-11-13: ProFeedback 2.3.0 (petición del cliente): los botones 3D mandan sobre Atelier y no se
  oscurecen con el ratón (FIX-006, !important en buttons.css), forma algo mejorada (canto de 4 px,
  brillo arriba, se elevan 1 px) e insignia «TARJETA NUEVA» en morado (FLAG_7). 18 pruebas.

## En curso

(Nada.)

## Siguiente paso

Nada pendiente de construir. A 2026-11-10, los ocho complementos pasan
`python herramientas/comprobar.py --ci --todos` con Anki 26.09.3, y
`python herramientas/empaquetar.py --revision` acaba en «REVISIÓN: nada pendiente.». Los fallos de
comprobación que seis de ellos traían de fuera del taller se corrigieron el 2026-11-09 (pull request #16).

Pendiente de probar por la persona dentro de Anki, de las entregas del 2026-11-09:

- Las ventanas de opciones nuevas de CoreProgress, ProFeedback, Hider, Restart, Always on Top y Edit
  field during review.
- La barra de CoreProgress 1.2.0, en el repaso y en la pantalla «¡Enhorabuena!».

## Dudas para la persona

- El repositorio es público: cualquiera puede ver el código y descargar los paquetes. Cambiarlo es decisión suya, en GitHub: Settings › General › Danger Zone › Change visibility.
- ProFeedback trae sonidos con nombres de marcas (Mario Bros, Duolingo, Khan). Si son copias de los originales, publicarlos en un repositorio público puede vulnerar derechos de autor; no se ha comprobado su origen.
