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
    
const boton = document.getElementById("modo");

if(localStorage.getItem("tema") === "dark"){
    document.body.classList.add("dark");
}

boton.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){
        localStorage.setItem("tema","dark");
    }else{
        localStorage.setItem("tema","light");
    }

});