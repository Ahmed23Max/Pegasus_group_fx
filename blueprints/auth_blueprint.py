# auth_blueprint.py
from flask import Blueprint, request, session, jsonify
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)

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
