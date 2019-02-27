from sqlalchemy import Integer, Column, String, ForeignKey, BigInteger, SmallInteger
from sqlalchemy.orm import relationship

from api.models.base import Base, db


class Suggestions(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)

    title=Column(String(50),nullable=False)
    content=Column(String(300),nullable=False)

    sugPubPersonId=Column(Integer,db.ForeignKey('user.userid'))
    pubPerson=db.relationship('User',back_populates='myPubSuggestions')

    sugStatus=Column(SmallInteger,default=1)

    reply=db.relationship('Reply',uselist=False)

    IGNORE=0
    NOREPLY=1
    HAVEREPLY=2
