
    const stripe = Stripe('your_stripe_publishable_key');
    const elements = stripe.elements();
    
    const card = elements.create('card');
    card.mount('#card-element');
    
    const form = document.getElementById('payment-form');
    
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const {token, error} = await stripe.createToken(card);
        
        if (error) {
            console.error(error);
        } else {
            // Send token to server for payment processing
            const amountInCents = {{ amount * 100 }};
            const response = await fetch('/process_payment', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token: token.id, amount: amountInCents})
            });
            
            const data = await response.json();
            
            if (data.success) {
                window.location.href = '/payment_success';
            } else {
                console.error(data.error);
            }
        }
    });


