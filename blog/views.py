from flask import Blueprint, render_template, abort, redirect, url_for, request, flash, g

from . import db
from .models import User, Post
from .auth import login_required, logout_required

bp = Blueprint("blog", __name__)

@bp.route("/users/")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

@bp.route("/user/<int:user_id>/")
def user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    return render_template("user.html", user=user)

@bp.route("/user/post/", defaults = { "post_id": None }, methods=["GET", "POST"])
@bp.route("/user/post/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post(post_id=None):
    user = g.user

    # New post
    if post_id is None:
        if request.method == "POST":
            form = request.form
            title = form["title"]
            contents = form["contents"]

            post = Post(title=title, contents=contents)
            user.posts.append(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.user", user_id=user.id))
        else:
            return render_template("post.html")

    # Update post

    # Check if post exists
    post = Post.query.get(post_id)
    if post is None:
        abort(404)

    # Check if author of the post if the user
    if post.user != user:
        abort(403)

    if request.method == "POST":
        # Update post
        form = request.form
        post.title = form["title"]
        post.contents = form["contents"]
        db.session.commit()

        return redirect(url_for("blog.user", user_id=user.id))

    # Display exisiting post for editing
    return render_template("post.html", title=post.title, contents=post.contents)

@bp.route("/remove/<int:post_id>/")
@login_required
def remove(post_id):
    # Check if post exists
    post = Post.query.get(post_id)
    if post is None:
        abort(404)

    # Check if logged in user is the author of the post
    user = post.user
    logged_user_id = g.user.id
    if logged_user_id != user.id:
        abort(403)

    # Remove the post from the database
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("blog.user", user_id=user.id))

@bp.route("/")
def index():
    return render_template("index.html")

