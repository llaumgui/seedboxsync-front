import os
import yaml
from flask import Flask
from .controlers import frontend
from .controlers import api
from . import db
from .controlers.page_not_found import page_not_found

__version__ = "1.0.0b1"

CONFIG_PATHS = [
    os.path.expanduser("~/.config/seedboxsync/seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync/config/seedboxsync.yml"),
    "/etc/seedboxsync/seedboxsync.yml",
]


def load_yaml_config():
    """
    Load config from the seedboxsync cli yaml.
    """
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            with open(path, "r") as f:
                return yaml.safe_load(f)
    return {}


def create_app(test_config=None):
    """
    Flask create app.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set SECRET_KEY
    app.config.from_prefixed_env()  # FRom env préfix by 'FLASK_'
    if app.config['SECRET_KEY'] is None:
        app.logger.warning('Warning: SECRET_KEY is still set to "dev". Change it in production to secure your sessions.')
        app.config['SECRET_KEY'] = 'dev'

    # Load config from SeedboxSync yaml
    yaml_config = load_yaml_config()
    if not yaml_config:
        app.config['INIT_ERROR'] = "No SeedboxSync configuration file found!"
        app.logger.error('No SeedboxSync configuration file found!')
    app.config.update(yaml_config)

    # DB lazly loading
    db.get_db(app)

    # Register blueprint and error handler
    app.register_blueprint(frontend.bp)
    app.register_blueprint(api.bp)
    app.register_error_handler(404, page_not_found)  # Utilisation de la fonction importée

    return app
