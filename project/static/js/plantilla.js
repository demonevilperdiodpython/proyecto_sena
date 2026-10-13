document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector('.toggle-btn');

    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Muestra/oculta el nav lateral (sidebar) en vez del menú antiguo
            const sidebar = document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.classList.toggle('sidebar-open');
            }
        });
    }
});
