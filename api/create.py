from flask import Flask

from api.libs.Command import register_commands
from api.libs.Login import login_manager
from api.mina import create_blueprint_mina
from api.models.base import db
from api.web import create_blueprint_web


def register_blueprints(app):
    app.register_blueprint(create_blueprint_mina(),url_prefix='/mina')
    app.register_blueprint(create_blueprint_web(),url_prefix='/web')


def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config.setting')
    app.config.from_object('api.config.secure')
    register_blueprints(app)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
    login_manager.init_app(app)
    register_commands(app)
    return app

