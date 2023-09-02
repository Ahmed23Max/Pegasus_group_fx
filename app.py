from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'In9$]~3raxeG%L"7toNZwnuS:0D$?aq%{8+^R}(~<Xh3*P}.nmB4|fixQVwQ]:B'  # Replace with a strong secret key

# Your database configuration
db_config = {
    'dbname': 'pegasus_g8fn',
    'user': 'pegasus_g8fn_user',
    'password': '11BVk9h5u7os4mCxD8dMNhMpSB4sivyv',
    'host': 'dpg-cjlngg8cfp5c739tetpg-a.oregon-postgres.render.com'
}

# Route to serve the checkout page
@app.route('/checkout')
def checkout():
    selected_amount = request.args.get('amount', type=int)
    selected_description = request.args.get('description')
    return render_template('checkout.html', selected_amount=selected_amount,selected_description = selected_description )

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
                return jsonify({"message": "Login successful!"}), 200
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
    flash('You have been logged out.', 'success')
    return redirect(url_for('checkout'))  # Redirect to the /checkout page


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/guaranteed-pass')
def guaranteed_pass():
    return render_template('guaranteed_pass.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')



if __name__ == '__main__':
    app.run(debug=True)
