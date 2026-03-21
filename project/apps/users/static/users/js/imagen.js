document.getElementById('id_imagen').addEventListener('change', function(event) {
    document.querySelectorAll('.image-radio').forEach(r => r.checked = false);
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            document.getElementById('preview').src = e.target.result;
        }

        reader.readAsDataURL(file);
    }
});
let seleccionado = false;

document.querySelectorAll('.image-radio').forEach(radio => {
    radio.addEventListener('change', function() {

        if (this.checked) {
            const selectedInput = document.getElementById('selected_image');
            const img = this.closest('label').querySelector('img');
            imgSrc = img.getAttribute('src');
            document.getElementById('preview').src = imgSrc;
            document.getElementById('id_imagen').value = '';
            document.getElementById('id_imagen').src= imgSrc;
        }

    });
});
