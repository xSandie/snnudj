from flask import Blueprint

from api.mina.auth import auth
from api.mina.createsome import create
from api.mina.signIn import signIn
from api.mina.suggestion import sug


def create_blueprint_mina():
    bp_mina=Blueprint('mina',__name__)
    auth.register(bp_mina,url_prefix='/auth')
    sug.register(bp_mina,url_prefix='/sug')
    signIn.register(bp_mina,url_prefix='/sign')
    create.register(bp_mina)
    return bp_mina