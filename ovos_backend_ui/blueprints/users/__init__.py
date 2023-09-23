from passlib.context import CryptContext

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required

from sqlalchemy.orm import Session

from ovos_backend_ui.database import User, db, add_new_user, encrypt_password, check_password

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
        )

users = Blueprint("users", __name__, template_folder="templates", static_folder="static")

@users.route("/")
@login_required
def index():
    page_data = {}
    return render_template("users.html", **page_data)

@users.route("/newuser")
def newuser():
    page_data = {}
    return render_template("new_user_short.html", **page_data)

@users.route("/adduser", methods=["POST"])
def adduser():
    user_data = request.form
    add_new_user(
        display_name=user_data["user_id"],
        password=encrypt_password(user_data["password"]),
        is_admin=True
        )
    # db.add(new_user)
    # db.commit()
    return redirect(url_for("auth.login"))

