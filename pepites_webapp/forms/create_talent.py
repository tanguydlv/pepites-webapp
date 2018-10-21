from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, Length

from pepites_webapp import conf


class CreateTalentForm(FlaskForm):
    title = StringField('Titre',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    description = TextAreaField('Description',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    categorie = SelectField(
        'Categorie',
        choices=[('Bricolage', 'bricolage'), ('Culinaire', 'culinaire'), ('Sport', 'sport')],
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    nb_participant = StringField('Nombre de participants max',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    nb_session = SelectField(
        'Nombre de sessions',
        choices=[('1', '1'), ('2', '2'), ('3', '3')],
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    lieu = StringField('Lieu',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    prenom = StringField('Prenom',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    nom = StringField('Nom',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
    numero = StringField('Numero',
        validators=[
            InputRequired(),
            DataRequired(),
        ]
    )
