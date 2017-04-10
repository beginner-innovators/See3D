import os

from secret_key import key

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = key
