from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager


class MediaTypeForm(FlaskForm):
    mediatypes = dbmanager.find_all_mediatypes()
    if mediatypes is None:
        mediatype_list = [("0", "Root")]
    else:
        mediatype_list = [("0", "Root")]
        for m in mediatypes:
            type = (m.id, m.name)
            mediatype_list.append(type)

    name = StringField("Your user name.", validators=[DataRequired(), Length(max=255)])
    parent = SelectField("Media Type List", choices=mediatype_list, coerce=int)

    def validate(self):
        super(MediaTypeForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Media type can not be empty.")
            return False

        return True
