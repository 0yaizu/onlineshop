# models.py
class User:
	def __init__(self):
		self.id = None
		self.username = None
		self.password = None
	def __repr__(self):
		return "<User %r>" % self.id

class Item:
	def __init__(self):
		self.id = None
		self.owner_id = None
		self.owner_name = None
		self.name = None
		self.price = None
		self.file_name = None
		self.file_type = None

	def __repr__(self):
		return "<Item %r>" % self.id

class Order:
	def __init__(self):
		self.id = None
		self.order_code = None
		self.user_id = None
		self.item_id = None
		self.quantity = None
		self.price = None
  
	def __repr__(self):
		return "<Order %r>" % self.id