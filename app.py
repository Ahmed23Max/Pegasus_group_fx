from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import uuid


app = Flask(__name__)
app.secret_key = 'In9$]~3raxeG%L"7toNZwnuS:0D$?aq%{8+^R}(~<Xh3*P}.nmB4|fixQVwQ]:B'  # Replace with a strong secret key

active_sessions = {}

# Your database configuration
db_config = {
    'dbname': 'pegasus_g8fn',
    'user': 'pegasus_g8fn_user',
    'password': '11BVk9h5u7os4mCxD8dMNhMpSB4sivyv',
    'host': 'dpg-cjlngg8cfp5c739tetpg-a.oregon-postgres.render.com'
}

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51NfpBYL5fKqjqr4brHAttz9zTiXePX1pNh1nez4pbDTasqu8YrFy8otnJsfbyqqs5au4C5Nyq3EHVyGERFG7lUr300ZfXuqwzy'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51NfpBYL5fKqjqr4bdI5TLSqA4pQXSXqKIy7rHkzcEt689S2Lv6BPkUB7JLU3xHp4nVAiQvFrE0K8iwYGnXwtO7mm00ZvVxJV9c'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Add 27 more countries with flags to the dictionary
countries_with_flags = {
    "Albania": "🇦🇱",
    "Algeria": "🇩🇿",
    "Argentina": "🇦🇷",
    "Armenia": "🇦🇲",
    "Australia": "🇦🇺",
    "Bahamas": "🇧🇸",
    "Bahrain": "🇧🇭",
    "Bangladesh": "🇧🇩",
    "Barbados": "🇧🇧",
    "Belarus": "🇧🇾",
    "Belize": "🇧🇿",
    "Benin": "🇧🇯",
    "Bhutan": "🇧🇹",
    "Bolivia": "🇧🇴",
    "Brazil": "🇧🇷",
    "Brunei": "🇧🇳",
    "Bulgaria": "🇧🇬",
    "Cambodia": "🇰🇭",
    "Canada": "🇨🇦",
    "Cabo Verde": "🇨🇻",
    "Cameroon": "🇨🇲",
    "Chad": "🇹🇩",
    "Chile": "🇨🇱",
    "China": "🇨🇳",
    "Colombia": "🇨🇴",
    "Comoros": "🇰🇲",
    "Croatia": "🇭🇷",
    "Cyprus": "🇨🇾",
    "Côte d'Ivoire": "🇨🇮",
    "Djibouti": "🇩🇯",
    "Dominican Republic": "🇩🇴",
    "DR Congo": "🇨🇩",
    "Ecuador": "🇪🇨",
    "Egypt": "🇪🇬",
    "El Salvador": "🇸🇻",
    "Eritrea": "🇪🇷",
    "Estonia": "🇪🇪",
    "Eswatini": "🇸🇿",
    "Ethiopia": "🇪🇹",
    "Fiji": "🇫🇯",
    "Finland": "🇫🇮",
    "France": "🇫🇷",
    "Gambia": "🇬🇲",
    "Georgia": "🇬🇪",
    "Germany": "🇩🇪",
    "Ghana": "🇬🇭",
    "Grenada": "🇬🇩",
    "Guinea": "🇬🇳",
    "Guyana": "🇬🇾",
    "Haiti": "🇭🇹",
    "Honduras": "🇭🇳",
    "Hungary": "🇭🇺",
    "Iceland": "🇮🇸",
    "India": "🇮🇳",
    "Indonesia": "🇮🇩",
    "Iran": "🇮🇷",
    "Iraq": "🇮🇶",
    "Italy": "🇮🇹",
    "Jamaica": "🇯🇲",
    "Japan": "🇯🇵",
    "Jordan": "🇯🇴",
    "Kazakhstan": "🇰🇿",
    "Kenya": "🇰🇪",
    "Kuwait": "🇰🇼",
    "Kyrgyzstan": "🇰🇬",
    "Lao PDR": "🇱🇦",
    "Latvia": "🇱🇻",
    "Lebanon": "🇱🇧",
    "Liberia": "🇱🇷",
    "Libya": "🇱🇾",
    "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Macau": "🇲🇴",
    "Madagascar": "🇲🇬",
    "Malawi": "🇲🇼",
    "Maldives": "🇲🇻",
    "Mali": "🇲🇱",
    "Malta": "🇲🇹",
    "Mauritania": "🇲🇷",
    "Mauritius": "🇲🇺",
    "Mexico": "🇲🇽",
    "Moldova": "🇲🇩",
    "Mozambique": "🇲🇿",
    "Myanmar": "🇲🇲",
    "Namibia": "🇳🇦",
    "Nepal": "🇳🇵",
    "Netherlands": "🇳🇱",
    "New Zealand": "🇳🇿",
    "Nicaragua": "🇳🇮",
    "Niger": "🇳🇪",
    "Nigeria": "🇳🇬",
    "North Korea": "🇰🇵",
    "Norway": "🇳🇴",
    "Oman": "🇴🇲",
    "Pakistan": "🇵🇰",
    "Palestine": "🇵🇸",
    "Panama": "🇵🇦",
    "Peru": "🇵🇪",
    "Philippines": "🇵🇭",
    "Poland": "🇵🇱",
    "Portugal": "🇵🇹",
    "Qatar": "🇶🇦",
    "Rwanda": "🇷🇼",
    "Saint Lucia": "🇱🇨",
    "Saint Vincent and the Grenadines": "🇻🇨",
    "Samoa": "🇼🇸",
    "Saudi Arabia": "🇸🇦",
    "Senegal": "🇸🇳",
    "Sierra Leone": "🇸🇱",
    "Singapore": "🇸🇬",
    "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮",
    "Solomon Islands": "🇸🇧",
    "Somalia": "🇸🇴",
    "South Africa": "🇿🇦",
    "South Korea": "🇰🇷",
    "Spain": "🇪🇸",
    "Sri Lanka": "🇱🇰",
    "Sudan": "🇸🇩",
    "Suriname": "🇸🇷",
    "Sweden": "🇸🇪",
    "Switzerland": "🇨🇭",
    "Syria": "🇸🇾",
    "Taiwan": "🇹🇼",
    "Tajikistan": "🇹🇯",
    "Tanzania": "🇹🇿",
    "Timor-Leste": "🇹🇱",
    "Trinidad and Tobago": "🇹🇹",
    "Tunisia": "🇹🇳",
    "Turkey": "🇹🇷",
    "Uganda": "🇺🇬",
    "Ukraine": "🇺🇦",
    "United Arab Emirates": "🇦🇪",
    "United Kingdom": "🇬🇧",
    "United States": "🇺🇸",
    "Uruguay": "🇺🇾",
    "Uzbekistan": "🇺🇿",
    "Vanuatu": "🇻🇺",
    "Venezuela": "🇻🇪",
    "Vietnam": "🇻🇳",
    "Yemen": "🇾🇪",
    "Zimbabwe": "🇿🇼",
}


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

            cursor.execute("SELECT id, username, password, email FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                # Generate a unique session ID
                session_id = str(uuid.uuid4())

                # Store user data in the active_sessions dictionary
                active_sessions[session_id] = {
                    'user_id': user[0],
                    'user_name': user[1],
                    'user_email': user[3]  # Set the user's email in the session
                }

                # Store the user's ID, name, and email in the session
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['user_email'] = user[3]  # Set the user's email in the session

                # Set the session ID as a cookie
                response = jsonify({"message": "Login successful!"})
                response.set_cookie('session_id', session_id)
                return response
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


@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        # Remove the session data from the active_sessions dictionary
        active_sessions.pop(session_id, None)

        # Clear the session data
        session.clear()

    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if 'user_id' in session and 'user_name' in session:
        user_id = session['user_id']

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Retrieve the user's profile data from the database
            cursor.execute("SELECT username, email, date_of_birth, location, phone_number FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                user_name = user_data[0]
                user_email = user_data[1]
                user_date_of_birth = user_data[2] or 'Not provided'
                user_location = user_data[3] or 'Not provided'
                user_phone_number = user_data[4] or 'Not provided'
            else:
                # Handle the case where user_data is None
                user_name = session['user_name']
                user_email = session.get('user_email', 'Not provided')
                user_date_of_birth = session.get('user_date_of_birth', 'Not provided')
                user_location = session.get('user_location', 'Not provided')
                user_phone_number = session.get('user_phone_number', 'Not provided')

            return render_template('profile.html', user_name=user_name, user_email=user_email,
                                   user_date_of_birth=user_date_of_birth, user_location=user_location,
                                   user_phone_number=user_phone_number, countries_with_flags=countries_with_flags)
        except psycopg2.Error as e:
            flash('An error occurred while retrieving your profile. Please try again.', 'danger')
            return redirect(url_for('login'))
        finally:
            conn.close()
    else:
        return redirect(url_for('login'))





@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' in session and 'user_name' in session:
        user_id = session['user_id']
        
        # Get the profile information from the submitted form data
        date_of_birth = request.form.get('date_of_birth')
        location = request.form.get('location')
        phone_number = request.form.get('phone_number')

        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Update the user's profile in the database
            cursor.execute("UPDATE users SET date_of_birth = %s, location = %s, phone_number = %s WHERE id = %s",
                           (date_of_birth, location, phone_number, user_id))

            conn.commit()

            # Update session variables with the new profile information
            session['user_date_of_birth'] = date_of_birth
            session['user_location'] = location
            session['user_phone_number'] = phone_number

            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        except psycopg2.Error as e:
            conn.rollback()
            flash('Profile update failed. Please try again.', 'danger')
            return redirect(url_for('profile'))
        finally:
            conn.close()
    else:
        return redirect(url_for('login'))




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

