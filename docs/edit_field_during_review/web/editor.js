// Historial de correcciones de este archivo:
// FIX-001 (2026-07-24) — El recuadro de edición se partía por líneas.
// FIX-002 (2026-07-24) — Escape guardaba en vez de cancelar, y al cancelar
//                        seguía viéndose el texto tecleado sin guardar.

(() => {
  "use strict";

  if (window.LFE) {
    return;
  }

  const ATTR = "data-lfe";
  const EDIT_CLASS = "lfe-editing";
  const BOX_CLASS = "lfe-editing-box";
  const WRAP_CLASS = "lfe-wrap";
  const MSG_PREFIX = "lfe:";
  const KIND_TAGS = "tags";

  const SKIP_TAGS = new Set([
    "SCRIPT", "STYLE", "HEAD", "TITLE", "META", "LINK", "BR", "HR", "IMG",
    "INPUT", "TEXTAREA", "SELECT", "OPTION", "AUDIO", "VIDEO", "SOURCE",
    "IFRAME", "CANVAS", "SVG", "PATH",
  ]);
  const INTERACTIVE = "a, input, textarea, select, .replay-button, .soundLink";
  const CLOZE_SELECTOR = ".cloze, .cloze-inactive";
  const CLOZE_CONTENT_RE = /\{\{c\d+::[\s\S]*?\}\}/g;

  let payload = null;
  let active = null;
  let clickPoint = { x: 0, y: 0 };

  const root = () => document.getElementById("qa") || document.body;

  const scratch = (tag) => document.createElement(tag);

  const canon = (html) => {
    const holder = scratch("div");
    holder.innerHTML = html;
    return holder.innerHTML.trim();
  };

  // Texto plano de un fragmento HTML. Se usa como filtro barato: comparar
  // innerHTML obliga al navegador a rehacer el HTML de todo el subárbol, y en
  // tarjetas grandes eso se nota; comparar el texto es mucho más rápido y
  // descarta de golpe casi todos los candidatos.
  const textOf = (html) => {
    const holder = scratch("div");
    holder.innerHTML = html;
    return (holder.textContent || "").trim();
  };

  const serialize = (node) => {
    if (node.nodeType === Node.ELEMENT_NODE) {
      return node.outerHTML;
    }
    const holder = scratch("span");
    holder.appendChild(node.cloneNode(true));
    return holder.innerHTML;
  };

  const depth = (el) => {
    let n = 0;
    let cur = el.parentElement;
    while (cur) {
      n += 1;
      cur = cur.parentElement;
    }
    return n;
  };

  const descendants = (scope) => {
    const out = [];
    const walk = (parent) => {
      for (const child of parent.children) {
        if (SKIP_TAGS.has(child.tagName)) {
          continue;
        }
        out.push(child);
        walk(child);
      }
    };
    walk(scope);
    return out;
  };

  const marked = (el) => el.nodeType === Node.ELEMENT_NODE && el.hasAttribute(ATTR);

  const insideMarked = (el) => {
    let cur = el.parentElement;
    while (cur) {
      if (marked(cur)) {
        return true;
      }
      cur = cur.parentElement;
    }
    return false;
  };

  const holdsMarker = (node) =>
    marked(node) ||
    (node.nodeType === Node.ELEMENT_NODE && !!node.querySelector(`[${ATTR}]`));

  const wrapRun = (parent, index, nodes) => {
    if (!nodes.length || nodes.some(holdsMarker)) {
      return null;
    }
    const wrapper = scratch("span");
    wrapper.setAttribute(ATTR, String(index));
    wrapper.className = WRAP_CLASS;
    const doc = parent.ownerDocument || document;
    const range = doc.createRange();
    range.setStartBefore(nodes[0]);
    range.setEndAfter(nodes[nodes.length - 1]);
    try {
      range.surroundContents(wrapper);
    } catch (err) {
      return null;
    }
    return wrapper;
  };

  const markPlain = (scope, index, field) => {
    const target = canon(field.raw);
    if (!target) {
      return;
    }
    const targetText = textOf(field.raw);
    const candidates = descendants(scope).filter(
      (el) => !marked(el) && !insideMarked(el)
    );

    const exact = candidates.filter(
      (el) =>
        (el.textContent || "").trim() === targetText &&
        el.innerHTML.trim() === target
    );
    if (exact.length) {
      exact
        .filter((el) => !exact.some((other) => other !== el && el.contains(other)))
        .forEach((el) => el.setAttribute(ATTR, String(index)));
      return;
    }

    // La profundidad se calcula una sola vez por elemento: hacerlo dentro del
    // comparador recorrería el árbol en cada comparación.
    const parents = candidates
      .map((el) => ({ el, depth: depth(el) }))
      .sort((a, b) => b.depth - a.depth)
      .map((entry) => entry.el);
    parents.push(scope);

    for (const parent of parents) {
      // Si el texto buscado no está dentro de este elemento, ninguna
      // combinación de sus hijos puede componerlo: se descarta sin serializar.
      if (targetText && !(parent.textContent || "").includes(targetText)) {
        continue;
      }
      const kids = Array.from(parent.childNodes);
      if (!kids.length) {
        continue;
      }
      const parts = kids.map(serialize);
      for (let i = 0; i < kids.length; i += 1) {
        let acc = "";
        for (let j = i; j < kids.length; j += 1) {
          acc += parts[j];
          const trimmed = acc.trim();
          if (trimmed === target) {
            if (wrapRun(parent, index, kids.slice(i, j + 1))) {
              return;
            }
            break;
          }
          if (trimmed.length > target.length) {
            break;
          }
        }
      }
    }
  };

  const clozeOutsidePieces = (raw) => {
    const holder = scratch("div");
    holder.innerHTML = raw;
    const text = holder.textContent || "";
    return text
      .replace(CLOZE_CONTENT_RE, "\u0000")
      .split("\u0000")
      .map((piece) => piece.trim())
      .filter((piece) => piece.length > 1);
  };

  const coversPieces = (text, pieces) => {
    let from = 0;
    for (const piece of pieces) {
      const at = text.indexOf(piece, from);
      if (at === -1) {
        return false;
      }
      from = at + piece.length;
    }
    return true;
  };

  const commonAncestor = (nodes) => {
    let ancestor = nodes[0].parentElement;
    while (ancestor && !nodes.every((node) => ancestor.contains(node))) {
      ancestor = ancestor.parentElement;
    }
    return ancestor;
  };

  const markCloze = (scope, index, field) => {
    const clozes = Array.from(scope.querySelectorAll(CLOZE_SELECTOR));
    if (!clozes.length) {
      return;
    }
    const pieces = clozeOutsidePieces(field.raw);
    const scopeEl = scope.nodeType === Node.ELEMENT_NODE ? scope : null;

    let el = commonAncestor(clozes);
    while (
      el &&
      el !== scopeEl &&
      el !== document.body &&
      el !== document.documentElement &&
      !coversPieces(el.textContent || "", pieces)
    ) {
      el = el.parentElement;
    }

    if (el && el !== scopeEl && el !== document.body && el !== document.documentElement) {
      if (!marked(el) && !insideMarked(el)) {
        el.setAttribute(ATTR, String(index));
      }
      return;
    }

    // The field is not inside any wrapper of its own: wrap the run of nodes that
    // holds the cloze deletions, extending over neighbouring text only.
    const parent = scopeEl || scope;
    const kids = Array.from(parent.childNodes);
    let first = -1;
    let last = -1;
    kids.forEach((node, i) => {
      const holds = clozes.some((cloze) => node === cloze || node.contains(cloze));
      if (holds) {
        if (first === -1) {
          first = i;
        }
        last = i;
      }
    });
    if (first === -1) {
      return;
    }
    while (first > 0 && kids[first - 1].nodeType === Node.TEXT_NODE) {
      first -= 1;
    }
    while (last < kids.length - 1 && kids[last + 1].nodeType === Node.TEXT_NODE) {
      last += 1;
    }
    const run = kids.slice(first, last + 1);
    const text = run.map((node) => node.textContent || "").join("");
    if (!coversPieces(text, pieces)) {
      return;
    }
    wrapRun(parent, index, run);
  };

  const markFields = (scope, fields) => {
    fields.forEach((field, index) => {
      if (scope.querySelector(`[${ATTR}="${index}"]`)) {
        return;
      }
      if (!field.raw || !field.raw.trim()) {
        return;
      }
      if (field.cloze) {
        markCloze(scope, index, field);
      } else {
        markPlain(scope, index, field);
      }
    });
  };

  const placeCaret = (el) => {
    const selection = window.getSelection();
    if (!selection) {
      return;
    }
    let range = null;
    if (document.caretRangeFromPoint) {
      range = document.caretRangeFromPoint(clickPoint.x, clickPoint.y);
    }
    if (!range || !el.contains(range.startContainer)) {
      range = document.createRange();
      range.selectNodeContents(el);
      range.collapse(false);
    }
    selection.removeAllRanges();
    selection.addRange(range);
  };

  const onBlur = () => finish(true);

  const onKeydown = (event) => {
    // Anki's webview blocks Backspace at document level unless the target is an
    // input or an editable DIV; keeping every key inside the editor lets the
    // default behaviour (deleting, typing) work in any element.
    event.stopPropagation();
    // --- FIX-002 (2026-07-24) --------------------------------------
    // Síntoma: Escape guardaba el cambio en lugar de descartarlo.
    // Causa: Escape y Enter compartían la misma salida, que siempre guardaba.
    // Regla: Enter confirma y Escape descarta, como en cualquier programa;
    //        una tecla de cancelar nunca debe escribir en la colección.
    // ---------------------------------------------------------------
    if (event.key === "Escape") {
      event.preventDefault();
      finish(false);
      return;
    }
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      finish(true);
    }
  };

  const start = (el, index) => {
    if (active) {
      finish(true);
    }
    if (!payload) {
      return;
    }
    const field = payload.fields[index];
    if (!field) {
      return;
    }

    const rendered = el.innerHTML;
    let mode = "plain";
    if (field.kind === KIND_TAGS) {
      mode = KIND_TAGS;
    } else if (field.cloze || canon(rendered) !== canon(field.raw)) {
      mode = "raw";
    }

    active = {
      el,
      index,
      mode,
      rendered,
      noteId: payload.nid,
      cardId: payload.cid,
      side: payload.side,
      name: field.name,
      kind: field.kind,
      cloze: !!field.cloze,
      original: mode === "plain" ? rendered : field.raw,
    };

    if (mode === KIND_TAGS) {
      el.textContent = field.raw;
    } else if (mode === "raw") {
      el.innerHTML = field.raw;
    }

    el.classList.add(EDIT_CLASS);
    // --- FIX-001 (2026-07-24) --------------------------------------
    // Síntoma: en campos largos el recuadro salía troceado, uno por línea.
    // Causa: el navegador dibuja el contorno de un elemento en línea (inline)
    //        en fragmentos, uno por cada línea que ocupa.
    // Regla: convertir en caja SOLO lo que sea inline, comprobándolo en el
    //        momento; forzarlo en todo movería los campos que ya son bloque.
    // ---------------------------------------------------------------
    if (window.getComputedStyle(el).display === "inline") {
      el.classList.add(BOX_CLASS);
    }
    el.setAttribute("contenteditable", "true");
    el.addEventListener("blur", onBlur);
    el.addEventListener("keydown", onKeydown);
    el.focus({ preventScroll: true });
    placeCaret(el);
  };

  const finish = (save) => {
    if (!active) {
      return;
    }
    const edit = active;
    active = null;

    const el = edit.el;
    el.removeEventListener("blur", onBlur);
    el.removeEventListener("keydown", onKeydown);
    el.removeAttribute("contenteditable");
    el.classList.remove(EDIT_CLASS);
    el.classList.remove(BOX_CLASS);

    const value =
      edit.mode === KIND_TAGS ? (el.textContent || "").trim() : el.innerHTML;
    const changed = canon(value) !== canon(edit.original);

    // --- FIX-002 (2026-07-24) --------------------------------------
    // Síntoma: al cancelar seguía viéndose en pantalla el texto tecleado,
    //          aunque no se hubiera guardado nada.
    // Causa: al cancelar solo se restauraba la vista de algunos modos.
    // Regla: cancelar debe dejar la pantalla exactamente como estaba antes
    //        de empezar a editar, sea cual sea el modo.
    // ---------------------------------------------------------------
    if (!save) {
      // Solo se repinta si hacía falta, para no provocar un parpadeo inútil.
      if (changed || edit.mode !== "plain") {
        el.innerHTML = edit.rendered;
      }
      return;
    }

    if (!changed) {
      if (edit.mode !== "plain") {
        el.innerHTML = edit.rendered;
      }
      return;
    }

    if (payload && payload.nid === edit.noteId && payload.fields[edit.index]) {
      payload.fields[edit.index].raw = value;
    }

    if (edit.mode === "plain" && payload && payload.nid === edit.noteId) {
      root()
        .querySelectorAll(`[${ATTR}="${edit.index}"]`)
        .forEach((twin) => {
          if (twin !== el) {
            twin.innerHTML = value;
          }
        });
    }

    pycmd(
      MSG_PREFIX +
        JSON.stringify({
          cmd: "save",
          nid: edit.noteId,
          cid: edit.cardId,
          side: edit.side,
          index: edit.index,
          name: edit.name,
          kind: edit.kind,
          value,
          // Cuando se ha editado el texto interno del campo, lo que quedó en
          // pantalla es ese texto, no el resultado montado por la plantilla:
          // se pide a Anki que lo devuelva ya montado para repintar solo ese
          // trozo. Hoy esto solo ocurre en las tarjetas de rellenar huecos,
          // pero la condición mira el modo y no el tipo de tarjeta, para no
          // depender de esa coincidencia.
          patch: edit.mode === "raw",
        })
    );
  };

  const onClick = (event) => {
    const target = event.target;
    if (!target || !target.closest) {
      return;
    }
    const el = target.closest(`[${ATTR}]`);
    if (!el) {
      return;
    }
    if (active && active.el === el) {
      return;
    }
    if (target.closest(INTERACTIVE)) {
      return;
    }
    // When the option is on (default), editing only starts if a modifier key
    // is held: Ctrl on Windows/Linux, Cmd on Mac. Without it we return before
    // preventDefault so a plain click still selects text as usual. An edit
    // already in progress still commits on blur, so nothing is lost.
    if (payload && payload.requireModifier && !(event.ctrlKey || event.metaKey)) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    clickPoint = { x: event.clientX, y: event.clientY };
    const index = Number(el.getAttribute(ATTR));
    if (Number.isNaN(index)) {
      return;
    }
    try {
      start(el, index);
    } catch (err) {
      console.error("LFE start", err);
    }
  };

  const init = (data) => {
    try {
      finish(true);
      payload = data;
      const current = payload;
      markFields(root(), payload.fields);
      // Second pass once the card's own scripts have run, for fields that were
      // not reachable in the first pass.
      window.setTimeout(() => {
        if (payload !== current) {
          return;
        }
        try {
          markFields(root(), payload.fields);
        } catch (err) {
          console.error("LFE mark", err);
        }
      }, 0);
    } catch (err) {
      console.error("LFE init", err);
    }
  };

  const patch = (index, html, raw, noteId) => {
    try {
      if (!payload || payload.nid !== noteId) {
        return;
      }
      const field = payload.fields[index];
      if (!field) {
        return;
      }
      field.raw = raw;
      if (active && active.index === index) {
        return;
      }
      const live = root().querySelector(`[${ATTR}="${index}"]`);
      if (!live) {
        return;
      }
      const template = scratch("template");
      template.innerHTML = html;
      markFields(template.content, payload.fields);
      const fresh = template.content.querySelector(`[${ATTR}="${index}"]`);
      if (!fresh) {
        return;
      }
      live.innerHTML = fresh.innerHTML;
    } catch (err) {
      console.error("LFE patch", err);
    }
  };

  document.addEventListener("click", onClick, true);

  window.LFE = { init, patch };
})();