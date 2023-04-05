from json_database import JsonDatabaseXDG
from json_database.xdg_utils import xdg_data_home

try:
    from .configuration import DEFAULT_DATABASE_NAME
    from .exceptions import DuplicateUserError, NoUserError
except ImportError:
    from configuration import DEFAULT_DATABASE_NAME
    from exceptions import DuplicateUserError, NoUserError

class BackendDatabase(JsonDatabaseXDG):
    def __init__(self, name=None, xdg_folder=xdg_data_home(),
                 disable_lock=False, subfolder="json_database",
                 extension="jsondb", auto_commit=True):
        name = name or DEFAULT_DATABASE_NAME
        super().__init__(name, xdg_folder=xdg_data_home(),
                 disable_lock=False, subfolder="json_database",
                 extension="jsondb")
        self.auto_commit = auto_commit

    @property
    def users(self):
        return self.db[self.name]

    @property
    def admin_users(self):
        return self.search_by_value('admin', True)

    def get_user(self, user_id):
        user = self.search_by_value('id', user_id)
        if user:
            return (user[0], self.get_item_id(user[0]))
        raise NoUserError(user_id)

    def add_user(self, user_dict):
        try:
            self.get_user(user_dict['id'])
            raise DuplicateUserError(user_dict['id'])
        except NoUserError:
            self.add_item(user_dict)
            if self.auto_commit:
                self.commit()
            return True

    def remove_user(self, user_id):
        try:
            self.remove_item(self.get_user(user_id)[1])
            if self.auto_commit:
                self.commit()
            return True
        except Exception as e:
            print(e)
            return False

DEFAULT_DATABASE = BackendDatabase()
