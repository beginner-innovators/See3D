import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# This is a bad idea. Do not use this during production. Restarting the server will destroy all sessions.
SECRET_KEY = os.urandom(50)
