from flask import render_template
from pepites_webapp import app


@app.route("/home", methods=["GET"])
def home_page():
        return render_template(
            "home.html",
            logo_name="Pépites",
            navbar_color="#1D809F",
            login=False
        )
