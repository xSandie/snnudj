#todo 文章相关发布 删除 查看详情 查看列表
from api.libs.redprint import Redprint

article=Redprint('article')

@article.route('/pub',methods=['POST'])
def pub_article():
    pass

@article.route('/delete',methods=['POST'])
def delete_article():
    pass

@article.route('/list',methods=['GET'])
def list_article():
    #todo 文章列表
    pass

@article.route('/detail',methods=['GET'])
def article_detail():
    pass
