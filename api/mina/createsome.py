from api.libs.redprint import Redprint
from api.models.Permission import Permission
from api.models.Roles import Roles
from api.models.base import db

create = Redprint('create')

@create.route('/create',methods=['POST'])
def init_role():
    roles_permissions_map = {
        'User': ['LOOK', 'PUBSIGNIN'],
        'Moderator': ['LOOK', 'PUBSIGNIN', 'UPLOAD', 'DELSELF'],
        'Administrator': ['LOOK', 'PUBSIGNIN', 'UPLOAD', 'CREATEOTHER', 'DELOTHER']
    }

    for role_name in roles_permissions_map:
        print(role_name)
        print(str(roles_permissions_map[role_name]))
        role = Roles.query.filter_by(name=role_name).first()
        # role = None
        if role is None:
            role = Roles()
            role.name = role_name
            db.session.add(role)
        role.permissions = []
        for permission_name in roles_permissions_map[role_name]:
            permission = Permission.query.filter_by(name=permission_name).first()
            if permission is None:
                permission = Permission()
                permission.name=permission_name
                db.session.add(permission)
            print(permission)
            role.permissions.append(permission)
    db.session.commit()

    return 'ok'