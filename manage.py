from flask import Flask, render_template
from flask_script import Manager
from app import create_app


#app = Flask(__name__)
app = create_app("development")
manager = Manager(app)


@app.route('/')
def index():
    # return '<h1> Hello World! </h1>'
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return '<h1> Hello, %s!</h1>' % name


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

