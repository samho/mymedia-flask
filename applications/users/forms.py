from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager


class UserForm(FlaskForm):
    username = StringField("Your user name.", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Your password.", validators=[DataRequired()])

    def validate(self):
        super(UserForm, self).validate()

        if self.username.data.strip() == "":
            self.username.errors.append("User name can not be empty.")
            return False

        if self.password.data.strip() == "":
            self.password.errors.append("Passowrd can not be empty.")
            return False

        user = dbmanager.find_user_by_name(username=self.username.data)

        if not user:
            dbmanager.save_user(self.username.data, self.password.data)
            return True
        else:
            self.username.errors.append("User is existed.")
            return False



