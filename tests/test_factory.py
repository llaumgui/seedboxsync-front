from seedboxsync_front import create_app
from seedboxsync_front.app import create_app as app_create_app


def test_config(app):
    assert not create_app().testing
    assert app.testing


def test_wrapper(app):
    assert app_create_app
