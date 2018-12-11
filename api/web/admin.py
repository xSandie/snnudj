#todo 网页管理员查看，创建与删除逻辑
from api.libs.redprint import Redprint

admin=Redprint('admin')

@admin.route('/all',methods=['GET'])
def see_all_admin():
    #todo 查看所有管理员逻辑
    pass

@admin.route('/create',methods=['POST'])
def create_admin():
    #todo 创建管理员逻辑
    pass

@admin.route('/delete',methods=['POST'])
def delete_admin():
    #todo 删除管理员逻辑
    pass

@admin.route('/giveup',methods=['POST'])
def giveup_admin():
    #todo 放弃管理
    pass