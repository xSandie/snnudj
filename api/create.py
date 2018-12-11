from flask import Flask

from api.mina import create_blueprint_mina
from api.web import create_blueprint_web


def register_blueprints(app):
    app.register_blueprint(create_blueprint_mina(),url_prefix='/mina')
    app.register_blueprint(create_blueprint_web(),url_prefix='/web')


def create_app():
    app = Flask(__name__)
    register_blueprints(app)

    return app

