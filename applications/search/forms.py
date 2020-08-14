from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager, logger


logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


class SearchForm(FlaskForm):

    name = StringField("Search Content ...", validators=[DataRequired(), Length(max=255)])

    def validate(self):
        super(SearchForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Search content connot be empty.")
            return False

        return True

