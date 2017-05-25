from index import app ,session
from models import Users
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"

@login_manager.user_loader
def load_user(id):
    return session.query(Users).get(int(id))




