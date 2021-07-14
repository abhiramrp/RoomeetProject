import os
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

@app.route("/")
def index():
<<<<<<< HEAD
    return render_template("home.html")
=======
    return render_template("profile.html")
>>>>>>> b3a0a32cfe171b7764d9fb4c5571f46dbe11fc62

if __name__ == "__main__":
    app.secret_key = 'super secret key'

    app.debug = True
    app.run()

@app.route("/registration", methods=["GET","POST"])
def Registration():
    session.clear()
    

    if request.method == "POST":
        request.form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
<<<<<<< HEAD
        rpassword = request.form.get("rpassword")

    return render_template("registration.html")
=======
        rpassword = request.form.get("rpassword")
>>>>>>> b3a0a32cfe171b7764d9fb4c5571f46dbe11fc62
