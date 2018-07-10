from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

from . import conf


def make_app():
    app = Flask(__name__)
    app.secret_key = conf.FLASK_SECRET_KEY
    app.config['WTF_CSRF_SECRET_KEY'] = conf.WTF_CSRF_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = conf.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RECAPTCHA_PUBLIC_KEY'] = conf.RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = conf.RECAPTCHA_PRIVATE_KEY
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    return app


app = make_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

#from pepites_webapp.models import *
from pepites_webapp.views import *
from pepites_webapp.forms import *

@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.filter_by(id=int(user_id)).first()
    except:
        return None
    else:
        return user
