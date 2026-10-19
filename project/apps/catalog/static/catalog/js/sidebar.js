/* Sidebar del home (la columna lateral del grid) y arreglo de CoreUI.

   El menu lateral que abre el boton de hamburguesa lo maneja sidemenu.js,
   que se carga en la plantilla base. Este archivo solo se carga en el
   home, donde el sidebar forma parte del grid. */

function iniciarSidebar() {
    const sidebarElement = document.querySelector('.sidebar');
    if (!sidebarElement) return;
    const ccontainer = document.querySelector('.container-2')
        ? document.querySelector('.container-2').parentElement
        : null;

    /* Ancho en el que el sidebar se ve. El mismo corte que layout.css. */
    const ANCHO_SIDEBAR = 1200;

    /* PROBLEMA QUE ARREGLA ESTO:
       CoreUI trata el sidebar como un cajon superpuesto cuando la pantalla
       es angosta y, al estar "abierto", registra un listener de "clic
       fuera" en el document. Ese listener hace preventDefault() y
       stopPropagation() en CUALQUIER clic de la pagina, asi que ningun
       boton respondia en el celular: publicar, editar, eliminar,
       like, dislike... todos dead.

       El sidebar de este proyecto lo dibuja el CSS con la clase
       .sidebar-open, asi que en el celular no hace falta el de CoreUI:
       lo unico que hay que hacer es quitarle ese listener. */
    function quitarListenerClicFuera() {
        if (window.innerWidth > ANCHO_SIDEBAR) return;
        if (typeof coreui === 'undefined') return;
        const inst = coreui.Sidebar.getInstance(sidebarElement);
        if (inst && typeof inst._removeClickOutListener === 'function') {
            inst._removeClickOutListener();
        }
    }

    /* En pantallas anchas se crea la instancia de CoreUI, que ahi si hace
       falta para el comportamiento normal del sidebar. */
    function crearSidebarSiHaceFalta() {
        if (window.innerWidth > ANCHO_SIDEBAR && typeof coreui !== 'undefined') {
            coreui.Sidebar.getOrCreateInstance(sidebarElement);
        }
    }

    crearSidebarSiHaceFalta();
    quitarListenerClicFuera();

    /* CoreUI puede crear la instancia un poco despues (en el load o con
       un resize), asi que se revisa otra vez al rato y en cada cambio de
       tamano de pantalla. */
    window.addEventListener('load', function () {
        crearSidebarSiHaceFalta();
        quitarListenerClicFuera();
    });
    setTimeout(quitarListenerClicFuera, 300);
    setTimeout(quitarListenerClicFuera, 1200);

    window.addEventListener('resize', function () {
        crearSidebarSiHaceFalta();
        quitarListenerClicFuera();
    });

    /* El boton que va DENTRO del sidebar (esquina inferior) sigue
       encogiendo la columna en pantallas anchas. El del navbar lo lleva
       sidemenu.js. */
    const botonInterno = document.getElementById('sidebar-btn');
    if (botonInterno && ccontainer) {
        botonInterno.addEventListener('click', function () {
            ccontainer.classList.toggle('sidebar-closed');
            sidebarElement.classList.toggle('sidebar-narrow');
        });
    }
}

/* Igual que en sidemenu.js: si el DOM ya esta listo se arranca ya, para
   que la hoja llegue tarde (cache) y no se quede sin listener. */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciarSidebar);
} else {
    iniciarSidebar();
}