from api.libs.redprint import Redprint
#todo 用户登录注销，与修改自己账号密码逻辑

auth=Redprint('auth')

@auth.route('/login',methods=['POST'])
def web_login():
    #todo 网页的登录
    pass

@auth.route('/logout',methods=['POST'])
def web_register():
    #todo 网页的注销
    pass

@auth.route('/change',methods=['POST'])
def web_changeuser():
    #todo 修改自己帐号密码逻辑
    pass
