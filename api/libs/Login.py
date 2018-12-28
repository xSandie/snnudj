from flask_login import LoginManager

login_manager=LoginManager()

@login_manager.user_loader
def load_user(user_phone):
    from api.models.User import User
    user = User.query.get(user_phone)
    return user