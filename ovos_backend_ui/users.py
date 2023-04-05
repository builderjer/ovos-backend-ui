from json_database.search import Query

try:
    from .database import DEFAULT_DATABASE as DATABASE
    from .exceptions import DuplicateUserError
    from .configuration import pwd_context
except ImportError:
    from database import DEFAULT_DATABASE as DATABASE
    from exceptions import DuplicateUserError
    from configuration import pwd_context

class User():
    def __init__(self, user_id, user_password, admin=False, extra_data=None):
        self._id = user_id
        self._password = user_password
        self._admin = admin
        self._data = extra_data

    @property
    def user_id(self):
        return self._id

    @property
    def password(self):
        return self._password

    @property
    def is_admin(self):
        return self._admin

    @property
    def extra_data(self):
        return self._data

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        # TODO make this work
        return True

    def is_anonymous(self):
        return False

    def to_dict(self):
        return {
            'id': self.user_id,
            'password': self.password,
            'admin': self.is_admin,
            'extra_data': self.extra_data
            }

    @staticmethod
    def create_new_user(user_id, password, admin=False, extra_data=None, database=None, auto_add_to_db=True):
        db = database or DATABASE

        if Query(db).contains_value('id', user_id).build():
            raise DuplicateUserError(user_id)
        password = User.encrypt_password(password)
        try:
            db.add_item({'id': user_id, 'password': password, 'admin': admin, 'data': extra_data})
        except Exception as e:
            print(f"can not add user {user_id} to database: {e}")
        try:
            user = User(user_id, password, admin, extra_data)
        except Exception as e:
            print(f"can not create user {user_id}")
            return False
        if auto_add_to_db:
            db.commit()
        return user

    @staticmethod
    def user_from_db(user):
        if not isinstance(user, dict):
            raise TypeError('user need to be of type dict')
        temp_dict = {}
        for k, v in user.items():
            temp_dict[k] = v
        user_id = temp_dict.pop('id')
        password = temp_dict.pop('password')
        admin = temp_dict.pop('admin')
        return User(user_id, password, admin, temp_dict)

    @staticmethod
    def encrypt_password(password):
        return pwd_context.encrypt(password)

    @staticmethod
    def check_password(password, encrypted_password):
        return pwd_context.verify(password, encrypted_password)

def remove_user(user_id, database=None):
    db = database or DATABASE.database
    q = Query(db).contains_value('id', user_id).build()

