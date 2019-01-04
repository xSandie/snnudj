#todo 网页管理员查看，创建与删除逻辑
from flask import request, render_template
from flask_login import login_required, current_user

from api.libs.redprint import Redprint
from api.models.Roles import Roles
from api.models.User import User
from api.models.base import db

admin=Redprint('admin')

@admin.route('/all',methods=['GET'])
@login_required
def see_all_admin():
    # 查看所有管理员逻辑
    users=User.query.filter(User.admin==True,User.userid!=current_user.userid).all()
    return render_template('adminInterface.html',admin=current_user,users=users)#正好看下current_user会不会变

@admin.route('/create',methods=['POST'])
@login_required
def create_admin():
    #todo 创建管理员逻辑
    req_args=request.json
    user_phone=req_args.get('userPhone')
    user_name=req_args.get('userName','')
    user_password=req_args.get('userPassword','')

    new_admin=User.query.filter_by(userPhone=user_phone).first()

    if new_admin is None:
        # 用户不存在，不允许创建
        with db.auto_commit():
            new_admin.username=user_name
            new_admin.password=user_password
            new_admin.admin=True
            new_admin.roleId=Roles.Moderator




    pass

@admin.route('/delete',methods=['POST'])
@login_required
def delete_admin():
    # 删除管理员逻辑
    user_phone=request.json.get('userPhone')

    admin_to_delete=User.query.filter_by(userPhone=user_phone).first()

    with db.auto_commit():
        admin_to_delete.roleId=Roles.User
        admin_to_delete.admin=False

    return 'ok'

@admin.route('/giveup',methods=['POST'])
@login_required
def giveup_admin():
    # 放弃管理
    user_id=int(current_user.userid)
    admin_to_giveup = User.query.get(user_id)
    if admin.roleId!=Roles.Administrator:
        with db.auto_commit():
            admin_to_giveup.roleId=Roles.User
            admin_to_giveup.admin=False
        return 'ok'
    else:
        return 'error'