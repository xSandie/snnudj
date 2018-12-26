import time

from flask import request, jsonify, abort

from api.libs.redprint import Redprint
from api.libs.wxcode import wx_decode
from api.models.User import User

from api.models.base import db
import datetime

auth = Redprint('auth')

@auth.route('/login',methods=['GET'])
def wx_login():
    #微信登录逻辑
    req_arg = request.args
    code = req_arg['code']
    openId = wx_decode(code)

    if openId:
        user=User.query.filter_by(wxopenId=openId).first()
        if user is None:
            #用户不存在新建用户
            with db.auto_commit():
                user=User()
                user.wxopenId=openId
                db.session.add(user)
            return_dict={
                'openId':user.wxopenId,
                'userId':user.userid
            }
        else:
            #用户存在返回相关信息,三元表达式确定有无注册
            today = datetime.datetime.now()
            tomorrow = today + datetime.timedelta(days=1)
            endday=today+datetime.timedelta(days=60)
            return_dict={
                'openId':user.wxopenId,
                'userId':user.userid,
                'admin':user.admin,
                'username':user.username if user.username else '',
                'userPhone':user.userPhone if user.userPhone else False,
                'date':str(tomorrow.date()),
                'startDate':str(today.date()),
                'endDate':str(endday.date())
            }
    else:
        abort(404)

    return jsonify(return_dict)

@auth.route('/register',methods=['POST'])
def user_register():
    #   微信小程序注册\修改
    req_args = request.json

    userId=req_args.get('userId')
    password=req_args.get('password')
    userName=req_args.get('userName')
    userPhone=req_args.get('userPhone')

    user=User.query.filter_by(userid=int(userId)).first()
    if user:
        with db.auto_commit():
            user.password=password
            user.userPhone=userPhone
            user.username=userName
    else:
        abort(404)

    return jsonify({'status':'changed'})

@auth.route('/getUser',methods=['GET'])
def user_info():
    req_arg = request.args
    userId=int(req_arg['userId'])

    user=User.query.get(userId)
    createTimeArray=time.localtime(user.create_time)
    createTime=time.strftime("%Y-%m-%d %H:%M", createTimeArray)
    return_dict={
        'username':user.username,
        'userPhone':user.userPhone,
        'userCreateTime':createTime,
        'totalJoin':user.signInCount,
        'totalPub':user.pubCount
    }
    return jsonify(return_dict)