# __init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login_manager = LoginManager()

app = Flask(__name__)
Bootstrap(app)
with open('key_secret.txt', 'r') as read_file:
    key = read_file.read()
app.config['SECRET_KEY'] = key
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'




