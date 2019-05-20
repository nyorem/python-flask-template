from flask import Flask, render_template, abort, session

app = Flask(__name__)

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/logout/")
def logout():
    abort(404)

@app.route("/user/<int:user_id>/")
def user(user_id):
    abort(404)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
