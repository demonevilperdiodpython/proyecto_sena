/* Boton de hamburguesa del navbar: abre y cierra el menu lateral (.sidebar).

   El menu es el que ya traia home.html; aqui solo se le da al boton la
   forma de moverlo. El boton vive en el navbar, que es fixed, asi que
   funciona estando en cualquier parte de la pagina.

   Antes este boton no hacia nada: sidemenu.js buscaba una clase
   ".button-menu" que no existe en ninguna plantilla. */

function iniciarMenuLateral() {
    const cuerpo = document.body;
    const sidebar = document.querySelector('.sidebar');

    /* En pantallas donde el sidebar ya se ve (ancho), el boton lo
       encoge y lo vuelve a abrir. En angosto lo muestra encima. */
    const ANCHO_SIDEBAR = 1200;

    function estaAbierto() {
        return cuerpo.classList.contains('menu-abierto');
    }

    function abrirMenu(abrir) {
        cuerpo.classList.toggle('menu-abierto', abrir);
        if (sidebar) {
            sidebar.classList.toggle('sidebar-open', abrir && window.innerWidth <= ANCHO_SIDEBAR);
        }
        document.querySelectorAll('.toggle-btn').forEach(function (boton) {
            boton.setAttribute('aria-expanded', abrir ? 'true' : 'false');
        });
    }

    document.querySelectorAll('.toggle-btn').forEach(function (boton) {
        boton.addEventListener('click', function (evento) {
            // Sin esto el clic llega al document y lo cierra enseguida.
            evento.stopPropagation();
            abrirMenu(!estaAbierto());
        });
    });

    /* El velo oscuro: pulsarlo cierra. */
    document.querySelectorAll('[data-cerrar-menu]').forEach(function (capa) {
        capa.addEventListener('click', function () { abrirMenu(false); });
    });

    /* Al pulsar FUERA del menu se cierra.
       OJO: los clics DENTRO del menu no lo cierran. Si no, el boton de
       usuario del pie (que abre un desplegable) cerraba el sidebar entero
       y el desplegable se abria y desaparecia en el mismo instante. */
    document.addEventListener('click', function (evento) {
        if (sidebar && sidebar.contains(evento.target)) return;
        abrirMenu(false);
    });

    /* Escape cierra. */
    document.addEventListener('keydown', function (evento) {
        if (evento.key === 'Escape') {
            abrirMenu(false);
            // Si el desplegable de usuario esta abierto, tambien se cierra.
            document.querySelectorAll('.sidebar-footer .dropdown-menu.show')
                .forEach(function (sub) { sub.classList.remove('show'); });
        }
    });

    /* Al elegir un enlace del menu se cierra, porque va a otra pagina. */
    if (sidebar) {
        sidebar.querySelectorAll('a').forEach(function (enlace) {
            // El boton de usuario es un <a href="#"> que abre un desplegable:
            // no navega a ninguna parte, asi que no debe cerrar el menu.
            if (enlace.getAttribute('href') === '#') return;
            enlace.addEventListener('click', function () { abrirMenu(false); });
        });
    }

    /* Al pasar a pantalla ancha el menu se cierra solo: si no se queda
       tapando el contenido. */
    window.addEventListener('resize', function () {
        if (window.innerWidth > ANCHO_SIDEBAR) abrirMenu(false);
    });
}

/* ===========================================================================
   TEMA CLARO / OSCURO
   Este bloque se perdio al reescribir el archivo para el menu lateral: los
   botones #modo se quedaron sin listener y no cambiaban de color.
   =========================================================================== */
function iniciarTema() {
    /* Se aplica el tema guardado antes de pintar, asi no hay parpadeo. */
    if (localStorage.getItem("tema") === "dark") {
        document.body.classList.add("dark");
    }

    function pintarBotones() {
        const oscuro = document.body.classList.contains("dark");
        /* querySelectorAll y no getElementById: hay varios botones con el
           mismo id (el del navbar y el de ajustes) y getElementById solo
           devolveria el primero. */
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

    /* Se conecta a TODOS los que existan, no solo al primero. */
    document.querySelectorAll("#modo, #modo-mobile").forEach(function (boton) {
        boton.addEventListener("click", toggleTema);
    });

    pintarBotones();
}

/* Si el DOM ya esta listo se arranca ahora mismo. Esperar siempre a
   DOMContentLoaded hacia que, si la hoja se carga tarde (por ejemplo desde
   la cache), el boton se quedara sin listener y no hara nada. */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
        iniciarMenuLateral();
        iniciarTema();
    });
} else {
    iniciarMenuLateral();
    iniciarTema();
}