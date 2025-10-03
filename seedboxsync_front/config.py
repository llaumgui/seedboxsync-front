# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import Flask
import os
import yaml


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


def init_config(app: Flask) -> None:
    # Set from env prefixed by 'FLASK_'
    app.config.from_prefixed_env()  # From env préfix by 'FLASK_'

    # SECRET_KEY warning
    if app.config.get('SECRET_KEY') is None:
        app.logger.warning('Warning: SECRET_KEY is still not set. Set it in production to secure your sessions.')

    # Init Flask Cache
    app.config.setdefault('CACHE_TYPE', 'SimpleCache')

    # Load config from SeedboxSync yaml
    yaml_config = __load_yaml_config()
    if not yaml_config:
        app.config['INIT_ERROR'] = "No SeedboxSync configuration file found!"
        app.logger.error('No SeedboxSync configuration file found!')

    app.config.update(yaml_config)
