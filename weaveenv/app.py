import eventlet
eventlet.monkey_patch()  # NOLINT

import logging
import os
import signal
import sys

import appdirs

from weaveenv.database import PluginsDatabase
from weaveenv.http import WeaveHTTPServer
from weaveenv.plugins import PluginManager, get_plugin_id, VirtualEnvManager
from weaveenv.plugins import PluginInfoFilter


logging.basicConfig()


def get_config_path():
    if os.environ.get("WEAVE_DIR"):
        return os.environ["WEAVE_DIR"]

    weave_base = appdirs.user_data_dir("homeweave")
    try:
        os.makedirs(weave_base)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return os.path.join(weave_base, "weaveenv.db")


def handle_main():
    plugins_db = PluginsDatabase(os.path.join(get_config_path(), "db"))
    plugin_manager = PluginManager(get_config_path(), plugins_db)
    http_modules = [
        ("/plugins", plugin_manager),
    ]
    plugin_manager.start()
    http = WeaveHTTPServer(http_modules)

    http.run(port=15000, host="")


def handle_messaging_token():
    plugins_db = PluginsDatabase(os.path.join(get_config_path(), "db"))
    plugins_db.start()

    messaging_server_url = "https://github.com/HomeWeave/WeaveServer.git"
    if sys.argv[1] == 'set':
        plugins_db.insert(app_id=get_plugin_id(messaging_server_url),
                          app_secret_token=sys.argv[2], is_remote=True)
    elif sys.argv[1] == 'get':
        plugin_data = plugins_db.query(get_plugin_id(messaging_server_url))
        print(plugin_data.app_secret_token)
    else:
        print("Supported operations: 'get' and 'set'")


def handle_weave_launch():
    plugin_dir = sys.argv[1]
    os.chdir(plugin_dir)
    sys.path.append(plugin_dir)

    token = sys.stdin.readline().strip()

    venv_path = sys.argv[2]
    venv = VirtualEnvManager(venv_path)
    venv.activate()

    filt = PluginInfoFilter()
    plugin_info = filt.filter(dict(installed=True, install_path=plugin_dir))
    app = plugin_info["cls"](token, plugin_info["config"], venv_path)

    signal.signal(signal.SIGTERM, lambda x, y: app.on_service_stop())
    signal.signal(signal.SIGINT, lambda x, y: app.on_service_stop())

    app.before_service_start()
    app.on_service_start()
