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

        if user:
            self.username.errors.append("User is existed.")
            return False

        return True


class UserEditForm(FlaskForm):
    password = PasswordField("Your new password.", validators=[DataRequired()])
    password_confirm = PasswordField("Your new password again.", validators=[DataRequired()])

    def validate(self):
        super(UserEditForm, self).validate()

        if self.password.data.strip() == "":
            self.password.errors.append("New Password can not be empty.")
            return False

        if self.password_confirm.data.strip() == "":
            self.password_confirm.errors.append("Confirm Password can not be empty.")
            return False

        if not (self.password.data.strip() == self.password_confirm.data.strip()):
            self.password_confirm.errors.append("Confirm password is not equal the new password.")
            return False

        return True
