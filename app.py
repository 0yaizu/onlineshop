# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import *
from models import *
import os
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import send_from_directory
from uuid import uuid4

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "onlineshop")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("WTF_CSRF_SECRET_KEY", "onlineshop")
app.config["SESSION_COOKIE_SECURE"] = bool(int(os.environ.get("SESSION_COOKIE_SECURE", 1))) # HTTPS必須(本番環境にて有効化する)
app.config["SESSION_COOKIE_HTTPONLY"] = bool(int(os.environ.get("SESSION_COOKIE_HTTPONLY", 1))) # JSから参照不可
app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax") # CSRF経路を抑制
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
print("app.config['UPLOAD_FOLDER']", app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

import dataaccess as da

@app.before_request
def check_session_timeout():
	SESSION_TIMEOUT = 30 * 60
	if "username" not in session:
		return

	now = datetime.now(timezone.utc)

	last_seen = session.get("last_seen")
	if last_seen:
		last_seen = datetime.fromisoformat(last_seen)
  
		diff_seconds = (now - last_seen).total_seconds()
		if diff_seconds > SESSION_TIMEOUT:
			session.clear()
			flash("Session timed out. Please log in again.", category="danger")
			return redirect(url_for("login"))

	session["last_seen"] = now.isoformat()

@app.route("/", methods=["GET", "POST"])
def index():
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

		session.clear()
		session.permanent = True
		session["username"] = user.username
		session["last_seen"] = datetime.now(timezone.utc).isoformat()
  
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

@app.route("/additem", methods=["GET", "POST"])
def additem():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = AddItemForm()

	if form.validate_on_submit():
		item = Item()
		form.copy_to(item)
		user = da.search_user(username=session["username"])
		item.owner_id = user.id

		file = form.file.data
		if not file or file.filename == "":
			flash("No file selected.", "danger")
			return redirect(url_for("additem"))
		if not ('.' in file.filename) and (file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']):
			flash("File type is not supported.", "danger")
			return redirect(url_for("additem"))

		original = secure_filename(file.filename)
		ext = original.rsplit('.', 1)[1].lower()
		unique_name = f"{uuid4().hex}.{ext}"
		os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
		save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
		file.save(save_path)

		item.file_name = unique_name
		item.file_type = ext
		da.add_item(item)

		flash("An item was added.", "info")
		return redirect(url_for("additem"))

	user = da.search_user(username=session["username"])
	item_list = da.search_items_by_owner_id(user.id)
	return render_template("additem.html", form=form, item_list=item_list)

@app.route("/shopping", methods=["GET", "POST"])
def shopping():
	if not "username" in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = ShoppingForm()
	item_list = None

	if form.validate_on_submit():
		q = (form.item_name.data or "").strip()
		return redirect(url_for("searchitem", q=q))

	q = (request.args.get("q") or "").strip()
	if q:
		item_list = da.search_item(q)
		form.item_name.data = q

	return render_template("shopping.html", form=form, item_list=item_list)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)

@app.route("/item/<int:item_id>", methods=["GET"])
def item_detail(item_id):
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))
	item = da.search_item_by_id(item_id)
	if item is None:
		flash("Item not found.", "danger")
		return redirect(url_for("searchitem"))
	return render_template("itemdetail.html", item=item)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)