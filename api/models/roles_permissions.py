
from api.models.base import db

roles_permissions=db.Table('roles_permissions',
                           db.Column('role_id',db.Integer,db.ForeignKey('roles.id')),
                           db.Column('permission_id',db.Integer,db.ForeignKey('permission.id'))
                           )