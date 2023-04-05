from flask import Flask
from flask_login import LoginManager, login_required, current_user

# Local imports
from users import User
from database import DEFAULT_DATABASE
from configuration import SECRET_KEY
from blueprints import auth, admin, backend, devices, location, users

def setup_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    # Blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(backend, url_prefix="/backend")
    app.register_blueprint(devices, url_prefix="/devices")
    app.register_blueprint(location, url_prefix="/location")
    app.register_blueprint(users, url_prefix="/users")

    @login_manager.user_loader
    def load_user(user_id):
        return User.user_from_db(DEFAULT_DATABASE.get_user(user_id)[0])


    return app
