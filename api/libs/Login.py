from flask_login import LoginManager

login_manager=LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from api.models.User import User
    user = User.query.get(int(user_id))
    return user
#默认使用session中存储的user_id来加载用户current_user

login_manager.login_view = 'web.web_login'