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
    };

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
                pcts[j].textContent = pctFmt.format(pct / 100);
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
    }

    /* Globo de un dia: la fecha y, en la linea de abajo, lo hecho («lunes,
     * 22 de junio de 2026» / «9 tarjetas»), igual en todos los idiomas.
     * Python ya ha decidido que plantilla toca (data-t) segun la medida y la
     * forma de plural; aqui solo se rellena la cifra. */
    function tooltipText(cell) {
        var count = parseInt(cell.getAttribute("data-v"), 10) || 0;
        var template = state.texts[cell.getAttribute("data-t") || "none"];
        return formatDate(cell.getAttribute("data-d")) + "<br>"
            + fill(template, { count: formatNumber(count) });
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
            var head = keyLabel ? "<b>★ " + keyLabel + "</b><br>" : "";
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
        var bubble = tip();
        if (bubble) {
            bubble.style.display = "none";
        }
    }

    function closest(target, selector) {
        return target instanceof Element ? target.closest(selector) : null;
    }

    function send(element) {
        if (element && !element.hasAttribute("disabled") && element.getAttribute("data-gritmap-cmd")) {
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
        box.innerHTML = (keyLabel ? "★ " + keyLabel + ". " : "") + tooltipText(cell).replace("<br>", ". ");
        return box.textContent || "";
    }

    var KEY_STEPS = { ArrowUp: -1, ArrowDown: 1, ArrowLeft: -7, ArrowRight: 7 };

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
        var step = KEY_STEPS[event.key];
        var day = parseDay(cell.getAttribute("data-d"));
        if (!step || !day) {
            return;
        }
        event.preventDefault();
        var target = container.querySelector(
            ".gritmap-cell[data-d='" + isoDay(new Date(day.getTime() + step * DAY_MS + DAY_MS / 2)) + "']"
        );
        if (target) {
            focusCell(container, target);
        }
    }

    function bind(container) {
        /* FIX-009: la marca va en el contenedor, no en una variable. */
        if (container.getAttribute(BOUND_ATTR)) {
            return;
        }
        container.setAttribute(BOUND_ATTR, "1");

        container.addEventListener("click", function (event) {
            var target = closest(event.target, "[data-gritmap-cmd]");
            send(target);
            /* «Hoy» en el mismo ano no cambia el mapa: basta con volver a la
             * semana de hoy. Si cambia de ano, el dibujado nuevo lo hace. */
            if (target && target.getAttribute("data-gritmap-cmd") === "today") {
                scrollToToday(container);
            }
        });
        container.addEventListener("keydown", onKeyDown);
        container.addEventListener("mouseover", function (event) {
            var cell = closest(event.target, "[data-gritmap-tip]");
            if (cell) {
                showTip(cell);
            }
        });
        container.addEventListener("mouseout", function (event) {
            /* Pasar de una parte a otra de la misma cifra (etiqueta y valor)
             * no cierra el globo: asi no parpadea. */
            var from = closest(event.target, "[data-gritmap-tip]");
            if (from && from !== closest(event.relatedTarget, "[data-gritmap-tip]")) {
                hideTip();
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
        container.addEventListener("mouseleave", hideTip);
        /* Si el mapa se desplaza lateralmente, el globo dejaria de apuntar a
         * su celda: se oculta en cuanto empieza el desplazamiento. */
        container.addEventListener("scroll", hideTip, true);
    }

    /* La comparativa semanal se acopla al texto "Estudiaste ... hoy" que dibuja
     * Anki en la lista de mazos. Se reutiliza el mismo elemento en cada
     * dibujado en lugar de crear uno nuevo, para no duplicarlo. El color lo
     * pone la hoja de estilos segun la clase (sube, baja o igual). */
    function renderWeekDiff(week) {
        var studied = document.getElementById("studiedToday");
        var span = document.getElementById("gritmap-wd");
        if (!week || !studied) {
            if (span && span.parentNode) {
                span.parentNode.removeChild(span);
            }
            return;
        }
        if (!span) {
            span = document.createElement("span");
            span.id = "gritmap-wd";
            (studied.querySelector("span") || studied).appendChild(span);
        }
        span.className = "gritmap-wd-" + (week.cls || "flat");
        span.title = week.title || "";
        span.innerHTML = week.html || "";
        localizeNumbers(span);
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
            var cellBox = today.getBoundingClientRect();
            var gridBox = grid.getBoundingClientRect();
            var centre = cellBox.left - gridBox.left + grid.scrollLeft - grid.clientWidth / 2;
            grid.scrollLeft = Math.max(0, centre);
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
        if (html === state.lastHtml && container.querySelector(".gritmap-nav")) {
            renderWeekDiff(payload.week);
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
        var oldGrid = container.querySelector(".gritmap-grid");
        var oldYear = (container.querySelector(".gritmap-yv") || {}).textContent;
        var oldScroll = oldGrid ? oldGrid.scrollLeft : 0;

        hideTip();
        container.innerHTML = html;
        state.lastHtml = html;
        /* Ya hay contenido real: se libera el alto reservado por el marcador
         * de posicion para no dejar un hueco sobrante debajo. */
        container.style.minHeight = "";
        localizeCalendar(container);
        localizeNumbers(container);
        bind(container);
        renderWeekDiff(payload.week);

        var newGrid = container.querySelector(".gritmap-grid");
        var newYear = (container.querySelector(".gritmap-yv") || {}).textContent;
        if (newGrid && oldGrid && newYear === oldYear) {
            newGrid.scrollLeft = oldScroll;
        } else if (newGrid) {
            scrollToToday(container);
        }

        if (focusBtn) {
            var button = container.querySelector("button[data-gritmap-btn='" + focusBtn + "']");
            if (!button || button.disabled) {
                button = container.querySelector("button[data-gritmap-btn='today']")
                    || container.querySelector("button[data-gritmap-btn='opts']");
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
