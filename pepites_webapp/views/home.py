from flask import render_template, flash
from flask_login import login_required, current_user

from pepites_webapp import app


@app.route("/home", methods=["GET"])
@login_required
def home_page():
        flash('You must first validate your email.', 'warning')
        return render_template(
            "home.html",
            login=True
        )
