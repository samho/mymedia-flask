from flask import Blueprint, render_template, url_for, flash, redirect, session
from forms import LoginForm
from applications.utils import dbmanager


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html', form=LoginForm())


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        dbmanager.refresh_logon_datetime(form.username.data)
        flash("You have been logged in.", category="success")
        return redirect(url_for("main.index"))

    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove the username from session
    session.pop('username', None)
    return render_template('login.html', form=LoginForm())


@main.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return render_template('index.html', logon_user=session['username'])
    else:
        return render_template('login.html', form=LoginForm())


@main.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template('demo.html')


