from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    username = StringField("Your user name.", validators=[Required])
    password = PasswordField("Your user name.", validators=[Required])
    submit = SubmitField("SIGN IN")

