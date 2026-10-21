/* ProFeedback · confeti de fin de repaso.

   Un único motor de partículas con dos formas de soltarlas:
   - burst: dos cañones, uno en cada esquina de abajo (al terminar un mazo);
   - rain: lluvia desde arriba durante siete segundos (al terminar todo el día).
   Cada una, en versión «normal» (colores de la paleta) o «gold» (tonos cálidos y brillo
   en el título, para las sesiones sin ningún fallo).

   Colores: se leen de las variables de la paleta de Anki en el momento de soltar el confeti
   (las redefine Nocturne), así que acompañan al modo día o noche; no hay ninguno escrito
   a mano. Con «reducir movimiento» activado en el sistema no hay confeti ni brillo animado.

   Es idempotente: Python lo envía completo cada vez, y si ya está cargado no hace nada. */
(function () {
  'use strict';
  if (window.profeedbackConfetti) {
    return;
  }

  var NORMAL_VARS = [
    '--accent-danger', '--flag-2', '--accent-note',
    '--accent-card', '--state-marked', '--flag-5'
  ];
  var GRAVITY = 0.00125; /* px por ms al cuadrado */
  var RAIN_MS = 7000;
  var RAIN_PER_SECOND = 34;
  var BURST_PIECES = 160;
  var STAR_CHANCE = 0.12;

  var canvas = null;
  var ctx = null;
  var pieces = [];
  var spawner = null;
  var frame = 0;
  var lastTime = 0;
  var scratch = null;

  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function random(min, max) {
    return Math.random() * (max - min) + min;
  }

  /* ── colores ─────────────────────────────────────────────────────────────── */
  function cssVar(name) {
    var value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return value || getComputedStyle(document.body).color;
  }

  /* Cualquier color CSS (hex, rgb, nombre…) a [r, g, b], con un lienzo de 1 píxel. */
  function toRgb(color) {
    if (!scratch) {
      scratch = document.createElement('canvas');
      scratch.width = scratch.height = 1;
    }
    var c = scratch.getContext('2d', { willReadFrequently: true });
    c.clearRect(0, 0, 1, 1);
    c.fillStyle = color;
    c.fillRect(0, 0, 1, 1);
    var d = c.getImageData(0, 0, 1, 1).data;
    return [d[0], d[1], d[2]];
  }

  function mix(a, b, t) {
    return [
      Math.round(a[0] + (b[0] - a[0]) * t),
      Math.round(a[1] + (b[1] - a[1]) * t),
      Math.round(a[2] + (b[2] - a[2]) * t)
    ];
  }

  function css(rgb) {
    return 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
  }

  function palette(kind) {
    if (kind === 'gold') {
      var deep = toRgb(cssVar('--state-buried'));
      var warm = toRgb(cssVar('--flag-2'));
      var white = toRgb(cssVar('--highlight-fg'));
      return [
        deep, warm, mix(deep, warm, 0.5),
        mix(warm, white, 0.35), mix(deep, white, 0.35), mix(warm, white, 0.6)
      ].map(css);
    }
    return NORMAL_VARS.map(function (name) {
      return css(toRgb(cssVar(name)));
    });
  }

  /* ── brillo dorado del título ────────────────────────────────────────────── */
  function goldTitle() {
    if (document.getElementById('profeedback-gold-style')) {
      return;
    }
    var style = document.createElement('style');
    style.id = 'profeedback-gold-style';
    style.textContent =
      '.congrats h1{' +
      'background-image:linear-gradient(100deg,var(--state-buried) 0%,' +
      'var(--flag-2) 30%,' +
      'color-mix(in srgb,var(--flag-2) 55%,var(--highlight-fg)) 50%,' +
      'var(--flag-2) 70%,var(--state-buried) 100%);' +
      'background-size:200% auto;background-position:0% center;' +
      '-webkit-background-clip:text;background-clip:text;' +
      'color:transparent;-webkit-text-fill-color:transparent;' +
      'animation:profeedback-gold-shine 3.6s ease-in-out 2;' +
      'filter:drop-shadow(0 1px 2px var(--shadow-subtle))}' +
      '@keyframes profeedback-gold-shine{0%{background-position:0% center}' +
      '50%{background-position:100% center}100%{background-position:0% center}}' +
      '@media (prefers-reduced-motion:reduce){.congrats h1{animation:none}}';
    (document.head || document.documentElement).appendChild(style);
  }

  /* ── partículas ──────────────────────────────────────────────────────────── */
  function Piece(x, y, vx, vy, color, rain) {
    this.x = x;
    this.y = y;
    this.vx = vx;
    this.vy = vy;
    this.color = color;
    this.rain = rain;
    this.star = Math.random() < STAR_CHANCE;
    this.w = random(7, 13);
    this.h = this.star ? this.w : random(9, 18);
    this.angle = random(0, Math.PI * 2);
    this.spin = random(-0.012, 0.012);
    this.flip = random(0, Math.PI * 2);
    this.flipSpeed = random(0.004, 0.012);
    this.baseX = x;
    this.sway = random(0.0006, 0.0016);
    this.swayAmp = random(20, 55);
    this.age = 0;
  }

  Piece.prototype.update = function (dt) {
    this.age += dt;
    this.angle += this.spin * dt;
    this.flip += this.flipSpeed * dt;
    if (this.rain) {
      this.y += this.vy * dt;
      this.x = this.baseX + Math.sin(this.age * this.sway + this.angle) * this.swayAmp;
    } else {
      this.vy += GRAVITY * dt;
      this.vx *= Math.pow(0.9994, dt);
      this.x += this.vx * dt;
      this.y += this.vy * dt;
    }
  };

  Piece.prototype.gone = function (height, width) {
    return this.y > height + 40 || this.x < -220 || this.x > width + 220;
  };

  function drawStar(c, radius) {
    var spikes = 4;
    var step = Math.PI / spikes;
    var rot = (Math.PI / 2) * 3;
    c.beginPath();
    c.moveTo(0, -radius);
    for (var i = 0; i < spikes; i += 1) {
      c.lineTo(Math.cos(rot) * radius, Math.sin(rot) * radius);
      rot += step;
      c.lineTo(Math.cos(rot) * radius * 0.5, Math.sin(rot) * radius * 0.5);
      rot += step;
    }
    c.closePath();
    c.fill();
  }

  Piece.prototype.draw = function (c, height) {
    var fade = Math.max(0, Math.min(1, (height + 20 - this.y) / 90));
    c.save();
    c.translate(this.x, this.y);
    c.rotate(this.angle);
    c.fillStyle = this.color;
    if (this.star) {
      c.globalAlpha = (0.65 + 0.35 * Math.sin(this.flip * 6)) * fade;
      drawStar(c, this.w / 2);
    } else {
      c.scale(Math.cos(this.flip), 1);
      c.globalAlpha = fade;
      c.fillRect(-this.w / 2, -this.h / 2, this.w, this.h);
    }
    c.restore();
  };

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
    document.body.appendChild(canvas);
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
    window.cancelAnimationFrame(frame);
    frame = 0;
    if (canvas) {
      canvas.remove();
      canvas = null;
      ctx = null;
    }
  }

  function loop(now) {
    var dt = Math.min(48, now - lastTime);
    lastTime = now;
    resize();
    var width = window.innerWidth;
    var height = window.innerHeight;
    ctx.clearRect(0, 0, width, height);
    pieces = pieces.filter(function (piece) {
      piece.update(dt);
      piece.draw(ctx, height);
      return !piece.gone(height, width);
    });
    if (pieces.length > 0 || spawner) {
      frame = window.requestAnimationFrame(loop);
    } else {
      finish();
    }
  }

  function start() {
    if (!frame) {
      lastTime = performance.now();
      frame = window.requestAnimationFrame(loop);
    }
  }

  /* ── formas de soltarlo ──────────────────────────────────────────────────── */
  function burst(kind) {
    if (kind === 'gold') {
      goldTitle();
    }
    if (reducedMotion()) {
      return;
    }
    ensureCanvas();
    resize();
    var colors = palette(kind);
    var width = window.innerWidth;
    var height = window.innerHeight;
    var scale = Math.max(0.6, Math.min(1.2, Math.log(width) / Math.log(1920)));
    for (var i = 0; i < BURST_PIECES; i += 1) {
      var fromLeft = i % 2 === 0;
      var angle = (random(15, 82) * Math.PI) / 180;
      var speed = random(0.9, 1.7) * scale;
      var x = fromLeft ? random(-20, 20) : width + random(-20, 20);
      var y = height * (5 / 7) + random(-20, 20);
      pieces.push(new Piece(
        x, y,
        (fromLeft ? 1 : -1) * Math.cos(angle) * speed,
        -Math.sin(angle) * speed,
        colors[Math.floor(Math.random() * colors.length)],
        false
      ));
    }
    start();
  }

  function rain(kind) {
    if (kind === 'gold') {
      goldTitle();
    }
    if (reducedMotion()) {
      return;
    }
    ensureCanvas();
    resize();
    var colors = palette(kind);
    var width = window.innerWidth;
    var height = window.innerHeight;
    function add(y) {
      pieces.push(new Piece(
        random(0, width), y, 0, random(0.1, 0.22),
        colors[Math.floor(Math.random() * colors.length)],
        true
      ));
    }
    for (var i = 0; i < 44; i += 1) {
      add(random(-40, height * 0.9));
    }
    var startedAt = performance.now();
    var carry = 0;
    var previous = startedAt;
    window.clearInterval(spawner);
    spawner = window.setInterval(function () {
      var now = performance.now();
      if (now - startedAt > RAIN_MS) {
        window.clearInterval(spawner);
        spawner = null;
        return;
      }
      carry += (RAIN_PER_SECOND * (now - previous)) / 1000;
      previous = now;
      while (carry >= 1) {
        add(-20);
        carry -= 1;
      }
    }, 50);
    start();
  }

  window.profeedbackConfetti = { burst: burst, rain: rain };
})();
