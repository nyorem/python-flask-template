import pytest
import tempfile
import os

from blog import create_app, db
from blog.models import User, Post

def init_db():
    db.create_all()

    user1 = User(username="test")
    user1.set_password("test")

    user2 = User(username="user2")
    user2.set_password("password2")

    post1 = Post(title="Post by user 1", contents="Contens from user 1", user=user1)
    post2 = Post(title="Post by user 2", contents="Contens from user 2", user=user2)

    db.session.add(user1, user2)
    db.session.add(post1, post2)

    db.session.commit()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login/",
            data={ "username": username, "password": password },
            follow_redirects=True,
        )

    def logout(self):
        return self._client.get("/auth/logout/", follow_redirects=True)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        "SECRET_KEY": "test",
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthActions(client)
