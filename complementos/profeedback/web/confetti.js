/* ProFeedback · celebración al terminar: confeti, brillo del título y destellos fijos.

   Versión 2.6.0 (informe «Rediseño de color y forma: ProFeedback 2.5.0», aprobado entero el
   2026-11-17, apartados 2.5, 2.6, 3.2, 5.3, 5.4 y 8.7 a 8.9). Dos formas de soltarlo:
   - burst (fin de mazo): 72 piezas desde dos cañones, a 24 px de las esquinas de abajo, en dos
     ráfagas dentro de 0,12 s; 2,4 s en total, desvaneciéndose desde 2,0.
   - rain (fin del día): 120 piezas que entran por arriba repartidas en 0,9 s; 3,8 s en total,
     desvaneciéndose desde 3,4. El título de la pantalla pasa a dorado y lo cruza una banda
     más clara una sola vez (1,2 s, desde los 0,3 s); después se queda dorado y quieto.

   Formas: tiras de 6 × 14 px con esquinas de 2, círculos de 8 y destellos de cuatro puntas de
   12 (los de CoreProgress); en la lluvia, también estrellas de cinco puntas de 13. Tamaño
   ±15 % al azar. Cada pieza sale disparada, frena con el aire (frenada exponencial de
   0,16 s), cae despacio, se mece de lado y gira como papel; su posición depende solo del
   tiempo, con fórmulas cerradas. Como mucho 1,4 vueltas por segundo y 14 px por pieza: sin
   destellos peligrosos.

   Colores: llegan de Python (look.py) en JSON, de día y de noche; aquí no hay ninguno
   escrito a mano. Con «reducir movimiento» no hay confeti ni brillo: tres destellos fijos
   encima del título. Con el contraste alto de Windows, ni confeti ni destellos y el título en
   el color del texto.

   Es idempotente: Python lo envía completo cada vez, y si ya está cargado no se redefine. */
(function () {
  'use strict';
  if (window.profeedbackConfetti) {
    return;
  }

  var TAU = Math.PI * 2;
  var DRAG = 0.16; /* s: frenada exponencial del impulso */
  var EFFECTS = {
    burst: { pieces: 72, duration: 2.4, fadeFrom: 2.0 },
    rain: { pieces: 120, duration: 3.8, fadeFrom: 3.4 }
  };
  /* Reparto de formas: tira, círculo, destello y estrella. */
  var SHAPES = {
    burst: [['strip', 0.5], ['circle', 0.25], ['sparkle', 0.25]],
    rain: [['strip', 0.4], ['circle', 0.2], ['sparkle', 0.25], ['star', 0.15]]
  };

  var canvas = null;
  var ctx = null;
  var pieces = [];
  var frame = 0;
  var startedAt = 0;
  var current = null;

  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function forcedColors() {
    return !!(window.matchMedia && window.matchMedia('(forced-colors: active)').matches);
  }

  function isNight() {
    var html = document.documentElement;
    var body = document.body;
    return html.classList.contains('night-mode') ||
      !!(body && (body.classList.contains('night_mode') || body.classList.contains('nightMode')));
  }

  function random(min, max) {
    return Math.random() * (max - min) + min;
  }

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function shapeFor(effect) {
    var roll = Math.random();
    var table = SHAPES[effect];
    for (var i = 0; i < table.length; i += 1) {
      roll -= table[i][1];
      if (roll < 0) {
        return table[i][0];
      }
    }
    return table[0][0];
  }

  /* ── estilo: título dorado y destellos fijos ─────────────────────────────── */
  /* Tres destellos de cuatro puntas (10, 12 y 10 px) en una imagen SVG de 44 × 12 px. */
  function sparklesSvg(colors) {
    var shapes = colors.map(function (color, i) {
      var cx = 6 + i * 16;
      var r = i === 1 ? 6 : 5;
      var points = [];
      for (var k = 0; k < 8; k += 1) {
        var radius = k % 2 === 0 ? r : r * 0.3;
        var a = (k * Math.PI) / 4 - Math.PI / 2;
        points.push((cx + Math.cos(a) * radius).toFixed(2) + ',' + (6 + Math.sin(a) * radius).toFixed(2));
      }
      return '<polygon fill="' + color + '" points="' + points.join(' ') + '"/>';
    }).join('');
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="44" height="12" viewBox="0 0 44 12">' +
      shapes + '</svg>';
    return 'url("data:image/svg+xml,' + encodeURIComponent(svg) + '")';
  }

  function addStyle(id, css) {
    var old = document.getElementById(id);
    if (old) {
      old.remove();
    }
    var style = document.createElement('style');
    style.id = id;
    style.textContent = css;
    (document.head || document.documentElement).appendChild(style);
  }

  var NIGHT = ':is(.night-mode,.night_mode,.nightMode) ';

  /* Título del fin del día: el oro de CoreProgress y una sola pasada de brillo. */
  function goldTitle(colors) {
    addStyle(
      'profeedback-gold-style',
      '.congrats h1{--profeedback-title:' + colors.title.day + ';--profeedback-band:' + colors.band.day + '}' +
      NIGHT + '.congrats h1{--profeedback-title:' + colors.title.night + ';--profeedback-band:' +
      colors.band.night + '}' +
      '.congrats h1{color:var(--profeedback-title);background-image:linear-gradient(100deg,' +
      'var(--profeedback-title) 0%,var(--profeedback-title) 40%,var(--profeedback-band) 50%,' +
      'var(--profeedback-title) 60%,var(--profeedback-title) 100%);background-size:250% 100%;' +
      'background-position:100% 0;-webkit-background-clip:text;background-clip:text;' +
      '-webkit-text-fill-color:transparent;' +
      'animation:profeedback-gold-shine 1.2s cubic-bezier(.2,.8,.2,1) .3s 1 both}' +
      '@keyframes profeedback-gold-shine{from{background-position:100% 0}to{background-position:0% 0}}' +
      '@media (prefers-reduced-motion:reduce){.congrats h1{animation:none;background:none;' +
      '-webkit-text-fill-color:currentColor}}' +
      '@media (forced-colors:active){.congrats h1{animation:none;background:none;' +
      'color:CanvasText;-webkit-text-fill-color:CanvasText}}'
    );
  }

  /* «Reducir movimiento»: tres destellos fijos encima del título, que no desplazan nada. */
  function fixedSparkles(list) {
    addStyle(
      'profeedback-sparkles-style',
      '.congrats h1{position:relative}' +
      '.congrats h1::before{content:"";position:absolute;left:50%;bottom:100%;width:44px;height:12px;' +
      'transform:translate(-50%,-6px);background:' + sparklesSvg(list.day) + ' no-repeat;' +
      'pointer-events:none}' +
      NIGHT + '.congrats h1::before{background-image:' + sparklesSvg(list.night) + '}' +
      '@media (forced-colors:active){.congrats h1::before{display:none}}'
    );
  }

  /* ── piezas ──────────────────────────────────────────────────────────────── */
  function burstPiece(i, width, height, colors) {
    var left = i % 2 === 0;
    var angle = (random(40, 75) * Math.PI) / 180;
    return {
      shape: shapeFor('burst'),
      color: pick(colors),
      t0: i < 36 ? random(0, 0.02) : random(0.06, 0.12),
      x0: left ? 24 : width - 24,
      y0: height - 24,
      dx: (left ? 1 : -1) * Math.cos(angle),
      dy: -Math.sin(angle),
      reach: random(0.4, 0.85) * height,
      fall: random(0.14, 0.24) * height,
      swayAmp: random(6, 20),
      swayHz: random(0.5, 1.2),
      phase: random(0, TAU),
      flipHz: random(0.6, 1.4),
      spin: random(60, 240) * (Math.random() < 0.5 ? -1 : 1),
      rot0: random(0, 360),
      size: random(0.85, 1.15)
    };
  }

  function rainPiece(width, height, colors) {
    return {
      shape: shapeFor('rain'),
      color: pick(colors),
      t0: random(0, 0.9),
      x0: random(0, width),
      y0: -random(20, 60),
      dx: 0,
      dy: 1,
      reach: random(0.05, 0.45) * height,
      fall: random(0.15, 0.33) * height,
      swayAmp: random(12, 38),
      swayHz: random(0.4, 1.0),
      phase: random(0, TAU),
      flipHz: random(0.6, 1.4),
      spin: random(60, 240) * (Math.random() < 0.5 ? -1 : 1),
      rot0: random(0, 360),
      size: random(0.85, 1.15)
    };
  }

  /* Posición en el instante t (s): impulso que frena, caída lenta y vaivén. */
  function place(p, t) {
    var u = t - p.t0;
    var push = p.reach * (1 - Math.exp(-u / DRAG));
    var sway = p.swayAmp * Math.sin(TAU * p.swayHz * u + p.phase) * Math.min(1, u / 0.4);
    return {
      x: p.x0 + p.dx * push + sway,
      y: p.y0 + p.dy * push + p.fall * u,
      rot: ((p.rot0 + p.spin * u) * Math.PI) / 180,
      flip: Math.cos(TAU * p.flipHz * u + p.phase)
    };
  }

  function star(c, points, outer, inner) {
    c.beginPath();
    for (var i = 0; i < points * 2; i += 1) {
      var r = i % 2 === 0 ? outer : inner;
      var a = (i * Math.PI) / points - Math.PI / 2;
      if (i === 0) {
        c.moveTo(Math.cos(a) * r, Math.sin(a) * r);
      } else {
        c.lineTo(Math.cos(a) * r, Math.sin(a) * r);
      }
    }
    c.closePath();
    c.fill();
  }

  function draw(c, p, at) {
    c.save();
    c.translate(at.x, at.y);
    c.rotate(at.rot);
    c.scale(p.size, p.size);
    c.fillStyle = p.color;
    if (p.shape === 'strip') {
      c.scale(1, at.flip);
      c.beginPath();
      if (c.roundRect) {
        c.roundRect(-3, -7, 6, 14, 2);
      } else {
        c.rect(-3, -7, 6, 14);
      }
      c.fill();
    } else if (p.shape === 'circle') {
      c.scale(1, Math.max(0.15, Math.abs(at.flip)));
      c.beginPath();
      c.arc(0, 0, 4, 0, TAU);
      c.fill();
    } else if (p.shape === 'sparkle') {
      star(c, 4, 6, 1.8);
    } else {
      star(c, 5, 6.5, 2.6);
    }
    c.restore();
  }

  /* ── lienzo y bucle ──────────────────────────────────────────────────────── */
  function ensureCanvas() {
    if (canvas) {
      return;
    }
    canvas = document.createElement('canvas');
    canvas.id = 'profeedback-confetti';
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText =
      'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1000';
    (document.body || document.documentElement).appendChild(canvas);
    ctx = canvas.getContext('2d');
  }

  function resize() {
    var dpr = window.devicePixelRatio || 1;
    var w = Math.round(window.innerWidth * dpr);
    var h = Math.round(window.innerHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function finish() {
    if (frame) {
      window.cancelAnimationFrame(frame);
    }
    frame = 0;
    pieces = [];
    current = null;
    if (canvas) {
      canvas.remove();
      canvas = null;
      ctx = null;
    }
  }

  function loop(now) {
    frame = 0;
    if (!canvas || !current) {
      finish();
      return;
    }
    var t = (now - startedAt) / 1000;
    if (t >= current.duration) {
      finish();
      return;
    }
    resize();
    var width = window.innerWidth;
    var height = window.innerHeight;
    ctx.clearRect(0, 0, width, height);
    ctx.globalAlpha = t <= current.fadeFrom ? 1 :
      Math.max(0, 1 - (t - current.fadeFrom) / (current.duration - current.fadeFrom));
    for (var i = 0; i < pieces.length; i += 1) {
      var p = pieces[i];
      if (t < p.t0) {
        continue;
      }
      var at = place(p, t);
      if (at.y > height + 30 || at.x < -40 || at.x > width + 40) {
        continue;
      }
      draw(ctx, p, at);
    }
    frame = window.requestAnimationFrame(loop);
  }

  function launch(effect, kind, colors) {
    var gold = kind === 'gold';
    if (gold && colors) {
      goldTitle(colors);
    }
    if (forcedColors() || !colors) {
      return;
    }
    if (reducedMotion()) {
      fixedSparkles(gold ? colors.sparklesGold : colors.sparklesDeck);
      return;
    }
    finish();
    ensureCanvas();
    resize();
    current = EFFECTS[effect];
    var width = window.innerWidth;
    var height = window.innerHeight;
    var night = isNight();
    var source = gold ? colors.gold : colors.deck;
    var list = night ? source.night : source.day;
    for (var i = 0; i < current.pieces; i += 1) {
      pieces.push(effect === 'burst' ? burstPiece(i, width, height, list) : rainPiece(width, height, list));
    }
    startedAt = performance.now();
    frame = window.requestAnimationFrame(loop);
  }

  window.profeedbackConfetti = {
    burst: function (kind, colors) { launch('burst', kind, colors); },
    rain: function (kind, colors) { launch('rain', kind, colors); }
  };
})();
