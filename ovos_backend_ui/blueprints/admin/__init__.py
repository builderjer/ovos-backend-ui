from copy import copy, deepcopy
import subprocess

from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import current_user

from ovos_local_backend.configuration import CONFIGURATION
from ovos_utils.json_helper import merge_dict

try:
    from decorators import admin_required
    from info import TOOLTIPS
except ImportError:
    from ovos_backend_ui.decorators import admin_required
    from ovos_backend_ui.info import TOOLTIPS

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

UNAPPLIED_CHANGES = []
# Get the settings from the backend server


@admin.route("/")
@admin_required
def index():
    default_data = copy(get_new_data())
    new_data = {
        "navbar_button_url": url_for('auth.logout'),
        "page_title": "ADMINISTRATION",
        "navbar_button_title": "LOGOUT",
        "anonymous": current_user.is_authenticated()
            }
    page_data = merge_dict(default_data, new_data)
    return render_template("admin.html", **page_data)


@admin.route("/test", methods=["POST"])
@admin_required
def test():
    bool_list = ["dev_auth", "geolocate", "override_location"]
    for k in request.form:
        # Take care of the bool values
        if k in bool_list: # Checkbox is checked
            # Change value in CONFIGURATION
            # dev_auth must be reversed
            if k == "dev_auth":
                CONFIGURATION["skip_auth"] = False
            else:
                CONFIGURATION[k] = True
            # Get rid of them from the list once processed
            bool_list.remove(k)
        # Go through the rest of the form that IS NOT a bool
        else:
            CONFIGURATION[k] = request.form.get(k)
    # Cycle through the rest of the bool_list that ARE NOT in the form
    for bl in bool_list:
        # Still have to deal with dev_auth
        if bl == "dev_auth":
            CONFIGURATION["skip_auth"] = True
        else:
            CONFIGURATION[bl] = False
        # Save the configuration
        CONFIGURATION.store()
    subprocess.call("sudo systemctl restart local_backend", shell=True)
    return redirect(url_for("backend.index"))

def changes_made(changed_setting):
    UNAPPLIED_CHANGES.append(changed_setting)
    print(f"in changes made {UNAPPLIED_CHANGES}")

def check_bool(bool_to_check):
    if bool_to_check:
        print(f"true in check_bool {bool_to_check}")
        return 'true'
    print(f"false in check_bool {bool_to_check}")
    return 'false'

def reverse_bool(bool_to_reverse):
    if bool_to_reverse:
        return 'false'
    return 'true'

def get_new_data():
    DEFAULT_PAGE_DATA = {
                "navbar_button_icon": "icon_im-user",
                "navbar_button_title": "LOGOUT",
                "navbar_button_url": '',
                "anonymous": True,
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
                    "changes_made": changes_made
                    }
                }
    return DEFAULT_PAGE_DATA
