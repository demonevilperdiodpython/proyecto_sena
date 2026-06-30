const sidebar = coreui.Sidebar.getOrCreateInstance(
    document.querySelector('#sidebar')
);

document.getElementById("btnMenu").onclick = () => {
    sidebar.toggle();
};