from datetime import datetime

from sqlalchemy import Column, BigInteger, ForeignKey, Integer, Time, String
from sqlalchemy.orm import relationship

from api.models.base import Base


class SignInPeople(Base):
    id = Column(Integer,autoincrement=True,primary_key=True)

    signInOrderId=Column(Integer,ForeignKey('sign_in_order.id'))
    signInOrder=relationship('SignInOrder',back_populates='signInPerson')

    userId=Column(Integer,index=True,nullable=False)
    username = Column(String(20))
    userPhone = Column(String(20), index=True)

    signInTime=Column(Time)
    # Time 	datetime.time 	时间

    def generate_signInTime(self):
        return datetime.time(datetime.now())#17:51:30.854656修改
