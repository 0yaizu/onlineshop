# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, length, EqualTo
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
  username = StringField(
    "User Name",
    validators=[
      DataRequired(message="User Name is required."),
      length(max=64, message="User Name should be input within 64 characters."),
    ],
  )
  password = PasswordField(
    "Password",
    validators=[
      DataRequired(message="Password is required."),
    ],
  )
  submit = SubmitField("Login")

  def copy_from(self, user):
    self.username.data = user.username
    self.password.data = user.password

  def copy_to(self, user):
    user.username = self.username.data
    user.password = self.password.data

class LogoutForm(FlaskForm):
  submit = SubmitField("Logout")

class SignupForm(FlaskForm):
	username = StringField(
		"User Name",
		validators = [
		DataRequired(message="User Name is required."),
		length(max=64, message="User Name should be input within 64 characters."),
		],
	)
	password = PasswordField(
		"Password",
		validators = [
		DataRequired(message="Password is required."),
		],
	)
	confirmed_password = PasswordField(
		"Confirm Password",
		validators=[
		DataRequired(message="Confirmed Password is required."),
		EqualTo("password", message="Passwords must match")
		],
	)
	submit = SubmitField("Sign Up")

	def copy_from(self, user):
		self.username.data = user.username
		self.password.data = user.password
		self.confirmed_password.data = user.password

	def copy_to(self, user):
		user.username = self.username.data
		user.password = self.password.data

class AddItemForm(FlaskForm):
	item_name = StringField(
		"Item Name",
		validators = [
			DataRequired(message="Item Name is required."),
		],
	)
	price = IntegerField(
		"Price",
		validators = [
			DataRequired(message="Price is required."),
		],
	)
	file = FileField(
		"File",
  	validators=[
			FileRequired(message="Image File is required."),
 			FileAllowed(("png","jpg","jpeg","gif","webp"), message="Allowed types: png, jpg, jpeg, gif, webp"),
		],
	)
	submit = SubmitField("Add Item")

	def copy_from(self, item):
		self.item_name.data = item.item_name
		self.price.data = item.price

	def copy_to(self, item):
		item.item_name = self.item_name.data
		item.price = self.price.data

class ShoppingForm(FlaskForm):
	item_name = StringField(
		"Item Name",
		validators = [
			DataRequired(message="Item Name is required."),
		],
	)
	submit = SubmitField("Search")

	def copy_from(self, item):
		self.item_name.data = item.item_name

	def copy_to(self, item):
		item.item_name = self.item_name.data