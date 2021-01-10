from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length
from wtforms import ValidationError

from flask_login import current_user
from application.models import UserModel
import datetime
from wtforms.widgets import PasswordInput

class check_duplicate():
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field

        if not message:
            message = f'The {self.field.name} has been registerd already.'
        self.message = message

    def __call__(self, form, field):
        instance = self.model.query.filter(self.field == field.data).first()
        if instance:
            raise ValidationError(self.message)



class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email('Please provide a valid email address.'),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ],
        default='test@example.com'
    )
    password = StringField(
        'Password',
        validators=[
            InputRequired()
        ],
        widget=PasswordInput(hide_value=False), #for demo user
        default=123123123 #for demo user
    )
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    family_name = StringField(
        'Family Name',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ],
        default='Franecki195' #for demo user
    )
    date_of_birth = DateField(
        'Date of Birth',
        format='%Y-%m-%d',
        validators=[InputRequired()],
        default=datetime.datetime(1995,4,20) #for demo user
    )
    identifier_system = SelectField(
        'ID',
        choices=[
            ('http://hl7.org/fhir/sid/us-ssn', 'Social Security Number')
        ],
        validators=[
            InputRequired()
        ],
        default='http://hl7.org/fhir/sid/us-ssn' #for demo user
    )
    identifier_value = StringField(
        'ID Number',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ],
        render_kw = {"placeholder": "Your ID Number"},
        default='999-45-3776' #for demo user
    )
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email('Please provide a valid email address'),
            Length(max=64, message='Must be less than %(max)d characters long.'),
            check_duplicate(model=UserModel, field=UserModel.email)
        ],
        default='test@example.com' #for demo user
    )
    password = StringField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=8, max=64, message='Must be between %(min)d and %(max)d characters long.')
        ],
        widget=PasswordInput(hide_value=False), #for demo user
        default=123123123 #for demo user
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            InputRequired(),
            EqualTo('password', message=('Password does not match, please try again.'))
        ],
        widget=PasswordInput(hide_value=False), #for demo user
        default=123123123 #for demo user
    )
    submit = SubmitField('Register')
