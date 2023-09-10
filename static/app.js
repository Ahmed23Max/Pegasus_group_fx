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

function startLoading(buttonId) {
    var button = document.getElementById(buttonId);
    var loadingIcon = button.querySelector(".loading-icon");
  
    // Disable the button
    button.disabled = true;
  
    // Change text to "Loading..."
    button.innerHTML = "Loading";
  
    // Show loading icon
    loadingIcon.style.display = "inline-block";
  
    // Simulate a loading delay (you can replace this with your actual loading code)
    setTimeout(function() {
      // Once the loading is complete, you can reset the button
      button.disabled = false;
      button.innerHTML = "Select";
      loadingIcon.style.display = "none";
    }, 500); // Replace 2000 with your desired loading time in milliseconds
  }






 
  // JavaScript function to capture the selected card amount and description, and redirect to checkout
  function selectCard(amount, description) {
    window.location.href = `/checkout?amount=${amount}&description=${encodeURIComponent(description)}`;
}

