from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.models.Permission import Permission
from api.models.base import Base, db
from api.models.roles_permissions import roles_permissions


class Roles(Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(30),unique=True)

    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')#在对方那叫做roles
    users=db.relationship('User',back_populates='role')

    Administrator=3
    Moderator=2
    User=1

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'User': ['LOOK', 'PUBSIGNIN'],
            'Moderator': ['LOOK', 'PUBSIGNIN', 'UPLOAD', 'DELSELF'],
            'Administrator': ['LOOK', 'PUBSIGNIN', 'UPLOAD', 'CREATEOTHER', 'DELOTHER']
        }

        for role_name in roles_permissions_map:
            # print(role_name)
            # print(str(roles_permissions_map[role_name]))
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
                    permission.name = permission_name
                    db.session.add(permission)
                # print(permission)
                role.permissions.append(permission)
        db.session.commit()



