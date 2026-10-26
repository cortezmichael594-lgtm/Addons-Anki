/* Historial de correcciones de este archivo:
 * FIX-008 (2026-10-08) — Los ids, atributos y ordenes usaban el prefijo "shm",
 *                        que no es el nombre del paquete.
 * FIX-009 (2026-10-08) — Si el codigo se cargaba dos veces en la misma pagina,
 *                        cada clic enviaba la orden dos veces.
 * FIX-019 (2026-10-13) — En espanol, las cifras de cuatro digitos salian sin
 *                        punto de millar («1240 repasos»).
 * FIX-020 (2026-10-13) — Al cambiar de ano con el teclado se perdia el foco y
 *                        habia que volver a tabular hasta el mapa.
 * FIX-021 (2026-10-13) — En persa y tailandes los meses y el ano salian de
 *                        otro calendario, distinto del de la rejilla.
 */

/* GritMap - comportamiento del mapa de calor dentro de la pagina de Anki.
 *
 * Se carga una sola vez con la pagina. Python se limita a llamar a
 * GritMap.render(datos) cuando el mapa esta listo, asi que en cada dibujado no
 * se vuelve a enviar codigo ni se vuelven a crear detectores de eventos: esa
 * era la causa de los parpadeos al cambiar de ano o de opciones.
 *
 * Los detectores estan puestos sobre el contenedor y funcionan por delegacion,
 * de modo que siguen valiendo aunque el contenido interior se sustituya entero.
 */

/* --- FIX-009 (2026-10-08) ---
 * Sintoma: si Anki u otro complemento volvia a cargar este archivo en la misma
 *          pagina, se creaba un segundo GritMap y cada clic en un dia o en un
 *          boton se enviaba dos veces.
 * Causa: la variable global se sobrescribia sin comprobar si ya existia, y la
 *        marca de "detectores puestos" vivia en el objeto nuevo, no en la
 *        pagina.
 * Regla: el codigo inyectado es idempotente: reutiliza el GritMap que ya
 *        exista y marca en el propio contenedor que sus detectores estan puestos.
 */
var GritMap = (typeof GritMap !== "undefined" && GritMap) || (function () {
    "use strict";

    /* --- FIX-008 (2026-10-08) ---
     * Sintoma: los ids, atributos data- y ordenes pycmd empezaban por "shm" y
     *          podian chocar con los de otro complemento en la misma pagina.
     * Causa: el prefijo venia de un nombre antiguo, no del nombre del paquete.
     * Regla: todo lo que este codigo busca o crea en la pagina empieza por
     *        "gritmap".
     */
    var ROOT_ID = "gritmap-root";
    var TIP_ID = "gritmap-tip";
    var BOUND_ATTR = "data-gritmap-bound";
    var MONTH_MAX_LENGTH = 6;
    var DAY_MS = 86400000;

    var state = {
        prefix: "gritmap_",
        locale: undefined,
        texts: {},
        lastHtml: null,
        /* Dia que debe recibir el foco cuando llegue el ano pedido con el
         * teclado (4.7.0). */
        pendingFocus: null,
        hideTimer: null,
    };
    var LIVE_ID = "gritmap-live";

    function root() {
        return document.getElementById(ROOT_ID);
    }

    function tip() {
        return document.getElementById(TIP_ID);
    }

    /* --- FIX-021 (2026-10-13) ---
     * Sintoma: en persa los meses de la rejilla salian del calendario persa
     *          (y unos pocos del gregoriano), y en tailandes el globo decia
     *          2569 mientras el mapa decia 2026.
     * Causa: Intl usa el calendario propio de cada idioma, y la rejilla se
     *        dibuja con el gregoriano.
     * Regla: toda fecha que se escribe en el mapa pide el calendario
     *        gregoriano, el mismo de la rejilla y de Anki.
     */
    function formatter(options) {
        var opts = Object.assign({ calendar: "gregory" }, options);
        /* Un idioma que Intl no conozca no debe tumbar el mapa: se prueba una
         * vez y, si falla, se deja que el navegador use su idioma por defecto. */
        try {
            return new Intl.DateTimeFormat(state.locale, opts);
        } catch (err) {
            try {
                return new Intl.DateTimeFormat(undefined, opts);
            } catch (err2) {
                return null;
            }
        }
    }

    /* --- FIX-019 (2026-10-13) ---
     * Sintoma: en espanol salia «1240 repasos» pero «12.240 repasos».
     * Causa: la costumbre que trae el navegador para el espanol no separa los
     *        millares con cuatro cifras.
     * Regla: en espanol, toda cifra lleva punto de millar desde 1.000
     *        (useGrouping "always"); los demas idiomas siguen su costumbre.
     */
    function numberOptions(extra) {
        var opts = Object.assign({}, extra);
        if (/^es(\b|[-_])/i.test(state.locale || "")) {
            opts.useGrouping = "always";
        }
        return opts;
    }

    function numberFormatter(extra) {
        try {
            return new Intl.NumberFormat(state.locale, numberOptions(extra));
        } catch (err) {
            try {
                return new Intl.NumberFormat(undefined, extra);
            } catch (err2) {
                return null;
            }
        }
    }

    function formatNumber(value) {
        var fmt = numberFormatter();
        return fmt ? fmt.format(value) : String(value);
    }

    /* Python deja cada cifra en un <span class="gritmap-n" data-n="...">, sin
     * separadores, y cada porcentaje en un <span class="gritmap-pct"
     * data-p="...">; aqui se reescriben con el formato del idioma. */
    function localizeNumbers(container) {
        var fmt = numberFormatter();
        var spans = container.querySelectorAll(".gritmap-n[data-n]");
        for (var i = 0; fmt && i < spans.length; i++) {
            var value = parseInt(spans[i].getAttribute("data-n"), 10);
            if (!isNaN(value)) {
                spans[i].textContent = fmt.format(value);
            }
        }
        var pctFmt = numberFormatter({ style: "percent", maximumFractionDigits: 0 });
        var pcts = container.querySelectorAll(".gritmap-pct[data-p]");
        for (var j = 0; pctFmt && j < pcts.length; j++) {
            var pct = parseInt(pcts[j].getAttribute("data-p"), 10);
            if (!isNaN(pct)) {
                /* El signo % va como unidad (mas pequeno), igual que «repasos». */
                pcts[j].innerHTML = "";
                pctFmt.formatToParts(pct / 100).forEach(function (part) {
                    var piece = document.createElement("span");
                    if (part.type === "percentSign") {
                        piece.className = "gritmap-unit";
                    }
                    piece.textContent = part.value;
                    pcts[j].appendChild(piece);
                });
            }
        }
    }

    function fill(template, values) {
        return String(template || "").replace(/\{(\w+)\}/g, function (match, name) {
            return name in values ? String(values[name]) : "";
        });
    }

    function parseDay(iso) {
        var parts = String(iso).split("-");
        if (parts.length !== 3) {
            return null;
        }
        return new Date(+parts[0], +parts[1] - 1, +parts[2]);
    }

    function isoDay(day) {
        var month = String(day.getMonth() + 1);
        var date = String(day.getDate());
        return day.getFullYear() + "-" + (month.length < 2 ? "0" : "") + month + "-"
            + (date.length < 2 ? "0" : "") + date;
    }

    function formatDate(iso) {
        var day = parseDay(iso);
        if (!day) {
            return iso;
        }
        var fmt = formatter({
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
        });
        return fmt ? fmt.format(day) : iso;
    }

    /* Los nombres de mes los pone el navegador,
     * que conoce todos los idiomas en los que se puede usar Anki. Los meses
     * se cambian todos o ninguno: si alguno no cabe en su hueco, se queda la
     * fila entera de reserva que deja Python, para no mezclar estilos. */
    function localizeCalendar(container) {
        var months = container.querySelectorAll("[data-gritmap-month]");
        var monthFmt = months.length ? formatter({ month: "short" }) : null;
        if (monthFmt) {
            var names = [];
            try {
                for (var m = 0; m < 12; m++) {
                    names.push(monthFmt.format(new Date(2021, m, 1)));
                }
            } catch (err) {
                names = [];
            }
            var fits = names.length === 12 && names.every(function (name) {
                return name && name.length <= MONTH_MAX_LENGTH;
            });
            for (var i = 0; fits && i < months.length; i++) {
                var month = parseInt(months[i].getAttribute("data-gritmap-month"), 10);
                if (month >= 1 && month <= 12) {
                    months[i].textContent = names[month - 1];
                }
            }
        }
        /* 4.7.0: iniciales de lunes, miercoles y viernes (el 1 de enero de
         * 2024 fue lunes) y las fechas cortas («5 nov.»). */
        var initials = container.querySelectorAll("[data-gritmap-dayname]");
        var narrowFmt = initials.length ? formatter({ weekday: "narrow" }) : null;
        for (var w = 0; narrowFmt && w < initials.length; w++) {
            var row = parseInt(initials[w].getAttribute("data-gritmap-dayname"), 10);
            initials[w].textContent = narrowFmt.format(new Date(2024, 0, 1 + row));
        }
        var dates = container.querySelectorAll("[data-gritmap-date]");
        var shortFmt = dates.length ? formatter({ day: "numeric", month: "short" }) : null;
        for (var d = 0; shortFmt && d < dates.length; d++) {
            var shortDay = parseDay(dates[d].getAttribute("data-gritmap-date"));
            if (shortDay) {
                dates[d].textContent = shortFmt.format(shortDay);
            }
        }
    }

    /* Si el ano no cabe, el borde por donde sigue el mapa se desvanece
     * (4.8.0); al llegar al final de ese lado, el degradado se va. */
    function updateEdgeFade(container) {
        var grid = container.querySelector(".gritmap-grid");
        if (!grid) {
            return;
        }
        var hidden = grid.scrollWidth - grid.clientWidth;
        grid.classList.toggle("gritmap-more-left", hidden > 1 && grid.scrollLeft > 1);
        grid.classList.toggle("gritmap-more-right", hidden > 1 && grid.scrollLeft < hidden - 1);
    }

    /* Al cambiar de ano, el lector de pantalla dice la cifra (4.8.0). La
     * zona que lo anuncia vive fuera del mapa, porque el contenido del mapa
     * se sustituye entero y una zona recien creada no se anuncia. */
    function announce(text) {
        var live = document.getElementById(LIVE_ID);
        if (!live) {
            live = document.createElement("div");
            live.id = LIVE_ID;
            live.className = "gritmap-live";
            live.setAttribute("aria-live", "polite");
            document.body.appendChild(live);
        }
        live.textContent = text;
    }

    /* Globo de un dia: la fecha y, en la linea de abajo, lo hecho («lunes,
     * 22 de junio de 2026» / «9 tarjetas»), igual en todos los idiomas.
     * Python ya ha decidido que plantilla toca (data-t) segun la medida y la
     * forma de plural; aqui solo se rellena la cifra. */
    function tooltipText(cell) {
        var count = parseInt(cell.getAttribute("data-v"), 10) || 0;
        var template = state.texts[cell.getAttribute("data-t") || "none"];
        /* La fecha, en gris y mas pequena; lo hecho, debajo y destacado. */
        var text = '<span class="gritmap-tip-date">' + formatDate(cell.getAttribute("data-d"))
            + "</span><br>" + fill(template, { count: formatNumber(count) });
        /* Los dias que abren Explorar lo dicen en una ultima linea gris: el
         * puntero en forma de mano no se ve con el teclado (3.6.0). */
        var cmd = cell.getAttribute("data-gritmap-cmd") || "";
        var hint = state.texts[cmd.indexOf("future:") === 0 ? "click_future" : "click_past"];
        /* 4.0.0: si el dia esta perdonado (comodin o pausa). */
        var forgiven = cell.getAttribute("data-gritmap-forgiven");
        if (forgiven && state.texts["forgiven_" + forgiven]) {
            text += '<br><span class="gritmap-tip-hint">' + state.texts["forgiven_" + forgiven] + "</span>";
        }
        if (cmd && hint) {
            text += '<br><span class="gritmap-tip-hint">' + hint + "</span>";
        }
        return text;
    }

    function showTip(cell) {
        var container = root();
        var bubble = tip();
        if (!container || !bubble) {
            return;
        }
        var info = cell.getAttribute("data-gritmap-info");
        if (info) {
            /* Globo de una cifra de las estadisticas: el texto viene hecho. */
            bubble.innerHTML = info;
        } else {
            /* La cabecera de una fecha clave viene ya escapada desde Python
             * (nombres y cuenta atras). */
            var keyLabel = cell.getAttribute("data-gritmap-key");
            var head = keyLabel ? "<b>" + keyLabel + "</b><br>" : "";
            bubble.innerHTML = head + tooltipText(cell);
        }
        localizeNumbers(bubble);
        bubble.style.display = "block";

        var cellBox = cell.getBoundingClientRect();
        var rootBox = container.getBoundingClientRect();
        var left = cellBox.left - rootBox.left + cellBox.width / 2 - bubble.offsetWidth / 2;
        var top = cellBox.top - rootBox.top - bubble.offsetHeight - 8;
        /* Se recorta por los dos lados para que no se salga de la ventana. */
        var maxLeft = rootBox.width - bubble.offsetWidth;
        if (left > maxLeft) {
            left = maxLeft;
        }
        if (left < 0) {
            left = 0;
        }
        /* Para la fila de arriba no cabe encima: se pasa debajo de la celda en
         * lugar de taparle los botones de la cabecera. */
        if (top < 0) {
            top = cellBox.top - rootBox.top + cellBox.height + 8;
        }
        bubble.style.left = left + "px";
        bubble.style.top = top + "px";
        return bubble.textContent;
    }

    function hideTip() {
        cancelHide();
        var bubble = tip();
        if (bubble) {
            bubble.style.display = "none";
        }
    }

    /* El globo se puede recorrer con el raton sin que se cierre (WCAG 1.4.13,
     * 4.7.0): al salir del dia se espera un instante, por si el raton va
     * hacia el globo. */
    function hideTipSoon() {
        cancelHide();
        state.hideTimer = setTimeout(hideTip, 200);
    }

    function cancelHide() {
        if (state.hideTimer) {
            clearTimeout(state.hideTimer);
            state.hideTimer = null;
        }
    }

    function closest(target, selector) {
        return target instanceof Element ? target.closest(selector) : null;
    }

    function send(element) {
        if (element && element.getAttribute("aria-disabled") !== "true" && element.getAttribute("data-gritmap-cmd")) {
            pycmd(state.prefix + element.getAttribute("data-gritmap-cmd"));
        }
    }

    /* Teclado en la rejilla: un solo dia recibe el tabulador y las flechas
     * mueven el foco por dias (arriba y abajo) y por semanas (a los lados). */
    function focusCell(container, cell) {
        var previous = container.querySelectorAll(".gritmap-cell[tabindex='0']");
        for (var i = 0; i < previous.length; i++) {
            if (previous[i] !== cell) {
                previous[i].setAttribute("tabindex", "-1");
            }
        }
        cell.setAttribute("tabindex", "0");
        cell.setAttribute("role", cell.hasAttribute("data-gritmap-cmd") ? "button" : "img");
        cell.setAttribute("aria-label", plainTip(cell));
        cell.focus({ preventScroll: false });
    }

    function plainTip(cell) {
        var box = document.createElement("div");
        var keyLabel = cell.getAttribute("data-gritmap-key");
        box.innerHTML = (keyLabel ? keyLabel + ". " : "") + tooltipText(cell).replace(/<br>/g, ". ");
        return box.textContent || "";
    }

    var KEY_STEPS = { ArrowUp: -1, ArrowDown: 1, ArrowLeft: -7, ArrowRight: 7 };

    function addMonths(day, months) {
        var target = new Date(day.getFullYear(), day.getMonth() + months, 1);
        var last = new Date(target.getFullYear(), target.getMonth() + 1, 0).getDate();
        target.setDate(Math.min(day.getDate(), last));
        return target;
    }

    /* Dia al que lleva cada tecla (4.7.0, como el selector de fechas de las
     * practicas de WAI-ARIA): flechas, dias y semanas; Inicio y Fin, lunes y
     * domingo de la semana; RePag y AvPag, el mismo dia del mes anterior o
     * siguiente; con Mayus, del ano anterior o siguiente. */
    function keyTarget(event, day) {
        var step = KEY_STEPS[event.key];
        if (step) {
            return new Date(day.getTime() + step * DAY_MS + DAY_MS / 2);
        }
        var weekday = (day.getDay() + 6) % 7;
        if (event.key === "Home") {
            return new Date(day.getFullYear(), day.getMonth(), day.getDate() - weekday);
        }
        if (event.key === "End") {
            return new Date(day.getFullYear(), day.getMonth(), day.getDate() + 6 - weekday);
        }
        if (event.key === "PageUp" || event.key === "PageDown") {
            var sign = event.key === "PageUp" ? -1 : 1;
            return addMonths(day, sign * (event.shiftKey ? 12 : 1));
        }
        return null;
    }

    /* Un dia de otro ano: se pide ese ano con su flecha y el foco espera a
     * que llegue. Si no hay ano al que ir, no pasa nada. */
    function moveToOtherYear(container, target, shownYear) {
        var cmd = target.getFullYear() < shownYear ? "prev" : "next";
        var button = container.querySelector("button[data-gritmap-btn='" + cmd + "']");
        if (button && button.getAttribute("aria-disabled") !== "true") {
            state.pendingFocus = isoDay(target);
            send(button);
        }
    }

    function onKeyDown(event) {
        var cell = closest(event.target, ".gritmap-cell");
        var container = root();
        if (!cell || !container) {
            return;
        }
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            send(cell);
            return;
        }
        var day = parseDay(cell.getAttribute("data-d"));
        var targetDay = day ? keyTarget(event, day) : null;
        if (!targetDay) {
            return;
        }
        event.preventDefault();
        var target = container.querySelector(".gritmap-cell[data-d='" + isoDay(targetDay) + "']");
        if (target) {
            focusCell(container, target);
        } else if (targetDay.getFullYear() !== day.getFullYear()) {
            moveToOtherYear(container, targetDay, day.getFullYear());
        }
    }

    function bind(container) {
        /* FIX-009: la marca va en el contenedor, no en una variable. */
        if (container.getAttribute(BOUND_ATTR)) {
            return;
        }
        container.setAttribute(BOUND_ATTR, "1");

        container.addEventListener("click", function (event) {
            send(closest(event.target, "[data-gritmap-cmd]"));
        });
        container.addEventListener("keydown", onKeyDown);
        container.addEventListener("mouseover", function (event) {
            if (closest(event.target, "#" + TIP_ID)) {
                /* El raton ha llegado al globo: se queda abierto. */
                cancelHide();
                return;
            }
            var cell = closest(event.target, "[data-gritmap-tip]");
            if (cell) {
                cancelHide();
                showTip(cell);
            }
        });
        container.addEventListener("mouseout", function (event) {
            /* Pasar de una parte a otra de la misma cifra (etiqueta y valor)
             * no cierra el globo: asi no parpadea. Al salir del globo o del
             * dia, se cierra tras un instante. */
            var from = closest(event.target, "[data-gritmap-tip], #" + TIP_ID);
            var to = closest(event.relatedTarget, "[data-gritmap-tip], #" + TIP_ID);
            if (from && from !== to) {
                hideTipSoon();
            }
        });
        container.addEventListener("focusin", function (event) {
            var cell = closest(event.target, "[data-gritmap-tip]");
            if (cell) {
                if (cell.classList.contains("gritmap-cell") && !cell.hasAttribute("aria-label")) {
                    cell.setAttribute("role", cell.hasAttribute("data-gritmap-cmd") ? "button" : "img");
                    cell.setAttribute("aria-label", plainTip(cell));
                }
                showTip(cell);
            }
        });
        container.addEventListener("focusout", hideTip);
        /* La tecla Esc cierra el globo (WCAG 1.4.13: lo que aparece al pasar
         * el raton o al enfocar se puede descartar). */
        container.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                hideTip();
            }
        });
        container.addEventListener("mouseleave", hideTip);
        /* Si el mapa se desplaza lateralmente, el globo dejaria de apuntar a
         * su celda: se oculta en cuanto empieza el desplazamiento. */
        container.addEventListener("scroll", function (event) {
            hideTip();
            if (closest(event.target, ".gritmap-grid")) {
                updateEdgeFade(container);
            }
        }, true);
        window.addEventListener("resize", function () {
            var current = root();
            if (current) {
                updateEdgeFade(current);
            }
        });
    }

    /* Desde 4.0.0 la comparativa semanal vive en la tarjeta de estadisticas:
     * se quita la frase que versiones anteriores dejaban junto al texto de
     * Anki, por si la pagina aun la tiene. */
    function removeOldWeekDiff() {
        var span = document.getElementById("gritmap-wd");
        if (span && span.parentNode) {
            span.parentNode.removeChild(span);
        }
    }

    /* Centra un dia en la rejilla si no cabe entera a lo ancho. */
    function centreCell(grid, cell) {
        if (grid.scrollWidth <= grid.clientWidth) {
            return;
        }
        var cellBox = cell.getBoundingClientRect();
        var gridBox = grid.getBoundingClientRect();
        var centre = cellBox.left - gridBox.left + grid.scrollLeft - grid.clientWidth / 2;
        grid.scrollLeft = Math.max(0, centre);
    }

    /* Al abrir un ano se ensena la semana de hoy aunque la ventana sea
     * estrecha; en un ano pasado, su final, y en uno futuro, su principio. */
    function scrollToToday(container) {
        var grid = container.querySelector(".gritmap-grid");
        if (!grid || grid.scrollWidth <= grid.clientWidth) {
            return;
        }
        var today = grid.querySelector("[data-gritmap-today]");
        if (today) {
            centreCell(grid, today);
            return;
        }
        var shown = parseInt((container.querySelector(".gritmap-yv") || {}).textContent, 10);
        grid.scrollLeft = shown < new Date().getFullYear() ? grid.scrollWidth : 0;
    }

    function render(payload) {
        var container = root();
        if (!container) {
            return;
        }
        state.prefix = payload.prefix || state.prefix;
        state.locale = payload.locale || undefined;
        state.texts = payload.texts || {};
        var html = payload.html || "";

        /* Los mismos datos que ya se ven (por ejemplo, al terminar el calculo
         * tras volver a esta pantalla) no se vuelven a pintar: asi no se
         * pierden el desplazamiento ni el foco. */
        if (html === state.lastHtml && container.querySelector(".gritmap-card")) {
            return;
        }

        /* --- FIX-020 (2026-10-13) ---
         * Sintoma: al pulsar Retroceder, Avanzar u Hoy con el teclado, el foco
         *          saltaba al principio de la pagina, y cada redibujado
         *          devolvia el mapa a enero.
         * Causa: el contenido se sustituye entero y el boton que tenia el foco
         *        desaparecia con el; el desplazamiento tambien se perdia.
         * Regla: antes de sustituir el contenido se anotan el boton o el dia
         *        con el foco, el ano y el desplazamiento, y despues se
         *        devuelven si siguen teniendo sentido.
         */
        var active = document.activeElement;
        var hadFocus = active && active !== container && container.contains(active);
        var focusBtn = hadFocus ? active.getAttribute("data-gritmap-btn") : null;
        var focusDay = hadFocus && active.classList.contains("gritmap-cell")
            ? active.getAttribute("data-d") : null;
        if (state.pendingFocus) {
            focusDay = state.pendingFocus;
            focusBtn = null;
            state.pendingFocus = null;
        }
        var oldGrid = container.querySelector(".gritmap-grid");
        var oldYear = (container.querySelector(".gritmap-yv") || {}).textContent;
        var oldScroll = oldGrid ? oldGrid.scrollLeft : 0;

        hideTip();
        container.innerHTML = html;
        container.removeAttribute("aria-busy");
        state.lastHtml = html;
        localizeCalendar(container);
        localizeNumbers(container);
        bind(container);
        removeOldWeekDiff();

        var newGrid = container.querySelector(".gritmap-grid");
        var newYear = (container.querySelector(".gritmap-yv") || {}).textContent;
        if (newGrid && oldGrid && newYear === oldYear) {
            newGrid.scrollLeft = oldScroll;
        } else if (newGrid) {
            scrollToToday(container);
        }
        updateEdgeFade(container);
        if (oldYear && newYear && newYear !== oldYear) {
            announce(newYear);
        }

        if (focusBtn) {
            var button = container.querySelector("button[data-gritmap-btn='" + focusBtn + "']");
            if (!button || button.getAttribute("aria-disabled") === "true") {
                button = container.querySelector("button[data-gritmap-btn='opts']");
            }
            if (button) {
                button.focus({ preventScroll: true });
            }
        } else if (focusDay) {
            var cell = container.querySelector(".gritmap-cell[data-d='" + focusDay + "']");
            if (cell) {
                focusCell(container, cell);
            }
        }
    }

    return { render: render };
})();
