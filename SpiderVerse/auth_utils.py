from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for

from models.conn import db
from models.models import User


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_current_user() is None:
            flash("Effettua il login per accedere a questa pagina.", "error")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def admin_page_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if user is None:
            flash("Effettua il login per accedere a questa pagina.", "error")
            return redirect(url_for("auth.login", next=request.path))
        if not user.is_admin:
            return "Permessi amministratore richiesti.", 403
        return view(*args, **kwargs)
    return wrapped


def admin_api_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({"error": "Autenticazione richiesta."}), 401
        if not user.is_admin:
            return jsonify({"error": "Permessi amministratore richiesti."}), 403
        return view(*args, **kwargs)
    return wrapped
