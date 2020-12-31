from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length
from wtforms import ValidationError

from flask_login import current_user
from application.models import UserModel


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email('Please provide a valid email address.'),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()
        ]
    )
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    date_of_birth = DateField(
        'Date of Birth',
        format='%Y-%m-%d',
        validators=[InputRequired()]
    )
    insurance_id = StringField(
        'Insurance ID Number',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email('Please provide a valid email address'),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=8, max=64, message='Must be between %(min)d and %(max)d characters long.')
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            InputRequired(),
            EqualTo('password', message=('Password does not match, please try again.'))
        ]
    )
    submit = SubmitField('Register')

    def validate_email(self, field): #in-line validator, will be validated once validate_on_submit is called.
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('The email has been registered already.')
