document.getElementById('sidebar-toggle').addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('collapsed');
    document.getElementById('main-content').classList.toggle('collapsed');
});
