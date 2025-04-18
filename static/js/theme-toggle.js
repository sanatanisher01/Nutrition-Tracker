document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeStylesheet = document.getElementById('theme-style');
    const themeIcon = themeToggle.querySelector('i');
    
    // Check if user has a theme preference stored
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Set initial theme
    if (currentTheme === 'dark') {
        themeStylesheet.href = '/static/css/dark-theme.css';
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        document.body.classList.add('dark-theme');
    } else {
        themeStylesheet.href = '/static/css/light-theme.css';
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        document.body.classList.remove('dark-theme');
    }
    
    // Toggle theme when button is clicked
    themeToggle.addEventListener('click', function() {
        if (themeStylesheet.href.includes('light-theme')) {
            themeStylesheet.href = '/static/css/dark-theme.css';
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            themeStylesheet.href = '/static/css/light-theme.css';
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            document.body.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        }
    });
});
