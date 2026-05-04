const button = document.querySelectorAll(".button-menu")

button.forEach(e => {
    console.log("a")
    const button = e.children[0];
    const button_button = button.querySelector("button") 
    const menu = e.children[1];
    button_button.addEventListener("click", function(){
        menu.classList.toggle("menu-close");
        menu.classList.toggle('menu-open');
        
    });

    menu.addEventListener("mouseout", function(){
        menu.classList.toggle("menu-close");
        menu.classList.toggle('menu-open');
        
    });
});
    
