from flask import render_template
from pepites_webapp import app


@app.route("/", methods=["GET"])
def home_page():
        return render_template(
            "home.html",
            navbar_color='#1D809F',
        )
