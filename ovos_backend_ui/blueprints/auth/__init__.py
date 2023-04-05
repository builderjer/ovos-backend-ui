from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, current_user
from users import User
from database import DEFAULT_DATABASE as db
from info import NO_USER, NO_USERS, NO_ADMIN, WRONG_PASSWORD
from exceptions import NoUserError

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/')
def index():
    if not db.admin_users:
        if not db.users:
            flash(NO_USERS)
            return redirect(url_for('index'))
        flash(NO_ADMIN)
        return redirect(url_for('index'))
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        try:
            if current_user.is_admin:
                return redirect(url_for("admin.index"))
        except AttributeError:
            pass
        return "User pages" # redirect(url_for(f"user/<{current_user.id}>"))
    page_data = {
        "navbar_button_icon": "icon_im-user",
        "page_title": "OVOS BACKEND",
        "navbar_button_title": "HOME",
        "navbar_button_url": url_for('index'),
        "anonymous": current_user.is_authenticated
            }
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        try:
            user = db.get_user(user_id)[0]
        except NoUserError:
            flash(NO_USER)
            return redirect(url_for("auth.login"))
        if User.check_password(password, user["password"]):
            user = User.user_from_db(user)
            login_user(user)
            if user.is_admin:
                return redirect(url_for("admin.index"))
            else:
                return "user page"
        else:
            flash(WRONG_PASSWORD)
    return render_template("auth.html", **page_data)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
