# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, EqualTo


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