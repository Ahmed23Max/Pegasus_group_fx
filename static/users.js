// Select the login and signup elements
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

// Function to toggle password visibility
function togglePasswordVisibility(inputElement, eyeIcon) {
    const passwordInput = inputElement;
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('bi-eye-slash');
        eyeIcon.classList.add('bi-eye');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('bi-eye');
        eyeIcon.classList.add('bi-eye-slash');
    }
}

// Event listener for the login button
loginButton.addEventListener('click', () => {
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
});

// Event listener for the signup button
signupButton.addEventListener('click', () => {
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
});

// Event listener for the "Show Password" buttons
const togglePasswordButtons = document.querySelectorAll('.btn-toggle-password');
togglePasswordButtons.forEach((button) => {
    const passwordInput = button.parentElement.querySelector('input[type="password"]');
    const eyeIcon = button.querySelector('i');

    button.addEventListener('click', () => {
        togglePasswordVisibility(passwordInput, eyeIcon);
    });
});

// Event listener for the signup form submission
signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const signupUsername = document.getElementById('signup-username').value;
    const signupEmail = document.getElementById('signup-email').value;
    const signupPassword = document.getElementById('signup-password').value;
    const signupConfirmPassword = document.getElementById('signup-confirm-password').value;

    if (signupPassword !== signupConfirmPassword) {
        alert('Password and Confirm Password must match.');
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

// Event listener for the login form submission
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const loginUsername = document.getElementById('login-username').value;
    const loginPassword = document.getElementById('login-password').value;

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: loginUsername,
                password: loginPassword,
            }),
        });

        if (response.ok) {
            alert('Login successful!');
            // Reload the page after successful login
            window.location.reload();
        } else {
            alert('Login failed. Please try again.');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred. Please try again.');
    }
});
