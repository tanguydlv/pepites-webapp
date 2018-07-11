from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Email, Length

from pepites_webapp import conf


class LoginForm(FlaskForm):
    email = StringField('Adresse mail',
        validators=[
            InputRequired(),
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Mot de passe',
        validators=[
            InputRequired(),
            DataRequired(),
            Length(
                min=conf.MIN_PASSWORD_LEN,
                max=conf.MAX_PASSWORD_LEN,
                message='Le mot de passe doit faire entre %(min)d '
                        'et %(max)d charactères.'
            )
        ]
    )
    recaptcha = RecaptchaField()
