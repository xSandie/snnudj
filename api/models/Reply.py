from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.models.base import Base


class Reply(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    content = Column(String(300), nullable=False)

    suggestionId=Column(Integer,ForeignKey('suggestions.id'))
    suggestion=relationship('Suggestions')