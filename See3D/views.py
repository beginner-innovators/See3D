import json

import httplib2
import flask
from flask_login import login_required, login_user, logout_user
from oauth2client import client

from See3D import app, db, login_manager
from See3D.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index/')
def index():
    return flask.render_template('index.html')

@app.route('/about/')
@login_required
def about():
    return flask.render_template('about.html', title="About")

@app.route('/gallery/')
def gallery():
    requests = []

    requests.append({
        "id": 5738493,
        "title": "Castle",
        "description": "A small, basic castle would do just fine.",
        "user": {"email":"jbr101@gmail.com"}
    })

    requests.append({
        "id": 2023423,
        "title": "House",
        "description": "Make it the largest mansion you've ever felt.",
        "user": {"email":"aubrymanson@yahoo.com"}
    })

    return flask.render_template('gallery.html', title="Gallery", requests=requests)

@app.route('/requests/<request_id>/')
def request(request_id):
    return "Request {}".format(request_id)

@app.route('/submit/')
@login_required
def submit():
    return "This is where users will submit requests."

@app.route('/profile/')
@login_required
def profile():
    return flask.render_template('profile.html', title="Profile")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        '../client_secrets.json',
        scope='email profile',
        redirect_uri=flask.url_for('oauth2callback', _external=True),
    )
    flow.params['include_granted_scopes'] = "true"

    # Redirect user to Google sign-in.
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)

    # Upon callback, obtain the user's credentials.
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)

        user_info = json.loads(credentials.to_json())

        sub = user_info["id_token"]["sub"]        # Primary identification of Google account
        user = User.query.filter_by(sub=sub).first()

        # Add user to database if not already there.
        if not user:
            email = user_info["id_token"]["email"]
            user = User(email=email, creator=False, sub=sub)

            db.session.add(user)
            db.session.commit()

        login_user(user, remember=True)
        return flask.redirect(flask.url_for('index'))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect('index')
