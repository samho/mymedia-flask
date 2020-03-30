from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from applications.utils import dbmanager


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired("Username needed.")])
    password = PasswordField("password", validators=[DataRequired("Password needed.")])

    def validate(self):
        super(LoginForm, self).validate()


        #if not check_validate:
        #    return False

        user = dbmanager.find_user_by_name(username=self.username.data)

        if not user:
            self.username.errors.append("Invalid username or password.")
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True

