from flask import Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger
from applications.storage.forms import StorageForm

storage = Blueprint("storage",
                  __name__,
                  template_folder="templates",
                  url_prefix="/storage"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@storage.route('/all')
def storage_index():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        storages = dbmanager.find_all_storages()
        if storages is None:
            return render_template("storages.html", pagename="Storages", logon_user=session['username'])
        else:
            storage_list = []
            for s in storages:
                mediatype = dbmanager.find_mediatype_by_id(s.mediatype)
                storage_list.append({"id": s.id, "name": s.name, "mediatype": mediatype.name, "size": s.size})

            return render_template("storages.html", pagename="Storage List", logon_user=session['username'], storage_list=storage_list)


@storage.route('/new')
def new_storage():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    storageform = StorageForm()
    return render_template("create_storage.html", pagename="New Storage", logon_ueer=session['username'], storageform=storageform)


@storage.route('/create_storage', methods=['GET', 'POST'])
def create_storage():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    storageform = StorageForm()
    if storageform.validate_on_submit():
        storage = dbmanager.find_storage_by_name(storageform.name.data.strip())
        if len(storage) == 0:
            logger.info("Saving new media type to db.")
            op_result = dbmanager.save_storage(storageform.name.data.strip(), storageform.mediatype.data, float(storageform.size.data))
            logger.info("Save new storage complete, status: %s." % op_result["op_status"])
            return redirect("/storage/all")
        else:
            logger.info("The storage with name %s is existed." % storageform.name.data.strip())
            storageform.name.errors.append("Storage with name '%s' is existed." % storageform.name.data.strip())
            return render_template("create_storage.html", pagename="Create Storage", logon_user=session['username'], storageform=storageform)

    logger.error("Create new storage fail.")
    return render_template("create_storage.html", pagename="Create Storage", logon_user=session['username'], storageform=storageform)


@storage.route('/edit/<int:storage_id>', methods=['GET', 'POST'])
def edit_storage(storage_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    storage = dbmanager.find_storage_by_id(storage_id)
    if storage is None:
        logger.error("There is not any storage match id %d." % storage_id)
        return redirect("/storge/all")
    else:
        mediatype = dbmanager.find_mediatype_by_id(storage.mediatype)
        cur_storage = {"id": storage.id, "name": storage.name, "mediatype_name": mediatype.name, "size": storage.size}
        storageform = StorageForm()
        return render_template("edit_storage.html", pagename="Edit Storage", logon_user=session['username'], storageform=storageform, cur_storage=cur_storage)


@storage.route('/update_storage/<int:storage_id>', methods=['GET', 'POST'])
def update_storage(storage_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    cur_storage = dbmanager.find_storage_by_id(storage_id)
    storageform = StorageForm()
    if storageform.validate_on_submit():
        storages = dbmanager.find_storage_by_name(storageform.name.data.strip())
        if len(storages) == 0:
            logger.info("Update new storage to db.")
            op_result = dbmanager.update_storage(storage_id, storageform.name.data.strip(), storageform.mediatype.data, float(storageform.size.data))
            logger.info("Update new storage complete, status: %s." % op_result["op_status"])
            return redirect("/storage/all")
        else:
            logger.info("Storage %s is existed." % storageform.name.data.strip())
            storageform.name.errors.append("Storage is existed.")
            return render_template("edit_storage.html", pagename="Edit Storage", logon_user=session['username'], storageform=storageform, cur_storage=cur_storage)
    else:
        return render_template("edit_storage.html", pagename="Edit Storage", logon_user=session['username'], storageform=storageform, cur_storage=cur_storage)


@storage.route('/delete_confirm/<int:storage_id>', methods=['GET', 'POST'])
def delete_confirm(storage_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    storage = dbmanager.find_storage_by_id(storage_id)
    if storage is None:
        logger.error("There is not any storage match id %d." % storage_id)
        return redirect("/storage/all")
    else:
        mediatype = dbmanager.find_mediatype_by_id(storage.mediatype)
        cur_storage = {"id": storage.id, "name": storage.name, "mediatype_name": mediatype.name, "size": storage.size}
        return render_template("delete_storage_confirm.html", pagename="Delete Storage Confirm", logon_user=session['username'], cur_storage=cur_storage)


@storage.route('/delete_storage/<int:storage_id>')
def delete_storge(storage_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    storage = dbmanager.find_storage_by_id(storage_id)
    if storage is None:
        logger.error("There is not any storage match id %d." % storage_id)
        return redirect("/storage/all")
    else:
        op_result = dbmanager.delete_storage(storage_id)
        logger.info("Delete the storage with id: %d success." % storage_id)
        return redirect("/storage/all")














