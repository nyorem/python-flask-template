from flask import g, session
import pytest

def test_index(client):
    rv = client.get("/")
    assert b"Index" in rv.data

def test_login(client, auth):
    assert client.get("/auth/login/").status_code == 200
    response = auth.login()

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.username == "test"
