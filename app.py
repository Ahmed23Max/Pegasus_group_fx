from flask import Flask, session, jsonify, render_template  # Add render_template import
from config import SECRET_KEY, DB_CONFIG
from auth_routes import auth_blueprint
from other_routes import other_blueprint
from stripe_routes import stripe_blueprint

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Use the database configuration from config.py
db_config = DB_CONFIG

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(other_blueprint, url_prefix='/other')
app.register_blueprint(stripe_blueprint, url_prefix='/stripe')

if __name__ == '__main__':
    app.run(debug=True)
