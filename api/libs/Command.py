import click

from api.models.Permission import Permission
from api.models.Roles import Roles
from api.models.User import User
from api.models.base import db


# def register_commands(app):
#     @app.cli.command()
#     def init():
#         #创建第一个管理员
#         # click.echo("Initializing the first admin")
#         # admin=User()
#         # admin.username='马正平'
#         # admin.userPhone='18349250473'
#         # admin.password='Mzp12345678'
#         # db.session.add(admin)
#         # db.auto_commit()
#         # click.echo("Done")
#
#         click.echo("Initializing roles and permissions")
#         init_role()
#         click.echo("Done.")



if __name__=='__main__':
    # def init_role():
    roles_permissions_map={
        'User':['LOOK','PUBSIGNIN'],
        'Moderator':['LOOK','PUBSIGNIN','UPLOAD','DELSELF'],
        'Administrator':['LOOK','PUBSIGNIN','UPLOAD','CREATEOTHER','DELOTHER']
    }

    for role_name in roles_permissions_map:
        print(role_name)
        print(str(roles_permissions_map[role_name]))
        role = Roles.query.filter_by(name=role_name).first()
        if role is None:
            role = Roles()
            role.name=role_name
            db.session.add(role)
        role.permissions=[]
        for permission_name in roles_permissions_map[role_name]:
            permission=Permission.query.filter_by(name=permission_name)
            if permission is None:
                permission = Permission(name=permission_name)
                db.session.add(permission)
            role.permissions.append(permission)
    db.session.commit()