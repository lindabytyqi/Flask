from flask import render_template
from . import characters
from models.models import Character

@characters.route("/")
def all_characters():
    characters_list = Character.query.order_by(Character.name).all()
    return render_template("characters/characters.html", characters=characters_list)

@characters.route("/<int:id>")
def character_detail(id):
    character = Character.query.get_or_404(id)
    return render_template("characters/character_detail.html", character=character)
