# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from forms import *
from models import *
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "onlineshop")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY", "onlineshop")
# app.config["SESSION_COOKIE_SECURE"] = bool(int(os.environ.get("SESSION_COOKIE_SECURE", 1))) # HTTPS必須(本番環境にて有効化する)
app.config["SESSION_COOKIE_HTTPONLY"] = bool(int(os.environ.get("SESSION_COOKIE_HTTPONLY", 1))) # JSから参照不可
app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax") # CSRF経路を抑制

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

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		confirmed_password = form.confirmed_password.data

		user = da.search_user(username)
		if user:
			flash("This username is already used.", category="danger")
			return redirect(url_for("signup"))

		user = User()
		user.username = username
		user.password = generate_password_hash(password)
		user = da.add_user(user)

		flash("You are Sign Up.", category="success")
		return redirect(url_for("index"))

	return render_template("signup.html", form=form)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)