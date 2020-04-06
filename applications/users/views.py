from flask import Blueprint, render_template, session, flash
from applications.main.forms import LoginForm
from applications.users.forms import UserForm
from applications.utils import dbmanager

users = Blueprint("users",
                  __name__,
                  template_folder="templates",
                  url_prefix="/users"
                  )


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
        user_list = dbmanager.find_all_users()
        if user_list is None:
            return render_template("users.html", pagename="Users", logon_user=session['username'])
        else:
            return render_template("users.html", pagename="Users", logon_user=session['username'], users=user_list)

    return render_template("/user_new.html", userform=userform)


