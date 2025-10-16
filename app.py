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
		return redirect(url_for("shopping", q=q))

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

def get_cart():
	cart = session.get("cart")
	if not isinstance(cart, dict):
		cart = {}
	return cart

def save_cart(cart: dict):
	cleaned = {}
	for k, v in cart.items():
		try:
			qty = int(v)
		except (TypeError, ValueError):
			continue
		if qty <= 0:
			continue
		cleaned[str(k)] = qty
	session["cart"] = cleaned
 
@app.route("/cart", methods=["GET"])
def cart():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = CheckOutForm()

	cart_dict = get_cart()

	items = []
	total = 0
	for sid, quantity in cart_dict.items():
		try:
			item_id = int(sid)
			quantity = int(quantity)
		except Exception:
			continue
		if quantity <= 0:
			continue

		it = da.search_item_by_id(item_id)
		if not it:
			continue

		it.quantity = quantity
		it.subtotal = it.price * quantity

		items.append(it)
		total += it.subtotal

	return render_template("cart.html", form=form, item_list=items, total=total)

@app.route("/cart/add", methods=["POST"])
def cart_add():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = AddToCartForm()

	if form.validate_on_submit():
		item_id = int(form.item_id.data)
		quantity = max(1, int(form.quantity.data))
		if not da.search_item_by_id(item_id):
			flash("Item not found.", "danger")
			return redirect(url_for("cart"))

		cart_dict = get_cart()
		cart_dict[str(item_id)] = cart_dict.get(str(item_id), 0) + quantity

		save_cart(cart_dict)
		flash("Added to cart.", "success")
		return redirect(url_for("cart"))
	flash("Failed to add item to cart.", "danger")
	return redirect(url_for("cart"))

@app.route("/cart/update", methods=["POST"])
def cart_update():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = UpdateCartForm()
 
	if form.validate_on_submit():
		item_id = int(form.item_id.data)
		quantity = int(form.quantity.data)
		cart_dict = get_cart()
		if quantity <= 0:
			cart_dict.pop(str(item_id), None)
		else:
			if not da.search_item_by_id(item_id):
				flash("Item not found.", "danger")
				return redirect(url_for("cart"))
			cart_dict[str(item_id)] = quantity

		save_cart(cart_dict)
		flash("Updated cart.", "info")
		return redirect(url_for("cart"))

	flash("Failed to update cart.", "danger")
	return redirect(url_for("cart"))

@app.route("/cart/remove", methods=["POST"])
def cart_remove():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))

	form = RemoveFromCartForm()

	if form.validate_on_submit():
		item_id = int(form.item_id.data)
		cart_dict = get_cart()
		cart_dict.pop(str(item_id), None)
		save_cart(cart_dict)
		flash("Removed from cart.", "warning")
		return redirect(url_for("cart"))

	flash("Failed to remove item.", "danger")
	return redirect(url_for("cart"))

def _new_order_code():
	now_utc = datetime.now(timezone.utc)
	now_local = now_utc.astimezone()
	ts = now_local.strftime("%Y%m%d_%H%M%S")
	rand6 = uuid4().hex[:6]
	order_code = ts + "_" + rand6
	return order_code

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))
	
	form = CheckOutForm()
	
	if form.validate_on_submit():
		cart_dict = get_cart()
		if not cart_dict:
			flash("Cart is empty.", "warning")
			return redirect(url_for("cart"))
		
		user = da.search_user(session["username"])
		if not user:
			flash("User not found.", "danger")
			return redirect(url_for("cart"))
		
		order_code = _new_order_code()
		order_list = []
		
		for sid, qty in cart_dict.items():
			try:
				item_id = int(sid)
				quantity = int(qty)
			except Exception:
				continue
			if quantity <= 0:
				continue
			
			item = da.search_item_by_id(item_id)
			if not item:
				continue
			
			od = Order()
			od.order_code = order_code
			od.user_id = user.id
			od.item_id = item_id
			od.quantity = quantity
			od.price = item.price
			order_list.append(od)
		
		if not order_list:
			flash("Cart items are no longer available.", "warning")
			save_cart({})
			return redirect(url_for("cart"))
		
		try:
			da.add_order(order_list)
		except Exception:
			app.logger.exception("checkout failed")
			flash("Failed to checkout due to server error.", "danger")
			return redirect(url_for("cart"))
		
		save_cart({})
		return redirect(url_for("checkout") + f"?order_code={order_code}")
	
	order_code = request.args.get("order_code")
	if not order_code:
		return redirect(url_for("cart"))
	
	user = da.search_user(session["username"])
	if not user:
		flash("User not found.", "danger")
		return redirect(url_for("shopping"))
	
	lines = da.search_order_lines(order_code, user_id=user.id)
	if not lines:
		flash("Order not found.", "warning")
		return redirect(url_for("shopping"))
	
	total = 0
	for ln in lines:
		ln["subtotal"] = ln["price"] * ln["quantity"]
		total += ln["subtotal"]
	
	return render_template("checkout.html", order_code=order_code, items=lines, total=total)

@app.route("/orders", methods=["GET"])
def orders():
	if "username" not in session:
		flash("Log in is required.", "danger")
		return redirect(url_for("login"))
	
	user = da.search_user(session["username"])
	if not user:
		flash("User not found.", "danger")
		return redirect(url_for("shopping"))
	
	# 該当ユーザーの注文行を取得
	rows = da.search_orders_by_user(user.id)
	
	# order_code ごとにまとめ、表示用情報を付与
	groups = {}  # order_code -> {"order_code":..., "lines":[...], "total":int}
	order_groups = []
	
	for od in rows:
		code = od.order_code
		if code not in groups:
			groups[code] = {"order_code": code, "lines": [], "total": 0}
			order_groups.append(groups[code])
		
		# 名称・画像・出品者名を表示に利用
		item = da.search_item_by_id(od.item_id)
		line = {
			"item_id": od.item_id,
			"item_name": item.item_name if item else f"#{od.item_id}",
			"owner_name": item.owner_name if item else "-",
			"file_name": item.file_name if item else None,
			"price": od.price,
			"quantity": od.quantity,
			"subtotal": od.price * od.quantity,
		}
		groups[code]["lines"].append(line)
		groups[code]["total"] += line["subtotal"]
	
	return render_template("orders.html", order_groups=order_groups)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)