from flask import Blueprint, render_template

app_misc = Blueprint('misc', __name__,
                     url_prefix='/other/',
                     template_folder='templates/',
                     static_folder='static',
                     static_url_path='assets')

@app_misc.route('/')
def index():
    return render_template("index.html")

@app_misc.route('/calendar/')
def calendar():
    return render_template("testing/calendartest.html")