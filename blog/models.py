from . import db
from werkzeug.security import generate_password_hash, check_password_hash

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

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "posts": dict([ (post.id, post.api_uri()) for post in self.posts ]),
            "uri": self.api_uri(),
        }

    def api_uri(self):
        return "/api/user/{}/".format(self.id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=False, nullable=False)
    contents = db.Column(db.String(200), index=True, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "contents": self.contents,
            "owner": self.user_id,
            "uri": self.api_uri(),
        }

    def api_uri(self):
        return "/api/post/{}/".format(self.id)
