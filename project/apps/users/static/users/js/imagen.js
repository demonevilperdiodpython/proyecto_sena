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

    