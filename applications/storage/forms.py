from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager, logger


logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


class StorageForm(FlaskForm):
    mediatypes = dbmanager.find_all_mediatypes()
    if mediatypes is None:
        mediatype_list = [("0", "Root")]
    else:
        mediatype_list = [("0", "Root")]
        for m in mediatypes:
            type = (m.id, m.name)
            mediatype_list.append(type)

    name = StringField("Your user name.", validators=[DataRequired(), Length(max=255)])
    mediatype = SelectField("Media Type List", coerce=int, choices=mediatype_list)
    size = StringField("Storage Size", validators=[DataRequired()])

    def validate(self):
        super(StorageForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Storage name can not be empty.")
            return False

        if self.size.data.strip() == "":
            self.size.errors.append("Storage size can not be empty.")
            return False

        try:
            s_size = float(self.size.data)
        except ValueError as e:
            self.size.errors.append("Storage size must be digital.")
            logger.error("The storage size is not digital.")
            return False

        return True

