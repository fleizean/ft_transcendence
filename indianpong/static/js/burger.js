export function initializeBurger () {
    document.querySelector(".burger-menu").addEventListener("click", function () {
        var navLinks = document.querySelector(".nav-links");
        if (navLinks.classList.contains("show")) {
            navLinks.classList.remove("show");
        } else {
            navLinks.classList.add("show");
        }
    });
}