# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import *
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "onlineshop")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY", "onlineshop")

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

@app.route("/", methods=["GET", "POST"])
def index():
	username = None
	return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		flash("You are now logged in.", category="success")
		return redirect(url_for("index"))
	return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
	form = LogoutForm()

	if form.validate_on_submit():
		flash("You are now logged out.", category="success")
		return redirect(url_for("index"))

	return render_template("logout.html", form=form)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)