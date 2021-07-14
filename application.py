import os
import sqlite3

from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Home.html")


@app.route("/register", methods=["GET","POST"])
def register():
    session.clear()

    if request.method == "POST":
        request.form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        rpassword = request.form.get("rpassword")


