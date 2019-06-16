from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    username = StringField("Your user name.")
    password = PasswordField("Your user name.")
    submit = SubmitField("SIGN IN")

