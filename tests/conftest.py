import os
import yaml
import pytest
import shutil
import tempfile
from seedboxsync_front import create_app


@pytest.fixture
def app():
    """
    Create app fixture
    """
    db_fd, tmp_db = tempfile.mkstemp()
    conf_fd, tmp_conf = tempfile.mkstemp()

    # Copy database
    test_db = os.path.abspath("tests/resources/seedboxsync.db")
    shutil.copy(test_db, tmp_db)

    # Copy and load config
    test_conf = os.path.abspath("tests/resources/seedboxsync.yml")
    shutil.copy(test_conf, tmp_conf)
    with open(tmp_conf, "r") as f:
        yaml_config = yaml.safe_load(f)  # type: ignore[no-any-return]

    app = create_app({
        'TESTING': True,
        'DATABASE': tmp_db,
        'SECRET_KEY': 'pytest',
        'CACHE_TYPE': 'NullCache',
        'BABEL_DEFAULT_LOCALE': 'en',
        'CONFIG_YAML_PATH': tmp_conf
    })
    app.config.update(yaml_config)  # Load YAML config
    yield app

    os.close(db_fd)
    os.close(conf_fd)
    os.unlink(tmp_db)


@pytest.fixture
def client(app):
    """
    Create client fixture
    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
