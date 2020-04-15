from flask import Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger
from applications.mediatype.forms import MediaTypeForm

mediatype = Blueprint("mediatype",
                  __name__,
                  template_folder="templates",
                  url_prefix="/mediatype"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@mediatype.route('/all')
def mediatype_index():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        mediatypes = dbmanager.find_all_mediatypes()
        if mediatypes is None:
            return render_template("mediatypes.html", pagename="Media Type", logon_user=session['username'])
        else:
            mediatype_list = []
            for m in mediatypes:
                if m.parent == 0:
                    mediatype_list.append({"id": m.id, "name": m.name, "parent_name": "None", "parent_id": ""})
                else:
                    p_type = dbmanager.find_mediatype_by_id(m.parent)
                    mediatype_list.append({"id": m.id, "name": m.name, "parent_name": p_type.name, "parent_id": p_type.id})

            return render_template("mediatypes.html", pagename="Media Type", logon_user=session['username'], mediatype_list=mediatype_list)


@mediatype.route('/new')
def new_mediatype():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        mediatypes = dbmanager.find_all_mediatypes()
        if mediatypes is None:
            return render_template("create_mediatype.html", pagename="Create Media Type", logon_user=session['username'], mediatypeform=MediaTypeForm())
        else:
            mediatype_list = []
            for m in mediatypes:
                if m.parent == 0:
                    mediatype_list.append({"id": m.id, "name": m.name, "parent_name": "None", "parent_id": 0})
                else:
                    p_type = dbmanager.find_mediatype_by_id(m.parent)
                    mediatype_list.append({"id": m.id, "name": m.name, "parent_name": p_type.name, "parent_id": p_type.id})

        return render_template("create_mediatype.html", pagename="Create Media Type", logon_user=session['username'], mediatypeform=MediaTypeForm())


@mediatype.route('/create_mediatype', methods=['GET', 'POST'])
def create_mediatype():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    mediatypeform = MediaTypeForm()
    if mediatypeform.validate_on_submit():
        mediatype = dbmanager.find_mediatype_by_name(mediatypeform.name.data.strip())
        if len(mediatype) == 0:
            logger.info("Saving new media type to db.")
            op_result = dbmanager.save_mediatype(mediatypeform.name.data.strip(), mediatypeform.parent.data)
            logger.info("Save new media type complete, status: %s." % op_result["op_status"])
            #return render_template("mediatypes.html", pagename="Media Type", logon_user=session['username'], mediatype_list=mediatype_list)
            return redirect("/mediatype/all")
        else:
            logger.info("Media type is existed.")
            mediatypeform.name.errors.append("Media Type is existed.")
            return render_template("create_mediatype.html", pagename="Create Media Type", logon_user=session['username'], mediatypeform=mediatypeform)

    return render_template("create_mediatype.html", pagename="Create Media Type", logon_user=session['username'], mediatypeform=mediatypeform)


@mediatype.route('/edit/<int:mediatype_id>', methods=['GET', 'POST'])
def edit_mediatype(mediatype_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    mediatype = dbmanager.find_mediatype_by_id(mediatype_id)
    if mediatype is None:
        logger.error("There is not any media type match id %d." % mediatype_id)
        return redirect("/mediatype/all")
    else:
        mediatypeform = MediaTypeForm()
        return render_template("edit_mediatype.html", pagename="Edit Media Type", logon_user=session['username'],
                       mediatypeform=mediatypeform, cur_mediatype=mediatype)


@mediatype.route('/update_mediatype/<int:mediatype_id>', methods=['GET', 'POST'])
def update_mediatype(mediatype_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_mediatype = dbmanager.find_mediatype_by_id(mediatype_id)
    mediatypeform = MediaTypeForm()
    if mediatypeform.validate_on_submit():
        mediatype = dbmanager.find_mediatype_by_name(mediatypeform.name.data.strip())
        if len(mediatype) == 0:
            logger.info("Update new media type to db.")
            op_result = dbmanager.update_mediatype(mediatype_id, mediatypeform.name.data.strip(), mediatypeform.parent.data)
            logger.info("Update new media type complete, status: %s." % op_result["op_status"])
            return redirect("/mediatype/all")
        else:
            logger.info("Media type is existed.")
            mediatypeform.name.errors.append("Media Type is existed.")
            return render_template("edit_mediatype.html", pagename="Edit Media Type", logon_user=session['username'], mediatypeform=mediatypeform, cur_mediatype=cur_mediatype)
    else:
        return render_template("edit_mediatype.html", pagename="Edit Media Type", logon_user=session['username'], mediatypeform=mediatypeform, cur_mediatype=cur_mediatype)


@mediatype.route('/delete_confirm/<int:mediatype_id>', methods=['GET', 'POST'])
def delete_confirm(mediatype_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    mediatype = dbmanager.find_mediatype_by_id(mediatype_id)
    if mediatype is None:
        logger.error("There is not any media type match id %d." % mediatype_id)
        return redirect("/mediatype/all")
    else:
        return render_template("delete_mediatype_confirm.html", pagename="Delete Media Type Confirm", logon_user=session['username'], cur_mediatype=mediatype)


@mediatype.route('/delete_mediatype/<int:mediatype_id>')
def delete_mediatype(mediatype_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    mediatype = dbmanager.find_mediatype_by_id(mediatype_id)
    if mediatype is None:
        logger.error("There is not any media type match id %d." % mediatype_id)
        return redirect("/mediatype/all")
    else:
        op_result = dbmanager.delete_mediatype(mediatype_id)
        logger.info("Delete the media type with id: %d success." % mediatype_id)
        return redirect("/mediatype/all")














