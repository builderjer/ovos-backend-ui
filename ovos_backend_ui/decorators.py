from functools import wraps
from flask import request, current_app
from flask_login import current_user

try:
    from .users import User
    from .database import DEFAULT_DATABASE as db
except ImportError:
    from users import User
    from database import DEFAULT_DATABASE as db

# def admin_required(user_id):
#     def _check_for_admin(func):
#         for user in db.admin_users:
#             if user['id'] == user_id:
#                 return func()
#         return None
#     return _check_for_admin



def admin_required(func):
    """Expands the `flask_login login_required` decorator to be
specific to the User used here by checking if the user is an admin"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            admin = current_user.is_admin
        except AttributeError:
            admin = False
        if request.method in {"OPTIONS"} or current_app.config.get("LOGIN_DISABLED"):
            pass
        elif not admin:
            return current_app.login_manager.unauthorized()
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)
    return decorated_view
