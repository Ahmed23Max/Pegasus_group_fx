from flask import Flask, render_template, request, jsonify
import stripe
import os

# Initialize Stripe with your secret key
stripe.api_key = 'YOUR_STRIPE_SECRET_KEY'

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/guaranteed-pass')
def guaranteed_pass():
    return render_template('guaranteed_pass.html')

@app.route('/25000-guaranteed-funding')
def funding_25000():
    return render_template('guaranteed_funding/funding_25000.html')

@app.route('/50000-guaranteed-funding')
def funding_50000():
    return render_template('guaranteed_funding/funding_50000.html')

@app.route('/100000-guaranteed-funding')
def funding_100000():
    return render_template('guaranteed_funding/funding_100000.html')

@app.route('/200000-guaranteed-funding')
def funding_200000():
    return render_template('guaranteed_funding/funding_200000.html')

@app.route('/300000-guaranteed-funding')
def funding_300000():
    return render_template('guaranteed_funding/funding_300000.html')

@app.route('/400000-guaranteed-funding')
def funding_400000():
    return render_template('guaranteed_funding/funding_400000.html')

@app.route('/550000-guaranteed-funding')
def funding_550000():
    return render_template('guaranteed_funding/funding_550000.html')

@app.route('/650000-guaranteed-funding')
def funding_650000():
    return render_template('guaranteed_funding/funding_650000.html')


@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    amount = int(request.form['amount'])
    email = request.form['email']

    # Create a payment intent
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='gbp',  # Change to your preferred currency
        receipt_email=email,
    )

    return jsonify(client_secret=payment_intent.client_secret)



if __name__ == '__main__':
    app.run(debug=True)
