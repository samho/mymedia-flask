from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import os
from applications.extensions import bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    #app.config.from_mapping(
    #    DEBUG = False,
    #    MAIL_SERVER = 'smtp.gmail.com',
    #    MAIL_PORT = 587,
    #    MAIL_USE_TLS = True,
    #    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'samhocngz@gmail.com',
    #    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '19781117samho',
    #    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev.sqlite'),
    #)
    #config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)


    # register blueprint
    from applications.main.views import main
    app.register_blueprint(main)

    # register user blueprint
    from applications.users.views import users
    app.register_blueprint(users, url_prefix="/users")

    return app

