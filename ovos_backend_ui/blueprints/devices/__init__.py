from uuid import uuid4

from flask import Blueprint, render_template, redirect, request, url_for

from flask_login import current_user, login_required

from ovos_local_backend.configuration import CONFIGURATION
from ovos_local_backend.database.settings import DeviceDatabase
from ovos_local_backend.utils import generate_code

try:
    # lingua_franca is optional
    from lingua_franca.internal import get_supported_langs, get_full_lang_code
    SUPPORTED_LANGS = get_supported_langs()
except ImportError:
    SUPPORTED_LANGS = ['en-us']

try:
    from decorators import admin_required
    from info import TOOLTIPS
except ImportError:
    from ovos_backend_ui.decorators import admin_required
    from ovos_backend_ui.info import TOOLTIPS

devices = Blueprint("devices", __name__, template_folder="templates", static_folder="static")

@devices.route("/")
def index():
    devices = {uuid: f"{device['name']}@{device['device_location']}"
            for uuid, device in DeviceDatabase().items()}
    print(devices.keys())

    page_data = {
        "navbar_button_url": url_for('admin.index'),
        "navbar_button_title": "BACK",
        "navbar_button_icon": "icon_edit-reset",
        "page_title": "DEVICE CONFIGURATION",
        "anonymous": True,
        "devices": devices
            }
    return render_template("device_config.html", **page_data)

@devices.route("/pair_new_device")
def pair_new_device():
    page_data = {
        "navbar_button_url": url_for('devices.index'),
        "navbar_button_title": "BACK",
        "navbar_button_icon": "icon_edit-reset",
        "page_title": "NEW DEVICE",
        "anonymous": current_user.is_authenticated,
        "tooltips": TOOLTIPS,
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
        "supported_langs": {
            "avaliable": get_lang_html()
            }
        }
    return render_template("new_device.html", **page_data)

@devices.route("pair_device", methods=["POST"])
def pair_device():
    # for d in request.form:
    #     print(d)
    instant_pair(request.form)
    return redirect("/devices")

def instant_pair(device_info=None):
    uuid = str(uuid4())
    code = generate_code()
    token = f"{code}:{uuid}"
    for d in device_info:
        print(d)
    with DeviceDatabase() as db:
        db.add_device(uuid, token,
                      name = device_info.get("device_name") or None,
                      device_location = device_info.get("device_placement") or None,
                      opt_in = device_info.get("opt_in") or False,
                      time_format = device_info.get("date_format") or None,
                      email = device_info.get("email") or None,
                      isolated_skills = device_info.get("isolated_skills") or None,
                      default_ww = device_info.get("default_ww") or "hey mycroft",
                      default_tts = device_info.get("default_tts") or "ovos-tts-plugin-mimic2",
                      )
    # with DeviceDatabase() as db:
    #     db.add_device(uuid, token)

def show_devices():
    print(DeviceDatabase())

def get_lang_html():
    # Changes the html from dropdown to textbox if lingua_franca not avaliable
    loc = CONFIGURATION["default_location"]["city"]["state"]["country"]["code"].lower()
    if len(SUPPORTED_LANGS) > 1:
        html = """
            <tr class="table_value">
                <th title="">Language</th>
                <td>
                    <select id="lang_dropdown" class="bkend_dropdown" name="lang_dropdown">
                """
        for lang in SUPPORTED_LANGS:
            full_lang = get_full_lang_code(lang)
            if loc in full_lang:
                cl = "selected"
                print("YUP")
            else:
                cl = ""
            html = f"""{html}
                        <option value="{full_lang}" {cl}>{full_lang}</option>
                    """
        html = f"""{html}
                </select>
                </td>
            </tr>
            """
        return html
    else:
        return """
            <tr class="table_value">
                <th title="">Language</th>
                <td>
                    <input id="language" type="text" placeholder="en-us" class="table_text_value" name="language">
                </td>
            </tr>
            """
