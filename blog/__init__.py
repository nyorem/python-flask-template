#! /usr/bin/env python3

import os
from flask import Flask, render_template, abort, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

import click
from flask.cli import with_appcontext

db = SQLAlchemy()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initializes the database."""
    db.create_all()
    click.echo("Database initialized")

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(app.instance_path, "table.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    if test_config is not None:
        app.config.from_mapping(test_config, silent=True)

    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)

    # Register blueprints
    from .views import bp as blog_bp
    app.register_blueprint(blog_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .rest import bp as rest_bp
    app.register_blueprint(rest_bp)

    return app

app = create_app()

from .models import User, Post

@app.shell_context_processor
def make_shell_context():
    return { "db": db, "User": User, "Post": Post }

if __name__ == "__main__":
    app.run()
