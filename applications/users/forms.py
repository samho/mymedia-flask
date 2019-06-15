from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required


class UserForm(Form):

    username = StringField("Your user name.", validators=[Required])
    password = PasswordField("Your user name.", validators=[Required])
    submit = SubmitField("Submit")
