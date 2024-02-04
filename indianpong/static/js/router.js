// myapp/static/app.js
document.addEventListener("DOMContentLoaded", function() {
    fetchData('/');
    var dataContainer = document.getElementById("app");
    function fetchData(url) {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            }) 
            .then(htmlContent => {
                dataContainer.innerHTML = htmlContent;
                history.pushState({ htmlContent: htmlContent }, "", url);
            })
            .catch(error => {
                console.error('HTML içeriği alınırken bir hata oluştu:', error);
            });
    }

    window.addEventListener("popstate", function(event) {
        var htmlContent = event.state.htmlContent;
        dataContainer.innerHTML = htmlContent;
    });

    // Kullanıcının URL'sini elle girmesini dinlemek için popstate olayını dinleyin
    window.addEventListener("popstate", function(event) {
        // Yeni URL'yi al
        var newURL = location.pathname;
        // fetchData fonksiyonunu yeni URL ile çağır
        fetchData(newURL);
    });

    // URL'yi el ile değiştirmek için bir fonksiyon
    function changeUrl(url) {
        history.pushState({ htmlContent: dataContainer.innerHTML }, "", url);
        fetchData(url);
    }

    // ileri ve geri butonlarının çalışmasını sağlamak için popstate olayını dinle
    window.addEventListener("popstate", function(event) {
        var htmlContent = event.state.htmlContent;
        dataContainer.innerHTML = htmlContent;
    });

    // Sayfa yüklendiğinde index.html içeriğini almak için bir istek yap
    
    
});
