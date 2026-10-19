document.addEventListener('DOMContentLoaded', function () {
    const sidebarbutton = document.getElementById('sidebar-btn');
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
        const inst = coreui.Sidebar.getInstance(sidebarElement);
        if (inst && typeof inst._removeClickOutListener === 'function') {
            inst._removeClickOutListener();
        }
    }

    /* En pantallas anchas se crea la instancia de CoreUI, que ahi si hace
       falta para el comportamiento normal del sidebar. */
    function crearSidebarSiHaceFalta() {
        if (window.innerWidth > ANCHO_SIDEBAR) {
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

    if (sidebarbutton && ccontainer) {
        sidebarbutton.addEventListener('click', function () {
            ccontainer.classList.toggle('sidebar-closed');
            sidebarElement.classList.toggle('sidebar-narrow');
        });
    }
});
