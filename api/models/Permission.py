from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.models.base import Base, db
from api.models.roles_permissions import roles_permissions


class Permission(Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(30),unique=True)

    roles=db.relationship('Roles',secondary=roles_permissions,back_populates='permissions')