/* Historial de correcciones de este archivo:
 * FIX-008 (2026-10-08) — Los ids, atributos y ordenes usaban el prefijo "shm",
 *                        que no es el nombre del paquete.
 * FIX-009 (2026-10-08) — Si el codigo se cargaba dos veces en la misma pagina,
 *                        cada clic enviaba la orden dos veces.
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

    var state = {
        prefix: "gritmap_",
        locale: undefined,
        texts: {},
    };

    function root() {
        return document.getElementById(ROOT_ID);
    }

    function tip() {
        return document.getElementById(TIP_ID);
    }

    /* Un idioma que Intl no conozca no debe tumbar el mapa: se prueba una vez
     * y, si falla, se deja que el navegador use su idioma por defecto. */
    function formatter(options) {
        try {
            return new Intl.DateTimeFormat(state.locale, options);
        } catch (err) {
            try {
                return new Intl.DateTimeFormat(undefined, options);
            } catch (err2) {
                return null;
            }
        }
    }

    /* Cifras con el formato del idioma de Anki: en espanol, 1240 y 12.240. */
    function numberFormatter() {
        try {
            return new Intl.NumberFormat(state.locale);
        } catch (err) {
            try {
                return new Intl.NumberFormat(undefined);
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
     * separadores; aqui se reescribe con el formato del idioma. */
    function localizeNumbers(container) {
        var spans = container.querySelectorAll(".gritmap-n[data-n]");
        if (!spans.length) {
            return;
        }
        var fmt = numberFormatter();
        if (!fmt) {
            return;
        }
        for (var i = 0; i < spans.length; i++) {
            var value = parseInt(spans[i].getAttribute("data-n"), 10);
            if (!isNaN(value)) {
                spans[i].textContent = fmt.format(value);
            }
        }
    }

    function fill(template, values) {
        return String(template || "").replace(/\{(\w+)\}/g, function (match, name) {
            return name in values ? String(values[name]) : "";
        });
    }

    function formatDate(iso) {
        var parts = String(iso).split("-");
        if (parts.length !== 3) {
            return iso;
        }
        var date = new Date(+parts[0], +parts[1] - 1, +parts[2]);
        var fmt = formatter({
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
        });
        return fmt ? fmt.format(date) : iso;
    }

    /* Los nombres de mes los pone el navegador, que conoce todos los idiomas
     * en los que se puede usar Anki. Python deja escrita una abreviatura de
     * reserva, que se conserva si la del navegador fuera demasiado larga para
     * el hueco disponible. */
    function localizeMonths(container) {
        var labels = container.querySelectorAll("[data-gritmap-month]");
        if (!labels.length) {
            return;
        }
        var fmt = formatter({ month: "short" });
        if (!fmt) {
            return;
        }
        for (var i = 0; i < labels.length; i++) {
            var month = parseInt(labels[i].getAttribute("data-gritmap-month"), 10);
            if (!(month >= 1 && month <= 12)) {
                continue;
            }
            var text;
            try {
                text = fmt.format(new Date(2021, month - 1, 1));
            } catch (err) {
                continue;
            }
            if (text && text.length <= MONTH_MAX_LENGTH) {
                labels[i].textContent = text;
            }
        }
    }

    /* Python ya ha decidido que plantilla toca a cada dia (data-t) segun la
     * medida elegida; aqui solo se rellenan la cifra y la fecha. */
    function tooltipText(cell) {
        var count = parseInt(cell.getAttribute("data-v"), 10) || 0;
        var template = state.texts[cell.getAttribute("data-t") || "none"];
        return fill(template, {
            count: formatNumber(count),
            date: formatDate(cell.getAttribute("data-d")),
        });
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
        var top = cellBox.top - rootBox.top - bubble.offsetHeight - 7;
        /* Se recorta por los dos lados: antes solo se controlaba el izquierdo
         * y el globo podia salirse por la derecha de la ventana. */
        var maxLeft = rootBox.width - bubble.offsetWidth;
        if (left > maxLeft) {
            left = maxLeft;
        }
        if (left < 0) {
            left = 0;
        }
        /* Para la fila de arriba no cabe encima: se pasa debajo de la celda en
         * lugar de taparle los botones de navegacion. */
        if (top < 0) {
            top = cellBox.top - rootBox.top + cellBox.height + 7;
        }
        bubble.style.left = left + "px";
        bubble.style.top = top + "px";
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

    function bind(container) {
        /* FIX-009: la marca va en el contenedor, no en una variable. */
        if (container.getAttribute(BOUND_ATTR)) {
            return;
        }
        container.setAttribute(BOUND_ATTR, "1");

        container.addEventListener("click", function (event) {
            var button = closest(event.target, "[data-gritmap-cmd]");
            if (button && !button.hasAttribute("disabled")) {
                pycmd(state.prefix + button.getAttribute("data-gritmap-cmd"));
            }
        });
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
        span.innerHTML = week.html || "";
        localizeNumbers(span);
    }

    function render(payload) {
        var container = root();
        if (!container) {
            return;
        }
        state.prefix = payload.prefix || state.prefix;
        state.locale = payload.locale || undefined;
        state.texts = payload.texts || {};

        hideTip();
        container.innerHTML = payload.html || "";
        /* Ya hay contenido real: se libera el alto reservado por el marcador
         * de posicion para no dejar un hueco sobrante debajo. */
        container.style.minHeight = "";
        localizeMonths(container);
        localizeNumbers(container);
        bind(container);
        renderWeekDiff(payload.week);
    }

    return { render: render };
})();
