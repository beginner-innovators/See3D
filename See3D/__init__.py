from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'oauth2callback'

# Import views at end to avoid a circular reference
from . import views
