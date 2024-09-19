// Collapse the sidebar
function collapseSidebar() {
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.getElementById('sidebar');
        const collapseArrow = document.getElementById('collapse-arrow');

        collapseArrow.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            const arrowIcon = collapseArrow.querySelector('i');
            if (sidebar.classList.contains('collapsed')) {
                arrowIcon.classList.remove('fa-chevron-left');
                arrowIcon.classList.add('fa-chevron-right');
            } else {
                arrowIcon.classList.remove('fa-chevron-right');
                arrowIcon.classList.add('fa-chevron-left');
            }        });
    });
}

collapseSidebar();