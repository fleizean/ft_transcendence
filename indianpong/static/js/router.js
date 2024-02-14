/* // Function to update inner HTML of app class with fetched text
function updateAppInnerHTML(text) {
    console.log("çalışıyorum");
    const appElement = document.querySelector('.app');
    if (appElement) {
        appElement.innerHTML = text;
    }
}

// Event listener for URL changes
window.addEventListener('popstate', async () => {
    try {
        const path = window.location.pathname;
        console.log("path: " + path);
        const response = await fetch(path);
        const text = await response.text();
        updateAppInnerHTML(text);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});
 */