from flask import Flask, url_for, redirect, render_template
from flask_login import LoginManager, login_required, current_user
import requests

# Local imports
# from ovos_backend_ui.users import User
from ovos_backend_ui.database import connect_db# DEFAULT_DATABASE
from ovos_backend_ui.configuration import SECRET_KEY
from ovos_backend_ui.blueprints import auth, users#, admin, backend, devices, location, users
from ovos_backend_ui.info import APP_INFO, ENABLE_BACKEND_TEXT

from ovos_config import Configuration

def setup_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    app, db = connect_db(app)


    # Blueprints
    app.register_blueprint(auth, url_prefix="/auth")
    # app.register_blueprint(admin, url_prefix="/admin")
    # app.register_blueprint(backend, url_prefix="/backend")
    # app.register_blueprint(devices, url_prefix="/devices")
    # app.register_blueprint(location, url_prefix="/location")
    app.register_blueprint(users, url_prefix="/users")

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_user_def(user_id)
        # return User.user_from_db(DEFAULT_DATABASE.get_user(user_id)[0])

    @app.route("/", methods=["GET"])
    def index():
        app.logger.info(Configuration().get("backend_ui", "NONE"))
        page_info = {
            "app_info": APP_INFO,
            "backend_enabled": False
            }
        backend_enabled = check_for_backend_auth()
        if backend_enabled:
            app.logger.info("Authorized")
        else:
            app.logger.info("UnAuthorized")
            page_info["enable_backend_text"] = ENABLE_BACKEND_TEXT

        return render_template("base.html", **page_info)
    return app
# try:
#     host = Configuration()["backend_ui"].get("host", "127.0.0.1")
#     port=Configuration()["backend_ui"].get("port", 9876)
# except KeyError as e:
#     host = "127.0.0.1"
#     port = 9876

def start_backend_ui(host, port, debug=False):
    app = setup_app()
    app.run(host=host, port=port, debug=debug)
    return app

def check_for_backend_auth():
    conf = Configuration()["backend_ui"]
    headers = {"Authorization": f"Bearer {conf.get('backend_auth')}"}
    # headers = {"Authorization": f"Bearer {conf.get('backend_auth')}"}
    backend_url = conf.get("backend_url")
    backend_port = conf.get("backend_port")
    return requests.get(f"http://{backend_url}:{backend_port}/v1/admin/config", headers=headers)

