from werkzeug.security import check_password_hash, generate_password_hash

from models.conn import db


character_universe = db.Table(
    "character_universe",
    db.Column("character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True),
    db.Column("universe_id", db.Integer, db.ForeignKey("universe.id"), primary_key=True),
)

character_movie = db.Table(
    "character_movie",
    db.Column("character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_authenticated(self):
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }


class Universe(db.Model):
    __tablename__ = "universe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    actor = db.Column(db.String(150), nullable=False)

    movies = db.relationship("Movie", back_populates="universe", cascade="all, delete-orphan")
    characters = db.relationship("Character", secondary=character_universe, back_populates="universes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "actor": self.actor,
            "movies": [{"id": m.id, "title": m.title} for m in self.movies],
            "characters": [{"id": c.id, "name": c.name} for c in self.characters],
        }


class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    director = db.Column(db.String(150), nullable=False)

    universe_id = db.Column(db.Integer, db.ForeignKey("universe.id"), nullable=False)
    universe = db.relationship("Universe", back_populates="movies")
    characters = db.relationship("Character", secondary=character_movie, back_populates="movies")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "description": self.description,
            "poster": self.poster,
            "duration": self.duration,
            "director": self.director,
            "universe": {"id": self.universe.id, "name": self.universe.name} if self.universe else None,
            "characters": [{"id": c.id, "name": c.name} for c in self.characters],
        }


class Character(db.Model):
    __tablename__ = "character"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    actor = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    powers = db.Column(db.Text, nullable=False)

    universes = db.relationship("Universe", secondary=character_universe, back_populates="characters")
    movies = db.relationship("Movie", secondary=character_movie, back_populates="characters")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "alias": self.alias,
            "description": self.description,
            "image": self.image,
            "gender": self.gender,
            "role": self.role,
            "status": self.status,
            "actor": self.actor,
            "type": self.type,
            "powers": self.powers,
            "universes": [{"id": u.id, "name": u.name} for u in self.universes],
            "movies": [{"id": m.id, "title": m.title} for m in self.movies],
        }


CharacterUniverse = character_universe
CharacterMovie = character_movie
