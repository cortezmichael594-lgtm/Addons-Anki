"""Everything that renders inside the reviewer web view.

The bar is built once per review session and updated in place (no per-card
rebuild, hence no flicker). All rendering lives in a small ``window._cprog``
namespace; ``ensure()`` heals the DOM if something removed it and re-syncs the
colors with the card currently on screen.

Surface colors (track, pending checkpoints, light/dark choice) come from the
CARD'S REAL RENDERED BACKGROUND: on build and on every question the JS samples
getComputedStyle(.card/body).backgroundColor, decides dark-vs-light by
luminance, and derives the channel by lightly shading that color. A template
may override the channel by defining --cprog-track on .card. Anki's
theme_did_change (pushed from Python) just triggers a re-sample.

HISTORIAL: antes la barra coloreaba con variables del TEMA de Anki
(--canvas-inset/--border); si la tarjeta imponia su propio fondo (plantillas
con background propio), la barra chocaba con ella. Muestrear el fondo real
armoniza con cualquier tarjeta, coincida o no con el tema.

HISTORIAL: el muestreo era correcto pero llegaba DEMASIADO PRONTO. El CSS de
la plantilla no esta en la pagina cuando Anki pide la pregunta: viaja dentro
del propio HTML de la tarjeta ("<style>" + contenido, ver
TemplateRenderOutput.question_and_style en pylib/anki/template.py) y Anki lo
inserta en #qa un instante despues, al terminar su fundido. Midiendo antes de
ese momento se media el lienzo del TEMA de Anki y no el fondo de la tarjeta
(comprobado sobre la captura del usuario: canal gris #3C3C3C, que es
exactamente el derivado de #2C2C2C, sobre una tarjeta pintada en #12161F), y
la correccion no llegaba hasta la pregunta siguiente: de ahi el "a veces si y
a veces no" y el repintado visible al responder la primera tarjeta de la
sesion. Ahora el JS: (1) comprueba que la tarjeta este realmente en pantalla
antes de dar por buena una medida; (2) mientras no lo este pinta el canal
translucido, que encaja con cualquier fondo; (3) vuelve a medir en cuanto la
tarjeta llega, avisado por un observador de #qa y de las clases de body/html
mas una tanda de reintentos cortos. El resultado no depende ya del momento en
que Python inyecta la barra, que es lo que variaba entre arranques.

Python never builds HTML by hand: data travels as JSON, so quoting is always
valid.
"""

# Historial de correcciones de este archivo:
# FIX-001 (2026-07-23) — Tirón/congelación de la barra en la primera tarjeta.

from __future__ import annotations

import json

from aqt import mw

from .effects import STREAK_LABEL_MIN_LEFT_PERCENT
from .errors import report
from .palettes import StyleBundle

# --- static stylesheet (raw string: no escaping surprises) -------------------
_STATIC_CSS = r"""
#qa{padding-top:var(--cprog-push,0px);}
#_mark,#_flag{top:var(--cprog-mark-top,30px) !important;}
img#star{top:var(--cprog-mark-top,30px) !important;}
.cprog-sheen{position:absolute;top:-25%;height:150%;width:22%;left:-30%;
 background:linear-gradient(90deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.5) 50%,rgba(255,255,255,0) 100%);
 transform:skewX(-18deg);opacity:0;animation:cprogSheen 9s ease-in-out infinite;}
@keyframes cprogSheen{0%{left:-30%;opacity:0;}6%{opacity:.22;}22%{opacity:.22;}
 32%{left:130%;opacity:0;}100%{left:130%;opacity:0;}}
@keyframes cprogGlow{0%{filter:brightness(1);}35%{filter:brightness(1.10);}100%{filter:brightness(1);}}
@keyframes cprogPop{0%{transform:scale(1);}45%{transform:scale(1.07);}100%{transform:scale(1);}}
@keyframes cprogSpark{0%{transform:translate(-50%,-50%) scale(.2) rotate(0deg);opacity:1;}
 100%{transform:translate(calc(-50% + var(--dx)),calc(-50% + var(--dy))) scale(1) rotate(90deg);opacity:0;}}
.cprog-spark{position:absolute;top:50%;width:12px;height:12px;pointer-events:none;color:#fff;
 font-size:12px;line-height:12px;text-align:center;text-shadow:0 0 4px rgba(255,255,255,.9);
 animation:cprogSpark .7s ease-out forwards;}
@media (prefers-reduced-motion: reduce){.cprog-sheen{animation:none;left:24%;opacity:.12;}}
"""
# HISTORIAL: cprogGlow usaba brightness(1.45)+drop-shadow animado: caro por
# frame (tirones) y llamativo; ahora brightness suave. cprogPop llego a 1.28
# con rebote; debe ser un adorno que no distraiga: 1.07 sin rebote.

# --- the namespace: build / update / heal / celebrate ------------------------
_BOOTSTRAP_JS = r"""
(function(){
  if(!window._cprog){ window._cprog={}; }
  var C=window._cprog;
  C.WRAP='_cprogBar'; C.TRACK='_cprogTrack'; C.FILL='_cprogFill'; C.LABEL='_cprogLabel'; C.STYLE='_cprogStyle';
  C.CP='cprog-cp';
  C.FONT='"Nunito","Segoe UI Semibold","SF Pro Text",system-ui,-apple-system,sans-serif';

  C._err=function(e){ try{ console.log('[coreprogress]', e); }catch(_){ } };

  // HISTORIAL: adivinar el modo con matchMedia/clases fallaba cuando el SO y
  // Anki no coincidian (colores del modo contrario, numeros invisibles). El
  // modo lo empuja Python (_forceDark) y, por encima, manda la luminancia del
  // fondo REAL de la tarjeta (_surfDark), muestreado abajo.
  C.isDark=function(){
    if(C._forceDark===true) return true;
    if(C._forceDark===false) return false;
    try{
      var b=document.body;
      if(b && (b.classList.contains('night-mode')||b.classList.contains('nightMode'))) return true;
      if(document.documentElement.getAttribute('data-bs-theme')==='dark') return true;
      return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }catch(e){ return false; }
  };
  C.setDark=function(d){
    try{ C._forceDark=!!d; C._lastDark=C.isDark(); C.reapply(); }catch(e){ C._err(e); }
  };
  C.reduceMotion=function(){
    try{ return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){ return false; }
  };
  C.cardVar=function(name, fallback){
    try{
      var el=document.querySelector('.card')||document.body;
      var v=getComputedStyle(el).getPropertyValue(name).trim();
      return v||fallback;
    }catch(e){ return fallback; }
  };
  C.injectStyle=function(css){
    try{
      if(document.getElementById(C.STYLE)) return;
      var st=document.createElement('style'); st.id=C.STYLE; st.textContent=css;
      (document.head||document.documentElement).appendChild(st);
    }catch(e){ C._err(e); }
  };

  // ---- fondo real de la tarjeta -> luminancia -> derivados -----------------
  C._parseColor=function(s){
    try{
      var m=/rgba?\(([^)]+)\)/.exec(s||'');
      if(!m) return null;
      var p=m[1].split(',');
      var a=(p.length>3)?parseFloat(p[3]):1;
      return {r:parseFloat(p[0]),g:parseFloat(p[1]),b:parseFloat(p[2]),a:isNaN(a)?1:a};
    }catch(e){ return null; }
  };
  C._over=function(top, base){
    // Composicion normal: color de encima, con su alfa, sobre el de debajo.
    var a=top.a+base.a*(1-top.a);
    if(a<=0){ return {r:0,g:0,b:0,a:0}; }
    var mix=function(t,b){ return (t*top.a+b*base.a*(1-top.a))/a; };
    return {r:mix(top.r,base.r), g:mix(top.g,base.g), b:mix(top.b,base.b), a:a};
  };
  // HISTORIAL (ver cabecera): el estilo de la plantilla llega DENTRO del HTML
  // de la pregunta y Anki lo inserta en #qa un instante despues de pedirla;
  // medir antes devuelve el lienzo del tema y no el fondo de la tarjeta. Esta
  // prueba dice si la tarjeta ya esta en pantalla: Anki pone la clase "card"
  // en <body> y llena #qa en el mismo paso en que aplica ese estilo.
  C._cardReady=function(){
    try{
      if(document.body && document.body.classList.contains('card')) return true;
      var qa=document.getElementById('qa');
      return !!(qa && qa.firstChild);
    }catch(e){ return false; }
  };
  C._sampleBg=function(){
    try{
      var els=[document.querySelector('.card'), document.body, document.documentElement];
      var seen=[], acc=null;
      for(var i=0;i<els.length;i++){
        var el=els[i];
        if(!el || seen.indexOf(el)>=0) continue;
        seen.push(el);
        var c=C._parseColor(getComputedStyle(el).backgroundColor);
        if(!c || c.a<=0.02) continue;
        acc=acc?C._over(acc,c):c;
        if(acc.a>=0.995) return acc;
      }
      // Plantilla translucida de arriba abajo: se apoya en el lienzo del modo.
      if(acc){ return C._over(acc, C.isDark()?{r:0,g:0,b:0,a:1}:{r:255,g:255,b:255,a:1}); }
    }catch(e){ }
    return null;
  };
  C._lum=function(c){ return (0.2126*c.r+0.7152*c.g+0.0722*c.b)/255; };
  C._shade=function(c,f){
    var m=function(v){ return Math.round(f>0 ? v+(255-v)*f : v*(1+f)); };
    return 'rgb('+m(c.r)+','+m(c.g)+','+m(c.b)+')';
  };
  C._surface=function(){
    var ready=C._cardReady();
    return {ready:ready, bg:ready?C._sampleBg():null, ovr:C.cardVar('--cprog-track','')};
  };
  C._keyOf=function(s){
    var c=s.bg?(Math.round(s.bg.r)+','+Math.round(s.bg.g)+','+Math.round(s.bg.b)):'x';
    return (s.ready?'1':'0')+':'+c+'|'+(s.ovr||'');
  };
  C._m=function(bundle){
    var dark=(C._surfDark!==undefined && C._surfDark!==null)?C._surfDark:C.isDark();
    return dark?bundle.dark:bundle.light;
  };

  C.paintTrack=function(){
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    // FIX-001: medida cacheada del canal y de los hitos. Se toma aqui
    // (construccion, repintado, cambio de tema, redimension), nunca en
    // apply(), que corre en cada respuesta; asi actualizar el progreso no
    // vuelve a leer offsetWidth/offsetLeft y no fuerza maquetacion mientras
    // el relleno se anima.
    C._trackW=tr.offsetWidth||0;
    var cps=tr.getElementsByClassName(C.CP);
    for(var ci=0;ci<cps.length;ci++){ cps[ci]._cpLeft=cps[ci].offsetLeft; }
    var s=C._surface();
    var bg=s.bg;
    var dark=bg?(C._lum(bg)<0.5):C.isDark();
    C._surfDark=dark;
    C._bgKey=C._keyOf(s);
    // Override opcional por plantilla: si .card define --cprog-track, manda.
    // Sin medida fiable todavia (la tarjeta no esta en pantalla), el canal va
    // translucido: se apoya en lo que haya pintado y no puede desentonar.
    C._trackBg=s.ovr||(bg?C._shade(bg, dark?0.075:-0.075)
                          :(dark?'rgba(255,255,255,0.06)':'rgba(0,0,0,0.06)'));
    C._trackShadow=dark
      ?'inset 0 2px 6px rgba(0,0,0,0.55), inset 0 1px 2px rgba(0,0,0,0.40)'
      :'inset 0 2px 5px rgba(0,0,0,0.13), inset 0 1px 2px rgba(0,0,0,0.09)';
    // El primer pintado es seco; cualquier correccion posterior funde, para que
    // un ajuste tardio no se perciba como un salto.
    if(C._trackPainted){ tr.style.transition='background-color .3s ease, box-shadow .3s ease'; }
    tr.style.background=C._trackBg;
    tr.style.boxShadow=C._trackShadow;
    C._trackPainted=true;
    // La barra no se enseña hasta tener una medida de verdad: asi nunca se ve
    // un color provisional corrigiendose en pantalla.
    if(s.ready){ C.reveal(); }
  };
  C.reveal=function(){
    try{
      var w=document.getElementById(C.WRAP);
      if(w && w.style.opacity!=='1'){ w.style.opacity='1'; }
    }catch(e){ C._err(e); }
  };

  C.sync=function(){
    try{
      if(C._keyOf(C._surface())!==C._bgKey){ C.reapply(); }
    }catch(e){ C._err(e); }
  };
  // Una comprobacion por par de fotogramas como mucho: los observadores pueden
  // dispararse en rafaga y cada medida cuesta un recalculo de estilo.
  C._syncSoon=function(){
    if(C._syncQ) return;
    C._syncQ=true;
    var done=false;
    var run=function(){ if(done) return; done=true; C._syncQ=false; C.sync(); };
    try{
      if(window.requestAnimationFrame){
        requestAnimationFrame(function(){ requestAnimationFrame(run); });
        // Con la ventana oculta no se dibujan fotogramas: red de seguridad.
        setTimeout(run,250);
      }else{ setTimeout(run,16); }
    }catch(e){ C._syncQ=false; C.sync(); }
  };
  C._watchQa=function(){
    if(C._qaObs) return;
    try{
      var qa=document.getElementById('qa'); if(!qa) return;
      new MutationObserver(function(){ C._syncSoon(); }).observe(qa,{childList:true});
      C._qaObs=true;
    }catch(e){ }
  };
  // Reintentos cortos al construir la barra y en cada pregunta: cubren el
  // fundido de Anki, las fuentes web y los scripts propios de la plantilla.
  C._settle=function(){
    try{
      C._watchQa();
      if(C._settleT){ for(var i=0;i<C._settleT.length;i++){ clearTimeout(C._settleT[i]); } }
      C._settleT=[];
      // FIX-001: el momento fiable para remuestrear es el evento de #qa (Anki
      // acaba de insertar el HTML+estilo de la tarjeta) y el rAF posterior,
      // ambos ya cubiertos. Estos tres relojes son solo la red de seguridad
      // para CSS/fuentes tardias; antes eran seis y cada uno leia el estilo
      // (recalculo forzado), compitiendo con la animacion del relleno.
      // Regla: remuestrear el fondo por eventos reales de render, no a base de
      //   relojes; los pocos que queden son red de seguridad, no el mecanismo.
      var delays=[0,150,500];
      var tick=function(){ C.sync(); };
      for(var j=0;j<delays.length;j++){ C._settleT.push(setTimeout(tick, delays[j])); }
      C._syncSoon();
    }catch(e){ C._err(e); }
  };

  C.build=function(args){
    try{
      C._args=args; C._minLeft=(args.minLeft||2.8); C._prevP=null; C._last=null;
      if(typeof args.dark==='boolean'){ C._forceDark=args.dark; }
      // Si hay un aviso de racha/record visible, sobrevive a la reconstruccion
      // (p. ej. cambio de color en mitad del repaso): solo cambia de color y su
      // reloj de visibilidad sigue corriendo, sin reiniciarse.
      // HISTORIAL: solo se conserva si los efectos siguen ACTIVOS. Al desmarcar
      // "Efectos de racha y record" durante el repaso se reconstruye la barra;
      // sin esta condicion la etiqueta visible reaparecia y se quedaba hasta la
      // siguiente tarjeta, en vez de irse al instante con el resto de efectos.
      var keepText='', keepShownAt=null;
      var effectsOn=(args.effects!==false);
      var oldLbl=document.getElementById(C.LABEL);
      if(effectsOn && oldLbl && oldLbl.style.opacity==='1' && oldLbl.textContent){
        keepText=oldLbl.textContent; keepShownAt=C._labelShownAt||null;
      }
      var prev=document.getElementById(C.WRAP); if(prev) prev.remove();

      var wrap=document.createElement('div'); wrap.id=C.WRAP;
      wrap.style.cssText='position:fixed;top:0;left:0;right:0;z-index:99999;padding:10px 18px;pointer-events:none;'
        +'opacity:0;transition:opacity .28s ease;';

      var track=document.createElement('div'); track.id=C.TRACK;
      // --- FIX-001 (2026-07-23) --------------------------------------
      // Sintoma: al responder la primera tarjeta la barra daba un tiron.
      // Causa: animar el ancho del relleno recalcula la maquetacion en
      //   cada fotograma y esa recalcula subia hasta la pagina entera,
      //   compitiendo con MathJax y el remuestreo de color.
      // Regla: toda animacion de tamano vive dentro de un limite de
      //   maquetacion (contain:layout); nunca dejar que un cambio de
      //   ancho/alto de la barra obligue a remaquetar la pagina del repaso.
      // ---------------------------------------------------------------
      track.style.cssText='position:relative;width:100%;box-sizing:border-box;height:'+args.barHeight+'px;'
        +'border-radius:'+args.radius+'px;overflow:visible;contain:layout;';
      C._trackPainted=false;

      var fill=document.createElement('div'); fill.id=C.FILL;
      fill.style.cssText='position:relative;height:100%;width:0%;border-radius:'+args.fillRadius+'px;overflow:hidden;'
        +'transition:width .4s cubic-bezier(.5,0,.2,1),box-shadow .5s ease;';

      // HISTORIAL: los degradados NO se pueden transicionar en CSS (saltan en
      // seco mientras la sombra transiciona: se percibe como "lag"). Los
      // cambios de color funden a traves de esta capa.
      var xf=document.createElement('div');
      xf.style.cssText='position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:0;';
      fill.appendChild(xf);
      C._xf=xf; C._curBg=null;

      var gloss=document.createElement('div');
      gloss.style.cssText='position:absolute;inset:0;border-radius:inherit;pointer-events:none;'
        +'background:linear-gradient(180deg,rgba(255,255,255,.30),rgba(255,255,255,0) 55%);';
      fill.appendChild(gloss);
      var sheen=document.createElement('div'); sheen.className='cprog-sheen'; fill.appendChild(sheen);
      track.appendChild(fill);

      if(args.showCheckpoints && args.checkpoints){
        for(var i=0;i<args.checkpoints.length;i++){
          var cp=args.checkpoints[i];
          var el=document.createElement('div'); el.className=C.CP;
          el.setAttribute('data-pos', cp.pos); el.setAttribute('data-reached','0');
          // Alineacion por borde derecho: cuando has despachado N, el relleno
          // se detiene exactamente en la bolita N.
          // HISTORIAL: la bolita era un circulo de tamaño fijo y en mazos
          // grandes el numero se salia por los lados (se veia con hitos de
          // cuatro cifras). Ahora el ancho lo manda el numero: circulo con una
          // o dos cifras y pastilla en cuanto hace falta, sin desbordar.
          el.style.cssText='position:absolute;top:50%;left:'+cp.pos+'%;transform:translate(-100%,-50%);'
            +'height:'+args.cpSize+'px;pointer-events:none;';
          var inner=document.createElement('div');
          inner.style.cssText='height:100%;min-width:'+args.cpSize+'px;box-sizing:border-box;'
            +'padding:0 5px;border-radius:999px;'
            +'display:flex;align-items:center;justify-content:center;line-height:1;'
            +'font-size:'+args.cpFont+'px;font-weight:700;'
            +'font-family:'+C.FONT+';'
            +'transition:color .35s ease,box-shadow .35s ease,background-color .3s ease;';
          inner.textContent=String(Math.round(cp.num));
          el.appendChild(inner);
          track.appendChild(el);
        }
      }

      var label=document.createElement('div'); label.id=C.LABEL;
      label.style.cssText='position:absolute;top:100%;left:'+C._minLeft+'%;transform:translateX(-50%);'
        +'margin-top:7px;white-space:nowrap;pointer-events:none;opacity:0;'
        +'font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;'
        +'font-family:'+C.FONT+';'
        +'transition:opacity .3s ease,left .4s cubic-bezier(.5,0,.2,1);';
      label.textContent=''; track.appendChild(label);

      wrap.appendChild(track);
      (document.body||document.documentElement).prepend(wrap);

      try{
        var totalTop=args.barHeight+20;
        document.documentElement.style.setProperty('--cprog-push',(args.push||0)+'px');
        document.documentElement.style.setProperty('--cprog-mark-top',(totalTop+2)+'px');
      }catch(e){ }

      C.paintTrack();
      C.apply(args.progress, args.bundle);
      if(keepText){
        C.showLabel(keepText, args.bundle);
        if(keepShownAt){ C._labelShownAt=keepShownAt; }
      }
      C._setupObserver();
      C._settle();
      // Red de seguridad: si por lo que sea nunca llega una medida buena, la
      // barra se enseña igual pasado medio segundo.
      setTimeout(function(){ C.reveal(); }, 600);
    }catch(e){ C._err(e); }
  };

  C.ensure=function(){
    try{
      if(!document.getElementById(C.WRAP) && C._args){ C.build(C._args); }
      else{ C.sync(); C._settle(); }
    }catch(e){ C._err(e); }
  };

  C._setFillBg=function(f,newBg){
    if(C.reduceMotion()||C._curBg==null||!C._xf){
      if(C._xfT){ clearTimeout(C._xfT); C._xfT=null; }
      if(C._xf){ C._xf.style.transition='none'; C._xf.style.opacity='0'; }
      f.style.background=newBg; C._curBg=newBg; return;
    }
    if(newBg===C._curBg) return;
    var xf=C._xf;
    if(C._xfT){ clearTimeout(C._xfT); C._xfT=null; f.style.background=C._curBg; }
    xf.style.transition='none'; xf.style.background=newBg; xf.style.opacity='0';
    void xf.offsetWidth;
    xf.style.transition='opacity .45s ease'; xf.style.opacity='1';
    C._curBg=newBg;
    C._xfT=setTimeout(function(){
      f.style.background=newBg;
      xf.style.transition='none'; xf.style.opacity='0';
      C._xfT=null;
    }, 470);
  };

  C.apply=function(p, bundle){
    try{
      if(typeof p!=='number'){ p=parseFloat(p)||0; }
      var f=document.getElementById(C.FILL); if(!f) return;
      var m=C._m(bundle);
      f.style.width=p+'%'; C._setFillBg(f, m.gradient); f.style.boxShadow=m.shadow;
      var lbl=document.getElementById(C.LABEL);
      if(lbl){
        lbl.style.left=Math.max(C._minLeft||2.8, p/2)+'%';
        if(lbl.style.opacity!=='0'){ lbl.style.color=m.solid; if(m.glow){ lbl.style.textShadow=m.glow; } }
      }
      C._applyCheckpoints(p, bundle);
      C._last={p:p, b:bundle}; C._prevP=p;
    }catch(e){ C._err(e); }
  };

  C._applyCheckpoints=function(p, bundle){
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    var m=C._m(bundle);
    var dk=(C._surfDark!==undefined && C._surfDark!==null)?C._surfDark:C.isDark();
    // FIX-001: ancho y x de cada hito desde la medida cacheada en paintTrack,
    // para no forzar maquetacion en el camino caliente de cada respuesta.
    var tw=C._trackW||tr.offsetWidth||0;
    var pendFg=dk?'rgba(233,237,244,0.78)':'rgba(20,28,38,0.62)';
    var list=tr.getElementsByClassName(C.CP);
    var prev=(C._prevP==null)?p:C._prevP;
    for(var i=0;i<list.length;i++){
      var el=list[i]; var inner=el.firstChild; if(!inner) continue;
      var pos=parseFloat(el.getAttribute('data-pos'))||0;
      var cpLeft=(el._cpLeft!==undefined&&el._cpLeft!==null)?el._cpLeft:el.offsetLeft;
      var reached=p>=pos-0.001;
      if(reached){
        // Pinta el trozo EXACTO del degradado que hay detras de esta bolita:
        // misma imagen, dimensionada al canal y desplazada por su propia x.
        inner.style.backgroundImage=m.gradient;
        if(tw>0){
          inner.style.backgroundSize=tw+'px 100%';
          inner.style.backgroundPosition=(-cpLeft)+'px 0';
        }else{
          inner.style.backgroundSize='';
          inner.style.backgroundPosition='';
        }
        inner.style.backgroundColor='transparent';
        inner.style.boxShadow=m.shadow;
        inner.style.color='#fff';
        inner.style.textShadow='0 1px 2px rgba(0,0,0,.45)';
        if(prev<pos-0.001){
          inner.style.animation='none'; void inner.offsetWidth;
          inner.style.animation='cprogPop .4s cubic-bezier(.33,1,.68,1)';
          C._sparkleAt(el);
        }
        el.setAttribute('data-reached','1');
      }else{
        inner.style.backgroundImage='none';
        inner.style.backgroundColor=C._trackBg||'transparent';
        // HISTORIAL: reutilizar la sombra interior del canal en un circulo
        // pequeno rodeaba todo su perimetro y parecia un "borde negro".
        inner.style.boxShadow='none';
        inner.style.color=pendFg;
        inner.style.textShadow='none';
        el.setAttribute('data-reached','0');
      }
    }
  };

  C._spawnSparks=function(leftPercent, count, spread){
    if(C.reduceMotion()) return;
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    for(var i=0;i<count;i++){
      var s=document.createElement('span'); s.className='cprog-spark'; s.textContent='\u2726';
      var ang=(Math.PI*2*i)/count+(Math.random()*0.6-0.3);
      var dist=spread+Math.random()*spread;
      s.style.left=leftPercent+'%';
      s.style.setProperty('--dx',(Math.cos(ang)*dist)+'px');
      s.style.setProperty('--dy',(Math.sin(ang)*dist)+'px');
      tr.appendChild(s);
      (function(node){ node.addEventListener('animationend', function(){ if(node.parentNode) node.parentNode.removeChild(node); }); })(s);
    }
  };
  C._sparkleAt=function(el){
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    var tw=C._trackW||tr.offsetWidth||0;
    var cpLeft=(el._cpLeft!==undefined&&el._cpLeft!==null)?el._cpLeft:el.offsetLeft;
    var pct;
    if(tw>0){ pct=(cpLeft+el.offsetWidth/2)/tw*100; }
    else{ pct=parseFloat(el.getAttribute('data-pos'))||0; }
    C._spawnSparks(pct, 3, 7);
  };
  C.celebrate=function(){
    try{
      var f=document.getElementById(C.FILL); if(!f) return;
      f.style.animation='none'; void f.offsetWidth; f.style.animation='cprogGlow .6s ease-out';
      var edge=parseFloat(f.style.width)||0;
      C._spawnSparks(edge, 4, 9);
    }catch(e){ C._err(e); }
  };

  C.showLabel=function(text, bundle){
    try{
      var lbl=document.getElementById(C.LABEL); if(!lbl||!text) return;
      var m=C._m(bundle);
      lbl.textContent=text; lbl.style.color=m.solid; lbl.style.textShadow=m.glow||'none';
      lbl.style.opacity='1'; C._labelShownAt=Date.now();
      if(C._hideTimer){ clearTimeout(C._hideTimer); C._hideTimer=null; }
    }catch(e){ C._err(e); }
  };
  C.hideLabel=function(minMs){
    try{
      var lbl=document.getElementById(C.LABEL); if(!lbl) return;
      if(lbl.style.opacity==='0' || !C._labelShownAt) return;
      var wait=(minMs||0)-(Date.now()-C._labelShownAt);
      if(C._hideTimer){ clearTimeout(C._hideTimer); C._hideTimer=null; }
      if(wait<=0){ lbl.style.opacity='0'; }
      else{ C._hideTimer=setTimeout(function(){ var l=document.getElementById(C.LABEL); if(l) l.style.opacity='0'; C._hideTimer=null; }, wait); }
    }catch(e){ C._err(e); }
  };

  C.reapply=function(){
    try{ C.paintTrack(); if(C._last){ C.apply(C._last.p, C._last.b); } }catch(e){ C._err(e); }
  };
  C._setupObserver=function(){
    if(!C._resz){
      C._resz=true;
      var t=null;
      try{
        window.addEventListener('resize', function(){
          if(t){ clearTimeout(t); }
          t=setTimeout(function(){ t=null; C.reapply(); }, 120);
        });
      }catch(e){ }
    }
    if(C._obs) return; C._obs=true; C._lastDark=C.isDark();
    // Anki escribe las clases de la tarjeta en <body> en el mismo paso en que
    // inserta su estilo: ese cambio de clase avisa de que ya se puede medir el
    // fondo de verdad, asi que tambien dispara una comprobacion.
    var onChange=function(){
      var d=C.isDark();
      if(d!==C._lastDark){ C._lastDark=d; C.reapply(); return; }
      C._syncSoon();
    };
    try{ window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', onChange); }catch(e){ }
    try{
      var mo=new MutationObserver(onChange);
      if(document.body){ mo.observe(document.body,{attributes:true,attributeFilter:['class']}); }
      mo.observe(document.documentElement,{attributes:true,attributeFilter:['data-bs-theme','class']});
    }catch(e){ }
    C._watchQa();
  };
})();
"""


# --- content that travels inside the reviewer page --------------------------
# HISTORIAL: el estilo y las funciones llegaban en un eval posterior a la carga
# de la pagina del repaso. En un arranque en frio esa carga es lenta, asi que
# todo aterrizaba tarde sobre la primera tarjeta. Viajando dentro de la propia
# pagina existen desde el primer fotograma y al eval solo le queda pedir
# "dibuja". Se mantiene tambien en build_enter_js (es idempotente), por si otro
# complemento reemplaza el contenido de la pagina.
def reviewer_page_head() -> str:
    """The static stylesheet, tagged with the id ``injectStyle`` looks for."""
    return '<style id="_cprogStyle">' + _STATIC_CSS + "</style>"


def reviewer_page_body() -> str:
    """The whole ``window._cprog`` namespace, ready before Python asks to draw."""
    return "<script>" + _BOOTSTRAP_JS + "</script>"


# --- Python-side command builders -------------------------------------------
def _num(value: float) -> str:
    return json.dumps(round(value, 3))


def build_enter_js(
    bundle: StyleBundle,
    progress: float,
    bar_height: int,
    push_down: int,
    show_checkpoints: bool,
    marks: list[dict[str, float]],
    dark: bool,
    effects: bool = True,
) -> str:
    cp_font = max(9, min(13, round(bar_height * 0.62)))
    args = {
        "barHeight": bar_height,
        "radius": bar_height,
        "fillRadius": bar_height / 2,
        "cpSize": bar_height + 6,
        "cpFont": cp_font,
        "minLeft": STREAK_LABEL_MIN_LEFT_PERCENT,
        "push": push_down,
        "showCheckpoints": bool(show_checkpoints),
        "checkpoints": marks,
        "progress": round(progress, 3),
        "dark": bool(dark),
        # Tells build() whether to keep a visible streak/record label across a
        # rebuild; when effects are off the label must disappear at once.
        "effects": bool(effects),
        "bundle": bundle.to_dict(),
    }
    # --- FIX-001 (2026-07-23) --------------------------------------
    # Sintoma: al empezar el repaso / primera tarjeta la barra se atascaba.
    # Causa: aqui se re-ejecutaba TODO el espacio de nombres de la barra
    #   (cientos de lineas) aunque ya viaja dentro de la pagina del repaso
    #   (webview_will_set_content); ese trabajo caia justo sobre la primera
    #   tarjeta, con MathJax inicializandose a la vez.
    # Regla: no reejecutar codigo que ya esta en la pagina; reinyectar el
    #   espacio de nombres solo si de verdad falta (otro complemento borro la
    #   pagina). En marcha normal el arranque solo pide "construye".
    # ---------------------------------------------------------------
    return (
        "(function(){if(!(window._cprog&&window._cprog.build)){\n"
        + _BOOTSTRAP_JS
        + "\n}})();"
        + "\nwindow._cprog.injectStyle(" + json.dumps(_STATIC_CSS) + ");"
        + "\nwindow._cprog.build(" + json.dumps(args, separators=(",", ":")) + ");"
    )


def build_ensure_js() -> str:
    return "window._cprog&&window._cprog.ensure&&window._cprog.ensure();"


def build_set_dark_js(dark: bool) -> str:
    return (
        "window._cprog&&window._cprog.setDark&&window._cprog.setDark("
        + ("true" if dark else "false") + ");"
    )


def build_apply_js(bundle: StyleBundle, progress: float) -> str:
    return (
        "window._cprog&&window._cprog.apply&&window._cprog.apply("
        + _num(progress) + "," + bundle.to_json() + ");"
    )


def build_show_label_js(text: str, bundle: StyleBundle) -> str:
    return (
        "window._cprog&&window._cprog.showLabel&&window._cprog.showLabel("
        + json.dumps(text) + "," + bundle.to_json() + ");"
    )


def build_hide_label_js(min_ms: int) -> str:
    return (
        "window._cprog&&window._cprog.hideLabel&&window._cprog.hideLabel("
        + json.dumps(int(min_ms)) + ");"
    )


def build_celebrate_js() -> str:
    return "window._cprog&&window._cprog.celebrate&&window._cprog.celebrate();"


def reviewer_eval(js: str) -> None:
    try:
        if mw and mw.reviewer and mw.reviewer.web:
            mw.reviewer.web.eval(js)
    except Exception as exc:
        report(exc, "view.reviewer_eval")