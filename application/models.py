from application import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

class UserModel(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) #can't change to user_id, it will crash the UserMixin
    given_name = db.Column(db.String(64))
    family_name = db.Column(db.String(64), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    identifier_system = db.Column(db.String(), nullable=True)
    identifier_value = db.Column(db.String(64), nullable=True)
    oauth_server = db.Column(db.String(64))
    patient_id = db.Column(db.Integer)
    email = db.Column(db.String(64), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)


    def __init__(self, given_name, family_name, date_of_birth, identifier_system, identifier_value, oauth_server, patient_id, email, password):
        self.given_name = given_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.identifier_system = identifier_system
        self.identifier_value = identifier_value
        self.oauth_server = oauth_server
        self.patient_id = patient_id
        self.email = email
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Email: {self.email}, given_name: {self.given_name}"
