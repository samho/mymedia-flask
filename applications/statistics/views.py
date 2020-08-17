# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session, request
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger
from applications.config import PHOTO_PER_PAGE, PHOTO_TYPE
from applications.search.forms import SearchForm


statistics = Blueprint("statistics",
                   __name__,
                   template_folder="templates",
                   url_prefix="/statistics"
                   )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@statistics.route('/<string:statistics_type>', methods=['GET'])
def search_result(statistics_type):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        statistics_result = []
        result_number = 0
        if statistics_type == "movieofactor":
            db_all_actor_with_movie = dbmanager.get_all_actor_by_movie()
            for actor_id, movies in db_all_actor_with_movie:
                result_number = result_number + 1
                actor = dbmanager.find_actor_by_id(actor_id)
                statistics_result.append({"result_number": result_number, "name": actor.name, "name_url": "/actor/detail/%d" % actor_id, "count": movies})

        if statistics_type == "ebookoftype":
            db_all_ebook_with_type = dbmanager.get_all_ebook_by_type()
            for ebook_type_id, ebooks in db_all_ebook_with_type:
                result_number = result_number + 1
                m_type = dbmanager.find_mediatype_by_id(ebook_type_id)
                statistics_result.append({"result_number": result_number, "name": m_type.name, "name_url": "#", "count": ebooks})

        return render_template("statistics_result.html", pagename="Statistics Page",
                                search_form=SearchForm(),
                                logon_user=session['username'],
                                statistics_result=statistics_result)

