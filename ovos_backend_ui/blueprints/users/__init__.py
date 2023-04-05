from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required

users = Blueprint("users", __name__, template_folder="templates", static_folder="static")

@users.route("/")
@login_required
def index():
    page_data = {}
    return render_template("users.html", **page_data)
