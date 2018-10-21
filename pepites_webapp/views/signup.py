from datetime import datetime

from flask import render_template, redirect, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from pepites_webapp.utils import url_for
from pepites_webapp import app, forms, bcrypt, conf, db
from pepites_webapp.models import User


@app.route('/signup', methods=['GET'])
def signup_page():
    form = forms.SignupForm()
    return render_template(
        "signup.html",
        form=form,
        login=False
    )


@app.route('/signup', methods=['POST'])
def signup_post():
    form = forms.SignupForm()
    now = datetime.utcnow()

    if not form.validate_on_submit():
        return render_template(
            "signup.html",
            form=form,
            login=False,
            errors=form.errors
        )

    email = form.email.data.strip().lower()
    user = User.query.filter_by(email=email).first()

    # Check if email is already registered
    if user is not None:
        app.logger.warning(
            f'Someone tried to signup with {email} which is already registered.'
        )
        flash('Email address already registered. Please login!', 'warning')
        return render_template(
            'signup.html',
            form=form,
            errors={'email': ['This email address is already registered.']}
        )

    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user = User(
        email=email,
        hashed_password=hashed_password.decode('utf-8'),
        created_at=now,
        has_confirmed_email=True,
        is_administrator=False
    )
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login_page'))
