from flask import Blueprint, render_template, redirect, request, flash, url_for, current_app
from flask_login import login_user, logout_user, current_user
from sqlalchemy import select
# from ovos_backend_ui.users import User
from ovos_backend_ui.database import User, db
from ovos_backend_ui.info import NO_USER, NO_USERS, NO_ADMIN, WRONG_PASSWORD
from ovos_backend_ui.exceptions import NoUserError
from ovos_backend_ui.database import check_password, get_user_def

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/')
def index():
    no_of_users = 0
    no_of_admin_users = 0
    print("no_of_admin_users")
    with current_app.app_context():
        my_query = select(User).where(User.is_admin == True)
        no_of_admin_users = db.session.execute(my_query).scalar()
        print("Im here")
    if not no_of_admin_users:
        print("No Admin")
    # if not db.admin_users:
    #     if not db.users:
    #         flash(NO_USERS)
    #         return render_template("base.html")
        flash(NO_ADMIN)
        return redirect(url_for('index'))
    #     return "no admin"
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=["GET", "POST"])
def login():
    print(current_user.is_authenticated)
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
        print(user_id, password)
        try:
            user = get_user_def(user_id)
            print(f"user in login form {user}")
            db.execute(user).first()
        except NoUserError:
            flash(NO_USER)
            return redirect(url_for("auth.login"))
        print(f"scalars {db.scalars(user)}")

        if check_password(password, "user".password):
            user = get_user_def(user_id)
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
