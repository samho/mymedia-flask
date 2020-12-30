# -*- coding: utf-8 -*-
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import desc

from applications.actors.model import Actor, Actor_Type
from applications.config import DEFAULT_PAGE_SIZE, PHOTO_PER_PAGE, MOVIE_PER_PAGE, EBOOK_PER_PAGE, ACTOR_PER_PAGE
from applications.ebooks.model import EBook, EBook_Type
from applications.mediatype.model import MediaType
from applications.movies.model import Movie, Movie_Actor, Movie_Photo, Movie_Type
from applications.photo.model import Photo
from applications.storage.model import Storage
from applications.users.model import User
from applications.utils import logger


logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()

app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.app_context().push()
db = SQLAlchemy(app)

# DB Operations for MediaType


def save_mediatype(name, parent):
    try:
        new_mediatype = MediaType(name=name, parent=parent)
        db.session.add(new_mediatype)
        db.session.commit()
        return {"err_msg": "Save media type success.", "obj": None, "op_status": True, "new_id": new_mediatype.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save media type fail.", "obj": None, "op_status": False}


def find_mediatype_by_id(id):
    return MediaType.query.filter_by(id=id).first()


def find_mediatype_by_name(name):
    return MediaType.query.filter_by(name=name).all()


def find_all_mediatypes():
    mediatype_list = MediaType.query.all()
    if mediatype_list is None:
        return None
    return mediatype_list


def find_mediatypes_pagenate(index=1):
    return MediaType.query.paginate(index, DEFAULT_PAGE_SIZE)


def update_mediatype(id, name, parent):

    upate_mediatype = find_mediatype_by_id(id)
    if upate_mediatype is None:
        return {"err_msg": "The mediatype with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(MediaType).filter_by(id=id).update({"name": name, "parent": parent})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_mediatype(id):
    delete_mediatype = find_mediatype_by_id(id)
    if delete_mediatype is None:
        return {"err_msg": "The mediatype with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(MediaType).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def get_type_name_list_by_id(id):
    type_name_list = []
    parent = find_mediatype_by_id(id)
    if parent is None:
        return None
    else:
        type_name_list.append({"name":parent.name, "id": parent.id})
        sons = MediaType.query.filter(MediaType.parent==id).all()
        if sons is None:
            return type_name_list
        else:
            for s in sons:
                type_name_list.append({"name": s.name, "id": s.id})
            return type_name_list

# DB Operations for User


def save_user(username, password):
    try:
        new_user = User(username=username, password=password, create_at=datetime.datetime.now(), update_at=datetime.datetime.now())
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {"err_mst": "Save user success.", "obj": None, "op_status": True, "new_id": new_user.id}
    except Exception as e:
        logger.error(e)
        return {"err_mst": "Save user fail.", "obj": None, "op_status": False}


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def find_user_by_name(username):
    return User.query.filter_by(username=username).first()


def find_all_users():
    user_list = User.query.all()
    if user_list is None:
        return None
    return user_list


def refresh_logon_datetime(username):
    logon_user = find_user_by_name(username)
    if logon_user is None:
        return {"err_msg": "The user with user name %s is not existed." % username, "obj": None, "op_status": False}
    else:
        db.session.query(User).filter_by(id=logon_user.id).update({"update_at": datetime.datetime.now()})
        db.session.commit()
        return {"err_msg": "Update logon user success.", "obj": None, "op_status": True}


def update_user(id, username, password):

    update_user = find_user_by_id(id)
    if update_user is None:
        return {"err_msg": "The user with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(User).filter_by(id=id).update({"username": username, "password": update_user.set_password(password), "update_at": datetime.datetime.now()})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_user(id):
    delete_user = find_user_by_id(id)
    if delete_user is None:
        return {"err_msg": "The user with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}

# DB Operations for Storage


def save_storage(name, mediatype, size):
    try:
        new_storage = Storage(name=name, mediatype=mediatype, size=size)
        db.session.add(new_storage)
        db.session.commit()
        return {"err_msg": "Save stage success.", "obj": None, "op_status": True, "new_id": new_storage.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save stage fail.", "obj": None, "op_status": False}


def find_storage_by_id(id):
    return Storage.query.filter_by(id=id).first()


def find_storage_by_name(name):
    return Storage.query.filter_by(name=name).all()


def find_all_storages():
    return Storage.query.all()


def update_storage(id, name, mediatype, size):

    update_storage = find_storage_by_id(id)
    if update_storage is None:
        return {"err_msg": "The storage with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Storage).filter_by(id=id).update({"name": name, "mediatype": mediatype, "size": size})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_storage(id):
    delete_storage = find_storage_by_id(id)
    if delete_storage is None:
        return {"err_msg": "The storage with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Storage).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}

# DB Operations for Photo


def save_photo(name, ext, content, photo_type=""):
    try:
        new_photo = Photo(name=name, ext=ext, content=content, type=photo_type)
        db.session.add(new_photo)
        db.session.commit()
        return {"err_msg": "Save photo success.", "obj": None, "op_status": True, "new_id": new_photo.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save photo fail.", "obj": None, "op_status": False}


def save_photo_with_string(name, ext, photo_type, path=""):
    try:
        new_photo = Photo(name=name, ext=ext, path=path, type=photo_type)
        db.session.add(new_photo)
        db.session.commit()
        return {"err_msg": "Save photo with string success.", "obj": None, "op_status": True, "new_id": new_photo.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save photo with string fail.", "obj": None, "op_status": False}


def find_photo_by_id(id):
    return Photo.query.filter_by(id=id).first()


def find_all_photo():
    return Photo.query.all()


def find_all_photo_by_page(per_page=PHOTO_PER_PAGE, page=1):
    return Photo.query.paginate(page=page, per_page=per_page)


def get_count_of_all_photos():
    return db.session.query(Photo.id).count()


def find_all_photo_with_type(photo_type):
    return Photo.query.filter_by(type=photo_type).all()


def get_count_of_all_photos_with_type(photo_type):
    return Photo.query.filter_by(type=photo_type).count()


def find_all_photo_with_type_by_page(photo_type, per_page=PHOTO_PER_PAGE, page=1):
    return Photo.query.filter_by(type=photo_type).paginate(page=page, per_page=per_page)


def update_photo(id, name, ext, content):

    update_photo = find_photo_by_id(id)
    if update_photo is None:
        return {"err_msg": "The photo with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Photo).filter_by(id=id).update({"name": name, "ext": ext, "content": content})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_photo(id):
    delete_photo = find_photo_by_id(id)
    if delete_photo is None:
        return {"err_msg": "The photo with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Photo).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


# DB Operations for EBook


def save_ebook(name, actors, mediatype, storage, file_path):
    try:
        new_ebook = EBook(name=name, actors=actors, mediatype=mediatype, storage=storage, file_path=file_path)
        db.session.add(new_ebook)
        db.session.commit()
        return {"err_msg": "Save book success.", "obj": None, "op_status": True, "new_id": new_ebook.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save book fail.", "obj": None, "op_status": False}


def find_ebook_by_id(id):
    return EBook.query.filter_by(id=id).first()


def find_ebook_by_name(name):
    return EBook.query.filter_by(name=name).all()


def find_ebook_by_name_for_search(ebook_name):
    return db.session.query(EBook).filter(EBook.name.like('%'+str(ebook_name).decode("utf8")+'%')).all()


def find_all_ebooks():
    return EBook.query.all()


def find_all_ebooks_by_page(per_page=EBOOK_PER_PAGE, page=1):
    return EBook.query.paginate(page=page, per_page=per_page)


def get_count_of_all_ebooks():
    return db.session.query(EBook.id).count()


def find_all_ebooks_with_type(ebook_type):
    return EBook.query.filter_by(mediatype=ebook_type).all()


def get_count_of_all_ebooks_with_type(ebook_type):
    return EBook.query.filter_by(mediatype=ebook_type).count()


def find_all_ebooks_with_type_by_page(ebook_type, per_page=EBOOK_PER_PAGE, page=1):
    return EBook.query.filter_by(mediatype=ebook_type).paginate(page=page, per_page=per_page)


def update_ebook(id, name, actors, mediatype, storage, file_path):

    update_ebook = find_ebook_by_id(id)
    if update_ebook is None:
        return {"err_msg": "The ebook with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(EBook).filter_by(id=id).update({"name": name, "actors": actors, "mediatype": mediatype, "storage": storage, "file_path": file_path})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_ebook(id):
    delete_ebook = find_ebook_by_id(id)
    if delete_ebook is None:
        return {"err_msg": "The ebook with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(EBook).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


# DB Operations for Actor


def save_actor(name, sex, country, description, thumb, types):
    try:
        new_actor = Actor(name=name, sex=sex, country=country, description=description, thumb=thumb, type=types)
        db.session.add(new_actor)
        db.session.commit()
        return {"err_msg": "Save actor success.", "obj": None, "op_status": True, "new_id": new_actor.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save actor fail.", "obj": None, "op_status": False}


def find_actor_by_id(id):
    return Actor.query.filter_by(id=id).first()


def find_actor_by_name(name):
    return Actor.query.filter_by(name=name).all()


def find_actor_by_type(type_name):
    return db.session.query(Actor).filter(Actor.type.like('%'+str(type_name)+'%')).all()


def find_actor_by_name_for_search(actor_name):
    return db.session.query(Actor).filter(Actor.name.like('%'+str(actor_name).decode("utf8")+'%')).all()


def find_all_actors():
    return Actor.query.all()


def find_all_actors_by_page(per_page=ACTOR_PER_PAGE, page=1):
    return Actor.query.paginate(page=page, per_page=per_page)


def get_count_of_all_actors():
    return db.session.query(Actor.id).count()


def find_all_actors(actor_type):
    return db.session.query(Actor).filter(Actor.type.like('%'+str(actor_type)+'%')).all()


def get_count_of_all_actors_with_type(actor_type):
    return db.session.query(Actor).filter(Actor.type.like('%'+str(actor_type)+'%')).count()


def find_all_actors_with_type_by_page(actor_type, per_page=ACTOR_PER_PAGE, page=1):
    return db.session.query(Actor).filter(Actor.type.like('%'+str(actor_type)+'%')).paginate(page=page, per_page=per_page)


def update_actor(id, name, sex, country, description, thumb, types):

    update_actor = find_actor_by_id(id)
    if update_actor is None:
        return {"err_msg": "The actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Actor).filter_by(id=id).update({"name": name, "sex": sex, "country": country, "description": description, "thumb": thumb, "type": types})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_actor(id):
    delete_actor = find_actor_by_id(id)
    if delete_actor is None:
        return {"err_msg": "The actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Actor).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}

# DB Operations for Movie


def save_movie(name, actors, snapshots, cover, types, provider, storage, file_path):
    try:
        new_movie = Movie(name=name, actors=actors, cover=cover, snapshots=snapshots, types=types, provider=provider, storage=storage, file_path=file_path)
        db.session.add(new_movie)
        db.session.commit()
        return {"err_msg": "Save Movie sucess.", "obj": None, "op_status": True, "new_id": new_movie.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie fail.", "obj": None, "op_status": False}


def find_movie_by_id(id):
    return Movie.query.filter_by(id=id).first()


def find_movie_by_name(name):
    return Movie.query.filter_by(name=name).all()


def find_movie_by_name_for_search(movie_name):
    return db.session.query(Movie).filter(Movie.name.like('%'+str(movie_name).decode("utf8")+'%')).all()


def find_movie_by_provider(provider):
    return Movie.query.filter_by(provider=provider).all()


def find_all_movies():
    return Movie.query.all()


def find_all_movie_by_page(per_page=MOVIE_PER_PAGE, page=1):
    return Movie.query.paginate(page=page, per_page=per_page)


def get_count_of_all_movies():
    return db.session.query(Movie.id).count()


def find_all_movie_with_type(movie_type):
    return Movie.query.filter_by(types=movie_type).all()


def get_count_of_all_movies_with_type(movie_type):
    return Movie.query.filter_by(types=movie_type).count()


def find_all_movie_with_type_by_page(movie_type, per_page=MOVIE_PER_PAGE, page=1):
    return Movie.query.filter_by(types=movie_type).paginate(page=page, per_page=per_page)


def update_movie(id, name, actors, snapshots, types, provider, storage, file_path):

    update_movie = find_movie_by_id(id)
    if update_movie is None:
        return {"err_msg": "The movie with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie).filter_by(id=id).update({"name": name, "actors": actors, "snapshots": snapshots, "types": types, "provider": provider, "storage": storage, "file_path": file_path})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_movie(id):
    delete_movie = find_movie_by_id(id)
    if delete_movie is None:
        return {"err_msg": "The movie with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


# Movie type mapping

def save_movie_type(movie_id, type_id):
    try:
        new_movie_type = Movie_Type(movie_id=movie_id, type_id=type_id)
        db.session.add(new_movie_type)
        db.session.commit()
        return {"err_msg": "Save Movie and Type mapping sucess.", "obj": None, "op_status": True, "new_id": new_movie_type.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie and MediaType mapping fail.", "obj": None, "op_status": False}


def update_movie_type(id, movie_id, type_id):

    u_movie_type = find_movie_type_by_id(id)
    if u_movie_type is None:
        return {"err_msg": "The mapping of Movie and MediaType with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Type).filter_by(id=id).update({"movie_id": movie_id, "type_id": type_id})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_movie_type(id):
    delete_movie_type = find_movie_type_by_id(id)
    if delete_movie_type is None:
        return {"err_msg": "The mapping of Movie and MediaType with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Type).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def find_movie_type_by_id(id):
    return Movie_Type.query.filter_by(id=id).first()


def find_movie_type_by_movie_id(movie_id):
    return Movie_Type.query.filter_by(movie_id=movie_id).all()


def find_movie_type_by_type_id(type_id):
    return Movie_Type.query.filter_by(type_id=type_id).all()


def find_all_movie_type():
    return Movie_Type.query.all()


def get_count_of_all_movie_type():
    return db.session.query(Movie_Type.id).count()


def get_count_of_all_movie_type_with_type(type_id):
    return Movie_Type.query.filter_by(type_id=type_id).count()


def get_count_of_all_movie_type_with_movie(movie_id):
    return Movie_Type.query.filter_by(movie_id=movie_id).count()


# Movie actor mapping

def save_movie_actor(movie_id, actor_id):
    try:
        new_movie_actor = Movie_Actor(movie_id=movie_id, actor_id=actor_id)
        db.session.add(new_movie_actor)
        db.session.commit()
        return {"err_msg": "Save Movie and Actor mapping sucess.", "obj": None, "op_status": True, "new_id": new_movie_actor.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie and Actor mapping fail.", "obj": None, "op_status": False}


def update_movie_actor(id, movie_id, actor_id):

    u_movie_actor = find_movie_actor_by_id(id)
    if u_movie_actor is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Actor).filter_by(id=id).update({"movie_id": movie_id, "actor_id": actor_id})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_movie_actor(id):
    delete_movie_actor = find_movie_actor_by_id(id)
    if delete_movie_actor is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Actor).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def find_movie_actor_by_id(id):
    return Movie_Actor.query.filter_by(id=id).first()


def find_movie_actor_by_movie_id(movie_id):
    return Movie_Actor.query.filter_by(movie_id=movie_id).all()


def find_movie_actor_by_actor_id(actor_id):
    return Movie_Actor.query.filter_by(actor_id=actor_id).all()


def find_all_movie_actor():
    return Movie_Actor.query.all()


def get_count_of_all_movie_actor():
    return db.session.query(Movie_Actor.id).count()


def get_count_of_all_movie_actor_with_actor(actor_id):
    return Movie_Actor.query.filter_by(actor_id=actor_id).count()


def get_count_of_all_movie_actor_with_movie(movie_id):
    return Movie_Actor.query.filter_by(movie_id=movie_id).count()


# Movie photo mapping

def save_movie_photo(movie_id, photo_id):
    try:
        new_movie_photo = Movie_Photo(movie_id=movie_id, photo_id=photo_id)
        db.session.add(new_movie_photo)
        db.session.commit()
        return {"err_msg": "Save Movie and Actor mapping sucess.", "obj": None, "op_status": True, "new_id": new_movie_photo.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie and Actor mapping fail.", "obj": None, "op_status": False}


def update_movie_photo(id, movie_id, photo_id):

    u_movie_photo = find_movie_photo_by_id(id)
    if u_movie_photo is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Photo).filter_by(id=id).update({"movie_id": movie_id, "photo_id": photo_id})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_movie_photo(id):
    delete_movie_photo = find_movie_photo_by_id(id)
    if delete_movie_photo is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Movie_Photo).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def find_movie_photo_by_id(id):
    return Movie_Photo.query.filter_by(id=id).first()


def find_movie_photo_by_movie_id(movie_id):
    return Movie_Photo.query.filter_by(movie_id=movie_id).all()


def find_movie_photo_by_photo_id(photo_id):
    return Movie_Photo.query.filter_by(photo_id=photo_id).all()


def find_all_movie_photo():
    return Movie_Photo.query.all()


def get_count_of_all_movie_photo():
    return db.session.query(Movie_Photo.id).count()


def get_count_of_all_movie_photo_with_photo(photo_id):
    return Movie_Photo.query.filter_by(photo_id=photo_id).count()


def get_count_of_all_movie_photo_with_movie(movie_id):
    return Movie_Photo.query.filter_by(movie_id=movie_id).count()


# Actor MediaType mapping

def save_actor_type(actor_id, type_id):
    try:
        new_actor_type = Actor_Type(actor_id=actor_id, type_id=type_id)
        db.session.add(new_actor_type)
        db.session.commit()
        return {"err_msg": "Save Movie and Actor mapping sucess.", "obj": None, "op_status": True, "new_id": new_actor_type.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie and Actor mapping fail.", "obj": None, "op_status": False}


def update_actor_type(id, actor_id, type_id):

    u_actor_type = find_actor_type_by_id(id)
    if u_actor_type is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Actor_Type).filter_by(id=id).update({"actor_id": actor_id, "type_id": type_id})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_actor_type(id):
    delete_actor_type = find_actor_type_by_id(id)
    if delete_actor_type is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(Actor_Type).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def find_actor_type_by_id(id):
    return Actor_Type.query.filter_by(id=id).first()


def find_actor_type_by_actor_id(actor_id):
    return Actor_Type.query.filter_by(actor_id=actor_id).all()


def find_actor_type_by_type_id(type_id):
    return Actor_Type.query.filter_by(type_id=type_id).all()


def find_all_actor_type():
    return Actor_Type.query.all()


def get_count_of_all_actor_type():
    return db.session.query(Actor_Type.id).count()


def get_count_of_all_actor_type_with_type(type_id):
    return Actor_Type.query.filter_by(type_id=type_id).count()


def get_count_of_all_actor_type_with_actor(actor_id):
    return Actor_Type.query.filter_by(actor_id=actor_id).count()


# EBook MediaType mapping

def save_ebook_type(ebook_id, type_id):
    try:
        new_ebook_type = EBook_Type(ebook_id=ebook_id, type_id=type_id)
        db.session.add(new_ebook_type)
        db.session.commit()
        return {"err_msg": "Save Movie and Actor mapping sucess.", "obj": None, "op_status": True, "new_id": new_ebook_type.id}
    except Exception as e:
        logger.error(e)
        return {"err_msg": "Save Movie and Actor mapping fail.", "obj": None, "op_status": False}


def update_ebook_type(id, ebook_id, type_id):

    u_ebook_type = find_ebook_type_by_id(id)
    if u_ebook_type is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(EBook_Type).filter_by(id=id).update({"ebook_id": ebook_id, "type_id": type_id})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None, "op_status": True}


def delete_ebook_type(id):
    delete_ebook_type = find_ebook_type_by_id(id)
    if delete_ebook_type is None:
        return {"err_msg": "The mapping of Movie and Actor with id %d is not existed." % id, "obj": None, "op_status": False}
    else:
        db.session.query(EBook_Type).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None, "op_status": True}


def find_ebook_type_by_id(id):
    return EBook_Type.query.filter_by(id=id).first()


def find_ebook_type_by_ebook_id(ebook_id):
    return EBook_Type.query.filter_by(ebook_id=ebook_id).all()


def find_ebook_type_by_type_id(type_id):
    return EBook_Type.query.filter_by(type_id=type_id).all()


def find_all_ebook_type():
    return EBook_Type.query.all()


def get_count_of_all_ebook_type():
    return db.session.query(EBook_Type.id).count()


def get_count_of_all_ebook_type_with_type(type_id):
    return EBook_Type.query.filter_by(type_id=type_id).count()


def get_count_of_all_ebook_type_with_ebook(ebook_id):
    return EBook_Type.query.filter_by(ebook_id=ebook_id).count()


#  Statistics and analysis
def get_top5_actor_by_movie():
    return db.session.query(Movie_Actor.actor_id, func.count(Movie_Actor.movie_id)).group_by(Movie_Actor.actor_id).order_by(desc(func.count(Movie_Actor.movie_id))).limit(5)


def get_all_actor_by_movie():
    return db.session.query(Movie_Actor.actor_id, func.count(Movie_Actor.movie_id)).group_by(Movie_Actor.actor_id).order_by(desc(func.count(Movie_Actor.movie_id)))


def get_top5_ebook_by_type():
    return db.session.query(EBook_Type.type_id, func.count(EBook_Type.ebook_id)).group_by(EBook_Type.type_id).order_by(desc(func.count(EBook_Type.ebook_id))).limit(5)


def get_all_ebook_by_type():
    return db.session.query(EBook_Type.type_id, func.count(EBook_Type.ebook_id)).group_by(EBook_Type.type_id).order_by(desc(func.count(EBook_Type.ebook_id)))


if __name__ == '__main__':
    #actors = get_count_of_all_actors_with_type(actor_type=4)
    #actors = find_all_actors_with_type_by_page(actor_type=14, per_page=2, page=2)
    # print actors
    #for actor in actors.items:
    #    print(actor.name)
    # a = get_top5_actor_by_movie()
    a = find_actor_by_name_for_search("有贺美穗")
    print(type(a))
