from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.models.base import Base
from api.models.roles_permissions import roles_permissions


class Roles(Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(30),unique=True)

    permissions = relationship('Permission', secondary=roles_permissions, back_populates='roles')#在对方那叫做roles
    users=relationship('User',back_populates='role')


