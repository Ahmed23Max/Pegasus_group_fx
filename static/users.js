// users.js

// Function to toggle password visibility
function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

// Toggle password visibility for login form
document.getElementById("show-login-password").addEventListener("click", function () {
    togglePasswordVisibility("login-password");
});

// Toggle password visibility for signup form
document.getElementById("show-signup-password").addEventListener("click", function () {
    togglePasswordVisibility("signup-password");
});

// Toggle password visibility for confirm password in signup form
document.getElementById("show-signup-confirm-password").addEventListener("click", function () {
    togglePasswordVisibility("signup-confirm-password");
});

// Select the login and signup elements
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const paymentBox = document.getElementById('payment-box');

// Event listener for the signup form submission
signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const signupUsername = document.getElementById('signup-username').value;
    const signupEmail = document.getElementById('signup-email').value;
    const signupPassword = document.getElementById('signup-password').value;
    const signupConfirmPassword = document.getElementById('signup-confirm-password').value;

    // Check if the password and confirm password match
    if (signupPassword !== signupConfirmPassword) {
        alert('Password and confirm password do not match. Please try again.');
        return;
    }

    try {
        const response = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: signupUsername,
                email: signupEmail,
                password: signupPassword,
            }),
        });

        if (response.ok) {
            alert('Registration successful! You can now log in.');
            loginForm.style.display = 'block'; // Show the login form after successful registration
            signupForm.style.display = 'none'; // Hide the signup form
            // Optionally, you can clear the signup form fields here
        } else {
            alert('Registration failed. Please try again.');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred. Please try again.');
    }
});
