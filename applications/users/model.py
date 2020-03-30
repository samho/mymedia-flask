from applications import db
import datetime
from applications.extensions import bcrypt


#class User(db.Model):
#    __tablename__ = 'user'
#
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(50), unique=True)
#    password = db.Column(db.String(50))
#    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#    update_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#
#    def __repr__(self):
#        return '<User %r>' % self.username
#
#
#    def get_id(self):
#        return unicode(self.id)
#
#
#    def get_username(self):
#        return unicode(self.username)
#
##
#    def get_password(self):
#        return unicode(self.password)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    create_at = db.Column(db.DateTime, default=datetime.datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
