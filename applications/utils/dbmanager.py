from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from applications.models import MediaType, User, Storage
import datetime

db = SQLAlchemy(create_app())

# DB Operations for MediaType


def save_mediatype(name, parent):
    new_mediatype = MediaType(name=name, parent=parent)
    db.session.add(new_mediatype)
    db.session.commit()


def find_mediatype_by_id(id):
    return MediaType.query.filter_by(id=id).first()


def find_mediatype_by_name(name):
    return MediaType.query.filter_by(name=name).first()


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
    return User.query.filter_by(username=username).first()


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
    return Storage.query.filter_by(name=name).first()


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


if __name__ == '__main__':
    #save_mediatype("photo", 0)
    #mediatype = find_mediatype_by_name("photo")
    #print mediatype.id

    #update_mediatype(1, 'photo', 2)
    #msg = delete_mediatype(1)
    m_list = find_all_mediatypes()
    for m in m_list:
        print m.parent


