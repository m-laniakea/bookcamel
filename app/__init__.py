##
# App Initializer
# Prepare for launch
##

from flask import Flask 
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from cfg import cfg

login_manager = LoginManager()
db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

login_manager.session_protection = 'strong'

##
# Database popoulation for dev mode
##
def db_init(app):
    with app.app_context():

        try:
            db.create_all()
            print('Database initiation: \033[92mSuccess.\033[0m')
        except:
            print('Database initiation: \033[91mFailed.\033[0m')


def db_populate(app):
    with app.app_context():
        from models import User

        try:
            User.populate()
            print('Database population: \033[92mSuccess.\033[0m')
        except:
            print('Database: \033[93mAlready Populated.\033[0m')


def create_app(name):
    app = Flask(__name__)
    app.config.from_object(cfg[name])

    cfg[name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)

    # Initialize database
    db_init(app)

    if 'dev' == name or 'default' == name:
        db_populate(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    ##
    # Prepare blueprint for use in main/__init__.py
    ##
    from .main import main as template
    app.register_blueprint(template)

    return app
