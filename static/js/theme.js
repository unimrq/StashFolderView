function switchTheme(theme) {
    let themeStylesheet = document.getElementById("theme-stylesheet");

    if (theme === 'light') {
        themeStylesheet.setAttribute("href", "light-light-theme.css");
    } else if (theme === 'dark') {
        themeStylesheet.setAttribute("href", "dark-light-theme.css");
    } else if (theme === 'contrast') {
        themeStylesheet.setAttribute("href", "contrast-light-theme.css");
    }
}