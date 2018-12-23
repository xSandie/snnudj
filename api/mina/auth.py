from flask import request, jsonify

from api.libs.redprint import Redprint
from api.libs.wxcode import wx_decode
from api.models.User import User

from api.models.base import db

auth = Redprint('auth')

@auth.route('/login',methods=['GET'])
def wx_login():
    #todo 微信登录逻辑
    req_arg = request.args
    code = req_arg['code']
    userId = wx_decode(code)

    if userId:
        user=User.query.filter_by(wxopenId=userId).first()
        if user is None:
            #todo 用户不存在新建用户
            with db.auto_commit():
                user=User()
                user.wxopenId=userId
            return_dict={
                'userId':user.wxopenId
            }
    return jsonify(return_dict)

@auth.route('/register',methods=['POST'])
def user_register():
    #todo 微信小程序注册
    pass

@auth.route('/change',methods=['POST'])
def user_change():
    #todo 微信修改自己帐号密码
    pass