from flask_sqlalchemy import SQLAlchemy
from applications import create_app
from applications.models import MediaType

db = SQLAlchemy(create_app())


def save_mediatype(name, parent):
    _mediatype = MediaType(name=name, parent=parent)
    db.session.add(_mediatype)
    db.session.commit()


def find_mediatype_by_id(id):
    _mediatype = MediaType.query.filter_by(id=id).first()
    return _mediatype


def find_mediatype_by_name(name):
    _mediatype = MediaType.query.filter_by(name=name).first()
    return _mediatype


def find_all_mediatype():
    _mediatype_list = MediaType.query.all()
    return _mediatype_list


if __name__ == '__main__':
    #save_mediatype("photo", 0)
    #mediatype = find_mediatype_by_name("photo")
    #print mediatype.id
    m_list = find_all_mediatype()
    for m in m_list:
        print m.name

