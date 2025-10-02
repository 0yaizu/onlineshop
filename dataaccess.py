# dataaccess.py
import sqlite3
from models import User, Item, Order

DB_PATH = "instance/database.db"

def get_connection(autocommit=False):
	con = sqlite3.connect(DB_PATH)
	con.row_factory = sqlite3.Row
	con.execute("PRAGMA foreign_keys = ON")
	if autocommit:
		con.isolation_level = None
	return con

# ---------- Users ----------
def auth(username, password):
	query = "SELECT * FROM users WHERE username = ? AND password = ?"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (username, password))
		row = cur.fetchone()
		if not row:
			return None
		user = User()
		user.id = row["id"]
		user.username = row["username"]
		user.password = row["password"]
		return user
	finally:
		con.close()

def add_user(user):
	query = "INSERT INTO users (username, password) VALUES (?, ?)"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (user.username, user.password))
		user.id = cur.lastrowid
		con.commit()
		return user
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()
  
def search_users():
	query = "SELECT * FROM users"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query)
		rows = cur.fetchall()
		users = []
		for row in rows:
			u = User()
			u.id = row["id"]
			u.username = row["username"]
			u.password = row["password"]
			users.append(u)
		return users
	finally:
		con.close()

def search_user_by_id(id):
	query = "SELECT * FROM users WHERE id = ?"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (id,))
		row = cur.fetchone()
		if not row:
			return None
		u = User()
		u.id = row["id"]
		u.username = row["username"]
		u.password = row["password"]
		return u
	finally:
		con.close()

def search_user(username):
	query = "SELECT * FROM users WHERE username = ?"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (username,))
		row = cur.fetchone()
		if not row:
			return None
		u = User()
		u.id = row["id"]
		u.username = row["username"]
		u.password = row["password"]
		return u
	finally:
		con.close()

def edit_user(user):
	query = "UPDATE users SET username = ?, password = ? WHERE id = ?"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (user.username, user.password, user.id))
		con.commit()
		return user
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

def remove_user(user):
	query = "DELETE FROM users WHERE id = ?"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (user.id,))
		con.commit()
		return None
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()


def search_items_by_owner_id(owner_id):
	query = """
		SELECT items.id, items.owner_id, users.username AS owner_name, items.item_name, items.price
		FROM items, users
		WHERE items.owner_id = ?
		AND items.owner_id = users.id
	"""
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (owner_id,))
		res = cur.fetchall()
		item_list = []
		for r in res:
			item = Item()
			item.id = r["id"]
			item.owner_id = r["owner_id"]
			item.owner_name = r["owner_name"]
			item.item_name = r["item_name"]
			item.price = r["price"]
			item_list.append(item)
		return item_list
	finally:
		con.close()

def search_items_by_item_name(item_name):
	query = """
	SELECT items.id, items.owner_id, users.username AS owner_name,
	items.item_name, items.price
	FROM items, users
	WHERE item_name LIKE ?
	AND items.owner_id = users.id
	"""
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, ("%" + item_name + "%",))
		res = cur.fetchall()
		item_list = []
		for r in res:
			item = Item()
			item.id = r["id"]
			item.owner_id = r["owner_id"]
			item.owner_name = r["owner_name"]
			item.item_name = r["item_name"]
			item.price = r["price"]
			item_list.append(item)
		return item_list
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

# ---------- Items ----------
def search_items():
	query = """
		SELECT items.id, items.owner_id, users.username AS owner_name, items.item_name, items.price
		FROM items, users
		WHERE users.id = items.owner_id
	"""
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query)
		rows = cur.fetchall()
		items = []
		for row in rows:
			it = Item()
			it.id = row["id"]
			it.owner_id = row["owner_id"]
			it.owner_name = row["owner_name"]
			it.item_name = row["item_name"]
			it.price = row["price"]
			items.append(it)
		return items
	finally:
		con.close()

def search_item_by_id(id):
	query = """
		SELECT items.id, items.owner_id, users.username AS owner_name, items.item_name, items.price
		FROM items, users
		WHERE items.id = ?
		AND users.id = items.owner_id
	"""
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (id,))
		row = cur.fetchone()
		if not row:
			return None
		it = Item()
		it.id = row["id"]
		it.owner_id = row["owner_id"]
		it.owner_name = row["owner_name"]
		it.item_name = row["item_name"]
		it.price = row["price"]
		return it
	finally:
		con.close()

def search_item(item_name):
	query = """
		SELECT items.id, items.owner_id, users.username AS owner_name, items.item_name, items.price
		FROM items, users
		WHERE item_name LIKE ?
		AND items.owner_id = users.id
	"""
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (f"%{item_name}%",))
		rows = cur.fetchall()
		items = []
		for row in rows:
			it = Item()
			it.id = row["id"]
			it.owner_id = row["owner_id"]
			it.owner_name = row["owner_name"]
			it.item_name = row["item_name"]
			it.price = row["price"]
			items.append(it)
			return items
	finally:
		con.close()

def add_item(item):
	query = """
	INSERT INTO items (owner_id, item_name, price) VALUES (?, ?, ?)
	"""
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (item.owner_id, item.item_name, item.price))
		item.id = cur.lastrowid
		con.commit()
		return item
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()
def edit_item(item):
	query = "UPDATE items SET owner_id = ?, item_name = ?, price = ? WHERE id = ?"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (item.owner_id, item.item_name, item.price, item.id))
		con.commit()
		return item
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()
 
def remove_item(item):
	query = "DELETE FROM items WHERE id = ?"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (item.id,))
		con.commit()
		return None
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

# ---------- Orders ----------
def search_orders():
	query = "SELECT * FROM orders"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query)
		rows = cur.fetchall()
		orders = []
		for row in rows:
			od = Order()
			od.id = row["id"]
			od.order_code = row["order_code"]
			od.user_id = row["user_id"]
			od.item_id = row["item_id"]
			od.quantity = row["quantity"]
			od.price = row["price"]
			orders.append(od)
		return orders
	finally:
		con.close()

def search_order_by_id(id):
	query = "SELECT * FROM orders WHERE id = ?"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (id,))
		row = cur.fetchone()
		if not row:
			return None
		od = Order()
		od.id = row["id"]
		od.order_code = row["order_code"]
		od.user_id = row["user_id"]
		od.item_id = row["item_id"]
		od.quantity = row["quantity"]
		od.price = row["price"]
		return od
	finally:
		con.close()

def search_order(order_code):
	query = "SELECT * FROM orders WHERE order_code = ?"
	con = get_connection()
	try:
		cur = con.cursor()
		cur.execute(query, (order_code,))
		rows = cur.fetchall()
		orders = []
		for row in rows:
			od = Order()
			od.id = row["id"]
			od.order_code = row["order_code"]
			od.user_id = row["user_id"]
			od.item_id = row["item_id"]
			od.quantity = row["quantity"]
			od.price = row["price"]
			orders.append(od)
		return orders
	finally:
		con.close()

def add_order(order_list):
	query = """
		INSERT INTO orders (order_code, user_id, item_id, quantity, price)
		VALUES (?, ?, ?, ?, ?)
	"""
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		for order in order_list:
			cur.execute(query, (order.order_code, order.user_id, order.item_id, order.quantity, order.price))
			order.id = cur.lastrowid
		con.commit()
		return order_list
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

def edit_order(order):
	query = """
		UPDATE orders
		SET order_code = ?, user_id = ?, item_id = ?, quantity = ?, price = ?
		WHERE id = ?
	"""
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (order.order_code, order.user_id, order.item_id, order.quantity, order.price, order.id))
		con.commit()
		return order
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

def remove_order(order):
	query = "DELETE FROM orders WHERE id = ?"
	con = get_connection(autocommit=False)
	try:
		cur = con.cursor()
		cur.execute(query, (order.id,))
		con.commit()
		return None
	except Exception:
		con.rollback()
		raise
	finally:
		con.close()

if __name__ == "__main__":
	print("== Users ==")
	print(auth("admin", "password"))
	print(search_users())
	print(search_user_by_id(1))
	print(search_user("user"))

	new_user = User()
	new_user.username = "student"
	new_user.password = "password"
	new_user = add_user(new_user)
	print(new_user)

	new_user.username = "student1"
	new_user.password = "password1"
	print(edit_user(new_user))
	print(remove_user(new_user))

	print("\n== Items ==")

	print(search_items())
	print(search_item_by_id(1))
	print(search_item("りんご"))

	new_item = Item()
	new_item.owner_id = 1
	new_item.item_name = "さんま"
	new_item.price = 300
	new_item = add_item(new_item)
	print(new_item)

	new_item.item_name = "さんま1"
	new_item.price = "400"
	print(edit_item(new_item))
	print(remove_item(new_item))

	print("\n== Orders ==")

	print(search_orders())
	print(search_order_by_id(1))
	print(search_order("20250815092401"))

	order1 = Order()
	order1.order_code = "20250815092401"
	order1.user_id = 2
	order1.item_id = 1
	order1.quantity = 1
	order1.price = 200

	order2 = Order()
	order2.order_code = "20250815092401"
	order2.user_id = 2
	order2.item_id = 2
	order2.quantity = 2
	order2.price = 300

	order_list = [order1, order2]
	print(add_order(order_list))

	target_order = search_order_by_id(2)
	print(target_order)
	target_order.order_code = "20250815093001"
	target_order.user_id = 2
	target_order.quantity = 5
	target_order.price = 500

	print(edit_order(target_order))
	print(remove_order(target_order))