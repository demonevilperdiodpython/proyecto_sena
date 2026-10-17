/* Menú lateral + tema claro/oscuro.
   Se carga al FINAL del <body> (ver plantilla.html): si estuviera en el
   <head>, el botón #modo todavía no existiría en el DOM y el listener
   nunca se conectaría. Aun así se espera al DOMContentLoaded por si acaso. */

document.addEventListener("DOMContentLoaded", function () {
    /* ---------- Menú lateral ---------- */
    document.querySelectorAll(".button-menu").forEach(function (contenedor) {
        const boton = contenedor.querySelector("button");
        const menu = contenedor.children[1];
        if (!boton || !menu) return;

        boton.addEventListener("click", function () {
            menu.classList.toggle("menu-close");
            menu.classList.toggle("menu-open");
        });
        menu.addEventListener("mouseout", function () {
            menu.classList.toggle("menu-close");
            menu.classList.toggle("menu-open");
        });
    });

    /* ---------- Tema claro / oscuro ---------- */
    // Aplica el tema guardado antes de pintar, así no hay parpadeo.
    if (localStorage.getItem("tema") === "dark") {
        document.body.classList.add("dark");
    }

    function pintarBotones() {
        const oscuro = document.body.classList.contains("dark");
        // querySelectorAll y no getElementById: hay varios botones con
        // el mismo id (navbar y settings) y solo WIN busca el primero.
        document.querySelectorAll("#modo, #modo-mobile").forEach(function (boton) {
            boton.textContent = oscuro ? "☀️" : "🌙";
            boton.setAttribute("aria-pressed", oscuro ? "true" : "false");
            boton.setAttribute("title", oscuro ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
        });
    }

    function toggleTema() {
        document.body.classList.toggle("dark");
        localStorage.setItem("tema", document.body.classList.contains("dark") ? "dark" : "light");
        pintarBotones();
    }

    // Se conecta a TODOS los que existan, no solo al primero.
    document.querySelectorAll("#modo, #modo-mobile").forEach(function (boton) {
        boton.addEventListener("click", toggleTema);
    });

    pintarBotones();
});