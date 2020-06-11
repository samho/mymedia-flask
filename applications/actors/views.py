# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger, combineIntegerToStr, splitStrIdToInteger
from applications.actors.forms import ActorForm
from applications.config import MEDIA_SAVE_TO_DB, MEDIA_LOCAL_PATH, PHOTO_TYPE, MEDIA_URL, basedir
import uuid
import os


actor = Blueprint("actor",
                  __name__,
                  template_folder="templates",
                  url_prefix="/actor"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@actor.route('/all')
def actor_index():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        actors = dbmanager.find_all_actors()
        if actors is None:
            return render_template("actors.html", pagename="Actors", logon_user=session['username'])
        else:
            actor_list = []
            for a in actors:
                if a.sex == 0:
                    cur_sex = "Male"
                else:
                    cur_sex = "Female"

                actor_list.append({"id": a.id, "name": a.name, "sex": cur_sex, "country": a.country, "description": a.description})

            return render_template("actors.html", pagename="Actors", logon_user=session['username'], actor_list=actor_list)


@actor.route('/new')
def new_actor():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    actorform = ActorForm()
    return render_template("create_actor.html", pagename="New Actor", logon_ueer=session['username'], actorform=actorform)


@actor.route('/create_actor', methods=['POST'])
def create_storage():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    actorform = ActorForm()
    if actorform.validate_on_submit():
        actors = dbmanager.find_actor_by_name(actorform.name.data.strip())
        if len(actors) == 0:
            logger.info("Saving new actor to db.")
            if actorform.thumb.data.filename.strip() != "":
                if MEDIA_SAVE_TO_DB:
                    pass
                else:
                    upload_file = actorform.thumb.data.filename
                    logger.info("Upload file %s" % upload_file)
                    upload_filename = os.path.splitext(upload_file)[0]
                    upload_suffix = os.path.splitext(upload_file)[1]
                    save_filename = str(uuid.uuid3(uuid.NAMESPACE_URL, upload_filename.encode('utf-8')))
                    save_fullfilename = save_filename + upload_suffix
                    save_path = MEDIA_LOCAL_PATH + save_fullfilename
                    logger.info("Save path is %s" % save_path)
                    actorform.thumb.data.save(save_path)
                    op_photo_result = dbmanager.save_photo_with_string(save_filename, upload_suffix, PHOTO_TYPE["NORMAL"])
                    type_list = combineIntegerToStr(actorform.types.data)
                    op_result = dbmanager.save_actor(actorform.name.data.strip(), actorform.sex.data, actorform.country.data.strip(), actorform.description.data.strip(), op_photo_result["new_id"],
                                                      type_list)
                    logger.info("Save new actor complete, status: %s." % op_result["op_status"])
                    return redirect("/actor/all")
            else:
                thumb_url = actorform.thumb_path.data.strip()
                logger.info("Upload file path is %s" % thumb_url)
                thumb_url_name = os.path.splitext(thumb_url.split("/")[-1])[0]
                thumb_url_suffix = os.path.splitext(thumb_url.split("/")[-1])[1]
                op_photo_result = dbmanager.save_photo_with_string(thumb_url_name, thumb_url_suffix, PHOTO_TYPE["NORMAL"], thumb_url)
                type_list = combineIntegerToStr(actorform.types.data)
                op_result = dbmanager.save_actor(actorform.name.data.strip(), actorform.sex.data, actorform.country.data.strip(), actorform.description.data.strip(), op_photo_result["new_id"],
                                                 type_list)
                logger.info("Save new actor with url thumb complete, status is %s: " % op_result["op_status"])
                return redirect("/actor/all")
        else:
            logger.info("The actor with name %s is existed." % actorform.name.data.strip())
            actorform.name.errors.append("Actor with name '%s' is existed." % actorform.name.data.strip())
            return render_template("create_actor.html", pagename="Create Actor", logon_user=session['username'], actorform=actorform)

    logger.error("Create new actor fail.")
    return render_template("create_actor.html", pagename="Create Actor", logon_user=session['username'], actorform=actorform)


@actor.route('/detail/<int:actor_id>', methods=['GET', 'POST'])
def view_actor_detail(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_actor = dbmanager.find_actor_by_id(actor_id)
    sex = "Female"
    if db_actor is None:
        logger.error("There is not any actor with id %d is existd" % actor_id)
        return redirect("/actor/all")
    else:
        if db_actor.sex == 0:
            sex = "Male"

        int_list = splitStrIdToInteger(db_actor.type)
        str_list = []
        for i_type in int_list:
            db_mediatype = dbmanager.find_mediatype_by_id(i_type)
            str_list.append(db_mediatype.name)
        type_list = ", ".join(str_list)

        if db_actor.description == "":
            description = "The author is lazy, there is nothing for this actor yet, you can edit and add some description for her(him)."

        db_thumb = dbmanager.find_photo_by_id(db_actor.thumb)
        if db_thumb.path == "":
            thumb = MEDIA_URL + db_thumb.name + db_thumb.ext
        else:
            thumb = db_thumb.path

        actor = {"name": db_actor.name, "sex": sex, "country": db_actor.country, "description": description, "type_list": type_list, "thumb": thumb}
        return render_template("actor.html", pagename="Actor Details", logon_user=session["username"], actor=actor)


@actor.route('/edit/<int:actor_id>', methods=['GET', 'POST'])
def edit_actor(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_actor = dbmanager.find_actor_by_id(actor_id)
    if db_actor is None:
        logger.error("There is not any actor match id %d." % actor_id)
        return redirect("/actor/all")
    else:
        db_photo = dbmanager.find_photo_by_id(db_actor.thumb)
        actorform = ActorForm(name=db_actor.name, country=db_actor.country, sex=db_actor.sex, thumb_path=db_photo.path, description=db_actor.description)
        return render_template("edit_actor.html", pagename="Edit Actor", logon_user=session['username'], actorform=actorform, actor_id=actor_id)


@actor.route('/update_actor/<int:actor_id>', methods=['POST'])
def update_actor(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_actor = dbmanager.find_actor_by_id(actor_id)
    actorform = ActorForm(name=cur_actor.name)
    actorform.set_is_not_edit(False)
    if actorform.validate_on_submit():
        logger.info("Prepare to update info of actor with id %d to db." % actor_id)
        if actorform.country.data.strip() != cur_actor.country:
            new_country = actorform.country.data.strip()
        else:
            new_country = cur_actor.country

        if actorform.sex.data != cur_actor.sex:
            new_sex = actorform.sex
        else:
            new_sex = cur_actor.sex

        if actorform.description.data.strip() != cur_actor.description:
            new_description = actorform.description.data.strip()
        else:
            new_description = cur_actor.description

        new_type_list = combineIntegerToStr(actorform.types.data)

        # Process the photo update.
        if actorform.thumb.data.filename.strip() == "":
            new_thumb = cur_actor.thumb
        else:
            if MEDIA_SAVE_TO_DB:
                pass
            else:
                upload_file = actorform.thumb.data.filename
                logger.info("Upload file %s" % upload_file)
                upload_filename = os.path.splitext(upload_file)[0]
                upload_suffix = os.path.splitext(upload_file)[1]
                save_filename = str(uuid.uuid3(uuid.NAMESPACE_URL, upload_filename.encode('utf-8')))
                save_fullfilename = save_filename + upload_suffix
                save_path = MEDIA_LOCAL_PATH + save_fullfilename
                print(MEDIA_LOCAL_PATH, save_fullfilename)
                logger.info("Save path is %s" % save_path)
                actorform.thumb.data.save(save_path)
                op_photo_result = dbmanager.save_photo_with_string(save_filename, upload_suffix, PHOTO_TYPE["NORMAL"])
                new_thumb = op_photo_result["new_id"]

        if new_thumb == cur_actor.thumb and actorform.thumb_path.data.strip() != "":
            thumb_url = actorform.thumb_path.data.strip()
            logger.info("Upload file path is %s" % thumb_url)
            thumb_url_name = os.path.splitext(thumb_url.split("/")[-1])[0]
            thumb_url_suffix = os.path.splitext(thumb_url.split("/")[-1])[1]
            op_photo_result = dbmanager.save_photo_with_string(thumb_url_name, thumb_url_suffix, PHOTO_TYPE["NORMAL"], thumb_url)
            new_thumb = op_photo_result["new_id"]

        op_result = dbmanager.update_actor(id=actor_id, name=cur_actor.name, country=new_country, sex=new_sex, types=new_type_list, description=new_description, thumb=new_thumb)
        logger.info("Update actor with new data complete, status: %s." % op_result["op_status"])
        return redirect("/actor/all")
    else:
        return render_template("edit_actor.html", pagename="Edit Actor", logon_user=session['username'], actorform=actorform, actor_id=actor_id)


# @storage.route('/delete_confirm/<int:storage_id>', methods=['GET', 'POST'])
# def delete_confirm(storage_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     storage = dbmanager.find_storage_by_id(storage_id)
#     if storage is None:
#         logger.error("There is not any storage match id %d." % storage_id)
#         return redirect("/storage/all")
#     else:
#         mediatype = dbmanager.find_mediatype_by_id(storage.mediatype)
#         cur_storage = {"id": storage.id, "name": storage.name, "mediatype_name": mediatype.name, "size": storage.size}
#         return render_template("delete_storage_confirm.html", pagename="Delete Storage Confirm", logon_user=session['username'], cur_storage=cur_storage)
#
#
# @storage.route('/delete_storage/<int:storage_id>')
# def delete_storge(storage_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     storage = dbmanager.find_storage_by_id(storage_id)
#     if storage is None:
#         logger.error("There is not any storage match id %d." % storage_id)
#         return redirect("/mediatype/all")
#     else:
#         op_result = dbmanager.delete_storage(storage_id)
#         logger.info("Delete the storage with id: %d success." % storage_id)
#         return redirect("/storage/all")
#

