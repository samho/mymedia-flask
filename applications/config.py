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
MEDIA_EBOOK_ID = 3
MEDIA_URL = "/static/media/"
MEDIA_LOCAL_PATH = "/Users/samho/workspace/mymedia-upload"
MEDIA_SAVE_TO_DB = False

PHOTO_TYPE = {"NORMAL": 6, "COVER": 7, "SNAPSHOT": 8}
PHOTO_PER_PAGE = 20

MOVIE_TYPE = {"REGULAR": 13, "ADULT": 14}
MOVIE_PER_PAGE = 20
MOVIE_DEFAULT_COVER_URL = "/static/media/7c60cf3b-7d74-312f-aa57-70b4c1701bed.jpg"

EBOOK_PER_PAGE = 20
EBOOK_TYPE = {"DEVELOPMENT": 12, "ENTERTAINMENT": 13, "PYTHON": 20, "GOLANG": 21, "KUBERNETES": 22}
EBOOK_WRITER_ID = 17

