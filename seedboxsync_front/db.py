import os
from peewee import SqliteDatabase
from cement.utils import fs
from seedboxsync.core.dao.model import global_database_object

"""
Load SeedboxSync DB from SeedboxSyncFront
"""
def get_db(app):
    db_file = fs.abspath(app.config.get('local').get('db_file'))

    if os.path.exists(db_file):
        db = SqliteDatabase(db_file)
        global_database_object.initialize(db)
    else:
        app.config['INIT_ERROR'] = "Can't load seedbox database!"
