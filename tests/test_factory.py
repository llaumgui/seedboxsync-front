from seedboxsync_front.app import create_app


def test_config(app):
    assert not create_app().testing
    assert app.testing


def test_wrapper(app):
    assert create_app
