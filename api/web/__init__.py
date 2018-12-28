from flask import Blueprint

from api.web.admin import admin
from api.web.article import article
from api.web.auth import auth


def create_blueprint_web():
    bp_web=Blueprint('web',__name__,template_folder='templates',static_folder='static')
    auth.register(bp_web,url_prefix='/auth')
    admin.register(bp_web,url_prefix='/admin')
    article.register(bp_web,url_prefix='/art')
    return bp_web