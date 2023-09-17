from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify, session  # Update imports
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import uuid
from config import DB_CONFIG

auth_blueprint = Blueprint('auth', __name__)
active_sessions = {}

# Use the database configuration from config.py
db_config = DB_CONFIG

# Add 27 more countries with flags to the dictionary
countries_with_flags = {
    "USA": "🇺🇸",
    "Canada": "🇨🇦",
    "United Kingdom": "🇬🇧",
    "Germany": "🇩🇪",
    "France": "🇫🇷",
    "Australia": "🇦🇺",
    "Japan": "🇯🇵",
    "India": "🇮🇳",
    "Brazil": "🇧🇷",
    "Mexico": "🇲🇽",
    "China": "🇨🇳",
    "Russia": "🇷🇺",
    "South Korea": "🇰🇷",
    "Italy": "🇮🇹",
    "Spain": "🇪🇸",
    "Netherlands": "🇳🇱",
    "Sweden": "🇸🇪",
    "Norway": "🇳🇴",
    "Denmark": "🇩🇰",
    "Finland": "🇫🇮",
    "Switzerland": "🇨🇭",
    "Austria": "🇦🇹",
    "Belgium": "🇧🇪",
    "Greece": "🇬🇷",
    "Portugal": "🇵🇹",
    "Ireland": "🇮🇪",
    "New Zealand": "🇳🇿",
}

# Login route
@auth_blueprint.route('/login', methods=['POST'])
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
@auth_blueprint.route('/signup', methods=['POST'])
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
@auth_blueprint.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        # Remove the session data from the active_sessions dictionary
        active_sessions.pop(session_id, None)

        # Clear the session data
        session.clear()

    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Profile route
@auth_blueprint.route('/profile')
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

# Update Profile route
@auth_blueprint.route('/update_profile', methods=['POST'])
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
