from flask import Flask
from flask_migrate import Migrate

from auth_utils import get_current_user
from config import Config
from models.conn import db

from blueprints.main import main
from blueprints.characters import characters
from blueprints.movies import movies
from blueprints.universes import universes
from blueprints.api import api
from blueprints.auth import auth
from blueprints.admin import admin


migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(characters)
    app.register_blueprint(movies)
    app.register_blueprint(universes)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    @app.context_processor
    def inject_current_user():
        return {"current_user": get_current_user()}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
