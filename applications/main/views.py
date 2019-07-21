from flask import Blueprint, render_template, url_for, flash
from forms import LoginForm


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html', form=LoginForm())


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("You have been logged in.", category="success")
        return url_for("main.view")

    return render_template('login.html', form=form)


@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

