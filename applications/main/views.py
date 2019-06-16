from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required, login_user
from forms import LoginForm
from ..utils import dbmanager


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html', form=LoginForm())


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = dbmanager.find_user_by_name(form.username.data)
        if user is not None and (user.password == form.password.data):
            login_user(user)
            return url_for("main.view")
        flash("Invalid username or password.")
    return render_template('login.html', form=form)


@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated user are allowed.'
