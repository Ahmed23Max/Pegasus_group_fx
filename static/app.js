
$(document).ready(function() {
    $(".navbar-toggler").click(function() {
        $("#overlay").toggle();
        $("body").toggleClass("blurred");
    });
});
