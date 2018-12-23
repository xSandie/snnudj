# -*- coding:utf-8 -*- 
from sqlalchemy import Integer, Column, String

from api.models.base import Base


class WXToken(Base):
    id=Column(Integer,primary_key=True,autoincrement=True)
    token=Column(String(200))