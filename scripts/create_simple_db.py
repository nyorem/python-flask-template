#! /usr/bin/env python3

import sys
sys.path.append(".")

from app import db, User, Post

# db.drop_all()
db.create_all()

user = User(username="hello")
user.set_password("lol")

post = Post(title="Hello", contents="world")
user.posts.append(post)

db.session.add(post)
db.session.add(user)
db.session.commit()
