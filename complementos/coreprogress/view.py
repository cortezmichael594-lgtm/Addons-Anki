"""Everything that renders inside the reviewer web view.

The bar is built once per review session and updated in place (no per-card
rebuild, hence no flicker). All rendering lives in a small ``window.coreprogress``
namespace; ``ensure()`` heals the DOM if something removed it and re-syncs the
colors with the card currently on screen.

Surface colors (track, pending checkpoints, light/dark choice) come from the
CARD'S REAL RENDERED BACKGROUND: on build and on every question the JS samples
getComputedStyle(.card/body).backgroundColor, decides dark-vs-light by
luminance, and picks the channel: Nocturne's grey on Nocturne's background, or
a grey with the same contrast on any other background (1.5.0). A template may
override the channel by defining --coreprogress-track (or the older
--cprog-track) on .card. Anki's
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

from .errors import report
from .palettes import StyleBundle, neutral

# --- hoja de estilo fija (cadena en bruto: sin sorpresas al escapar) ----------
# 1.5.0 (informe del 2026-11-17, aplicado entero): todos los colores llegan como
# variables desde Python (palettes.py); aquí solo hay formas, medidas y
# movimiento. Todo lo que se inyecta lleva el prefijo del paquete.
_STATIC_CSS = r"""#qa{padding-top:var(--coreprogress-push,0px);}
#_mark,#_flag{top:var(--coreprogress-mark-top,30px) !important;}
img#star{top:var(--coreprogress-mark-top,30px) !important;}
#coreprogress-bar{position:fixed;top:0;left:0;right:0;z-index:99999;padding:10px 18px 8px;pointer-events:none;
 opacity:0;transition:opacity .28s ease;background:var(--coreprogress-cut,transparent);}
#coreprogress-bar.coreprogress-full #coreprogress-track{max-width:none;}
#coreprogress-track{position:relative;box-sizing:border-box;width:100%;max-width:710px;margin:0 auto;
 height:var(--coreprogress-h);border-radius:calc(var(--coreprogress-h) / 2);contain:layout;}
#coreprogress-fill{position:relative;height:100%;width:0%;min-width:var(--coreprogress-h);
 border-radius:calc(var(--coreprogress-h) / 2);overflow:hidden;
 transition:width .3s cubic-bezier(.2,.8,.2,1);}
#coreprogress-fill::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
 box-shadow:var(--coreprogress-contour,none);}
.coreprogress-xf{position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:0;}
.coreprogress-star{position:absolute;top:50%;right:var(--coreprogress-star-gap);width:var(--coreprogress-star-size);
 height:var(--coreprogress-star-size);translate:0 -50%;color:var(--coreprogress-star);opacity:0;
 transition:opacity .4s ease;}
.coreprogress-star svg{display:block;width:100%;height:100%;}
#coreprogress-bar[data-gold] .coreprogress-star{opacity:1;}
.coreprogress-cp{position:absolute;top:0;bottom:0;width:0;pointer-events:none;}
.coreprogress-cut{position:absolute;top:0;bottom:0;left:-1px;width:2px;background:var(--coreprogress-cut);opacity:0;}
.coreprogress-disc{position:absolute;top:50%;left:0;translate:-50% -50%;box-sizing:border-box;
 height:var(--coreprogress-d);min-width:var(--coreprogress-d);padding:0 4px;border-radius:999px;
 display:flex;align-items:center;justify-content:center;line-height:1;white-space:nowrap;
 font:600 var(--coreprogress-fs)/1 var(--coreprogress-font);font-variant-numeric:tabular-nums;
 background:var(--coreprogress-disc);opacity:0;transition:opacity .2s ease;}
.coreprogress-cp[data-final] .coreprogress-disc{translate:-100% -50%;}
.coreprogress-cp[data-s=cut] .coreprogress-cut{opacity:1;}
.coreprogress-cp[data-s=next] .coreprogress-disc{opacity:1;box-shadow:inset 0 0 0 2px var(--coreprogress-ink);
 color:var(--coreprogress-ink);}
.coreprogress-cp.coreprogress-late .coreprogress-disc{transition-delay:.45s;}
.coreprogress-cp[data-s=total] .coreprogress-disc{opacity:1;box-shadow:inset 0 0 0 1.5px var(--coreprogress-faint);
 color:var(--coreprogress-subtle);}
.coreprogress-cp:is([data-s=done],[data-s=hit]) .coreprogress-disc{opacity:1;transition:none;
 background:var(--coreprogress-ink);color:var(--coreprogress-on-ink);}
.coreprogress-cp[data-s=hit] .coreprogress-disc{animation:coreprogressHit .6s ease-out forwards;}
#coreprogress-bar.coreprogress-small .coreprogress-disc{display:none;}
#coreprogress-bar.coreprogress-small .coreprogress-cp[data-s=next] .coreprogress-cut{opacity:1;left:-1.5px;width:3px;
 background:var(--coreprogress-ink);}
#coreprogress-label{position:absolute;top:100%;left:50%;translate:-50% 0;margin-top:4px;box-sizing:border-box;
 height:20px;padding:0 12px;border-radius:10px;white-space:nowrap;pointer-events:none;opacity:0;
 background:var(--coreprogress-pill);color:var(--coreprogress-ink);
 font:700 12.5px/20px var(--coreprogress-font);letter-spacing:.06em;text-transform:uppercase;}
.coreprogress-spark{position:absolute;top:50%;pointer-events:none;color:var(--coreprogress-ink);line-height:1;
 animation:coreprogressSpark .5s ease-out forwards;}
#coreprogress-bar.coreprogress-instant,#coreprogress-bar.coreprogress-instant *{transition:none !important;}
@keyframes coreprogressHit{0%{scale:1;opacity:1;}25%{scale:1.15;}75%{scale:1.15;opacity:1;}100%{scale:.3 1;opacity:0;}}
@keyframes coreprogressSpark{0%{transform:translate(-50%,-50%) scale(.6);opacity:1;}
 100%{transform:translate(calc(-50% + var(--dx)),calc(-50% - 8px)) scale(1);opacity:0;}}
@media (prefers-reduced-motion: reduce){
 #coreprogress-bar,#coreprogress-bar *{transition:none !important;animation:none !important;}
 .coreprogress-spark{display:none;}
}
@media (forced-colors: active){
 #coreprogress-track{forced-color-adjust:none;background:Canvas !important;border:1px solid CanvasText;}
 #coreprogress-fill{forced-color-adjust:none;background:Highlight !important;}
 #coreprogress-fill::after,.coreprogress-xf{display:none;}
 .coreprogress-cut{forced-color-adjust:none;background:Canvas !important;}
 #coreprogress-bar.coreprogress-small .coreprogress-cp[data-s=next] .coreprogress-cut{background:CanvasText !important;}
 .coreprogress-disc{forced-color-adjust:none;}
 .coreprogress-cp[data-s=next] .coreprogress-disc{background:Canvas;box-shadow:inset 0 0 0 2px Highlight;color:CanvasText;}
 .coreprogress-cp[data-s=total] .coreprogress-disc{background:Canvas;box-shadow:inset 0 0 0 1px CanvasText;color:CanvasText;}
 .coreprogress-cp:is([data-s=done],[data-s=hit]) .coreprogress-disc{background:Highlight;color:HighlightText;}
 .coreprogress-star{forced-color-adjust:none;color:HighlightText;}
 #coreprogress-label{forced-color-adjust:none;background:Canvas;border:1px solid CanvasText;color:CanvasText;}
 .coreprogress-spark{display:none;}
}
"""
# 1.5.0 (informe del 2026-11-17, 5.4): en el contraste alto de Windows cada pieza
# tiene su color del sistema: canal Canvas con borde, relleno Highlight, cortes
# Canvas, próximo hito con aro Highlight, total con aro CanvasText, estrella
# HighlightText (la única señal de la racha dorada, porque el oro desaparece) y
# el aviso con borde.
# 1.2.0 (informe del 2026-11-09): se retiró el destello que cruzaba el relleno
# cada 9 segundos. 1.5.0: tampoco se aviva el relleno al celebrar ni hay halo
# dorado: una sola cosa en movimiento por celebración, en el sitio donde ocurre.

_STAR_SVG = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" '
    'd="M12 2l2.9 6.6 7.1.7-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.3l7.1-.7z"/></svg>'
)

# --- el espacio de nombres: construir / poner al día / curar / celebrar -------
_BOOTSTRAP_JS = r"""// colores-ok: canal translúcido provisional y fondos de reserva de la tarjeta (decisión del autor)
(function(){
  if(!window.coreprogress){ window.coreprogress={}; }
  var C=window.coreprogress;
  C.WRAP='coreprogress-bar'; C.TRACK='coreprogress-track'; C.FILL='coreprogress-fill';
  C.LABEL='coreprogress-label'; C.STYLE='coreprogress-style'; C.CP='coreprogress-cp';
  C.FONT='"Segoe UI Variable Text","Segoe UI",system-ui,-apple-system,sans-serif';

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

  // ---- fondo real de la tarjeta -> luminancia -> canal y cortes ------------
  C._parseColor=function(s){
    try{
      var m=/rgba?\(([^)]+)\)/.exec(s||'');
      if(!m) return null;
      var p=m[1].split(',');
      var a=(p.length>3)?parseFloat(p[3]):1;
      return {r:parseFloat(p[0]),g:parseFloat(p[1]),b:parseFloat(p[2]),a:isNaN(a)?1:a};
    }catch(e){ return null; }
  };
  C._hex=function(h){
    var v=parseInt(String(h).replace('#',''),16);
    return {r:(v>>16)&255,g:(v>>8)&255,b:v&255,a:1};
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
      if(acc){
        var nb=C._nOf(C.isDark()).bg;
        var base=nb?C._hex(nb):(C.isDark()?{r:0,g:0,b:0,a:1}:{r:255,g:255,b:255,a:1});
        return C._over(acc, base);
      }
    }catch(e){ }
    return null;
  };
  C._lin=function(v){ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); };
  C._rl=function(c){ return 0.2126*C._lin(c.r)+0.7152*C._lin(c.g)+0.0722*C._lin(c.b); };
  C._contrast=function(a,b){
    var x=C._rl(a), y=C._rl(b);
    return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);
  };
  C._shadeC=function(c,f){
    var m=function(v){ return f>0 ? v+(255-v)*f : v*(1+f); };
    return {r:m(c.r),g:m(c.g),b:m(c.b),a:1};
  };
  C._css=function(c){ return 'rgb('+Math.round(c.r)+','+Math.round(c.g)+','+Math.round(c.b)+')'; };
  C._near=function(a,b){
    return Math.abs(a.r-b.r)<=3 && Math.abs(a.g-b.g)<=3 && Math.abs(a.b-b.b)<=3;
  };
  // 1.5.0 (informe del 2026-11-17, 2.1): el canal es el gris de Nocturne,
  // plano. Sobre una tarjeta con otro fondo se calcula un gris que dé el mismo
  // contraste con ese fondo (1,33 a 1 de día y 1,35 de noche).
  C._trackFor=function(bg, dark, n){
    if(C._near(bg, C._hex(n.bg))) return n.track;
    var target=dark?1.35:1.33, lo=0, hi=1, sign=dark?1:-1, best=null;
    for(var i=0;i<18;i++){
      var mid=(lo+hi)/2, c=C._shadeC(bg, sign*mid);
      if(C._contrast(c,bg)<target){ lo=mid; } else { hi=mid; best=c; }
    }
    return C._css(best||C._shadeC(bg, sign*hi));
  };
  C._surface=function(){
    var ready=C._cardReady();
    var ovr=C.cardVar('--coreprogress-track','')||C.cardVar('--cprog-track','');
    return {ready:ready, bg:ready?C._sampleBg():null, ovr:ovr};
  };
  C._keyOf=function(s){
    var c=s.bg?(Math.round(s.bg.r)+','+Math.round(s.bg.g)+','+Math.round(s.bg.b)):'x';
    return (s.ready?'1':'0')+':'+c+'|'+(s.ovr||'');
  };
  C._dark=function(){
    return (C._surfDark!==undefined && C._surfDark!==null)?C._surfDark:C.isDark();
  };
  C._nOf=function(dark){
    var n=(C._args&&C._args.n)||{};
    return (dark?n.dark:n.light)||{};
  };
  C._m=function(bundle){ return C._dark()?bundle.dark:bundle.light; };

  C.paintTrack=function(){
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    var w=document.getElementById(C.WRAP);
    var s=C._surface();
    var bg=s.bg;
    var dark=bg?(C._rl(bg)<0.21):C.isDark();
    C._surfDark=dark;
    C._bgKey=C._keyOf(s);
    var n=C._nOf(dark);
    // Override opcional por plantilla: si .card define --coreprogress-track
    // (o el antiguo --cprog-track), manda. Sin medida fiable todavia (la
    // tarjeta no esta en pantalla), el canal va translucido: se apoya en lo
    // que haya pintado y no puede desentonar.
    C._trackBg=s.ovr||(bg?C._trackFor(bg, dark, n):(dark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.08)'));
    // El primer pintado es seco; cualquier correccion posterior funde, para que
    // un ajuste tardio no se perciba como un salto.
    tr.style.transition=C._trackPainted?'background-color .3s ease':'none';
    tr.style.background=C._trackBg;
    C._trackPainted=true;
    if(w){
      w.style.setProperty('--coreprogress-cut', bg?C._css(bg):(n.bg||'transparent'));
      w.style.setProperty('--coreprogress-disc', n.disc||'transparent');
      w.style.setProperty('--coreprogress-faint', n.faint||'currentColor');
      w.style.setProperty('--coreprogress-subtle', n.subtle||'currentColor');
    }
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
  // Lo que se construye o se recoloca entero no se anima: se pinta en su sitio
  // y las transiciones vuelven dos fotogramas despues (1.5.0: sin deslizarse
  // desde cero al entrar a un mazo a medias ni al cambiar las opciones).
  C._still=function(w){
    w.classList.add('coreprogress-instant');
    var on=function(){ w.classList.remove('coreprogress-instant'); };
    try{
      if(window.requestAnimationFrame){ requestAnimationFrame(function(){ requestAnimationFrame(on); }); }
      setTimeout(on, 120);
    }catch(e){ on(); }
  };

  C.build=function(args){
    try{
      C._args=args; C._prevP=null; C._last=null;
      C._effects=(args.effects!==false); C._labelMs=args.labelMs||1500;
      C._small=!!args.small;
      if(typeof args.dark==='boolean'){ C._forceDark=args.dark; }
      // Si hay un aviso de racha/record visible, sobrevive a la reconstruccion
      // (p. ej. cambio de color en mitad del repaso): solo cambia de color y su
      // reloj de visibilidad sigue corriendo, sin reiniciarse.
      // HISTORIAL: solo se conserva si los efectos siguen ACTIVOS. Al desmarcar
      // "Efectos de racha y record" durante el repaso se reconstruye la barra;
      // sin esta condicion la etiqueta visible reaparecia y se quedaba hasta la
      // siguiente tarjeta, en vez de irse al instante con el resto de efectos.
      var keepText='', keepShownAt=null;
      var oldLbl=document.getElementById(C.LABEL);
      if(C._effects && oldLbl && oldLbl.style.opacity==='1' && oldLbl.textContent){
        keepText=oldLbl.textContent; keepShownAt=C._labelShownAt||null;
      }
      var prev=document.getElementById(C.WRAP);
      var wasShown=!!(prev && prev.style.opacity==='1');
      if(prev) prev.remove();

      var h=args.barHeight;
      var wrap=document.createElement('div'); wrap.id=C.WRAP;
      if(C._small){ wrap.classList.add('coreprogress-small'); }
      // 1.6.0: «Ventana», de lado a lado como hasta la 1.4.0; «Tarjeta», 720 px centrada.
      if(args.fullWidth){ wrap.classList.add('coreprogress-full'); }
      // 1.2.0: la barra se anuncia como barra de progreso, con el valor en
      // palabras («30 de 50 tarjetas»), para quien use lector de pantalla. Sin
      // anuncios automaticos: no interrumpe la lectura de la tarjeta.
      wrap.setAttribute('role','progressbar');
      wrap.setAttribute('aria-valuemin','0'); wrap.setAttribute('aria-valuemax','100');
      // 1.3.0: la barra tiene nombre («Progreso de hoy»), no solo valor.
      if(args.name){ wrap.setAttribute('aria-label', args.name); }
      var star=Math.max(8, h-5);
      wrap.style.setProperty('--coreprogress-h', h+'px');
      wrap.style.setProperty('--coreprogress-d', args.cpSize+'px');
      wrap.style.setProperty('--coreprogress-fs', args.cpFont+'px');
      wrap.style.setProperty('--coreprogress-font', C.FONT);
      wrap.style.setProperty('--coreprogress-star-size', star+'px');
      wrap.style.setProperty('--coreprogress-star-gap', ((h-star)/2)+'px');
      // Al reconstruir con la barra ya a la vista (cambio de opciones), sin
      // fundido de entrada: se cambia en su sitio.
      if(wasShown){ wrap.style.opacity='1'; }
      C._still(wrap);

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
      // (contain:layout va en la hoja fija, en #coreprogress-track.)
      C._trackPainted=false;

      var fill=document.createElement('div'); fill.id=C.FILL;
      // HISTORIAL: los degradados NO se pueden transicionar en CSS (saltan en
      // seco). Los cambios de color funden a traves de esta capa.
      var xf=document.createElement('div'); xf.className='coreprogress-xf';
      fill.appendChild(xf);
      C._xf=xf; C._curBg=null;
      // 1.5.0 (informe del 2026-11-17, 2.5): la racha dorada lleva una
      // estrella en la punta, que no depende del color.
      var st=document.createElement('span'); st.className='coreprogress-star';
      st.innerHTML=args.star||'';
      fill.appendChild(st);
      track.appendChild(fill);

      if(args.showCheckpoints && args.checkpoints){
        for(var i=0;i<args.checkpoints.length;i++){
          var cp=args.checkpoints[i];
          var el=document.createElement('div'); el.className=C.CP;
          el.style.left=cp.pos+'%';
          el.setAttribute('data-pos', cp.pos);
          if(cp.final){ el.setAttribute('data-final','1'); }
          var cut=document.createElement('span'); cut.className='coreprogress-cut';
          var disc=document.createElement('span'); disc.className='coreprogress-disc';
          // Con muchas cifras, el disco se ensancha en forma de pastilla.
          disc.textContent=String(Math.round(cp.num));
          (function(node, d){
            d.addEventListener('animationend', function(){
              if(node.getAttribute('data-s')==='hit'){ node.setAttribute('data-s', node._rest||'cut'); }
            });
          })(el, disc);
          el.appendChild(cut); el.appendChild(disc);
          track.appendChild(el);
        }
      }

      // 1.5.0 (informe del 2026-11-17, 2.4): el aviso va en una píldora
      // tintada del tema, centrada bajo la barra, 4 px por debajo.
      var label=document.createElement('div'); label.id=C.LABEL;
      label.textContent=''; track.appendChild(label);

      wrap.appendChild(track);
      (document.body||document.documentElement).prepend(wrap);

      try{
        document.documentElement.style.setProperty('--coreprogress-push',(args.push||0)+'px');
        document.documentElement.style.setProperty('--coreprogress-mark-top',(h+22)+'px');
      }catch(e){ }

      C.paintTrack();
      C.apply(args.progress, args.bundle, args.aria);
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
    // 1.5.0: el cambio de color (al oro y de vuelta) dura 0,4 s.
    xf.style.transition='opacity .4s ease'; xf.style.opacity='1';
    C._curBg=newBg;
    C._xfT=setTimeout(function(){
      f.style.background=newBg;
      xf.style.transition='none'; xf.style.opacity='0';
      C._xfT=null;
    }, 420);
  };

  C._paintVars=function(m){
    var w=document.getElementById(C.WRAP); if(!w) return;
    w.style.setProperty('--coreprogress-ink', m.ink);
    w.style.setProperty('--coreprogress-pill', m.pill);
    w.style.setProperty('--coreprogress-on-ink', m.onInk);
    w.style.setProperty('--coreprogress-contour', m.contour||'none');
    if(m.star){ w.style.setProperty('--coreprogress-star', m.star); w.setAttribute('data-gold',''); }
    else{ w.removeAttribute('data-gold'); }
  };

  C.apply=function(p, bundle, aria, quiet){
    try{
      if(typeof p!=='number'){ p=parseFloat(p)||0; }
      var f=document.getElementById(C.FILL); if(!f) return;
      var w=document.getElementById(C.WRAP);
      if(w){
        w.setAttribute('aria-valuenow', String(Math.round(p)));
        if(aria){ w.setAttribute('aria-valuetext', aria); C._aria=aria; }
      }
      var m=C._m(bundle);
      C._paintVars(m);
      f.style.width=p+'%'; C._setFillBg(f, m.gradient);
      // Con un aviso en esta respuesta, el hito que se alcance solo cambia:
      // una celebración por respuesta (1.3.0).
      var celebrate=C._effects && !quiet && !C.reduceMotion();
      var hit=C._applyMarks(p, celebrate);
      if(hit!==null){ C._spawnSparks(hit); }
      C._last={p:p, b:bundle, a:(aria||C._aria||'')}; C._prevP=p;
    }catch(e){ C._err(e); }
  };

  // 1.5.0 (informe del 2026-11-17, 2.3 y 8.4): los hitos pasados y los lejanos
  // son cortes finos del color del fondo; solo el próximo hito lleva disco con
  // número (aro y número en la tinta) y el total queda en gris al final. Al
  // alcanzar un hito, su disco se llena de tinta, crece un poco y se convierte
  // en corte; el siguiente aparece después. Sin estado guardado: cada llamada
  // decide el estado de cada marca a partir del avance.
  C._applyMarks=function(p, celebrate){
    var tr=document.getElementById(C.TRACK); if(!tr) return null;
    var list=tr.getElementsByClassName(C.CP);
    if(!list.length) return null;
    var prev=(C._prevP==null)?p:C._prevP;
    var pos=[], i, next=-1, hit=-1;
    for(i=0;i<list.length;i++){ pos.push(parseFloat(list[i].getAttribute('data-pos'))||0); }
    for(i=0;i<list.length;i++){ if(pos[i]>p+0.001){ next=i; break; } }
    if(p>prev){
      for(i=0;i<list.length;i++){ if(pos[i]>prev+0.001 && pos[i]<=p+0.001){ hit=i; } }
    }
    for(i=0;i<list.length;i++){
      var el=list[i], fin=el.hasAttribute('data-final'), rest;
      if(i===next){ rest='next'; }
      else if(pos[i]<=p+0.001){ rest=fin?'done':'cut'; }
      else{ rest=fin?'total':'cut'; }
      // Con la barra fina no hay discos: el final del canal ya es el total.
      if(C._small && fin){ rest='none'; }
      el.classList.toggle('coreprogress-late', i===next && hit>=0 && celebrate && !C._small);
      el._rest=rest;
      var cur=el.getAttribute('data-s');
      if(i===hit && celebrate && !C._small){
        el.setAttribute('data-s','none'); void el.offsetWidth; el.setAttribute('data-s','hit');
      }else if(cur==='hit' && (rest==='cut'||rest==='done')){
        // Sigue su animación; al acabar, pasa a rest.
      }else if(cur!==rest){
        el.setAttribute('data-s', rest);
      }
    }
    return (hit>=0 && celebrate)?pos[hit]:null;
  };

  // 1.5.0 (8.7): tres chispas de cuatro puntas, de 7 a 9 px, en la tinta, que
  // suben 8 px y se apagan en medio segundo.
  C._spawnSparks=function(leftPercent){
    if(C.reduceMotion()) return;
    var tr=document.getElementById(C.TRACK); if(!tr) return;
    var dx=[-7,0,7];
    for(var i=0;i<3;i++){
      var s=document.createElement('span'); s.className='coreprogress-spark'; s.textContent='✦';
      s.style.left=leftPercent+'%';
      s.style.fontSize=(7+Math.round(Math.random()*2))+'px';
      s.style.setProperty('--dx',(dx[i]+Math.random()*2-1)+'px');
      tr.appendChild(s);
      (function(node){ node.addEventListener('animationend', function(){ if(node.parentNode) node.parentNode.removeChild(node); }); })(s);
    }
  };
  // Aviso de racha o récord: tres chispas desde la punta, sin avivar el relleno.
  C.celebrate=function(){
    try{
      if(C.reduceMotion() || !C._last) return;
      C._spawnSparks(C._last.p);
    }catch(e){ C._err(e); }
  };

  // 1.3.0: entrada en 150 ms y salida en 300; sin fundido con «reducir el
  // movimiento».
  C._fade=function(lbl, on){
    lbl.style.transition=C.reduceMotion()?'none':('opacity '+(on?'.15s':'.3s')+' ease');
    lbl.style.opacity=on?'1':'0';
  };
  C.showLabel=function(text, bundle){
    try{
      var lbl=document.getElementById(C.LABEL); if(!lbl||!text) return;
      if(bundle){ C._paintVars(C._m(bundle)); }
      lbl.textContent=text;
      C._fade(lbl, true); C._labelShownAt=Date.now();
      // 1.2.0: el aviso dura lo justo (1,5 s) y se apaga solo, pase lo que pase
      // con la tarjeta; uno nuevo sustituye al anterior.
      if(C._hideTimer){ clearTimeout(C._hideTimer); C._hideTimer=null; }
      C._hideTimer=setTimeout(function(){ var l=document.getElementById(C.LABEL); if(l) C._fade(l, false); C._hideTimer=null; }, C._labelMs||1500);
    }catch(e){ C._err(e); }
  };
  C.hideLabel=function(minMs){
    try{
      var lbl=document.getElementById(C.LABEL); if(!lbl) return;
      if(lbl.style.opacity!=='1' || !C._labelShownAt) return;
      var wait=(minMs||0)-(Date.now()-C._labelShownAt);
      if(C._hideTimer){ clearTimeout(C._hideTimer); C._hideTimer=null; }
      if(wait<=0){ C._fade(lbl, false); }
      else{ C._hideTimer=setTimeout(function(){ var l=document.getElementById(C.LABEL); if(l) C._fade(l, false); C._hideTimer=null; }, wait); }
    }catch(e){ C._err(e); }
  };

  C.reapply=function(){
    try{
      C.paintTrack();
      if(C._last){
        // Repintar no es avanzar: ni chispas ni saltos.
        C._prevP=C._last.p;
        C.apply(C._last.p, C._last.b, C._last.a, true);
      }
    }catch(e){ C._err(e); }
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
    return '<style id="coreprogress-style">' + _STATIC_CSS + "</style>"


def reviewer_page_body() -> str:
    """The whole ``window.coreprogress`` namespace, ready before Python asks to draw."""
    return "<script>" + _BOOTSTRAP_JS + "</script>"


# --- Python-side command builders -------------------------------------------
def _num(value: float) -> str:
    return json.dumps(round(value, 3))


# 1.2.0: por debajo de 14 px de barra los números no se leerían. 1.5.0: con la
# barra fina no hay discos; el próximo hito es un corte de 3 px en la tinta.
SMALL_BAR_BELOW: int = 14


def mark_font(bar_height: int) -> int:
    """Letra de los números de hito: 11 px, y 12 a partir de 20 px de barra."""
    return 12 if bar_height >= 20 else 11


def build_args(
    bundle: StyleBundle,
    progress: float,
    bar_height: int,
    push_down: int,
    show_checkpoints: bool,
    marks: list[dict[str, float]],
    dark: bool,
    effects: bool = True,
    label_ms: int = 1500,
    aria: str = "",
    name: str = "",
    full_width: bool = False,
) -> dict[str, object]:
    return {
        "fullWidth": bool(full_width),
        "barHeight": bar_height,
        "cpSize": bar_height + 4,
        "cpFont": mark_font(bar_height),
        "small": bar_height < SMALL_BAR_BELOW,
        "push": push_down,
        "labelMs": label_ms,
        "aria": aria,
        "name": name,
        "showCheckpoints": bool(show_checkpoints),
        "checkpoints": marks,
        "progress": round(progress, 3),
        "dark": bool(dark),
        # Tells build() whether to keep a visible streak/record label across a
        # rebuild; when effects are off the label must disappear at once.
        "effects": bool(effects),
        "bundle": bundle.to_dict(),
        "n": {"light": neutral(False), "dark": neutral(True)},
        "star": _STAR_SVG,
    }


def build_enter_js(
    bundle: StyleBundle,
    progress: float,
    bar_height: int,
    push_down: int,
    show_checkpoints: bool,
    marks: list[dict[str, float]],
    dark: bool,
    effects: bool = True,
    label_ms: int = 1500,
    aria: str = "",
    name: str = "",
    full_width: bool = False,
) -> str:
    args = build_args(
        bundle, progress, bar_height, push_down, show_checkpoints, marks, dark, effects, label_ms, aria, name,
        full_width,
    )
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
        "(function(){if(!(window.coreprogress&&window.coreprogress.build)){\n"
        + _BOOTSTRAP_JS
        + "\n}})();"
        + "\nwindow.coreprogress.injectStyle(" + json.dumps(_STATIC_CSS) + ");"
        + "\nwindow.coreprogress.build(" + json.dumps(args, separators=(",", ":")) + ");"
    )


def build_ensure_js() -> str:
    return "window.coreprogress&&window.coreprogress.ensure&&window.coreprogress.ensure();"


def build_set_dark_js(dark: bool) -> str:
    return (
        "window.coreprogress&&window.coreprogress.setDark&&window.coreprogress.setDark("
        + ("true" if dark else "false") + ");"
    )


def build_apply_js(bundle: StyleBundle, progress: float, aria: str = "", quiet: bool = False) -> str:
    """quiet: esta respuesta ya trae un aviso; el hito que se alcance solo
    cambia, sin salto ni chispas (1.3.0)."""
    return (
        "window.coreprogress&&window.coreprogress.apply&&window.coreprogress.apply("
        + _num(progress) + "," + bundle.to_json() + "," + json.dumps(aria) + ","
        + ("true" if quiet else "false") + ");"
    )


def build_show_label_js(text: str, bundle: StyleBundle) -> str:
    return (
        "window.coreprogress&&window.coreprogress.showLabel&&window.coreprogress.showLabel("
        + json.dumps(text) + "," + bundle.to_json() + ");"
    )


def build_hide_label_js(min_ms: int) -> str:
    return (
        "window.coreprogress&&window.coreprogress.hideLabel&&window.coreprogress.hideLabel("
        + json.dumps(int(min_ms)) + ");"
    )


def build_celebrate_js() -> str:
    return "window.coreprogress&&window.coreprogress.celebrate&&window.coreprogress.celebrate();"


def reviewer_eval(js: str) -> None:
    try:
        if mw and mw.reviewer and mw.reviewer.web:
            mw.reviewer.web.eval(js)
    except Exception as exc:
        report(exc, "view.reviewer_eval")
