from time import sleep

from flask import Flask, request, redirect, url_for, render_template, flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user

try:
    from .database import DEFAULT_DATABASE
    from .users import User
    from .configuration import SECRET_KEY
    from .exceptions import NoUserError
    from .decorators import admin_required
    from .tooltips import tooltips
    from .backend import TTS_IDS, WW_IDS
except ImportError:
    from database import DEFAULT_DATABASE
    from users import User
    from configuration import SECRET_KEY
    from exceptions import NoUserError
    from decorators import admin_required
    from tooltips import tooltips
    from backend import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@app.route('/')
def index():
    if not DEFAULT_DATABASE.admin_users:
        return "setup admin user first"
    session.pop('_flashes', None)
    # au = []
    # for user in DEFAULT_DATABASE.admin_users:
    #     au.append(user['id'])
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    @admin_required(current_user.user_id)
    def display():
        page_data = {
            'page_title': 'ADMIN CONTROLS',
            'user_id': current_user.user_id
            }
        return render_template('admin.html', **page_data)
    return display or flash_admin()

@app.route('/user_page')
@login_required
def user_login():
    page_data = {'page_title': 'USER CONTROLS'}
    return render_template('user.html', **page_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    page_data = {'page_title': 'LOGIN'}
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        try:
            registerd_user = DEFAULT_DATABASE.get_user(user_id)[0]
        except NoUserError:
            flash(f'No user {user_id} in database')
            return render_template('login.html', **page_data)
        if User.check_password(password, registerd_user['password']):
            user = User.user_from_db(registerd_user)
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user_page'))
        else:
            flash('Username and Password Mismatch', 'error')
    return render_template('login.html', **page_data)

@app.route("/backend")
@login_required
def backend():
    page_data = {
        "page_title": "Backend Config",
        "tooltips": tooltips,
        "tts_ids": {
            "default": DEFAULT_TTS,
            "avaliable": TTS_IDS
            },
        "ww_ids": {
            "default": DEFAULT_WW,
            "avaliable": WW_IDS}
        }
    return render_template("backend.html", **page_data)

@app.route('/config_change', methods=['POST'])
def config_change():
    key = request.args['config_key']
    rval = request.args['config_value']
    value = request.form.get(request.args['config_value'])
    print(f"start of route /config_change {key} {rval} {value}")
    if request.args.get('reverse_bool'):
        value = reverse_bool(value)
    if request.args.get('parse_bool'):
        print(f"in args.get('parse_bool') {rval}")
        value = parse_bool(value)
    print(f"end of route /config_change {key}, {value}")
    change_config(key, value)
    return '', 204

@app.errorhandler(401)
def page_not_found(e):
    return 'Login Failed'

@login_manager.user_loader
def load_user(user_id):
    return User.user_from_db(DEFAULT_DATABASE.get_user(user_id)[0])

def flash_admin():
    print("flash_admin")
    flash("You must be an Admin to view this page")
    return redirect(url_for('user_page'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9876, debug=True)
