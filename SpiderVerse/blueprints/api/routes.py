from flask import jsonify, request
from . import api
from models.conn import db
from models.models import Character, Movie, Universe
from auth_utils import admin_api_required

def error(message, status=400):
    return jsonify({"error": message}), status


@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.order_by(Character.name).all()
    return jsonify([c.to_dict() for c in characters])

@api.route("/characters/<int:id>", methods=["GET"])
def get_character(id):
    character = Character.query.get_or_404(id)
    return jsonify(character.to_dict())

@api.route("/characters", methods=["POST"])
@admin_api_required
def create_character():
    data = request.get_json(silent=True) or {}
    required = [
        "name", "alias", "description", "image", "gender",
        "role", "status", "actor", "type", "powers"
    ]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return error(f"Campi mancanti: {', '.join(missing)}")

    character = Character(
        name=data["name"],
        alias=data["alias"],
        description=data["description"],
        image=data["image"],
        gender=data["gender"],
        role=data["role"],
        status=data["status"],
        actor=data["actor"],
        type=data["type"],
        powers=data["powers"],
    )

    universe_ids = data.get("universe_ids", [])
    movie_ids = data.get("movie_ids", [])

    if not isinstance(universe_ids, list) or not isinstance(movie_ids, list):
        return error("universe_ids e movie_ids devono essere liste.")

    universes = Universe.query.filter(Universe.id.in_(universe_ids)).all() if universe_ids else []
    movies = Movie.query.filter(Movie.id.in_(movie_ids)).all() if movie_ids else []

    if len(universes) != len(set(universe_ids)):
        return error("Uno o più universe_ids non esistono.", 404)
    if len(movies) != len(set(movie_ids)):
        return error("Uno o più movie_ids non esistono.", 404)

    character.universes = universes
    character.movies = movies

    db.session.add(character)
    db.session.commit()

    return jsonify(character.to_dict()), 201

@api.route("/characters/<int:id>", methods=["PUT"])
@admin_api_required
def update_character(id):
    character = Character.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    fields = [
        "name", "alias", "description", "image", "gender",
        "role", "status", "actor", "type", "powers"
    ]

    for field in fields:
        if field in data:
            if not data[field]:
                return error(f"Il campo '{field}' non può essere vuoto.")
            setattr(character, field, data[field])

    if "universe_ids" in data:
        ids = data["universe_ids"]
        if not isinstance(ids, list):
            return error("universe_ids deve essere una lista.")
        universes = Universe.query.filter(Universe.id.in_(ids)).all()
        if len(universes) != len(set(ids)):
            return error("Uno o più universe_ids non esistono.", 404)
        character.universes = universes

    if "movie_ids" in data:
        ids = data["movie_ids"]
        if not isinstance(ids, list):
            return error("movie_ids deve essere una lista.")
        movies = Movie.query.filter(Movie.id.in_(ids)).all()
        if len(movies) != len(set(ids)):
            return error("Uno o più movie_ids non esistono.", 404)
        character.movies = movies

    db.session.commit()
    return jsonify(character.to_dict())

@api.route("/characters/<int:id>", methods=["DELETE"])
@admin_api_required
def delete_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Character eliminato correttamente."})

@api.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.order_by(Movie.year.desc()).all()
    return jsonify([m.to_dict() for m in movies])

@api.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return jsonify(movie.to_dict())

@api.route("/movies", methods=["POST"])
@admin_api_required
def create_movie():
    data = request.get_json(silent=True) or {}
    required = ["title", "year", "description", "poster", "director", "universe_id"]
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return error(f"Campi mancanti: {', '.join(missing)}")

    universe = Universe.query.get(data["universe_id"])
    if not universe:
        return error("L'universo indicato non esiste.", 404)

    movie = Movie(
        title=data["title"],
        year=int(data["year"]),
        description=data["description"],
        poster=data["poster"],
        duration=int(data["duration"]) if data.get("duration") else None,
        director=data["director"],
        universe=universe,
    )

    character_ids = data.get("character_ids", [])
    if not isinstance(character_ids, list):
        return error("character_ids deve essere una lista.")

    characters = Character.query.filter(Character.id.in_(character_ids)).all() if character_ids else []
    if len(characters) != len(set(character_ids)):
        return error("Uno o più character_ids non esistono.", 404)

    movie.characters = characters
    db.session.add(movie)
    db.session.commit()

    return jsonify(movie.to_dict()), 201

@api.route("/movies/<int:id>", methods=["PUT"])
@admin_api_required
def update_movie(id):
    movie = Movie.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    fields = ["title", "year", "description", "poster", "duration", "director"]
    for field in fields:
        if field in data:
            if data[field] in (None, "") and field != "duration":
                return error(f"Il campo '{field}' non può essere vuoto.")
            setattr(movie, field, data[field])

    if "universe_id" in data:
        universe = Universe.query.get(data["universe_id"])
        if not universe:
            return error("L'universo indicato non esiste.", 404)
        movie.universe = universe

    if "character_ids" in data:
        ids = data["character_ids"]
        if not isinstance(ids, list):
            return error("character_ids deve essere una lista.")
        characters = Character.query.filter(Character.id.in_(ids)).all()
        if len(characters) != len(set(ids)):
            return error("Uno o più character_ids non esistono.", 404)
        movie.characters = characters

    db.session.commit()
    return jsonify(movie.to_dict())

@api.route("/movies/<int:id>", methods=["DELETE"])
@admin_api_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Film eliminato correttamente."})


@api.route("/universes", methods=["GET"])
def get_universes():
    universes = Universe.query.order_by(Universe.name).all()
    return jsonify([u.to_dict() for u in universes])

@api.route("/universes/<int:id>", methods=["GET"])
def get_universe(id):
    universe = Universe.query.get_or_404(id)
    return jsonify(universe.to_dict())

@api.route("/universes", methods=["POST"])
@admin_api_required
def create_universe():
    data = request.get_json(silent=True) or {}
    required = ["name", "description", "image", "actor"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return error(f"Campi mancanti: {', '.join(missing)}")

    if Universe.query.filter_by(name=data["name"]).first():
        return error("Esiste già un universo con questo nome.", 409)

    universe = Universe(
        name=data["name"],
        description=data["description"],
        image=data["image"],
        actor=data["actor"],
    )

    db.session.add(universe)
    db.session.commit()
    return jsonify(universe.to_dict()), 201

@api.route("/universes/<int:id>", methods=["PUT"])
@admin_api_required
def update_universe(id):
    universe = Universe.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    for field in ["name", "description", "image", "actor"]:
        if field in data:
            if not data[field]:
                return error(f"Il campo '{field}' non può essere vuoto.")
            setattr(universe, field, data[field])

    db.session.commit()
    return jsonify(universe.to_dict())

@api.route("/universes/<int:id>", methods=["DELETE"])
@admin_api_required
def delete_universe(id):
    universe = Universe.query.get_or_404(id)
    db.session.delete(universe)
    db.session.commit()
    return jsonify({"message": "Universo eliminato correttamente."})

@api.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify([])

    characters = Character.query.filter(
        (Character.name.ilike(f"%{query}%")) |
        (Character.alias.ilike(f"%{query}%"))
    ).order_by(Character.name).all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "alias": c.alias,
            "image": c.image,
            "actor": c.actor
        }
        for c in characters
    ])
