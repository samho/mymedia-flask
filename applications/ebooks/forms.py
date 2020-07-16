from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager
from applications.config import MEDIA_EBOOK_ID, EBOOK_WRITER_ID


class eBookForm(FlaskForm):

    is_not_edited = True

    mediatypes = dbmanager.get_type_name_list_by_id(MEDIA_EBOOK_ID)
    media_choices = []
    for m in mediatypes:
        media_choices.append((m["id"], m["name"]))

    storages_choices = []
    storages = dbmanager.find_all_storages()
    for s in storages:
        storages_choices.append((s.id, s.name))

    name = StringField("The name of the eBook.", validators=[DataRequired(), Length(max=255)])
    actors = StringField("The writer of the eBook.", validators=[DataRequired(), Length(max=100)])
    types = SelectMultipleField("Select the type of the eBook.", choices=media_choices, coerce=int)
    storage = SelectField("Select the storage of the eBook.", validators=[DataRequired()], choices=storages_choices, coerce=int)
    storage_path = StringField("The file path of the ebook in storage.", validators=[DataRequired(), Length(max=255)])

    def validate(self):
        super(eBookForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("eBook name can not be empty.")
            return False

        if self.storage_path.data.strip() == "":
            self.storage_path.errors.append("The path in storage for movie can not be empty.")
            return False

        return True

    def set_is_not_edit(self, is_edit):
        self.is_not_edited = is_edit
