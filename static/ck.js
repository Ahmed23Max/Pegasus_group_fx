// Select the login, signup, and payment elements
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const paymentBox = document.getElementById('payment-box');
const payButton = document.getElementById('pay-button');



// Function to toggle between payment methods
const paymentMethodToggle = document.getElementById('payment-method-toggle');
const paypalPayment = document.querySelector('.paypal-payment');

// Initially, set the default payment method to credit card
paymentMethodToggle.addEventListener('change', () => {
    const selectedPaymentMethod = paymentMethodToggle.value;

    if (selectedPaymentMethod === 'paypal') {
        creditCardPayment.style.display = 'none';
        paypalPayment.style.display = 'block';
        initializePayPalButton(); // Initialize the PayPal button when selecting PayPal as the payment method
    }
});

// Function to simulate payment processing
async function simulatePaymentProcessing() {
    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    // Simulate successful payment
    // Replace this with actual payment processing logic
}



// Trigger form validation on page load
window.addEventListener('load', () => {
    checkPaymentFormValidity();
});

// Event listener for the login button
loginButton.addEventListener('click', () => {
    loginForm.style.display = 'block';
    signupForm.style.display = 'none';
    paymentBox.style.display = 'none';
});

// Event listener for the signup button
signupButton.addEventListener('click', () => {
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
    paymentBox.style.display = 'none';
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
            paymentBox.style.display = 'block';
            // Optionally, you can redirect to another page here
        } else {
            alert('Login failed. Please try again.');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred. Please try again.');
    }
});

// Event listener for the signup form submission
signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const signupUsername = document.getElementById('signup-username').value;
    const signupEmail = document.getElementById('signup-email').value;
    const signupPassword = document.getElementById('signup-password').value;

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
            paymentBox.style.display = 'none'; // Hide the payment box
            // Optionally, you can clear the signup form fields here
        } else {
            alert('Registration failed. Please try again.');
        }
    } catch (error) {
        console.error(error);
        alert('An error occurred. Please try again.');
    }
});

// Function to initialize PayPal button
function initializePayPalButton() {
    paypal.Buttons({
        createOrder: function(data, actions) {
            // Add your PayPal payment details here
            return actions.order.create({
                purchase_units: [
                    {
                        amount: {
                            value: '10.00' // Replace with the amount you want to charge
                        }
                    }
                ]
            });
        },
        onApprove: function(data, actions) {
            // Capture the PayPal transaction and handle the payment confirmation
            return actions.order.capture().then(function(details) {
                alert('Payment successful! Transaction ID: ' + details.id);
                // Optionally, you can redirect or perform other actions here
            });
        },
        onError: function(err) {
            alert('Payment failed. Please try again or choose another payment method.');
        }
    }).render('paypal-button-container');
}

// Initial state: Hide all forms and payment box
loginForm.style.display = 'none';
signupForm.style.display = 'none';
paymentBox.style.display = 'none';
initializePayPalButton();
