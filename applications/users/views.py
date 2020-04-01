from flask import Blueprint, render_template, session
from applications.main.forms import LoginForm
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

