from flask import Blueprint

movies = Blueprint("movies", __name__, url_prefix="/movies")
from . import routes
