# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import os
import yaml
from flask import Flask, Response, request
from .controlers import bp as bp_frontend, error as error_front
from .controlers.api import bp as bp_api, error as error_api
from . import db
from . import cache

__version__ = "1.0.0b1"

CONFIG_PATHS = [
    os.path.expanduser("~/.config/seedboxsync/seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync.yml"),
    os.path.expanduser("~/.seedboxsync/config/seedboxsync.yml"),
    "/etc/seedboxsync/seedboxsync.yml",
]


def __load_yaml_config() -> dict:  # type: ignore[type-arg]
    """
    Load config from the seedboxsync cli yaml.
    """
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            with open(path, "r") as f:
                return yaml.safe_load(f)  # type: ignore[no-any-return]
    return {}


def __handle_http_exception(e: Exception) -> tuple[Response, int | None] | tuple[str, int | None]:
    """
    Global 404 handler.
    Return JSON for /api routes, else return frontend template.
    """
    if request.path.startswith("/api"):
        return error_api.error(e)
    return error_front.error(e)


def create_app() -> Flask:
    """
    Flask create app.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cache.cache.init_app(app)

    # Set SECRET_KEY
    app.config.from_prefixed_env()  # From env préfix by 'FLASK_'
    if app.config['SECRET_KEY'] is None:
        app.logger.warning('Warning: SECRET_KEY is still set to "dev". Change it in production to secure your sessions.')
        app.config['SECRET_KEY'] = 'dev'

    # Load config from SeedboxSync yaml
    yaml_config = __load_yaml_config()
    if not yaml_config:
        app.config['INIT_ERROR'] = "No SeedboxSync configuration file found!"
        app.logger.error('No SeedboxSync configuration file found!')
    app.config.update(yaml_config)

    # DB lazly loading
    db.get_db(app)

    # Register blueprint and error handler
    app.register_blueprint(bp_frontend)
    app.register_blueprint(bp_api)
    app.register_error_handler(Exception, __handle_http_exception)  # type: ignore[arg-type]

    return app
