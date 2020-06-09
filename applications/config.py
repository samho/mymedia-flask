import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or 'c2VjcmV0X2tleQ=='
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
MEDIA_MAIL_SUBJECT_PREFIX = '[Flask]'
MEDIA_MAIL_SENDER = 'Media Admin <samhocngz@gmail.com>'
MEDIA_ADMIN = os.environ.get('MEDIA_ADMIN')
LOG_FILE = os.path.join(basedir, 'application.log')
LOG_DEFAULT_LEVEL = 'INFO'
DEBUG = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'samhocngz@gmail.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '19781117samho'
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
DEFAULT_PAGE_SIZE = 20

TEM_PATH = "/tmp"

MEDIA_ACTOR_ID = 4
MEDIA_URL = "/static/media/"
MEDIA_LOCAL_PATH = os.path.join(basedir, MEDIA_URL)
MEDIA_SAVE_TO_DB = False

PHOTO_TYPE = {"NORMAL": 6, "COVER": 7, "SNAPSHOT": 8}


