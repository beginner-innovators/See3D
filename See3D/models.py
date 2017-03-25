from See3D import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sub = db.Column(db.Text)        # Taken from 'sub' field of Google ID Token
    is_creator = db.Column(db.Boolean, default=False)
    
    creation_date = db.Column(db.DateTime)
    email = db.Column(db.String(254))

    requests = db.relationship('Request', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(16))
    description = db.Column(db.String(64))
    
    creation_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Request {} - {}>'.format(self.id, self.title)
