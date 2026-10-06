from flask import render_template
from . import movies
from models.models import Movie

@movies.route("/")
def all_movies():
    movies_list = Movie.query.order_by(Movie.year.desc()).all()
    return render_template("movies/movies.html", movies=movies_list)

@movies.route("/<int:id>")
def movie_detail(id):
    movie = Movie.query.get_or_404(id)
    return render_template("movies/movie_detail.html", movie=movie)
