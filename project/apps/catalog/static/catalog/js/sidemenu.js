const buttons = document.querySelectorAll(".button-menu");

buttons.forEach(e => {
    const button = e.children[0];
    const button_button = button.querySelector("button");
    const menu = e.children[1];
    button_button.addEventListener("click", function() {
        menu.classList.toggle("menu-close");
        menu.classList.toggle('menu-open');
    });
    menu.addEventListener("mouseout", function() {
        menu.classList.toggle("menu-close");
        menu.classList.toggle('menu-open');
    });
});

// Aplica el tema guardado al cargar
if (localStorage.getItem("tema") === "dark") {
    document.body.classList.add("dark");
}

// Función para alternar tema
function toggleTema() {
    document.body.classList.toggle("dark");
    localStorage.setItem("tema", document.body.classList.contains("dark") ? "dark" : "light");
}

// Botón tema en navbar desktop
const boton = document.getElementById("modo");
if (boton) {
    boton.addEventListener("click", toggleTema);
}

// Botón tema en menú hamburguesa móvil
const botonMobile = document.getElementById("modo-mobile");
if (botonMobile) {
    botonMobile.addEventListener("click", toggleTema);
}
