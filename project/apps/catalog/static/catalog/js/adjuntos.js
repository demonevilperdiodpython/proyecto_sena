/* Boton de adjuntar archivos del post.

   Hay un solo boton (antes habia uno de imagen y otro de video). El input
   va oculto y con multiple, asi que el navegador deja marcar cuantos
   archivos se quiera, de cualquier tipo: este boton solo lo abre.

   Los archivos elegidos se listan antes de publicar, para que se vea lo
   que se va a enviar y se pueda quitar algo. */

(function () {
    function tamano(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(0) + " KB";
        if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + " MB";
        return (bytes / (1024 * 1024 * 1024)).toFixed(1) + " GB";
    }

    function pintarLista(input, lista) {
        lista.innerHTML = "";
        if (!input.files || input.files.length === 0) {
            lista.hidden = true;
            return;
        }
        lista.hidden = false;

        for (const archivo of input.files) {
            const fila = document.createElement("li");
            fila.className = "archivo-lista-item";

            const nombre = document.createElement("span");
            nombre.className = "archivo-nombre";
            nombre.textContent = archivo.name;
            nombre.title = archivo.name;

            const peso = document.createElement("span");
            peso.className = "archivo-peso";
            peso.textContent = tamano(archivo.size);

            /* Poner un archivo suelto en la lista, para poder quitarlo sin
               tener que abrir otra vez el selector. */
            const quitar = document.createElement("button");
            quitar.type = "button";
            quitar.className = "archivo-quitar";
            quitar.textContent = "×";
            quitar.title = "Quitar " + archivo.name;
            quitar.setAttribute("aria-label", "Quitar " + archivo.name);
            quitar.addEventListener("click", function () {
                const transfer = new DataTransfer();
                for (const otro of input.files) {
                    if (otro !== archivo) transfer.items.add(otro);
                }
                input.files = transfer.files;
                pintarLista(input, lista);
            });

            fila.appendChild(nombre);
            fila.appendChild(peso);
            fila.appendChild(quitar);
            lista.appendChild(fila);
        }
    }

    function conectar(boton) {
        const form = boton.closest("form");
        if (!form) return;
        const input = form.querySelector("input[type=file].input-archivos")
            || form.querySelector("input[type=file]");
        if (!input) return;

        const lista = form.querySelector("[data-lista-archivos]");

        boton.addEventListener("click", function () {
            input.click();
        });

        input.addEventListener("change", function () {
            if (lista) pintarLista(input, lista);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            document.querySelectorAll("[data-abrir-archivos]").forEach(conectar);
        });
    } else {
        document.querySelectorAll("[data-abrir-archivos]").forEach(conectar);
    }
})();