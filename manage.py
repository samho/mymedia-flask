from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from applications import create_app

from applications import db
from applications.actors.model import Actor
from applications.ebooks.model import EBook
from applications.mediatype.model import MediaType
from applications.movies.model import Movie
from applications.photo.model import Photo
from applications.storage.model import Storage
from applications.users.model import User

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

#@manager.shell
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Actor=Actor, EBook=EBook, MediaType=MediaType, Movie=Movie, Photo=Photo, Storage=Storage)


if __name__ == '__main__':
    manager.run()

