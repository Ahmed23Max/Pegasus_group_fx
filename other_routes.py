from flask import Blueprint, render_template

other_blueprint = Blueprint('other', __name__)

@other_blueprint.route('/')
def index():
    return render_template('home.html')

@other_blueprint.route('/about_us')
def about_us():
    return render_template('about_us.html')

@other_blueprint.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

