# import "packages" from flask
from __init__ import app
from flask import Flask, render_template

# create a Flask instance
# app = Flask(__name__)

# blueprint importing
from routes.misc import app_misc
from routes.event_routes import app_events

# blueprint registration
app.register_blueprint(app_misc)
app.register_blueprint(app_events)

# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/industry-sectors/')
def industry():
    return render_template("CTE/industry-sectors/industrysectors.html")

# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
