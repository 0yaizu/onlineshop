# app.py
from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)
app.secret_key = "onlineshop"

@app.route("/", methods=["GET", "POST"])
def index():
	username = None
	return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
	username = None
	password = None
	if request.method == "POST":
		time.sleep(3)
		username = request.form.get("username")
		password = request.form.get("password")
		print(username)
		print(password)
		return redirect(url_for("index"))

	return render_template("login.html", username=username, password=password)

@app.route("/logout", methods=["GET", "POST"])
def logout():
	if request.method == "POST":
		return redirect(url_for("index"))
	return render_template("logout.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)