from flask import request, make_response, redirect, url_for, render_template
from flask_login import login_user

from api.libs.redprint import Redprint
#todo 用户登录注销，与修改自己账号密码逻辑
from api.models.User import User

auth=Redprint('auth')

@auth.route('/',methods=['GET'])
def login_index():
    return render_template('login.html')

@auth.route('/login',methods=['POST'])
def web_login():
    #todo 网页的登录
    req_args=request.json
    password=str(req_args.get('password'))
    account=str(req_args.get('account'))

    user=User.query.filter_by(userPhone=account).first()
    if user.admin and user.validate_password(password):
        login_user(user)
        redirect(url_for('web.list_article'))
    else:
        response = make_response('error')
        # 以下为打开跨站响应的代码
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response





@auth.route('/logout',methods=['POST'])
def web_register():
    #todo 网页的注销
    pass

@auth.route('/change',methods=['POST'])
def web_changeuser():
    #todo 修改自己帐号密码逻辑
    pass
