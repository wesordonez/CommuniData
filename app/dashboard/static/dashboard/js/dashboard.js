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

// Get today's date
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

const date = new Date();
const today = formatDate(date);
document.getElementById('current-date').textContent = today;