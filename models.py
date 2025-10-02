# models.py
class User:
	def __init__(self):
		self.id = None
		self.username = None
		self.password = None
	def __repr__(self):
		return "<User %r>" % self.id