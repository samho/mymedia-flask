from flask import Blueprint, render_template
from flask_login import login_required
from forms import LoginForm


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html', form=LoginForm())


@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated user are allowed.'
