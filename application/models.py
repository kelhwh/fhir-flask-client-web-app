from application import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)

class UserModel(db.Model, UserMixin):
    """docstring for UserModel."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date)
    insurance_id = db.Column(db.String(64))


    def __init__(self, first_name, last_name, date_of_birth, insurance_id, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.insurance_id = insurance_id
        self.email = email
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Email: {self.email}, First_name: {self.first_name}"
