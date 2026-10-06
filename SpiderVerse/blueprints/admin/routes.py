from flask import flash, redirect, render_template, url_for

from auth_utils import admin_page_required, get_current_user
from models.conn import db
from models.models import Character, Movie, Universe, User
from . import admin


@admin.route("/")
@admin_page_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        user_count=User.query.count(),
        universe_count=Universe.query.count(),
        movie_count=Movie.query.count(),
        character_count=Character.query.count(),
        users=User.query.order_by(User.username).all(),
    )


@admin.route("/users/<int:user_id>/toggle-role", methods=["POST"])
@admin_page_required
def toggle_role(user_id):
    current_user = get_current_user()
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Non puoi rimuovere il tuo ruolo amministratore mentre sei autenticato.", "error")
        return redirect(url_for("admin.dashboard"))

    user.role = "admin" if user.role != "admin" else "user"
    db.session.commit()
    flash(f"Ruolo di {user.username} aggiornato a {user.role}.", "success")
    return redirect(url_for("admin.dashboard"))
