from flask import Blueprint, render_template, url_for, flash, redirect, session, send_from_directory
from forms import LoginForm
from applications.utils import dbmanager
from applications.config import MEDIA_LOCAL_PATH, MOVIE_TYPE
from applications.search.forms import SearchForm


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html', form=LoginForm())


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        dbmanager.refresh_logon_datetime(form.username.data)
        flash("You have been logged in.", category="success")
        return redirect(url_for("main.index"))

    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove the username from session
    session.pop('username', None)
    return render_template('login.html', form=LoginForm())


@main.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        ebook_count = dbmanager.get_count_of_all_ebooks()
        actor_count = dbmanager.get_count_of_all_actors()
        photo_count = dbmanager.get_count_of_all_photos()
        movie_count = dbmanager.get_count_of_all_movies()

        r_movie_count = dbmanager.get_count_of_all_movie_type_with_type(MOVIE_TYPE["REGULAR"])
        a_movie_count = dbmanager.get_count_of_all_movie_type_with_type(MOVIE_TYPE["ADULT"])

        top5_actor_with_movie = []
        db_top5_actor_with_movie = dbmanager.get_top5_actor_by_movie()
        for actor_id, movies in db_top5_actor_with_movie:
            actor = dbmanager.find_actor_by_id(actor_id)
            top5_actor_with_movie.append({"name": actor.name, "count": movies})

        top5_ebook_with_type = []
        db_top5_ebook_with_type = dbmanager.get_top5_ebook_by_type()
        for ebook_type_id, ebooks in db_top5_ebook_with_type:
            m_type = dbmanager.find_mediatype_by_id(ebook_type_id)
            top5_ebook_with_type.append({"name": m_type.name, "count": ebooks})

        dash = {"ebook_count": ebook_count,
                "actor_count": actor_count,
                "photo_count": photo_count,
                "movie_count": movie_count,
                "r_movie_percent": round(float(r_movie_count)/float(movie_count),3) * 100,
                "a_movie_percent": round(float(a_movie_count)/float(movie_count),3) * 100,
                "top5_actor": top5_actor_with_movie,
                "top5_ebook": top5_ebook_with_type
                }

        return render_template('index.html', search_form=SearchForm(), logon_user=session['username'], dash=dash)
    else:
        return render_template('login.html', form=LoginForm())


@main.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template('demo.html')


@main.route('/static/media/<string:filename>', methods=['GET', 'POST'])
def get_upload_res(filename):
    return send_from_directory(MEDIA_LOCAL_PATH, filename)

