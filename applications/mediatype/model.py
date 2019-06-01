from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from applications.config import config


db = SQLAlchemy(create_app(config['development']))


class MediaType(db.Model):
    __tablename__ = 'mediatype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent = db.Column(db.Integer)


    def __repr__(self):
        return '<MediaType %r>' % self.name


    def getName(self):
        return unicode(self.name)


    def getNameById(self, id_list):
        pass


    def getParent(self):
        return self.parent

