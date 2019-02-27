#todo 网页管理员查看，创建与删除逻辑
from flask import request, render_template, redirect, url_for
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
    if current_user.can('CREATEOTHER'):
        users=User.query.filter(User.admin==True,User.userid!=current_user.userid).all()
        return render_template('adminInterface.html',admin=current_user,users=users)#正好看下current_user会不会变
    else:
        return redirect(url_for('web.list_article'))

@admin.route('/create',methods=['POST'])
@login_required
def create_admin():
    #创建管理员逻辑
    req_args=request.json
    user_phone=req_args.get('userPhone')
    user_name=req_args.get('userName','')
    user_password=req_args.get('userPassword','')
    user_canPub=req_args.get('canPub',False)
    user_canEdit=req_args.get('canEdit',False)

    new_admin=User.query.filter_by(userPhone=user_phone).first()
    if new_admin is None:
        #用户不存在不允许创建
        return 'error'
    if user_password=='' and user_name=='':
        # 未设置新密码,新名字
        with db.auto_commit():
            # new_admin.username=user_name
            new_admin.admin=True
            new_admin.roleId=Roles.Moderator
            new_admin.canPub = user_canPub
            new_admin.canEdit = user_canEdit
    elif user_name=='':
        #未设置新名字
        with db.auto_commit():
            new_admin.admin = True
            new_admin.roleId = Roles.Moderator
            new_admin.password=user_password
            new_admin.canPub = user_canPub
            new_admin.canEdit = user_canEdit
    else:
        #未设置密码
        with db.auto_commit():
            new_admin.admin = True
            new_admin.roleId = Roles.Moderator
            new_admin.username = user_name
            new_admin.canPub = user_canPub
            new_admin.canEdit = user_canEdit
    return 'ok'



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
    if admin_to_giveup.roleId!=Roles.Administrator:
        with db.auto_commit():
            admin_to_giveup.roleId=Roles.User
            admin_to_giveup.admin=False
        return 'ok'
    else:
        return 'error'