from api.libs.redprint import Redprint

sug=Redprint('sug')

@sug.route('/pub',methods=['POST'])
def suggestion_pub():
    #todo 发布建议
    pass

@sug.route('/reply',methods=['POST'])
def suggestion_reply():
    #todo 回复建议
    pass

@sug.route('/all',methods=['GET'])
def suggestion_all():
    #todo 查看所有建议
    pass
