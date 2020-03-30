from flask_login import LoginManager
from applications.users.model import User
from .views import auth_blueprint


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


def create_module(app, **kwargs):
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint)

