import stripe
from flask import Blueprint, render_template, current_app

stripe_blueprint = Blueprint('stripe', __name__)

# Stripe Configuration (Move the configuration to the top)
STRIPE_PUBLIC_KEY = 'pk_test_51NfpBYL5fKqjqr4brHAttz9zTiXePX1pNh1nez4pbDTasqu8YrFy8otnJsfbyqqs5au4C5Nyq3EHVyGERFG7lUr300ZfXuqwzy'
STRIPE_SECRET_KEY = 'sk_test_51NfpBYL5fKqjqr4bdI5TLSqA4pQXSXqKIy7rHkzcEt689S2Lv6BPkUB7JLU3xHp4nVAiQvFrE0K8iwYGnXwtO7mm00ZvVxJV9c'

# Set up Stripe
stripe.api_key = STRIPE_SECRET_KEY  # Use the configured Stripe secret key

@stripe_blueprint.route('/guaranteed-pass')
def guaranteed_pass():
    session_basic = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1NoP1zL5fKqjqr4bIDXv8EjT',
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://pegasus-group-fx.onrender.com/success',
        cancel_url='https://pegasus-group-fx.onrender.com/cancel'
    )
    session_intermediate = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1NoOGCL5fKqjqr4bIlHGer5D',
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://pegasus-group-fx.onrender.com/success',
        cancel_url='https://pegasus-group-fx.onrender.com/cancel'
    )
    session_elite = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1NoP42L5fKqjqr4bxKpnA7rY',
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://pegasus-group-fx.onrender.com/success',
        cancel_url='https://pegasus-group-fx.onrender.com/cancel'
    )
    session_ultimate = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1NoP4eL5fKqjqr4baxCYNkLs',
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://pegasus-group-fx.onrender.com/success',
        cancel_url='https://pegasus-group-fx.onrender.com/cancel'
    )

    return render_template('guaranteed_pass.html',
                           checkout_session_basic_id=session_basic['id'],
                           checkout_session_intermediate_id=session_intermediate['id'],
                           checkout_session_elite_id=session_elite['id'],
                           checkout_session_ultimate_id=session_ultimate['id'],
                           checkout_public_key=STRIPE_PUBLIC_KEY)  # Use the configured Stripe public key


@stripe_blueprint.route('/success')
def success():
    # Render your success template or return a success message
    return render_template('success.html')


@stripe_blueprint.route('/cancel')
def cancel():
    # Render your cancel template or return a cancel message
    return render_template('cancel.html')