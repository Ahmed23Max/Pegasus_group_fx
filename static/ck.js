// Select the login, signup, and payment elements
const loginButton = document.getElementById('login-button');
const signupButton = document.getElementById('signup-button');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const paymentBox = document.getElementById('payment-box');
const payButton = document.getElementById('pay-button');

// Select the payment method buttons
const stripeButton = document.getElementById('stripe-button');
const paypalButton = document.getElementById('paypal-button');

// Select the payment forms
const stripePayment = document.querySelector('.stripe-payment');
const paypalPayment = document.querySelector('.paypal-payment');

// Select the Stripe payment form fields
const stripePaymentForm = document.getElementById('stripe-payment-form');
const cardElement = document.getElementById('card-element');
const cardErrors = document.getElementById('card-errors');

// Function to toggle between payment methods
const paymentMethodToggle = document.getElementById('payment-method-toggle');

paymentMethodToggle.addEventListener('change', () => {
    const selectedPaymentMethod = paymentMethodToggle.value;

    if (selectedPaymentMethod === 'stripe') {
        stripePayment.style.display = 'block';
        paypalPayment.style.display = 'none';
    } else if (selectedPaymentMethod === 'paypal') {
        stripePayment.style.display = 'none';
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

// Function to check if all required fields are filled and enable the pay button
function checkPaymentFormValidity() {
    const cardNumberValue = cardElement.value.trim();

    const isCardNumberValid = cardNumberValue.length === 16; // You may need to adjust this validation logic

    const isFormValid = isCardNumberValid;
    payButton.disabled = !isFormValid;
}

// Listen for input changes in the payment form fields
cardElement.addEventListener('input', checkPaymentFormValidity);

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

// Event listener for the stripe button
stripeButton.addEventListener('click', () => {
    stripePayment.style.display = '
