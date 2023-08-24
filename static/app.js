$(document).ready(function () {
    $(".navbar-toggler").click(function () {
        $(".mobile-overlay").fadeToggle(); // Toggle the overlay
        $("body").toggleClass("no-scroll"); // Prevent scrolling on background
    });

    // Close the overlay when clicking anywhere on it
    $(".mobile-overlay").click(function () {
        $(this).fadeOut();
        $("body").removeClass("no-scroll");
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCloseIcon = document.querySelector(".navbar-close-icon");

    navbarToggler.addEventListener("click", function () {
        navbarToggler.classList.toggle("active");
        navbarCloseIcon.classList.toggle("active");
    });
});

