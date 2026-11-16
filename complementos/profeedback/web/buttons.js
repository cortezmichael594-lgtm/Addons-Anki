/* ProFeedback · pulsado de los botones y ajuste del texto al botón.

   1. Desde la 2.5.0 (informe 2.4.0, apartado 8.5) la respuesta sale en el instante en que se
      suelta el botón, sin la espera de 0,1 s de antes: el hundimiento se ve mientras el dedo
      está abajo (:active en buttons.css). Soltar fuera del botón no responde. Un segundo
      clic antes de 0,4 s se ignora. Los atajos de teclado no pasan por aquí.
   2. Ajusta el tamaño de la letra cuando la palabra no cabe: el botón nunca cambia de forma,
      se encoge el texto.

   Anki cambia el contenido de la barra al pasar de pregunta a respuesta, así que un
   observador vuelve a preparar los botones nuevos. El script es idempotente: si Anki lo
   inyecta otra vez, no duplica nada. */
(function () {
  'use strict';
  if (window.profeedbackButtonsReady) {
    return;
  }
  window.profeedbackButtonsReady = true;

  var DOUBLE_CLICK = 400;
  var MIN_SIZE = 9;
  /* El filtro del doble clic es solo para responder; «Editar» y «Más» abren su ventana al
     momento. */
  var WRAP_SELECTOR =
    "#ansbut,button[onclick*='ease1'],button[onclick*='ease2']," +
    "button[onclick*='ease3'],button[onclick*='ease4']";
  var FIT_SELECTOR =
    WRAP_SELECTOR + ",button[onclick*='edit'],button[onclick*='more']";

  function wrap(button) {
    if (!button || button.dataset.profeedbackWrapped === '1') {
      return;
    }
    var original = button.onclick;
    if (!original) {
      return;
    }
    button.dataset.profeedbackWrapped = '1';
    button.onclick = null;
    button.addEventListener(
      'click',
      function (event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        /* Doble clic: la primera respuesta ya está en camino, la segunda sobra. */
        var now = Date.now();
        if (now - (Number(button.dataset.profeedbackLast) || 0) < DOUBLE_CLICK) {
          return;
        }
        button.dataset.profeedbackLast = String(now);
        original.call(button, event);
      },
      true
    );
  }

  /* Mide solo el texto suelto del botón: el intervalo y los recuentos van en spans
     colocados por encima y no cuentan para el ancho disponible. */
  function textWidth(button) {
    var range = document.createRange();
    var width = 0;
    button.childNodes.forEach(function (node) {
      if (node.nodeType === 3 && node.textContent.trim() !== '') {
        range.selectNodeContents(node);
        width += range.getBoundingClientRect().width;
      }
    });
    return width;
  }

  function fit(button) {
    button.style.fontSize = '';
    var style = window.getComputedStyle(button);
    var base = parseFloat(style.fontSize);
    var inner =
      button.clientWidth -
      parseFloat(style.paddingLeft) -
      parseFloat(style.paddingRight);
    if (!(base > 0) || !(inner > 0)) {
      return;
    }
    var width = textWidth(button);
    if (width === 0 || width <= inner) {
      return;
    }
    var size = Math.max(MIN_SIZE, Math.floor(((base * inner * 0.98) / width) * 10) / 10);
    button.style.fontSize = size + 'px';
  }

  function refresh() {
    document.querySelectorAll(WRAP_SELECTOR).forEach(wrap);
    document.querySelectorAll(FIT_SELECTOR).forEach(fit);
  }

  var pending = null;
  function later() {
    window.clearTimeout(pending);
    pending = window.setTimeout(refresh, 30);
  }

  function start() {
    refresh();
    new MutationObserver(later).observe(document.body, {
      childList: true,
      subtree: true
    });
    window.addEventListener('resize', later);
    /* La tipografía propia puede llegar después del primer pintado y cambia lo que ocupa
       el texto: se vuelve a medir cuando esté lista. */
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(refresh).catch(function () {});
    }
  }

  if (document.readyState !== 'loading') {
    start();
  } else {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  }
})();
