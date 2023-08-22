 document.addEventListener("DOMContentLoaded", function () {
        const blurBackground = document.querySelector(".blur-background");
        const fullScreenNavbar = document.querySelector(".full-screen-navbar");
        const mainNavbarToggler = document.querySelector(".navbar-toggler");
        const mobileNavbarToggler = document.querySelector(".navbar-content .navbar-toggler");
        
        mainNavbarToggler.addEventListener("click", function () {
            blurBackground.classList.toggle("show-blur");
            fullScreenNavbar.classList.toggle("show-navbar");
            document.body.style.overflow = "hidden";
        });
        
        mobileNavbarToggler.addEventListener("click", function () {
            blurBackground.classList.remove("show-blur");
            fullScreenNavbar.classList.remove("show-navbar");
            document.body.style.overflow = "auto";
        });
    });
