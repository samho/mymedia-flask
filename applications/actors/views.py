# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger, combineIntegerToStr, splitStrIdToInteger
from applications.actors.forms import ActorForm
from applications.search.forms import SearchForm
from applications.config import MEDIA_SAVE_TO_DB, MEDIA_LOCAL_PATH, PHOTO_TYPE, MEDIA_URL, ACTOR_PER_PAGE, ACTOR_TYPE
import uuid
import os


actor = Blueprint("actor",
                  __name__,
                  template_folder="templates",
                  url_prefix="/actor"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@actor.route('/<string:actor_type>/<int:page_id>')
def actor_index(actor_type, page_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        actors = None
        if actor_type == "all":
            count_actor = dbmanager.get_count_of_all_actors()
            if count_actor < ACTOR_PER_PAGE:
                actors = dbmanager.find_all_actors_by_page(per_page=count_actor, page=page_id)
            else:
                actors = dbmanager.find_all_actors_by_page(per_page=ACTOR_PER_PAGE, page=page_id)

        if actor_type == "regular":
            count_actor = dbmanager.get_count_of_all_actors_with_type(ACTOR_TYPE["REGULAR"])
            if count_actor < ACTOR_PER_PAGE:
                actors = dbmanager.find_all_actors_with_type_by_page(actor_type=ACTOR_TYPE["REGULAR"], per_page=count_actor, page=page_id)
            else:
                actors = dbmanager.find_all_actors_with_type_by_page(actor_type=ACTOR_TYPE["REGULAR"], per_page=ACTOR_PER_PAGE, page=page_id)

        if actor_type == "adult":
            count_actor = dbmanager.get_count_of_all_actors_with_type(ACTOR_TYPE["ADULT"])
            if count_actor < ACTOR_PER_PAGE:
                actors = dbmanager.find_all_actors_with_type_by_page(actor_type=ACTOR_TYPE["ADULT"], per_page=count_actor, page=page_id)
            else:
                actors = dbmanager.find_all_actors_with_type_by_page(actor_type=ACTOR_TYPE["ADULT"], per_page=ACTOR_PER_PAGE, page=page_id)

        if actors is None:
            return render_template("actors.html", pagename="Actors", search_form=SearchForm(), logon_user=session['username'])
        else:
            min_item = (page_id - 1) * ACTOR_PER_PAGE + 1
            if page_id * ACTOR_PER_PAGE >= count_actor:
                max_item = count_actor
            else:
                max_item = page_id * ACTOR_PER_PAGE

            actor_list = []
            for a in actors.items:
                if a.sex == 0:
                    cur_sex = "Male"
                else:
                    cur_sex = "Female"

                actor_list.append({"id": a.id, "name": a.name, "sex": cur_sex, "country": a.country, "description": a.description})

            return render_template("actors.html",
                                   pagename="Actors",
                                   logon_user=session['username'],
                                   actor_list=actor_list,
                                   has_prev=actors.has_prev,
                                   has_next=actors.has_next,
                                   page=actors.page,
                                   pages=actors.pages,
                                   prev_num=actors.prev_num,
                                   next_num=actors.next_num,
                                   min_item=min_item,
                                   max_item=max_item,
                                   count_actors=count_actor,
                                   search_form = SearchForm()
                                   )


@actor.route('/new')
def new_actor():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    actorform = ActorForm()
    return render_template("create_actor.html", pagename="New Actor", search_form=SearchForm(), logon_ueer=session['username'], actorform=actorform)


@actor.route('/create_actor', methods=['POST'])
def create_actor():
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
                    op_photo_result = dbmanager.save_photo_with_string(save_filename, upload_suffix, PHOTO_TYPE["NORMAL"], MEDIA_URL+save_fullfilename)
                    type_list = combineIntegerToStr(actorform.types.data)
                    op_result = dbmanager.save_actor(actorform.name.data.strip(), actorform.sex.data, actorform.country.data.strip(), actorform.description.data.strip(), op_photo_result["new_id"],
                                                      type_list)
                    # save mapping of actor and mediatype
                    for type_id in actorform.types.data:
                        op_a_type_result = dbmanager.save_actor_type(op_result["new_id"], type_id)

                    logger.info("Save new actor complete, status: %s." % op_result["op_status"])
                    return redirect("/actor/all/1")
            else:
                thumb_url = actorform.thumb_path.data.strip()
                logger.info("Upload file path is %s" % thumb_url)
                thumb_url_name = os.path.splitext(thumb_url.split("/")[-1])[0]
                thumb_url_suffix = os.path.splitext(thumb_url.split("/")[-1])[1]
                op_photo_result = dbmanager.save_photo_with_string(thumb_url_name, thumb_url_suffix, PHOTO_TYPE["NORMAL"], thumb_url)
                type_list = combineIntegerToStr(actorform.types.data)
                op_result = dbmanager.save_actor(actorform.name.data.strip(), actorform.sex.data, actorform.country.data.strip(), actorform.description.data.strip(), op_photo_result["new_id"],
                                                 type_list)

                # save mapping of actor and mediatype
                for type_id in actorform.types.data:
                    op_a_type_result = dbmanager.save_actor_type(op_result["new_id"], type_id)

                logger.info("Save new actor with url thumb complete, status is %s: " % op_result["op_status"])
                return redirect("/actor/all/1")
        else:
            logger.info("The actor with name %s is existed." % actorform.name.data.strip())
            actorform.name.errors.append("Actor with name '%s' is existed." % actorform.name.data.strip())
            return render_template("create_actor.html", pagename="Create Actor", search_form=SearchForm(), logon_user=session['username'], actorform=actorform)

    logger.error("Create new actor fail.")
    return render_template("create_actor.html", pagename="Create Actor", search_form=SearchForm(), logon_user=session['username'], actorform=actorform)


@actor.route('/detail/<int:actor_id>', methods=['GET', 'POST'])
def view_actor_detail(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_actor = dbmanager.find_actor_by_id(actor_id)
    sex = "Female"
    if db_actor is None:
        logger.error("There is not any actor with id %d is existd" % actor_id)
        return redirect("/actor/all/1")
    else:
        if db_actor.sex == 0:
            sex = "Male"

        # int_list = splitStrIdToInteger(db_actor.type)
        # str_list = []
        # for i_type in int_list:
        str_list = []
        for a_type in dbmanager.find_actor_type_by_actor_id(db_actor.id):
            db_mediatype = dbmanager.find_mediatype_by_id(a_type.type_id)
            str_list.append(db_mediatype.name)
        type_list = ", ".join(str_list)

        if db_actor.description == "":
            description = "The author is lazy, there is nothing for this actor yet, you can edit and add some description for her(him)."
        else:
            description = db_actor.description

        db_thumb = dbmanager.find_photo_by_id(db_actor.thumb)
        if db_thumb.path == "":
            thumb = MEDIA_URL + db_thumb.name + db_thumb.ext
        else:
            thumb = db_thumb.path

        actor = {"id": actor_id, "name": db_actor.name, "sex": sex, "country": db_actor.country, "description": description, "type_list": type_list, "thumb": thumb}
        return render_template("actor.html", pagename="Actor Details", search_form=SearchForm(), logon_user=session["username"], actor=actor)


@actor.route('/edit/<int:actor_id>', methods=['GET', 'POST'])
def edit_actor(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_actor = dbmanager.find_actor_by_id(actor_id)
    if db_actor is None:
        logger.error("There is not any actor match id %d." % actor_id)
        return redirect("/actor/all/1")
    else:
        db_photo = dbmanager.find_photo_by_id(db_actor.thumb)
        actorform = ActorForm(name=db_actor.name, country=db_actor.country, sex=db_actor.sex, thumb_path=db_photo.path, description=db_actor.description)
        return render_template("edit_actor.html", pagename="Edit Actor", search_form=SearchForm(), logon_user=session['username'], actorform=actorform, actor_id=actor_id)


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
        # Clear the original mapping
        for origin_map in dbmanager.find_actor_type_by_actor_id(actor_id):
            op_origin_map_result = dbmanager.delete_actor_type(origin_map.id)
        # Save mapping with new one
        for new_type_id in actorform.types.data:
            op_new_map_result = dbmanager.save_actor_type(actor_id, new_type_id)

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
        return redirect("/actor/all/1")
    else:
        return render_template("edit_actor.html", pagename="Edit Actor", search_form=SearchForm(), logon_user=session['username'], actorform=actorform, actor_id=actor_id)


@actor.route('/delete_confirm/<int:actor_id>', methods=['GET'])
def delete_confirm(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_actor = dbmanager.find_actor_by_id(actor_id)
    if cur_actor is None:
        logger.error("There is not any actor match id %d." % actor_id)
        return redirect("/actor/all/1")
    else:
        if cur_actor.sex == 0:
            sex = "Male"
        else:
            sex = 'Female'

        # int_list = splitStrIdToInteger(cur_actor.type)
        # str_list = []
        # for i_type in int_list:
        #     db_mediatype = dbmanager.find_mediatype_by_id(i_type)
        #     str_list.append(db_mediatype.name)
        # type_list = ", ".join(str_list)
        str_list = []
        for i_type in dbmanager.find_actor_type_by_actor_id(actor_id):
            db_mediatype = dbmanager.find_mediatype_by_id(i_type.type_id)
            str_list.append(db_mediatype.name)
        type_list = ", ".join(str_list)

        if cur_actor.description == "":
            description = "The author is lazy, there is nothing for this actor yet, you can edit and add some description for her(him)."
        else:
            description = cur_actor.description

        db_thumb = dbmanager.find_photo_by_id(cur_actor.thumb)
        if db_thumb.path == "":
            thumb = MEDIA_URL + db_thumb.name + db_thumb.ext
        else:
            thumb = db_thumb.path

        actor = {"id": actor_id, "name": cur_actor.name, "sex": sex, "country": cur_actor.country, "description": description, "type_list": type_list, "thumb": thumb}
        return render_template("delete_actor_confirm.html", pagename="Actor Delete Confirm", search_form=SearchForm(), logon_user=session["username"], actor=actor)


@actor.route('/delete_actor/<int:actor_id>')
def delete_actor(actor_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_actor = dbmanager.find_actor_by_id(actor_id)
    if cur_actor is None:
        logger.error("There is not any actor match id %d." % actor_id)
        return redirect("/actor/all/1")
    else:
        op_photo_delete = dbmanager.delete_photo(cur_actor.thumb)
        if op_photo_delete["op_status"]:
            logger.info("Delete photo with id %d is success." % cur_actor.thumb)
        else:
            logger.error("Delete photo with id %d is fail." % cur_actor.thumb)

        for map_id in dbmanager.find_actor_type_by_actor_id(actor_id):
            op_mapping_delete = dbmanager.delete_actor_type(map_id.id)
            if op_mapping_delete["op_status"]:
                logger.info("Delete mapping with id %d is success." % map_id.id)
            else:
                logger.error("Delete mapping with id %d is fail." % map_id.id)

        op_actor_delete = dbmanager.delete_actor(actor_id)
        if op_actor_delete["op_status"]:
            logger.info("Delete actor with id %d is success." % actor_id)
        else:
            logger.error("Delete actor with id %d fail." % actor_id)
    return redirect("/actor/all/1")

