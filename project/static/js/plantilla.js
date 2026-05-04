document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector('.toggle-btn');
    const menu = document.querySelector('.menu');

    btn.addEventListener('click', (e) => {
        e.preventDefault(); 
        menu.classList.toggle('open');
    });
    
    const btnLogOut = document.querySelector('#btnLogOut');
});