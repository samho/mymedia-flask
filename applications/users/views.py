from flask import Blueprint, render_template, session
from applications.main.forms import LoginForm

users = Blueprint("users",
                  __name__,
                  template_folder="templates",
                  url_prefix="/users"
                  )


@users.route('/all')
def user_index():
    #return render_template("users/users.html", pagename="Users")
    if 'username' in session:
        return render_template("users.html", pagename="Users")
    else:
        return render_template('login.html', form=LoginForm())
