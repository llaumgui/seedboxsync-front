import os
#import yaml
from flask import Flask
from . import homepage
from .page_not_found import page_not_found

CONFIG_PATHS = [
    os.path.expanduser("~/.config/seedboxsync/seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync/config/seedboxsync.yml"),
    "/etc/seedboxsync/seedboxsync.yml",
]

#def load_yaml_config():
#    for path in CONFIG_PATHS:
#        if os.path.exists(path):
#            with open(path, "r") as f:
#                return yaml.safe_load(f)
#    return {}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Charger la config YAML
    #yaml_config = load_yaml_config()
    #app.config.update(yaml_config)

    app.register_blueprint(homepage.bp)
    app.register_error_handler(404, page_not_found)  # Utilisation de la fonction importée

    return app
