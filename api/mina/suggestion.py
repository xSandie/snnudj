from flask import request, jsonify, abort
from sqlalchemy import and_, desc

from api.config.myConfig import PAGE_SIZE
from api.libs.redprint import Redprint
from api.models.Reply import Reply
from api.models.Suggestions import Suggestions
from api.models.User import User
from api.models.base import db

sug=Redprint('sug')

@sug.route('/pub',methods=['POST'])
def suggestion_pub():
    #发布建议
    req_args = request.json
    userId = int(req_args.get('userId'))
    content = req_args.get('content')
    title = req_args.get('title')

    user=User.query.get(userId)

    with db.auto_commit():
        suggestion=Suggestions()
        suggestion.content=content
        suggestion.title=title
        suggestion.pubPerson=user
        suggestion.sugPubPersonId=user.userid
        db.session.add(suggestion)

    return jsonify({'status':'ok'})


@sug.route('/reply',methods=['POST'])
def suggestion_reply():
    #回复建议
    req_args = request.json
    userId = int(req_args.get('userId'))
    content = req_args.get('content')
    sug_Id = int(req_args.get('sugId'))

    admin=User.query.get(userId)
    suggestion=Suggestions.query.get(sug_Id)

    if admin.admin:
        with db.auto_commit():
            reply=Reply()
            reply.content=content
            reply.suggestion=suggestion
            reply.replyPerson=admin
            reply.replyPersonId=admin.userid
            reply.suggestionId=suggestion.id
            db.session.add(reply)
        with db.auto_commit():
            suggestion.sugStatus=Suggestions.HAVEREPLY
            suggestion.reply = reply
            admin.myReplySuggestions.append(reply)


        return jsonify({'status':'ok'})
    else:
        abort(403)

@sug.route('/all',methods=['GET'])
def suggestion_all():
    #查看所有建议
    req_args = request.args
    userId = int(req_args.get('userId'))
    nextPage = int(req_args.get('nextPage'))
    # sug_Id = int(req_args.get('sugId'))
    suggestions_toreturn = []
    user=User.query.get(userId)
    if user:
        suggestions_all=db.session.query(Suggestions).filter(Suggestions.sugStatus!=Suggestions.IGNORE).order_by(desc("id")).limit(PAGE_SIZE).offset((nextPage - 1) * PAGE_SIZE)
        for suggestion in suggestions_all:
            if suggestion.reply is None:
                suggestions_toreturn.append({
                    'sugId':suggestion.id,
                    'sugTitle':suggestion.title,
                    'sugContent':suggestion.content
                })
            else:
                suggestions_toreturn.append({
                    'sugId':suggestion.id,
                    'sugTitle':suggestion.title,
                    'sugContent':suggestion.content,
                    'reply':[suggestion.reply.replyPerson.username,suggestion.reply.content]
                })
        return jsonify({
            'suggestions':suggestions_toreturn
        })
    else:
        abort(403)

@sug.route('/igonore',methods=['POST'])
def suggestion_ignore():
    req_args = request.json
    userId = int(req_args.get('userId'))
    sug_id=int(req_args.get('sugId'))

    suggestion=Suggestions.query.get(sug_id)
    admin=User.query.get(userId)
    if admin.admin:
        with db.auto_commit():
            suggestion.sugStatus=Suggestions.IGNORE
        return jsonify({'status':'ignore'})
    else:
        abort(403)

@sug.route('/igonorelist',methods=['GET'])
def suggestion_ignorelist():
    req_args = request.args
    userId = int(req_args.get('userId'))
    nextPage = int(req_args.get('nextPage'))
    suggestions_toreturn = []
    user=User.query.get(userId)
    if user:
        suggestions_all=db.session.query(Suggestions).filter(Suggestions.sugStatus==Suggestions.IGNORE).order_by(desc("id")).limit(PAGE_SIZE).offset((nextPage - 1) * PAGE_SIZE)
        for suggestion in suggestions_all:
            suggestions_toreturn.append({
                'sugId':suggestion.id,
                'sugTitle':suggestion.title,
                'sugContent':suggestion.content
            })
        return jsonify({
            'ignoreSug':suggestions_toreturn
        })
    else:
        abort(403)