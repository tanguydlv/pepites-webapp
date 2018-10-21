from datetime import datetime

from flask import render_template, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from pepites_webapp.utils import url_for
from pepites_webapp import app, forms, bcrypt, conf, db
from pepites_webapp.models import User


@app.route('/create_talent', methods=['GET'])
def create_talent_page():
    form = forms.CreateTalentForm()
    return render_template(
        "create_talent.html",
        form=form
    )


@app.route('/create_talent', methods=['POST'])
def create_talent_post():
    form = forms.CreateTalentForm()
    if form.validate_on_submit():
        flash('Error while logging in.', 'error')
    else:
        flash('Error while logging in.', 'error')
        return render_template(
            'create_talent.html',
            form=form,
            errors=form.errors
        )
