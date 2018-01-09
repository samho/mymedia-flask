from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from config import config
from applications.mediatype.model import MediaType
from applications.actors.model import Actor
from applications.storage.model import Storage
from applications.photo.model import Photo



db = SQLAlchemy(create_app(config['development']))


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    actors = db.Column(db.String(100))  # with the actor id list: 1,2,3
    snapshots = db.Column(db.String(100))  # with the photo id list: 1,2,3
    types = db.Column(db.String(100))  # with the media type id list: 1,2,3
    provider = db.Column(db.String(100))  # the provider of the movie
    storage = db.Column(db.Integer)  # with the storage id
    file_path = db.Column(db.String(500))  # file path on storage

    def __repr__(self):
        return '<Movie %r>' % self.getName()


    def getName(self):
        return unicode(self.name)


    def getId(self):
        return self.id


    def getActors(self):
        if self.actors is None:
            return "None"

        return Actor.getActorsWithName(self.actors)


    def getSnapshots(self):
        if self.snapshots is None:
            return "None"

        return Photo.getPhotoes(self.snapshots)


    def getTypes(self):
        if self.types is None:
            return "None"

        return MediaType.getNameById(self.types)


    def getProvider(self):
        return unicode(self.provider)


    def getStorage(self):
        return Storage.getNameById(self.storage)


    def getFilePath(self):
        return unicode(self.file_path)