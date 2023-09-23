import os.path

from ovos_config.utils import init_module_config
from ovos_utils.log import LOG

init_module_config("ovos_backend_ui",
                   "backend_ui",
                   {"config_filename": "ovos_backend_ui.conf",
                    "base_folder" :"ovos_backend",
                    "default_config_path": f"{os.path.dirname(__file__)}/ovos_backend_ui.conf"})

from ovos_backend_ui.setup_app import start_backend_ui
