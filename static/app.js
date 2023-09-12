// welcome.js

// Check if a flag is set in session storage
if (!sessionStorage.getItem('visited_welcome_page')) {
    // If not set, it means the user hasn't seen the welcoming page before
    // Perform the animation and set the flag
    setTimeout(function () {
        // Redirect to the homepage (replace 'home.html' with your homepage URL)
        window.location.href = 'home.html';
    }, 5000); // 5000 milliseconds (5 seconds) delay before redirecting

    // Set the flag in session storage to indicate that the user has visited the welcoming page
    sessionStorage.setItem('visited_welcome_page', 'true');
} else {
    // If the flag is set, the user has already seen the welcoming page
    // Redirect to the homepage immediately
    window.location.href = 'home.html';
}
