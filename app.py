from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify,session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

app = Flask(__name__)
app.secret_key = 'In9$]~3raxeG%L"7toNZwnuS:0D$?aq%{8+^R}(~<Xh3*P}.nmB4|fixQVwQ]:B'  # Replace with a strong secret key



# Your database configuration
db_config = {
    'dbname': 'pegasus_g8fn',
    'user': 'pegasus_g8fn_user',
    'password': '11BVk9h5u7os4mCxD8dMNhMpSB4sivyv',
    'host': 'dpg-cjlngg8cfp5c739tetpg-a.oregon-postgres.render.com'
}

app.config['STRIPE_PUBLIC_KEY']= 'pk_test_51NfpBYL5fKqjqr4brHAttz9zTiXePX1pNh1nez4pbDTasqu8YrFy8otnJsfbyqqs5au4C5Nyq3EHVyGERFG7lUr300ZfXuqwzy'
app.config['STRIPE_SECRET_KEY']= 'sk_test_51NfpBYL5fKqjqr4bdI5TLSqA4pQXSXqKIy7rHkzcEt689S2Lv6BPkUB7JLU3xHp4nVAiQvFrE0K8iwYGnXwtO7mm00ZvVxJV9c'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Route to serve the checkout page


# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['user_name'] = user[1]  # Store the user's name in the session
                return redirect(url_for('index'))  # Redirect to the home page
            else:
                return jsonify({"message": "Login failed. Please check your credentials."}), 401
        except psycopg2.Error as e:
            return jsonify({"message": "An error occurred. Please try again."}), 500
        finally:
            conn.close()



# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='sha256')

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            
            conn.commit()
            return jsonify({"message": "Registration successful! You can now log in."}), 200
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"message": "Registration failed. Please try again."}), 400
        finally:
            conn.close()



# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You  have been logged out.', 'success')
    return redirect(url_for('index'))  # Redirect to the /checkout page


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/guaranteed-pass')
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
                           checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])


@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/success')
def success():
    # Render your success template or return a success message
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    # Render your cancel template or return a cancel message
    return render_template('cancel.html')

@app.route('/Account')
def Account():
    # Render your cancel template or return a cancel message
    return render_template('account.html')

if __name__ == '__main__':
    app.run(debug=True)