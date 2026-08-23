function openchat(element, id) {
    const comentarios = document.querySelector(`.comentarios[data-id="${id}"]`);
    if (comentarios) {
        if (comentarios.style.display === "none" || !comentarios.style.display) {
            comentarios.style.display = "block";
        } else {
            comentarios.style.display = "none";
        }
    }
}
function respondbox(element, id){
    const comentarios = document.querySelector(`.comentary-form[data-id="${id}"]`);
    if (comentarios) {
        if (comentarios.style.display === "none" || !comentarios.style.display) {
            comentarios.style.display = "block";
        } else {
            comentarios.style.display = "none";
        }
    }
}