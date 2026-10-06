from flask import Blueprint

characters = Blueprint("characters", __name__, url_prefix="/characters")
from . import routes
