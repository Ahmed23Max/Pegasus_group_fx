document.addEventListener("DOMContentLoaded", function () {
            const blurBackground = document.querySelector(".blur-background");
            const fullScreenNavbar = document.querySelector(".full-screen-navbar");
            const navbarToggler = document.querySelector(".navbar-toggler");
            
            navbarToggler.addEventListener("click", function () {
                blurBackground.classList.toggle("show-blur");
                fullScreenNavbar.classList.toggle("show-navbar");
                document.body.style.overflow = "hidden";
            });
            
            blurBackground.addEventListener("click", function () {
                blurBackground.classList.remove("show-blur");
                fullScreenNavbar.classList.remove("show-navbar");
                document.body.style.overflow = "auto";
            });
        });
