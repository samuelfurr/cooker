from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

cooker = Flask(__name__)
cooker.config.from_object(Config)
db = MongoEngine(cooker)
login = LoginManager(cooker)
login.login_view = 'login'
bootstrap = Bootstrap(cooker)

from cooker import routes, models, errors
