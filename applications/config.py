import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('MYMEDIA_SECRET_KEY') or 'c2VjcmV0X2tleQ=='
SQLALCHEMY_COMMIT_ON_TEARDOWN = os.environ.get('MYMEDIA_SQLALCHEMY_COMMIT_ON_TEARDOWN') or True
MEDIA_MAIL_SUBJECT_PREFIX = os.environ.get('MYMEDIA_MEDIA_MAIL_SUBJECT_PREFIX') or '[Flask]'
MEDIA_MAIL_SENDER = os.environ.get('MYMEDIA_MEDIA_MAIL_SENDER') or 'Media Admin <samhocngz@gmail.com>'
MEDIA_ADMIN = os.environ.get('MYMEDIA_MEDIA_ADMIN') or 'samhocngz@gmail.com'
LOG_FILE = os.environ.get('MYMEDIA_LOG_FILE') or os.path.join(basedir, 'application.log')
LOG_DEFAULT_LEVEL = os.environ.get('MYMEDIA_LOG_DEFAULT_LEVEL') or 'INFO'
DEBUG = os.environ.get('MYMEDIA_DEBUG') or False
MAIL_SERVER = os.environ.get('MYMEDIA_MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = os.environ.get('MYMEDIA_MAIL_PORT') or 587
MAIL_USE_TLS = os.environ.get('MYMEDIA_MAIL_USE_TLS') or True
MAIL_USERNAME = os.environ.get('MYMEDIA_MAIL_USERNAME') or 'samhocngz@gmail.com'
MAIL_PASSWORD = os.environ.get('MYMEDIA_MAIL_PASSWORD') or '19781117samho'
SQLALCHEMY_DATABASE_URI = os.environ.get('MYMEDIA_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev.sqlite')
DEFAULT_PAGE_SIZE = os.environ.get('MYMEDIA_DEFAULT_PAGE_SIZE') or 20

TEM_PATH = os.environ.get('MYMEDIA_TEM_PATH') or "/tmp"

MEDIA_ACTOR_ID = os.environ.get('MYMEDIA_MEDIA_ACTOR_ID') or 4
MEDIA_EBOOK_ID = os.environ.get('MYMEDIA_MEDIA_EBOOK_ID') or 3
MEDIA_URL = os.environ.get('MYMEDIA_MEDIA_URL') or "/static/media/"
MEDIA_LOCAL_PATH = os.environ.get('MYMEDIA_MEDIA_LOCAL_PATH') or "/Users/samho/workspace/mymedia-upload"
MEDIA_SAVE_TO_DB = os.environ.get('MYMEDIA_MEDIA_SAVE_TO_DB') or False

PHOTO_TYPE = os.environ.get('MYMEDIA_PHOTO_TYPE') or {"NORMAL": 6, "COVER": 7, "SNAPSHOT": 8}
PHOTO_PER_PAGE = os.environ.get('MYMEDIA_PHOTO_PER_PAGE') or 20

MOVIE_TYPE = os.environ.get('MYMEDIA_MOVIE_TYPE') or {"REGULAR": 9, "ADULT": 10}
MOVIE_PER_PAGE = os.environ.get('MYMEDIA_MOVIE_PER_PAGE') or 20
MOVIE_DEFAULT_COVER_URL = os.environ.get('MYMEDIA_MOVIE_DEFAULT_COVER_URL') or "/static/media/7c60cf3b-7d74-312f-aa57-70b4c1701bed.jpg"

EBOOK_PER_PAGE = os.environ.get('MYMEDIA_EBOOK_PER_PAGE') or 20
EBOOK_TYPE = os.environ.get('MYMEDIA_EBOOK_TYPE') or {"DEVELOPMENT": 12, "ENTERTAINMENT": 13, "PYTHON": 20, "GOLANG": 21, "KUBERNETES": 22}
EBOOK_WRITER_ID = os.environ.get('MYMEDIA_EBOOK_WRITER_ID') or 17

ACTOR_PER_PAGE = os.environ.get('MYMEDIA_ACTOR_PER_PAGE') or 3
ACTOR_TYPE = os.environ.get('MYMEDIA_ACTOR_TYPE') or {"REGULAR": 13, "ADULT": 14}

