# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger
from applications.config import PHOTO_PER_PAGE, PHOTO_TYPE


photo = Blueprint("photo",
                  __name__,
                  template_folder="templates",
                  url_prefix="/photo"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@photo.route('/<string:photo_type>/<int:page_id>')
def photo_index_with_type(photo_type, page_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        if photo_type == "all":
            count_photos = dbmanager.get_count_of_all_photos()
            if count_photos < PHOTO_PER_PAGE:
                photos = dbmanager.find_all_photo_by_page(per_page=count_photos, page=page_id)
            else:
                photos = dbmanager.find_all_photo_by_page(per_page=PHOTO_PER_PAGE, page=page_id)

        if photo_type == "regular":
            count_photos = dbmanager.get_count_of_all_photos_with_type(PHOTO_TYPE["NORMAL"])
            if count_photos < PHOTO_PER_PAGE:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["NORMAL"], per_page=count_photos, page=page_id)
            else:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["NORMAL"], per_page=PHOTO_PER_PAGE, page=page_id)

        if photo_type == "cover":
            count_photos = dbmanager.get_count_of_all_photos_with_type(PHOTO_TYPE["COVER"])
            if count_photos < PHOTO_PER_PAGE:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["COVER"], per_page=count_photos, page=page_id)
            else:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["COVER"], per_page=PHOTO_PER_PAGE, page=page_id)

        if photo_type == "snap":
            count_photos = dbmanager.get_count_of_all_photos_with_type(PHOTO_TYPE["SNAPSHOT"])
            if count_photos < PHOTO_PER_PAGE:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["SNAPSHOT"], per_page=count_photos, page=page_id)
            else:
                photos = dbmanager.find_all_photo_with_type_by_page(PHOTO_TYPE["SNAPSHOT"], per_page=PHOTO_PER_PAGE, page=page_id)

        if photos is None:
            return render_template("photoes.html", pagename="Photos", logon_user=session['username'])
        else:
            min_item = (page_id - 1) * PHOTO_PER_PAGE + 1
            if page_id * PHOTO_PER_PAGE >= count_photos:
                max_item = count_photos
            else:
                max_item = page_id * PHOTO_PER_PAGE

            return render_template("photoes.html",
                                   pagename="%s Photos" % photo_type.title(),
                                   logon_user=session['username'],
                                   photos=photos,
                                   count_photos=count_photos,
                                   min_item=min_item,
                                   max_item=max_item)

