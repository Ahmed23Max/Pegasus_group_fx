from flask import Flask, render_template, request
import stripe

app = Flask(__name__)

# Set your Stripe secret key here
stripe.api_key = 'your_stripe_secret_key'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/guaranteed-pass')
def guaranteed_pass():
    return render_template('guaranteed_pass.html')

@app.route('/funding_25k')
def funding_25k():
    return render_template('guaranteed_funding/funding_25000.html')

@app.route('/funding_50k')
def funding_50k():
    return render_template('guaranteed_funding/funding_50000.html')

@app.route('/funding_100k')
def funding_100k():
    return render_template('guaranteed_funding/funding_100000.html')

@app.route('/funding_200k')
def funding_200k():
    return render_template('guaranteed_funding/funding_200000.html')

@app.route('/funding_300k')
def funding_300k():
    return render_template('guaranteed_funding/funding_300000.html')

@app.route('/funding_400k')
def funding_400k():
    return render_template('guaranteed_funding/funding_400000.html')

@app.route('/funding_550k')
def funding_550k():
    return render_template('guaranteed_funding/funding_550000.html')

@app.route('/funding_650k')
def funding_650k():
    return render_template('guaranteed_funding/funding_650000.html')


@app.route('/purchase/<int:amount>', methods=['GET', 'POST'])
def purchase(amount):
    if request.method == 'POST':
        try:
            # Create a payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount * 100,  # Stripe uses cents, so multiply by 100
                currency='gbp',  # Use appropriate currency code
            )
            
            return render_template('payment.html', client_secret=payment_intent.client_secret)
        except Exception as e:
            return str(e)
    
    return render_template('funding_purchase.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)
