# import "packages" from flask
from __init__ import app
from flask import Flask, render_template

# create a Flask instance
# app = Flask(__name__)

# blueprint importing
from routes.misc import app_misc
from routes.event_routes import app_events
from flask import render_template
from __init__ import app
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api
from content import app_content

app.register_blueprint(app_crud)
# app.register_blueprint(app_crud_api)

# blueprint registration
app.register_blueprint(app_misc)
app.register_blueprint(app_events)
app.register_blueprint(app_content)

# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/internships-and-work')
def internwork():
    return render_template('internandwork.html')

@app.route('/industry-sectors/')
def industry():
    return render_template("CTE/industry-sectors/industrysectors.html")

@app.route('/authorize')
def authorize():
    return render_template("authorize.html")


@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/CTE')
def CTE():
    return render_template("CTE/info-pages/CTE.html")

@app.route('/calendar/')
def calendar():
    return render_template("calendar.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
