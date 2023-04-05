from ovos_local_backend.configuration import CONFIGURATION
from js2py import translate_file
import os
from pathlib import Path

DEFAULT_TTS = CONFIGURATION['default_tts']
TTS_IDS = list(CONFIGURATION['tts_configs'].keys())

DEFAULT_WW = CONFIGURATION['default_ww']
WW_IDS = list(CONFIGURATION['ww_configs'].keys())

AUTH = CONFIGURATION['skip_auth']
DATE_FORMAT = CONFIGURATION['date_format']
TIME_FORMAT = CONFIGURATION['time_format']
GEOLOCATE = CONFIGURATION['geolocate']
OVERRIDE_LOCATION = CONFIGURATION['override_location']

# functions
def change_config(key_to_change, new_value):
    print(key_to_change, new_value)
    try:
        CONFIGURATION[key_to_change] = new_value
        CONFIGURATION.store()
        CONFIGURATION.reload()
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
