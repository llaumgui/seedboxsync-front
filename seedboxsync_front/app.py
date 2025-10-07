# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
#
from flask import Flask, Response, request
from flask_babel import Babel
from .controlers import bp as bp_frontend, error as error_front
from .controlers.api import bp as bp_api, error as error_api
from .db import Database
from .cache import cache
from .config import Config
from .utils import get_locale


def __handle_http_exception(e: Exception) -> tuple[Response, int | None] | tuple[str, int | None]:
    """
    Global 404 handler.

    Returns:
        tuple[Response, int | None] | tuple[str, int | None]: JSON for /api routes, else return frontend template.
    """
    if request.path.startswith("/api"):
        return error_api.error(e)
    return error_front.error(e)


def create_app(test_config: dict[str, str] | None = None) -> Flask:
    """
    Flask create app.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    Config(app, test_config)

    # Babel lazy loading
    Babel(app, locale_selector=get_locale)

    # Cache lazy loading
    cache.init_app(app)

    # DB loading
    Database(app)

    # Register blueprint and error handler
    app.register_blueprint(bp_frontend)
    app.register_blueprint(bp_api)
    app.register_error_handler(Exception, __handle_http_exception)  # type: ignore[arg-type]

    return app


app = create_app()
