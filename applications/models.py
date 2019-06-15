import datetime
from flask_sqlalchemy import SQLAlchemy
from applications import create_app

db = SQLAlchemy(create_app())


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sex = db.Column(db.Boolean)
    country = db.Column(db.String(50))
    description = db.Column(db.Text)
    thumb = db.Column(db.Integer)  # the record id in photo table.

    def __repr__(self):
        return '<Actor %r>' % self.name


class EBook(db.Model):
    __tablename__ = 'ebook'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mediatype = db.Column(db.String(100)) # with the media type id
    storage = db.Column(db.Integer)
    file_path = db.Column(db.String(500))

    def __repr__(self):
        return '<EBook %r>' % self.name


class MediaType(db.Model):
    __tablename__ = 'mediatype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent = db.Column(db.Integer)

    def __repr__(self):
        return '<MediaType %r>' % self.name


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
        return '<Movie %r>' % self.name


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ext = db.Column(db.String(10))
    content = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Photo %r>' % self.name


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mediatype = db.Column(db.Integer)
    size = db.Column(db.Float)

    def __repr__(self):
        return '<Storage %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username



