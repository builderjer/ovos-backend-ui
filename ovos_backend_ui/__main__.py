from argparse import ArgumentParser
from os.path import exists

from flask import Flask, render_template, url_for, session, request, redirect
from flask_login import LoginManager, login_required, current_user

from json_database.exceptions import DatabaseNotCommitted

from users import User
from setup_app import setup_app
from database import BackendDatabase, DEFAULT_DATABASE
from info import NO_ADMIN, APP_INFO


def main(host=None, port=None, debug=None):
    host = host or "localhost"
    port = port or 9876
    debug = debug or False

    app = setup_app()

    @app.route('/')
    def index():
        db = BackendDatabase()

        page_data = {
            "navbar_button_icon": "icon_im-user",
            "page_title": "OVOS BACKEND",
            "navbar_button_title": "LOGIN",
            "navbar_button_url": url_for('auth.index'),
            "app_info": APP_INFO,
            "anonymous": current_user.is_authenticated
                }
        return render_template("base.html", **page_data)


    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    parser = ArgumentParser(description="Local Backend UI", allow_abbrev=False)
    parser.add_argument("--host", nargs="?", help="IP address to broadcast")
    parser.add_argument("--port", nargs="?", help="Port to broadcast on.")
    parser.add_argument("--debug", help="When present, debug is True", action="store_true")

    args = parser.parse_args()

    main(args.host, args.port, args.debug)
