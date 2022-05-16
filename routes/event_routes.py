"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required, current_user
from flask_restful import Api, Resource
import requests

from model import Events
from cruddy.model import Users
from cruddy.query import user_by_id

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_events = Blueprint('events', __name__,
                       url_prefix='/events',
                       template_folder='events/',
                       static_folder='static',
                       static_url_path='assets')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
# api = Api(app_events)

""" Application control for CRUD is main focus of this File, key features:
    1.) Event table queries
    2.) app routes (Blueprint)
    3.) API routes
    4.) API testing
"""

""" Users table queries"""


# Event/Events extraction from SQL
def events_all():
    """converts Events table into JSON list """
    return [item.read() for item in Events.query.all()]


def events_ilike(term):
    """filter Users table by term into JSON list """
    term = "%{}%".format(term)
    table = Events.query.filter((Events.name.ilike(term)) | (Events.description.ilike(term)))
    return [item.read() for item in table]


# User extraction from SQL
def event_by_id(eventid):
    """finds event in table matching userid """
    return Events.query.filter_by(eventID=eventid).first()


# User extraction from SQL
def event_by_name(name):
    """finds event in table matching url """
    return Events.query.filter_by(name=name).first()


""" app route section """


# Default URL
@app_events.route('/', methods=["GET", "POST"])
@login_required
def mainframe():
    """obtains all Events from table and loads Admin Form"""
    uo = user_by_id(current_user.userID)
    print(uo.email)
    if uo.email == "admin@admin.com":
        return render_template("event_edit.html", table=events_all())
    return render_template("entry.html")

# CRUD create/add
@app_events.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to event table"""
    if request.form:
        po = Events(
            request.form.get("name"),
            request.form.get("datetime"),
            request.form.get("description")
        )
        po.create()
    return render_template("event_edit.html", table=events_all())


# CRUD read
@app_events.route('/read/', methods=["POST"])
def read():
    """gets eventid from form and obtains corresponding data from events table"""
    table = []
    if request.form:
        eventid = request.form.get("eventid")
        po = event_by_id(eventid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("event_edit.html", table=table)


# CRUD update
@app_events.route('/update/', methods=["POST"])
def update():
    """gets eventid and name from form and filters/modifies the data from event table"""
    if request.form:
        eventid = request.form.get("eventid")
        name = request.form.get("name")
        po = event_by_id(eventid)
        if po is not None:
            po.update(name)
    return render_template("event_edit.html", table=events_all())


# CRUD delete
@app_events.route('/delete/', methods=["POST"])
def delete():
    """gets eventid from form delete corresponding record from event table"""
    if request.form:
        eventid = request.form.get("eventid")
        po = event_by_id(eventid)
        if po is not None:
            po.delete()
    return render_template("event_edit.html", table=events_all())


# # Search Form
# @app_events.route('/search/')
# def search():
#     return render_template("full_search.html")


#Search request and response
@app_events.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    output = events_ilike(term)
    # output.sort(key=lambda x: x["name"])
    response = make_response(jsonify(output), 200)
    return response


""" API routes section """

# class UsersAPI:
#     # class for create/post
#     class _Create(Resource):
#         def post(self, name, url, description, usertag):
#             po = Users(name, url, description, usertag)
#             person = po.create()
#             if person:
#                 return person.read()
#             return {'message': f'Processed {name}, either a format error or {url} is duplicate'}, 210

#     # class for read/get
#     class _Read(Resource):
#         def get(self):
#             return users_all()

#     # class for read/get
#     class _ReadILike(Resource):
#         def get(self, term):
#             return users_ilike(term)

#     # class for update/put
#     class _Update(Resource):
#         def put(self, url, name):
#             po = user_by_url(url)
#             if po is None:
#                 return {'message': f"{url} is not found"}, 210
#             po.update(name)
#             return po.read()

#     class _UpdateAll(Resource):
#         def put(self, url, name, description, usertag):
#             po = user_by_url(url)
#             if po is None:
#                 return {'message': f"{url} is not found"}, 210
#             po.update(name, description, usertag)
#             return po.read()

#     # class for delete
#     class _Delete(Resource):
#         def delete(self, userid):
#             po = user_by_id(userid)
#             if po is None:
#                 return {'message': f"{userid} is not found"}, 210
#             data = po.read()
#             po.delete()
#             return data

#     # building RESTapi resource
#     api.add_resource(_Create, '/create/<string:name>/<string:url>/<string:description>/<string:usertag>')
#     api.add_resource(_Read, '/read/')
#     api.add_resource(_ReadILike, '/read/ilike/<string:term>')
#     api.add_resource(_Update, '/update/<string:url>/<string:name>')
#     api.add_resource(_UpdateAll, '/update/<string:url>/<string:name>/<string:description>/<string:usertag>')
#     api.add_resource(_Delete, '/delete/<int:userid>')


# """ API testing section """


# def api_tester():
#     # local host URL for model
#     url = 'http://127.0.0.1:5000/mongus'

#     # test conditions
#     API = 0
#     METHOD = 1
#     tests = [
#         ['/create/Wilma Flintstone/wilma@bedrock.org/123wifli/0001112222', "post"],
#         ['/create/Fred Flintstone/fred@bedrock.org/123wifli/0001112222', "post"],
#         ['/read/', "get"],
#         ['/read/ilike/John', "get"],
#         ['/read/ilike/com', "get"],
#         ['/update/wilma@bedrock.org/Wilma S Flintstone/123wsfli/0001112229', "put"],
#         ['/update/wilma@bedrock.org/Wilma Slaghoople Flintstone', "put"],
#         ['/delete/4', "delete"],
#         ['/delete/5', "delete"],
#     ]

#     # loop through each test condition and provide feedback
#     for test in tests:
#         print()
#         print(f"({test[METHOD]}, {url + test[API]})")
#         if test[METHOD] == 'get':
#             response = requests.get(url + test[API])
#         elif test[METHOD] == 'post':
#             response = requests.post(url + test[API])
#         elif test[METHOD] == 'put':
#             response = requests.put(url + test[API])
#         elif test[METHOD] == 'delete':
#             response = requests.delete(url + test[API])
#         else:
#             print("unknown RESTapi method")
#             continue

#         print(response)
#         try:
#             print(response.json())
#         except:
#             print("unknown error")


# def api_printer():
#     print()
#     print("Users table")
#     for user in users_all():
#         print(user)


# # """validating api's requires server to be running"""
# # if __name__ == "__main__":
# #     api_tester()
# #     api_printer()
