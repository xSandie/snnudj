# 文章相关发布 删除 查看详情 查看列表
from flask import make_response, render_template, request, session
from flask_login import current_user, login_required

from api.config.myConfig import PER_PAGE
from api.libs.redprint import Redprint
from api.models.Post import Post
from api.models.base import db

article=Redprint('article')

@article.route('/pub',methods=['POST'])
@login_required
def pub_article():
    req_args = request.json
    post_body=req_args.get('body')
    post_title=req_args.get('title')

    with db.auto_commit():
        post=Post()
        post.title=post_title
        post.body=post_body
        post.pubPersonId=current_user.userid
        db.session.add(post)

    return 'ok'



@article.route('/delete',methods=['POST'])
@login_required
def delete_article():
    req_args = request.json
    postId = int(req_args.get('postId'))
    page = int(req_args.get('page'))

    with db.auto_commit():
        post_to_del = Post.query.get(postId)
        post_to_del.status=0#删除状态
    response = make_response('ok')
    return response

@article.route('/list',methods=['GET'])
def list_article():
    # 文章列表
    page=request.args.get('page',1,type=int)
    pagination=Post.query.filter_by(status=1).order_by(Post.create_time.desc()).paginate(page,per_page=PER_PAGE)#分页对象
    posts=pagination.items#当前页数的记录列表

    return render_template('articleList.html',pagination=pagination,posts=posts)

@article.route('/detail',methods=['GET'])
def article_detail():
    post_id=int(request.args.get('Id'))
    post=Post.query.get(post_id)

    return render_template('articleDetail.html',post=post)

@article.route('/edit',methods=['GET'])
@login_required
def edit_article():
    return render_template('pubArticles.html')
