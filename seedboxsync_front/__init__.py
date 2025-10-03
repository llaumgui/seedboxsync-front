# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import Flask, Response, request
from .controlers import bp as bp_frontend, error as error_front
from .controlers.api import bp as bp_api, error as error_api
from . import db
from .cache import cache
from .config import init_config

__version__ = "1.0.0b1"


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
    init_config(app)

    # Cache lazly loading
    cache.init_app(app)

    # DB lazly loading
    db.get_db(app)

    # Register blueprint and error handler
    app.register_blueprint(bp_frontend)
    app.register_blueprint(bp_api)
    app.register_error_handler(Exception, __handle_http_exception)  # type: ignore[arg-type]

    return app
