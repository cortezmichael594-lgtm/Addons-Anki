// Historial de correcciones de este archivo:
// FIX-009 (2026-10-28): el panel no se mostraba nunca y siempre se abría la ventana sencilla.

// Atelier - panel de configuración a medida (versión 3.7.0).
//
// Dibuja la lista de paletas y gestiona la elección con el patrón de grupo de
// botones de opción del W3C: el tabulador entra en la elegida; las flechas mueven y
// eligen a la vez, y de la última pasan a la primera; la barra espaciadora o un clic
// eligen. Un clic aplica al momento («pick»); las flechas, cuando la elección lleva
// 200 ms quieta («move», lo decide Python). Ctrl+Intro acepta y Esc cancela.
//
// Todo lleva el prefijo «nocturne» (nombre del paquete).

(function () {
    "use strict";

    var SVG = "http://www.w3.org/2000/svg";
    var state = { data: null, rows: [], current: null };

    function send(action, arg) {
        pycmd("nocturne:" + action + (arg === undefined ? "" : ":" + arg));
    }

    function el(tag, className, text) {
        var node = document.createElement(tag);
        if (className) {
            node.className = className;
        }
        if (text !== undefined) {
            node.textContent = text;
        }
        return node;
    }

    function icon(className, paths) {
        var svg = document.createElementNS(SVG, "svg");
        svg.setAttribute("viewBox", "0 0 16 16");
        svg.setAttribute("aria-hidden", "true");
        svg.setAttribute("class", className);
        paths.forEach(function (d) {
            var path = document.createElementNS(SVG, "path");
            path.setAttribute("d", d);
            svg.appendChild(path);
        });
        return svg;
    }

    function thumb(colors, radius) {
        var box = el("div", "nocturne-p-thumb");
        Object.keys(colors).forEach(function (key) {
            box.style.setProperty("--t-" + key, colors[key]);
        });
        box.style.setProperty("--t-radius", radius + "px");
        var bar = el("div", "nocturne-t-bar");
        for (var i = 0; i < 3; i++) {
            bar.appendChild(el("i"));
        }
        var card = el("div", "nocturne-t-card");
        for (var j = 0; j < 2; j++) {
            var line = el("div", "nocturne-t-line");
            line.appendChild(el("b"));
            line.appendChild(el("i", "nocturne-t-new"));
            line.appendChild(el("i", "nocturne-t-learn"));
            line.appendChild(el("i", "nocturne-t-review"));
            card.appendChild(line);
        }
        box.appendChild(bar);
        box.appendChild(card);
        box.appendChild(el("div", "nocturne-t-button"));
        return box;
    }

    function row(palette, texts) {
        var node = el("div", "nocturne-p-row");
        node.setAttribute("role", "radio");
        node.dataset.id = palette.id;
        var thumbs = el("div", "nocturne-p-thumbs");
        thumbs.setAttribute("aria-hidden", "true");
        thumbs.appendChild(thumb(palette.day, palette.radius));
        thumbs.appendChild(thumb(palette.night, palette.radius));
        var text = el("div", "nocturne-p-text");
        var name = el("div", "nocturne-p-name", palette.name);
        name.id = "nocturne-p-name-" + palette.id;
        if (palette.headingFont) {
            // El nombre de Papel en su letra de títulos: es la muestra de lo que la distingue.
            name.style.fontFamily = palette.headingFont;
            name.style.fontWeight = "700";
            name.style.fontSize = "13px";
        }
        if (palette.isDefault) {
            name.appendChild(el("span", "nocturne-p-default", texts["default"]));
        }
        var desc = el("div", "nocturne-p-desc", palette.description);
        desc.id = "nocturne-p-desc-" + palette.id;
        text.appendChild(name);
        text.appendChild(desc);
        node.setAttribute("aria-labelledby", name.id);
        node.setAttribute("aria-describedby", desc.id);
        node.appendChild(thumbs);
        node.appendChild(text);
        node.appendChild(icon("nocturne-p-check", ["M3 8.5l3.2 3L13 4.5"]));
        node.addEventListener("click", function () {
            choose(palette.id, "pick");
            node.focus();
        });
        return node;
    }

    function choose(id, how) {
        if (id === state.current && how !== "pick") {
            return;
        }
        state.current = id;
        state.rows.forEach(function (node) {
            var on = node.dataset.id === id;
            node.setAttribute("aria-checked", on ? "true" : "false");
            node.tabIndex = on ? 0 : -1;
        });
        send(how, id);
    }

    function move(step) {
        var index = 0;
        state.rows.forEach(function (node, i) {
            if (node.dataset.id === state.current) {
                index = i;
            }
        });
        var next = state.rows[(index + step + state.rows.length) % state.rows.length];
        choose(next.dataset.id, "move");
        next.focus();
    }

    function banner(text, buttonText, onPress) {
        var box = el("div", "nocturne-p-banner");
        box.setAttribute("role", "status");
        box.appendChild(icon("", ["M8 2.5l6 10.5H2z", "M8 6.5v3", "M8 11.5v.01"]));
        box.appendChild(el("span", "", text));
        if (buttonText) {
            var button = el("button", "", buttonText);
            button.type = "button";
            button.addEventListener("click", onPress);
            box.appendChild(button);
        }
        return box;
    }

    function setNight(night) {
        var data = state.data;
        if (!data) {
            return;
        }
        var labels = document.querySelectorAll("#nocturne-panel .nocturne-p-modes span");
        if (labels.length === 2) {
            labels[0].classList.toggle("nocturne-p-active", !night);
            labels[1].classList.toggle("nocturne-p-active", !!night);
        }
        var note = document.querySelector("#nocturne-panel .nocturne-p-note");
        if (note) {
            note.textContent = night ? data.texts.modeNoteNight : data.texts.modeNoteDay;
        }
    }

    function updateEdges(shell, body) {
        shell.classList.toggle("nocturne-p-scrolled", body.scrollTop > 0);
        shell.classList.toggle("nocturne-p-overflow", body.scrollHeight > body.clientHeight + 1);
    }

    function init(data) {
        state.data = data;
        var texts = data.texts;
        var app = document.getElementById("nocturne-panel");
        var shell = el("div", "nocturne-p-shell");

        var head = el("header", "nocturne-p-head");
        var title = el("h1", "", texts.title);
        title.id = "nocturne-p-title";
        head.appendChild(title);

        var body = el("div", "nocturne-p-body");
        if (data.failures) {
            body.appendChild(banner(texts.failures, texts.openLog, function () {
                send("log");
            }));
        }
        if (data.steppedAside) {
            body.appendChild(banner(texts.contrast));
        } else {
            body.appendChild(el("p", "nocturne-p-intro", texts.intro));
        }
        var modes = el("div", "nocturne-p-modes");
        modes.setAttribute("aria-hidden", "true");
        modes.appendChild(el("span", "", texts.day));
        modes.appendChild(el("span", "", texts.night));
        body.appendChild(modes);

        var list = el("div", "nocturne-p-list");
        list.setAttribute("role", "radiogroup");
        list.setAttribute("aria-labelledby", title.id);
        data.palettes.forEach(function (palette) {
            var node = row(palette, texts);
            state.rows.push(node);
            list.appendChild(node);
        });
        list.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown" || event.key === "ArrowRight") {
                move(1);
                event.preventDefault();
            } else if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
                move(-1);
                event.preventDefault();
            } else if (event.key === " ") {
                var focused = document.activeElement;
                if (focused && focused.dataset && focused.dataset.id) {
                    choose(focused.dataset.id, "pick");
                }
                event.preventDefault();
            }
        });
        body.appendChild(list);
        body.appendChild(el("p", "nocturne-p-note", texts.modeNote));

        var foot = el("footer", "nocturne-p-foot");
        var cancel = el("button", "", texts.cancel);
        cancel.type = "button";
        cancel.addEventListener("click", function () {
            send("cancel");
        });
        var accept = el("button", "nocturne-p-primary", texts.accept);
        accept.type = "button";
        accept.addEventListener("click", function () {
            send("accept");
        });
        foot.appendChild(cancel);
        foot.appendChild(accept);

        shell.appendChild(head);
        shell.appendChild(body);
        shell.appendChild(foot);
        app.appendChild(shell);

        // Estado inicial, sin avisar a Python (no es una elección).
        state.current = data.current;
        state.rows.forEach(function (node) {
            var on = node.dataset.id === data.current;
            node.setAttribute("aria-checked", on ? "true" : "false");
            node.tabIndex = on ? 0 : -1;
        });
        setNight(data.night);

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                send("cancel");
                event.preventDefault();
            } else if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
                send("accept");
                event.preventDefault();
            }
        });
        body.addEventListener("scroll", function () {
            updateEdges(shell, body);
        });
        window.addEventListener("resize", function () {
            updateEdges(shell, body);
        });

        // --- FIX-009 (2026-10-28) ---
        // Síntoma: al pulsar «Configuración» no aparecía el panel: a los 3 segundos se abría
        //          siempre la ventana sencilla de emergencia y el registro decía «el panel no se
        //          dibujó en 3000 ms».
        // Causa: el aviso de «lista» esperaba al siguiente fotograma (requestAnimationFrame),
        //        pero la página está oculta hasta que avisa, y una página oculta no pinta
        //        fotogramas: cada una esperaba a la otra.
        // Regla: una página que se enseña cuando avisa de que está lista avisa sin esperar a
        //        pintar (con setTimeout), midiendo su contenido, que se calcula aunque no se vea.
        setTimeout(function () {
            // Alto del contenido del cuerpo (no el del hueco que ocupa ahora).
            var last = body.lastElementChild;
            var padding = parseFloat(getComputedStyle(body).paddingBottom) || 0;
            var content = last.getBoundingClientRect().bottom - body.getBoundingClientRect().top
                + body.scrollTop + padding;
            var wanted = head.offsetHeight + content + foot.offsetHeight;
            var selected = state.rows.filter(function (node) {
                return node.dataset.id === state.current;
            })[0];
            if (selected) {
                selected.focus();
            }
            updateEdges(shell, body);
            send("ready", Math.ceil(wanted));
        }, 0);
    }

    window.NocturnePanel = { init: init, setNight: setNight };
})();
