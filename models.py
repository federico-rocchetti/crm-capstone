import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from server import login_manager

db = SQLAlchemy()

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)

    contacts = db.relationship("Contact", backref = "contact", lazy = True)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    name = db.Column(db.String(40), nullable = False)
    contact_type = db.Column(db.String(40), nullable = False)
    email = db.Column(db.VARCHAR(60))
    work_phone = db.Column(db.Integer())
    mobile_phone = db.Column(db.Integer())
    address = db.Column(db.VARCHAR(60))
    company = db.Column(db.String(60))

    def __init__(self, user_id, name, contact_type, email, work_phone, mobile_phone, address, company):
        self.user_id = user_id
        self.name = name
        self.contact_type = contact_type
        self.email = email
        self.work_phone = work_phone
        self.mobile_phone = mobile_phone
        self.address = address
        self.company = company

class Note(db.Model):

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable = False)
    note = db.Column(db.Text(255), nullable = False)

    def __init__(self, contact_id, note):
        self.contact_id = contact_id
        self.note = note
    
def connect_to_db(flask_app):

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")

