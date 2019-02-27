from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.models.base import Base, db


class Reply(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    content = Column(String(300), nullable=False)

    suggestionId=Column(Integer,db.ForeignKey('suggestions.id'))
    suggestion=db.relationship('Suggestions')

    replyPersonId=Column(Integer,db.ForeignKey('user.userid'))
    replyPerson=db.relationship('User',back_populates='myReplySuggestions')