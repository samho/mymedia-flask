from flask_sqlalchemy import SQLAlchemy
from applications import db
#from applications.config import config


# db = SQLAlchemy(create_app(config['development']))
#
#
# class Photo(db.Model):
#     __tablename__ = 'photo'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     ext = db.Column(db.String(10))
#     content = db.Column(db.LargeBinary)
#
#     def __repr__(self):
#         return '<Photo %r>' % self.name
#
#     def getPhotoes(self, photo_id_list):
#         pass


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ext = db.Column(db.String(10))
    content = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Photo %r>' % self.name
