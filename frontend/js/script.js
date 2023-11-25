document.addEventListener('DOMContentLoaded', function () {
    // Hemen çalıştırılacak kod buraya eklenecek

    const cover = document.querySelector('.backgroundimage');

    for (let i = 1; i < 100; i++) {
        const snowFlake = document.createElement('div');
        snowFlake.className = 'snow';
        cover.appendChild(snowFlake);

        const size = Math.random() * 3;
        snowFlake.style.width = `${size}px`;
        snowFlake.style.height = `${size}px`;

        const delay = Math.random();
        snowFlake.style.animation = `snowRain 5s linear ${delay}s infinite`;
        console.log("delay" + delay);

        const left = Math.random() * 100;
        snowFlake.style.left = `${left}vw`;

        const animationDuration = 5 + Math.random() * 5;
        snowFlake.style.animationDuration = `${animationDuration}s`;

        // Kar tanelerini ilk 3 saniye boyunca görünmez yap
        snowFlake.style.opacity = 0;
        snowFlake.style.animationPlayState = 'running';

        // Zamanlayıcı ile 3 saniye sonra görünürlüğü aç
        setTimeout(() => {
            snowFlake.style.opacity = 1;
            snowFlake.style.animationPlayState = 'running';
        }, 1300);
    }

});

function toggleShowContainer() {
    var popupContainer = document.getElementById('popupContainer');
    popupContainer.style.display = (popupContainer.style.display === 'none' || popupContainer.style.display === '') ? 'block' : 'none';
}