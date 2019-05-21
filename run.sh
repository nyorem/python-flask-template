#! /usr/bin/env bash

source venv/bin/activate

export FLASK_ENV="development"
# Obtained with the following command: python -c 'import os; print(os.urandom(12).hex())'
export FLASK_SECRET_KEY="48610aee4c5aad2f8faec3f5"
flask run
