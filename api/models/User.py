from flask_login import UserMixin
from flask_login._compat import text_type
from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

from api.models.Permission import Permission
from api.models.base import Base, db


class User(UserMixin,Base):
    userid=Column(Integer,primary_key=True,autoincrement=True)#主键
    username=Column(String(20))
    userPhone=Column(String(20),index=True)
    password_hash=Column(String(128))

    wxopenId=Column(String(100),index=True,nullable=True)

    roleId=Column(Integer,db.ForeignKey('roles.id'))
    role=db.relationship('Roles',back_populates='users')

    pubCount=Column(Integer,default=0)
    signInCount=Column(Integer,default=0)

    pubSignIns=db.relationship('SignInOrder',back_populates='pubPerson')

    myPubSuggestions=db.relationship('Suggestions',back_populates='pubPerson')

    myReplySuggestions=db.relationship('Reply',back_populates='replyPerson')

    posts=db.relationship('Post',back_populates='pubPerson')
    admin=Column(Boolean,default=False)

    canPub = db.Column(db.Boolean, default=False, nullable=False)#可以发布签到
    canEdit = db.Column(db.Boolean, default=False, nullable=False)#可以发布文章


    @property
    def password(self):
        return self.password_hash

    # 装饰器装饰后，可以像调用属性一样调用password

    @password.setter
    def password(self, raw):
        self.password_hash = generate_password_hash(raw)  # 密码加密
    # 装饰器装饰后，可以像设置属性一样调用password

    def validate_password(self,password):
        return check_password_hash(self.password,password)

    def increase_pubCount(self):
        self.pubCount+=1

    def increase_signInCount(self):
        self.signInCount+=1

    def get_id(self):
        #覆盖父类的id
        try:
            return text_type(self.userid)
        except AttributeError:
            raise NotImplementedError('`get_id`error')

    def can(self,permission_name):
        #判断是否有权限
        permission=Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and \
            permission in self.role.permissions
