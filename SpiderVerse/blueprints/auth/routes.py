from flask import flash, redirect, render_template, request, session, url_for

from auth_utils import get_current_user, login_required
from models.conn import db
from models.models import User
from . import auth


@auth.route("/register", methods=["GET", "POST"])
def register():
    if get_current_user() is not None:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or len(password) < 8:
            flash("Compila tutti i campi. La password deve avere almeno 8 caratteri.", "error")
            return render_template("auth/register.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username o email già utilizzati.", "error")
            return render_template("auth/register.html")

        user = User(username=username, email=email, role="user")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registrazione completata. Ora puoi accedere.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user() is not None:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            flash("Accesso effettuato.", "success")
            return redirect(request.args.get("next") or url_for("main.home"))

        flash("Email o password non corretti.", "error")

    return render_template("auth/login.html")


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("Logout effettuato.", "success")
    return redirect(url_for("main.home"))


@auth.route("/profile")
@login_required
def profile():
    return render_template("auth/profile.html")
