from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, static_folder='static')

@auth.route('/')
def index():
    return render_template('auth.html')
