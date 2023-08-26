from flask import Flask, render_template, jsonify


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

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/basket')
def basket():
    return render_template('basket.html')

if __name__ == '__main__':
    app.run(debug=True)
