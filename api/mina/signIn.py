import datetime

from flask import request, abort, jsonify
from sqlalchemy import and_, desc

from api.config.myConfig import NET_PREFIX, PAGE_SIZE
from api.libs.QRCode import get_QRCode
from api.libs.redprint import Redprint
from api.models.SignInOrder import SignInOrder
from api.models.SignInPeople import SignInPeople
from api.models.User import User
from api.models.base import db

signIn=Redprint('signIn')

# 创建 查看 和 签到
@signIn.route('/finlist',methods=['GET'])
def fin_signIn_list():
    #获取已完成签到
    req_arg = request.args
    userId = int(req_arg['userId'])
    next_Page=int(req_arg['nextPage'])

    mypub_fin_orders = db.session.query(SignInOrder).filter(
        and_(SignInOrder.signInStatus==0, SignInOrder.pubPersonId==userId)).order_by(
        desc("id")).limit(PAGE_SIZE).offset((next_Page - 1) * PAGE_SIZE)

    myjoin_as_signInPeople = db.session.query(SignInPeople).join(SignInOrder).filter(
        and_(SignInOrder.signInStatus==0,SignInPeople.userId==userId)).order_by(
        desc("id")).limit(PAGE_SIZE).offset((next_Page - 1) * PAGE_SIZE)
    myjoin_fin_signIn_orders=[joined_signIn.signInOrder for joined_signIn in myjoin_as_signInPeople]

    finPubAct_toreturn=compose_signIn_finPubAct(mypub_fin_orders)
    finJoinAct_toreturn=compose_signIn_finJoinAct(myjoin_fin_signIn_orders,userId)

    return jsonify({
        'finJoinedAct':finJoinAct_toreturn,
        'finPubAct':finPubAct_toreturn
    })


@signIn.route('/ongolist',methods=['GET'])
def ongo_signIn_list():
    #获取未完成签到
    req_arg = request.args
    userId = int(req_arg['userId'])

    mypub_ongo_orders = db.session.query(SignInOrder).filter(
        and_(SignInOrder.signInStatus==1, SignInOrder.pubPersonId==userId)).order_by(
        desc("id")).all()

    myjoin_as_signInPeople = db.session.query(SignInPeople).join(SignInOrder).filter(
        and_(SignInOrder.signInStatus ==1,SignInPeople.userId==userId)).order_by(
        desc("id")).all()
    myjoin_fin_signIn_orders=[joined_signIn.signInOrder for joined_signIn in myjoin_as_signInPeople]

    ongoJoinAct_toreturn=compose_signIn_ongoJoinAct(myjoin_fin_signIn_orders,userId)

    ongoPubAct_toreturn=compose_signIn_ongoPubAct(mypub_ongo_orders)

    return jsonify({
        'joinedAct':ongoJoinAct_toreturn,
        'pubAct':ongoPubAct_toreturn
    })

@signIn.route('/pub',methods=['POST'])
def pub_signIn():
    #发布签到

    req_args = request.json
    userId=int(req_args.get('userId'))
    peopleNum=req_args.get('peopleNum')
    endDateTime=req_args.get('endDateTime')

    datetime_shift=datetime.datetime.strptime(endDateTime, "%Y-%m-%d %H:%M")

    user=User.query.get(userId)
    with db.auto_commit():
        sign_in_order=SignInOrder()
        sign_in_order.pubPersonId=user.userid
        sign_in_order.pubPerson=user
        sign_in_order.needtoSignIn=int(peopleNum)
        sign_in_order.endTime=datetime_shift
        sign_in_order.pubTime=sign_in_order.generate_pubTime()
        db.session.add(sign_in_order)

    code_local_url=get_QRCode(sign_in_order)
    if code_local_url:
        with db.auto_commit():
            sign_in_order.qrcodeUrl=code_local_url

        code_net_url=NET_PREFIX+code_local_url

        with db.auto_commit():
            user.increase_pubCount()

        return_dict={
            'CodeURl':code_net_url,
            'createTime':sign_in_order.pubTime.strftime("%Y-%m-%d %H:%M"),
            'signInId':sign_in_order.id
        }
    else:
        abort(500)

    return jsonify(return_dict)

@signIn.route('/In',methods=['POST'])
def sign_In():
    #点击签到
    req_args = request.json

    userId=int(req_args.get('userId'))
    signIn_Id=int(req_args.get('signInId'))

    signIn_order=SignInOrder.query.get(signIn_Id)
    user=User.query.get(userId)
    if signIn_order.signInStatus==1:
        with db.auto_commit():
            people_to_sign=SignInPeople()
            people_to_sign.signInOrder=signIn_order
            people_to_sign.signInOrderId=signIn_order.id#有改动
            people_to_sign.userId=user.userid
            people_to_sign.username=user.username
            people_to_sign.userPhone=user.userPhone
            people_to_sign.signInTime=people_to_sign.generate_signInTime()
            db.session.add(people_to_sign)
            signIn_order.haveSignIn += 1
            # 加入已签到人列表
        with db.auto_commit():
            signIn_order.signInPerson.append(people_to_sign)

        with db.auto_commit():
            user.increase_signInCount()

        return jsonify({'status':'ok'})

@signIn.route('/pubDetail',methods=['GET'])
def sign_detail():
    #发布者查看签到进度
    req_arg = request.args
    userId=int(req_arg['userId'])
    signIn_id=int(req_arg['signInId'])

    signIn_order=SignInOrder.query.get(signIn_id)
    user=User.query.get(userId)
    all_signIn=list(compose_signIn_people(signIn_order))
    if user.userid==signIn_order.pubPersonId:
        return_dict={
            'signInPeople':all_signIn,
            'username':signIn_order.pubPerson.username,
            'userPhone':signIn_order.pubPerson.userPhone,
            'createTime':str(signIn_order.pubTime.strftime("%Y-%m-%d %H:%M")),
            'processing':True if signIn_order.signInStatus==1 else False,
            'endTime':str(signIn_order.endTime.strftime("%Y-%m-%d %H:%M")),
            'haveSignIn':signIn_order.haveSignIn,
            'needSignIn':signIn_order.needtoSignIn,
            'qrCode':NET_PREFIX+signIn_order.qrcodeUrl
        }
    else:
        abort(404)
    return jsonify(return_dict)

@signIn.route('/fin',methods=['POST'])
def fin_sign():
    #发布人结束签到
    req_args = request.json
    userId = int(req_args.get('userId'))
    signIn_Id = int(req_args.get('signInId'))
    signIn_order=SignInOrder.query.get(signIn_Id)
    if userId==signIn_order.pubPersonId:
        now = datetime.datetime.now()
        with db.auto_commit():
            signIn_order.signInStatus=0
            signIn_order.endTime=now
        return jsonify({'status':'ok'})
    else:
        abort(403)

@signIn.route('/tempOpen',methods=['POST'])
def temp_open_sign():
    #临时开启签到10分钟
    req_args = request.json
    userId = int(req_args.get('userId'))
    signIn_Id =int(req_args.get('signInId'))
    now= datetime.datetime.now()
    next_time = now + datetime.timedelta(minutes=10)
    signIn_order=SignInOrder.query.get(signIn_Id)
    if signIn_order.pubPersonId==userId:
        with db.auto_commit():
            signIn_order.signInStatus=1
            signIn_order.endTime=next_time

        return jsonify({'status':'ok'})
    else:
        abort(403)

@signIn.route('/pubgetagain',methods=['GET'])
def signIn_pubgetagain():
    #发布页面刷新
    req_args = request.args
    userId = int(req_args.get('userId'))
    signIn_Id = int(req_args.get('signInId'))
    signIn_order = SignInOrder.query.get(signIn_Id)

    if userId==signIn_order.pubPersonId:
        return_dict={
            'CodeURl':NET_PREFIX+signIn_order.qrcodeUrl,
            'createTime':str(signIn_order.pubTime.strftime("%Y-%m-%d %H:%M"))
        }
    else:
        abort(404)
    return jsonify(return_dict)

@signIn.route('/Detail',methods=['GET'])
def get_signIn_detail():
    #签到人查看详情
    req_args = request.args
    userId = int(req_args.get('userId'))
    signIn_Id = int(req_args.get('signInId'))
    signIn_order = SignInOrder.query.get(signIn_Id)
    if userId!=signIn_order.pubPersonId:
        can_SignIn=True if SignInPeople.query.filter_by(userId=userId,signInOrderId=signIn_Id).first() is None else False
        user=User.query.get(userId)
        return_dict={
            'pubuserPhone':signIn_order.pubPerson.userPhone,
            'pubuserName':signIn_order.pubPerson.username,
            'endTime':str(signIn_order.endTime.strftime("%Y-%m-%d %H:%M")),
            'signInNum':signIn_order.haveSignIn,
            'canSignIn':can_SignIn,
            'myName':user.username
        }
    else:
        abort(403)
    return jsonify(return_dict)

def compose_signIn_people(signIn_order):
    people_list=[]
    for people in signIn_order.signInPerson:
        people_list.append({
            'signInTime':people.signInTime.strftime("%H:%M"),
            'username':people.username,
            'userPhone':people.userPhone
        })
    return people_list

def compose_signIn_finPubAct(orders):
    finPubAct_list=[]
    for order in orders:
        finPubAct_list.append({
            'pubTime':str(order.pubTime.strftime("%m-%d %H:%M")),
            'haveSignIn':order.haveSignIn,
            'needSignIn':order.needtoSignIn,
            'endTime':str(order.endTime.strftime("%m-%d %H:%M")),
            'signInId':order.id
        })
    return finPubAct_list

def compose_signIn_ongoPubAct(orders):
    ongoPubAct_list=[]
    now=datetime.datetime.now()
    for order in orders:
        urgent = True if order.endTime < now+datetime.timedelta(minutes=10) else False
        ongoPubAct_list.append({
            'pubTime':str(order.pubTime.strftime("%m-%d %H:%M")),
            'haveSignIn':order.haveSignIn,
            'needSignIn':order.needtoSignIn,
            'urgent':urgent,
            'endTime':str(order.endTime.strftime("%m-%d %H:%M")),
            'signInId':order.id
        })
    return ongoPubAct_list

def compose_signIn_finJoinAct(orders,userId):
    finJoinAct_list=[]
    for order in orders:
        finJoinAct_list.append({
            'pubPhoneNum':order.pubPerson.userPhone,
            'pubName':order.pubPerson.username,
            'signInTotal':order.haveSignIn,
            'signInTime':[people.signInTime.strftime("%H:%M")
                          for people in order.signInPerson if people.userId==userId][0],
            'endTime':str(order.endTime.strftime("%m-%d %H:%M")),
            'signInId':order.id
        })
    return finJoinAct_list

def compose_signIn_ongoJoinAct(orders,userId):
    ongoJoinAct_list = []
    for order in orders:
        ongoJoinAct_list.append({
            'pubPhoneNum':order.pubPerson.userPhone,
            'pubName':order.pubPerson.username,
            'signInTotal':order.haveSignIn,
            'signInTime':[people.signInTime.strftime("%H:%M")
                          for people in order.signInPerson if people.userId==userId][0],
            'endTime':str(order.endTime.strftime("%m-%d %H:%M")),
            'signInId':order.id
        })
    return ongoJoinAct_list