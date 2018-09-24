from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login'

from app import routes
from app import routes_chart
from app import models
from app import errors

if not app.debug:
    if not os.path.exists(app.config['LOG_DIR']):
        os.mkdir(app.config['LOG_DIR'])
    file_handler = RotatingFileHandler(app.config['LOG_DIR'] +"/"+ app.config['LOG_NAME'], maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask Web Application Startup')
