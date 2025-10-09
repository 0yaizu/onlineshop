# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from forms import *
from models import *
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "onlineshop")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY", "onlineshop")

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

import dataaccess as da

@app.route("/", methods=["GET", "POST"])
def index():
	if not "username" in session:
		session["username"] = "student1"
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
  
		user = da.search_user(username)
		if not (user and check_password_hash(user.password, password)):
			flash("Username or Password is wrong.", category="danger")
			return redirect(url_for("login"))

		flash("You are now logged in.", category="success")
		return redirect(url_for("index"))

	return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
	form = LogoutForm()

	if form.validate_on_submit():
		session.pop("username", None)
		session.clear()
		flash("You are now logged out.", category="success")
		return redirect(url_for("index"))

	return render_template("logout.html", form=form)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)