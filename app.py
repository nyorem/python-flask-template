#! /usr/bin/env python3

from functools import wraps
from flask import Flask, render_template, abort, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///table.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: {}>".format(self.username)

    @staticmethod
    def exists(username, password=None):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return False
        if password is None:
            return True
        return user.check_password(password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=False, nullable=False)
    contents = db.Column(db.String(200), index=True, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username"):
            redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username"):
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register/", methods=["GET", "POST"])
@already_logged_in
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
            return redirect(url_for("login"))
        else:
            flash("User already exists")
    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
@already_logged_in
def login():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        if User.exists(username, password):
            session["username"] = form["username"]
            return redirect(url_for("index"))
        else:
            flash("Wrong credentials")
    return render_template("login.html")

@app.route("/logout/")
@login_required
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/users/")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/user/<int:user_id>/")
def user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    posts = user.posts
    return render_template("user.html", user=user, posts=posts)

@app.route("/user/<int:user_id>/post/", methods=["GET", "POST"])
@login_required
def post(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)

    if request.method == "POST":
        form = request.form
        title = form["title"]
        contents = form["contents"]
        post = Post(title=title, contents=contents)
        user.posts.append(post)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("user", user_id=user.id))
    return render_template("post.html")

@app.route("/")
def index():
    username = session.get("username", None)
    user = None
    if username is not None:
        user = User.query.filter_by(username=username).first()
    return render_template("index.html", user=user)

@app.shell_context_processor
def make_shell_context():
    return { "db": db, "User": User, "Post": Post }

if __name__ == "__main__":
    app.run()
