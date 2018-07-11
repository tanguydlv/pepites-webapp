import uuid
import datetime

from pepites_webapp import db, conf


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    has_confirmed_email = db.Column(db.Boolean, nullable=False, default=False)
    last_login_succeed_at = db.Column(db.DateTime, nullable=True)
    last_login_failed_at = db.Column(db.DateTime, nullable=True)
    num_login_failed = db.Column(db.Integer, default=0)
    is_administrator = db.Column(db.Boolean, nullable=False, default=False)


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.has_confirmed_email

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class AccountConfirmationCode(db.Model):
    __tablename__ = 'account_confirmation_codes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    code = db.Column(
        db.String,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        unique=True,
        index=True,
    )
    expire_at = db.Column(
        db.DateTime,
        default=lambda: datetime.datetime.utcnow() + conf.ACTIVATION_CODE_LIFETIME,
        nullable=False,
    )
    activated_at = db.Column(
        db.DateTime,
    )

    user = db.relationship(User, backref='activation_codes', lazy=True)

    @property
    def has_expired(self):
        return not self.is_active or datetime.datetime.utcnow() > self.expire_at

    @classmethod
    def generate_for_user(cls, user):
        '''Generate a new activation code for user and invalidate all the existing ones

        Args:
            * user: User, user model already in db
        '''
        for old_code in user.activation_codes:
            old_code.is_active = False
        code = cls(user_id=user.id)
        db.session.add(code)
        db.session.commit()
        return code
