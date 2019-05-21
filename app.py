from functools import wraps
from flask import Flask, render_template, abort, session, redirect, url_for, request, flash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# TODO: database for users, hashing for passwords
class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = [ User("nyorem", "lol") ]
def user_exists(username, password):
    for user in users:
        if user.username == username and user.password == password:
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username"):
            redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if user_exists(form["username"], form["password"]):
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

# TODO
@app.route("/user/<int:user_id>/")
# @login_required
def user(user_id):
    abort(404)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
