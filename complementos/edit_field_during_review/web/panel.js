/* Panel de opciones con el modelo de GritMap
 * (docs/fichas-diseno/09-patron-configuracion.md).
 *
 * Python (panel.py) pone en la pagina la descripcion del panel (recuadros y
 * controles), los valores guardados y los de serie; la pagina se dibuja
 * entera antes de verse. Nada se guarda hasta pulsar Aceptar: entonces se
 * envian los valores a Python, que los comprueba y, si algo no sirve,
 * devuelve el error para ensenarlo encima de su campo.
 *
 * Los controles son elementos de verdad (<button>, <input>, <select>,
 * <dialog>) dibujados a medida: conservan su teclado, su foco y lo que
 * anuncia el lector de pantalla.
 *
 * Todo lo que este codigo crea o busca empieza por «edit_field_during_review» y el codigo es
 * idempotente: si se carga dos veces, se reutiliza el que ya existe.
 */
var EditFieldDuringReviewPanel = (typeof EditFieldDuringReviewPanel !== "undefined" && EditFieldDuringReviewPanel) || (function () {
    "use strict";

    var P = "edit_field_during_review";
    var REPEAT_DELAY = 400;
    var REPEAT_EVERY = 80;

    var S = {
        p: null,
        t: {},
        v: {},
        ctl: {},
        cards: [],
        page: "main",
        opener: null,
        undo: null,
        ready: false,
        nodes: {},
    };

    // Utilidades
    // -------------------------------------------------------------------

    function el(tag, attrs, children) {
        var node = document.createElement(tag);
        var key;
        for (key in attrs || {}) {
            if (!Object.prototype.hasOwnProperty.call(attrs, key)) {
                continue;
            }
            var value = attrs[key];
            if (value === undefined || value === null || value === false) {
                continue;
            }
            if (key === "class") {
                node.className = value.split(" ").map(function (name) {
                    return name ? P + "-" + name : name;
                }).join(" ");
            } else if (key === "text") {
                node.textContent = value;
            } else if (key.indexOf("on") === 0) {
                node.addEventListener(key.slice(2), value);
            } else {
                node.setAttribute(key, value === true ? "" : value);
            }
        }
        (children || []).forEach(function (child) {
            if (child === null || child === undefined) {
                return;
            }
            node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
        });
        return node;
    }

    var uid = 0;

    function newId(name) {
        uid += 1;
        return P + "-" + name + "-" + uid;
    }

    var ICONS = {
        tick: '<path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        chevron: '<path d="M6 3.5l4.5 4.5L6 12.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        down: '<path d="M3.5 6l4.5 4.5L12.5 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        back: '<path d="M10 3.5L5.5 8l4.5 4.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>',
        clear: '<path d="M4.5 4.5l7 7M11.5 4.5l-7 7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
        info: '<circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 7.2v4M8 4.8v.1" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
        alert: '<circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 4.6v4.2M8 11.1v.1" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    };

    function svg(name, size) {
        var holder = document.createElement("span");
        holder.innerHTML = '<svg width="' + size + '" height="' + size + '" viewBox="0 0 16 16"'
            + ' aria-hidden="true" focusable="false">' + ICONS[name] + "</svg>";
        return holder.firstChild;
    }

    /* El canal con Python (pycmd) lo crea Anki un instante despues de leer
     * la pagina: lo que se envia antes espera en cola, en orden. */
    var queue = [];
    var waiting = false;

    function whenBridge(fn) {
        if (typeof pycmd === "function" && !queue.length) {
            fn();
            return;
        }
        queue.push(fn);
        if (waiting) {
            return;
        }
        waiting = true;
        (function poll() {
            if (typeof pycmd !== "function") {
                setTimeout(poll, 10);
                return;
            }
            waiting = false;
            var pending = queue;
            queue = [];
            pending.forEach(function (item) {
                item();
            });
        })();
    }

    function send(action, data, callback) {
        var cmd = S.p.prefix + action + ":" + JSON.stringify(data === undefined ? null : data);
        whenBridge(function () {
            pycmd(cmd, callback);
        });
    }

    function announce(text) {
        if (S.nodes.live) {
            S.nodes.live.textContent = "";
            S.nodes.live.textContent = text;
        }
    }

    function copy(value) {
        return JSON.parse(JSON.stringify(value));
    }

    // Controles
    // -------------------------------------------------------------------

    /* Cada control se guarda en S.ctl[clave] con set(valor), enable(si/no) y
     * su hueco de error. Al cambiar, escribe en S.v y repasa las dependencias. */
    function changed() {
        refreshDependencies();
        refreshSummaries();
    }

    function errorSlot() {
        var node = el("div", { class: "error", role: "alert", hidden: true });
        return node;
    }

    function option(item, labelId, control, extra) {
        var parts = [];
        if (item.label) {
            parts.push(el("span", { class: "label", id: labelId, text: item.label }));
        }
        var slot = errorSlot();
        parts.push(slot);
        parts.push(control);
        if (item.note) {
            parts.push(el("p", { class: "rule", text: item.note }));
        }
        (extra || []).forEach(function (node) {
            parts.push(node);
        });
        var node = el("div", { class: "option" }, parts);
        return { node: node, slot: slot };
    }

    function checkbox(text, checked, onChange, opts) {
        var input = el("input", { type: "checkbox" });
        input.checked = !!checked;
        input.addEventListener("change", function () {
            onChange(input.checked);
        });
        var box = el("span", { class: "box", "aria-hidden": "true" }, [svg("tick", 14)]);
        var label = el("label", { class: "check" }, [
            input,
            box,
            el("span", { class: "check-text", text: text }),
        ]);
        if (opts && opts.describedBy) {
            input.setAttribute("aria-describedby", opts.describedBy);
        }
        return { node: label, input: input };
    }

    function buildCheck(item) {
        var noteId = item.note ? newId("note") : null;
        var box = checkbox(item.label, S.v[item.key], function (on) {
            S.v[item.key] = on;
            changed();
        }, { describedBy: noteId });
        var slot = errorSlot();
        var parts = [slot, box.node];
        if (item.note) {
            parts.push(el("p", { class: "rule", id: noteId, text: item.note }));
        }
        var group = null;
        if (item.children && item.children.length) {
            group = el("div", { class: "group" }, item.children.map(buildItem));
            parts.push(group);
        }
        var node = el("div", { class: "option" }, parts);
        S.ctl[item.key] = {
            item: item,
            node: node,
            slot: slot,
            focus: box.input,
            set: function (value) {
                box.input.checked = !!value;
            },
            enable: function (on) {
                box.input.disabled = !on;
                box.node.classList.toggle(P + "-off", !on);
            },
            group: group,
        };
        return node;
    }

    function clamp(value, item) {
        var n = Math.round(Number(value));
        if (!isFinite(n)) {
            n = S.p.defaults[item.key];
        }
        return Math.max(item.min, Math.min(item.max, n));
    }

    function buildStepper(item) {
        var labelId = newId("label");
        var step = item.step || 1;
        var input = el("input", {
            type: "text",
            inputmode: "numeric",
            role: "spinbutton",
            "aria-labelledby": labelId,
            "aria-valuemin": String(item.min),
            "aria-valuemax": String(item.max),
        });
        var minus = el("button", { type: "button", "aria-label": "−", tabindex: "-1", text: "−" });
        var plus = el("button", { type: "button", "aria-label": "+", tabindex: "-1", text: "+" });
        var row = el("div", { class: "step-row" }, [
            el("div", { class: "step" }, [minus, input, plus]),
            item.unit ? el("span", { class: "unit", text: item.unit }) : null,
        ]);

        function show() {
            var value = S.v[item.key];
            input.value = String(value);
            input.setAttribute("aria-valuenow", String(value));
            input.setAttribute("aria-valuetext", value + (item.unit ? " " + item.unit : ""));
            minus.disabled = input.disabled || value <= item.min;
            plus.disabled = input.disabled || value >= item.max;
        }

        function put(value) {
            var next = clamp(value, item);
            if (next !== S.v[item.key]) {
                S.v[item.key] = next;
                changed();
            }
            show();
        }

        function repeat(button, delta) {
            var timer = null;
            function stop() {
                clearTimeout(timer);
                timer = null;
            }
            button.addEventListener("pointerdown", function (event) {
                if (button.disabled || event.button !== 0) {
                    return;
                }
                put(S.v[item.key] + delta);
                timer = setTimeout(function again() {
                    if (button.disabled) {
                        stop();
                        return;
                    }
                    put(S.v[item.key] + delta);
                    timer = setTimeout(again, REPEAT_EVERY);
                }, REPEAT_DELAY);
            });
            ["pointerup", "pointerleave", "pointercancel"].forEach(function (name) {
                button.addEventListener(name, stop);
            });
            button.addEventListener("keydown", function (event) {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    put(S.v[item.key] + delta);
                }
            });
        }

        repeat(minus, -step);
        repeat(plus, step);
        input.addEventListener("keydown", function (event) {
            if (event.key === "ArrowUp") {
                event.preventDefault();
                put(S.v[item.key] + step);
            } else if (event.key === "ArrowDown") {
                event.preventDefault();
                put(S.v[item.key] - step);
            } else if (event.key === "Enter") {
                event.preventDefault();
                put(input.value);
            }
        });
        input.addEventListener("change", function () {
            put(input.value);
        });
        input.addEventListener("blur", function () {
            put(input.value);
        });
        var built = option(item, labelId, row);
        S.ctl[item.key] = {
            item: item,
            node: built.node,
            slot: built.slot,
            focus: input,
            field: input,
            set: show,
            enable: function (on) {
                input.disabled = !on;
                show();
            },
        };
        show();
        return built.node;
    }

    function buildChips(item) {
        var labelId = newId("label");
        var name = newId("chips");
        var group = el("div", { class: "chips", role: "radiogroup", "aria-labelledby": item.label ? labelId : null });
        var inputs = [];
        item.options.forEach(function (opt) {
            var input = el("input", { type: "radio", name: name, value: opt.value });
            input.checked = S.v[item.key] === opt.value;
            input.addEventListener("change", function () {
                if (input.checked) {
                    S.v[item.key] = opt.value;
                    changed();
                }
            });
            inputs.push(input);
            var swatch = opt.swatch
                ? el("span", { class: "swatch", "aria-hidden": "true", style: "background:" + opt.swatch })
                : null;
            group.appendChild(el("label", { class: "chip" }, [
                input,
                swatch,
                el("span", { class: "chip-name", text: opt.label }),
                el("span", { class: "tick", "aria-hidden": "true" }, [svg("tick", 16)]),
            ]));
        });
        var built = option(item, labelId, group);
        S.ctl[item.key] = {
            item: item,
            node: built.node,
            slot: built.slot,
            focus: null,
            set: function (value) {
                inputs.forEach(function (input) {
                    input.checked = input.value === value;
                });
            },
            enable: function (on) {
                inputs.forEach(function (input) {
                    input.disabled = !on;
                });
                group.classList.toggle(P + "-off", !on);
            },
            firstFocus: function () {
                return group.querySelector("input:checked") || inputs[0];
            },
        };
        return built.node;
    }

    function buildSelect(item) {
        var labelId = newId("label");
        var select = el("select", { class: "select", "aria-labelledby": item.label ? labelId : null });
        item.options.forEach(function (opt) {
            var node = el("option", { value: opt.value, text: opt.label });
            select.appendChild(node);
        });
        select.value = S.v[item.key];
        if (select.selectedIndex < 0 && item.options.length) {
            select.selectedIndex = 0;
            S.v[item.key] = select.value;
        }
        select.addEventListener("change", function () {
            S.v[item.key] = select.value;
            changed();
        });
        var test = null;
        if (item.test) {
            test = el("button", { type: "button", class: "btn", text: item.test.label, onclick: function () {
                send("action", { name: item.test.action, key: item.key, values: S.v });
            } });
        }
        var row = el("div", { class: "select-row" }, [
            el("div", { class: "select-wrap" }, [select, svg("down", 12)]),
            test,
        ]);
        var empty = !item.options.length || !!item.unavailable;
        var extra = [];
        if (empty && item.empty) {
            extra.push(el("p", { class: "rule", text: item.empty }));
        }
        var built = option(item, labelId, row, extra);
        S.ctl[item.key] = {
            item: item,
            node: built.node,
            slot: built.slot,
            focus: select,
            field: select,
            set: function (value) {
                select.value = value;
            },
            enable: function (on) {
                var usable = on && !empty;
                select.disabled = !usable;
                if (test) {
                    test.disabled = !usable;
                }
                row.classList.toggle(P + "-off", !usable);
            },
        };
        return built.node;
    }

    function buildSlider(item) {
        var labelId = newId("label");
        var input = el("input", {
            type: "range",
            class: "slider",
            min: String(item.min),
            max: String(item.max),
            step: String(item.step || 1),
            "aria-labelledby": labelId,
        });
        var value = el("span", { class: "slider-value", "aria-hidden": "true" });

        function show() {
            var current = S.v[item.key];
            input.value = String(current);
            var share = (current - item.min) / Math.max(1, item.max - item.min) * 100;
            input.style.setProperty("--" + P + "-fill", share + "%");
            var text = current + (item.suffix || "");
            value.textContent = text;
            input.setAttribute("aria-valuetext", text);
        }

        input.addEventListener("input", function () {
            S.v[item.key] = clamp(input.value, item);
            show();
            changed();
        });
        var built = option(item, labelId, el("div", { class: "slider-row" }, [input, value]));
        S.ctl[item.key] = {
            item: item,
            node: built.node,
            slot: built.slot,
            focus: input,
            set: show,
            enable: function (on) {
                input.disabled = !on;
                built.node.classList.toggle(P + "-off", !on);
            },
        };
        show();
        return built.node;
    }

    // Grabador de atajos: graba la combinacion que se pulse con el foco en el
    // campo. Tab y Mayus+Tab siguen moviendo el foco, Esc sigue cancelando la
    // ventana y Retroceso o Supr solos vacian el campo.
    var KEY_NAMES = {
        Enter: "Return", Escape: "Esc", Delete: "Del", Insert: "Ins", " ": "Space",
        ArrowUp: "Up", ArrowDown: "Down", ArrowLeft: "Left", ArrowRight: "Right",
        PageUp: "PgUp", PageDown: "PgDown", Backspace: "Backspace", Home: "Home", End: "End",
        Tab: "Tab",
    };

    function keyName(event) {
        var code = event.code || "";
        if (/^Key[A-Z]$/.test(code)) {
            return code.slice(3);
        }
        if (/^Digit[0-9]$/.test(code)) {
            return code.slice(5);
        }
        if (/^F[0-9]{1,2}$/.test(event.key)) {
            return event.key;
        }
        if (KEY_NAMES[event.key]) {
            return KEY_NAMES[event.key];
        }
        if (event.key && event.key.length === 1) {
            return event.key.toUpperCase();
        }
        return "";
    }

    function portable(event) {
        var name = keyName(event);
        if (!name || ["Control", "Shift", "Alt", "Meta", "AltGraph"].indexOf(event.key) >= 0) {
            return "";
        }
        var mods = [];
        // En Mac, Qt llama «Ctrl» a la tecla ⌘ y «Meta» a Control.
        var ctrl = S.p.isMac ? event.metaKey : event.ctrlKey;
        var meta = S.p.isMac ? event.ctrlKey : event.metaKey;
        if (ctrl) {
            mods.push("Ctrl");
        }
        if (event.altKey) {
            mods.push("Alt");
        }
        if (event.shiftKey) {
            mods.push("Shift");
        }
        if (meta) {
            mods.push("Meta");
        }
        return mods.concat([name]).join("+");
    }

    function buildShortcut(item) {
        var labelId = newId("label");
        var input = el("input", {
            type: "text",
            class: "key",
            readonly: true,
            "aria-labelledby": labelId,
            placeholder: item.placeholder || "",
            autocomplete: "off",
            spellcheck: "false",
        });
        var clear = el("button", {
            type: "button",
            class: "icon-btn",
            "aria-label": item.clear || "",
            title: item.clear || "",
        }, [svg("clear", 14)]);

        function show() {
            var value = S.v[item.key] || "";
            input.value = "";
            if (!value) {
                return;
            }
            input.value = S.p.keytext[value] || value;
            if (!S.p.keytext[value]) {
                send("keytext", value, function (text) {
                    if (typeof text === "string" && text) {
                        S.p.keytext[value] = text;
                        if (S.v[item.key] === value) {
                            input.value = text;
                        }
                    }
                });
            }
        }

        function put(value) {
            S.v[item.key] = value;
            setError(item.key, "");
            show();
            announce(input.value);
            changed();
        }

        input.addEventListener("keydown", function (event) {
            var plain = !event.ctrlKey && !event.altKey && !event.metaKey;
            if (event.key === "Tab" && plain) {
                return;
            }
            if (event.key === "Escape" && plain && !event.shiftKey) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            if ((event.key === "Backspace" || event.key === "Delete") && plain && !event.shiftKey) {
                put("");
                return;
            }
            if (event.repeat) {
                return;
            }
            var value = portable(event);
            if (value) {
                put(value);
            }
        });
        clear.addEventListener("click", function () {
            put("");
            input.focus();
        });
        var built = option(item, labelId, el("div", { class: "key-row" }, [input, clear]));
        S.ctl[item.key] = {
            item: item,
            node: built.node,
            slot: built.slot,
            focus: input,
            field: input,
            set: show,
            enable: function (on) {
                input.disabled = !on;
                clear.disabled = !on;
                built.node.classList.toggle(P + "-off", !on);
            },
        };
        show();
        return built.node;
    }

    // Linea de dato con accion: «Su récord actual: 7» y «Restablecer», que
    // pregunta antes y no cambia nada hasta Aceptar.
    function statText(parts) {
        return el("span", { class: "stat-text" }, [
            parts.before || "",
            parts.strong ? el("strong", { text: parts.strong }) : null,
            parts.after || "",
        ]);
    }

    function buildStat(item) {
        var holder = el("span");
        holder.appendChild(statText(S.v[item.key] ? item.done : item.parts));
        var button = el("button", { type: "button", class: "link", text: item.action.label });
        button.disabled = !!S.v[item.key] || !!item.action.disabled;
        button.addEventListener("click", function () {
            confirmBox(item.action.confirm, function () {
                S.v[item.key] = true;
                holder.textContent = "";
                holder.appendChild(statText(item.done));
                button.disabled = true;
                announce(holder.textContent);
                changed();
            }, button);
        });
        var node = el("div", { class: "option" }, [el("div", { class: "stat" }, [holder, button])]);
        S.ctl[item.key] = {
            item: item,
            node: node,
            slot: null,
            focus: button,
            set: function (value) {
                holder.textContent = "";
                holder.appendChild(statText(value ? item.done : item.parts));
                button.disabled = !!value || !!item.action.disabled;
            },
            enable: function () {},
        };
        return node;
    }

    // Fila de resumen que abre su subpagina (lista con buscador y casillas).
    function buildRow(item) {
        var summary = el("span", { class: "row-summary" }, [el("span", { class: "bone" })]);
        var button = el("button", { type: "button", class: "row" }, [
            el("span", { class: "row-text" }, [
                el("span", { class: "row-title", text: item.label }),
                summary,
            ]),
            el("span", { class: "chevron" }, [svg("chevron", 16)]),
        ]);
        button.addEventListener("click", function () {
            openPage(item, button);
        });
        var slot = errorSlot();
        var node = el("div", { class: "option" }, [slot, button]);
        S.ctl[item.key] = {
            item: item,
            node: node,
            slot: slot,
            focus: button,
            summary: summary,
            set: function () {},
            enable: function (on) {
                button.disabled = !on;
                button.classList.toggle(P + "-off", !on);
            },
        };
        return node;
    }

    function buildNote(item) {
        return el("p", { class: "rule option", text: item.text });
    }

    function buildNotice(item) {
        return el("div", { class: "notice" }, [svg("info", 16), el("span", { text: item.text })]);
    }

    function buildItem(item) {
        switch (item.type) {
        case "check":
            return buildCheck(item);
        case "stepper":
            return buildStepper(item);
        case "chips":
            return buildChips(item);
        case "select":
            return buildSelect(item);
        case "slider":
            return buildSlider(item);
        case "shortcut":
            return buildShortcut(item);
        case "stat":
            return buildStat(item);
        case "row":
            return buildRow(item);
        case "notice":
            return buildNotice(item);
        default:
            return buildNote(item);
        }
    }

    function itemKeys(items, out) {
        (items || []).forEach(function (item) {
            if (item.key && item.type !== "stat" && item.type !== "row") {
                out.push(item.key);
            }
            itemKeys(item.children, out);
        });
        return out;
    }

    // Dependencias: lo que cuelga de una casilla se apaga si esta desmarcada.
    function isOn(key) {
        var ctl = S.ctl[key];
        if (!ctl || !ctl.parent) {
            return true;
        }
        return !!S.v[ctl.parent] && isOn(ctl.parent);
    }

    function refreshDependencies() {
        Object.keys(S.ctl).forEach(function (key) {
            S.ctl[key].enable(isOn(key));
        });
    }

    function markParents(items, parent) {
        (items || []).forEach(function (item) {
            if (item.key && S.ctl[item.key] && parent) {
                S.ctl[item.key].parent = parent;
            }
            markParents(item.children, item.key);
        });
    }

    function refreshSummaries() {
        Object.keys(S.ctl).forEach(function (key) {
            var ctl = S.ctl[key];
            if (ctl.item.type !== "row") {
                return;
            }
            send("summary", { key: key, values: S.v }, function (text) {
                if (typeof text === "string") {
                    ctl.summary.textContent = text;
                }
            });
        });
    }

    // Errores: encima del campo, con icono, y el campo con borde rojo.
    function setError(key, text) {
        var ctl = S.ctl[key];
        if (!ctl || !ctl.slot) {
            return;
        }
        ctl.slot.textContent = "";
        ctl.slot.hidden = !text;
        if (ctl.field) {
            ctl.field.classList.toggle(P + "-invalid", !!text);
            if (text) {
                ctl.field.setAttribute("aria-invalid", "true");
            } else {
                ctl.field.removeAttribute("aria-invalid");
            }
        }
        if (text) {
            ctl.slot.appendChild(svg("alert", 16));
            ctl.slot.appendChild(el("span", { text: text }));
        }
    }

    function clearErrors() {
        Object.keys(S.ctl).forEach(function (key) {
            setError(key, "");
        });
    }

    // Restaurar por recuadro, con «Deshacer» al lado.
    function restoreCard(card, links) {
        var keys = itemKeys(card.items, []);
        var before = {};
        keys.forEach(function (key) {
            before[key] = copy(S.v[key]);
            S.v[key] = copy(S.p.defaults[key]);
            S.ctl[key].set(S.v[key]);
        });
        clearErrors();
        changed();
        links.undo.hidden = false;
        S.undo = { keys: keys, before: before, links: links };
        announce(S.t.restore);
    }

    function undoRestore() {
        var undo = S.undo;
        if (!undo) {
            return;
        }
        undo.keys.forEach(function (key) {
            S.v[key] = undo.before[key];
            S.ctl[key].set(S.v[key]);
        });
        undo.links.undo.hidden = true;
        undo.links.restore.focus();
        S.undo = null;
        changed();
        announce(S.t.undo);
    }

    function buildCard(card) {
        var head = [];
        var headingId = card.title ? newId("card") : null;
        if (card.title) {
            head.push(el("h2", { id: headingId, text: card.title }));
        }
        var links = null;
        if (card.restore) {
            links = {};
            links.restore = el("button", { type: "button", class: "link", text: S.t.restore });
            links.undo = el("button", { type: "button", class: "link", text: S.t.undo, hidden: true });
            links.restore.addEventListener("click", function () {
                restoreCard(card, links);
            });
            links.undo.addEventListener("click", undoRestore);
            head.push(el("div", { class: "card-actions" }, [links.undo, links.restore]));
        }
        var parts = [];
        if (head.length) {
            parts.push(el("div", { class: "card-head" }, head));
        }
        if (card.note) {
            parts.push(el("p", { class: "card-note", text: card.note }));
        }
        card.items.forEach(function (item) {
            parts.push(buildItem(item));
        });
        return el("section", {
            class: "card",
            "aria-labelledby": headingId,
            "aria-label": card.title ? null : S.p.title,
        }, parts);
    }

    // Subpagina: lista con buscador y casillas, dentro de la misma ventana.
    function openPage(item, opener) {
        S.page = item.key;
        S.opener = opener;
        var n = S.nodes;
        n.title.hidden = true;
        n.back.hidden = false;
        n.main.hidden = true;
        n.sub.hidden = false;
        n.sub.textContent = "";
        var search = el("input", {
            type: "search",
            class: "search",
            placeholder: S.t.search,
            "aria-label": S.t.search,
        });
        var list = el("ul", { class: "list", "aria-label": item.label });
        var empty = el("p", { class: "rule", text: item.empty || "", hidden: true });
        var card = el("section", { class: "card", "aria-label": item.label }, [
            el("div", { class: "card-head" }, [el("h2", { text: item.label })]),
            item.note ? el("p", { class: "card-note", text: item.note }) : null,
            el("div", { class: "option" }, [search]),
            list,
            empty,
        ]);
        n.sub.appendChild(card);
        var entries = [];

        function render() {
            var query = search.value.trim().toLowerCase();
            list.textContent = "";
            var chosen = {};
            (S.v[item.key] || []).forEach(function (value) {
                chosen[String(value)] = true;
            });
            var shown = 0;
            entries.forEach(function (entry) {
                if (query && entry.label.toLowerCase().indexOf(query) < 0) {
                    return;
                }
                shown += 1;
                var box = checkbox(entry.label, chosen[String(entry.value)], function (on) {
                    var current = (S.v[item.key] || []).filter(function (value) {
                        return String(value) !== String(entry.value);
                    });
                    if (on) {
                        current.push(entry.value);
                    }
                    S.v[item.key] = current;
                    changed();
                });
                list.appendChild(el("li", {}, [box.node]));
            });
            empty.hidden = shown > 0 || !entries.length || !item.empty;
        }

        search.addEventListener("input", render);
        list.appendChild(el("li", {}, [el("span", { class: "bone" })]));
        send("options", item.key, function (data) {
            entries = Array.isArray(data) ? data : [];
            render();
        });
        n.body.scrollTop = 0;
        n.back.focus();
        refreshScroll();
    }

    function closePage() {
        var n = S.nodes;
        S.page = "main";
        n.title.hidden = false;
        n.back.hidden = true;
        n.sub.hidden = true;
        n.sub.textContent = "";
        n.main.hidden = false;
        if (S.opener) {
            S.opener.focus();
        }
        refreshScroll();
    }

    // Pregunta con un <dialog> de verdad; el foco empieza en la respuesta que
    // no cambia nada.
    function confirmBox(texts, onYes, returnTo) {
        var dialog = el("dialog", { "aria-labelledby": newId("q") });
        var title = el("h2", { id: dialog.getAttribute("aria-labelledby"), text: texts.title });
        var no = el("button", { type: "button", class: "btn", text: texts.no });
        var yes = el("button", { type: "button", class: "btn primary", text: texts.yes });
        function close() {
            dialog.close();
            dialog.remove();
            if (returnTo) {
                returnTo.focus();
            }
        }
        no.addEventListener("click", close);
        yes.addEventListener("click", function () {
            close();
            onYes();
        });
        dialog.addEventListener("cancel", function (event) {
            event.preventDefault();
            close();
        });
        dialog.appendChild(title);
        if (texts.body) {
            dialog.appendChild(el("p", { text: texts.body }));
        }
        dialog.appendChild(el("div", { class: "dialog-actions" }, [yes, no]));
        S.nodes.app.appendChild(dialog);
        dialog.showModal();
        no.focus();
    }

    // Altura y desplazamiento (regla de FIX-028 de GritMap).
    function naturalHeight() {
        var n = S.nodes;
        var bodyStyle = window.getComputedStyle(n.body);
        var padding = parseFloat(bodyStyle.paddingTop) + parseFloat(bodyStyle.paddingBottom);
        return Math.ceil(n.head.offsetHeight + n.main.offsetHeight + padding + n.foot.offsetHeight);
    }

    function updateScrollState() {
        var body = S.nodes.body;
        var overflow = body.scrollHeight > body.clientHeight + 1;
        S.nodes.shell.classList.toggle(P + "-overflow", overflow);
        S.nodes.shell.classList.toggle(P + "-scrolled", overflow && body.scrollTop > 0);
    }

    function refreshScroll() {
        if (S.ready) {
            setTimeout(updateScrollState, 0);
        }
    }

    // Aceptar y cancelar
    function accept() {
        clearErrors();
        send("accept", S.v, function (result) {
            if (!result || !result.error) {
                return;
            }
            if (S.page !== "main") {
                closePage();
            }
            var ctl = S.ctl[result.field];
            if (ctl) {
                setError(result.field, result.error);
                if (ctl.focus) {
                    ctl.focus.focus();
                }
                ctl.node.scrollIntoView({ block: "nearest" });
            }
            announce(result.error);
        });
    }

    function cancel() {
        send("cancel", null);
    }

    function init(payload) {
        if (S.nodes.app) {
            return;
        }
        S.p = payload;
        S.p.keytext = S.p.keytext || {};
        S.t = payload.texts;
        S.v = copy(payload.values);
        var app = document.getElementById(P + "-app");
        var n = S.nodes;
        n.app = app;
        n.title = el("h1", { text: payload.title });
        n.back = el("button", { type: "button", class: "back", hidden: true, onclick: closePage }, [
            svg("back", 16),
            S.t.back || payload.title,
        ]);
        n.head = el("div", { class: "head" }, [n.title, n.back]);
        n.main = el("div", {}, payload.cards.map(buildCard));
        n.sub = el("div", { hidden: true });
        n.body = el("div", { class: "body" }, [n.main, n.sub]);
        var ok = el("button", { type: "button", class: "btn primary", text: S.t.ok, onclick: accept });
        var no = el("button", { type: "button", class: "btn", text: S.t.cancel, onclick: cancel });
        n.foot = el("div", { class: "foot" }, [ok, no]);
        n.live = el("div", { class: "live", "aria-live": "polite" });
        n.shell = el("div", { class: "shell" }, [n.head, n.body, n.foot]);
        app.appendChild(n.shell);
        app.appendChild(n.live);
        payload.cards.forEach(function (card) {
            markParents(card.items, null);
        });
        refreshDependencies();
        refreshSummaries();
        n.body.addEventListener("scroll", updateScrollState);
        window.addEventListener("resize", updateScrollState);
        // La pagina entera nunca se desplaza (regla de FIX-030 de GritMap).
        window.addEventListener("scroll", function () {
            window.scrollTo(0, 0);
        });
        document.addEventListener("keydown", function (event) {
            if (document.querySelector("#" + P + "-app dialog[open]")) {
                return;
            }
            if (event.key === "Escape") {
                event.preventDefault();
                if (S.page !== "main") {
                    closePage();
                } else {
                    cancel();
                }
            } else if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
                event.preventDefault();
                accept();
            }
        });
        S.ready = true;
        var first = null;
        var focusCtl = payload.focus ? S.ctl[payload.focus] : null;
        if (focusCtl) {
            first = focusCtl.firstFocus ? focusCtl.firstFocus() : focusCtl.focus;
        }
        if (first) {
            first.focus({ preventScroll: true });
        }
        send("ready", naturalHeight());
        updateScrollState();
    }

    return {
        init: init,
    };
})();
