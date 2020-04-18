from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager
from applications.config import MEDIA_ACTOR_ID


class ActorForm(FlaskForm):
    mediatypes = dbmanager.get_type_name_list_by_id(MEDIA_ACTOR_ID)
    media_choices = []
    for m in mediatypes:
        media_choices.append((m["id"], m["name"]))

    sex_choices = ((0, "Male"), (1, "Female"))

    name = StringField("The name of the Actor.", validators=[DataRequired(), Length(max=255)])
    country = StringField("The nation of the Actor.", validators=[DataRequired(), Length(max=255)])
    sex = RadioField("Select the sex of Actor.", validators=[DataRequired()], choices=sex_choices, coerce=int)
    types = SelectMultipleField("Select the type of Actor.", validators=[DataRequired()], choices=media_choices, coerce=int)
    description = StringField("The description of the Actor.", validators=[Length(max=500)])
    thumb = FileField("Upload file and store image fele into db.")
    thumb_path = StringField("The file path or url of the actor thumb.", validators=[Length(max=255)])

    def validate(self):
        super(ActorForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Media type can not be empty.")
            return False

        if self.country.data.strip() == "":
            self.country.errors.append("Media type can not be empty.")
            return False

        if self.sex.data.strip() == "":
            self.sex.errors.append("Media type can not be empty.")
            return False

        if self.types.data.strip() == "":
            self.types.errors.append("Media type can not be empty.")
            return False

        return True
