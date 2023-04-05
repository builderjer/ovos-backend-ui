from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user

from ovos_local_backend.configuration import CONFIGURATION

from decorators import admin_required
from info import TOOLTIPS

backend = Blueprint("backend", __name__, template_folder="templates", static_folder="static")

@backend.route("/")
@admin_required
def index():
    page_data = {
        "navbar_button_icon": "icon_im-user",
        "navbar_button_title": "BACK",
        "navbar_button_url": url_for("admin.index"),
        "navbar_button_icon": "icon_edit-reset",
        "anonymous": current_user.is_authenticated(),
        "page_title": "ADMINISTRATION",
        "tooltips": TOOLTIPS,
        "changes": False,
        "skip_auth": not CONFIGURATION['skip_auth'],
        "override_location": CONFIGURATION['override_location'],
        "geolocate": CONFIGURATION['geolocate'],
        "selene_proxy": CONFIGURATION['selene']['enabled'],
        "tts_ids": {
            "default": CONFIGURATION['default_tts'],
            "avaliable": list(CONFIGURATION['tts_configs'].keys())
            },
        "ww_ids": {
            "default": CONFIGURATION['default_ww'],
            "avaliable": list(CONFIGURATION['ww_configs'].keys())
            },
        "date_format": {
            "default": CONFIGURATION['date_format'],
            "avaliable": ['MDY', 'DMY']
            },
        "system_unit": {
            "default": CONFIGURATION['system_unit'],
            "avaliable": ['metric', 'imperial']
            },
        "time_format": {
            "default": CONFIGURATION['time_format'],
            "avaliable": ['long', 'short']
            },
        "functions": {

            }
        }
    return render_template("backend_config.html", **page_data)
