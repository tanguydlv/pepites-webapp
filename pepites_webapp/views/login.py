from datetime import datetime

from flask import render_template, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from pepites_webapp.utils import url_for
from pepites_webapp import app, forms, bcrypt, conf, db
from pepites_webapp.models import User


@app.route('/login', methods=['GET'])
def login_page():
    form = forms.LoginForm()
    return render_template(
        "login.html",
        form=form,
        logo_name="Pépites",
        navbar_color="#1D809F",
        login=False
    )


@app.route('/login', methods=['POST'])
def login_post():
    form = forms.LoginForm()
    if form.validate_on_submit():
        now = datetime.utcnow()

        # check if email is registered
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        if user is None:
            app.logger.warning(
                f'Someone tried to login with {email} which is not registred.'
            )
            return render_template(
                'login.html',
                form=form,
                errors={'email': ['Invalid email/password combination.']}
            )

        # check if user has confirmed his email
        if not user.has_confirmed_email:
            app.logger.warning(
                f'User {user.id} tried to login without having confirmed his email.'
            )
            flash('You must first validate your email.', 'warning')
            return redirect(url_for('login_page'))

        # check if user has not exceed maximum number of login attempts per 24h
        if user.num_login_failed >= conf.MAX_LOGIN_ATTEMPTS:
            if now < user.last_login_failed_at + conf.BAN_MAX_LOGIN_ATTEMPTS_DURATION:
                app.logger.warning(
                    f'User {user.id} has exceeded maximum number of login attemps.'
                )
                flash('You have exceeded your maximum number of login attempts.', 'error')
                return redirect(url_for('login_page'))
            else:
                app.logger.info(
                    f'Resetting number of login attemps to zero for user {user.id}.'
                )
                user.num_login_failed = 0
                db.session.add(user)
                db.session.commit()

        # check if password is correct
        password_ok = bcrypt.check_password_hash(
            user.hashed_password,
            form.password.data
        )
        if not password_ok:
            app.logger.warning(
                f'User {user.id} provided wrong password to login.'
            )
            user.num_login_failed += 1
            user.last_login_failed_at = now
            db.session.add(user)
            db.session.commit()
            return render_template(
                'login.html',
                form=form,
                errors={'email': ['Invalid email/password combination.']}
            )

        # write the user's id to the session
        if login_user(user):
            user.last_login_succeed_at = now
            user.num_login_failed = 0
            db.session.add(user)
            db.session.commit()
            flash('You are now logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error while logging in.', 'error')
            return render_template(
                'login.html',
                form=form
            )
    else:
        return render_template(
            'login.html',
            form=form,
            errors=form.errors
        )


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    app.logger.info(f'User {current_user.id} has logged out.')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index_page'))
