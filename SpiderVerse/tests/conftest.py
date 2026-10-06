import pytest

from app import create_app
from models.conn import db
from models.models import Character, Movie, Universe, User


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()

        universe = Universe(
            name="Test Universe",
            description="Universo per i test.",
            image="raimi.webp",
            actor="Test Actor",
        )
        movie = Movie(
            title="Test Movie",
            year=2026,
            description="Film per i test.",
            poster="spiderman-2002.jpg",
            duration=120,
            director="Test Director",
            universe=universe,
        )
        character = Character(
            name="Test Spider",
            alias="Spider-Test",
            description="Personaggio per i test.",
            image="peter-tom.jpg",
            gender="Male",
            role="Hero",
            status="Active",
            actor="Test Actor",
            type="Human",
            powers="Testing",
        )
        character.universes.append(universe)
        character.movies.append(movie)

        admin = User(username="admin", email="admin@test.local", role="admin")
        admin.set_password("Admin123!")
        user = User(username="user", email="user@test.local", role="user")
        user.set_password("User123!")

        db.session.add_all([universe, movie, character, admin, user])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, email, password):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )
