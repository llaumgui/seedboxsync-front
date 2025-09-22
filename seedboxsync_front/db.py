import os
from peewee import SqliteDatabase
from cement.utils import fs
from seedboxsync.core.dao.model import global_database_object


def sizeof(num, suffix='B'):
    """
    Convert in human readable units.

    From: https://stackoverflow.com/a/1094933
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_db(app):
    """
    Load SeedboxSync DB from SeedboxSyncFront
    """
    db_file = fs.abspath(app.config.get('local').get('db_file'))

    if not os.path.exists(db_file):
        app.logger.error('No database %s found', db_file)
        app.config['INIT_ERROR'] = "Can't load seedbox database!"
    else:
        app.logger.debug('Use database %s', db_file)
        db = SqliteDatabase(db_file)
        global_database_object.initialize(db)

        @db.func('sizeof')
        def db_sizeof(num, suffix='B'):
            return sizeof(num, suffix)
