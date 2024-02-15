/* 
window.addEventListener('load', () => {
    loadPage(window.location.pathname);
    console.log("test: " + window.location.pathname);
});

// Capture all links
document.querySelectorAll('a[data-link]').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        const href = link.getAttribute('href');
        history.pushState({ path: href }, '', href);
        console.log("href: " + href);
        loadPage(href);
    });
});

// Listen to the popstate event
window.addEventListener('popstate', e => {
    const path = e.state.path;
    loadPage(path);
});

// Page loading function
function loadPage(path) {
    // Always load index.html first
    fetch('/')
        .then(response => response.text())
        .then(html => {
            if (path !== '/') {
                fetch(path)
                .then(response => response.text())
                .then(partHtml => {
                        document.documentElement.innerHTML = html;
                        document.querySelector('.app').innerHTML = partHtml;
                    })
                    .catch(error => console.error('Error fetching additional part:', error));
            }
            else {
                document.documentElement.innerHTML = html;
            }
        })
        .catch(error => console.error('Error fetching index.html:', error));
}
 */