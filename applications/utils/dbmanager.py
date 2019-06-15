from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from applications.models import MediaType, User, Storage, Photo, Actor, EBook, Movie
import datetime
import marshal
import  os

db = SQLAlchemy(create_app())

# DB Operations for MediaType


def save_mediatype(name, parent):
    new_mediatype = MediaType(name=name, parent=parent)
    db.session.add(new_mediatype)
    db.session.commit()


def find_mediatype_by_id(id):
    return MediaType.query.filter_by(id=id).first()


def find_mediatype_by_name(name):
    return MediaType.query.filter_by(name=name).all()


def find_all_mediatypes():
    return MediaType.query.all()


def update_mediatype(id, name, parent):

    upate_mediatype = find_mediatype_by_id(id)
    if upate_mediatype is None:
        return {"err_msg": "The mediatype with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(MediaType).filter_by(id=id).update({"name": name, "parent": parent})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_mediatype(id):
    delete_mediatype = find_mediatype_by_id(id)
    if delete_mediatype is None:
        return {"err_msg": "The mediatype with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(MediaType).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}

# DB Operations for User


def save_user(username, password):
    new_user = User(username=username, password=password, create_at=datetime.datetime.now(), update_at=datetime.datetime.now())
    db.session.add(new_user)
    db.session.commit()


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def find_user_by_name(username):
    return User.query.filter_by(username=username).all()


def find_all_users():
    return User.query.all()


def update_user(id, username, password):

    update_user = find_user_by_id(id)
    if update_user is None:
        return {"err_msg": "The user with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(User).filter_by(id=id).update({"username": username, "password": password, "update_at": datetime.datetime.now()})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_user(id):
    delete_user = find_user_by_id(id)
    if delete_user is None:
        return {"err_msg": "The user with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(User).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}

# DB Operations for Storage


def save_storage(name, mediatype, size):
    new_storage = Storage(name=name, mediatype=mediatype, size=size)
    db.session.add(new_storage)
    db.session.commit()


def find_storage_by_id(id):
    return Storage.query.filter_by(id=id).first()


def find_storage_by_name(name):
    return Storage.query.filter_by(name=name).all()


def find_all_storages():
    return Storage.query.all()


def update_storage(id, name, mediatype, size):

    update_storage = find_storage_by_id(id)
    if update_storage is None:
        return {"err_msg": "The storage with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Storage).filter_by(id=id).update({"name": name, "mediatype": mediatype, "size": size})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_storage(id):
    delete_storage = find_storage_by_id(id)
    if delete_storage is None:
        return {"err_msg": "The storage with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Storage).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}

# DB Operations for Photo

def save_photo(name, ext, content):
    new_photo = Photo(name=name, ext=ext, content=content)
    db.session.add(new_photo)
    db.session.commit()


def find_photo_by_id(id):
    return Photo.query.filter_by(id=id).first()


def find_all_photo():
    return Photo.query.all()


def update_photo(id, name, ext, content):

    update_photo = find_photo_by_id(id)
    if update_photo is None:
        return {"err_msg": "The photo with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Photo).filter_by(id=id).update({"name": name, "ext": ext, "content": content})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_photo(id):
    delete_photo = find_photo_by_id(id)
    if delete_photo is None:
        return {"err_msg": "The photo with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Photo).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}


# DB Operations for EBook


def save_ebook(name, mediatype, storage, file_path):
    new_ebook = EBook(name=name, mediatype=mediatype, storage=storage, file_path=file_path)
    db.session.add(new_ebook)
    db.session.commit()


def find_ebook_by_id(id):
    return EBook.query.filter_by(id=id).first()


def find_ebook_by_name(name):
    return EBook.query.filter_by(name=name).all()


def find_all_ebooks():
    return EBook.query.all()


def update_ebook(id, name, mediatype, storage, file_path):

    update_ebook = find_ebook_by_id(id)
    if update_ebook is None:
        return {"err_msg": "The ebook with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(EBook).filter_by(id=id).update({"name": name, "mediatype": mediatype, "storage": storage, "file_path": file_path})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_ebook(id):
    delete_ebook = find_ebook_by_id(id)
    if delete_ebook is None:
        return {"err_msg": "The ebook with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(EBook).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}


# DB Operations for Actor


def save_actor(name, sex, country, description, thumb):
    new_actor = Actor(name=name, sex=sex, country=country, description=description, thumb=thumb)
    db.session.add(new_actor)
    db.session.commit()


def find_actor_by_id(id):
    return Actor.query.filter_by(id=id).first()


def find_actor_by_name(name):
    return Actor.query.filter_by(name=name).all()


def find_all_actors():
    return Actor.query.all()


def update_actor(id, name, sex, country, description, thumb):

    update_actor = find_actor_by_id(id)
    if update_actor is None:
        return {"err_msg": "The actor with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Actor).filter_by(id=id).update({"name": name, "sex": sex, "country": country, "description": description, "thumb": thumb})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_actor(id):
    delete_actor = find_actor_by_id(id)
    if delete_actor is None:
        return {"err_msg": "The actor with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Actor).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}

# DB Operations for Movie


def save_movie(name, actors, snapshots, types, provider, storage, file_path):
    new_movie = Movie(name=name, actors=actors, snapshots=snapshots, types=types, provider=provider, storage=storage, file_path=file_path)
    db.session.add(new_movie)
    db.session.commit()


def find_movie_by_id(id):
    return Movie.query.filter_by(id=id).first()


def find_movie_by_name(name):
    return Movie.query.filter_by(name=name).all()


def find_movie_by_provider(provider):
    return Movie.query.filter_by(provider=provider).all()


def find_all_movies():
    return Movie.query.all()


def update_movie(id, name, actors, snapshots, types, provider, storage, file_path):

    update_movie = find_movie_by_id(id)
    if update_movie is None:
        return {"err_msg": "The movie with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Movie).filter_by(id=id).update({"name": name, "actors": actors, "snapshots": snapshots, "types": types, "provider": provider, "storage": storage, "file_path": file_path})
        db.session.commit()
        return {"err_msg": "Update success.", "obj": None}


def delete_movie(id):
    delete_movie = find_movie_by_id(id)
    if delete_movie is None:
        return {"err_msg": "The movie with id %d is not existed." % id, "obj": None}
    else:
        db.session.query(Movie).filter_by(id=id).delete()
        db.session.commit()
        return {"err_msg": "Delete success.", "obj": None}



if __name__ == '__main__':
    #save_mediatype("photo", 0)
    #mediatype = find_mediatype_by_name("photo")
    #print mediatype.id

    #update_mediatype(1, 'photo', 2)
    #msg = delete_mediatype(1)
    #m_list = find_all_mediatypes()
    #for m in m_list:
    #    print m.parent
    #with open("/tmp/viewfile.jpg", 'rb') as input_file:
    #    base = os.path.basename("/tmp/viewfile.jpg")
    #    file_name, ext = os.path.splitext(base)
    #    photo_blob = marshal.dumps(input_file.read(), 2)
    #    save_photo(name=file_name, ext=ext, content=photo_blob)

    try:
        p = find_photo_by_id(1)
        name = p.name
        ext = p.ext
        static_path = "/tmp/"
        print p.name
        print p.ext
        file_name = "%s%s" % (name, ext)
        file_path = os.path.join(static_path, "%s" % file_name)
        with open(file_path, 'wb') as output_file:
            output_file.write(marshal.loads(p.content))
    except Exception:
        print "file not existed."

