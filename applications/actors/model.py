from flask_sqlalchemy import SQLAlchemy
from applications import db
from applications import utils


# db = SQLAlchemy(create_app(config['development']))


# class Actor(db.Model):
#     __tablename__ = 'actor'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     sex = db.Column(db.Boolean)
#     country = db.Column(db.String(50))
#     description = db.Column(db.Text)
#     thumb = db.Column(db.Integer)
#
#
#     def __repr__(self):
#         return '<Actor %r>' % self.getName()
#
#
#     def getName(self):
#         return unicode(self.name)
#
#
#     def getId(self):
#         return self.id
#
#
#     def getCountry(self):
#         return unicode(self.country)
#
#
#     def getDescription(self):
#         return unicode(self.description)
#
#
#     def getThumbList(self):
#         return self.thumb
#
#
#     def getActorsWithName(self, actors_list):
#         actors_id_list = utils.splitStrIdToInteger(actors_list)
#         print actors_id_list

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


