from flask import Blueprint, render_template


main = Blueprint("main", __name__)


@main.route('/', methods=['GET'])
def root():
    return render_template('login.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
