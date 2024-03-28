function updateApp(path) {
    fetch(path)
        .then(response => response.text())
        .then(html => document.body.innerHTML = html)
        .catch(error => console.error(error));
}

function swapApp(path) {
    currentPath = window.location.pathname;
    window.history.pushState({}, '', path);
    updateApp(path);
}

window.onpopstate = function(event) {
    updateApp(window.location.pathname);
};

function setLanguage(language) {
    document.cookie = "selectedLanguage=" + language;
    swapApp(window.location.pathname);
}