document.addEventListener('DOMContentLoaded', function(){
    const videoButton = document.getElementById('videoButton');
    const imagenButton = document.getElementById('imagenButton');
    const handleFileChanger = (e) => {
        const archivo = e.target.files[0];
        const nombreDisplay = document.getElementById('nombre-archivo');
        
        if (archivo) {
            nombreDisplay.textContent = archivo.name;
            console.log('Archivo seleccionado:', archivo.name);
        } else {
            nombreDisplay.textContent = 'Ningún archivo seleccionado';
        }
    };
});

