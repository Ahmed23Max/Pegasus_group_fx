// pay.js

// Initialize Stripe
const stripe = Stripe('YOUR_STRIPE_PUBLIC_KEY'); // Replace with your actual Stripe public key
const elements = stripe.elements();

// Initialize the card element
const cardElement = elements.create('card');
cardElement.mount('#card-element');

// Handle errors from Stripe Elements
const cardErrors = document.getElementById('card-errors');

cardElement.on('change', (event) => {
    if (event.error) {
        cardErrors.textContent = event.error.message;
    } else {
        cardErrors.textContent = '';
    }
});

// Handle payment method toggle
const paymentMethodToggle = document.getElementById('payment-method-toggle');
const paypalPayment = document.querySelector('.paypal-payment');
const stripePayment = document.querySelector('.stripe-payment');
const stripeButton = document.getElementById('stripe-button');
const paypalButton = document.getElementById('paypal-button');

paymentMethodToggle.addEventListener('change', () => {
    const selectedPaymentMethod = paymentMethodToggle.value;

    if (selectedPaymentMethod === 'paypal') {
        stripePayment.style.display = 'none';
        paypalPayment.style.display = 'block';
        initializePayPalButton(); // Initialize the PayPal button when selecting PayPal as the payment method
    } else if (selectedPaymentMethod === 'stripe') {
        paypalPayment.style.display = 'none';
        stripePayment.style.display = 'block';
    }
});

paypalButton.addEventListener('click', () => {
    stripePayment.style.display = 'none';
    paypalPayment.style.display = 'block';
    initializePayPalButton(); // Initialize the PayPal button
});

stripeButton.addEventListener('click', async () => {
    try {
        // Send an AJAX request to get the client secret
        const response = await fetch('/create-payment-intent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: 1000,  // Replace with the actual amount in cents
            }),
        });

        const { clientSecret } = await response.json();

        // Confirm the payment on the client side using the client secret
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
            },
        });

        if (result.error) {
            // Handle payment error
            cardErrors.textContent = result.error.message;
            console.error('Stripe Error:', result.error.message); // Log the error to the console
        } else if (result.paymentIntent.status === 'succeeded') {
            // Payment was successful
            alert('Payment successful! Payment Intent ID: ' + result.paymentIntent.id);
            // Optionally, you can redirect or perform other actions here
        }
    } catch (error) {
        console.error('An error occurred:', error); // Log any unexpected errors
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
