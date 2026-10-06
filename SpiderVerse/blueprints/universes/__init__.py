from flask import Blueprint

universes = Blueprint("universes", __name__, url_prefix="/universes")
from . import routes
