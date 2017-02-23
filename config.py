import os
from client_info import client_id, client_secret, key

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

GOOGLE_LOGIN_CLIENT_ID = client_id
GOOGLE_LOGIN_CLIENT_SECRET = client_secret

SECRET_KEY = key

OAUTH_CREDENTIALS = {
    'google': {
        'id': client_id,
        'secret': client_secret
    }
}
