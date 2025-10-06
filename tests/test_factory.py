from seedboxsync_front import create_app


def test_config(app):
    assert not create_app().testing
    assert app.testing
