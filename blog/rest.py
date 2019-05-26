from flask import Blueprint, jsonify

from .models import User, Post

bp = Blueprint("rest", __name__, url_prefix="/api")

# GET
@bp.route("/user/", defaults = {"user_id": None }, methods=["GET"])
@bp.route("/user/<int:user_id>/", methods=["GET"])
def user(user_id=None):
    if user_id is None:
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    user = User.query.get(user_id)
    if user is None:
        return jsonify({
            "error": "User with id {} not found".format(user_id)
        })
    else:
        return jsonify(user.serialize())

@bp.route("/post/", defaults = {"post_id": None }, methods=["GET"])
@bp.route("/post/<int:post_id>/", methods=["GET"])
def post(post_id=None):
    if post_id is None:
        posts = Post.query.all()
        return jsonify([post.serialize() for post in posts])

    post = Post.query.get(post_id)
    if post is None:
        return jsonify({
            "error": "Post with id {} not found".format(post_id)
        })
    else:
        return jsonify(post.serialize())
