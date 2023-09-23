# from argparse import ArgumentParser
# from os.path import exists
#
# from flask import Flask, render_template, url_for, session, request, redirect
# from flask_login import LoginManager, login_required, current_user
#
# from json_database.exceptions import DatabaseNotCommitted
#
# from ovos_backend_ui.users import User
# from ovos_backend_ui import start_backend_ui
# from ovos_backend_ui.database import BackendDatabase, DEFAULT_DATABASE
# from ovos_backend_ui.info import NO_ADMIN, APP_INFO
#
#
# def main(host=None, port=None, debug=True):
#     host = host or "0.0.0.0"
#     port = port or 9876
#     debug = debug or False
#
#     app = setup_app()
#
#     @app.route('/')
#     def index():
#         db = BackendDatabase()
#         app.logger.debug(f"db is {db}")
#         page_data = {
#             "navbar_button_icon": "icon_im-user",
#             "page_title": "OVOS BACKEND",
#             "navbar_button_title": "LOGIN",
#             "navbar_button_url": url_for('auth.index'),
#             "app_info": APP_INFO,
#             "anonymous": current_user.is_authenticated
#                 }
#         return render_template("base.html", **page_data)
#
#
#     app.run(host=host, port=port, debug=debug)
#
# if __name__ == "__main__":
#     parser = ArgumentParser(description="Local Backend UI", allow_abbrev=False)
#     parser.add_argument("--host", nargs="?", help="IP address to broadcast")
#     parser.add_argument("--port", nargs="?", help="Port to broadcast on.")
#     parser.add_argument("--debug", help="When present, debug is True", action="store_true")
#
#     args = parser.parse_args()
#
#     main(args.host, args.port, args.debug)
from ovos_backend_ui import start_backend_ui

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Local Backend UI", allow_abbrev=False)
    parser.add_argument("--host", nargs="?", help="IP address to broadcast", default="0.0.0.0")
    parser.add_argument("--port", nargs="?", help="Port to broadcast on.", default=9876)
    parser.add_argument("--debug", help="When present, debug is True", action="store_true")

    args = parser.parse_args()
    start_backend_ui(args.host, args.port, True)

if __name__ == "__main__":
    main()
