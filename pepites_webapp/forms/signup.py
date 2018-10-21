from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, Length, Optional
from flask import flash

from pepites_webapp import conf
from pepites_webapp.misc import MAIL_BLACKLIST
import re


class SignupForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            InputRequired(),
            DataRequired(),
            Email(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            DataRequired(),
            Length(
                min=conf.MIN_PASSWORD_LEN,
                max=conf.MAX_PASSWORD_LEN,
                message='Password must be at least %(min)d '
                        'and at most %(max)d characters long.'
            ),
            EqualTo(
                'password_confirmation',
                message='Password must be equal to Password Confirmation'
            )
        ]
    )
    password_confirmation = PasswordField(
        'Password Confirmation',
        validators=[
            InputRequired(),
            DataRequired()
        ]
    )
    access_code = StringField(
        'Code de connexion',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )

    def validate_email(form, field):
        domain = field.data.split('@')[-1].strip().lower()
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if domain in MAIL_BLACKLIST:
            flash('Your email is invalid. Domain not allowed.', 'error')
            raise ValidationError(
                f'Your email is invalid. Domain {domain} not allowed.')
        if not re.match(pattern, field.data):
            flash('Your email is invalid. Format error.', 'error')
            raise ValidationError(
                f'Your email is invalid. Email {field.data} invalid.')
