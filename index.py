from flask import Flask ,Markup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  sqlalchemy.sql.expression import func
from werkzeug.security import generate_password_hash,check_password_hash
import traceback
import mistune
from flask import render_template, request, redirect, url_for, Markup , flash
from models import Users
from flask_login import LoginManager


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://m4bulmagd:123@localhost/personalblog'
app.secret_key="dsfaskjgjfdhjkl"
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
session = Session()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_get"

@login_manager.user_loader
def load_user(id):
    return session.query(Users).get(int(id))

from views import *

if __name__ == '__main__':
    app.run(port=8000)