document.addEventListener('DOMContentLoaded', function(){
    const sidebarbutton = document.getElementById('sidebar-btn')
    const sidebar = coreui.Sidebar.getOrCreateInstance(document.querySelector('.sidebar'));
    const ccontainer = document.querySelector('.container-2').parentElement
    const sidebarElement = document.querySelector('.sidebar');
    

    sidebarbutton.addEventListener('click',function(){
        console.log(ccontainer.className)
        ccontainer.classList.toggle('sidebar-closed')
        sidebarElement.classList.toggle('sidebar-narrow');
    });
});
