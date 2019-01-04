from flask import request, make_response, redirect, url_for, render_template
from flask_login import login_user, current_user, login_required, logout_user

from api.libs.redprint import Redprint
# 用户登录注销，与修改自己账号密码逻辑
from api.models.User import User
from api.models.base import db

auth=Redprint('auth')

@auth.route('/',methods=['GET'])
def login_index():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def web_login():
    # 网页的登录
    req_args=request.json
    password=str(req_args.get('password'))
    account=str(req_args.get('account'))

    user=User.query.filter_by(userPhone=account).first()
    try:
        if user.admin and user.validate_password(password):
            login_user(user,remember=True)
            response = make_response('ok')

        else:
            response = make_response('error')
            # 以下为打开跨站响应的代码
            response.headers['Access-Control-Allow-Origin'] = '*'
    except Exception as e:
        response = make_response('error')
        # 以下为打开跨站响应的代码
        response.headers['Access-Control-Allow-Origin'] = '*'

    return response



@auth.route('/logout',methods=['GET'])
@login_required
def web_logout():
    # 网页的注销
    logout_user()
    return redirect(url_for('web.list_article'))

@auth.route('/change',methods=['POST'])
@login_required
def web_changemyinfo():
    # 修改自己帐号密码逻辑
    req_args=request.json
    user_phone=req_args.get('userPhone')
    user_name=req_args.get('userName')
    new_password=req_args.get('userPassword')

    user_id=current_user.userid
    admin=User.query.get(user_id)

    with db.auto_commit():
        admin.password=new_password
        admin.userPhone=user_phone
        admin.username=user_name
    return 'ok'
