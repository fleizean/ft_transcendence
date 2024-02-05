function showcontent(url) {
    console.log("url bu: " + url);
    fetch(url)
    .then(response => response.text())
    .then (text => {
        document.querySelector('#app').innerHTML = text;
        // Yeni butonları seç ve dinleyici ekle
        document.querySelectorAll('button').forEach(button => {
            button.onclick = function () {
                showcontent(this.dataset.section);
            };
        });
        window.addEventListener("popstate", function(event) {
            var htmlContent = event.state.htmlContent;
            document.querySelector('#app').innerHTML = htmlContent;
        });
        // URL'yi güncelle
        history.pushState({ htmlContent: text }, "", url);
    })
}

// Sayfa yüklendiğinde
window.addEventListener('load', function() {
    // Mevcut butonları seç ve dinleyici ekle
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function () {
            showcontent(this.dataset.section);
        };
    });

    // Belirli bir sınıfa sahip butonlara tıklandığında
    document.addEventListener('click', function(event) {
        const element = event.target;
        if (element.tagName === 'button' && element.className === 'registerbtn') {
            showcontent(element.dataset.section);
        }
    });

    // Geri ve ileri butonlarına basıldığında
    window.addEventListener("popstate", function(event) {
        var htmlContent = event.state.htmlContent;
        document.querySelector('#app').innerHTML = htmlContent;
    });

    // URL'yi elle yazdığında veya sayfa yenilendiğinde
    var currentURL = window.location.pathname;
    showcontent(currentURL);
});
