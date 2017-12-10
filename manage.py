from flask import Flask, render_template
from flask_script import Manager
from applications import create_app


#applications = Flask(__name__)
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
    # applications.run(debug=True)
    manager.run()

