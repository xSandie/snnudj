import click
from flask import Flask
from flask.cli import AppGroup, with_appcontext

from api.libs.Login import login_manager
from api.mina import create_blueprint_mina
from api.models.Permission import Permission
from api.models.Roles import Roles
from api.models.User import User
from api.models.base import db
from api.web import create_blueprint_web


def create_app():
    app = Flask(__name__)
    app.config.from_object('api.config.setting')
    app.config.from_object('api.config.secure')
    register_blueprints(app)
    db.init_app(app)
    login_manager.init_app(app)
    # print(OS_PATH)
    # FlaskCLI(app)
    register_shell_context(app)
    register_commands(app)
    # app.cli.add_command(app)


    return app

def register_blueprints(app):
    app.register_blueprint(create_blueprint_mina(),url_prefix='/mina')
    app.register_blueprint(create_blueprint_web(),url_prefix='/web')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app,db=db, User=User, Permission=Permission, Roles=Roles)



def register_commands(app):
    @app.cli.command('init')
    def init():
        # 创建第一个管理员
        click.echo("Initializing roles and permissions")
        Roles.init_role()

        click.echo("Initializing the first admin")
        with db.auto_commit():
            admin = User()
            admin.username = '马正平'
            admin.userPhone = '18349250473'
            admin.password = 'Mzp12345678'
            admin.admin = True
            admin.roleId=Roles.Administrator
            db.session.add(admin)
        click.echo("Done")

    @app.cli.command('initdb')
    def initdb():
        click.echo("Initializing the database")
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo("Done")


