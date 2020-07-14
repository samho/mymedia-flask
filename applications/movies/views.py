# -*- coding: utf-8 -*-
from flask import request, Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger, combineIntegerToStr, splitStrIdToInteger
from applications.movies.forms import MovieRegularForm, MovieAdultForm
from applications.config import MOVIE_TYPE, MEDIA_LOCAL_PATH, MEDIA_URL, MOVIE_PER_PAGE, PHOTO_TYPE
import uuid
import os


movie = Blueprint("movie",
                  __name__,
                  template_folder="templates",
                  url_prefix="/movie"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@movie.route('/<string:movie_type>/<int:page_id>')
def movie_index(movie_type, page_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        movies = None
        if movie_type == "all":
            count_movies = dbmanager.get_count_of_all_movies()
            if count_movies < MOVIE_PER_PAGE:
                movies = dbmanager.find_all_movie_by_page(per_page=count_movies, page=page_id)
            else:
                movies = dbmanager.find_all_movie_by_page(per_page=MOVIE_PER_PAGE, page=page_id)

        if movie_type == "regular":
            count_movies = dbmanager.get_count_of_all_movies_with_type(MOVIE_TYPE["REGULAR"])
            if count_movies < MOVIE_PER_PAGE:
                movies = dbmanager.find_all_movie_with_type_by_page(MOVIE_TYPE["REGULAR"], per_page=count_movies, page=page_id)
            else:
                movies = dbmanager.find_all_movie_with_type_by_page(MOVIE_TYPE["REGULAR"], per_page=MOVIE_PER_PAGE, page=page_id)

        if movie_type == "adult":
            count_movies = dbmanager.get_count_of_all_movies_with_type(MOVIE_TYPE["ADULT"])
            if count_movies < MOVIE_PER_PAGE:
                movies = dbmanager.find_all_movie_with_type_by_page(MOVIE_TYPE["ADULT"], per_page=count_movies, page=page_id)
            else:
                movies = dbmanager.find_all_movie_with_type_by_page(MOVIE_TYPE["ADULT"], per_page=MOVIE_PER_PAGE, page=page_id)

        if movies is None:
            return render_template("movies.html", pagename="Movie", logon_user=session['username'])
        else:
            min_item = (page_id - 1) * MOVIE_PER_PAGE + 1
            if page_id * MOVIE_PER_PAGE >= count_movies:
                max_item = count_movies
            else:
                max_item = page_id * MOVIE_PER_PAGE

            movies_list = []
            for m in movies.items:
                types_list = []
                for type_id in splitStrIdToInteger(m.types):
                    tmp_type = dbmanager.find_mediatype_by_id(type_id)
                    types_list.append(tmp_type.name)
                types = ", ".join(types_list)
                actors_list = []
                for actor_id in splitStrIdToInteger(m.actors):
                    tmp_actor = dbmanager.find_actor_by_id(actor_id)
                    actors_list.append(tmp_actor.name)
                actors = ", ".join(actors_list)
                storage = dbmanager.find_storage_by_id(m.storage)
                tmp_movie = {"id": m.id, "name": m.name, "provider": m.provider, "type": types, "actors": actors, "storage": storage.name}
                movies_list.append(tmp_movie)

            return render_template("movies.html",
                                   pagename="%s Movies" % movie_type.title(),
                                   logon_user=session['username'],
                                   movies=movies_list,
                                   count_movies=count_movies,
                                   min_item=min_item,
                                   max_item=max_item,
                                   has_prev=movies.has_prev,
                                   has_next=movies.has_next,
                                   prev_num=movies.prev_num,
                                   page=movies.page,
                                   next_num=movies.next_num)


@movie.route('/new/<string:movie_type>')
def new_movie(movie_type):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    if movie_type == "adult":
        movieform = MovieAdultForm()
        return render_template("create_movie.html", pagename="New Movie", logon_ueer=session['username'],
                               movieform=movieform, movie_type=movie_type)

    if movie_type == "regular":
        movieform = MovieRegularForm()
        return render_template("create_movie.html", pagename="New Movie", logon_ueer=session['username'],
                               movieform=movieform, movie_type=movie_type)


@movie.route('/create_movie/<string:movie_type>', methods=['POST'])
def create_movie(movie_type):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    if movie_type == "regular":
        movieform = MovieRegularForm()

    if movie_type == "adult":
        movieform = MovieAdultForm()

    if movieform.validate_on_submit():
        cur_movie = dbmanager.find_movie_by_name(movieform.name.data.strip())
        if len(cur_movie) == 0:
            logger.info("Saving new movie to db.")
            new_name = movieform.name.data.strip()

            if movieform.provider.data.strip() == "":
                new_provider = "Default Provider"
            else:
                new_provider = movieform.provider.data.strip()

            new_actor_list = combineIntegerToStr(movieform.actors.data)
            new_storage = movieform.storage.data
            new_filepath = movieform.storage_path.data.strip()
            # Save the cover file
            cover_file = movieform.cover.data.filename
            logger.info("Upload file %s" % cover_file)
            upload_filename = os.path.splitext(cover_file)[0]
            upload_suffix = os.path.splitext(cover_file)[1]
            save_filename = str(uuid.uuid3(uuid.NAMESPACE_URL, upload_filename.encode('utf-8')))
            save_fullfilename = save_filename + upload_suffix
            save_path = MEDIA_LOCAL_PATH + save_fullfilename
            logger.info("Save path is %s" % save_path)
            movieform.cover.data.save(save_path)
            op_cover_save = dbmanager.save_photo_with_string(save_filename, upload_suffix, PHOTO_TYPE["COVER"], MEDIA_URL+save_fullfilename)
            # end of saving cover file
            # Save snapshot files
            snapshot_list = request.files.getlist('snapshots')
            op_snapshots = []
            for snapshot in snapshot_list:
                # Save the snapshot file
                snapshot_file = snapshot.filename
                logger.info("Upload file %s" % snapshot_file)
                snapshot_filename = os.path.splitext(snapshot_file)[0]
                snapshot_suffix = os.path.splitext(snapshot_file)[1]
                snapshot_filename = str(uuid.uuid3(uuid.NAMESPACE_URL, snapshot_filename.encode('utf-8')))
                snapshot_fullfilename = snapshot_filename + snapshot_suffix
                snapshot_path = MEDIA_LOCAL_PATH + snapshot_fullfilename
                logger.info("Save path is %s" % snapshot_path)
                snapshot.save(snapshot_path)
                op_snapshot_save = dbmanager.save_photo_with_string(snapshot_filename, snapshot_suffix, PHOTO_TYPE["SNAPSHOT"], MEDIA_URL+snapshot_fullfilename)
                op_snapshots.append(op_snapshot_save["new_id"])
                # end of saving cover file
            op_movie_save = dbmanager.save_movie(name=new_name, actors=new_actor_list, 
                                                 snapshots=combineIntegerToStr(op_snapshots), 
                                                 cover=op_cover_save["new_id"], types=MOVIE_TYPE[movie_type.upper()],
                                                 provider=new_provider, storage=new_storage,
                                                 file_path=new_filepath)
            return redirect("/movie/all/1")
        else:
            logger.info("The movie with name %s seems existed." % movieform.name.strip())
            return render_template("create_movie.html", pagename="New Movie", loggon_user=session['username'],
                                   movieform=movieform, movie_type=movie_type)
    else:
        return render_template("create_movie.html", pagename="New Movie", logon_ueer=session['username'],
                               movieform=movieform, movie_type=movie_type)


# @actor.route('/detail/<int:actor_id>', methods=['GET', 'POST'])
# def view_actor_detail(actor_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     db_actor = dbmanager.find_actor_by_id(actor_id)
#     sex = "Female"
#     if db_actor is None:
#         logger.error("There is not any actor with id %d is existd" % actor_id)
#         return redirect("/actor/all")
#     else:
#         if db_actor.sex == 0:
#             sex = "Male"
#
#         int_list = splitStrIdToInteger(db_actor.type)
#         str_list = []
#         for i_type in int_list:
#             db_mediatype = dbmanager.find_mediatype_by_id(i_type)
#             str_list.append(db_mediatype.name)
#         type_list = ", ".join(str_list)
#
#         if db_actor.description == "":
#             description = "The author is lazy, there is nothing for this actor yet, you can edit and add some description for her(him)."
#         else:
#             description = db_actor.description
#
#         db_thumb = dbmanager.find_photo_by_id(db_actor.thumb)
#         if db_thumb.path == "":
#             thumb = MEDIA_URL + db_thumb.name + db_thumb.ext
#         else:
#             thumb = db_thumb.path
#
#         actor = {"name": db_actor.name, "sex": sex, "country": db_actor.country, "description": description, "type_list": type_list, "thumb": thumb}
#         return render_template("actor.html", pagename="Actor Details", logon_user=session["username"], actor=actor)


# @actor.route('/edit/<int:actor_id>', methods=['GET', 'POST'])
# def edit_actor(actor_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     db_actor = dbmanager.find_actor_by_id(actor_id)
#     if db_actor is None:
#         logger.error("There is not any actor match id %d." % actor_id)
#         return redirect("/actor/all")
#     else:
#         db_photo = dbmanager.find_photo_by_id(db_actor.thumb)
#         actorform = ActorForm(name=db_actor.name, country=db_actor.country, sex=db_actor.sex, thumb_path=db_photo.path, description=db_actor.description)
#         return render_template("edit_actor.html", pagename="Edit Actor", logon_user=session['username'], actorform=actorform, actor_id=actor_id)
#
#
# @actor.route('/update_actor/<int:actor_id>', methods=['POST'])
# def update_actor(actor_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     cur_actor = dbmanager.find_actor_by_id(actor_id)
#     actorform = ActorForm(name=cur_actor.name)
#     actorform.set_is_not_edit(False)
#     if actorform.validate_on_submit():
#         logger.info("Prepare to update info of actor with id %d to db." % actor_id)
#         if actorform.country.data.strip() != cur_actor.country:
#             new_country = actorform.country.data.strip()
#         else:
#             new_country = cur_actor.country
#
#         if actorform.sex.data != cur_actor.sex:
#             new_sex = actorform.sex
#         else:
#             new_sex = cur_actor.sex
#
#         if actorform.description.data.strip() != cur_actor.description:
#             new_description = actorform.description.data.strip()
#         else:
#             new_description = cur_actor.description
#
#         new_type_list = combineIntegerToStr(actorform.types.data)
#
#         # Process the photo update.
#         if actorform.thumb.data.filename.strip() == "":
#             new_thumb = cur_actor.thumb
#         else:
#             if MEDIA_SAVE_TO_DB:
#                 pass
#             else:
#                 upload_file = actorform.thumb.data.filename
#                 logger.info("Upload file %s" % upload_file)
#                 upload_filename = os.path.splitext(upload_file)[0]
#                 upload_suffix = os.path.splitext(upload_file)[1]
#                 save_filename = str(uuid.uuid3(uuid.NAMESPACE_URL, upload_filename.encode('utf-8')))
#                 save_fullfilename = save_filename + upload_suffix
#                 save_path = MEDIA_LOCAL_PATH + save_fullfilename
#                 print(MEDIA_LOCAL_PATH, save_fullfilename)
#                 logger.info("Save path is %s" % save_path)
#                 actorform.thumb.data.save(save_path)
#                 op_photo_result = dbmanager.save_photo_with_string(save_filename, upload_suffix, PHOTO_TYPE["NORMAL"])
#                 new_thumb = op_photo_result["new_id"]
#
#         if new_thumb == cur_actor.thumb and actorform.thumb_path.data.strip() != "":
#             thumb_url = actorform.thumb_path.data.strip()
#             logger.info("Upload file path is %s" % thumb_url)
#             thumb_url_name = os.path.splitext(thumb_url.split("/")[-1])[0]
#             thumb_url_suffix = os.path.splitext(thumb_url.split("/")[-1])[1]
#             op_photo_result = dbmanager.save_photo_with_string(thumb_url_name, thumb_url_suffix, PHOTO_TYPE["NORMAL"], thumb_url)
#             new_thumb = op_photo_result["new_id"]
#
#         op_result = dbmanager.update_actor(id=actor_id, name=cur_actor.name, country=new_country, sex=new_sex, types=new_type_list, description=new_description, thumb=new_thumb)
#         logger.info("Update actor with new data complete, status: %s." % op_result["op_status"])
#         return redirect("/actor/all")
#     else:
#         return render_template("edit_actor.html", pagename="Edit Actor", logon_user=session['username'], actorform=actorform, actor_id=actor_id)
#
#
# @actor.route('/delete_confirm/<int:actor_id>', methods=['GET'])
# def delete_confirm(actor_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     cur_actor = dbmanager.find_actor_by_id(actor_id)
#     if cur_actor is None:
#         logger.error("There is not any actor match id %d." % actor_id)
#         return redirect("/actor/all")
#     else:
#         if cur_actor.sex == 0:
#             sex = "Male"
#         else:
#             sex = 'Female'
#
#         int_list = splitStrIdToInteger(cur_actor.type)
#         str_list = []
#         for i_type in int_list:
#             db_mediatype = dbmanager.find_mediatype_by_id(i_type)
#             str_list.append(db_mediatype.name)
#         type_list = ", ".join(str_list)
#
#         if cur_actor.description == "":
#             description = "The author is lazy, there is nothing for this actor yet, you can edit and add some description for her(him)."
#         else:
#             description = cur_actor.description
#
#         db_thumb = dbmanager.find_photo_by_id(cur_actor.thumb)
#         if db_thumb.path == "":
#             thumb = MEDIA_URL + db_thumb.name + db_thumb.ext
#         else:
#             thumb = db_thumb.path
#
#         actor = {"id": actor_id, "name": cur_actor.name, "sex": sex, "country": cur_actor.country, "description": description, "type_list": type_list, "thumb": thumb}
#         return render_template("delete_actor_confirm.html", pagename="Actor Delete Confirm", logon_user=session["username"], actor=actor)
#
#
# @actor.route('/delete_actor/<int:actor_id>')
# def delete_actor(actor_id):
#     if 'username' not in session:
#         return render_template('login.html', form=LoginForm())
#
#     cur_actor = dbmanager.find_actor_by_id(actor_id)
#     if cur_actor is None:
#         logger.error("There is not any actor match id %d." % actor_id)
#         return redirect("/actor/all")
#     else:
#         op_photo_delete = dbmanager.delete_photo(cur_actor.thumb)
#         if op_photo_delete["op_status"]:
#             logger.info("Delete photo with id %d is success." % cur_actor.thumb)
#         else:
#             logger.error("Delete photo with id %d is fail." % cur_actor.thumb)
#
#         op_actor_delete = dbmanager.delete_actor(actor_id)
#         if op_actor_delete["op_status"]:
#             logger.info("Delete actor with id %d is success." % actor_id)
#         else:
#             logger.error("Delete actor with id %d fail." % actor_id)
#     return redirect("/actor/all")
