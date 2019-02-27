from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from api.models.base import Base, db


class Post(Base):
    id = Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(60))
    body=Column(Text)
    time=Column(DateTime,default=datetime.now)
    pubPersonId=Column(Integer,db.ForeignKey('user.userid'))
    pubPerson=db.relationship('User',back_populates='posts')
    status=Column(SmallInteger,default=1)