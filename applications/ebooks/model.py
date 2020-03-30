from flask_sqlalchemy import SQLAlchemy
from applications import db
from applications.mediatype.model import MediaType


# db = SQLAlchemy(create_app(config['development']))
#
#
# class EBook(db.Model):
#     __tablename__ = 'ebook'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     mediatype = db.Column(db.Integer)
#     storage = db.Column(db.Integer)
#     file_path = db.Column(db.String(500))
#
#     def __repr__(self):
#         return '<EBook %r>' % self.name
#
#     def getId(self):
#         return self.id
#
#     def getName(self):
#         return unicode(self.name)
#
#     def getMeditype(self):
#         return self.mediatype
#
#     def getMediatypeName(self, mediatype_id):
#         return MediaType.getNameById(mediatype_id)
#
#     def getStorage(self):
#         return unicode(self.storage)
#
#     def getFilePath(self):
#         return unicode(self.file_path)

class EBook(db.Model):
    __tablename__ = 'ebook'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mediatype = db.Column(db.String(100)) # with the media type id
    storage = db.Column(db.Integer)
    file_path = db.Column(db.String(500))

    def __repr__(self):
        return '<EBook %r>' % self.name


