from flask import Blueprint, render_template

users = Blueprint("users", __name__, template_folder="templates")


@users.route('/users')
def user_index():
    return render_template("users/users.html")

