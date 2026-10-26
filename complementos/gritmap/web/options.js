/* GritMap - panel de opciones a medida (4.9.0).
 *
 * Python (options.py) pone en la pagina todo lo que hace falta y la pagina se
 * dibuja entera antes de verse. Lo elegido no se guarda hasta pulsar
 * Aceptar; mientras, la apariencia se ensena en el mapa de detras.
 *
 * Los controles son elementos de verdad (<button>, <input type="radio">,
 * <input type="checkbox">, <dialog>) dibujados a medida: conservan su
 * teclado, su foco y lo que anuncia el lector de pantalla.
 *
 * Todo lo que este codigo crea o busca empieza por «gritmap» (regla de
 * FIX-008) y el codigo es idempotente (regla de FIX-009): si se carga dos
 * veces, se reutiliza el que ya existe.
 */
var GritMapOptions = (typeof GritMapOptions !== "undefined" && GritMapOptions) || (function () {
    "use strict";

    var DAY_MS = 86400000;
    var PREVIEW_DELAY = 80;
    var REPEAT_DELAY = 400;
    var REPEAT_EVERY = 80;

    var S = {
        p: null,
        t: {},
        cfg: null,
        initialDates: "",
        decks: null,
        hidden: [],
        own: {},
        folded: {},
        page: "main",
        opener: null,
        goalProposed: null,
        undoLook: null,
        undoDate: null,
        editing: null,
        previewTimer: null,
        texts: { decks: null, dates: "", countdowns: {}, pause_days: "" },
        cal: null,
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
            if (value === null || value === undefined || value === false) {
                continue;
            }
            if (key === "class") {
                node.className = value;
            } else if (key === "text") {
                node.textContent = value;
            } else if (key.indexOf("on") === 0 && typeof value === "function") {
                node.addEventListener(key.slice(2), value);
            } else if (value === true) {
                node.setAttribute(key, "");
            } else {
                node.setAttribute(key, String(value));
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

    function svg(markup, size) {
        var holder = document.createElement("span");
        holder.innerHTML = '<svg width="' + (size || 16) + '" height="' + (size || 16)
            + '" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"'
            + ' stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            + markup + "</svg>";
        return holder.firstChild;
    }

    var ICONS = {
        tick: '<path d="M3.5 8.5 6.5 11.5 12.5 4.5"/>',
        chevron: '<path d="M6 3.5 10.5 8 6 12.5"/>',
        back: '<path d="M10 3.5 5.5 8 10 12.5"/>',
        calendar: '<rect x="2.5" y="3.5" width="11" height="10" rx="2"/><path d="M2.5 6.5h11M5.5 2v3M10.5 2v3"/>',
        pencil: '<path d="M10.5 2.5 13.5 5.5 6 13H3v-3z"/>',
        trash: '<path d="M3 4.5h10M6.5 4.5V3h3v1.5M4.5 4.5l.7 8.5h5.6l.7-8.5"/>',
        info: '<circle cx="8" cy="8" r="6"/><path d="M8 7.2v4M8 4.8v.2"/>',
        alert: '<circle cx="8" cy="8" r="6"/><path d="M8 4.8v4M8 11v.2"/>',
        fold: '<path d="M4.5 6 8 9.5 11.5 6"/>',
        unfold: '<path d="M6 4.5 9.5 8 6 11.5"/>',
    };

    function fill(template, values) {
        return String(template || "").replace(/\{(\w+)\}/g, function (match, name) {
            return name in values ? String(values[name]) : match;
        });
    }

    function parseDay(iso) {
        var parts = String(iso || "").split("-");
        return parts.length === 3 ? new Date(+parts[0], +parts[1] - 1, +parts[2]) : null;
    }

    function isoDay(day) {
        var m = String(day.getMonth() + 1);
        var d = String(day.getDate());
        return day.getFullYear() + "-" + (m.length < 2 ? "0" : "") + m + "-" + (d.length < 2 ? "0" : "") + d;
    }

    function addDays(iso, days) {
        var day = parseDay(iso);
        return isoDay(new Date(day.getTime() + days * DAY_MS + DAY_MS / 2));
    }

    function clampIso(iso, low, high) {
        if (low && iso < low) {
            return low;
        }
        if (high && iso > high) {
            return high;
        }
        return iso;
    }

    /* Toda fecha pide el calendario gregoriano, el de la rejilla (regla de
     * FIX-021). */
    function formatter(options) {
        var opts = Object.assign({ calendar: "gregory" }, options);
        try {
            return new Intl.DateTimeFormat(S.p.locale, opts);
        } catch (err) {
            try {
                return new Intl.DateTimeFormat(undefined, opts);
            } catch (err2) {
                return null;
            }
        }
    }

    function formatDay(iso, options) {
        var fmt = formatter(options || { day: "numeric", month: "short", year: "numeric" });
        var day = parseDay(iso);
        return fmt && day ? fmt.format(day) : iso;
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
        var cmd = S.p.prefix + action + (data === undefined ? "" : ":" + JSON.stringify(data));
        whenBridge(function () {
            pycmd(cmd, callback);
        });
    }

    function sendRaw(action, value) {
        whenBridge(function () {
            pycmd(S.p.prefix + action + ":" + value);
        });
    }

    function announce(text) {
        if (S.nodes.live) {
            S.nodes.live.textContent = "";
            S.nodes.live.textContent = text;
        }
    }

    // Lo elegido
    // -------------------------------------------------------------------

    function effectiveExcluded() {
        if (!S.decks) {
            return null;
        }
        var byName = {};
        S.decks.forEach(function (deck) {
            byName[deck.name] = deck;
        });
        var result = S.hidden.slice();
        S.decks.forEach(function (deck) {
            if (!S.own[deck.id]) {
                return;
            }
            // Un submazo de un mazo marcado ya va con su padre (FIX-016).
            var parts = deck.name.split("::");
            for (var i = parts.length - 1; i > 0; i--) {
                var parent = byName[parts.slice(0, i).join("::")];
                if (parent && S.own[parent.id]) {
                    return;
                }
            }
            result.push(deck.id);
        });
        return result;
    }

    function selection() {
        var c = S.cfg;
        return {
            theme: c.theme,
            cell_size: c.fit ? 0 : c.cell,
            border_radius: c.radius,
            measure: c.measure,
            avg_window: c.window,
            goal_mode: c.goal_mode,
            goal: c.goal,
            freezes: c.freezes,
            show_streak: c.show_streak,
            pause: c.pause_on ? { start: c.pause_start, end: c.pause_end } : null,
            excluded: effectiveExcluded(),
            key_dates: c.key_dates.slice(),
        };
    }

    function datesDirty() {
        return JSON.stringify(S.cfg.key_dates) !== S.initialDates;
    }

    function schedulePreview() {
        clearTimeout(S.previewTimer);
        S.previewTimer = setTimeout(function () {
            send("preview", selection());
        }, PREVIEW_DELAY);
    }

    /* Los textos con plurales y fechas los escribe Python, para que digan lo
     * mismo que el mapa. Llegan un instante despues; sus huecos ya estan
     * reservados, asi que nada salta. */
    function refreshTexts() {
        send("texts", { excluded: effectiveExcluded(), key_dates: S.cfg.key_dates, pause: selection().pause }, function (res) {
            if (!res) {
                return;
            }
            S.texts = res;
            updateSummaries();
            updatePause();
            if (S.page === "dates") {
                renderDateList();
            }
            if (S.page === "decks") {
                updateDeckCount();
            }
        });
    }

    // Piezas de la interfaz
    // -------------------------------------------------------------------

    /* Grupo de botones de opcion con aspecto de carril (patron Radio Group):
     * el tabulador entra en el elegido y las flechas cambian el valor. */
    function segmented(name, options, value, labelId, onChange) {
        var node = el("div", { class: "gritmap-o-seg", role: "radiogroup", "aria-labelledby": labelId });
        options.forEach(function (option) {
            var input = el("input", {
                type: "radio",
                name: "gritmap-o-" + name,
                value: String(option.id),
                checked: String(option.id) === String(value),
            });
            input.addEventListener("change", function () {
                if (input.checked) {
                    onChange(option.id);
                }
            });
            node.appendChild(el("label", {}, [input, el("span", { text: option.label })]));
        });
        return node;
    }

    function setSegmented(node, value) {
        node.querySelectorAll("input").forEach(function (input) {
            input.checked = input.value === String(value);
        });
    }

    /* Si algun valor no cabe en una linea, el carril pasa entero a lista
     * vertical: nunca se corta un texto dentro de un boton. */
    function fitSegmented() {
        document.querySelectorAll("#gritmap-o-app .gritmap-o-seg").forEach(function (node) {
            node.classList.remove("gritmap-o-vertical");
            var tooWide = Array.prototype.some.call(node.querySelectorAll("label"), function (label) {
                return label.scrollWidth > label.clientWidth + 1;
            });
            node.classList.toggle("gritmap-o-vertical", tooWide);
        });
        var chips = S.nodes.chips;
        if (chips) {
            chips.classList.remove("gritmap-o-one-col");
            var cut = Array.prototype.some.call(chips.querySelectorAll(".gritmap-o-chip-name"), function (name) {
                return name.scrollWidth > name.clientWidth + 1;
            });
            chips.classList.toggle("gritmap-o-one-col", cut);
        }
    }

    function checkbox(text, checked, onChange) {
        var input = el("input", { type: "checkbox", checked: checked });
        input.addEventListener("change", function () {
            onChange(input.checked);
        });
        var box = el("span", { class: "gritmap-o-box", "aria-hidden": "true" }, [svg(ICONS.tick, 14)]);
        var label = el("label", { class: "gritmap-o-check" }, [
            input,
            box,
            el("span", { class: "gritmap-o-check-text", text: text }),
        ]);
        return { node: label, input: input };
    }

    /* Campo numerico con − y + (patron Spinbutton): se puede escribir; las
     * flechas suben y bajan 1, RePag y AvPag 5, Inicio y Fin van al minimo y
     * al maximo; mantener pulsado − o + repite. Un valor fuera de rango se
     * corrige al limite mas cercano al salir del campo. */
    function stepper(opts) {
        var state = { value: opts.value, min: opts.min, max: opts.max };
        var input = el("input", {
            type: "text",
            inputmode: "numeric",
            role: "spinbutton",
            "aria-labelledby": opts.labelId,
            autocomplete: "off",
        });
        var minus = el("button", { type: "button", "aria-label": "−", tabindex: "-1" }, ["−"]);
        var plus = el("button", { type: "button", "aria-label": "+", tabindex: "-1" }, ["+"]);
        var unit = opts.unit ? el("span", { class: "gritmap-o-unit", text: opts.unit }) : null;
        var node = el("div", { class: "gritmap-o-step" }, [
            minus,
            el("span", { class: "gritmap-o-step-value" }, [input, unit]),
            plus,
        ]);

        function show() {
            input.value = String(state.value);
            input.setAttribute("aria-valuenow", String(state.value));
            input.setAttribute("aria-valuemin", String(state.min));
            input.setAttribute("aria-valuemax", String(state.max));
            input.setAttribute("aria-valuetext", state.value + (opts.unit ? " " + opts.unit : ""));
            minus.disabled = input.disabled || state.value <= state.min;
            plus.disabled = input.disabled || state.value >= state.max;
        }

        function set(value, quiet) {
            var next = Math.max(state.min, Math.min(state.max, Math.round(value)));
            var changed = next !== state.value;
            state.value = next;
            show();
            if (changed && !quiet) {
                opts.onChange(next);
            }
        }

        function hold(button, delta) {
            var timer = null;
            function stop() {
                clearTimeout(timer);
                clearInterval(timer);
                timer = null;
            }
            button.addEventListener("pointerdown", function (event) {
                if (button.disabled) {
                    return;
                }
                event.preventDefault();
                set(state.value + delta);
                stop();
                timer = setTimeout(function () {
                    timer = setInterval(function () {
                        set(state.value + delta);
                        if (button.disabled) {
                            stop();
                        }
                    }, REPEAT_EVERY);
                }, REPEAT_DELAY);
            });
            ["pointerup", "pointerleave", "pointercancel"].forEach(function (name) {
                button.addEventListener(name, stop);
            });
            button.addEventListener("keydown", function (event) {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    set(state.value + delta);
                }
            });
        }

        hold(minus, -1);
        hold(plus, 1);
        input.addEventListener("keydown", function (event) {
            var steps = { ArrowUp: 1, ArrowDown: -1, PageUp: 5, PageDown: -5 };
            if (event.key in steps) {
                event.preventDefault();
                set(state.value + steps[event.key]);
            } else if (event.key === "Home") {
                event.preventDefault();
                set(state.min);
            } else if (event.key === "End") {
                event.preventDefault();
                set(state.max);
            } else if (event.key === "Enter") {
                event.preventDefault();
                commit();
            }
        });
        function commit() {
            var typed = parseInt(input.value.replace(/[^\d-]/g, ""), 10);
            if (isNaN(typed)) {
                show();
                return;
            }
            set(typed);
        }
        input.addEventListener("blur", commit);
        show();
        return {
            node: node,
            input: input,
            get: function () {
                return state.value;
            },
            set: function (value) {
                set(value, true);
            },
            setMax: function (max) {
                state.max = max;
                if (state.value > max) {
                    set(max);
                } else {
                    show();
                }
            },
            setEnabled: function (on) {
                input.disabled = !on;
                show();
            },
        };
    }

    function summaryRow(title, onOpen) {
        var summary = el("span", { class: "gritmap-o-row-summary" }, [el("span", { class: "gritmap-o-bone" })]);
        var row = el("button", { type: "button", class: "gritmap-o-row", onclick: onOpen }, [
            el("span", { class: "gritmap-o-row-text" }, [el("span", { class: "gritmap-o-row-title", text: title }), summary]),
            el("span", { class: "gritmap-o-chevron" }, [svg(ICONS.chevron)]),
        ]);
        return { node: row, summary: summary };
    }

    function dateButton(onClick) {
        var label = el("span", {});
        var button = el("button", { type: "button", class: "gritmap-o-date-btn", "aria-haspopup": "dialog", onclick: onClick }, [
            label,
            svg(ICONS.calendar),
        ]);
        return { node: button, label: label };
    }

    function diamond() {
        var holder = document.createElement("span");
        holder.innerHTML = '<svg class="gritmap-o-diamond" viewBox="0 0 12 12" aria-hidden="true" focusable="false">'
            + '<polygon points="6,1.5 10.5,6 6,10.5 1.5,6"/></svg>';
        return holder.firstChild;
    }

    // Pagina principal
    // -------------------------------------------------------------------

    function buildMain() {
        var t = S.t;
        var c = S.cfg;
        var page = el("div", { "data-page": "main" });

        if (S.p.retired) {
            page.appendChild(el("div", { class: "gritmap-o-notice" }, [svg(ICONS.info), el("span", { text: S.p.retired })]));
        }

        // Apariencia
        var restore = el("button", { type: "button", class: "gritmap-o-link", onclick: restoreLook, text: t.opt_restore_look });
        var undo = el("button", { type: "button", class: "gritmap-o-link", hidden: true, onclick: undoRestore, text: t.undo });
        S.nodes.undoLook = undo;
        var chips = el("div", { class: "gritmap-o-chips", role: "radiogroup", "aria-labelledby": "gritmap-o-l-theme" });
        S.nodes.chips = chips;
        S.p.themes.forEach(function (theme) {
            var input = el("input", { type: "radio", name: "gritmap-o-theme", value: theme.name, checked: theme.name === c.theme });
            input.addEventListener("change", function () {
                if (input.checked) {
                    c.theme = theme.name;
                    lookChanged();
                }
            });
            chips.appendChild(el("label", { class: "gritmap-o-chip" }, [
                input,
                el("span", { class: "gritmap-o-swatch", "data-gritmap-theme": theme.name, style: "background:" + theme.color }),
                el("span", { class: "gritmap-o-chip-name", text: theme.label }),
                el("span", { class: "gritmap-o-tick" }, [svg(ICONS.tick)]),
            ]));
        });

        S.nodes.cell = stepper({
            labelId: "gritmap-o-l-size", min: S.p.limits.cell_min, max: S.p.limits.cell_max,
            value: c.fit ? S.p.defaults.cell_size || 24 : c.cell, unit: "px",
            onChange: function (value) {
                c.cell = value;
                lookChanged();
            },
        });
        var fit = checkbox(t.size_fit, c.fit, function (on) {
            c.fit = on;
            lookChanged();
        });
        S.nodes.fit = fit.input;
        S.nodes.sizeRule = el("p", { class: "gritmap-o-rule", text: t.fit_note });
        S.nodes.radius = stepper({
            labelId: "gritmap-o-l-radius", min: S.p.limits.radius_min, max: S.p.limits.radius_max,
            value: c.radius, unit: "px",
            onChange: function (value) {
                c.radius = value;
                lookChanged();
            },
        });
        S.nodes.radiusRule = el("p", { class: "gritmap-o-rule" });

        page.appendChild(el("section", { class: "gritmap-o-card", "aria-labelledby": "gritmap-o-h-look" }, [
            el("div", { class: "gritmap-o-card-head" }, [
                el("h2", { id: "gritmap-o-h-look", text: t.grp_look }),
                el("span", {}, [undo, restore]),
            ]),
            el("p", { class: "gritmap-o-card-note", text: t.look_live }),
            el("div", { class: "gritmap-o-option" }, [
                el("span", { class: "gritmap-o-label", id: "gritmap-o-l-theme", text: t.opt_theme }),
                chips,
            ]),
            el("div", { class: "gritmap-o-two" }, [
                el("div", { class: "gritmap-o-option" }, [
                    el("span", { class: "gritmap-o-label", id: "gritmap-o-l-size", text: t.opt_map_size }),
                    S.nodes.cell.node,
                    fit.node,
                    S.nodes.sizeRule,
                ]),
                el("div", { class: "gritmap-o-option" }, [
                    el("span", { class: "gritmap-o-label", id: "gritmap-o-l-radius", text: t.opt_radius }),
                    S.nodes.radius.node,
                    S.nodes.radiusRule,
                ]),
            ]),
        ]));

        // Que se cuenta
        S.nodes.measureHelp = el("p", { class: "gritmap-o-rule" });
        S.nodes.measure = segmented("measure", S.p.measures, c.measure, "gritmap-o-l-measure", function (value) {
            var proposed = c.goal_mode === "number" && c.goal === S.goalProposed;
            c.measure = value;
            if (proposed) {
                // La meta era la propuesta y no se toco: otra en la unidad
                // nueva, porque 50 repasos no son 50 nuevas.
                proposeGoal();
            }
            updateMeasure();
            updateGoal();
        });
        S.nodes.window = segmented("window", S.p.windows, c.window, "gritmap-o-l-window", function (value) {
            c.window = value;
        });
        var decksRow = summaryRow(t.opt_exclude, function () {
            openPage("decks", decksRow.node);
        });
        S.nodes.decksRow = decksRow;

        page.appendChild(el("section", { class: "gritmap-o-card", "aria-labelledby": "gritmap-o-h-count" }, [
            el("div", { class: "gritmap-o-card-head" }, [el("h2", { id: "gritmap-o-h-count", text: t.grp_count })]),
            el("p", { class: "gritmap-o-card-note", text: t.applied_on_ok }),
            el("div", { class: "gritmap-o-option" }, [
                el("span", { class: "gritmap-o-label", id: "gritmap-o-l-measure", text: t.opt_measure }),
                S.nodes.measure,
                S.nodes.measureHelp,
            ]),
            el("div", { class: "gritmap-o-option" }, [
                el("span", { class: "gritmap-o-label", id: "gritmap-o-l-window", text: t.opt_window }),
                S.nodes.window,
                el("p", { class: "gritmap-o-rule", text: t.window_help }),
            ]),
            el("div", { class: "gritmap-o-option" }, [decksRow.node]),
        ]));

        // Metas y fechas
        var streak = checkbox(t.opt_show_streak, c.show_streak, function (on) {
            c.show_streak = on;
            updateStreak();
        });
        S.nodes.streak = streak.input;
        S.nodes.streakNote = el("p", { class: "gritmap-o-rule", text: t.streak_off_note });
        S.nodes.goalMode = segmented("goal", S.p.goal_modes, c.goal_mode, "gritmap-o-l-goal", function (value) {
            c.goal_mode = value;
            if (value === "number") {
                // Al pasar a «Un numero», una meta a su medida (4.7.0).
                proposeGoal();
            }
            updateGoal();
        });
        S.nodes.goal = stepper({
            labelId: "gritmap-o-l-goal", min: S.p.limits.goal_min, max: S.p.limits.goal_max, value: c.goal,
            onChange: function (value) {
                c.goal = value;
                updateGoal();
            },
        });
        S.nodes.goalUnit = el("span", { class: "gritmap-o-unit" });
        S.nodes.goalNumber = el("div", {}, [
            el("div", { class: "gritmap-o-goal-row" }, [S.nodes.goal.node, S.nodes.goalUnit]),
            S.nodes.goalProposal = el("p", { class: "gritmap-o-rule" }),
        ]);
        S.nodes.goalDue = el("p", { class: "gritmap-o-rule", text: t.goal_due_note });

        var freezes = checkbox(t.opt_freezes, c.freezes, function (on) {
            c.freezes = on;
        });
        S.nodes.freezes = freezes.input;
        var freezeRule = t.freeze_tip + (S.p.freezes_now ? " " + S.p.freezes_now : "");

        var pause = checkbox(t.opt_pause, c.pause_on, function (on) {
            c.pause_on = on;
            updatePause();
            refreshTexts();
        });
        S.nodes.pause = pause.input;
        S.nodes.pauseStart = dateButton(function () {
            openCalendar(S.nodes.pauseStart.node, c.pause_start, S.p.limits.pause_min, S.p.limits.date_max, function (iso) {
                c.pause_start = iso;
                c.pause_end = clampIso(c.pause_end, iso, addDays(iso, S.p.limits.max_pause - 1));
                updatePause();
                refreshTexts();
            });
        });
        S.nodes.pauseEnd = dateButton(function () {
            openCalendar(S.nodes.pauseEnd.node, c.pause_end, c.pause_start, addDays(c.pause_start, S.p.limits.max_pause - 1), function (iso) {
                c.pause_end = iso;
                updatePause();
                refreshTexts();
            });
        });
        S.nodes.pauseDays = el("span", { class: "gritmap-o-unit" });
        S.nodes.pauseDetail = el("div", { class: "gritmap-o-pause" }, [
            el("span", { text: t.pause_from }),
            S.nodes.pauseStart.node,
            el("span", { text: t.pause_to }),
            S.nodes.pauseEnd.node,
            S.nodes.pauseDays,
        ]);

        S.nodes.group = el("div", { class: "gritmap-o-group" }, [
            el("div", { class: "gritmap-o-option" }, [
                el("span", { class: "gritmap-o-label", id: "gritmap-o-l-goal", text: t.opt_goal }),
                S.nodes.goalMode,
                S.nodes.goalNumber,
                S.nodes.goalDue,
            ]),
            el("div", { class: "gritmap-o-option" }, [freezes.node, el("p", { class: "gritmap-o-sub-rule", text: freezeRule })]),
            el("div", { class: "gritmap-o-option" }, [
                pause.node,
                S.nodes.pauseDetail,
                el("p", { class: "gritmap-o-sub-rule", text: t.pause_rule }),
            ]),
        ]);

        var datesRow = summaryRow(t.opt_key_dates, function () {
            openPage("dates", datesRow.node);
        });
        S.nodes.datesRow = datesRow;

        page.appendChild(el("section", { class: "gritmap-o-card", "aria-labelledby": "gritmap-o-h-goals" }, [
            el("div", { class: "gritmap-o-card-head" }, [el("h2", { id: "gritmap-o-h-goals", text: t.grp_goals })]),
            el("div", { class: "gritmap-o-option" }, [streak.node, S.nodes.streakNote, S.nodes.group]),
            el("div", { class: "gritmap-o-option" }, [datesRow.node]),
        ]));
        return page;
    }

    function lookChanged() {
        if (S.undoLook && !S.restoring) {
            S.undoLook = null;
            S.nodes.undoLook.hidden = true;
        }
        updateSize();
        schedulePreview();
    }

    function restoreLook() {
        var c = S.cfg;
        var d = S.p.defaults;
        S.undoLook = { theme: c.theme, cell: c.cell, fit: c.fit, radius: c.radius };
        S.restoring = true;
        setLook(d.theme, d.cell_size === 0 ? c.cell : d.cell_size, d.cell_size === 0, d.border_radius);
        S.restoring = false;
        S.nodes.undoLook.hidden = false;
        announce(S.t.opt_restore_look);
        schedulePreview();
    }

    function undoRestore() {
        var u = S.undoLook;
        if (!u) {
            return;
        }
        S.restoring = true;
        setLook(u.theme, u.cell, u.fit, u.radius);
        S.restoring = false;
        S.undoLook = null;
        S.nodes.undoLook.hidden = true;
        schedulePreview();
    }

    function setLook(theme, cell, fit, radius) {
        var c = S.cfg;
        c.theme = theme;
        c.cell = cell;
        c.fit = fit;
        c.radius = radius;
        S.nodes.chips.querySelectorAll("input").forEach(function (input) {
            input.checked = input.value === theme;
        });
        S.nodes.cell.set(cell);
        S.nodes.fit.checked = fit;
        updateSize();
        S.nodes.radius.set(radius);
    }

    function updateSize() {
        var c = S.cfg;
        S.nodes.cell.setEnabled(!c.fit);
        S.nodes.sizeRule.hidden = !c.fit;
        // El redondeo llega como mucho a la mitad del cuadrito (4.7.0).
        var half = Math.min(S.p.limits.radius_max, Math.floor((c.fit ? 14 : c.cell) / 2));
        S.nodes.radius.setMax(half);
        c.radius = S.nodes.radius.get();
        S.nodes.radiusRule.textContent = fill(S.t.radius_max, { n: half });
    }

    function updateMeasure() {
        var m = S.p.measures.filter(function (item) {
            return item.id === S.cfg.measure;
        })[0] || S.p.measures[0];
        S.nodes.measureHelp.textContent = m.help;
        S.nodes.goalUnit.textContent = fill(S.t.goal_unit_day, { unit: m.unit });
    }

    function proposeGoal() {
        var proposal = S.p.proposals[S.cfg.measure] || { value: S.cfg.goal };
        S.cfg.goal = proposal.value;
        S.goalProposed = proposal.value;
        S.nodes.goal.set(proposal.value);
    }

    function updateGoal() {
        var c = S.cfg;
        S.nodes.goalNumber.hidden = c.goal_mode !== "number";
        S.nodes.goalDue.hidden = c.goal_mode !== "due";
        var proposal = S.p.proposals[c.measure] || {};
        var showProposal = c.goal_mode === "number" && proposal.average !== null && proposal.average !== undefined;
        S.nodes.goalProposal.hidden = !showProposal;
        if (showProposal) {
            S.nodes.goalProposal.textContent = fill(S.t.goal_proposal_line, { n: proposal.average });
        }
    }

    function updateStreak() {
        var on = S.cfg.show_streak;
        S.nodes.streakNote.hidden = on;
        S.nodes.group.classList.toggle("gritmap-o-off", !on);
        S.nodes.group.querySelectorAll("input, button").forEach(function (node) {
            node.disabled = !on;
        });
        S.nodes.goal.setEnabled(on);
        if (on) {
            updatePause();
        }
    }

    function updatePause() {
        var c = S.cfg;
        S.nodes.pauseDetail.hidden = !c.pause_on;
        S.nodes.pauseStart.label.textContent = formatDay(c.pause_start);
        S.nodes.pauseEnd.label.textContent = formatDay(c.pause_end);
        S.nodes.pauseDays.textContent = S.texts.pause_days ? "· " + S.texts.pause_days : "";
        reportHeight();
    }

    function updateSummaries() {
        var decks = S.nodes.decksRow.summary;
        decks.textContent = "";
        if (S.texts.decks === null || S.texts.decks === undefined) {
            decks.appendChild(el("span", { class: "gritmap-o-bone" }));
        } else {
            decks.textContent = S.texts.decks;
        }
        S.nodes.datesRow.summary.textContent = S.texts.dates || "";
    }

    // Subpaginas
    // -------------------------------------------------------------------

    function openPage(name, opener) {
        closeCalendar();
        S.page = name;
        S.opener = opener || null;
        S.nodes.back.hidden = false;
        S.nodes.title.textContent = name === "decks" ? S.t.opt_exclude : S.t.opt_key_dates;
        S.nodes.pages.main.hidden = true;
        S.nodes.pages.decks.hidden = name !== "decks";
        S.nodes.pages.dates.hidden = name !== "dates";
        S.nodes.body.scrollTop = 0;
        if (name === "decks") {
            renderDecks();
            if (S.nodes.search) {
                S.nodes.search.focus();
            }
        } else {
            renderDateList();
            S.nodes.kdName.focus();
        }
        reportHeight();
    }

    function backToMain() {
        closeCalendar();
        cancelEdit();
        S.page = "main";
        S.nodes.back.hidden = true;
        S.nodes.title.textContent = S.t.nav_opts;
        S.nodes.pages.main.hidden = false;
        S.nodes.pages.decks.hidden = true;
        S.nodes.pages.dates.hidden = true;
        updateSummaries();
        // El foco vuelve a la fila que abrio la subpagina (patron de dialogo).
        if (S.opener) {
            S.opener.focus();
        }
        reportHeight();
    }

    function buildDecksPage() {
        var page = el("div", { "data-page": "decks", hidden: true });
        S.nodes.search = el("input", {
            type: "search",
            class: "gritmap-o-search",
            placeholder: S.t.search,
            "aria-label": S.t.search,
            oninput: renderDecks,
        });
        S.nodes.tree = el("ul", { class: "gritmap-o-tree" });
        S.nodes.deckEmpty = el("p", { class: "gritmap-o-empty", text: S.t.decks_no_match, hidden: true });
        S.nodes.deckCount = el("p", { class: "gritmap-o-count" });
        page.appendChild(S.nodes.search);
        page.appendChild(el("section", { class: "gritmap-o-card", style: "margin-top:16px", "aria-label": S.t.opt_exclude }, [
            S.nodes.tree,
            S.nodes.deckEmpty,
        ]));
        page.appendChild(el("p", { class: "gritmap-o-rule", text: S.t.decks_sub_note }));
        page.appendChild(S.nodes.deckCount);
        return page;
    }

    function updateDeckCount() {
        if (S.nodes.deckCount) {
            S.nodes.deckCount.textContent = S.texts.decks || "";
        }
    }

    /* Casillas con botones de plegar (patrones Checkbox y Disclosure). Un
     * mazo marcado marca y bloquea sus submazos (regla de FIX-016). */
    function renderDecks() {
        var tree = S.nodes.tree;
        if (!tree) {
            return;
        }
        tree.textContent = "";
        if (!S.decks) {
            for (var b = 0; b < 4; b++) {
                tree.appendChild(el("li", {}, [el("span", { class: "gritmap-o-bone" })]));
            }
            return;
        }
        var wanted = (S.nodes.search.value || "").trim().toLocaleLowerCase();
        var hasChildren = {};
        S.decks.forEach(function (deck) {
            var parts = deck.name.split("::");
            if (parts.length > 1) {
                hasChildren[parts.slice(0, -1).join("::")] = true;
            }
        });
        var visible = {};
        if (wanted) {
            S.decks.forEach(function (deck) {
                if (deck.name.toLocaleLowerCase().indexOf(wanted) !== -1) {
                    var parts = deck.name.split("::");
                    for (var i = 1; i <= parts.length; i++) {
                        visible[parts.slice(0, i).join("::")] = true;
                    }
                }
            });
        }
        var byName = {};
        S.decks.forEach(function (deck) {
            byName[deck.name] = deck;
        });
        var shown = 0;
        S.decks.forEach(function (deck) {
            var parts = deck.name.split("::");
            if (wanted && !visible[deck.name]) {
                return;
            }
            var locked = false;
            for (var i = parts.length - 1; i > 0; i--) {
                var ancestor = byName[parts.slice(0, i).join("::")];
                if (!wanted && ancestor && S.folded[ancestor.id]) {
                    return;
                }
                if (ancestor && S.own[ancestor.id]) {
                    locked = true;
                }
            }
            shown++;
            var box = checkbox(deck.leaf, locked || !!S.own[deck.id], function (on) {
                if (on) {
                    S.own[deck.id] = true;
                } else {
                    delete S.own[deck.id];
                }
                renderDecks();
                refreshTexts();
            });
            box.input.disabled = locked;
            box.input.setAttribute("aria-label", deck.name);
            if (locked) {
                box.node.classList.add("gritmap-o-locked");
            }
            var fold;
            if (hasChildren[deck.name]) {
                var folded = !!S.folded[deck.id];
                fold = el("button", {
                    type: "button",
                    class: "gritmap-o-fold",
                    "aria-expanded": folded ? "false" : "true",
                    "aria-label": deck.name,
                    onclick: function () {
                        if (S.folded[deck.id]) {
                            delete S.folded[deck.id];
                        } else {
                            S.folded[deck.id] = true;
                        }
                        renderDecks();
                        var again = tree.querySelector("[data-gritmap-deck='" + deck.id + "'] .gritmap-o-fold");
                        if (again) {
                            again.focus();
                        }
                    },
                }, [svg(folded ? ICONS.unfold : ICONS.fold)]);
            } else {
                fold = el("span", { class: "gritmap-o-fold-space" });
            }
            tree.appendChild(el("li", {
                "data-gritmap-deck": deck.id,
                style: "padding-inline-start:" + (deck.depth * 24) + "px",
            }, [fold, box.node]));
        });
        S.nodes.deckEmpty.hidden = shown > 0;
        updateDeckCount();
        reportHeight();
    }

    function buildDatesPage() {
        var t = S.t;
        var page = el("div", { "data-page": "dates", hidden: true });
        S.nodes.kdName = el("input", {
            type: "text",
            class: "gritmap-o-input",
            id: "gritmap-o-kd-name",
            maxlength: S.p.limits.max_label,
            placeholder: t.kd_name_ph,
            autocomplete: "off",
            onkeydown: function (event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    addDate();
                }
            },
            oninput: clearError,
        });
        S.kdDay = S.p.today;
        S.nodes.kdDate = dateButton(function () {
            openCalendar(S.nodes.kdDate.node, S.kdDay, S.p.limits.date_min, S.p.limits.date_max, function (iso) {
                S.kdDay = iso;
                S.nodes.kdDate.label.textContent = formatDay(iso);
                clearError();
            });
        });
        S.nodes.kdDate.node.id = "gritmap-o-kd-date";
        S.nodes.kdDate.label.textContent = formatDay(S.kdDay);
        // Los avisos salen encima de los campos, en rojo y con icono.
        S.nodes.kdError = el("p", { class: "gritmap-o-error", role: "alert", hidden: true });
        page.appendChild(el("section", { class: "gritmap-o-card", "aria-labelledby": "gritmap-o-h-new" }, [
            el("div", { class: "gritmap-o-card-head" }, [el("h2", { id: "gritmap-o-h-new", text: t.kd_new })]),
            S.nodes.kdError,
            el("div", { class: "gritmap-o-form" }, [
                el("div", {}, [el("label", { class: "gritmap-o-label", for: "gritmap-o-kd-name", text: t.kd_field_name }), S.nodes.kdName]),
                el("div", {}, [el("label", { class: "gritmap-o-label", for: "gritmap-o-kd-date", text: t.kd_field_date }), S.nodes.kdDate.node]),
                el("div", { class: "gritmap-o-form-actions" }, [
                    el("button", { type: "button", class: "gritmap-o-btn", onclick: addDate, text: t.add }),
                ]),
            ]),
        ]));
        S.nodes.kdList = el("ul", { class: "gritmap-o-dates" });
        S.nodes.kdListCard = el("section", { class: "gritmap-o-card", "aria-label": t.opt_key_dates }, [S.nodes.kdList]);
        page.appendChild(S.nodes.kdListCard);
        S.nodes.kdCount = el("p", { class: "gritmap-o-count" });
        page.appendChild(S.nodes.kdCount);
        return page;
    }

    function showError(text) {
        S.nodes.kdError.textContent = "";
        S.nodes.kdError.appendChild(svg(ICONS.alert));
        S.nodes.kdError.appendChild(document.createTextNode(text));
        S.nodes.kdError.hidden = false;
        S.nodes.kdName.classList.add("gritmap-o-invalid");
        S.nodes.kdName.setAttribute("aria-invalid", "true");
        reportHeight();
    }

    function clearError() {
        if (!S.nodes.kdError.hidden) {
            S.nodes.kdError.hidden = true;
            S.nodes.kdName.classList.remove("gritmap-o-invalid");
            S.nodes.kdName.removeAttribute("aria-invalid");
            reportHeight();
        }
    }

    function cleanLabel(text) {
        return String(text || "").replace(/\s+/g, " ").trim().slice(0, S.p.limits.max_label);
    }

    function sortDates() {
        S.cfg.key_dates.sort(function (a, b) {
            if (a.day !== b.day) {
                return a.day < b.day ? -1 : 1;
            }
            return a.label.toLocaleLowerCase().localeCompare(b.label.toLocaleLowerCase());
        });
    }

    function hasDate(day, label, except) {
        return S.cfg.key_dates.some(function (item) {
            return item !== except && item.day === day && item.label === label;
        });
    }

    function addDate() {
        var label = cleanLabel(S.nodes.kdName.value);
        if (!label) {
            showError(S.t.kd_name_required);
            S.nodes.kdName.focus();
            return;
        }
        if (S.cfg.key_dates.length >= S.p.limits.max_key_dates) {
            showError(fill(S.t.kd_limit, { count: S.p.limits.max_key_dates }));
            return;
        }
        if (hasDate(S.kdDay, label)) {
            showError(S.t.kd_duplicate);
            return;
        }
        clearError();
        S.cfg.key_dates.push({ day: S.kdDay, label: label });
        sortDates();
        S.undoDate = null;
        S.nodes.kdName.value = "";
        S.nodes.kdName.focus();
        renderDateList();
        refreshTexts();
    }

    function removeDate(item) {
        var index = S.cfg.key_dates.indexOf(item);
        if (index === -1) {
            return;
        }
        S.cfg.key_dates.splice(index, 1);
        S.undoDate = { item: item };
        cancelEdit();
        renderDateList();
        refreshTexts();
        var message = fill(S.t.kd_deleted, { name: item.label });
        announce(message);
        var undo = S.nodes.kdList.querySelector(".gritmap-o-undo-row button");
        if (undo) {
            undo.focus();
        }
    }

    function undoDelete() {
        if (!S.undoDate) {
            return;
        }
        S.cfg.key_dates.push(S.undoDate.item);
        sortDates();
        var item = S.undoDate.item;
        S.undoDate = null;
        renderDateList();
        refreshTexts();
        focusDateRow(item);
    }

    function focusDateRow(item) {
        var index = S.cfg.key_dates.indexOf(item);
        var row = S.nodes.kdList.querySelectorAll("li[data-gritmap-kd]")[index];
        var button = row ? row.querySelector(".gritmap-o-icon-btn") : null;
        if (button) {
            button.focus();
        }
    }

    function startEdit(item) {
        S.editing = { item: item, day: item.day };
        renderDateList();
        var input = S.nodes.kdList.querySelector(".gritmap-o-date-edit input");
        if (input) {
            input.focus();
            input.select();
        }
    }

    function cancelEdit() {
        if (S.editing) {
            var item = S.editing.item;
            S.editing = null;
            if (S.page === "dates") {
                renderDateList();
                focusDateRow(item);
            }
            return true;
        }
        return false;
    }

    function saveEdit(input) {
        var edit = S.editing;
        if (!edit) {
            return;
        }
        var label = cleanLabel(input.value);
        if (!label || hasDate(edit.day, label, edit.item)) {
            // Vacio o repetido: vuelve a como estaba.
            cancelEdit();
            return;
        }
        edit.item.label = label;
        edit.item.day = edit.day;
        S.editing = null;
        sortDates();
        S.undoDate = null;
        renderDateList();
        refreshTexts();
        focusDateRow(edit.item);
    }

    function renderDateList() {
        var list = S.nodes.kdList;
        if (!list) {
            return;
        }
        list.textContent = "";
        var today = S.p.today;
        if (S.undoDate) {
            var message = fill(S.t.kd_deleted, { name: S.undoDate.item.label });
            list.appendChild(el("li", { class: "gritmap-o-undo-row" }, [
                el("span", { style: "flex:1", text: message }),
                el("button", { type: "button", class: "gritmap-o-link", onclick: undoDelete, text: S.t.undo }),
            ]));
        }
        S.cfg.key_dates.forEach(function (item) {
            var past = item.day < today;
            var row = el("li", { "data-gritmap-kd": "1", class: past ? "gritmap-o-past" : "" }, [diamond()]);
            if (S.editing && S.editing.item === item) {
                var input = el("input", {
                    type: "text",
                    class: "gritmap-o-input",
                    value: item.label,
                    maxlength: S.p.limits.max_label,
                    "aria-label": S.t.kd_field_name,
                    onkeydown: function (event) {
                        if (event.key === "Enter") {
                            event.preventDefault();
                            saveEdit(input);
                        }
                    },
                });
                var dayButton = dateButton(function () {
                    openCalendar(dayButton.node, S.editing.day, S.p.limits.date_min, S.p.limits.date_max, function (iso) {
                        S.editing.day = iso;
                        dayButton.label.textContent = formatDay(iso);
                    });
                });
                dayButton.label.textContent = formatDay(S.editing.day);
                row.appendChild(el("div", { class: "gritmap-o-date-edit" }, [
                    input,
                    dayButton.node,
                    el("button", { type: "button", class: "gritmap-o-btn", onclick: function () {
                        saveEdit(input);
                    }, text: S.t.save }),
                ]));
            } else {
                var when = S.texts.countdowns ? S.texts.countdowns[item.day] || "" : "";
                var name = el("span", { class: "gritmap-o-date-name", text: item.label, ondblclick: function () {
                    startEdit(item);
                } });
                row.appendChild(el("span", { class: "gritmap-o-date-day", text: formatDay(item.day) }));
                row.appendChild(name);
                row.appendChild(el("span", { class: "gritmap-o-date-when", text: when }));
                row.appendChild(el("button", {
                    type: "button",
                    class: "gritmap-o-icon-btn",
                    title: S.t.kd_edit,
                    "aria-label": S.t.kd_edit + " " + item.label,
                    onclick: function () {
                        startEdit(item);
                    },
                }, [svg(ICONS.pencil)]));
                row.appendChild(el("button", {
                    type: "button",
                    class: "gritmap-o-icon-btn",
                    title: S.t.delete,
                    "aria-label": S.t.delete + " " + item.label,
                    onclick: function () {
                        removeDate(item);
                    },
                }, [svg(ICONS.trash)]));
                // Supr con el foco en la fila elimina, como antes.
                row.addEventListener("keydown", function (event) {
                    if (event.key === "Delete" && event.target.tagName !== "INPUT") {
                        event.preventDefault();
                        removeDate(item);
                    }
                });
            }
            list.appendChild(row);
        });
        S.nodes.kdListCard.hidden = !S.cfg.key_dates.length && !S.undoDate;
        S.nodes.kdCount.textContent = fill(S.t.kd_count, {
            count: S.cfg.key_dates.length,
            max: S.p.limits.max_key_dates,
        });
        reportHeight();
    }

    // Calendario propio
    // -------------------------------------------------------------------

    /* Capa flotante con el aspecto del mapa (patron de selector de fecha):
     * hoy con borde, el dia elegido en azul y las fechas clave con un rombo;
     * los dias fuera de rango no responden. Teclas: flechas, Inicio y Fin,
     * RePag y AvPag (con Mayus, de ano en ano), Intro elige y Esc cierra. */
    function openCalendar(anchor, value, min, max, onPick) {
        closeCalendar();
        var focusDay = clampIso(value || S.p.today, min, max);
        var cal = { anchor: anchor, min: min, max: max, onPick: onPick, value: value, focus: focusDay };
        S.cal = cal;
        var node = el("div", { class: "gritmap-o-cal", role: "dialog", "aria-modal": "false" });
        cal.node = node;
        S.nodes.app.appendChild(node);
        drawCalendar(true);
        placeCalendar();
    }

    function placeCalendar() {
        var cal = S.cal;
        if (!cal) {
            return;
        }
        var box = cal.anchor.getBoundingClientRect();
        var width = cal.node.offsetWidth;
        var height = cal.node.offsetHeight;
        var left = Math.min(Math.max(8, box.left), window.innerWidth - width - 8);
        var top = box.bottom + 4;
        if (top + height > window.innerHeight - 8) {
            top = Math.max(8, box.top - height - 4);
        }
        cal.node.style.left = left + "px";
        cal.node.style.top = top + "px";
    }

    function drawCalendar(takeFocus) {
        var cal = S.cal;
        var focus = parseDay(cal.focus);
        var year = focus.getFullYear();
        var month = focus.getMonth();
        var node = cal.node;
        node.textContent = "";
        var monthFmt = formatter({ month: "long", year: "numeric" });
        var title = monthFmt ? monthFmt.format(new Date(year, month, 1)) : year + "-" + (month + 1);
        node.setAttribute("aria-label", title);
        node.appendChild(el("div", { class: "gritmap-o-cal-head" }, [
            el("button", { type: "button", class: "gritmap-o-icon-btn", "aria-label": S.t.month_prev, onclick: function () {
                moveCalendar(-1, "month");
            } }, [svg(ICONS.back)]),
            el("span", { "aria-live": "polite", text: title }),
            el("button", { type: "button", class: "gritmap-o-icon-btn", "aria-label": S.t.month_next, onclick: function () {
                moveCalendar(1, "month");
            } }, [svg(ICONS.chevron)]),
        ]));
        var grid = el("div", { class: "gritmap-o-cal-grid", role: "grid" });
        var narrow = formatter({ weekday: "narrow" });
        for (var w = 0; w < 7; w++) {
            // Semana desde el lunes, como el mapa (el 1-1-2024 fue lunes).
            grid.appendChild(el("span", { class: "gritmap-o-cal-wd", "aria-hidden": "true", text: narrow ? narrow.format(new Date(2024, 0, 1 + w)) : "" }));
        }
        var first = new Date(year, month, 1);
        var offset = (first.getDay() + 6) % 7;
        var start = new Date(year, month, 1 - offset);
        var keyDays = {};
        S.cfg.key_dates.forEach(function (item) {
            keyDays[item.day] = true;
        });
        var longFmt = formatter({ weekday: "long", day: "numeric", month: "long", year: "numeric" });
        for (var i = 0; i < 42; i++) {
            var day = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
            var iso = isoDay(day);
            var outOfRange = (cal.min && iso < cal.min) || (cal.max && iso > cal.max);
            var classes = ["gritmap-o-cal-day"];
            if (day.getMonth() !== month) {
                classes.push("gritmap-o-other");
            }
            if (iso === S.p.today) {
                classes.push("gritmap-o-today");
            }
            if (keyDays[iso]) {
                classes.push("gritmap-o-key");
            }
            var button = el("button", {
                type: "button",
                class: classes.join(" "),
                "data-gritmap-day": iso,
                "aria-selected": iso === cal.value ? "true" : "false",
                "aria-label": longFmt ? longFmt.format(day) : iso,
                tabindex: iso === cal.focus ? "0" : "-1",
                disabled: outOfRange,
                text: String(day.getDate()),
            });
            grid.appendChild(button);
        }
        grid.addEventListener("click", function (event) {
            var target = event.target.closest ? event.target.closest("[data-gritmap-day]") : null;
            if (target && !target.disabled) {
                pickDay(target.getAttribute("data-gritmap-day"));
            }
        });
        grid.addEventListener("keydown", onCalendarKey);
        node.appendChild(grid);
        if (takeFocus) {
            var focused = grid.querySelector("[tabindex='0']");
            if (focused) {
                focused.focus();
            }
        }
    }

    function moveCalendar(amount, unit) {
        var cal = S.cal;
        var focus = parseDay(cal.focus);
        var next;
        if (unit === "month") {
            next = new Date(focus.getFullYear(), focus.getMonth() + amount, 1);
            var last = new Date(next.getFullYear(), next.getMonth() + 1, 0).getDate();
            next.setDate(Math.min(focus.getDate(), last));
        } else {
            next = new Date(focus.getTime() + amount * DAY_MS + DAY_MS / 2);
        }
        cal.focus = clampIso(isoDay(next), cal.min, cal.max);
        drawCalendar(true);
    }

    function onCalendarKey(event) {
        var cal = S.cal;
        var focus = parseDay(cal.focus);
        var weekday = (focus.getDay() + 6) % 7;
        var steps = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
        if (event.key in steps) {
            moveCalendar(steps[event.key], "day");
        } else if (event.key === "Home") {
            moveCalendar(-weekday, "day");
        } else if (event.key === "End") {
            moveCalendar(6 - weekday, "day");
        } else if (event.key === "PageUp" || event.key === "PageDown") {
            moveCalendar((event.key === "PageUp" ? -1 : 1) * (event.shiftKey ? 12 : 1), "month");
        } else if (event.key === "Enter" || event.key === " ") {
            pickDay(cal.focus);
        } else {
            return;
        }
        event.preventDefault();
    }

    function pickDay(iso) {
        var cal = S.cal;
        if (!cal) {
            return;
        }
        var onPick = cal.onPick;
        var anchor = cal.anchor;
        closeCalendar();
        onPick(iso);
        anchor.focus();
    }

    function closeCalendar(returnFocus) {
        var cal = S.cal;
        if (!cal) {
            return false;
        }
        S.cal = null;
        if (cal.node.parentNode) {
            cal.node.parentNode.removeChild(cal.node);
        }
        if (returnFocus) {
            cal.anchor.focus();
        }
        return true;
    }

    // Cerrar, aceptar y cancelar
    // -------------------------------------------------------------------

    /* Solo se pregunta antes de perder lo que se escribio a mano: las fechas
     * clave. Todo lo demas se vuelve a elegir en un clic. */
    function requestCancel() {
        if (datesDirty()) {
            S.nodes.confirm.showModal();
            S.nodes.keepEditing.focus();
            return;
        }
        send("cancel");
    }

    function accept() {
        // El ultimo numero escrito cuenta aunque no se haya salido del campo.
        if (document.activeElement && document.activeElement.blur) {
            document.activeElement.blur();
        }
        send("accept", selection());
    }

    function buildConfirm() {
        var t = S.t;
        var keep = el("button", { type: "button", class: "gritmap-o-btn gritmap-o-primary", text: t.keep_editing, onclick: function () {
            dialog.close();
        } });
        var discard = el("button", { type: "button", class: "gritmap-o-btn", text: t.discard, onclick: function () {
            dialog.close();
            send("cancel");
        } });
        var dialog = el("dialog", { "aria-labelledby": "gritmap-o-confirm-title" }, [
            el("h2", { id: "gritmap-o-confirm-title", text: t.discard_q }),
            el("p", { text: t.discard_body }),
            el("div", { class: "gritmap-o-dialog-actions" }, [discard, keep]),
        ]);
        S.nodes.keepEditing = keep;
        return dialog;
    }

    /* Esc cierra siempre la capa de mas arriba: el calendario, la edicion de
     * una fecha, la subpagina y, en la principal, la ventana (como Cancelar).
     * Se atiende aqui, antes que el cierre de Anki. */
    function onEscape(event) {
        if (event.key !== "Escape") {
            return;
        }
        if (S.nodes.confirm && S.nodes.confirm.open) {
            // El <dialog> se cierra solo con Esc.
            event.stopImmediatePropagation();
            return;
        }
        event.preventDefault();
        event.stopImmediatePropagation();
        if (closeCalendar(true)) {
            return;
        }
        if (cancelEdit()) {
            return;
        }
        if (S.page !== "main") {
            backToMain();
            return;
        }
        requestCancel();
    }

    function onOutsideClick(event) {
        if (S.cal && !S.cal.node.contains(event.target) && !S.cal.anchor.contains(event.target)) {
            closeCalendar();
        }
    }

    // Alto de la ventana
    // -------------------------------------------------------------------

    var heightTimer = null;

    function naturalHeight() {
        var n = S.nodes;
        var bodyStyle = window.getComputedStyle(n.body);
        var padding = parseFloat(bodyStyle.paddingTop) + parseFloat(bodyStyle.paddingBottom);
        return Math.ceil(n.head.offsetHeight + n.content.offsetHeight + padding + n.foot.offsetHeight);
    }

    function updateScrollState() {
        var body = S.nodes.body;
        var overflow = body.scrollHeight > body.clientHeight + 1;
        S.nodes.shell.classList.toggle("gritmap-o-overflow", overflow);
        S.nodes.shell.classList.toggle("gritmap-o-scrolled", overflow && body.scrollTop > 0);
    }

    function reportHeight() {
        if (!S.ready) {
            return;
        }
        clearTimeout(heightTimer);
        heightTimer = setTimeout(function () {
            sendRaw("height", naturalHeight());
            updateScrollState();
        }, 0);
    }

    // Arranque y ordenes de Python
    // -------------------------------------------------------------------

    function init(payload) {
        var app = document.getElementById("gritmap-o-app");
        if (!app || app.getAttribute("data-gritmap-ready")) {
            return;
        }
        app.setAttribute("data-gritmap-ready", "1");
        S.p = payload;
        S.t = payload.texts;
        var c = payload.cfg;
        var today = payload.today;
        S.cfg = {
            theme: c.theme,
            cell: c.cell_size === 0 ? payload.defaults.cell_size || 24 : c.cell_size,
            fit: c.cell_size === 0,
            radius: c.border_radius,
            measure: c.measure,
            window: c.avg_window,
            goal_mode: c.goal_mode,
            goal: c.goal,
            freezes: c.freezes,
            show_streak: c.show_streak,
            pause_on: !!c.pause,
            pause_start: c.pause ? c.pause.start : today,
            pause_end: c.pause ? c.pause.end : addDays(today, 6),
            key_dates: c.key_dates.map(function (item) {
                return { day: item.day, label: item.label };
            }),
        };
        (c.excluded || []).forEach(function (id) {
            S.own[id] = true;
        });
        S.initialDates = JSON.stringify(S.cfg.key_dates);
        S.goalProposed = c.goal;

        var n = S.nodes;
        n.app = app;
        n.back = el("button", { type: "button", class: "gritmap-o-back", hidden: true, onclick: backToMain }, [
            svg(ICONS.back),
            el("span", { text: S.t.nav_opts }),
        ]);
        n.title = el("h1", { text: S.t.nav_opts });
        n.head = el("header", { class: "gritmap-o-head" }, [n.back, n.title]);
        n.pages = { main: buildMain(), decks: buildDecksPage(), dates: buildDatesPage() };
        n.content = el("div", {}, [n.pages.main, n.pages.decks, n.pages.dates]);
        n.body = el("main", { class: "gritmap-o-body" }, [n.content]);
        n.body.addEventListener("scroll", updateScrollState);
        var cancel = el("button", { type: "button", class: "gritmap-o-btn", onclick: requestCancel, text: S.t.opt_cancel });
        var ok = el("button", { type: "button", class: "gritmap-o-btn gritmap-o-primary", onclick: accept, text: S.t.opt_save });
        n.foot = el("footer", { class: "gritmap-o-foot" }, [cancel, ok]);
        n.live = el("div", { class: "gritmap-o-live", "aria-live": "polite" });
        n.confirm = buildConfirm();
        n.shell = el("div", { class: "gritmap-o-shell" }, [n.head, n.body, n.foot]);
        app.appendChild(n.shell);
        app.appendChild(n.live);
        app.appendChild(n.confirm);

        updateSize();
        updateMeasure();
        updateGoal();
        updatePause();
        updateStreak();
        updateSummaries();
        fitSegmented();

        window.addEventListener("keydown", onEscape, true);
        document.addEventListener("pointerdown", onOutsideClick, true);
        window.addEventListener("resize", function () {
            placeCalendar();
            fitSegmented();
            updateScrollState();
        });

        S.ready = true;
        refreshTexts();
        if (payload.start === "exclude") {
            openPage("decks", n.decksRow.node);
        } else if (payload.start === "keydates") {
            openPage("dates", n.datesRow.node);
        } else {
            var chosen = n.chips.querySelector("input:checked");
            if (chosen) {
                chosen.focus({ preventScroll: true });
            }
        }
        sendRaw("ready", naturalHeight());
        updateScrollState();
    }

    function setDecks(data) {
        S.decks = data.decks || [];
        S.hidden = data.hidden || [];
        // Regla de FIX-016: solo cuentan los mazos que existen.
        var existing = {};
        (data.existing || []).forEach(function (id) {
            existing[id] = true;
        });
        Object.keys(S.own).forEach(function (id) {
            if (!existing[id]) {
                delete S.own[id];
            }
        });
        var hidden = {};
        S.hidden.forEach(function (id) {
            hidden[id] = true;
        });
        Object.keys(S.own).forEach(function (id) {
            if (hidden[id]) {
                delete S.own[id];
            }
        });
        if (S.page === "decks") {
            renderDecks();
        }
        refreshTexts();
    }

    /* Regla de FIX-018: al pasar de dia a noche con la ventana abierta, las
     * muestras toman el tono del modo nuevo. */
    function setSwatches(colors) {
        document.querySelectorAll("#gritmap-o-app [data-gritmap-theme]").forEach(function (node) {
            var color = colors[node.getAttribute("data-gritmap-theme")];
            if (color) {
                node.style.background = color;
            }
        });
    }

    return {
        init: init,
        setDecks: setDecks,
        setSwatches: setSwatches,
        requestCancel: requestCancel,
    };
})();
