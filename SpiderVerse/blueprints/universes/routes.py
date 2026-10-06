from flask import render_template
from . import universes
from models.models import Universe

@universes.route("/")
def all_universes():
    universes_list = Universe.query.all()
    return render_template("universes/universes.html", universes=universes_list)

@universes.route("/<int:id>")
def universe_detail(id):
    universe = Universe.query.get_or_404(id)
    return render_template("universes/universe_detail.html", universe=universe)
