from See3D import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(254))
    creator = db.Column(db.Boolean, default=False)

    sub = db.Column(db.Text)        # Taken from 'sub' field of Google ID Token

    def __init__(self, username, email, creator, sub):
        self.username = username
        self.email = email
        self.creator = creator

        self.sub = sub

    def __repr__(self):
        return '<User {}>'.format(self.email)

