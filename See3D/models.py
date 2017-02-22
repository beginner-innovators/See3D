from See3D import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    creator = db.Column(db.Boolean, default=False)

    id_token = db.Column(db.Text)        # Taken from 'sub' field of Google ID Token

    def __init__(self, username, creator, id_token):
        self.username = username
        self.creator = creator

        self.id_token = id_token

    def __repr__(self):
        return '<User {}>'.format(self.username)
