from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g

from . import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Loads the logged-in user if it exists
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# Decorator that prevents access to pages where login is required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

# Decorator that prevents access to pages where logout is required
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is not None:
            return redirect(url_for("blog.index"))
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/register/", methods=["GET", "POST"])
@logout_required
def register():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        if not User.exists(username):
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            flash("User {} already exists".format(username))

    return render_template("register.html")

@bp.route("/login/", methods=["GET", "POST"])
@logout_required
def login():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        if User.exists(username, password=password):
            user = User.query.filter_by(username=username).first()
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("blog.index"))
        else:
            flash("Wrong credentials")

    return render_template("login.html")

@bp.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for("blog.index"))

