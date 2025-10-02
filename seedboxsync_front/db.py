# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import os
from flask import Flask
from peewee import SqliteDatabase
from cement.utils import fs
from seedboxsync.core.dao.model import global_database_object
from .utils import sizeof, byte_to_gi


def get_db(app: Flask) -> None:
    """
    Load SeedboxSync DB from SeedboxSyncFront
    :param app: Flask application.
    """
    db_file = fs.abspath(str((app.config.get('local') or {}).get('db_file', 'default.db')))

    if not os.path.exists(db_file):
        app.logger.error('No database %s found', db_file)
        app.config['INIT_ERROR'] = "Can't load seedbox database!"
    else:
        app.logger.debug('Use database %s', db_file)
        db = SqliteDatabase(db_file)
        global_database_object.initialize(db)

        @db.func('sizeof')  # type: ignore
        def db_sizeof(num: float, suffix: str = 'B') -> str:
            return sizeof(num, suffix)

        @db.func('byte_to_gi')  # type: ignore
        def db_byte_to_gi(num: float, suffix: str = 'B') -> str:
            return byte_to_gi(num, suffix)
