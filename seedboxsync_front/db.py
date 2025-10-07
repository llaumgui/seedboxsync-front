# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import Flask
from peewee import SqliteDatabase
from seedboxsync.core.dao.model import global_database_object
from .utils import sizeof, byte_to_gi
import os


class Database(object):
    """
    Database connector using peewee.

    Attributes:
        app (Flask): The database object.
    """

    def __init__(self, app: Flask):
        """
        Initialize a new Database instance.

        Args:
            app (Flask): The database object.
            database (SqliteDatabase | None): The database object.
        """
        self.app = app
        self.dbProxy = global_database_object
        self.__load_database()
        self.__register_handlers()
        self.__register_functions()

    def __load_database(self) -> None:
        """
        Load SeedboxSync DB from SeedboxSyncFront.
        """

        # Get DB from config
        db_file = self.app.config['DATABASE']

        if not os.path.exists(db_file):
            self.app.logger.error('No database %s found', db_file)
            self.app.config['INIT_ERROR'] = "Can't load seedbox database!"
        else:
            self.db = SqliteDatabase(db_file)
            global_database_object.initialize(self.db)
            self.app.logger.debug('Use database %s', db_file)

    def __close_db(self, exc: BaseException | None = None) -> None:
        """
        Close database.

        Args:
            exc (BaseException  | None): An exception.
        """
        if self.dbProxy is not None and not self.dbProxy.is_closed():
            self.dbProxy.close()

    def __register_handlers(self) -> None:
        """
        Register DB hanlers.
        """
        self.app.teardown_request(self.__close_db)

    def __register_functions(self) -> None:
        """
        Register DB functions.
        """
        @self.db.func('byte_to_gi')  # type: ignore
        def db_byte_to_gi(num: float, suffix: str = 'B') -> str:
            return byte_to_gi(num, suffix)

        @self.db.func('sizeof')  # type: ignore
        def db_sizeof(num: float, suffix: str = 'B') -> str:
            return sizeof(num, suffix)
