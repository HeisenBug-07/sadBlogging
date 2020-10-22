import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gfhdlrghgg65454augyglhygfrtyougb'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'user.login'

from project.user.view import userBlueprint
from project.post.view import postBlueprint
from project.error_pages.handlers import error_pages

app.register_blueprint(userBlueprint)
app.register_blueprint(postBlueprint)
app.register_blueprint(error_pages)
