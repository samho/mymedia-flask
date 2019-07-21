from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager


class LoginForm(FlaskForm):
    username = StringField("Your user name.", validators=[DataRequired, Length(max=255)])
    password = PasswordField("Your user name.", validators=[DataRequired])

    def validate(self):
        #check_validate = super(LoginForm, self).validate()

        #if not check_validate:
        #    return False

        user = dbmanager.find_user_by_name(username=self.username.data)

        if not user:
            #self.username.errors.append("Invalid username or password.")
            return False

        if not self.user.check_password(self.password.data):
            #self.username.errors.append('Invalid username or password.')
            return False

        return True

