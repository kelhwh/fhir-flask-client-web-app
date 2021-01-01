from flask import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length
from wtforms import ValidationError

from flask_login import current_user
from application.models import UserModel

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
    family_name = StringField(
        'Family Name',
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
    identifier_system = SelectField(
        'ID',
        choices=[
            ('http://hl7.org/fhir/sid/us-ssn', 'Social Security Number')
        ],
        validators=[
            InputRequired()
        ]
    )
    identifier_value = StringField(
        'ID Number',
        validators=[
            InputRequired(),
            Length(max=64, message='Must be less than %(max)d characters long.')
        ],
        render_kw = {"placeholder": "Your ID Number"}
    )
    email = EmailField(
        'Email',
        validators=[
            InputRequired(),
            Email('Please provide a valid email address'),
            Length(max=64, message='Must be less than %(max)d characters long.'),
            check_duplicate(model=UserModel, field=UserModel.email)
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
