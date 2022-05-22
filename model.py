from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import app

# Define variable to define type of database (sqlite), and name and location of myDB.db
dbURI = 'sqlite:///model/myDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)

class Events(db.Model):

    eventID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    datetime = db.Column(db.String(19))
    description = db.Column(db.Text)

    # constructor of a Event object, initializes of instance variables within object
    def __init__(self, name, datetime, description):
        self.name = name
        self.datetime = datetime
        self.description = description

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Events(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Events table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "eventID": self.eventID,
            "name": self.name,
            "datetime": self.datetime,
            "description": self.description
        }

    # CRUD update: updates events name, description, etc
    # returns self
    def update(self, name, datetime="", description=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(datetime) > 0:
            self.datetime = datetime
        if len(description) > 0:
            self.description = description
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
        
def event_tester():
    print("--------------------------")
    print("Seed Data for Table: Events")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    u1 = Events(name='Event1', datetime='2020-03-02 15:00:00', description="This is a description for event 1 only!!!")
    u2 = Events(name='Event2', datetime='2022-04-17 08:30:00', description="This is a description for event 2 only!!!")
    u3 = Events(name='Event3', datetime='2022-12-01 22:00:00', description="This is a description for event 3 only!!!")
    table = [u1, u2, u3]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records exist, duplicate url, or error: {row.url}")

def event_printer():
    print("------------")
    print("Table: Events with SQL query")
    print("------------")
    result = db.session.execute('select * from events')
    print(result.keys())
    for row in result:
        print(row)

if __name__ == "__main__":
    event_tester()  #
    event_printer()