from flask import render_template
from pepites_webapp import app


@app.route("/", methods=["GET"])
def accueil_page():
        return render_template(
            "accueil.html",
            logo_name="Pépites",
            navbar_color="#1D809F",
            login=False
        )
