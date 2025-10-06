import os

import pytest
from seedboxsync_front import create_app


@pytest.fixture
def app():
    """
    Create app fixture
    """
    db_path = os.path.join(os.path.dirname(__file__), 'resources/seedboxsync.db')

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'pytest',
        'CACHE_TYPE': 'NullCache',
        'BABEL_DEFAULT_LOCALE': 'en'
    })
    yield app


@pytest.fixture
def client(app):
    """
    Create client fixture
    """
    return app.test_client()
