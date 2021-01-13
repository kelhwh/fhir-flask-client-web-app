from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms import ValidationError

from flask_login import current_user

class EditProfileForm(FlaskForm):
    city = StringField(
        'City',
        validators=[
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    state = StringField(
        'State',
        validators=[
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    postalcode = StringField(
        'Postal Code',
        validators=[
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    country = StringField(
        'Country',
        validators=[
            Length(max=64, message='Must be less than %(max)d characters long.')
        ]
    )
    submit = SubmitField('Confirm')
