# -*- encoding: utf-8 -*-
"""



"""

import boto3, os
from flask import Flask
from flaskext.markdown import Markdown
from flask_login import LoginManager
from importlib import import_module

REGION = os.environ.get("TABLE_REGION")

db = boto3.resource('dynamodb', region_name = REGION)
login_manager = LoginManager()


def register_extensions(app):
    Markdown(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app():
    app = Flask(__name__)
    app.secret_key = "something"
    register_extensions(app)
    register_blueprints(app)
    return app
