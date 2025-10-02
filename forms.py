# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length


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
