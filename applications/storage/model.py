from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from config import config


db = SQLAlchemy(create_app(config['development']))


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mediatype = db.Column(db.Integer)
    size = db.Column(db.Float)

    def __repr__(self):
        return '<Storage %r>' % self.name
