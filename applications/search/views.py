# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, request
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger
from applications.config import PHOTO_PER_PAGE, PHOTO_TYPE
from applications.search.forms import SearchForm

import sys
reload(sys)
sys.setdefaultencoding('utf8')

search = Blueprint("search",
                  __name__,
                  template_folder="templates",
                  url_prefix="/search"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@search.route('/', methods=['POST','GET'])
def search_result():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        search_form = SearchForm()
        if search_form.validate_on_submit():
            search_key = search_form.name.data.strip()

            results = []
        
            actors_search_result = dbmanager.find_actor_by_name_for_search(search_key)
            if len(actors_search_result) > 0:
                for actor in actors_search_result:
                    results.append({"name": actor.name,
                                    "name_url": "/actor/detail/%d" % actor.id,
                                    "category": "Actor",
                                    "category_url": "/actor/all/1"})
            else:
                pass

            movies_search_result = dbmanager.find_movie_by_name_for_search(search_key)
            if len(movies_search_result) > 0:
                for movie in movies_search_result:
                    results.append({"name": movie.name,
                                    "name_url": "/movie/detail/%d" % movie.id,
                                    "category": "Movie",
                                    "category_url": "/movie/all/1"})
            else:
                pass

            ebooks_search_result = dbmanager.find_ebook_by_name_for_search(search_key)
            if len(ebooks_search_result) > 0:
                for ebook in ebooks_search_result:
                    results.append({"name": ebook.name,
                                    "name_url": "#",
                                    "category": "EBook",
                                    "category_url": "/ebook/all/1"})
            else:
                pass

            return render_template("results.html", pagename="Search Result Page", search_for="Search Result of %s" % search_key,
                                   search_form=search_form,
                                   logon_user=session['username'],
                                   search_result=results)
        else:
            return render_template("results.html", pagename="Search Result Page", search_for="Search Result of %s" % "Nothing",
                                   search_form=search_form, logon_user=session['username'])


