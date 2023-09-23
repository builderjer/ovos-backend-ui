from ovos_config import Configuration
from js2py import translate_file
import os
from pathlib import Path
import os.path
import requests

from ovos_config.utils import init_module_config

init_module_config("ovos_backend_ui",
                   "ovos_backend_ui",
                   {"config_filename": "ovos_backend.conf",
                    "base_folder" :"ovos_backend",
                    "default_config_path": f"{os.path.dirname(__file__)}/ovos_backend.conf"})

ADMIN = Configuration()["server"]["admin_key"]
VERSION = Configuration()["server"]["version"]
HOST = Configuration()["server"].get("url", "localhost")
PORT = Configuration()["server"].get("port", "6712")
HEADERS = {
            "Authorization": f"Bearer {ADMIN}"
            }
URL = f"{HOST}:{PORT}/{VERSION}"
# DEFAULT_TTS = Configuration()['default_tts']
# TTS_IDS = list(Configuration()['tts_configs'].keys())
#
# DEFAULT_WW = Configuration()['default_ww']
# WW_IDS = list(Configuration()['ww_configs'].keys())
#
# AUTH = Configuration()['skip_auth']
# DATE_FORMAT = Configuration()['date_format']
# TIME_FORMAT = Configuration()['time_format']
# GEOLOCATE = Configuration()['geolocate']
# OVERRIDE_LOCATION = Configuration()['override_location']

# functions
def change_config(key_to_change, new_value):
    print(key_to_change, new_value)
    try:
        Configuration()[key_to_change] = new_value
        Configuration().store()
        Configuration().reload()
    except:
        pass

def reverse_bool(bool_value):
    if bool_value:
        new_value = 'false'
    else:
        new_value = 'true'
    return new_value

def parse_bool(bool_value):
    print(f"in parse_bool {bool_value}")
    if bool_value:
        new_value = 'true'
    else:
        new_value = 'false'
    print(f"new_value in parse_bool {new_value}")
    return new_value
