# -*- coding: utf-8 -*-
from flask import request, Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger, combineIntegerToStr, splitStrIdToInteger
from applications.movies.forms import MovieRegularForm, MovieAdultForm
from applications.config import MOVIE_TYPE, MEDIA_LOCAL_PATH, MEDIA_URL, MOVIE_PER_PAGE, PHOTO_TYPE, MOVIE_DEFAULT_COVER_URL, MOVIE_DEFAULT_SNAP_URL
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
                for m_type in dbmanager.find_movie_type_by_movie_id(m.id):
                    tmp_type = dbmanager.find_mediatype_by_id(m_type.type_id)
                    types_list.append(tmp_type.name)
                types = ", ".join(types_list)

                actors_list = []
                for m_actor in dbmanager.find_movie_actor_by_movie_id(m.id):
                    tmp_actor = dbmanager.find_actor_by_id(m_actor.actor_id)
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
                                   pages=movies.pages,
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
            if movieform.cover.data.filename == '':
                op_cover_save = dbmanager.save_photo_with_string("nopic", ".jpg", PHOTO_TYPE["COVER"], "")
            else:
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

            # Save the mapping between Movie and snapshots
            for s_id in op_snapshots:
                ob_map_m_s = dbmanager.save_movie_photo(op_movie_save["new_id"], s_id)

            # Save the mapping between Movie and actors
            for a_id in movieform.actors.data:
                ob_map_m_a = dbmanager.save_movie_actor(op_movie_save["new_id"], a_id)

            # Save the mapping between Movie and type
            op_map_m_t = dbmanager.save_movie_type(op_movie_save["new_id"], MOVIE_TYPE[movie_type.upper()])

            return redirect("/movie/all/1")
        else:
            logger.info("The movie with name %s seems existed." % movieform.name.data.strip())
            return render_template("create_movie.html", pagename="New Movie", loggon_user=session['username'],
                                   movieform=movieform, movie_type=movie_type)
    else:
        return render_template("create_movie.html", pagename="New Movie", logon_ueer=session['username'],
                               movieform=movieform, movie_type=movie_type)


@movie.route('/detail/<int:movie_id>', methods=['GET', 'POST'])
def view_movie_detail(movie_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_movie = dbmanager.find_movie_by_id(movie_id)

    if db_movie is None:
        logger.error("There is not any movie with id %d is existed" % movie_id)
        return redirect("/movie/all/1")
    else:
        snapshot_list = []
        # for sid in splitStrIdToInteger(db_movie.snapshots):
        for sid in dbmanager.find_movie_photo_by_movie_id(db_movie.id):
            tmp_snapshot = dbmanager.find_photo_by_id(sid.photo_id)
            if tmp_snapshot is None:
                logger.error("The snapshot with id %d is not existed." % sid.photo_id)
                continue
            else:
                if os.path.exists(os.path.join(MEDIA_LOCAL_PATH, tmp_snapshot.name+tmp_snapshot.ext)):
                    snapshot_list.append({"id": tmp_snapshot.id, "url": tmp_snapshot.path})
                else:
                    snapshot_list.append({"id": tmp_snapshot.id, "url": MOVIE_DEFAULT_SNAP_URL})

        types_list = []
        type_list = dbmanager.find_movie_type_by_movie_id(db_movie.id)
        for tid in type_list:
            tmp_type = dbmanager.find_mediatype_by_id(tid.type_id)
            types_list.append(tmp_type.name)
        types = ", ".join(types_list)

        actors_list = []
        # for actor_id in splitStrIdToInteger(db_movie.actors):
        for aid in dbmanager.find_movie_actor_by_movie_id(db_movie.id):
            tmp_actor = dbmanager.find_actor_by_id(aid.actor_id)
            actors_list.append(tmp_actor.name)
        actors = ", ".join(actors_list)

        storage = dbmanager.find_storage_by_id(db_movie.storage)

        cur_cover = dbmanager.find_photo_by_id(db_movie.cover)
        if cur_cover.path == "":
            logger.error("The Cover with id %d is not existed." % db_movie.cover)
            cover = MOVIE_DEFAULT_COVER_URL
        else:
            if os.path.exists(os.path.join(MEDIA_LOCAL_PATH, cur_cover.name + cur_cover.ext)):
                cover = cur_cover.path
            else:
                cover = MOVIE_DEFAULT_COVER_URL

        movie = {"id": db_movie.id,
                 "name": db_movie.name,
                 "type": types,
                 "provider": db_movie.provider,
                 "actors": actors,
                 "storage": storage.name,
                 "filepath": db_movie.file_path,
                 "cover": cover,
                 "snapshots": snapshot_list}
        return render_template("movie.html", pagename="Movie Details", logon_user=session["username"], movie=movie)


@movie.route('/delete_confirm/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie_confirm(movie_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_movie = dbmanager.find_movie_by_id(movie_id)

    if db_movie is None:
        logger.error("There is not any movie with id %d is existed" % movie_id)
        return redirect("/movie/all/1")
    else:
        snapshot_list = []
        for sid in dbmanager.find_movie_photo_by_movie_id(db_movie.id):
            tmp_snapshot = dbmanager.find_photo_by_id(sid.photo_id)
            if tmp_snapshot is None:
                logger.error("The snapshot with id %d is not existed." % sid.photo_id)
                continue
            else:
                if os.path.exists(os.path.join(MEDIA_LOCAL_PATH, tmp_snapshot.name+tmp_snapshot.ext)):
                    snapshot_list.append({"id": tmp_snapshot.id, "url": tmp_snapshot.path})
                else:
                    snapshot_list.append({"id": tmp_snapshot.id, "url": MOVIE_DEFAULT_SNAP_URL})

        types_list = []
        type_list = dbmanager.find_movie_type_by_movie_id(db_movie.id)
        for tid in type_list:
            tmp_type = dbmanager.find_mediatype_by_id(tid.type_id)
            types_list.append(tmp_type.name)
        types = ", ".join(types_list)

        actors_list = []
        for aid in dbmanager.find_movie_actor_by_movie_id(db_movie.id):
            tmp_actor = dbmanager.find_actor_by_id(aid.actor_id)
            actors_list.append(tmp_actor.name)
        actors = ", ".join(actors_list)

        storage = dbmanager.find_storage_by_id(db_movie.storage)

        cur_cover = dbmanager.find_photo_by_id(db_movie.cover)
        if cur_cover.path == "":
            logger.error("The snapshot with id %d is not existed." % sid)
            cover = MOVIE_DEFAULT_COVER_URL
        else:
            if os.path.exists(os.path.join(MEDIA_LOCAL_PATH, cur_cover.name + cur_cover.ext)):
                cover = cur_cover.path
            else:
                cover = MOVIE_DEFAULT_COVER_URL

        movie = {"id": db_movie.id,
                 "name": db_movie.name,
                 "type": types,
                 "provider": db_movie.provider,
                 "actors": actors,
                 "storage": storage.name,
                 "filepath": db_movie.file_path,
                 "cover": cover,
                 "snapshots": snapshot_list}
        return render_template("delete_movie_confirm.html", pagename="Movie Delete Confirm", logon_user=session["username"], movie=movie)


@movie.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_movie = dbmanager.find_movie_by_id(movie_id)
    if cur_movie is None:
        logger.error("There is not any movie match id %d." % movie_id)
        return redirect("/movie/all/1")
    else:
        op_cover_delete = dbmanager.delete_photo(cur_movie.cover)
        if op_cover_delete["op_status"]:
            logger.info("Delete cover with id %d is success." % cur_movie.cover)
        else:
            logger.error("Delete cover with id %d is fail." % cur_movie.cover)

        # snapshot_list = splitStrIdToInteger(cur_movie.snapshots)
        snapshot_list = dbmanager.find_movie_photo_by_movie_id(movie_id)
        for sid in snapshot_list:
            op_snapshots_delete = dbmanager.delete_photo(sid.photo_id)
            if op_snapshots_delete["op_status"]:
                logger.info("Delete snapshot with id %d is success." % sid.photo_id)
            else:
                logger.error("Delete snapshot with id %d is fail." % sid.photo_id)

        # Clear the mapping between movie and actor
        for m_a_map in dbmanager.find_movie_actor_by_movie_id(movie_id):
            op_m_a_result = dbmanager.delete_movie_actor(m_a_map.id)

        # Clear the mapping between movie and type
        for m_t_map in dbmanager.find_movie_type_by_movie_id(movie_id):
            op_m_t_result = dbmanager.delete_movie_type(m_t_map.id)

        # Clear the mapping between movie and photo
        for m_p_map in dbmanager.find_movie_photo_by_movie_id(movie_id):
            op_m_p_result = dbmanager.delete_movie_photo(m_p_map.id)

        op_movie_delete = dbmanager.delete_movie(movie_id)
        if op_movie_delete["op_status"]:
            logger.info("Delete movie with id %d is success." % movie_id)
        else:
            logger.error("Delete movie with id %d fail." % movie_id)
    return redirect("/movie/all/1")


