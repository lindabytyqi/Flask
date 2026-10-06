from flask import render_template
from . import main
from models.models import Universe, Movie, Character

@main.route("/")
def home():
    universes = Universe.query.all()
    movies = Movie.query.order_by(Movie.year.desc()).limit(6).all()
    characters = Character.query.order_by(Character.name).limit(8).all()
    return render_template(
        "index.html",
        universes=universes,
        movies=movies,
        characters=characters
    )
