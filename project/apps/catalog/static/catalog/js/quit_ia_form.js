function erase_pop_up_menu(menuId) {
    console.log("Erasing pop-up menu with ID:", menuId);
    const popUp = document.getElementById(menuId);
    const body = document.body;
    const toggleBtn = document.getElementById("botton-settings");
    if (popUp) {
        console.log("Found pop-up menu:", popUp);
        popUp.classList.remove("hidden");
    }

    body.addEventListener("click", function(event) {
        if (!popUp.contains(event.target) &&  !toggleBtn.contains(event.target)) {
            console.log("Click outside pop-up menu. Hiding it.");
            popUp.classList.add("hidden");
        }})
}