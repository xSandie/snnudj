from api.libs.redprint import Redprint

signIn=Redprint('signIn')

#todo 创建 查看 和 签到

@signIn.route('/pub',methods=['POST'])
def pub_signIn():
    #todo 发布签到
    pass

@signIn.route('/In',methods=['POST'])
def sign_In():
    #todo 点击签到
    pass

@signIn.route('/pubDetail',methods=['GET'])
def sign_detail():
    #todo 发布者查看签到进度
    pass

@signIn.route('/fin',methods=['POST'])
def fin_sign():
    #todo 发布人结束签到
    pass

@signIn.route('/tempOpen',methods=['POST'])
def temp_open_sign():
    #todo 临时开启签到10分钟
    pass
