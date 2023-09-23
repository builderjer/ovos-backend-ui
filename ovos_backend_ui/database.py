from passlib.context import CryptContext

import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_json import NestedMutableJson
from sqlalchemy import select

from ovos_utils.xdg_utils import xdg_data_home

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
        )

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_password(password, encrypted_password):
    if pwd_context.verify(password, encrypted_password):
        print("good password")
        return True
    print("bad password")
    return False

# create the db extension
db = SQLAlchemy()

def connect_db(app):
    # this defaults to use sqlite db, but can be changed to use mysql
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{xdg_data_home()}/ovos_backend_ui.db"
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app, db

class User(db.Model):
    display_name = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    # name = db.Column(NestedMutableJson, default="{}", nullable=True)
    # email = db.Column(db.String(100), nullable=True)
    # address = db.Column(NestedMutableJson, default="{}", nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def username(self):
        return self.display_name

    @staticmethod
    def deserialize(data):
        if isinstance(data, str):
            data = json.loads(data)

        display_name = data.get("display_name", self.display_name)
        password = data.get("password", self.password)
        # user_name_json = {}
        # user_name = data.get("name", {})
        # if user_name:
        #     user_name["first_name"] = user_name.get("first_name", "")
        #     user_name["last_name"] = user_name.get("last_name", "")
        # user_address_json = {}
        # user_address = data.get("address", {})
        # if user_address:
        #     user_address["street_name"] = user_address.get("street_name", "")
        #     user_address["apt_number"] = user_address.get("apt_number", "")
        #     user_address["city"] = user_address.get("city", "")
        #     user_address["state"] = user_address.get("state", "")
        #     user_address["zip_code"] = user_address.get("zip_code", "")
        #     user_address["country"] = user_address.get("country", "")
        is_admin = data.get("is_admin", self.is_admin)

        return update_user(display_name,
                           password,
                           # user_name_json,
                           # user_address_json,
                           is_admin)

def get_user_def(user_name) -> User:
    print(user_name)
    user = db.scalars(select(User).filter_by(display_name=user_name)).first()
    # return select(User).where(User.display_name == user_name)
    print(f"user in get_user_def {user}")
    return user

def add_new_user(display_name, password, user_name=None, user_address=None,
                 email=None, is_admin=False):
    entry = User(display_name=display_name, password=password,
                 is_admin=is_admin)

    db.session.add(entry)
    db.session.commit()
    return entry

def update_user(display_name,
                password,
                # user_name_json,
                # user_address_json,
                # email,
                is_admin):
    user_def: User = get_user_def(display_name)
    if not user_def:
        user_def = add_new_user(display_name=display_name,
                                password=password,
                                # username=user_name_json,
                                # address=user_address_json,
                                # email=email,
                                is_admin=is_admin)
    else:
        user_def.display_name = display_name
        user_def.password = password
        # user_def.user_name = user_name_json
        # user_def.user_address = user_address_json
        # user_def.email = email
        user_def.is_admin = is_admin
        db.session.commit()

    return user_def


# from json_database import JsonDatabaseXDG
# from json_database.xdg_utils import xdg_data_home
#
# try:
#     from .configuration import DEFAULT_DATABASE_NAME
#     from .exceptions import DuplicateUserError, NoUserError
# except ImportError:
#     from configuration import DEFAULT_DATABASE_NAME
#     from exceptions import DuplicateUserError, NoUserError
#
# class BackendDatabase(JsonDatabaseXDG):
#     def __init__(self, name=None, xdg_folder=xdg_data_home(),
#                  disable_lock=False, subfolder="json_database",
#                  extension="jsondb", auto_commit=True):
#         name = name or DEFAULT_DATABASE_NAME
#         super().__init__(name, xdg_folder=xdg_data_home(),
#                  disable_lock=False, subfolder="json_database",
#                  extension="jsondb")
#         self.auto_commit = auto_commit
#
#     @property
#     def users(self):
#         return self.db[self.name]
#
#     @property
#     def admin_users(self):
#         return self.search_by_value('admin', True)
#
#     def get_user(self, user_id):
#         user = self.search_by_value('id', user_id)
#         if user:
#             return (user[0], self.get_item_id(user[0]))
#         raise NoUserError(user_id)
#
#     def add_user(self, user_dict):
#         try:
#             self.get_user(user_dict['id'])
#             raise DuplicateUserError(user_dict['id'])
#         except NoUserError:
#             self.add_item(user_dict)
#             if self.auto_commit:
#                 self.commit()
#             return True
#
#     def remove_user(self, user_id):
#         try:
#             self.remove_item(self.get_user(user_id)[1])
#             if self.auto_commit:
#                 self.commit()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#
# DEFAULT_DATABASE = BackendDatabase()
