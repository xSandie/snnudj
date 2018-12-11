from api.libs.redprint import Redprint

auth = Redprint('auth')

@auth.route('/login',methods=['GET'])
def wx_login():
    #todo 微信登录逻辑
    pass

@auth.route('/register',methods=['POST'])
def user_register():
    #todo 微信小程序注册
    pass

@auth.route('/change',methods=['POST'])
def user_change():
    #todo 微信修改自己帐号密码
    pass