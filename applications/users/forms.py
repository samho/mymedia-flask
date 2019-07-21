from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(Form):

    username = StringField("Your user name.", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Your user name.", validators=[DataRequired()])
    submit = SubmitField("Submit")
