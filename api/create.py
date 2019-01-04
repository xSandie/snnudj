import click
from faker import Faker
from flask import Flask


from api.libs.Login import login_manager
from api.mina import create_blueprint_mina
from api.models.Permission import Permission
from api.models.Post import Post
from api.models.Roles import Roles
from api.models.User import User
from api.models.base import db
from api.web import create_blueprint_web


def create_app():
    app = Flask(__name__,static_folder='../static')
    app.config.from_object('api.config.setting')
    app.config.from_object('api.config.secure')
    register_blueprints(app)
    db.init_app(app)
    login_manager.init_app(app)

    register_shell_context(app)
    register_commands(app)

    #向jinjia注册自定义函数
    env = app.jinja_env
    env.filters['int_to_datetime'] = int_to_datetime

    return app

def register_blueprints(app):
    app.register_blueprint(create_blueprint_mina(),url_prefix='/mina')
    app.register_blueprint(create_blueprint_web(),url_prefix='/web')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app,db=db, User=User, Permission=Permission, Roles=Roles)



def register_commands(app):
    @app.cli.command('initAdmin')
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

        click.echo("Initializing the first moderator")
        with db.auto_commit():
            admin = User()
            admin.username = '张筠瑶'
            admin.userPhone = '15594989021'
            admin.password = '12345678'
            admin.admin = True
            admin.roleId = Roles.Moderator
            db.session.add(admin)
        click.echo("Done")

    @app.cli.command('initdb')
    def initdb():
        click.echo("Initializing the database")
        with app.app_context():
            db.drop_all()
            db.create_all()
        click.echo("Done")

    @app.cli.command('forge')
    @click.option('--count',default=20,help='生成数量')
    def forge(count):
        fake=Faker(locale='zh_CN')
        click.echo('生成中')

        for item in range(count):
            post=Post()
            post.title=fake.sentence(nb_words=20)
            post.time=fake.date_time_this_year()
            post.body='<p>'+fake.text()+'</p>'
            post.pubPersonId=1
            db.session.add(post)
        db.session.commit()
        click.echo('Done')



def int_to_datetime(day_int):
    import time, datetime
    timeArray = time.localtime(day_int)  # 1970秒数
    # print(timeArray)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    new_datetime = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d %H:%M:%S")
    return new_datetime
