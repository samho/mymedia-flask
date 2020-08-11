# -*- coding: utf-8 -*-
from flask import request, Blueprint, render_template, session, redirect
from applications.main.forms import LoginForm
from applications.utils import dbmanager, logger, combineIntegerToStr, splitStrIdToInteger
from applications.ebooks.forms import eBookForm
from applications.config import EBOOK_PER_PAGE, EBOOK_TYPE
import uuid
import os


ebook = Blueprint("ebook",
                  __name__,
                  template_folder="templates",
                  url_prefix="/ebook"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@ebook.route('/<string:ebook_type>/<int:page_id>')
def movie_index(ebook_type, page_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        ebooks = None
        if ebook_type == "all":
            count_ebooks = dbmanager.get_count_of_all_ebooks()
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_by_page(per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_by_page(per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "development":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["DEVELOPMENT"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DEVELOPMENT"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DEVELOPMENT"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "entertainment":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["ENTERTAINMENT"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["ENTERTAINMENT"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["ENTERTAINMENT"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "python":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["PYTHON"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["PYTHON"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["PYTHON"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "golang":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["GOLANG"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["GOLANG"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["GOLANG"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "kubernetes":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["KUBERNETES"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["KUBERNETES"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["KUBERNETES"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "database":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["DATABASE"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DATABASE"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DATABASE"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "devops":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["DEVOPS"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DEVOPS"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["DEVOPS"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebook_type == "system":
            count_ebooks = dbmanager.get_count_of_all_ebooks_with_type(EBOOK_TYPE["SYSTEM"])
            if count_ebooks < EBOOK_PER_PAGE:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["SYSTEM"], per_page=count_ebooks, page=page_id)
            else:
                ebooks = dbmanager.find_all_ebooks_with_type_by_page(EBOOK_TYPE["SYSTEM"], per_page=EBOOK_PER_PAGE, page=page_id)

        if ebooks is None:
            return render_template("ebooks.html", pagename="eBooks", logon_user=session['username'])
        else:
            min_item = (page_id - 1) * EBOOK_PER_PAGE + 1
            if page_id * EBOOK_PER_PAGE >= count_ebooks:
                max_item = count_ebooks
            else:
                max_item = page_id * EBOOK_PER_PAGE

            ebooks_list = []
            for b in ebooks.items:
                types_list = []
                for e_type in dbmanager.find_ebook_type_by_ebook_id(b.id):
                    tmp_type = dbmanager.find_mediatype_by_id(e_type.type_id)
                    types_list.append(tmp_type.name)
                types = ", ".join(types_list)
                actors = b.actors
                storage = dbmanager.find_storage_by_id(b.storage)
                tmp_book = {"id": b.id, "name": b.name, "type": types, "actors": actors, "storage": storage.name, "path": b.file_path}
                ebooks_list.append(tmp_book)

            return render_template("ebooks.html",
                                   pagename="%s eBooks" % ebook_type.title(),
                                   logon_user=session['username'],
                                   ebooks=ebooks_list,
                                   count_movies=count_ebooks,
                                   min_item=min_item,
                                   max_item=max_item,
                                   has_prev=ebooks.has_prev,
                                   has_next=ebooks.has_next,
                                   prev_num=ebooks.prev_num,
                                   page=ebooks.page,
                                   pages=ebooks.pages,
                                   next_num=ebooks.next_num)


@ebook.route('/new')
def new_ebook():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    ebookform = eBookForm()
    return render_template("create_ebook.html", pagename="New eBook", logon_ueer=session['username'], ebookform=ebookform)


@ebook.route('/create_ebook', methods=['POST'])
def crate_ebook():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    ebookform = eBookForm()
    if ebookform.validate_on_submit():
        new_name = ebookform.name.data.strip()
        if ebookform.actors.data.strip() == "":
            new_actors = "Anonymous Writer"
        else:
            new_actors = ebookform.actors.data.strip()
        new_types = combineIntegerToStr(ebookform.types.data)
        new_storage = ebookform.storage.data
        new_path = ebookform.storage_path.data.strip()
        
        op_save_ebook = dbmanager.save_ebook(name=new_name, actors=new_actors, mediatype=new_types, storage=new_storage, file_path=new_path)
        for type_id in ebookform.types.data:
            op_save_e_type = dbmanager.save_ebook_type(op_save_ebook["new_id"], type_id)

        if op_save_ebook["op_status"]:
            logger.info("Save new ebook success, new id is: %d" % op_save_ebook["new_id"])
            return redirect("/ebook/all/1")
        else:
            logger.error("There is some issue for saving new ebook.")
            return render_template("create_ebook.html", pagename="New eBook", logon_ueer=session['username'], ebookform=ebookform)
    else:
        return render_template("create_ebook.html", pagename="New eBook", logon_ueer=session['username'], ebookform=ebookform)


@ebook.route('/edit/<int:ebook_id>', methods=['GET', 'POST'])
def edit_ebook(ebook_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_ebook = dbmanager.find_ebook_by_id(ebook_id)
    if db_ebook is None:
        logger.error("There is not any ebook match id %d." % ebook_id)
        return redirect("/ebook/all/1")
    else:
        ebookform = eBookForm(name=db_ebook.name, actors=db_ebook.actors, storage_path=db_ebook.file_path)
        return render_template("edit_ebook.html", pagename="Edit eBook", logon_user=session['username'], ebookform=ebookform, ebook_id=ebook_id)


@ebook.route('/update_ebook/<int:ebook_id>', methods=['POST'])
def update_ebook(ebook_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_ebook = dbmanager.find_ebook_by_id(ebook_id)
    ebookform = eBookForm(name=db_ebook.name, actors=db_ebook.actors, storage_path=db_ebook.file_path)
    ebookform.set_is_not_edit(False)
    if ebookform.validate_on_submit():
        logger.info("Prepare to update info of eBook with id %d to db." % ebook_id)
        if ebookform.name.data.strip() != db_ebook.name:
            new_name = ebookform.name.data.strip()
        else:
            new_name = db_ebook.name

        if ebookform.actors.data.strip() != db_ebook.actors:
            new_actors = ebookform.actors.data.strip()
        else:
            new_actors = db_ebook.actors
            
        if ebookform.storage_path.data.strip() != db_ebook.file_path:
            new_path = ebookform.storage_path.data.strip()
        else:
            new_path = db_ebook.file_path

        new_types = combineIntegerToStr(ebookform.types.data)
        # Clear the ebook type mapping
        for e_type in dbmanager.find_ebook_type_by_ebook_id(ebook_id):
            op_delete_e_type = dbmanager.delete_ebook_type(e_type.id)
        # Save new type
        for new_e_type in ebookform.types.data:
            ob_update_e_type = dbmanager.save_ebook_type(ebook_id, new_e_type)

        new_storage = ebookform.storage.data

        op_ebook_resp = dbmanager.update_ebook(id=ebook_id, name=new_name, actors=new_actors, mediatype=new_types, storage=new_storage, file_path=new_path)
        logger.info("Update ebook with new data complete, status: %s." % op_ebook_resp["op_status"])
        return redirect("/ebook/all/1")
    else:
        return render_template("edit_ebook.html", pagename="Edit eBook", logon_user=session['username'], ebookform=ebookform, ebook_id=ebook_id)


@ebook.route('/delete/confirm/<int:ebook_id>', methods=['GET'])
def confirm_delete_ebook(ebook_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    db_ebook = dbmanager.find_ebook_by_id(ebook_id)

    if db_ebook is None:
        logger.errof("There is not any ebook matching id %d found." % ebook_id)
        return redirect("/ebook/all/1")
    else:
        types_list = []
        for e_type in dbmanager.find_ebook_type_by_ebook_id(db_ebook.id):
            tmp_type = dbmanager.find_mediatype_by_id(e_type.type_id)
            types_list.append(tmp_type.name)
        types = ", ".join(types_list)
        storage = dbmanager.find_storage_by_id(db_ebook.storage)
        cur_ebook = {"id": db_ebook.id,
                     "name": db_ebook.name,
                     "type": types,
                     "actors": db_ebook.actors,
                     "storage": storage.name,
                     "path": db_ebook.file_path}
        return render_template("delete_ebook_confirm.html", pagename="Delete eBook Confirm", logon_user=session['username'], cur_ebook=cur_ebook)


@ebook.route('/delete/operation/<int:ebook_id>', methods=['GET'])
def delete_ebook(ebook_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    # Clear the mapping
    for e_type in dbmanager.find_ebook_type_by_ebook_id(ebook_id):
        op_delete_e_type = dbmanager.delete_ebook_type(e_type.id)

    op_result = dbmanager.delete_ebook(ebook_id)

    if op_result["op_status"]:
        logger.info("The ebook with id %d has been deleted." % ebook_id)
        return redirect("/ebook/all/1")
    else:
        logger.error("There is some error appeared for deleting ebook with id %d, delete fail." % ebook_id)
        return redirect("/ebook/all/1")

