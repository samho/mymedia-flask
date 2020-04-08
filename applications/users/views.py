from flask import Blueprint, render_template, session, redirect, url_for
from applications.main.forms import LoginForm
from applications.users.forms import UserForm
from applications.utils import dbmanager, logger

users = Blueprint("users",
                  __name__,
                  template_folder="templates",
                  url_prefix="/users"
                  )

logger = logger.Logger(formatlevel=5, callfile=__file__).get_logger()


@users.route('/all')
def user_index():
    #return render_template("users/users.html", pagename="Users")
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())
    else:
        user_list = dbmanager.find_all_users()
        if user_list is None:
            return render_template("users.html", pagename="Users", logon_user=session['username'])
        else:
            return render_template("users.html", pagename="Users", logon_user=session['username'], users=user_list)


@users.route('/delete_confirm/<int:user_id>')
def delete_confirm(user_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    user = dbmanager.find_user_by_id(user_id)
    if user is None:
        return render_template('delete_confirm.html', pagename="User Delete Confirm", logon_user=session['username'])
    else:
        return render_template('delete_confirm.html', pagename="User Delete Confirm", logon_user=session['username'], user=user)


@users.route('/new')
def new_user():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    return render_template('/user_new.html', logon_user=session['username'], userform=UserForm())


@users.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    userform = UserForm()
    if userform.validate_on_submit():
        dbmanager.save_user(userform.username.data, userform.password.data)
        user_list = dbmanager.find_all_users()
        if user_list is None:
            return render_template("users.html", pagename="Users", logon_user=session['username'])
        else:
            return render_template("users.html", pagename="Users", logon_user=session['username'], users=user_list)

    return render_template("/user_new.html", userform=userform, logon_user=session['username'])


@users.route('/user_delete/<int:user_id>')
def delete_user(user_id):
    if 'username' not in session:
        return render_template('login.html', form=LoginForm())

    op_result = dbmanager.delete_user(user_id)

    if op_result["op_status"]:
        logger.info(op_result["err_msg"])
    else:
        logger.error(op_result["err_msg"])

    user_list = dbmanager.find_all_users()
    if user_list is None:
        return render_template("users.html", pagename="Users", logon_user=session['username'])
    else:
        return render_template("users.html", pagename="Users", logon_user=session['username'], users=user_list)







