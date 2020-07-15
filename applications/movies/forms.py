from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, FileField, SelectField
from wtforms.validators import DataRequired, Length
from applications.utils import dbmanager


class MovieAdultForm(FlaskForm):

    movie_type = 14
    is_not_edited = True
    actors_choices = []
    actors = dbmanager.find_actor_by_type(movie_type)
    for a in actors:
        actors_choices.append((a.id, a.name))

    storages_choices = []
    storages = dbmanager.find_all_storages()
    for s in storages:
        storages_choices.append((s.id, s.name))

    name = StringField("The name of the Movie.", validators=[DataRequired(), Length(max=255)])
    provider = StringField("The Provider of the Movie.", validators=[Length(max=255)])
    actors = SelectMultipleField("Select the Actor of the Movie.", validators=[DataRequired()], choices=actors_choices, coerce=int)
    storage = SelectField("Select the storage of the Movie.", validators=[DataRequired()], choices=storages_choices, coerce=int)
    storage_path = StringField("The file path of the movie in storage.", validators=[DataRequired(), Length(max=255)])
    cover = FileField("Upload cover file of the movie.")
    snapshots = FileField("Upload the snapshot files of the movie.")

    def validate(self):
        super(MovieAdultForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Movie name can not be empty.")
            return False

        if self.storage_path.data.strip() == "":
            self.storage_path.errors.append("The path in storage for movie can not be empty.")
            return False

        return True

    def set_is_not_edit(self, is_edit):
        self.is_not_edited = is_edit


class MovieRegularForm(FlaskForm):

    movie_type = 13
    is_not_edited = True
    actors_choices = []
    actors = dbmanager.find_actor_by_type(movie_type)
    for a in actors:
        actors_choices.append((a.id, a.name))

    storages_choices = []
    storages = dbmanager.find_all_storages()
    for s in storages:
        storages_choices.append((s.id, s.name))

    name = StringField("The name of the Movie.", validators=[DataRequired(), Length(max=255)])
    provider = StringField("The Provider of the Movie.", validators=[Length(max=255)])
    actors = SelectMultipleField("Select the Actor of the Movie.", choices=actors_choices, coerce=int)
    storage = SelectField("Select the storage of the Movie.", validators=[DataRequired()], choices=storages_choices, coerce=int)
    storage_path = StringField("The file path of the movie in storage.", validators=[Length(max=255)])
    cover = FileField("Upload cover file of the movie.")
    snapshots = FileField("Upload the snapshot files of the movie.")

    def validate(self):
        super(MovieRegularForm, self).validate()

        if self.name.data.strip() == "":
            self.name.errors.append("Movie name can not be empty.")
            return False

        if self.storage_path.data.strip() == "":
            self.storage_path.errors.append("The path in storage for movie can not be empty.")
            return False

        return True

    def set_is_not_edit(self, is_edit):
        self.is_not_edited = is_edit
