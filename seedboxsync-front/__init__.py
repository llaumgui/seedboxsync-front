import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import homepage
    app.register_blueprint(homepage.bp)

    return app
