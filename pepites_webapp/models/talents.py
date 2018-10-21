import uuid
import datetime

from pepites_webapp import db, conf


class Talent(db.Model):
    __tablename__ = 'talents'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    categorie = db.Column(db.String, nullable=True)
    nb_sessions = db.Column(db.Integer, default=1)
    nb_participants = db.Column(db.Integer, default=1)
    lieu = db.Column(db.String, nullable=True)
    user_owner_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False
    )
    forum_id = db.Column(
        db.Integer,
        db.ForeignKey(Forum.id),
        nullable=False
    )
